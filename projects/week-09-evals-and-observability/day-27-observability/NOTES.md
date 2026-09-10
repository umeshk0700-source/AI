# Day 27 — Observability — cheat sheet

## The one-sentence version

Wrap each pipeline stage in a timed **span**; a request's tree of spans is a **trace**, and
when the final answer is wrong you read the trace top-to-bottom to find the first span whose
output is wrong given a correct input — that span is the bug.

## Three pillars

| Pillar | Question | Shape |
| ------ | -------- | ----- |
| Logs | what happened at this moment? | structured timestamped events |
| **Traces** | the full path of *this one request*? | a tree of timed spans |
| Metrics | aggregate health over time? | p95 latency, error rate, cost/day, 👎 rate |

## The span model

```python
_current = contextvars.ContextVar("span", default=None)

@contextmanager
def span(name, kind="op", **inputs):
    s = Span(name, kind); s.parent = _current.get(); s.start = perf_counter()
    tok = _current.set(s)
    try: yield s
    except Exception as e: s.status = "error"; s.error = repr(e); raise
    finally: s.end = perf_counter(); _current.reset(tok)
```

A span has: `name`, `kind`, `parent`, `children`, `inputs`, `outputs`, `metadata`, `status`,
`start`/`end`. `@traceable` / `@observe` decorators (LangSmith / Langfuse) = this context
manager wrapped around a function.

## What to capture per stage

| Stage | Capture | Don't |
| ----- | ------- | ----- |
| request | trace_id, hashed user_id, app version, model+params | raw PII |
| retrieve | query, k, retrieved **ids + scores**, index version | full chunk text (store ids) |
| gate/guard | the decision + threshold + compared value | — |
| build prompt | **hash + token count** (full text only when sampled) | full prompt every request |
| generate | model, params, stop_reason, usage, latency, **cost**, raw response | — |
| tool call | name, args, result, latency, error | secrets in args |

**Rule:** capture enough to reconstruct the decision at every branch. Scores and ids, not text.

## Debugging workflow

1. 👎 / alert → get `trace_id` (surface it in the UI / error messages).
2. Open trace, read top→bottom. First span with **wrong output, correct input** = the fault.
3. Fix that span.
4. Add the failing input as a Day-26 test case.
5. Recurring → a metric/alert on that span's quality.

## Redaction / sampling / retention

- Redact emails/phones/cards at the *instrumentation layer* — no raw PII reaches the store.
- Store full prompt/response text for ~1–10% of traces + 100% of errors & 👎; ids+scores+hashes
  for the rest.
- Short TTL (7–30d) for full traces; longer for aggregates. Tracing overhead is tiny; storage
  isn't.

## Tools (same core model)

LangSmith (LangChain-native, datasets+eval) · Langfuse (OSS, self-host, prompt mgmt) · Arize
Phoenix (OSS, OTel, retrieval debugging) · OpenLLMetry/OTel GenAI (vendor-neutral) · Braintrust
/ W&B Weave (eval-forward).

## What this does not cover

- Deploying + serving the pipeline — Week 10.
- Alerting rules / on-call — ops-specific.
