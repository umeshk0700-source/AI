# Day 12 — Model bake-off — cheat sheet

## The one-sentence version

One `complete(system, user) -> {text, latency_s, tok_in, tok_out}` adapter per model, one gold
set, two scores (format + correctness) → a measured accuracy/cost/latency table you can
actually choose from.

## The harness (reusable)

```python
class LocalHF:                 # or ClaudeAPI, OpenAIAPI — same signature
    def complete(self, system, user) -> dict(text, latency_s, tok_in, tok_out): ...

for m in MODELS:
    for x, gold in GOLD:
        r = m.complete(SYSTEM, template(x))
        fmt_ok, correct, pred = score_one(r["text"], gold)
        rows.append({... r ..., fmt_ok, correct})
# aggregate per model: accuracy, format_ok, p50/p95 latency, $/1k, mean tok_out
```

Cost: `(tok_in·price_in + tok_out·price_out) / 1e6`.

## What this bake-off shows

- **Capability has a size threshold.** Qwen2.5-0.5B (few-shot) classifies the tickets ~0.83;
  SmolLM2-360M collapses to one label (~0.17); SmolLM2-135M emits prose (~0.00). Below some
  size, more prompting doesn't help.
- **Instruction tuning matters more than raw size** at the low end — a tuned 0.5B beats an
  untuned 0.1B by a mile on format adherence.
- When models are similarly priced, **capability, not price, is the deciding axis**.

## Rules

1. Score format and correctness separately — different fixes (parser/constrain vs better
   model/data).
2. Never choose on a single prompt phrasing — run a v2 wording; if the ranking flips, keep
   testing.
3. Report p50 **and** p95 latency.
4. 12 items ≈ ±15-point CI on accuracy. Scale the gold set to 50–200 before committing.
5. The set where two models disagree = the ambiguous/hard cases = highest-value items to label
   and add to the eval.

## Adding an API model

Implement one class with `complete()`; read `tok_in`/`tok_out` from `response.usage`; put real
$/1M prices in `PRICES`. Nothing downstream changes.

## What this does not cover

- No-ground-truth / LLM-as-judge scoring — Week 9.
- Concurrency / throughput under load — exercise 3, and Week 10.
- Retrieval-augmented tasks — Week 6.
