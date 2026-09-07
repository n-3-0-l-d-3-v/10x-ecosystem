# Phased Execution Plan

Reconciled against what's already built (see `../repo-map.md`) — phases that
would duplicate existing work are marked accordingly. Strict order still applies:
no phase starts until the previous one's success criteria are met. No OS/Linux
install work happens yet, per your instruction — Phases 1 and 3 (desktop, browser)
are deferred until you say so; everything else can proceed now.

Each phase below is a ticket: **Goal**, **Tasks**, **Success criteria**, **Status**.

---

## Phase 0 — Spec Freeze
**Status: in progress (this session).**

- [x] Hardware/software inventory of what already exists (jarvisOS, yugen, alfredOS docs)
- [x] Agent roster finalized: Jarvis/Friday/TARS/Ultron/Alfred/Wall-E/Vision, mapped to existing code where it exists
- [x] Repo strategy: isolated repos per agent + umbrella ecosystem repo
- [x] Hardware inventoried (this machine): Intel i5-11400H, 32GB RAM, RTX 3050 Laptop (~4GB VRAM). Used directly in Phase 5's model sizing.
- [ ] Vault structure sketch finalized (Phase 2 will build it, sketch happens here)

**Success criteria:** every agent has a spec file, every existing asset is mapped, no ambiguity left before code starts.

---

## Phase 1 — Base OS + Aesthetic + Power
**Status: deferred — explicitly skipped for now per your instruction.**

Omarchy/Arch+Hyprland/NixOS install, theming, power management, terminal/shell,
keybinds. Requires hands-on-machine work I can't do from here. Revisit once the
agent/repo layer is solid.

---

## Phase 2 — Brain (Obsidian)
**Status: not started. Vault skeleton folders created in this repo (`vault/`) but empty.**

