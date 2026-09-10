# Week 8 Lab — Resilient LLM Gateway

## The brief

Every team is now calling Claude directly. That's a reliability and cost problem: no failover
when Anthropic has an incident, no caching of repeated prompts, no per-team budgets, no single
place to see spend. Build the **gateway** every service calls instead.

```
Gateway.chat(tenant, ...) :
  1. SemanticCache.get(prompt)         -> hit? return it (0 cost)
  2. CircuitBreaker(primary).call(...) -> Claude
  3. on failure / open circuit         -> fallback (GPT)
  4. cache the result, charge the tenant's CostTracker
```

## Usage

```bash
cd projects/practice/week-08-llm-gateway
make setup        # install deps (into the shared ../../../.venv)
make test         # offline unit tests — your work-in-progress: TODOs + failures
make solution     # the same tests against the reference implementation (all green)
make live         # real Claude/GPT — needs keys, costs ~$0.10   (preset: .env.preset)
make lab          # open the walkthrough notebook
```

**Presets.** `.env.preset` (committed, no secrets) pins the models and the spend cap for this
lab. `make live` sources it automatically. Your keys go in `projects/practice/.env`
(gitignored) — copy `projects/practice/.env.example`. Override a preset per run:
`ANTHROPIC_MODEL=claude-sonnet-4-5 LAB_USD_CAP=1 make live`.

## What you implement (`src/gateway/`)

| File | TODOs |
| ---- | ----- |
| `cache.py` | `SemanticCache.get`, `SemanticCache.put` |
| `breaker.py` | `CircuitBreaker.call` (closed → open → half-open) |
| `gateway.py` | `Gateway.chat` (the orchestration) |

## Acceptance criteria

- `pytest -q` green: a near-duplicate prompt is a cache hit (cosine ≥ threshold); the breaker
  opens after `failure_threshold` consecutive failures and half-opens after `reset_timeout`;
  when the primary raises, `Gateway.chat` returns the fallback's answer and records which
  provider served the request; a tenant that exceeds its budget raises `BudgetExceeded`.
- `LLM_LIVE=1 pytest -q -m live`: a repeated real prompt is served from cache the second time
  (0 additional cost); with the primary forced to fail, the real GPT fallback answers.

Covers Day 08/22–24 (SDK, retries, streaming), Day 11 (caching, cascade), Day 27 (per-request tracing).
