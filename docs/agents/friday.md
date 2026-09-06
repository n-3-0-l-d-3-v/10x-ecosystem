# Friday — Knowledge, Docs, Writing

**Status:** working today, under the name "Jarvis," in the `jarvisOS` repo.
**Builds on:** `jarvisOS` (7.7k lines, 192 tests, `jar` CLI, MCP server, 18 MCP
tools) — see `../repo-map.md`. This is a rename of identity, not a rewrite.

## Job (already real, from jarvisOS's own README)

Capture → classify → format → save → push → link. Groq → Gemini → offline-keyword
fallback for classification. Notes land in `devNote` as cross-linked Markdown.

- `jar note "..."` / `jar youtube URL` / `jar article URL` / `jar rss`
- `jar wiki` — synthesizes scattered notes on a topic into one authoritative page
  (LLM Wiki pattern)
- `jar listen` — voice capture via Groq Whisper
- `jar daily` — streak, due reviews, one next action

## Known real problems to fix (from `alfredOS/ARCHITECTURE.md`'s honest audit)

1. **Catalogue drift.** 387 notes on disk, `index.json` lists only 112 — roughly
   70% of notes are invisible to search/linking/dashboard. Root cause: catalogue
   is maintained by hand as notes arrive through the primary path; anything
   arriving another way (manual edit, import) never gets registered.
2. **Adoption gap.** Last capture was over a month before this audit. This is a
   design problem (friction, no ambient trigger) not a discipline problem — Jarvis
   (orchestrator) taking over as the single entry point may fix this by removing
   the "which CLI do I even run" decision.

## Rename scope

Outward identity only unless you decide otherwise: CLI banner, README framing,
system prompt say "Friday." Code, module names, and the `jar` command can stay —
renaming a working CLI people (and muscle memory) already use is a real cost with
no functional benefit. Flag this file if you want a full rename instead.

## Vault relationship

Friday both feeds and reads the vault. Its `devNote` repo is either merged into
the Obsidian vault structure in Phase 2, or kept as a separate git-backed store
that the vault links into — decide when Phase 2 (Brain) starts, not before.

## Sensitivity tier default

`personal-token` — your own notes, using your own Groq/Gemini keys, not the
OmniRoute free-tier pool (see `../omniroute-privacy-spec.md`).
