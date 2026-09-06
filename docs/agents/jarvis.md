# Jarvis — Orchestrator

**Status:** net-new, not started.
**Builds on:** nothing existing; this is the piece that ties the others together.

## Job

Single entry point for "talk to my system." Classifies intent, assigns a
sensitivity tier (see `../omniroute-privacy-spec.md`), routes to the right
specialist agent (Friday/TARS/Ultron/Alfred/Wall-E/Vision), and holds the only
copy of cross-agent context (what you asked five minutes ago, which agent is
mid-task).

## Daily practical jobs

- Morning briefing: pulls from Friday's vault (streaks, due reviews, yesterday's
  captures) and Wall-E's last health report, presents one summary.
- Routes every incoming request through the sensitivity-tier check before any
  agent sees it.
- Voice interface entry point (whisper.cpp in, Piper/Coqui out) — later phase.

## Tools / access

- Read-only access to each agent's status/health endpoint.
- Write access to a shared short-term context store (not the vault itself —
  Jarvis doesn't write permanent notes, Friday does).
- The OmniRoute provider router lives here (single choke point, see privacy spec).

## Boundaries

- Does not do the actual work of any specialist — pure dispatch + context.
- Never bypasses the sensitivity-tier check, even for itself.

## Open questions

- CLI-first (a `jar`-style single command) or does it need a persistent background
  process for voice/context continuity? Affects Phase 6 implementation shape.
