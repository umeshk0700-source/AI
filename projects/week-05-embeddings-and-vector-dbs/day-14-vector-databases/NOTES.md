# Day 14 — Vector databases — cheat sheet

## The one-sentence version

A vector DB = an ANN index (IVF or HNSW) + metadata filtering + persistence + updates; pick
pgvector unless you've outgrown it, then Pinecone (scale/managed) or Weaviate (hybrid/OSS).

## The index families

| | **Flat** | **IVF** | **HNSW** |
| --- | --- | --- | --- |
| How | score every vector | k-means into `nlist` cells, search `nprobe` of them | greedy walk over a k-NN graph (`M` links/node) |
| Recall/speed dial | — | `nprobe` (per query) | `ef` (per query) |
| Training | none | **k-means** (retrain as data drifts) | none (incremental) |
| Build cost | none | medium | high |
| Memory overhead | none | small (centroids + lists) | large (`O(N·M)` graph) |
| Deletes | trivial | ok | awkward (tombstone + rebuild) |
| Good to | ~10⁵–10⁶ | 10⁶–10⁸ | 10⁶–10⁸, best recall@latency |

Rules of thumb: `nlist ≈ √N … 4√N`; tune `nprobe`/`ef` for ~0.95 recall on your data.
IVF's weakness: queries near cell boundaries (top-k spans multiple cells). HNSW's cost:
memory and build time.

## Metadata filtering — `nearest WHERE tenant = 42`

| Strategy | How | Fails when |
| -------- | --- | ---------- |
| Pre-filter | filter → exact search survivors | filter matches millions (back to brute force) |
| Post-filter | ANN → drop non-matches | selective filter → too few results, low recall |
| Over-fetch post-filter | fetch `k / selectivity · 1.5–2` | filter is *very* selective (0.1%) |
| **Filtered ANN** | index is filter-aware (Weaviate pre-filter, Qdrant payload index, pgvector iterative scan) | — (this is the good answer) |

## Choosing

1. **On Postgres, < few M vectors, want joins/transactions?** → **pgvector**. (Most apps.)
2. **Past ~10–50 M vectors, or want zero ops?** → **Pinecone** (or Aurora + pgvector, Turbopuffer).
3. **Want native hybrid (BM25+vector), OSS engine, built-in modules?** → **Weaviate** (or Qdrant).
4. **Prototype / notebook / small app?** → **Chroma**, FAISS, LanceDB.

Also: **Qdrant** (Rust, great filtered search), **Milvus** (very large scale), **FAISS**
(library, no persistence/filter), **Turbopuffer/LanceDB** (object-storage-backed, cheap at rest).

## What to actually measure (before committing)

recall@k and p95 latency **on your data, at your filter selectivity, at your scale** + cost at
that scale + fit with existing ops. Public benchmarks (ann-benchmarks.com) = shortlist only.

## Numbers from the toy (8k vectors, 50 clusters)

- IVF nlist=64: nprobe=2 → recall 0.99 scanning 3% of the corpus.
- HNSW: ef 8→128 → recall 0.96→0.999, latency 0.3→1.5 ms/query.
- HNSW graph memory: M=8 → 17%, M=32 → 67% of the raw vector memory.

## What this does not cover

- Product quantization / scalar quantization (compress vectors) — mentioned only.
- The SQL surface of pgvector — Day 15.
- Chunking, reranking, the full RAG pipeline — Week 6.
