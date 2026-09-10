# Day 14 — Vector databases: pgvector vs Pinecone vs Weaviate

Build the two ANN index families that matter (**IVF** and **HNSW**) from scratch, measure the
recall / latency / memory tradeoff, then map that understanding onto the real products.

## Learning objectives

By the end of the hour you should be able to:

1. Say what a vector DB adds over `np.argsort(D @ q)`: sublinear ANN index, metadata filtering,
   updates, persistence, scale.
2. Explain IVF (cluster + probe `nprobe` cells) and HNSW (navigable graph, `M` links, `ef`
   beam), including why IVF needs retraining and HNSW doesn't.
3. Read a recall/latency frontier and pick an operating point.
4. Explain the three metadata-filter strategies (pre / post / filtered-ANN) and their failure
   modes.
5. Choose between pgvector, Pinecone, and Weaviate for a given app, and name a runner-up.

## Agenda (60 min)

| # | Segment | Time |
| - | ------- | ---- |
| 0 | What a vector DB does beyond `np.argsort` | 4 min |
| 1 | Flat index — the exact baseline | 6 min |
| 2 | IVF: cluster, then probe a few clusters | 14 min |
| 3 | HNSW: a navigable graph | 14 min |
| 4 | Metadata filtering: the hard part | 10 min |
| 5 | pgvector vs Pinecone vs Weaviate — choosing | 9 min |
| 6 | Exercises and self-check quiz | 3 min |

## Setup

```bash
source ../../../.venv/bin/activate
```

Runs fully offline — IVF and HNSW built by hand in numpy over a synthetic 8k-vector corpus.
A full pass (including the HNSW builds in the exercises) is ~90 seconds.

## Run it

```bash
python -m jupyterlab projects/week-05-embeddings-and-vector-dbs/day-14-vector-databases/lesson.ipynb
```

Pinned to the **Python (ai-upskill)** kernel. Ships with outputs populated.

## Source material

- Malkov & Yashunin, "Efficient and robust approximate nearest neighbor search using HNSW" — https://arxiv.org/abs/1603.09320
- Jégou et al., "Product Quantization for Nearest Neighbor Search" (IVF/PQ lineage) — https://ieeexplore.ieee.org/document/5432202
- pgvector — https://github.com/pgvector/pgvector
- Pinecone docs — https://docs.pinecone.io/ ; Weaviate docs — https://weaviate.io/developers/weaviate
- ann-benchmarks — https://ann-benchmarks.com/

## Files

- `lesson.ipynb` — the guided lesson.
- `NOTES.md` — one-page cheat sheet.
- `requirements.txt` — numpy, matplotlib (base env).
