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

Phase 6 (all 7 agents) is done. Remaining open items, in rough priority order:
1. Jarvis's intent classifier is v1 keyword-matching — misses phrasings with no
   keyword hit (see `docs/repo-map.md`'s Jarvis entry).
2. Vision has no MCP server yet — health-checkable, not yet dispatchable through
   `jarvis ask`.
3. Phase 2 (Obsidian vault) — every agent already writes to its own local
   `vault/<Agent>/` folder; the real shared vault and the `devNote`-vs-vault
   merge decision haven't happened yet.
4. Phases 1/3 (Linux desktop, Zen browser) — still deliberately on hold.
5. Phase 5 (local Ollama models) — would upgrade Jarvis's classifier and unlock
   real OmniRoute cloud-fallback routing, currently a no-op tier-logging layer.
