# Day 15 — pgvector hands-on — cheat sheet

## The one-sentence version

`CREATE EXTENSION vector`, an `embedding vector(384)` column next to your normal columns, an
`hnsw` index, and `ORDER BY embedding <=> $1 LIMIT k` — semantic search as plain SQL, inside
the database you already run.

## Data model

```sql
CREATE EXTENSION IF NOT EXISTS vector;
CREATE TABLE docs (
  id bigserial PRIMARY KEY, title text, category text, body text,
  embedding vector(384)
);
CREATE INDEX docs_category_idx ON docs (category);   -- for filtered search
```

## Distance operators (smaller = closer)

| Op | Meaning | opclass for the index | Use for |
| -- | ------- | --------------------- | ------- |
| `<->` | L2 / Euclidean | `vector_l2_ops` | non-normalised vectors |
| `<=>` | cosine distance (`1 − cos`) | `vector_cosine_ops` | **normalised text embeddings** |
| `<#>` | negative inner product | `vector_ip_ops` | normalised + max speed |

The `ORDER BY` expression must match the index opclass, and the query **must** be
`ORDER BY <dist> LIMIT k` — a bare `WHERE dist < r` can't use the ANN index.

## Indexes

```sql
-- IVFFlat: quick/small build, needs data loaded first, needs `lists`
CREATE INDEX ON docs USING ivfflat (embedding vector_cosine_ops) WITH (lists = 100);
SET ivfflat.probes = 10;              -- query-time recall dial

-- HNSW: slower/bigger build, higher recall@latency, no training, incremental
CREATE INDEX ON docs USING hnsw (embedding vector_cosine_ops)
  WITH (m = 16, ef_construction = 64);
SET hnsw.ef_search = 40;              -- query-time recall dial
```

## Filtered + hybrid

```sql
SELECT id, title FROM docs
WHERE category = $2                   -- plain predicate; add a btree index on category
ORDER BY embedding <=> $1 LIMIT 5;
```
pgvector ≥ 0.8 does an *iterative* index scan for selective filters. Hybrid = Postgres
`tsvector`/`ts_rank` (or `pg_search`) for keywords + fuse with RRF (Day 13). Native
keyword+vector in one query → Weaviate (Day 14).

## Deploying on RDS

- Available on RDS PostgreSQL ≥ 15.2 and Aurora — just `CREATE EXTENSION`.
- **Load rows first**, `SET maintenance_work_mem = '2GB'`, *then* `CREATE INDEX ... hnsw`
  (or `CREATE INDEX CONCURRENTLY`).
- HNSW index wants to live in RAM: index bytes ≈ `rows · (1.1·dim·4 + m·8)`
  (5M × 384 × m16 ≈ 3.3 GB fp32, 1.9 GB with `halfvec`). Size the instance so table+index
  fit in cache.
- `hnsw.ef_search` is a session GUC — set per query class.
- RDS Proxy / PgBouncer for pooling. `db.t4g.medium` Multi-AZ ≈ $100–150/mo to start.
- Index dim limit 2000; use `halfvec` (fp16) to halve storage/memory.

## DuckDB ↔ pgvector map (for the notebook)

| pgvector | DuckDB (vss) |
| -------- | ------------ |
| `<=>` | `array_cosine_distance` |
| `<->` | `array_distance` |
| `vector(384)` | `FLOAT[384]` |
| `USING hnsw (... vector_cosine_ops)` | `USING HNSW (...) WITH (metric='cosine')` |
| `SET hnsw.ef_search` | `SET hnsw_ef_search` |

## What this does not cover

- The full RAG pipeline (chunking → retrieve → generate) — Week 6.
- Rerankers — Week 6.
- Multi-tenant partitioning strategies at scale — mentioned only.
