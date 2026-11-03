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
- Windows scheduled tasks: always create via `wall-e schedule install` (XML); plain `schtasks /Create` tasks won't run on battery.
- Friday health reports catalogue drift (108 on disk vs 100 indexed on 2026-10-02); `friday doctor` self-heals it. That edits the user's vault index, so left to the user.
- Docker Desktop is often not running; Wall-E then reports the sandbox image as "unknown".

## Queue (after the user's hands-on phase)
1. Fix whatever the user finds while using/breaking it (top priority).
2. Disk: ~9% free; Wall-E flags it every report. User's call on Downloads/temp.
3. Done 2026-09-23 (after handover): Friday MCP `content_ideas`/`content_calendar` + Jarvis routing (verified `jarvis do` plans both); num_ctx sizing in every Ollama client (Jarvis, Friday, Alfred, Ultron; Vision's prompt is only the user's short description). Live A/B: an oversized prompt at default ctx kept 2050/9037 tokens and lost its instruction; sized ctx kept all and obeyed.
3b. Done 2026-10-02 (found by the real Sunday 2026-09-28 run): both weekly tasks had failed with 0x800710E0 (schtasks defaults: no start on battery, no catch-up). `wall-e schedule install` now registers from XML (battery OK, StartWhenAvailable, 30 min limit); re-registered and verified Last Result 0. Scheduled report had also timed out collecting health: Friday `--health` lingered ~20s (thread-pool workers joined at exit; Ollama probe loaded the 7b model) -> daemon threads + /api/tags check (~5s); `jarvis health` checks agents in parallel. Report filename uses local date; health line lists real agent names. Scheduled report re-run: 6/6 healthy.
3c. Done 2026-11-03 (from a month of unattended runs):
   - `friday github` died 3 Sundays running (0xC000013A: catch-up console window closed). Jobs now run windowless via `pythonw -m walle.runjob` (CREATE_NO_WINDOW), logging to ~/.walle/jobs/<job>.log; the report flags failed/stale (>8 days) runs. Verified Last Result 0 for both.
   - 2026-11-01 report timed out collecting health at a busy logon catch-up: Wall-E timeout 30s -> 120s.
   - `jarvis daily` always showed Wall-E status "unknown": reader expected `overall_status:`, Wall-E writes `status:` (test fixture invented the same wrong key). Fixed + reasons included.
   - PRIVACY GAP: `jarvis do`, MCP `run` and MCP `agent_tool` never wrote the audit log (2 rows after weeks of use), so Wall-E's privacy audit was blind to them. All paths now audit allowed + refused; tests use a per-test JARVIS_DB_PATH. Verified live.
   - Cross-agent contract tests in 10x/tests/test_contracts.py (writer -> reader for Wall-E/Alfred/Ultron/Friday/Jarvis audit; shared constants). Run `python -m pytest -q tests` in 10x after changing any agent's vault output.
   - Planner drops optional booleans the request doesn't name; `mcp` capped `<3` everywhere; `wall-e cleanup` shows Docker's 18 GB virtual disk (never shrinks by itself).
4. Disk now 6.1% free (28 GB). Biggest reclaimable: Downloads 18.5 GB (Kali VM archives 7.3 GB), Docker virtual disk 18.3 GB (prune + compact; rebuild `ultron sandbox build`), Windows temp 4.2 GB. All the user's call.
5. Blocked on user: see PROJECT_CONTEXT.md section 8 (cloud keys, admin installs, Phases 1/3, MCP registration, renaming 10x-ecosystem).
