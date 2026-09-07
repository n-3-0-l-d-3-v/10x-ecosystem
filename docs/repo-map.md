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

## Existing, working — reuse, don't rewrite

| Repo | GitHub | State | Becomes |
|---|---|---|---|
| `jarvisOS` | github.com/n-3-0-l-d-3-v/jarvisOS (public) | 7.7k lines, 192 tests, MCP server, CLI (`jar`). Captures/classifies/stores notes via Groq → Gemini → offline keyword fallback. | **Friday**, full conversion. Package/CLI/docs renamed jarvisOS → Friday throughout. Existing capture/classify/store/push/link pipeline preserved as-is. Ecosystem requirements merged in: `agent.yaml`, fix the catalogue-drift bug (self-healing index instead of hand-maintained), `personal-token`-tier enforcement, health-check. GitHub repo rename itself is a separate, later action — done only after the code conversion is reviewed. |
| `devNote` | github.com/n-3-0-l-d-3-v/devNote (private) | The actual vault jarvisOS/Friday writes to — 387 notes on disk today. | Friday's memory store. Long-term this either becomes (or is absorbed by) the Obsidian vault in Phase 2, so Friday and Obsidian aren't two separate brains. |
| `yugen` | github.com/n-3-0-l-d-3-v/yugen (public, formerly aether-platform) | Evidence-first binary/firmware analysis. Ghidra headless + binwalk. Deterministic claim graph, no LLM in the core loop. Phase 0-2 shipped, 350 tests, ADRs. | **Ultron**, full conversion. Package/CLI/docs renamed yugen → Ultron throughout. All of yugen's existing requirements (evidence-graph discipline, claim schema, deterministic core, ADRs) preserved as Ultron's requirements. Ecosystem requirements (`agent.yaml` manifest, MCP server, sandboxed execution, vault-write with human review gate, `private`-tier enforcement, health-check) merged in as real missing functionality, not a wrapper layer. One repo, one identity, standalone-usable and ecosystem-member at once. |
| `LeetLearn` | github.com/n-3-0-l-d-3-v/LeetLearn (public) | 351 tests (323 Python + 28 JS). FastAPI backend + Chrome/Firefox extension. Socratic hint ladder + AC gate (structurally can't leak solutions pre-pass) + code-aware review + interview mode. Zero API key required. Own roadmap (Phase 6) already lists system-design mentor + second judge + VS Code extension. | **Alfred**, full conversion. Package/CLI/docs renamed LeetLearn → Alfred throughout. All existing requirements (AC gate, five-language static analysis, personas, cost fence) preserved. Ecosystem requirements (`agent.yaml`, MCP server, vault read/write, `personal-token`-tier enforcement, health-check) merged in as real missing functionality. |

## Net-new — nothing built yet

| Agent | Role | Notes |
|---|---|---|
| **Jarvis** | Orchestrator / router / chief of staff | Needs OmniRoute-style intent classification + privacy-aware routing (see `omniroute-privacy-spec.md`). This is the piece that makes "Gauntlet" feel like one system instead of 7 CLIs. |
| **TARS** | Code gen / build / test / refactor / scaffolding | Some prior art in `alfredOS`'s throwaway `dev` script (folder-copy + git init) — ergonomics worth keeping, code gets rewritten. |
| **Wall-E** | System health / cleanup / power profiles / weekly report | Net-new. This is the one agent that's mostly shell scripts + `systemd`/cron timers, not an LLM loop. |
| **Vision** | All creative: music, design, visual, video, photography, portfolio, ideation | Net-new. Owns Excalidraw, DAW project scaffolding, portfolio-asset generation. |

## `alfredOS` folder itself

Not a repo (no `.git`), not code — it's the "Studio" architecture redesign doc
(`ARCHITECTURE.md`, `PLAN.md`, `ECOSYSTEM.md`, `WORKFLOW.md`, `USECASES.md`). Its
honest current-state audit and role design fed directly into the agent specs in
`docs/agents/`. The folder itself doesn't need to become a GitHub repo — its content
is now absorbed into this ecosystem repo's docs. Flag if you want the raw docs kept
as their own artifact instead of being folded in.
