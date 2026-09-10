# Week 5 Lab — Knowledge Base Search

## The brief

The help-centre has ~1,200 articles. Support agents need a search box that finds the right
article by *meaning*, not keyword — and still nails exact things like error codes and SKUs.
Build the retrieval engine: an ANN index, BM25, and a hybrid retriever, evaluated on a
labelled query set.

```
articles ─▶ Indexer.build() ─▶ {FlatIndex | IVFIndex}   +   BM25
query ─▶ HybridRetriever.search(k) ─▶ ranked article ids   (RRF of dense + lexical)
```

## What you implement (`src/kbsearch/`)

| File | TODOs |
| ---- | ----- |
| `index.py` | `IVFIndex.build`, `IVFIndex.search`, `BM25.index`, `BM25.search` |
| `retriever.py` | `HybridRetriever.search` (Reciprocal Rank Fusion) |
| `evaluate.py` | `recall_at_k`, `mrr` |

`FlatIndex`, chunking and the embedder plumbing are given.

## Acceptance criteria

- `pytest -q` green: on synthetic clustered vectors `IVFIndex` recall@10 ≥ 0.9 at
  `nprobe=4`; BM25 ranks an exact-term query correctly where dense retrieval blurs it; RRF
  fuses two rankings without needing score calibration.
- `LLM_LIVE=1 pytest -q -m live`: with a real embedder (`openai` if a key is set, else the
  free local model) the `HybridRetriever` gets **recall@5 ≥ 0.8** on the 15 labelled queries,
  and beats pure-dense on the exact-term subset.

Covers Day 13 (semantic search, BM25, RRF), Day 14 (IVF/HNSW).
