# Repo Map

Two kinds of repo in this ecosystem:

- **Isolated repos** — one per agent/tool, installable and runnable standalone.
- **This repo (10x-ecosystem)** — the umbrella. Holds the vault template, cross-agent
  specs, phase tickets, the OmniRoute privacy rules, and bootstrap scripts that wire
  the isolated repos together. It references the isolated repos (as submodules or
  simple clone-paths — decide at Phase 8 packaging); it does not vendor their code.

Every isolated repo gets its own commits and its own pushes. This repo gets its own
commits and pushes for ecosystem-level changes (docs, bootstrap, vault template).
Nothing is duplicated between them.

## Converted — done, merged, pushed, renamed

| Agent | GitHub | Local | State |
|---|---|---|---|
| **Friday** | github.com/n-3-0-l-d-3-v/friday (public, formerly jarvisOS) | `Desktop/Neil/friday/` | 445 tests passing. Full conversion complete: package/CLI/docs renamed throughout, capture/classify/store/push/link pipeline preserved, catalogue-drift bug fixed (self-healing reindex wired into `friday doctor`/`friday daily`), `agent.yaml`, `friday --health`, `personal-token`-tier guard. Old `JARVIS_*` env vars still read with a deprecation warning. |
| **Ultron** | github.com/n-3-0-l-d-3-v/ultron (public, formerly yugen/aether-platform) | `Desktop/Neil/ultron/` | 385 tests passing. Full conversion complete: package/CLI/docs renamed throughout, evidence-graph discipline and all ADRs (0001-0010) preserved as history, new ADR 0011 documents the rename. `agent.yaml`, `ultron --health`, `ultron vault write/list/approve` (pending→approved human review gate), hard network lockdown enforcing the `private` tier (`RemoteHostRefused` unless explicitly overridden). Kept its own hand-rolled MCP transport per its existing zero-runtime-dependency ADR rather than adopting the `mcp` PyPI package. |
| **Alfred** | github.com/n-3-0-l-d-3-v/alfred (public, formerly LeetLearn) | `Desktop/Neil/alfred/` | 558 Python + 28 JS tests passing. Full conversion complete: package/CLI/extension/docs renamed throughout, AC gate and all existing pedagogy features preserved, `agent.yaml`, health check, MCP server (`get_hint`/`submit_for_ac_gate`/`get_review`/`get_interview_questions`), optional vault integration (`VAULT_PATH` env var — reads Friday's notes before explaining, writes progress notes back; true no-op when unset). |
| **Jarvis** | github.com/n-3-0-l-d-3-v/jarvis (public, net-new) | `Desktop/Neil/jarvis/` | 79 tests passing. Orchestrator: agent registry (`jarvis/agents.yaml`), one standard MCP client for all three siblings (Ultron's hand-rolled server turned out to speak the real MCP wire protocol — no second dialect needed), the tier engine from `omniroute-privacy-spec.md` (fail-closed default, path-based override, per-agent floor enforcement), a v1 keyword-based intent classifier (documented placeholder pending Phase 5's local models), context store + audit log, CLI (`jarvis ask/route/health/daily`, `jarvis --health`). Verified live against real (non-mocked) sibling processes. Known gap: classifier misses phrasings with no keyword hit (e.g. "explain hash maps" → silently defaults to Friday) — tracked, not yet fixed. |

`devNote` (private, github.com/n-3-0-l-d-3-v/devNote) — the vault Friday writes to,
387 notes on disk. Untouched by the conversion. Long-term this either becomes or is
absorbed by the Obsidian vault in Phase 2, so Friday and Obsidian aren't two
separate brains — still an open decision.

## Net-new — nothing built yet

| Agent | Role | Notes |
|---|---|---|
| **TARS** | Code gen / build / test / refactor / scaffolding | Some prior art in `alfredOS`'s throwaway `dev` script (folder-copy + git init) — ergonomics worth keeping, code gets rewritten. |
| **Wall-E** | System health / cleanup / power profiles / weekly report | Next up. This is the one agent that's mostly shell scripts + `systemd`/cron timers, not an LLM loop. Will poll all four existing agents' health checks (Jarvis already proved this pattern works — `jarvis health` aggregates all three siblings live). |
| **Vision** | All creative: music, design, visual, video, photography, portfolio, ideation | Net-new. Owns Excalidraw, DAW project scaffolding, portfolio-asset generation. |

## `alfredOS` folder itself

Not a repo (no `.git`), not code — it's the "Studio" architecture redesign doc
(`ARCHITECTURE.md`, `PLAN.md`, `ECOSYSTEM.md`, `WORKFLOW.md`, `USECASES.md`). Its
honest current-state audit and role design fed directly into the agent specs in
`docs/agents/`. The folder itself doesn't need to become a GitHub repo — its content
is now absorbed into this ecosystem repo's docs. Flag if you want the raw docs kept
as their own artifact instead of being folded in.
