# 10x — The Ecosystem Umbrella Repo

The single git repo tying together every isolated agent repo into one reproducible,
free, local-first developer/creative/security setup. All 7 Gauntlet agents are
built, tested, and wired together — see `docs/repo-map.md` for exactly which repo
is which.

## Start here

- [`docs/repo-map.md`](docs/repo-map.md) — all 7 agent repos, what each one does,
  test counts, and what's verified live vs. only unit-tested.
- [`docs/omniroute-privacy-spec.md`](docs/omniroute-privacy-spec.md) — the
  privacy/provider-routing rule: private tokens for personal work, free-tier
  OmniRoute pool for generic work, local-only fail-closed for sensitive content.
  Implemented for real in Jarvis's tier engine, enforced live.
- [`docs/phases/README.md`](docs/phases/README.md) — the phased build order,
  ticket-style, with status against each phase. Phase 6 (all 7 agents) is done;
  Phases 1/3 (OS/browser setup) are deliberately deferred.
- [`docs/agents/`](docs/agents/) — one spec per Gauntlet agent (Jarvis, Friday,
  TARS, Ultron, Alfred, Wall-E, Vision).
- [`vault/`](vault/) — Obsidian vault skeleton (folders only for now; Phase 2
  builds this out).

## Non-negotiables

100% free/open-source/local-first. Obsidian vault is the single brain for every
agent. Minimal interface, maximally stacked capability. Declarative and
git-managed so the whole thing is reproducible by anyone with the hardware
minimums. Sensitive content never leaves the machine — see the privacy spec.

## The 7 agents (all built, tested, pushed)

| Agent | Repo | Job |
|---|---|---|
| [friday](https://github.com/n-3-0-l-d-3-v/friday) | formerly jarvisOS | Knowledge capture, notes, writing |
| [ultron](https://github.com/n-3-0-l-d-3-v/ultron) | formerly yugen/aether-platform | Reverse engineering, binary/firmware analysis |
| [alfred](https://github.com/n-3-0-l-d-3-v/alfred) | formerly LeetLearn | Learning/upskilling mentor |
| [jarvis](https://github.com/n-3-0-l-d-3-v/jarvis) | net-new | Orchestrator — routes to the others over MCP, enforces the privacy tiers |
| [wall-e](https://github.com/n-3-0-l-d-3-v/wall-e) | net-new | System health, privacy-compliance audit, weekly reports |
| [tars](https://github.com/n-3-0-l-d-3-v/tars) | net-new | Code scaffolding, build/test dispatch, scoped git ops |
| [vision](https://github.com/n-3-0-l-d-3-v/vision) | net-new | Creative project scaffolding, Excalidraw, asset cataloging |

`devNote` (private) — Friday's vault store, pending the Phase 2 vault-merge decision.

Each repo is standalone-installable and independently useful on its own. Jarvis's
`agents.yaml` is the registry that wires all of them together — see
`docs/repo-map.md` for exact test counts and what's been verified running live
(not just unit-tested) versus what's still a documented gap.

## What's next

Phase 6 (all 7 agents) and Phase 5's core (local Ollama) are both done. Remaining
open items, in rough priority order:
1. Vision has no MCP server yet — health-checkable, not yet dispatchable through
   `jarvis ask`.
2. Real OmniRoute cloud-fallback (Groq/OpenRouter free tier) isn't wired in — no
   shared free-tier credentials configured yet. `work`/`public`-tier requests are
   local-only (`ollama-local`) until that's added.
3. Phase 2 (Obsidian vault) — every agent already writes to its own local
   `vault/<Agent>/` folder; the real shared vault and the `devNote`-vs-vault
   merge decision haven't happened yet.
4. Phases 1/3 (Linux desktop, Zen browser) — still deliberately on hold.

## Local AI (Phase 5 — done)

Ollama is installed and running (`127.0.0.1:11434`), sized to this machine's
actual hardware (Intel i5-11400H, 32GB RAM, RTX 3050 Laptop ~4GB VRAM):
`qwen2.5:3b` (routing/classification, fits fully in VRAM) and `qwen2.5:7b`
(larger, for future heavier local tasks). Jarvis's intent classifier now uses
the local model instead of the old v1 keyword table — verified live to fix the
documented "explain hash maps" misroute and to correctly route to every one of
the 5 health-checkable agents, with an automatic, tested fallback to the
keyword classifier if Ollama is ever down or the model isn't pulled.
