# Day 18 — Build a RAG pipeline — cheat sheet

## The one-sentence version

Assemble Days 13–17 into one `RAGPipeline` (chunk → embed → DuckDB store → hybrid retrieve →
grounded prompt → generate → cite), gate out-of-scope questions on retrieval score, and score
it on correctness + faithfulness + abstention + cost with a harness kept *outside* the
pipeline.

## The pipeline (components ↔ days)

| Stage | From | Here |
| ----- | ---- | ---- |
| chunk | Day 17 | recursive splitter, ~400 chars |
| embed | Day 13 | `all-MiniLM-L6-v2`, normalised |
| store | Day 15 | DuckDB + HNSW index |
| retrieve | Day 13 | vector + BM25, fused with RRF |
| gate | Day 16 | if top vscore < ~0.25 → "I don't know" (no LLM call) |
| generate | Week 8 | Anthropic Messages API (local fallback offline) |
| cite | Day 16 | extract `[n]`, or post-hoc attribution |

## The eval dimensions

| Metric | Definition | Bounded by |
| ------ | ---------- | ---------- |
| correctness | answer contains the gold fact | the generator |
| source precision | right doc in top-k | the retriever |
| **faithfulness** | gold fact **is in** the retrieved context | the retriever — the real ceiling |
| oos_abstention | says "I don't know" for out-of-scope | the gate + prompt |
| false_abstention | refuses a real question | gate threshold too high |

**Tune on retrieval metrics first** (fast, no LLM): faithfulness + source precision + gate
behaviour across mode × k. Then run the full LLM eval on your top 1–2 configs.

## Hybrid retrieval (RRF)

```python
vr = {i: r for r, i in enumerate(argsort(-vector_scores))}
br = {i: r for r, i in enumerate(argsort(-bm25_scores))}
fused = {i: 1/(60+vr[i]) + 1/(60+br[i]) for i in all_chunks}
```
BM25 catches exact terms ("$350", "429") dense retrieval blurs; RRF needs no score calibration.

## Cost

RAG prompts are **input-heavy** (k chunks + instructions on every call, short answer). Input
price and prompt caching dominate. `mean_ctx_tokens × k` is the lever; cache the static system
prompt.

## Rules

- Score **format/faithfulness/correctness separately** — different fixes.
- Keep the eval harness outside the framework/pipeline so it survives a swap.
- A correct-but-unfaithful answer is a hallucination waiting for the model's prior to be wrong.
- Feed the disagreement set / thumbs-down back into the eval (Day 25–27).

## What this does not cover

- Rerankers, query rewriting, HyDE, multi-hop — exercises / Week 7.
- LLM-as-judge scoring — Day 25.
- Deployment — Week 10.
