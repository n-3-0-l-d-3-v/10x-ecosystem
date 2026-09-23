# 10x — a free, local-first multi-agent developer setup

Seven agents, each its own repo and usable on its own, wired together by an
orchestrator (Jarvis) over MCP. Everything runs on your machine: local models via
Ollama, one shared Obsidian vault as memory, no paid services. Private content
never leaves the machine (see [`docs/omniroute-privacy-spec.md`](docs/omniroute-privacy-spec.md)).

**Status:** first build draft. 1,710 tests across the 7 repos, all green in CI.
Next steps and known gaps are in [`HANDOFF.md`](HANDOFF.md).

## The agents

| Agent | Job | Try it | Tests |
|---|---|---|---|
| [jarvis](https://github.com/n-3-0-l-d-3-v/jarvis) | Orchestrator: routes a sentence to the right agent (local model), enforces privacy tiers, plans and runs tool calls, voice in | `jarvis do "create a new python-cli project called demo" --dry-run` · `jarvis ask "explain two pointers"` · `jarvis daily` · `jarvis listen` | 118 |
| [friday](https://github.com/n-3-0-l-d-3-v/friday) | Knowledge capture into the vault, synthesis, GitHub presence, post drafts, portfolio page | `friday note "..."` · `friday draft linkedin <note>` · `friday github --readme` · `friday portfolio` | 454 |
| [alfred](https://github.com/n-3-0-l-d-3-v/alfred) | Learning mentor: LeetCode hint ladder with an answer gate, system-design practice, concept explanations built on your own notes | `python -m alfred --explain "binary search"` (from `apps/api`) · MCP: `sd_hint`, `sd_review` | 574 |
| [ultron](https://github.com/n-3-0-l-d-3-v/ultron) | Evidence-first binary/firmware analysis on Ghidra; network-less Docker sandbox | `ultron sandbox analyze <file> --project <dir>` · `ultron -P <dir> ask "what is the attack surface?"` | 388 |
| [tars](https://github.com/n-3-0-l-d-3-v/tars) | Scaffold projects, run tests/builds, git branch/commit inside an allowed-roots boundary (never pushes) | `tars new python-cli demo` · `tars test` | 56 |
| [vision](https://github.com/n-3-0-l-d-3-v/vision) | Creative projects: scaffolding, Excalidraw files, asset catalogs, opens the right app | `vision new song --type music` · `vision open song` | 76 |
| [wall-e](https://github.com/n-3-0-l-d-3-v/wall-e) | Weekly health + privacy audit report into the vault, focus/battery mode | `wall-e report` · `wall-e focus on` · `wall-e schedule install` | 44 |

## Set it up

```bash
python bootstrap/prereqs.py --install     # git, python, ollama, java, docker, Ghidra 11
python bootstrap/bootstrap.py             # clone + install all 7 agents, pull models, health-check
```

Then set `VAULT_PATH` to your Obsidian vault (agents write under `agents/<Name>/`)
and open [`vault/Home.md`](vault/Home.md) in Obsidian for the LifeOS dashboard.

## Map

- [`HANDOFF.md`](HANDOFF.md) — current state, gotchas, ordered next steps.
- [`docs/phases/README.md`](docs/phases/README.md) — the phased plan and status.
- [`docs/agents/`](docs/agents/) — one design spec per agent.
- [`docs/omniroute-privacy-spec.md`](docs/omniroute-privacy-spec.md) — sensitivity tiers and provider rules.
- [`vault/`](vault/) — Obsidian LifeOS template (dashboard, habit streaks, templates).
- [`bootstrap/`](bootstrap/) — one-command setup.

## Rules this project holds itself to

- Free and open source only; local model first, cloud only as an explicit, tier-checked fallback.
- Private-tier data never reaches a network (Ultron and Jarvis enforce this in code).
- Agents propose, humans approve anything irreversible: no agent pushes, publishes, or approves its own findings.
