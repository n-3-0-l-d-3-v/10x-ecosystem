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

## Queue (do in order)
1. Confirm install3 results (Krita/Blender/Inkscape/Ardour); if a user-scope install fails, use portable zips. 2. Look into Friday's Gemini failure. 3. Cloud fallback blocked on user's free-tier Groq/OpenRouter keys. 4. Phases 1/3 Linux/Zen config deferred by user. 5. New ideas: Alfred vault-aware explanations, Ultron eval suite in CI, bootstrap: add Ghidra/Ollama/JDK steps.