- [ ] Decide: does `devNote` (Friday's existing vault) become the Obsidian vault, or
  does Obsidian vault wrap/link to it?
- [ ] LifeOS dashboard (Dataview homepage)
- [ ] Daily notes + streak/habit tracking templates
- [ ] Media-note pipeline (YouTube transcript + timestamps)
- [ ] Plugin list finalized (Dataview, Templater, Calendar, Excalidraw, Media Extended, Tasks, QuickAdd, Linter, Style Settings)

**Success criteria:** single vault is the source of truth Friday, Alfred, Wall-E, and Vision all read/write to.

---

## Phase 3 — Browser + Core Creative Apps
**Status: deferred (Zen/browser setup needs hands-on-machine work) — creative app research can proceed now.**

- [ ] Zen Browser config (deferred with Phase 1)
- [ ] Free creative stack install list finalized per Vision's scope (Ardour, LMMS, Krita, GIMP, Penpot, Blender, Godot, DaVinci/Shotcut/Kdenlive/OBS, Darktable)
- [ ] Spotify/local-audio-player integration plan

---

## Phase 4 — Dev + Security + Systems Toolchain
**Status: Ultron done. TARS not started.**

- [ ] Language toolchain list finalized (Rust/Go/Python/C/C++/JS-TS/Zig/Java as needed)
- [x] ~~Ultron wraps `yugen`~~ — done, full conversion (not a wrapper): sandboxed network lockdown, vault writes with human review gate, `agent.yaml`, health check. See `../repo-map.md`.
- [ ] TARS scaffolding tool built (replaces the `alfredOS` throwaway `dev` script)
- [ ] Container runtime decision (Podman preferred per original plan)

**Success criteria:** ~~Ultron produces a real evidence-cited finding via yugen end to end~~ — met; TARS scaffolds a real project (pending).

---

## Phase 5 — Local AI Foundation
**Status: core done.** Hardware inventory: Intel i5-11400H, 32GB RAM, RTX 3050 Laptop (~4GB VRAM) — sized model selection to this.

- [x] Ollama installed via winget, running as a local service (`127.0.0.1:11434`).
- [x] Models pulled: `qwen2.5:3b` (routing/classification — fits fully in 4GB VRAM), `qwen2.5:7b` (larger, for future heavier local tasks — may partially offload to system RAM on this GPU, that's fine, just slower).
- [x] `providers.yaml` + `providers.py` in Jarvis — the OmniRoute eligibility table, honest about what's real (`ollama-local`, fully wired) vs. aspirational (`groq-free-tier`/`openrouter-free-tier` — no shared credentials configured yet, tracked not faked).
- [x] Jarvis's v1 keyword classifier replaced by a local-model classifier (`jarvis/local_classifier.py`), built from the live agent registry rather than a hardcoded keyword table — fixes both the "explain hash maps" gap and the fact that the keyword classifier never knew about TARS/Vision. Falls back to the keyword classifier silently on any failure (Ollama down, model not pulled, bad response) — verified both paths live.
- [ ] Real OmniRoute cloud-fallback routing (Groq/OpenRouter free tier) — not done. Needs the user to supply free-tier API keys first; `work`/`public` tier requests are local-only (`ollama-local`) until then.
- [ ] Friday/Alfred's own provider calls aren't centrally routed through Jarvis — each already had its own working, correctly tier-guaranteed provider logic before Jarvis existed. Retrofitting that through a central router is a real rewrite of working code, not done as part of this phase; `providers.yaml` documents this as the honest current state, not a gap to silently paper over.

**Success criteria:** ~~a request routes through Jarvis, gets a correct sensitivity tier, and reaches the right provider~~ — met for the local path (verified live: `jarvis route` correctly tier-gates and selects an agent using the real local model, not mocked). Not yet met for the cloud-fallback path, which doesn't exist yet by design (no credentials).

---

## Phase 6 — Gauntlet Agents (depth first)
**Status: DONE. All 7 agents built, tested, and pushed.**

1. ~~Friday~~ — converted from jarvisOS, merged, pushed, GitHub repo renamed. 445 tests.
2. ~~Ultron~~ — converted from yugen, merged, pushed, GitHub repo renamed. 385 tests.
3. ~~Alfred~~ — converted from LeetLearn, merged, pushed, GitHub repo renamed. 558 Python + 28 JS tests.
4. ~~Jarvis~~ — orchestrator, new repo. 79 tests. Real MCP client for all three siblings (Ultron's hand-rolled server speaks the actual MCP wire protocol — no second dialect needed), the tier engine, a v1 keyword-based intent classifier.
   - **Known gap (tracked, not blocking):** the v1 keyword classifier misses phrasings like "explain hash maps" (no keyword hit → silently defaults to Friday instead of Alfred). Needs either broader keyword coverage or the Phase 5 local-model classifier to fix properly.
5. ~~Wall-E~~ — system health, new repo. 35 tests. Aggregates all agents' health, audits Jarvis's dispatch log for privacy-tier violations, checks `agent.yaml` contract compliance, writes weekly vault reports. Power/thermal/scheduling deferred — no Linux target yet, `wall-e report` is manual for now.
6. ~~TARS~~ — code/build/test/scaffolding, new repo. 56 tests. Hard-enforced allowed-roots safety boundary (verified live to fail closed). Deliberately no `tars push`.
7. ~~Vision~~ — creative/ideation, new repo. 68 tests. Project scaffolding, real `.excalidraw` starter files, asset cataloging, vault MOC with working `--private` routing. No DAW/Krita/Blender automation — that software isn't installed yet (Phase 3 deferred).

**Success criteria per agent:** does its real daily job end-to-end, writes to the vault correctly, respects its declared sensitivity tier. All 7 meet this individually. Jarvis routing to real sibling agents over MCP is verified, and Wall-E polling all of them (including Jarvis itself) is verified, not just unit-tested — the ecosystem is wired together, not just seven parallel CLIs.

**What Phase 6 does NOT yet mean:** TARS/Vision aren't yet registered in Jarvis's `agents.yaml` (Jarvis currently only knows about Friday/Ultron/Alfred) — routing `jarvis ask` to TARS or Vision needs that registry updated. Small follow-up, not done automatically by building the agents themselves.

---

## Phase 7 — Socials & Creative Depth
**Status: not started.** GitHub maxing (contribution graphs, PR/star tracking), LinkedIn/Medium/Dev.to/portfolio pipeline, Reddit/Discord workflows — all driven from vault + Friday/Vision.

---

## Phase 8 — Packaging & Reproducibility
**Status: not started.** Decide Nix flakes vs. Ansible+Compose for the isolated-repos-plus-umbrella structure. One-command bootstrap. This is also where the "hold the whole setup, shareable to anyone with the hardware" goal gets solved concretely.

---

## Phase 9 — Hardening, Performance, Continuous Loop
**Status: not started.** Sandboxing (bubblewrap/firejail per-agent, especially Ultron), Focus Modes, Wall-E's weekly cadence running for real, update strategy that doesn't break things, computer-vision face-unlock-after-password layer if hardware supports it.
