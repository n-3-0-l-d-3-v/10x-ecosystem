"""One-command setup: clone every agent, install it, pull local models, health-check.

    python bootstrap/bootstrap.py [--root DIR] [--only a,b] [--dry-run] [--skip-models]
                                  [--vault DIR] [--set-env]
    python bootstrap/bootstrap.py --update [--root DIR] [--only a,b]

--vault DIR installs the LifeOS template into DIR (existing files are kept)
and makes DIR the shared VAULT_PATH. --set-env persists VAULT_PATH,
JAVA_HOME and GHIDRA_INSTALL_DIR for the current user (setx / ~/.profile).
--update pulls each existing clone, reinstalls and runs its tests; on failure
the clone is rolled back to its previous commit (dirty clones are skipped).

Idempotent: existing clones are pulled, not re-cloned. Needs git, python, pip;
Ollama optional (models are skipped with a note if it is missing).
"""
from __future__ import annotations

import argparse
import os
import shlex
import shutil
import subprocess
import sys
from pathlib import Path

import yaml

MANIFEST = Path(__file__).with_name("agents.yaml")


def load_manifest(path: Path = MANIFEST) -> dict:
    data = yaml.safe_load(path.read_text(encoding="utf-8"))
    for a in data["agents"]:
        for k in ("name", "repo", "install", "health"):
            if k not in a:
                raise ValueError(f"agent entry missing '{k}': {a}")
    return data


def plan(data: dict, root: Path, only: list[str] | None = None, skip_models: bool = False) -> list[tuple[str, list[str], Path | None]]:
    """Ordered (label, argv, cwd) steps. Pure function, no side effects."""
    steps: list[tuple[str, list[str], Path | None]] = []
    for a in data["agents"]:
        if only and a["name"] not in only:
            continue
        dest = root / a["name"]
        if dest.exists():
            steps.append((f"{a['name']}: update", ["git", "pull", "--ff-only"], dest))
        else:
            steps.append((f"{a['name']}: clone", ["git", "clone", "--branch", a.get("branch", "main"), f"https://github.com/{a['repo']}.git", str(dest)], None))
        work = dest / a.get("workdir", ".")
        steps.append((f"{a['name']}: install", [sys.executable, "-m", *shlex.split(a["install"])], work))
    if not skip_models:
        for m in data.get("models", []):
            steps.append((f"model: {m}", ["ollama", "pull", m], None))
    for a in data["agents"]:
        if only and a["name"] not in only:
            continue
        steps.append((f"{a['name']}: health", shlex.split(a["health"]), dest_for(root, a)))
    return steps


def dest_for(root: Path, a: dict) -> Path:
    return root / a["name"] / a.get("workdir", ".")


DEFAULT_TEST = "python -m pytest -q -x -p no:cacheprovider"


def _git(args: list[str], cwd: Path, run=subprocess.run):
    return run(["git", *args], cwd=cwd, capture_output=True, text=True)


def safe_update(a: dict, root: Path, run=subprocess.run) -> str:
    """Pull one agent, reinstall, run its tests; if they fail, roll the local
    branch back to where it was and reinstall that. Never touches a dirty
    tree or the remote, so the worst case is "stayed on the old version"."""
    repo = root / a["name"]
    work = repo / a.get("workdir", ".")
    if not (repo / ".git").exists():
        return "not cloned (run bootstrap without --update first)"
    if _git(["status", "--porcelain"], repo, run).stdout.strip():
        return "skipped: uncommitted changes"
    old = _git(["rev-parse", "HEAD"], repo, run).stdout.strip()
    pull = _git(["pull", "--ff-only", "-q"], repo, run)
    if pull.returncode != 0:
        return f"pull failed, unchanged: {(pull.stderr or pull.stdout).strip()[:120]}"
    new = _git(["rev-parse", "HEAD"], repo, run).stdout.strip()
    if new == old:
        return "up to date"
    install = [sys.executable, "-m", *shlex.split(a["install"])]
    test = shlex.split(a.get("test", DEFAULT_TEST))
    if test[0] == "python":
        test[0] = sys.executable
    ok = run(install, cwd=work, capture_output=True, text=True).returncode == 0
    if ok:
        ok = run(test, cwd=work, capture_output=True, text=True).returncode == 0
    if ok:
        return f"updated {old[:7]} -> {new[:7]}, tests pass"
    _git(["reset", "--hard", "-q", old], repo, run)
    run(install, cwd=work, capture_output=True, text=True)
    return f"ROLLED BACK to {old[:7]}: {new[:7]} failed install/tests (will retry next update)"


