# Week 10 Lab — Ship It: the RAG service as an API

## The brief

The policy assistant (Week 6) works in a notebook. Now put it behind an HTTP API the rest of
the company can call: **FastAPI**, API-key auth, per-key rate limiting, request/response
schemas, structured logging with a trace id, a health check, and errors mapped to proper
status codes. Then load-test it.

```
POST /ask   { "question": "..." }   ->  200 { answer, sources, gated, trace_id, latency_ms }
                                         401 no/bad key · 429 rate limited · 422 bad body · 503 upstream
GET  /healthz  -> 200 { status, checks }
```

## Usage

```bash
cd projects/practice/week-10-ship-it
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

## What you implement (`src/service/`)

| File | TODOs |
| ---- | ----- |
| `ratelimit.py` | `TokenBucket.allow` |
| `app.py` | `require_api_key`, the `/ask` handler, `_to_http_error` |

The FastAPI wiring, models, middleware hook and logging format are given.

## Acceptance criteria

- `pytest -q` green (uses `fastapi.testclient` + a `FakeRAG`, no network):
  `/healthz` → 200; `/ask` with no key → 401; wrong key → 401; valid key + good body → 200 with
  a `trace_id`; empty question → 422; oversized question → 413; more requests than the bucket
  allows → 429 with a `Retry-After` header; an upstream error → 503 (never a 500 stack trace).
- `LLM_LIVE=1 pytest -q -m live`: the app booted with a **real** `RAGPipeline` answers one
  question with grounded content and a populated `sources` list.

Covers Day 27 (logging + trace id), Day 30 (Lambda/API-GW contract, auth, limits, errors).
