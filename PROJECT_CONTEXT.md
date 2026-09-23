# PROJECT_CONTEXT — the whole 10x project, for a fresh session

Read this once at the start of a new chat. `HANDOFF.md` holds the short live
state and next-step queue; this file holds everything else: who the user is,
what they want, every decision made so far and why, how the machine is set up,
what each agent does, and the rules of working. Last updated 2026-09-23.

---

## 1. Who the user is and what they want

- CS student (GitHub `n-3-0-l-d-3-v`, email neilthomasmathew123@gmail.com),
  wants to be a "jack of all trades" across CS: dev, security/RE, AI, systems,
  networking, plus creative work (music production, design, video, photo,
  animation, game dev) and socials/presence (GitHub, LinkedIn, portfolio, blog).
- Goal: turn their laptop into a premium, aesthetic, efficient "Iron Man"
  setup: a gauntlet of specialized AI agents, one Obsidian brain, a polished
  desktop, all **completely free** (the self-imposed engineering challenge) and
  **local-first / private**. End state: the whole setup is a package anyone with
  similar hardware can reproduce with one or two commands.
- This is meant to be one of their best pieces of work. It is not a toy: it
  must be real, used daily, understood, then "broken" and refined repeatedly.
- **Build phase complete (first draft, 2026-09-23); now the user's hands-on phase.** During BUILD the rule was: The user is deliberately not interfering. The job is
  to keep building through tickets/phases autonomously at max quality and max
  token efficiency, stopping only for decisions that genuinely need a human.
  After the first complete build draft, the user steps in to learn it, use it,
  break it, and refine it.
- Original master plan: `C:\Users\Neil Thomas Mathew\Desktop\Neil\10x dev setup.txt`
  (10-layer architecture, agents, phases 0-9). `docs/phases/README.md` tracks
  the phases against reality.

## 2. Standing rules (user-set; follow exactly)

1. **Autonomous**: keep going ticket after ticket; do not ask for confirmation
   between tickets. Ask only on a real design ambiguity or anything that needs
   the user (keys, admin rights, account settings, publishing).
2. **No Claude co-author trailers** in commits or PRs, ever (also in the global
   `~/.claude/CLAUDE.md`). Never rewrite or force-push history to remove old
   trailers. Commit with
   `git -c user.email=neilthomasmathew123@gmail.com -c user.name="Neil Thomas Mathew" commit`.
3. **Token efficiency** (global CLAUDE.md): no subagents unless asked; quiet
   tool output (`-q`, `| tail`); don't re-read files already in context; batch
   independent calls; no narration; one docs update per milestone; keep
   sessions short and hand off via files.
4. **Free / open source only.** Local model first. Cloud only as an explicit,
   tier-checked fallback, and only with the user's own free-tier keys.
5. **Privacy**: private-tier data never touches a network (see §5).
6. **Agents propose, humans approve anything irreversible**: no agent pushes,
   publishes, posts, deletes, or approves its own findings. (I, the building
   assistant, do push code to the user's own repos as part of the build; that
   is established and fine.)
7. **Never fabricate user data**: don't tick habits, write fake notes, or post
   anything on the user's behalf. If a live test writes into the real vault,
   undo it (this happened once with a habit tick and was reverted).
8. **Quality gates**: run the repo's tests before every commit, gated with
   `&&` so a failure blocks the commit. Verify features live, not just with
   mocks. Report honestly what works and what doesn't.
9. Linux/Hyprland/Omarchy desktop, Zen browser config, and OS-level setup
   (Phases 1/3) are **deferred by the user** until the build is done. The
   machine is Windows 11 for now.

## 3. Key decisions and why

