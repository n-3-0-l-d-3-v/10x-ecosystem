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

## All 7 Gauntlet agents — built, tested, pushed

| Agent | GitHub | Local | State |
|---|---|---|---|
| **Friday** | github.com/n-3-0-l-d-3-v/friday (public, formerly jarvisOS) | `Desktop/Neil/friday/` | 445 tests passing. Full conversion complete: package/CLI/docs renamed throughout, capture/classify/store/push/link pipeline preserved, catalogue-drift bug fixed (self-healing reindex wired into `friday doctor`/`friday daily`), `agent.yaml`, `friday --health`, `personal-token`-tier guard. Old `JARVIS_*` env vars still read with a deprecation warning. |
| **Ultron** | github.com/n-3-0-l-d-3-v/ultron (public, formerly yugen/aether-platform) | `Desktop/Neil/ultron/` | 385 tests passing. Full conversion complete: package/CLI/docs renamed throughout, evidence-graph discipline and all ADRs (0001-0010) preserved as history, new ADR 0011 documents the rename. `agent.yaml`, `ultron --health`, `ultron vault write/list/approve` (pending→approved human review gate), hard network lockdown enforcing the `private` tier (`RemoteHostRefused` unless explicitly overridden). Kept its own hand-rolled MCP transport per its existing zero-runtime-dependency ADR rather than adopting the `mcp` PyPI package. |
| **Alfred** | github.com/n-3-0-l-d-3-v/alfred (public, formerly LeetLearn) | `Desktop/Neil/alfred/` | 558 Python + 28 JS tests passing. Full conversion complete: package/CLI/extension/docs renamed throughout, AC gate and all existing pedagogy features preserved, `agent.yaml`, health check, MCP server (`get_hint`/`submit_for_ac_gate`/`get_review`/`get_interview_questions`), optional vault integration (`VAULT_PATH` env var — reads Friday's notes before explaining, writes progress notes back; true no-op when unset). |
| **Jarvis** | github.com/n-3-0-l-d-3-v/jarvis (public, net-new) | `Desktop/Neil/jarvis/` | 108 tests passing. Orchestrator: agent registry (`jarvis/agents.yaml`, now includes all 5 health-checkable agents), one standard MCP client for all three MCP-capable siblings (Ultron's hand-rolled server speaks the real MCP wire protocol — no second dialect needed), the tier engine from `omniroute-privacy-spec.md` (fail-closed default, path-based override, per-agent floor enforcement), a local-model intent classifier (`jarvis/local_classifier.py`, Phase 5 — replaced the v1 keyword placeholder, prompt built from the live registry so new agents need no classifier code change), `providers.yaml`/`providers.py` (OmniRoute eligibility table), context store + audit log, CLI (`jarvis ask/route/health/daily`, `jarvis --health`). Verified live against real (non-mocked) sibling processes and a real running `qwen2.5:3b`: the old "explain hash maps → defaults to Friday" gap is fixed (now correctly routes to Alfred), and routing works correctly for TARS/Vision too. Falls back to the keyword classifier automatically if Ollama is down or the model isn't pulled — verified both paths. |
| **Wall-E** | github.com/n-3-0-l-d-3-v/wall-e (public, net-new) | `Desktop/Neil/wall-e/` | 35 tests passing. System health: shells out to `jarvis health` (real, not mocked) for agent aggregation, reads Jarvis's audit-log sqlite directly to flag any `private`-tier dispatch routed to a non-Ultron agent, checks all 4 agent.yaml files for contract compliance, checks disk space + git-dirty status across all 4 sibling repos, writes a weekly Markdown report to `vault/Wall-E/`. Verified live: 4/4 agents healthy, all 4 agent.yaml compliant, all 4 repos clean. Power/thermal/scheduling explicitly deferred — no Linux target yet (Phase 1 still on hold), `wall-e report` is a manual one-shot command for now, not a daemon. |
| **TARS** | github.com/n-3-0-l-d-3-v/tars (public, net-new) | `Desktop/Neil/tars/` | 56 tests passing. Scaffolding (`tars new <template> <name>`, 2 real starter templates), language-agnostic build/test dispatch (Python/Node marker-file detection, Rust/Go detection-only — no toolchain installed to test against), git ops (`branch`/`commit`/`status`) scoped to a hard-enforced allowed-roots safety boundary — verified live to fail closed on an out-of-bounds destination. Deliberately no `tars push` (publishing stays a user-confirmed action ecosystem-wide). MCP server, `agent.yaml`, `tars --health`. |
| **Vision** | github.com/n-3-0-l-d-3-v/vision (public, net-new) | `Desktop/Neil/vision/` | 68 tests passing. Creative project scaffolding (6 project types), real structurally-valid `.excalidraw` starter-file generation, asset manifest/cataloging, vault MOC integration with a working `--private` flag (routes to `vault/Vision/private/`, not a no-op). No DAW/Krita/Blender/etc. automation — none of that software is installed yet (Phase 3 deferred), documented as out of scope rather than faked. `agent.yaml`, `vision --health`. |

`devNote` (private, github.com/n-3-0-l-d-3-v/devNote) — the vault Friday writes to,
387 notes on disk. Untouched by the conversion. Long-term this either becomes or is
absorbed by the Obsidian vault in Phase 2, so Friday and Obsidian aren't two
separate brains — still an open decision.

## `alfredOS` folder itself

Not a repo (no `.git`), not code — it's the "Studio" architecture redesign doc
(`ARCHITECTURE.md`, `PLAN.md`, `ECOSYSTEM.md`, `WORKFLOW.md`, `USECASES.md`). Its
honest current-state audit and role design fed directly into the agent specs in
`docs/agents/`. The folder itself doesn't need to become a GitHub repo — its content
is now absorbed into this ecosystem repo's docs. Flag if you want the raw docs kept
as their own artifact instead of being folded in.
