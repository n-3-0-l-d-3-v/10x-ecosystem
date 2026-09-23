"""Environment + vault setup for bootstrap.py.

* Detects JAVA_HOME / GHIDRA_INSTALL_DIR (existing env var, else the
  portable installs prereqs.py puts in ~/tools) and VAULT_PATH (--vault).
* Persists them for the user only, no admin: `setx` on Windows, an
  idempotent marked block in ~/.profile elsewhere. A variable that
  already has the wanted value is left alone.
* Installs the LifeOS vault template (10x/vault) into a vault folder
  without ever overwriting a file that is already there.
"""
from __future__ import annotations

import os
import re
import shutil
import subprocess
from pathlib import Path

TEMPLATE = Path(__file__).resolve().parents[1] / "vault"
PROFILE_BEGIN = "# >>> 10x env >>>"
PROFILE_END = "# <<< 10x env <<<"


def _newest(parent: Path, pattern: str) -> Path | None:
    hits = sorted(p for p in parent.glob(pattern) if p.is_dir()) if parent.is_dir() else []
    return hits[-1] if hits else None


def detect(vault: str | None = None, tools: Path | None = None, env: dict | None = None) -> dict[str, str]:
    """Wanted values; a key is omitted when nothing sensible was found."""
    env = os.environ if env is None else env
    tools = tools or Path.home() / "tools"
    out: dict[str, str] = {}
    java = env.get("JAVA_HOME") or _newest(tools, "jdk-21*") or _newest(tools, "jdk-*")
    if java:
        out["JAVA_HOME"] = str(java)
    ghidra = env.get("GHIDRA_INSTALL_DIR") or _newest(tools, "ghidra_11*")
    if ghidra:
        out["GHIDRA_INSTALL_DIR"] = str(ghidra)
    v = vault or env.get("VAULT_PATH")
    if v:
        out["VAULT_PATH"] = str(Path(os.path.expanduser(v)).resolve())
    return out


def pending(wanted: dict[str, str], env: dict | None = None) -> dict[str, str]:
    env = os.environ if env is None else env
    return {k: v for k, v in wanted.items() if env.get(k) != v}


def profile_block(values: dict[str, str], existing: str) -> str:
    """~/.profile text with our marked block replaced (or appended)."""
    lines = [PROFILE_BEGIN] + [f'export {k}="{v}"' for k, v in sorted(values.items())] + [PROFILE_END]
    block = "\n".join(lines) + "\n"
    pat = re.compile(re.escape(PROFILE_BEGIN) + r".*?" + re.escape(PROFILE_END) + r"\n?", re.DOTALL)
    if pat.search(existing):
        return pat.sub(lambda _: block, existing)
    return existing + ("" if not existing or existing.endswith("\n") else "\n") + block


def persist(values: dict[str, str], *, run=subprocess.run, profile: Path | None = None) -> list[str]:
    """Persist for the current user. Returns one line per variable set."""
    done: list[str] = []
    if not values:
        return done
    if os.name == "nt":
        for k, v in values.items():
            r = run(["setx", k, v], capture_output=True, text=True)
            if r.returncode != 0:
                raise RuntimeError(f"setx {k} failed: {(r.stderr or r.stdout).strip()}")
            done.append(f"{k}={v}")
    else:
        profile = profile or Path.home() / ".profile"
        existing = profile.read_text(encoding="utf-8") if profile.exists() else ""
        m = re.search(re.escape(PROFILE_BEGIN) + r"(.*?)" + re.escape(PROFILE_END), existing, re.DOTALL)
        current = dict(re.findall(r'^export (\w+)="(.*)"$', m.group(1), re.M)) if m else {}
        profile.write_text(profile_block({**current, **values}, existing), encoding="utf-8")
        done += [f"{k}={v}" for k, v in values.items()]
    return done


def install_template(dest: Path, template: Path = TEMPLATE) -> tuple[list[str], list[str]]:
    """Copy the vault template into `dest`; existing files are kept. Returns (copied, kept)."""
    copied: list[str] = []
    kept: list[str] = []
    for src in sorted(template.rglob("*")):
        rel = src.relative_to(template)
        if "__pycache__" in rel.parts:
            continue
        target = dest / rel
        if src.is_dir():
            target.mkdir(parents=True, exist_ok=True)
        elif target.exists():
            kept.append(rel.as_posix())
        else:
            target.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(src, target)
            copied.append(rel.as_posix())
    return copied, kept
