# Day 11 — Cost / latency / accuracy tradeoffs — cheat sheet

## The one-sentence version

Find the smallest model that clears your accuracy bar, design latency around p95, and use a
cascade (cheap-first, escalate on low confidence) to buy big-model accuracy at small-model cost.

## The three axes

| Axis | Formula / metric | Notes |
| ---- | ---------------- | ----- |
| Accuracy | your task eval (not a benchmark) | subtract the chance floor |
| Cost/call | `in_tok·price_in + out_tok·price_out` | prices $/1e6 tokens |
| Latency | `TTFT + out_tok·s_per_tok`, measured at **p95** | users feel the tail |

## Pareto frontier

A model is **dominated** if another is ≥ on every axis and strictly better on one → never the
rational pick, drop it. On the frontier: choose the **leftmost (cheapest) model that clears
your accuracy bar**. Nothing clears it → fine-tune (Week 3) or RAG (Week 6) signal.

## Marginal cost of accuracy

Each frontier hop costs more per point than the last. The top hop (large → frontier) is
routinely 10–40× the $/accuracy-point of lower hops. Only pay it if those points are worth it
in the product.

## Latency

- Design SLAs on **p95 / p99**, not p50.
- **Streaming** shows the first token at TTFT → a model with fast TTFT but slow total gen can
  still feel responsive and pass a "first token < Xs" budget even if p95-total would fail
  non-streaming.

## Cost at volume + caching

- `monthly = cost_per_call · calls` — recompute at *real* volume before choosing.
- **Prompt caching** cuts the cached-prefix input cost ~50–90%. Put the stable content
  (system prompt, few-shot, RAG preamble) first so the provider caches a long prefix.
- A cost delta between models translates directly to engineer-months/year — use that framing.

## Cascade router

```
run cheap model -> if confident: ship it
                -> else: escalate to expensive model
blended_acc  = keep_rate·acc_when_confident + esc_rate·acc_expensive
blended_cost = cost_cheap·N + cost_expensive·(escalated count)
```

- Works when: a cheap confidence signal exists (logprob margin / self-check / small verifier),
  the task has a fat easy head, and paying 2 calls on escalation is acceptable.
- Typical result: match the big model's accuracy at ~⅓ its cost; or exceed any single model's
  accuracy below the big model's cost.
- Better confidence estimation ≈ real money (oracle vs noisy router gap is large).
- Cousins: speculative decoding, model routing (classify-then-dispatch), early-exit.

## Numbers worth remembering

- Doubling context ≈ 4× attention cost (Day 04) — long prompts are a latency and $ problem.
- A ~15-point score swing can come from prompt format alone (Day 10) — don't chase 1–2 points.

## What this does not cover

- Running the comparison against real models — Day 12.
- Serving infra (autoscaling, batching, adapter routing) — Week 10.
