# Week 6 Lab — Policy Assistant (production RAG)

## The brief

Employees keep asking HR the same handbook questions. Build the RAG service behind a
`/ask` bot: it must answer **only from the handbook**, cite the section, and say "I don't
know" when the handbook doesn't cover the question — no confident guesses.

```
handbook docs ─▶ RAGPipeline(embedder, llm).ingest()
question ─▶ .answer() ─▶ Answer{ text, sources[], gated, confidence }
                          gate: if top similarity < min_score -> refuse, no LLM call
```

## What you implement (`src/rag/`)

| File | TODOs |
| ---- | ----- |
| `pipeline.py` | `RAGPipeline._retrieve`, `._build_prompt`, `._attribute`, `.answer` |
| `evaluate.py` | `faithfulness`, `RAGEval.run` |

Chunking, embedding and the relevance-gate threshold check are given.

## Acceptance criteria

- `pytest -q` green: the gate refuses (and makes **no** LLM call) when the best chunk is weak;
  the prompt contains the retrieved context and the "answer only from context / cite" rules;
  `_attribute` maps an answer sentence back to its supporting chunk; `faithfulness` catches a
  claim no chunk supports (tested with a `FakeLLM`).
- `LLM_LIVE=1 pytest -q -m live`: real Claude + real embeddings over a 6-section handbook —
  correctness ≥ 0.7, faithfulness ≥ 0.9, out-of-scope abstention = 1.0, cost < $0.05.

Covers Day 16 (RAG end-to-end), Day 17 (chunking), Day 18 (pipeline + eval).
