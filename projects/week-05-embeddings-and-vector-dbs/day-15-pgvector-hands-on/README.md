# Day 15 — pgvector hands-on

Put embeddings in a real database and query them with SQL: the `vector` column, the distance
operators (`<->`, `<=>`, `<#>`), `ivfflat` vs `hnsw` indexes, metadata-filtered and hybrid
search — then the exact script to run it on AWS RDS.

The notebook executes against **DuckDB** (in-process, no server) whose vector SQL mirrors
pgvector almost line-for-line; every cell shows the pgvector SQL next to what we run.

## Learning objectives

By the end of the hour you should be able to:

1. Model documents + embeddings + metadata in one table with a `vector(384)` column.
2. Write a kNN query with the right distance operator and know why `ORDER BY <dist> LIMIT k`
   is what triggers the ANN index.
3. Choose between `ivfflat` and `hnsw`, build the index, and tune `ef_search` / `probes`.
4. Do metadata-filtered similarity search and hybrid (keyword + vector) fusion in SQL.
5. Deploy the whole thing on RDS: extension, index build settings, instance sizing, `ef_search`
   as a session GUC, connection pooling, cost.

## Agenda (60 min)

| # | Segment | Time |
| - | ------- | ---- |
| 0 | Why a database, not a pickle file | 4 min |
| 1 | The data model: a `vector` column | 8 min |
| 2 | Distance operators + kNN queries | 12 min |
| 3 | Indexes: ivfflat vs hnsw | 12 min |
| 4 | Metadata-filtered and hybrid search | 12 min |
| 5 | Deploying on AWS RDS: the real script | 9 min |
| 6 | Exercises and self-check quiz | 3 min |

## Setup

```bash
source ../../../.venv/bin/activate
```

Uses `duckdb` (+ its `vss` HNSW extension, auto-installed) and `sentence-transformers`. No
Postgres server and no AWS account needed to run the notebook; the RDS section is copy-paste
for when you provision real infra.

## Run it

```bash
python -m jupyterlab projects/week-05-embeddings-and-vector-dbs/day-15-pgvector-hands-on/lesson.ipynb
```

Pinned to the **Python (ai-upskill)** kernel. Ships with outputs populated.

## Source material

- pgvector README (operators, index types, tuning) — https://github.com/pgvector/pgvector
- AWS, "Using pgvector on Amazon RDS for PostgreSQL" — https://docs.aws.amazon.com/AmazonRDS/latest/UserGuide/CHAP_PostgreSQL.html
- DuckDB `vss` extension — https://duckdb.org/docs/extensions/vss
- "pgvector performance" / index tuning posts — https://github.com/pgvector/pgvector#performance

## Files

- `lesson.ipynb` — the guided lesson.
- `NOTES.md` — one-page cheat sheet.
- `requirements.txt` — duckdb, sentence-transformers, numpy.
