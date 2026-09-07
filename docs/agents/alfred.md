# Alfred — Learning / Upskilling Mentor

**Status:** working today, under the name "LeetLearn," in the `LeetLearn` repo.
**Builds on:** `LeetLearn` (351 tests — 323 Python + 28 JS, FastAPI backend +
Chrome/Firefox extension) — see `../repo-map.md`. This is a rename + scope
expansion, not a rewrite, same pattern as jarvisOS → Friday.

Not to be confused with the `alfredOS` folder (that's the architecture-planning
doc set that fed into this whole ecosystem's design, not an agent's codebase —
see `../repo-map.md`).

## Job (already real, from LeetLearn's own README/PLAN.md)

A Socratic coding mentor, not a solution dispenser. The defensible mechanism is
the **AC gate**: structurally incapable of emitting solution code until you pass
the problem yourself, enforced in two independent layers with tests proving no
solution can leak through pre-AC. After you pass: every approach, complexity
deep-dive, a five-persona code review, and a "failure gallery" showing the exact
input that breaks common mistakes.

- Static analysis in 5 languages (Python `ast` + tree-sitter for C++/Java/JS-TS/Go)
- Code-aware hints — nudges reference what you actually wrote, skip rungs you've
  already passed
- Interview mode — questions generated from your own submission
- Six personas (Mentor, Deadpan, Roast, Interviewer, Pragmatist, Professor) —
  same findings, different framing, never worse information
- Runs with **zero API key** — hints come from a DB of Problem Cards built from
  29 pattern archetypes, reviews are computed offline. LLM path is optional and
  daily-capped if ever switched on.
- Cross-browser extension (Chrome + Firefox, one source), reads the editor via
  Monaco rather than DOM-scraping LeetCode directly

## Scope expansion (LeetCode → all dev upskilling)

LeetLearn's own roadmap already points this direction — no new architecture
needed, just building out what Phase 6 ("Scale out") already lists:

- **Platform seam already built**: "a generic paste-anywhere adapter so the
  teaching works on any site or assignment" — this is the hook for expanding
  past LeetCode without rearchitecting.
- Phase 6 roadmap already includes: second judge (Codeforces/HackerRank), VS Code
  extension via the same adapter seam, and a **system-design mentor** — directly
  the "advanced CS topic deep-dive" scope this ecosystem's Alfred spec called for.
- What this ecosystem adds on top of LeetLearn's own roadmap: reading **Friday's
  vault** before explaining anything, so Alfred never re-teaches a concept you've
  already captured a note on, and writing spaced-repetition/streak data back to
  the vault instead of (or alongside) LeetLearn's own DB. This is the one real
  integration point Alfred needs that LeetLearn wasn't built with in mind.

## Key design constraint

Reads Friday's vault **before** explaining anything, so it never re-teaches a
concept you already have a note on. Directly avoids the "every agent starts from
zero" failure mode that `alfredOS/ARCHITECTURE.md`'s honest audit flagged as the
original throwaway prototype's core problem.

## Tools / access

- Read access to Friday's vault (notes, review-due queue).
- Write access to a spaced-repetition schedule / streak tracker — either
  LeetLearn's existing Postgres store, the vault, or both (decide at
  implementation time whether to migrate LeetLearn's DB into the vault or keep
  them separate and linked, same open question as Friday/devNote).

## Sensitivity tier default

`personal-token` — your own learning history is personal but not sensitive enough
to require `private`-tier lockout; still uses your own keys, not the free-tier
pool (see `../omniroute-privacy-spec.md`).

## Rename scope

Same policy as Friday: outward identity only unless you decide otherwise —
README framing and system prompt say "Alfred," code/module names/`LeetLearn`
class names can stay unless you want a full rename.
