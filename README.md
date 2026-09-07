# 10x — The Ecosystem Umbrella Repo

The single git repo tying together every isolated agent repo into one reproducible,
free, local-first developer/creative/security setup. See `docs/repo-map.md` for
exactly which repo is which and what's already built vs. net-new.

## Start here

- [`docs/repo-map.md`](docs/repo-map.md) — which repos are converted/built (Friday,
  Ultron, Alfred, Jarvis) vs. net-new, and where each one lives.
- [`docs/omniroute-privacy-spec.md`](docs/omniroute-privacy-spec.md) — the
  privacy/provider-routing rule: private tokens for personal work, free-tier
  OmniRoute pool for generic work, local-only fail-closed for sensitive content.
- [`docs/phases/README.md`](docs/phases/README.md) — the phased build order,
  ticket-style, with status against each phase.
- [`docs/agents/`](docs/agents/) — one spec per Gauntlet agent (Jarvis, Friday,
  TARS, Ultron, Alfred, Wall-E, Vision).
- [`vault/`](vault/) — Obsidian vault skeleton (folders only for now; Phase 2
  builds this out).

## Non-negotiables

100% free/open-source/local-first. Obsidian vault is the single brain for every
agent. Minimal interface, maximally stacked capability. Declarative and
git-managed so the whole thing is reproducible by anyone with the hardware
minimums. Sensitive content never leaves the machine — see the privacy spec.

## Related repos (isolated, each with its own commits/pushes)

Done:
- [friday](https://github.com/n-3-0-l-d-3-v/friday) (formerly jarvisOS)
- [ultron](https://github.com/n-3-0-l-d-3-v/ultron) (formerly yugen/aether-platform)
- [alfred](https://github.com/n-3-0-l-d-3-v/alfred) (formerly LeetLearn)
- [jarvis](https://github.com/n-3-0-l-d-3-v/jarvis) (net-new orchestrator — routes to the three above over MCP)
- `devNote` (private) — Friday's vault store, pending Phase 2 merge decision

New repos (TARS, Wall-E, Vision) get created and linked here as each is built, per
`docs/phases/README.md` Phase 6 order.
