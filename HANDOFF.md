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

## Done since last handoff
Vision MCP server (Jarvis dispatches to it); Ghidra 11.4.3 + Ultron real analysis verified; shared vault=devNote (agents/<Name>/); bootstrap script; Wall-E `schedule` (weekly task installed: WallE-WeeklyReport, Sun 09:00); Phase 2 LifeOS template (vault/Home.md, System/Templates, plugin list) also copied into devNote (uncommitted there); `friday github [--readme]` stats + profile README.

## Also done
`friday draft <platform> <note>` (local 7b, draft-only, thin-source guard + invented-number flag); `friday portfolio` (static page); `jarvis listen` (offline faster-whisper STT + SAPI TTS, verified round-trip); agent `description` fields in jarvis/agents.yaml drive routing; `jarvis daily` includes vault data; `ultron sandbox build|analyze` (network-less Docker; Dockerfile NOT yet built - Docker Desktop was still starting). App installs via winget: Obsidian+Zen done; Krita errored; Blender/OBS/Inkscape/Audacity/Ardour in queue (log: %TEMP%/install2.log).
Gotcha: this tool layer un-escapes backslashes in commands; in python edits use chr(92) or avoid backslash literals.

`jarvis do "<sentence>" [--dry-run]`: local qwen2.5:7b plans ONE tool call (validated against real MCP schema) then executes; verified live (TARS scaffold, Vision list, Friday capture). `wall-e focus on|off` (power saver + unload models, restores plan). `ultron sandbox build|analyze` VERIFIED: image ultron-sandbox (JDK21+Ghidra 11.4.3), no network (DNS fails), same 115 artifacts/35 claims as host; found+fixed a py3.14 argparse `%` help bug. Docker Desktop is up.

## Latest
Alfred system-design mentor (`sd_list/sd_hint/sd_review` MCP tools; 6 scenarios; reveal gate). Ultron sandbox image verified. Wall-E now checks all 6 sibling repos; its Sunday task really ran (report in devNote/agents/Wall-E) and flagged: Friday `--health` ~9s (jarvis health timeout raised to 30s) and DISK ~9.5% free (models ~7GB + Docker image 1.8GB) - free space soon. All repos' tests are hermetic to the global VAULT_PATH.

## Also done (queue items 2-4)
`vision open <project> [--app] [--dry-run]` launches Audacity/OBS/etc by project type (verified dry-run). Friday `--health` probes providers in parallel, 5s cap. Wall-E report lists `Reason:` lines and flags low disk (<10% or <20GB); cleaned pip+Docker build cache (disk now ~92% used; user's Downloads is 18GB - user's call). Gemini key in Friday fails (`response.text` empty) - check key/quota.
App installs: Obsidian, Zen, OBS, Audacity OK. Krita/Blender/Inkscape failed under UAC (machine-wide MSI cancelled); retrying with `--scope user` (log %TEMP%/install3.log).

## Also done (round 3)
Portable Blender 5.2.1 + Krita 6.0.4 in ~/tools (winget per-user installers don't exist; machine-wide MSI needs UAC). Inkscape/Ardour still missing (no non-admin path). Vision launcher finds them. `bootstrap/prereqs.py [--install]` checks git/python/ollama/java/docker/Ghidra11. CI (pytest, py3.12) added to jarvis, wall-e, tars, vision (verified all pass in clean python:3.12 containers first); check `gh run list -R n-3-0-l-d-3-v/<repo>`. Friday has no CI yet (2-min suite; needs requirements.txt) - add after verifying in a container.

## CI (all 7 repos green as of 2026-09-20)
jarvis/wall-e/tars/vision/friday: pytest py3.12 (each verified in clean python:3.12 containers first). ultron: README test-count check needs updating whenever tests are added (`# N tests` line ~329). alfred: apps/api/pytest.ini sets pythonpath; TARS tests need git identity env (conftest). Lesson: verify in a clean container BEFORE pushing CI.

## Latest (2026-09-23)
Alfred now has a free local-model backend (`llm_backend=auto` prefers Ollama qwen2.5:7b; `off` in tests) for personalized nudges (still AC-gated) and `explain` (vault-aware: ranked whole-word retrieval over devNote, citations filtered to real notes). `jarvis ask "explain X"` -> Alfred explain_concept. README rewritten with commands + test counts (1,710 total).

## Done (2026-09-23 burst)
Friday local Ollama provider (fallback always; `FRIDAY_AI_PRIMARY=ollama` to go local-first) + offline whisper fallback. `jarvis do` multi-step cross-agent (<=3 steps, schema-forced JSON, per-step schema+tier validation, confirm, {{prev}}, invented optional args dropped) + `jarvis tools [--refresh]` cache (~/.jarvis/tools.json). `vision diagram "<english or A -> B: label>"` -> tidy Excalidraw. `wall-e cleanup` (suggest-only). A demo note "Jarvis Multi Step Planning" was captured into devNote (12-ai-ml/planning) during a live test - harmless, user may delete.
Gotcha: gate commits with `pytest && git commit` (one broken Vision commit landed before a fix).

## Queue (do in order)
1. Alfred `quiz`: questions generated from the user's own vault notes on a topic, answers graded locally, results written as spaced-repetition due dates (agents/Alfred).
2. Jarvis as an MCP server (`jarvis mcp`): one server exposing do/ask/route/health so any MCP client (Claude Code, etc.) gets the whole gauntlet.
3. Wall-E weekly report: include cleanup summary when disk is low.
4. `jarvis listen` -> `do` path (voice into multi-step plans).
5. Blocked on user: cloud-fallback keys; Inkscape/Ardour admin; Phases 1/3.
