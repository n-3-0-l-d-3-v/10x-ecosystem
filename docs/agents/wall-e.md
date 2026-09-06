# Wall-E — System Health & Longevity

**Status:** net-new.

## Job

- System health, cleanup, updates, power profile management.
- Weekly health report written to the vault (Dataview-queryable): disk, thermal,
  battery, package update status, model/tool update cadence, and — critically —
  an audit line confirming no `private`-tier request ever reached a cloud provider
  (cross-checks the OmniRoute log, see `../omniroute-privacy-spec.md`).
- Flags any agent missing a declared sensitivity-tier default at startup.

## Key difference from the other agents

Mostly shell scripts + systemd/cron timers, not an LLM reasoning loop. It doesn't
need a chat interface — it needs a schedule and a report format.

## Tools / access

- System-level read access (sensors, package manager status, disk usage).
- Write access to its own weekly-report note in the vault.
- No write access to other agents' code or config — it reports problems, it
  doesn't silently fix them (matches the standing rule: risky/destructive actions
  need confirmation, not silent automation).

## Sensitivity tier default

`private` — system telemetry never needs to leave the machine.
