import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "bootstrap"))
import bootstrap as b  # noqa: E402


def test_manifest_has_all_seven_agents():
    names = [a["name"] for a in b.load_manifest()["agents"]]
    assert names == ["friday", "ultron", "alfred", "jarvis", "wall-e", "tars", "vision"]


def test_plan_clones_when_missing_and_pulls_when_present(tmp_path):
    data = b.load_manifest()
    steps = b.plan(data, tmp_path, only=["tars"], skip_models=True)
    assert steps[0][1][:2] == ["git", "clone"]
    (tmp_path / "tars").mkdir()
    assert b.plan(data, tmp_path, only=["tars"], skip_models=True)[0][1][:2] == ["git", "pull"]


def test_alfred_installs_from_apps_api(tmp_path):
    steps = b.plan(b.load_manifest(), tmp_path, only=["alfred"], skip_models=True)
    install = [s for s in steps if s[0] == "alfred: install"][0]
    assert install[2] == tmp_path / "alfred" / "apps/api"


def test_dry_run_touches_nothing(tmp_path, capsys):
    assert b.main(["--root", str(tmp_path / "x"), "--dry-run", "--skip-models"]) == 0
    assert not (tmp_path / "x").exists()


def test_prereqs_report_shape():
    import prereqs

    s = prereqs.report()
    assert {"git", "python", "ollama", "java", "docker", "ghidra"} <= set(s) and s["git"] and s["python"]


# --- env + vault setup -------------------------------------------------------

import envsetup  # noqa: E402


def test_detect_prefers_env_then_tools_and_resolves_vault(tmp_path):
    (tmp_path / "jdk-17.0.1").mkdir()
    (tmp_path / "jdk-21.0.5+11").mkdir()
    (tmp_path / "ghidra_11.4.3_PUBLIC").mkdir()
    got = envsetup.detect(str(tmp_path / "v"), tools=tmp_path, env={})
    assert got["JAVA_HOME"].endswith("jdk-21.0.5+11") and got["GHIDRA_INSTALL_DIR"].endswith("ghidra_11.4.3_PUBLIC")
    assert got["VAULT_PATH"] == str((tmp_path / "v").resolve())
    assert envsetup.detect(None, tools=tmp_path, env={"JAVA_HOME": "J"})["JAVA_HOME"] == "J"
    assert envsetup.detect(None, tools=tmp_path / "none", env={}) == {}


def test_pending_skips_values_already_set():
    assert envsetup.pending({"A": "1", "B": "2"}, env={"A": "1", "B": "x"}) == {"B": "2"}


def test_profile_block_is_idempotent_and_replaces_in_place():
    once = envsetup.profile_block({"A": "1"}, "alias ll='ls -l'\n")
    twice = envsetup.profile_block({"A": "2"}, once)
    assert twice.count(envsetup.PROFILE_BEGIN) == 1 and 'export A="2"' in twice and "alias ll" in twice


def test_persist_windows_uses_setx_and_raises_on_failure(monkeypatch):
    monkeypatch.setattr(envsetup.os, "name", "nt")
    calls = []

    class R:
        def __init__(self, rc): self.returncode, self.stderr, self.stdout = rc, "denied", ""
    envsetup.persist({"VAULT_PATH": "C:/v"}, run=lambda a, **k: calls.append(a) or R(0))
    assert calls == [["setx", "VAULT_PATH", "C:/v"]]
    import pytest
    with pytest.raises(RuntimeError):
        envsetup.persist({"X": "1"}, run=lambda a, **k: R(1))


def test_persist_posix_merges_block(monkeypatch, tmp_path):
    monkeypatch.setattr(envsetup.os, "name", "posix")
    prof = tmp_path / ".profile"
    envsetup.persist({"A": "1"}, profile=prof)
    envsetup.persist({"B": "2"}, profile=prof)
    text = prof.read_text()
    assert 'export A="1"' in text and 'export B="2"' in text and text.count(envsetup.PROFILE_BEGIN) == 1


def test_install_template_never_overwrites(tmp_path):
    dest = tmp_path / "vault"
    (dest).mkdir()
    (dest / "Home.md").write_text("mine")
    copied, kept = envsetup.install_template(dest)
    assert "Home.md" in kept and (dest / "Home.md").read_text() == "mine"
    assert "System/Templates/daily.md" in copied and (dest / "Daily").is_dir()
    assert envsetup.install_template(dest)[0] == []


def test_main_vault_dry_run_writes_nothing(tmp_path):
    assert b.main(["--root", str(tmp_path / "x"), "--dry-run", "--skip-models", "--vault", str(tmp_path / "v"), "--set-env"]) == 0
    assert not (tmp_path / "v").exists()


# --- safe update -------------------------------------------------------------

import subprocess  # noqa: E402


def _g(cwd, *args):
    subprocess.run(["git", *args], cwd=cwd, check=True, capture_output=True,
                   env={**__import__("os").environ, "GIT_AUTHOR_NAME": "t", "GIT_AUTHOR_EMAIL": "t@t",
                        "GIT_COMMITTER_NAME": "t", "GIT_COMMITTER_EMAIL": "t@t"})


def _setup(tmp_path):
    origin = tmp_path / "origin"
    origin.mkdir()
    _g(origin, "init", "-q", "-b", "main")
    (origin / "check.py").write_text("import sys; sys.exit(0)\n")
    _g(origin, "add", "-A")
    _g(origin, "commit", "-q", "-m", "ok")
    root = tmp_path / "root"
    root.mkdir()
    _g(root, "clone", "-q", str(origin), "agent")
    agent = {"name": "agent", "install": "pip --version", "test": "python check.py"}
    return origin, root, agent


def _push(origin, code, msg):
    (origin / "check.py").write_text(code)
    _g(origin, "commit", "-q", "-am", msg)


def _head(repo):
    return subprocess.run(["git", "rev-parse", "HEAD"], cwd=repo, capture_output=True, text=True).stdout.strip()


def test_update_keeps_passing_change_and_rolls_back_failing_one(tmp_path):
    origin, root, agent = _setup(tmp_path)
    assert b.safe_update(agent, root) == "up to date"
    _push(origin, "import sys; sys.exit(0)  # v2\n", "v2")
    assert b.safe_update(agent, root).startswith("updated")
    good = _head(root / "agent")
    _push(origin, "import sys; sys.exit(1)\n", "broken")
    assert b.safe_update(agent, root).startswith("ROLLED BACK")
    assert _head(root / "agent") == good


def test_update_skips_dirty_and_uncloned(tmp_path):
    origin, root, agent = _setup(tmp_path)
    (root / "agent" / "wip.txt").write_text("mine")
    assert b.safe_update(agent, root).startswith("skipped")
    assert b.safe_update({**agent, "name": "nope"}, root).startswith("not cloned")
