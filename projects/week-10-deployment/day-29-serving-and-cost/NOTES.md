# Day 29 — Model serving & cost — cheat sheet

## The one-sentence version

Decode (one token at a time, bandwidth-bound) dominates latency and cost; every lever is
"fewer input tokens (caching)" or "fewer output tokens (discipline / smaller model /
batching)", and you never run a replica above ~75% utilisation.

## Prefill vs decode

| Phase | Bound by | Cost ∝ | Speed |
| ----- | -------- | ------ | ----- |
| Prefill | compute (parallel) | input tokens | fast |
| Decode | memory bandwidth (sequential) | output tokens | **slow — the wall-clock** |

## Throughput knobs (they fight)

- **Batch size ↑** → total throughput ↑, per-request latency ↑ (decode pool split N ways).
- **Context length ↑** → concurrent requests ↓: `(GPU_mem − weights) / (ctx_tokens ·
  kv_bytes_per_token)` caps it, regardless of compute. (Long context is a *memory* problem →
  priced higher.)
- **Continuous batching** (vLLM/TGI/TRT-LLM) — add/remove requests from the running batch each
  step → 2–4× real throughput vs static batching (no padding waste).

## Capacity (Erlang-C)

Offered load `a = λ · service_s` Erlangs → need `c > a` replicas *just for stability*. p95
latency hockey-sticks as utilisation → 1 (`1/(cμ − λ)` term). **Operate at ≤ 75%
utilisation** — the last 20% of nominal capacity is where the tail breaks.

Autoscaling: scale on a **leading signal** (queue depth / concurrency / tokens-per-sec), not
lagging GPU util; account for **minutes** of scale-up lag (image + weights); keep a replica
floor; scale down slowly.

## Cost levers (apply top-down; measure after each)

| Lever | Saving | Free? |
| ----- | ------ | ----- |
| 1. Prompt caching (stable prefix first) | 30–90% of input | ✅ |
| 2. Input hygiene (trim chunks, compact history) | 10–40% of input | ✅ |
| 3. Output discipline (`max_tokens`, `stop`, "be concise") | 20–50% of output | ✅ |
| 4. Semantic cache (embed query, serve near-hits) | = hit rate | ~ |
| 5. Model right-sizing / cascade (Day 11) | 40–80% | trades quality |
| 6. Batch API (async traffic) | ~50% on that slice | ✅ |
| 7. Lower `effort` on routes that don't need it | 10–40% | trades quality |
| 8. (self-host) quantization / spot / continuous batching | 30–70% infra | high effort |

**Free wins before tradeoffs.** 5 and 7 must be measured against your eval (Day 26).

## Self-host vs API

Raw-token break-even is at *sustained very high volume* (~hundreds of M–B tokens/month). The
**all-in** break-even is far higher — add an ML-serving/on-call team, load-testing,
autoscaling, model updates, security, fine-tune evals. Self-host for hard data-residency, a
heavily-used fine-tune, or genuinely enormous steady volume.

## Numbers from the toy

- Utilisation cliff: c=13 (98% util) → p95 25s; c=17 (75%) → p95 2.6s, meets a 4s SLA.
- Stacked levers (caching + semantic + output discipline): $386k → $141k/month, 35 → 16 replicas.

## What this does not cover

- Deploying the actual endpoint — Day 30.
- GPU procurement, MIG partitioning, speculative decoding internals.
