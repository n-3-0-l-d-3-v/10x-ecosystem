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
