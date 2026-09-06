# OmniRoute Privacy & Provider Routing Spec

Problem this solves: the plan calls for "best of all worlds" routing across local
models and free-tier cloud fallbacks (Groq, OpenRouter free models, Gemini, etc.),
but naive routing sends everything — including personal, private, or sensitive
content — to whichever provider is free/fast/best at the moment. That's a privacy
leak by default. This spec makes the leak impossible by default instead of relying
on remembering to be careful.

## Core rule

Every request that reaches the router carries (or is assigned) a **sensitivity
tier**. The tier determines which providers are even eligible — not just preferred.

| Tier | Examples | Eligible providers |
|---|---|---|
| `private` | Personal journal entries, health/financial notes, anything in `vault/private/`, RE/security findings on real targets, identity-linked content | **Local only.** Ollama models on-device. Zero network calls. If local quality is insufficient, the task fails closed with a message — it does NOT silently fall back to cloud. |
| `personal-token` | Your own accounts/APIs used on your behalf (your GitHub, your LinkedIn draft, your email) | Local first; cloud fallback only via **your own personal API keys/tokens** (not shared/free-tier keys), and only after explicit per-session confirmation the first time a new provider is used for this tier. |
| `work` | Generic coding help, public repo work, non-identifying technical questions | Local first; cloud fallback via **OmniRoute free-tier pool** (Groq free tier, OpenRouter free models, etc.) allowed automatically. |
| `public` | Already-public content (public repo code, published blog drafts, public docs) | Any provider, local or free-tier cloud, automatically. |

## How tier is assigned

1. **Path-based default.** Content under `vault/private/**` or any folder tagged
   `sensitivity: private` in frontmatter defaults to `private`. `vault/public/**`
   or public repo working directories default to `public`.
2. **Agent-declared default.** Each agent declares its own default tier for its job
   (e.g. Ultron's RE findings on real binaries default to `private`; TARS scaffolding
   a public open-source repo defaults to `work`).
3. **Explicit override, one direction only.** You can always downgrade a request's
   eligible providers (force `private` even if content looks generic). You can
   never have Jarvis silently upgrade a `private` request to use cloud — that
   requires an explicit, per-request confirmation, not a config flag flipped once.
4. **No tier, no route.** If Jarvis's classifier can't confidently assign a tier,
   it defaults to `private` (fail closed) and asks you, rather than guessing toward
   convenience.

## Implementation shape

- Router lives in **Jarvis** (the orchestrator). Every other agent calls through it
  rather than hitting a model API directly — this is the single choke point where
  the rule is enforced, so it can't be bypassed by one agent forgetting to check.
- Config: a `providers.yaml` with `tier:` fields per provider entry, and per-agent
  `default_tier:` in each agent's config. Loud validation at startup if an agent has
  no default tier declared — Wall-E flags this in its health report.
- Free-tier cloud usage is metered and logged to the vault (which provider, which
  tier, token count, date) so you can audit "did anything private ever leave this
  machine" with a Dataview query, not a guess.
- Personal tokens (your own API keys for your own accounts) are stored separately
  from the OmniRoute free-tier key pool — different config file, different env var
  namespace (`PERSONAL_*` vs `OMNIROUTE_*`) — so a bug in the free-tier router code
  path can't accidentally reach into your personal-token credentials.

## Open decisions (need your call before Phase 5 implementation)

- Exact free-tier providers to pool into OmniRoute (Groq free tier + OpenRouter free
  models is the obvious start — confirm before wiring in others).
- Whether `work` tier cloud fallback needs a visible indicator (e.g. terminal prompt
  color / statusbar icon) so you always know when a request left the machine.
