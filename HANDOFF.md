# HANDOFF — read this first in any new session (keep it short, update at each milestone)

## Rules (user-set, durable)
- Autonomous: keep working through tickets/phases; ask only on real design ambiguity.
- No `Co-Authored-By: Claude` trailers; never rewrite old history. No subagents. Quiet tool output (`-q`, `| tail`). One docs commit per milestone.
- Free/local-first only. Sensitive data never leaves machine (see docs/omniroute-privacy-spec.md).

## State (2026-09-19)
7 agents built, pushed, tested: friday, ultron, alfred, jarvis, wall-e, tars, vision (github.com/n-3-0-l-d-3-v/<name>; local Desktop/Neil/<name>). `jarvis health` = all healthy.
- Jarvis: local Ollama classifier (qwen2.5:3b) + keyword fallback; MCP dispatch to all 5 MCP agents incl. Vision.
- Ollama installed (qwen2.5:3b/7b). Ghidra 11.4.3 in ~/tools (12.x drops Jython, Ultron's script needs it). User env: GHIDRA_INSTALL_DIR, JAVA_HOME=jdk-21, VAULT_PATH=devNote.
- Shared vault = devNote. Agents write `$VAULT_PATH/agents/<Name>/`; Friday reindex skips `agents/`; Alfred reads whole vault.
- Bootstrap: `python bootstrap/bootstrap.py [--dry-run --only x --skip-models]` (manifest bootstrap/agents.yaml), verified live.

## Gotchas
- Bash tool PATH is stale for new installs: call `~/AppData/Local/Programs/Ollama/ollama.exe` by full path.
- `pip install -e` from a temp clone repoints console scripts; reinstall from Desktop/Neil/<name> after.
- Friday tests are slow (~2 min); run in background. Ultron test_probe_* needs JAVA/GHIDRA env consistent.
- Old repos folder names renamed (reverse engineer→ultron, jarvisOS→friday, leetLearn→alfred).

## Queue (do in order)
1. Wall-E scheduling via Windows Task Scheduler (weekly report). 2. Phase 2: Obsidian LifeOS template in vault/ (dashboard, daily/weekly, streaks, media notes). 3. Phase 7: GitHub profile/portfolio pipeline (Friday+Vision). 4. Jarvis: default tools for more agents, voice (whisper.cpp) foundation. 5. Cloud fallback needs user's free-tier keys (blocked on user). 6. Phases 1/3 (Linux, Zen) deferred by user.
