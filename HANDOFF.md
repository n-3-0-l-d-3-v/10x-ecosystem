# HANDOFF — live state + queue. Read PROJECT_CONTEXT.md first for the full picture.

## Rules (user-set, durable)
- Autonomous: keep working through tickets/phases; ask only on real design ambiguity.
- No `Co-Authored-By: Claude` trailers; never rewrite old history. No subagents. Quiet tool output (`-q`, `| tail`). One docs commit per milestone.
- Free/local-first only. Sensitive data never leaves machine (see docs/omniroute-privacy-spec.md).

## State (2026-09-23): FIRST COMPLETE BUILD DRAFT, handed to the user
7 agents + umbrella, all pushed, CI green, 1,819 agent tests (+14 umbrella). Phase now: **user learns, uses and breaks it**; next work comes from their findings.
Current command surface per agent: `docs/repo-map.md`. How to try everything: README "The agents" table.

## Done in the final build burst (2026-09-23)
- TARS `guard install|scan|uninstall` + MCP `guard_scan`: pre-commit hook scans the staged index for secrets/.env/key files; fails closed; `tars:allow` / `.tars-guard-allow`. Installed in all 8 repos (not devNote: user's vault, their call). Ultron has a `.tars-guard-allow` for its deliberate fake-secret fixtures.
- Friday `ideas` (weekly post ideas grounded in the window's notes, invented sources/rehashes dropped, thin weeks refused; `--draft N`), `calendar [--write]` (Socials/ by publish_on/status), YouTube notes get a collapsed clickable-timestamp transcript and no longer dump transcript into "My Notes".
- Wall-E `schedule --job all|report|github` (new task `Friday-WeeklyGitHub`, Sun 09:15, verified by a manual run: result 0) and a setup-drift section in `report` (models, sandbox image, schedules, guard hooks; unknown when a daemon is down).
- bootstrap: `--vault DIR` (LifeOS template, never overwrites), `--set-env` (setx / ~/.profile, only changed values), `--update` (pull, reinstall, test, roll back failing clones; dirty clones skipped). docs/repo-map.md rewritten.

## Gotchas
- Bash tool PATH is stale for new installs: call `~/AppData/Local/Programs/Ollama/ollama.exe` by full path.
- Running `python -m tars...` from `Desktop/Neil` fails (the `tars/` folder shadows the package); use the `tars` command.
- The tool layer un-escapes backslashes in heredoc python (`"\n"` -> real newline); use Edit/Write for those.
- `pip install -e` from a temp clone repoints console scripts; reinstall from Desktop/Neil/<name> after.
- Friday tests are slow (~2 min). Ultron README has a CI-checked test count line; update when adding tests.
- Gate commits: `pytest && git commit`. The tars-guard hook now also runs on every commit in these repos.
- Docker Desktop is often not running; Wall-E then reports the sandbox image as "unknown".

## Queue (after the user's hands-on phase)
1. Fix whatever the user finds while using/breaking it (top priority).
2. Disk: ~9% free; Wall-E flags it every report. User's call on Downloads/temp.
3. Optional: Friday MCP tools for `ideas`/`calendar`; Jarvis routing phrases for them.
4. Context-window hardening (started): Ollama defaults to num_ctx 4096 and silently drops the START of an overflowing prompt. Done: Jarvis `ollama_client.context_options` (grows num_ctx only when needed), `friday ideas` listing budget. Still to do: same guard in Friday `ai.py`/`drafts.py`, Alfred `mentor/llm.py`, Vision `diagram.py`, Ultron `agents/backend.py` (measure with `prompt_eval_count`).
5. Blocked on user: see PROJECT_CONTEXT.md section 8 (cloud keys, admin installs, Phases 1/3, MCP registration, renaming 10x-ecosystem).
