"""One-command setup: clone every agent, install it, pull local models, health-check.

    python bootstrap/bootstrap.py [--root DIR] [--only a,b] [--dry-run] [--skip-models]

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


def main(argv: list[str] | None = None) -> int:
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--root")
    p.add_argument("--only")
    p.add_argument("--dry-run", action="store_true")
    p.add_argument("--skip-models", action="store_true")
    args = p.parse_args(argv)
    data = load_manifest()
    root = Path(os.path.expanduser(args.root or data["root_default"]))
    only = args.only.split(",") if args.only else None
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
