"""Check (and optionally install) the tools the agents rely on.

    python bootstrap/prereqs.py            # report only
    python bootstrap/prereqs.py --install  # winget-install what is missing (Windows)

Ghidra is fetched from GitHub releases into ~/tools and GHIDRA_INSTALL_DIR is
printed (11.x is required: Ultron's export script is Jython, removed in 12).
"""
from __future__ import annotations

import argparse
import json
import os
import shutil
import subprocess
import sys
import urllib.request
import zipfile
from pathlib import Path

TOOLS = Path.home() / "tools"
GHIDRA_TAG = "Ghidra_11.4.3_build"
CHECKS = {
    "git": (["git"], None),
    "python": ([sys.executable], None),
    "ollama": (["ollama"], "Ollama.Ollama"),
    "java": (["java"], "EclipseAdoptium.Temurin.21.JDK"),
    "docker": (["docker"], "Docker.DockerDesktop"),
}


def have(cmds: list[str]) -> bool:
    if cmds[0] == "java" and os.environ.get("JAVA_HOME"):
        if (Path(os.environ["JAVA_HOME"]) / "bin" / ("java.exe" if os.name == "nt" else "java")).exists():
            return True
    return bool(shutil.which(cmds[0]) or Path(cmds[0]).exists())


def ghidra_dir() -> Path | None:
    env = os.environ.get("GHIDRA_INSTALL_DIR")
    if env and Path(env).exists():
        return Path(env)
    found = sorted(TOOLS.glob("ghidra_11*_PUBLIC")) if TOOLS.exists() else []
    return found[-1] if found else None


def report() -> dict[str, bool]:
    status = {name: have(cmds) for name, (cmds, _) in CHECKS.items()}
    status["ghidra"] = ghidra_dir() is not None
    return status


def install_ghidra() -> Path:
    api = f"https://api.github.com/repos/NationalSecurityAgency/ghidra/releases/tags/{GHIDRA_TAG}"
    with urllib.request.urlopen(api, timeout=30) as r:
        asset = next(a for a in json.load(r)["assets"] if a["name"].endswith(".zip"))
    TOOLS.mkdir(parents=True, exist_ok=True)
    zpath = TOOLS / asset["name"]
    urllib.request.urlretrieve(asset["browser_download_url"], zpath)
    with zipfile.ZipFile(zpath) as z:
        z.extractall(TOOLS)
    zpath.unlink()
    return ghidra_dir()  # type: ignore[return-value]


def main(argv: list[str] | None = None) -> int:
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--install", action="store_true", help="install what is missing")
    args = p.parse_args(argv)
    status = report()
    for name, ok in status.items():
        print(f"{'OK     ' if ok else 'MISSING'} {name}")
    if args.install:
        for name, ok in status.items():
            if ok:
                continue
            winget_id = CHECKS.get(name, (None, None))[1]
            if winget_id and shutil.which("winget"):
                print(f"==> winget install {winget_id}")
                subprocess.run(["winget", "install", "--id", winget_id, "-e", "--silent",
                                "--accept-package-agreements", "--accept-source-agreements"])
            elif name == "ghidra":
                print(f"==> Ghidra installed at {install_ghidra()}; set GHIDRA_INSTALL_DIR to that path")
    return 0 if all(status.values()) else 1


if __name__ == "__main__":
    sys.exit(main())
