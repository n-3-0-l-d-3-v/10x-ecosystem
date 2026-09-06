# Alfred — Learning Tutor

**Status:** net-new. Not to be confused with the `alfredOS` folder (that's the
architecture-planning doc set that fed into this whole ecosystem's design, not an
agent's codebase — see `../repo-map.md`).

## Job

Spaced repetition, concept explanation, curriculum building from vault notes,
advanced CS topic deep-dives (OS, networking, systems, DBMS, system design,
formal methods light).

## Key design constraint

Reads Friday's vault **before** explaining anything, so it never re-teaches a
concept you've already captured a note on — it builds on your existing notes
instead of starting from zero. This directly avoids the "every agent starts from
zero" failure mode that the honest audit in `alfredOS/ARCHITECTURE.md` flagged as
the original prototype's core problem.

## Tools / access

- Read access to Friday's vault (notes, review-due queue).
- Write access to a spaced-repetition schedule / streak tracker in the vault
  (human review gate on new curriculum suggestions, not automatic).

## Sensitivity tier default

`personal-token` — your own learning history is personal but not sensitive enough
to require `private`-tier lockout; still uses your own keys, not the free-tier pool.
