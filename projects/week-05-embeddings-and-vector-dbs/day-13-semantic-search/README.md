# Day 13 — Semantic search from scratch

How "search by meaning" works: text → vectors so that similar meaning lands at nearby points,
then rank by cosine similarity. Word vectors built by hand from a co-occurrence matrix, then
compared to a real sentence-embedding model.

## Learning objectives

By the end of the hour you should be able to:

1. Explain why bag-of-words / one-hot representations can't capture synonymy.
2. Build dense word vectors from a co-occurrence matrix + PPMI + SVD (the Word2Vec objective
   without the SGD).
3. Choose a similarity metric and explain why normalised embeddings + inner product = cosine.
4. Compare BM25 keyword search with dense retrieval, and combine them with Reciprocal Rank
   Fusion.
5. Explain the exact-vs-approximate (ANN) search tradeoff and its two knobs (bucket size,
   number of probes).

## Agenda (60 min)

| # | Segment | Time |
| - | ------- | ---- |
| 0 | Why keyword search misses | 4 min |
| 1 | One-hot → the synonymy wall | 8 min |
| 2 | Distributional hypothesis: co-occurrence → PPMI → SVD → dense vectors | 14 min |
| 3 | Similarity metrics: cosine vs dot vs Euclidean | 10 min |
| 4 | BM25 vs semantic vs hybrid (RRF) | 12 min |
| 5 | Approximate nearest-neighbour search | 9 min |
| 6 | Exercises and self-check quiz | 3 min |

## Setup

```bash
source ../../../.venv/bin/activate
```

Uses `sentence-transformers` (`all-MiniLM-L6-v2`, ~90 MB, downloads once) for the real-model
comparison; everything else is numpy.

## Run it

```bash
python -m jupyterlab projects/week-05-embeddings-and-vector-dbs/day-13-semantic-search/lesson.ipynb
```

Pinned to the **Python (ai-upskill)** kernel. Ships with outputs populated.

## Source material

- Firth (1957) / the distributional hypothesis; Mikolov et al., "Efficient Estimation of Word
  Representations" (Word2Vec) — https://arxiv.org/abs/1301.3781
- Levy & Goldberg, "Neural Word Embedding as Implicit Matrix Factorization" (SVD ≈ Word2Vec) — https://papers.nips.cc/paper/5477
- Robertson & Zaragoza, "The Probabilistic Relevance Framework: BM25 and Beyond"
- Cormack et al., "Reciprocal Rank Fusion" — https://plg.uwaterloo.ca/~gvcormac/cormacksigir09-rrf.pdf
- `sentence-transformers` docs — https://www.sbert.net/

## Files

- `lesson.ipynb` — the guided lesson.
- `NOTES.md` — one-page cheat sheet.
- `requirements.txt` — numpy, matplotlib, sentence-transformers.
