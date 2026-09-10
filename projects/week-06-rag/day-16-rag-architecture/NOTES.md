# Day 16 — RAG architecture — cheat sheet

## The one-sentence version

RAG = chunk → embed → store (offline); then embed query → retrieve top-k → build a
"answer only from this context, cite it, refuse if absent" prompt → generate → extract
citations (per query).

## The pipeline

```
INGEST (once):  documents → chunk → embed → vector store
QUERY (each):   query → embed → retrieve top-k → build prompt → LLM → answer + [citations]
```

## The `k` tradeoff

- **k too small** → the answer's chunk isn't retrieved → "I don't know" or wrong.
- **k too large** → irrelevant chunks dilute the prompt, trigger lost-in-the-middle (Day 04),
  cost tokens/latency.
- Retrieval-recall usually plateaus by k≈3–5 on a small KB; raising k past that adds noise, not
  answers. Rerank the top-20 down to 3–5 instead.

## The system prompt (always)

```
Answer using ONLY the numbered context passages. Cite passage numbers like [1][2].
If the context does not contain the answer, reply exactly:
"I don't know based on the provided context."
```

## Grounded vs not (the demo)

| Setup | Behaviour |
| ----- | --------- |
| Good retrieval + strict prompt | answers from the passage, cites it |
| No retrieval | fabricates a plausible-but-wrong policy |
| Wrong retrieval + strict prompt | should refuse ("I don't know…") — the payoff |

## Out-of-scope questions

Add a **similarity gate**: if `top_score < ~0.3`, skip the LLM and return "no relevant info".
Plus: strict prompt, reranker, let the model hedge.

## Where each stage fails

| Stage | Failure → fix |
| ----- | ------------- |
| Chunk | splits a fact / dilutes → Day 17 (strategy, overlap) |
| Embed | domain mismatch → domain-tuned embeddings, hybrid BM25+vector |
| Retrieve k↓ | answer missing → raise k, rerank |
| Retrieve k↑ | noise, lost-in-middle → rerank to 3–5, reorder key chunk to first/last |
| Augment | weak prompt → strict "only from context" + refuse |
| Generate | weak model → bigger model; bad citations → check faithfulness |
| Generate | no gate → confident OOS answers → similarity threshold |

## Citation faithfulness

A citation is *faithful* if the cited passage actually contains the stated fact. Models cite
plausibly even when wrong — check by string-matching the key fact against the cited chunk.

## Code you will reuse

```python
def retrieve(query, k=3):
    q = embedder.encode([query], normalize_embeddings=True)[0]
    order = np.argsort(-(CHUNK_EMB @ q))[:k]
    return [dict(CHUNKS[i], score=float((CHUNK_EMB @ q)[i])) for i in order]
```

## What this does not cover

- Chunking strategy in depth — Day 17.
- Real API generation + a proper eval harness — Day 18 / Week 9.
- Query rewriting, HyDE, multi-hop RAG, agentic retrieval — Week 7.