def setup_env(vault: str | None, set_env: bool, dry_run: bool) -> bool:
    """Vault template + env vars. Returns True on failure."""
    import envsetup

    if vault:
        dest = Path(os.path.expanduser(vault))
        if dry_run:
            print(f"==> vault: would install LifeOS template into {dest} (existing files kept)")
        else:
            copied, kept = envsetup.install_template(dest)
            print(f"==> vault: {len(copied)} template file(s) copied into {dest}, {len(kept)} existing kept")
    if set_env:
        todo = envsetup.pending(envsetup.detect(vault))
        if not todo:
            print("==> env: VAULT_PATH/JAVA_HOME/GHIDRA_INSTALL_DIR already set (or not found)")
        for k, v in todo.items():
            print(f"==> env: {'would set' if dry_run else 'set'} {k}={v}")
        if todo and not dry_run:
            try:
                envsetup.persist(todo)
            except RuntimeError as exc:
                print(f"    FAILED: {exc}")
                return True
            print("    open a new terminal for the variables to take effect")
    return False


def main(argv: list[str] | None = None) -> int:
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--root")
    p.add_argument("--only")
    p.add_argument("--dry-run", action="store_true")
    p.add_argument("--skip-models", action="store_true")
    p.add_argument("--vault", help="Vault folder: install the LifeOS template there, use it as VAULT_PATH.")
    p.add_argument("--set-env", action="store_true", help="Persist VAULT_PATH/JAVA_HOME/GHIDRA_INSTALL_DIR (user scope).")
    p.add_argument("--update", action="store_true", help="Pull + test each clone; roll back any that fail.")
    args = p.parse_args(argv)
    if args.vault or args.set_env:
        if setup_env(args.vault, args.set_env, args.dry_run):
            return 1
    data = load_manifest()
    root = Path(os.path.expanduser(args.root or data["root_default"]))
    only = args.only.split(",") if args.only else None
    if args.update:
        bad = 0
        for a in data["agents"]:
            if only and a["name"] not in only:
                continue
            result = "would pull, test, roll back on failure" if args.dry_run else safe_update(a, root)
            bad += result.startswith(("ROLLED BACK", "pull failed"))
            print(f"==> {a['name']}: {result}")
        return 1 if bad else 0
    steps = plan(data, root, only, args.skip_models)
    if not args.dry_run:
        root.mkdir(parents=True, exist_ok=True)
    failures = []
    for label, cmd, cwd in steps:
        print(f"==> {label}: {' '.join(cmd)}")
        if args.dry_run:
            continue
        if cmd[0] == "ollama" and not shutil.which("ollama"):
            print("    skipped: ollama not installed (https://ollama.com/download)")
            continue
        r = subprocess.run(cmd, cwd=cwd if cwd and cwd.exists() else None, capture_output=True, text=True)
        if r.returncode != 0:
            failures.append(label)
            print(f"    FAILED ({r.returncode}): {(r.stderr or r.stdout).strip().splitlines()[-1:]}")
    print(f"\n{len(steps)} steps, {len(failures)} failed" + (f": {failures}" if failures else ""))
    return 1 if failures else 0


if __name__ == "__main__":
    sys.exit(main())
