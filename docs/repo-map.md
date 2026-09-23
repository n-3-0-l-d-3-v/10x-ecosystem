# Repo Map

Two kinds of repo:

- **Isolated repos**: one per agent, installable and runnable standalone
  (github.com/n-3-0-l-d-3-v/&lt;name&gt;, local `Desktop/Neil/<name>/`).
- **This repo (10x-ecosystem)**: the umbrella. Vault template, cross-agent
  specs, phase tickets, the OmniRoute privacy spec, and `bootstrap/`, which
  clones the isolated repos by path (manifest `bootstrap/agents.yaml`, no
  submodules). It never vendors agent code.

Every agent follows the contract: `agent.yaml`, a `--health` JSON command,
and (except Wall-E) an MCP server. Jarvis's `jarvis/agents.yaml` wires them
together. CI (pytest, Python 3.12) runs on every agent repo.

## Agents (test counts as of 2026-09-23)

| Agent | Role | Tests | Main commands |
|---|---|---|---|
| **Jarvis** | Orchestrator | 129 | `ask`, `do` (1-3 step cross-agent plans), `route`, `tools`, `daily`, `listen [--do]`, `health`; MCP server `python -m jarvis.mcp_server` |
| **Friday** (was jarvisOS) | Knowledge capture, socials | 483 | `note`, `youtube`, `article`, `ask`, `search`, `wiki`, `review`, `ideas`, `draft`, `calendar`, `github`, `portfolio`, `lifeos`, `habit`; branch `feat/knowledge-os-v2` mirrored to `main` |
| **Alfred** (was LeetLearn) | Learning mentor | 581 py + 28 js | LeetCode hint ladder + AC gate, system-design mentor, `python -m alfred --explain` / `--quiz` (run from `apps/api`) |
| **Ultron** (was yugen) | RE / security | 391 | `analyze` (Ghidra 11.4.3 + binwalk evidence graph), `ask`, `map/reach/diff`, `sandbox build|analyze` (no-network Docker), `vault approve` |
| **TARS** | Code / build / git | 94 | `new`, `test`, `build`, `branch`, `commit`, `status`, `guard install|scan|uninstall` (pre-commit secret blocker); no push, by design |
| **Vision** | Creative | 83 | `new --type ...`, `open`, `diagram`, `excalidraw`, `assets`, `list` |
| **Wall-E** | Health / maintenance | 58 | `report`, `schedule [--job report|github]`, `focus on|off`, `cleanup` |
| **10x** | Umbrella | 14 | `bootstrap/prereqs.py`, `bootstrap/bootstrap.py [--vault DIR --set-env] [--update]` |

## Shared vault

`devNote` (private, github.com/n-3-0-l-d-3-v/devNote) is the one vault, pointed
to by `VAULT_PATH`. Agents write only under `agents/<Name>/` (plus Friday's
`Socials/` drafts and notes); Friday's reindex skips `agents/`; Alfred reads
everything. The LifeOS template lives in `vault/` here and is installed with
`bootstrap.py --vault DIR` (never overwrites existing files).

## Scheduled jobs (Windows Task Scheduler, via `wall-e schedule`)

- `WallE-WeeklyReport`: `wall-e report`, Sundays 09:00.
- `Friday-WeeklyGitHub`: `friday github` snapshot, Sundays 09:15.

## `alfredOS` folder

Not a repo: the old "Studio" architecture docs. Its ideas were folded into
`docs/agents/`; the naming was rejected in favour of the agent names above.
