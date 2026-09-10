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
