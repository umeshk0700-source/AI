# Day 29 — Model serving & cost at scale

Whichever door you picked (Day 28), you have to size and pay for the serving layer. This hour:
throughput fundamentals (prefill vs decode, batching, KV cache), how many replicas a latency
SLA needs, the cost levers ranked by savings, the self-host-vs-API break-even, and a runnable
calculator.

## Learning objectives

By the end of the hour you should be able to:

1. Explain the prefill (compute-bound, ∝ input) vs decode (bandwidth-bound, ∝ output) split
   and why decode dominates wall-clock and cost.
2. Reason about the batch-size ↔ latency ↔ throughput tradeoff and the KV-cache concurrency
   ceiling; explain what continuous batching fixes.
3. Size replicas for a p95 SLA with an Erlang-C model, and explain the utilisation cliff.
4. Rank and apply the cost levers (caching → hygiene → output discipline → semantic cache →
   right-sizing → batch), knowing which are free.
5. Compute the self-host vs API break-even and why the all-in break-even is much higher.

## Agenda (60 min)

| # | Segment | Time |
| - | ------- | ---- |
| 0 | Where the time and money go | 4 min |
| 1 | Throughput: prefill, decode, batching, the KV-cache ceiling | 14 min |
| 2 | Capacity: replicas for a p95 SLA | 12 min |
| 3 | Cost levers, ranked | 14 min |
| 4 | Self-host vs API break-even | 8 min |
| 5 | A serving cost calculator | 5 min |
| 6 | Exercises and self-check quiz | 3 min |

## Setup

```bash
source ../../../.venv/bin/activate
```

Runs offline — numpy calculators over illustrative hardware/pricing numbers (real numbers come
from load-testing your model + hardware).

## Run it

```bash
python -m jupyterlab projects/week-10-deployment/day-29-serving-and-cost/lesson.ipynb
```

Pinned to the **Python (ai-upskill)** kernel. Ships with outputs populated.

## Source material

- "Efficient Memory Management for LLM Serving with PagedAttention" (vLLM) — https://arxiv.org/abs/2309.06180
- Anthropic, cost optimization (`claude-api` skill → `shared/cost-optimization.md`).
- "LLM Inference Performance Engineering: Best Practices" (Databricks) — https://www.databricks.com/blog/llm-inference-performance-engineering-best-practices
- Erlang-C / queueing for capacity planning.

## Files

- `lesson.ipynb` — the guided lesson.
- `NOTES.md` — one-page cheat sheet.
- `requirements.txt` — numpy, matplotlib.
