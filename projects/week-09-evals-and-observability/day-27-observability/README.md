# Day 27 — Observability: logging & tracing

The eval harness (Day 26) tells you about a frozen set. Production needs observability: a user
reports a bad answer and you must see every stage's input and output after the fact. Build a
tracer from scratch, instrument a RAG pipeline, render the trace tree, walk the "find the bug"
workflow, then map it onto LangSmith / Langfuse / OpenTelemetry.

## Learning objectives

By the end of the hour you should be able to:

1. Name the three pillars (logs, traces, metrics) and why the trace matters most for LLM apps.
2. Build a span/trace data model with a `contextvar` for nesting and a `with span(...)`
   context manager.
3. Instrument a pipeline without changing its logic; render the trace tree and a flat export.
4. Decide what to capture (and redact) at each stage — ids and scores, not walls of text.
5. Debug from a trace: find the first span whose output is wrong given a correct input.
6. Apply redaction, sampling, and retention; recognise what LangSmith / Langfuse / Phoenix add.

## Agenda (60 min)

| # | Segment | Time |
| - | ------- | ---- |
| 0 | The three pillars: logs, traces, metrics | 4 min |
| 1 | A trace is nested spans — build a tracer | 14 min |
| 2 | Instrument a RAG pipeline | 12 min |
| 3 | What to capture at each stage | 10 min |
| 4 | Debugging from a trace | 10 min |
| 5 | Redaction, sampling, cost; the real tools | 7 min |
| 6 | Exercises and self-check quiz | 3 min |

## Setup

```bash
source ../../../.venv/bin/activate
```

Uses `sentence-transformers` (MiniLM). The tracer is ~40 lines of stdlib; the pipeline is a
mock so the trace is the focus.

## Run it

```bash
python -m jupyterlab projects/week-09-evals-and-observability/day-27-observability/lesson.ipynb
```

Pinned to the **Python (ai-upskill)** kernel. Ships with outputs populated.

## Source material

- OpenTelemetry — GenAI semantic conventions — https://opentelemetry.io/docs/specs/semconv/gen-ai/
- LangSmith docs — https://docs.smith.langchain.com/
- Langfuse docs — https://langfuse.com/docs
- Arize Phoenix — https://docs.arize.com/phoenix

## Files

- `lesson.ipynb` — the guided lesson.
- `NOTES.md` — one-page cheat sheet.
- `requirements.txt` — sentence-transformers, numpy.
