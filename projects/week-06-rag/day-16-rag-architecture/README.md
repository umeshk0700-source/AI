# Day 16 — RAG architecture end-to-end

Build every stage of Retrieval-Augmented Generation from scratch over a small document set —
chunk, embed, store, retrieve, augment, generate, cite — then break each stage to see what it
contributes.

## Learning objectives

By the end of the hour you should be able to:

1. Draw the RAG pipeline and name what each stage does (offline ingest vs per-query).
2. Explain why `k` (retrieved chunks) is a tradeoff in both directions.
3. Write a RAG system prompt that grounds the model and makes it refuse when context is thin.
4. Demonstrate grounded vs no-context vs wrong-context generation and the refusal payoff.
5. Extract citations, check citation faithfulness, and add a similarity gate for out-of-scope
   questions.
6. Diagnose which pipeline stage caused a bad answer.

## Agenda (60 min)

| # | Segment | Time |
| - | ------- | ---- |
| 0 | The pipeline, and the failure it fixes | 4 min |
| 1 | Ingest: load + chunk + embed + store | 12 min |
| 2 | Retrieve: top-k, and why k matters | 10 min |
| 3 | Augment: building the prompt | 10 min |
| 4 | Generate: grounded vs ungrounded | 12 min |
| 5 | Citations + the "irrelevant context" problem | 9 min |
| 6 | Exercises and self-check quiz | 3 min |

## Setup

```bash
source ../../../.venv/bin/activate
```

Uses `sentence-transformers` (MiniLM) for retrieval and `Qwen2.5-0.5B-Instruct` for generation
— all local, all offline. Day 18 swaps in the Anthropic API. A full pass is ~3 minutes on CPU.

## Run it

```bash
python -m jupyterlab projects/week-06-rag/day-16-rag-architecture/lesson.ipynb
```

Pinned to the **Python (ai-upskill)** kernel. Ships with outputs populated.

## Source material

- Lewis et al., "Retrieval-Augmented Generation for Knowledge-Intensive NLP Tasks" (2020) — https://arxiv.org/abs/2005.11401
- Anthropic, "Retrieval augmented generation" — https://docs.anthropic.com/en/docs/build-with-claude/retrieval-augmented-generation
- "Lost in the Middle" (Day 04) — https://arxiv.org/abs/2307.03172
- Gao et al., "Retrieval-Augmented Generation for Large Language Models: A Survey" — https://arxiv.org/abs/2312.10997

## Files

- `lesson.ipynb` — the guided lesson.
- `NOTES.md` — one-page cheat sheet.
- `requirements.txt` — sentence-transformers, transformers, torch, numpy, matplotlib.
