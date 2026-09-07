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
- [ ] Hardware minimums documented (CPU/RAM/GPU/VRAM) — **needs your input**
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
**Status: not started. Blocked on hardware inventory (Phase 0 open item).**

- [ ] Ollama install + model selection sized to actual hardware
- [ ] OmniRoute provider config (`providers.yaml`) implementing `../omniroute-privacy-spec.md`
- [ ] Basic chat + vault integration (proves Jarvis → Friday round-trip works)

**Success criteria:** a request routes through Jarvis, gets a correct sensitivity tier, and reaches the right provider — verified by the Wall-E audit log, not just "it seemed to work."

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
