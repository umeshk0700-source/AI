# Day 18 — Build a RAG pipeline (hands-on)

Assemble Days 13–17 into one working system: a `RAGPipeline` class over a real document set,
with the Anthropic API doing generation (local fallback offline) and a small eval harness that
scores answer correctness, faithfulness, abstention, and cost.

## Learning objectives

By the end of the hour you should be able to:

1. Wire chunking → embedding → DuckDB vector store → hybrid retrieval (BM25 + dense, RRF) →
   grounded prompt → generation into one class.
2. Add a relevance gate so out-of-scope questions get a clean refusal without an LLM call.
3. Write the Anthropic Messages API generation call (system prompt, `messages`, `usage`).
4. Build an eval harness that scores correctness, source precision, faithfulness, and
   abstention separately — and tune on the retrieval metrics first (no LLM) before the full run.
5. Reason about RAG cost: input-token-heavy prompts, and where prompt caching helps.

## Agenda (60 min)

| # | Segment | Time |
| - | ------- | ---- |
| 0 | The pieces we're assembling | 3 min |
| 1 | Ingest: chunk + embed + store (DuckDB) | 10 min |
| 2 | Retrieve: hybrid (vector + BM25 + RRF) | 12 min |
| 3 | Generate: the Anthropic Messages API | 12 min |
| 4 | The `RAGPipeline` class | 8 min |
| 5 | The eval harness: correctness, faithfulness, abstention, cost | 12 min |
| 6 | Exercises and self-check quiz | 3 min |

## Setup

Runs in the shared uv venv at the repo root (see [the root README](../../../README.md)):

```bash
source ../../../.venv/bin/activate
```

Runs fully offline against a local model (`Qwen2.5-0.5B-Instruct`). Set `ANTHROPIC_API_KEY`
and swap the `generate()` backend to run the real thing — the code path is identical.

## Run it

```bash
python -m jupyterlab projects/week-06-rag/day-18-rag-pipeline/lesson.ipynb
```

Pinned to the **Python (ai-upskill)** kernel. Ships with outputs populated.

## Source material

- Lewis et al., "Retrieval-Augmented Generation for Knowledge-Intensive NLP Tasks" — https://arxiv.org/abs/2005.11401
- Anthropic, "Retrieval augmented generation" — https://docs.anthropic.com/en/docs/build-with-claude/retrieval-augmented-generation
- Days 13–17 (embeddings, vector DBs, chunking) and Day 06 (bake-off harness).

## Files

- `lesson.ipynb` — the guided lesson.
- `NOTES.md` — one-page cheat sheet.
- `requirements.txt` — sentence-transformers, duckdb, transformers, torch, numpy, matplotlib.