- **Agent names are Marvel/pop-culture** (user's choice): Jarvis, Friday, TARS,
  Ultron, Alfred, Wall-E, Vision. An earlier "Studio" naming (Baton/Canon/Tab...)
  from the user's old `alfredOS` design docs was rejected; its ideas were folded in.
- **Full conversion, not wrappers.** Three existing projects of the user's were
  converted in place into agents (renamed everywhere, all original requirements
  kept, ecosystem requirements added):
  - `jarvisOS` → **Friday** (knowledge capture). Jarvis name freed for the orchestrator.
  - `yugen` (formerly Aether / aether-platform, "reverse engineer" folder) → **Ultron**.
    Yugen was judged a serious standalone project; it became Ultron but keeps
    its evidence-first discipline and ADRs (0011 documents the rename).
  - `LeetLearn` → **Alfred** (learning mentor).
  GitHub repos and local folders were renamed to match.
- **Each agent is its own repo** (standalone-usable) + this umbrella repo
  `10x-ecosystem` (name is a placeholder; user rejected several suggestions and
  may rename later) holding docs, vault template, bootstrap.
- **Agent contract**: every agent has `agent.yaml` (name, role,
  default_sensitivity_tier, entrypoint, health_check_command, sandboxed,
  vault_write_path), a `--health` JSON command, and (except Wall-E) an MCP
  server. Jarvis's `jarvis/agents.yaml` is the registry wiring them together.
- **MCP everywhere**: Ultron keeps its hand-rolled stdio JSON-RPC server (its ADR
  forbids runtime deps) but it speaks the real protocol, so one standard MCP
  client in Jarvis talks to all agents.
- **Shared vault = the user's `devNote` repo** (private GitHub). `VAULT_PATH`
  points at it. Agents write only under `agents/<Name>/`; Friday's reindex
  skips `agents/`; Alfred reads the whole vault. Obsidian LifeOS files (Home.md
  dashboard, System/Templates, plugin list) were copied into devNote (the user
  has uncommitted edits there; don't commit devNote on their behalf).
- **Local models**: Ollama with `qwen2.5:3b` (routing/classification, fits 4 GB
  VRAM) and `qwen2.5:7b` (planning, explanations, drafts, quizzes). Structured
  output via Ollama `format` JSON schema wherever parsing matters.
- **Ghidra 11.4.3**, not 12.x (12 removed bundled Jython; Ultron's export script is Jython).
- **Design pattern for model features**: the model only proposes; code
  validates (schemas, grounding checks, citations filtered to real notes,
  invented optional args dropped, AC gate re-validation) and code does anything
  deterministic (e.g. diagram layout).

## 4. Machine and environment

- Windows 11, Intel i5-11400H, 32 GB RAM, RTX 3050 Laptop (~4 GB VRAM).
  Disk is low (~40 GB free of 452 GB). `wall-e cleanup` lists safe
  reclaims (19 GB Windows temp; Downloads 18 GB is the user's call).
- Repos: `C:\Users\Neil Thomas Mathew\Desktop\Neil\{10x,friday,ultron,alfred,jarvis,wall-e,tars,vision,devNote}`.
  Friday's working branch is `feat/knowledge-os-v2`; push it and also
  `feat/knowledge-os-v2:main`. Others use `main`; 10x uses `master`.
- User env vars set: `VAULT_PATH` (devNote), `GHIDRA_INSTALL_DIR`
  (`~/tools/ghidra_11.4.3_PUBLIC`), `JAVA_HOME` (`~/tools/jdk-21.0.5+11`).
- Installed: Ollama (winget; the Bash tool's PATH may be stale, so use
  `~/AppData/Local/Programs/Ollama/ollama.exe`), Docker Desktop (image
  `ultron-sandbox` built), Obsidian, Zen, OBS, Audacity, portable Blender 5.2.1 and
  Krita 6.0.4 in `~/tools`. Inkscape/Ardour are NOT installed (need admin/UAC).
  Godot via winget. faster-whisper for offline speech.
- Scheduled tasks: `WallE-WeeklyReport` (`wall-e report`, Sun 09:00) and
  `Friday-WeeklyGitHub` (`friday github`, Sun 09:15), managed by `wall-e schedule`.
- Friday's Gemini free quota is exhausted (429); Groq works; local Ollama is the
  always-on fallback.

## 5. Privacy model (docs/omniroute-privacy-spec.md)

Tiers: `private` (local only, fail closed) < `personal-token` (user's own keys)
< `work` < `public`. Jarvis computes a tier per request (agent floor from
agent.yaml, `vault/private/**` path override, fail-closed default) and refuses
dispatch on conflict; every decision is audit-logged (~/.jarvis/jarvis.db) and
Wall-E audits that log. Ultron hard-refuses non-local model hosts; Jarvis's
Ollama client has no remote-host path at all. `providers.yaml` lists which
providers are real (ollama-local) vs aspirational (shared free-tier pools: no
keys configured).

## 6. The agents: what exists now

Test counts are approximate as of 2026-09-23; CI (GitHub Actions) is green on all 7.

- **Jarvis** (orchestrator, ~129 tests): local-model intent classifier with
  keyword fallback; tier engine; MCP client; `jarvis ask` (default tools:
  Friday ask_knowledge_base, Alfred explain_concept); `jarvis do "<sentence>"`
  = 1-3 step cross-agent plan (schema-forced, each step validated + tier
  checked, confirmation before multi-step, `{{prev}}` chaining, ungrounded
  optional args dropped); `jarvis tools [--refresh]` (tool-spec cache
  ~/.jarvis/tools.json); `jarvis daily` (health + vault briefing); `jarvis listen
  [--do]` (offline STT + Windows TTS); `jarvis health`; **Jarvis MCP server**
  `python -m jarvis.mcp_server` (plan, run(confirm), route, agent_tool, health,
  daily). Not registered in the user's Claude config (their choice).
- **Friday** (knowledge, ~483 tests): capture/classify/format/save/push/link
  into devNote; wiki synthesis; MCP (18+ tools); providers Groq → Gemini →
  local Ollama (`FRIDAY_AI_PRIMARY=ollama` for local-first); offline whisper
  fallback; `friday github [--readme]`, `friday draft <linkedin|blog|devto|thread> <note>`
  (local 7b, draft-only, thin-source guard, invented-number flag),
  `friday portfolio` (static page), `friday lifeos` (create today's daily note
  from the vault template + streaks), `friday habit <name> [--undo]`; MCP
  `log_habit`, `today`. Note: an older `friday today` shows the daily log.
  `friday ideas` (weekly post ideas grounded in the window's notes),
  `friday calendar` (Socials/ content calendar); YouTube notes carry a
  collapsed clickable-timestamp transcript.
- **Alfred** (learning, ~582 tests, run from `apps/api`): LeetCode Socratic hint
  ladder + AC gate (no solution before you pass), personas, reviews, interview
  mode, browser extension; system-design mentor (6 scenarios, ladder, rubric,
  reveal gate; MCP sd_*); LLM backend `auto` = local Ollama first (free), paid
  Anthropic only if configured; `python -m alfred --explain "<concept>"`
  (vault-aware, cites your notes) and `--quiz "<topic>"` (questions only from
  your notes, local grading + key-term floor, SM-2-lite next_due into
  agents/Alfred); MCP explain_concept, quiz_start/answer/finish.
- **Ultron** (RE/security, ~391 tests): Ghidra + binwalk evidence graph,
  NL `ask`, map/reach/diff; `ultron sandbox build|analyze` (no network,
  read-only, caps dropped; verified); `analyze` writes a pending, claim-cited RE
  summary to the vault when VAULT_PATH is set; `ultron vault approve`.
- **TARS** (code, ~94 tests): `tars new <template> <name>` (python-cli,
  node-cli), `tars test|build` (language detection), branch/commit inside
  `TARS_ALLOWED_ROOTS`; deliberately no push. `tars guard install|scan|uninstall`
  (pre-commit secret blocker, installed in all 8 repos). MCP incl. `guard_scan`.
- **Vision** (creative, ~83 tests): `vision new <name> --type
  music|design|video|photo|writing|game [--private]`, `vision excalidraw`,
  `vision assets`, `vision list`, `vision open <project>` (launches the right
  installed app), `vision diagram "<english or A -> B: label>"` (local model
  extracts boxes/arrows; deterministic layered layout → valid Excalidraw). MCP.
- **Wall-E** (health, ~58 tests): `wall-e report` (agent health, privacy audit,
  contract compliance, disk/git hygiene, setup drift: models/sandbox image/
  schedules/guard hooks, reasons, cleanup suggestions when disk low) → vault;
  `wall-e schedule install|remove|status [--job all|report|github]`; `wall-e focus on|off`
  (power saver + unload models, restores plan); `wall-e cleanup` (suggest-only).
- **10x repo**: README (front door), HANDOFF.md (live state/queue),
  docs/agents, docs/phases, docs/repo-map.md (partly stale), docs/omniroute-privacy-spec.md,
  vault/ (LifeOS template), bootstrap/bootstrap.py + agents.yaml (clone/install/
  models/health, verified), bootstrap/prereqs.py (checks/installs prerequisites).

## 7. Gotchas learned the hard way

- The tool layer un-escapes backslashes inside heredoc/`python -c` edits:
  `"\n"` becomes a real newline and breaks string literals. Use the Edit/Write
  tools for code containing backslashes, or `chr(10)` / `chr(92)`.
- When inserting a new click command before an existing one, don't replace the
  existing `@cli.command(...)` decorator text. This broke Vision `list` and
  Friday `push` once each; tests caught it. Insert with `s[:i] + new + s[i:]`.
- Check for existing command names before adding one (Friday already had `today`).
- Tests must be hermetic: every repo's conftest removes `VAULT_PATH`; Friday
  disables the local model; Alfred sets `ALFRED_LLM_BACKEND=off`; TARS sets a
  git identity. Keep it that way.
- `pip install -e` from a temp clone repoints console scripts; reinstall from
  Desktop/Neil/<name> afterwards.
- winget machine-wide MSI installs hang or cancel on UAC in the background; use
  portable zips in ~/tools instead.
- Ultron's README has a CI-checked test count line (`# N tests`, ~line 329); update it when adding tests.
- Verify new CI in a clean `python:3.12-slim` container before pushing it.
- Jarvis MCP child stderr is hidden unless `JARVIS_DEBUG=1`.

## 8. Blocked on the user (don't try to do these yourself)

- Free-tier Groq/OpenRouter keys for real cloud fallback (work/public tiers).
- Admin approval to install Inkscape/Ardour (or accept portable alternatives).
- Phases 1/3: Linux/Hyprland desktop, Zen browser config (deferred by user).
- Registering the Jarvis MCP server in their Claude config; renaming 10x-ecosystem.
- Deleting Downloads/temp files; committing their devNote vault changes.

## 9. What's next

First complete build draft is done (2026-09-23). The user now learns, uses
and breaks it; fix their findings first. Remaining queue: `HANDOFF.md`.
Historical note from before the handover:

See `HANDOFF.md` → Queue. Next up (as of this writing): TARS `guard`
(pre-commit secret blocking), Friday weekly content `ideas` → Socials drafts,
then keep going through the remaining phase work in `docs/phases/README.md`
(Phase 7 socials depth, Phase 8 packaging polish, Phase 9 hardening) and any
high-value improvements found while using the agents together. When the first
full build draft is complete, stop and hand over to the user for learning,
use, and breaking.
