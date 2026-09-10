# Day 17 — Chunking strategies

The ingest stage decides everything downstream: if the answer's text isn't in a retrievable
chunk, no prompt or model recovers it. Six chunking strategies built from scratch and measured
on a fixed QA set.

## Learning objectives

By the end of the hour you should be able to:

1. Explain the retrievability vs answerability tradeoff that chunk size controls.
2. Implement fixed-size, sentence, paragraph/section, recursive, and semantic chunking.
3. Measure retrieval quality (recall@k, MRR) per strategy on a QA set and read the results.
4. Explain what overlap fixes and costs, and when semantic chunking earns its extra compute.
5. Apply metadata tagging and small-to-big (parent-document) retrieval.

## Agenda (60 min)

| # | Segment | Time |
| - | ------- | ---- |
| 0 | Why chunk at all, and what "good" means | 4 min |
| 1 | The corpus, the QA set, the metric | 8 min |
| 2 | Fixed-size, and the boundary problem | 10 min |
| 3 | Structure-aware: sentence, paragraph, recursive | 14 min |
| 4 | Semantic chunking | 10 min |
| 5 | Chunk size sweep + metadata + parent-doc retrieval | 11 min |
| 6 | Exercises and self-check quiz | 3 min |

## Setup

```bash
source ../../../.venv/bin/activate
```

Uses `sentence-transformers` (MiniLM). No LLM — retrieval metrics only. Runs in ~1 minute.

## Run it

```bash
python -m jupyterlab projects/week-06-rag/day-17-chunking-strategies/lesson.ipynb
```

Pinned to the **Python (ai-upskill)** kernel. Ships with outputs populated.

## Source material

- LangChain, "Recursively split by character" / text splitters — https://python.langchain.com/docs/concepts/text_splitters/
- Greg Kamradt, "5 Levels of Text Splitting" — https://github.com/FullStackRetrieval-com/RetrievalTutorials
- LlamaIndex, "Node parsers & chunking" — https://docs.llamaindex.ai/en/stable/module_guides/loading/node_parsers/
- "Semantic chunking" — https://python.langchain.com/docs/how_to/semantic-chunker/

## Files

- `lesson.ipynb` — the guided lesson.
- `NOTES.md` — one-page cheat sheet.
- `requirements.txt` — sentence-transformers, numpy, matplotlib, tiktoken.
