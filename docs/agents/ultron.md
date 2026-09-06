# Ultron — Reverse Engineering / Security

**Status:** backend engine working today under the name `yugen` (formerly Aether),
public repo `github.com/n-3-0-l-d-3-v/yugen`. Ultron itself (the agent wrapper) is
net-new.

## Relationship to yugen — kept separate, not merged

Yugen is a disciplined, tested, ADR-documented evidence-graph engine for binary and
firmware analysis (Ghidra headless + binwalk, deterministic claims, zero LLM in the
core loop, 350 tests, Phase 0-2 shipped). It has its own release cadence and rigor
that would only get diluted by folding it into a lifestyle/agent-ecosystem repo. See
`../repo-map.md` for the full reasoning.

Ultron is a **thin wrapper**: sandboxed process (separate user or container per the
plan's security principle), personalized system prompt, vault-aware (writes RE
findings as structured notes with human review gates), and it shells out to the
`yugen` CLI for the actual analysis work rather than reimplementing any of it.

```
you → Ultron (sandboxed) → yugen ask / yugen map / yugen reach → structured claims
                         → Ultron writes findings to vault (human review gate)
```

## Job

- CTF / binary analysis / exploit research support, always evidence-cited (yugen
  refuses free-text claims by design — Ultron inherits that discipline rather than
  wrapping it in looser natural language).
- Firmware analysis, cross-binary reachability, version diffing — via yugen's
  existing `yugen map`, `yugen reach`, `yugen diff-versions` commands.

## Sandboxing

Bubblewrap/firejail or a dedicated container/VM, separate user account for RE work.
Never runs with the same privileges as your daily driver shell.

## Sensitivity tier default

`private`. RE findings on real targets never leave the machine — local-only,
fail-closed if local model quality is insufficient (see
`../omniroute-privacy-spec.md`).
