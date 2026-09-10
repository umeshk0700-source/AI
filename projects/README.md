# AI Upskill — Daily Deep Dives

One concept per day, one hour each, learned by building it from scratch rather than reading about it.

Every day lives in its own folder with the same four files: a `README.md` with the agenda, a
`lesson.ipynb` you actually run, a `NOTES.md` cheat sheet to keep, and a `requirements.txt`.

## How to start a day

Open [_template/PROMPT.md](_template/PROMPT.md), copy the block, change the concept line, and paste it
into a new chat. Everything else is handled for you.

## Index

| Day | Concept | Folder | Status |
| --- | ------- | ------ | ------ |
| 01 | How text becomes numbers: tokenization, embeddings, Word2Vec | [day-01-text-to-numbers](day-01-text-to-numbers/) | Done |
| 02 | Attention mechanism: the core of transformers, from intuition to implementation | [day-02-attention-mechanism](day-02-attention-mechanism/) | Ready |
| 03 | Training paradigms: pretraining → fine-tuning → RLHF pipeline | [day-03-training-paradigms](day-03-training-paradigms/) | Ready |

## Environment

All days share one uv-managed venv at the repo root. See [the root README](../README.md) for
first-time setup; after that it is just:

```powershell
.venv\Scripts\activate
```

Notebooks are pinned to the **Python (ai-upskill)** kernel. Each day also keeps a
`requirements.txt` listing what that specific lesson needs, but the packages themselves are
installed once into the shared venv from the root `requirements.txt`.
