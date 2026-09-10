# Day 20 — Frameworks: LangChain vs LlamaIndex

Build tiny versions of each framework's core abstraction so the real APIs stop being magic,
map your Week 6–7 code onto them, and learn how to choose.

## Learning objectives

By the end of the hour you should be able to:

1. Explain LCEL: a `Runnable` with `.invoke()` and `|` composition (`prompt | llm | parser`).
2. Explain LlamaIndex's `Index` → `QueryEngine` model and what `from_documents` /
   `as_query_engine` hide.
3. Recognise which framework leans retrieval-first (LlamaIndex) vs orchestration-first
   (LangChain / LangGraph).
4. Choose between LangChain, LlamaIndex, and rolling your own for a given app — and know when
   they compose.
5. Keep the eval harness outside the framework.

## Agenda (60 min)

| # | Segment | Time |
| - | ------- | ---- |
| 0 | What a framework gives you (and takes) | 4 min |
| 1 | LangChain's core idea: composable `Runnable`s (LCEL) | 14 min |
| 2 | LangChain agents + tools + memory | 10 min |
| 3 | LlamaIndex's core idea: index → query engine | 14 min |
| 4 | The real quickstarts, side by side | 10 min |
| 5 | Choosing: LangChain vs LlamaIndex vs neither | 5 min |
| 6 | Exercises and self-check quiz | 3 min |

## Setup

```bash
source ../../../.venv/bin/activate
```

Uses `sentence-transformers` (MiniLM). The frameworks themselves are **not installed** — we
build ~20-line versions of their core abstractions and show the real quickstart code as
reference. This keeps the lesson runnable and dependency-free.

## Run it

```bash
python -m jupyterlab projects/week-07-agents/day-20-agent-frameworks/lesson.ipynb
```

Pinned to the **Python (ai-upskill)** kernel. Ships with outputs populated.

## Source material

- LangChain, "Conceptual guide" / LCEL — https://python.langchain.com/docs/concepts/
- LangGraph docs — https://langchain-ai.github.io/langgraph/
- LlamaIndex, "Starter tutorial" — https://docs.llamaindex.ai/en/stable/getting_started/starter_example/
- LlamaIndex, "High-level concepts" — https://docs.llamaindex.ai/en/stable/getting_started/concepts/

## Files

- `lesson.ipynb` — the guided lesson.
- `NOTES.md` — one-page cheat sheet.
- `requirements.txt` — sentence-transformers, numpy.
