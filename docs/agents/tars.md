# TARS — Code / Build / Test / Refactor

**Status:** net-new. Only prior art is a throwaway 15-line `dev` script in
`alfredOS` (folder-copy from template + `git init`) — ergonomics worth keeping,
code gets rewritten from scratch.

## Job

- Project scaffolding from templates (`tars new fastapi-app` style, matching the
  `dev new` ergonomics that already felt right).
- Code generation, refactoring, test authoring/running, build support.
- GitHub Actions / local CI helper (git hooks, local runners — Layer 9 concept).

## Tools / access

- Shell access scoped to project directories under an allowed-roots list — never
  arbitrary filesystem access.
- Git operations (branch, commit, PR draft) — PR creation/push still needs your
  confirmation per the standing action-confirmation rules, TARS doesn't get an
  exception.

## Sensitivity tier default

`work` unless the target repo is explicitly private/personal.

## Open questions

- Local model choice for code gen (Qwen3-coder family vs DeepSeek-Coder distill) —
  decide at Phase 5 (Local AI Foundation) once hardware specs are locked.
