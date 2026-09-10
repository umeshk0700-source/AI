# Day 13 — Semantic search — cheat sheet

## The one-sentence version

Embed text so that similar meaning → nearby vectors; retrieve by cosine similarity (= inner
product on normalised vectors); use ANN indexes past ~10⁵ vectors and hybrid (BM25 + dense) for
robustness.

## Why one-hot / bag-of-words fails

Distinct words are orthogonal dimensions → `cos(refund, money) = 0`, same as `cos(refund,
banana)`. No notion that words relate.

## Dense vectors from scratch

1. **Co-occurrence matrix** `C[word, context]` over a corpus (sliding window).
2. **PPMI** re-weight: `max(0, log( C·total / (row·col) ))` — down-weights frequent words.
3. **Truncated SVD**: `word_vecs = U[:, :K] · S[:K]` — the compressed rows are the embeddings.

This is Word2Vec / GloVe's objective; they use SGD instead of SVD, and billions of tokens
instead of 30 sentences (which is why a real model like `all-MiniLM-L6-v2` goes 5/5 where the
toy gets 2/5).

## Similarity metrics

| Metric | Formula | Sensitive to |
| ------ | ------- | ------------ |
| Dot | `a·b` | direction + magnitude |
| Cosine | `a·b / (‖a‖‖b‖)` | direction only |
| Euclidean | `‖a−b‖` | absolute position |

On **L2-normalised** vectors all three give the **same ranking** (`‖a−b‖² = 2 − 2·a·b`). So:
normalise once, then a single matmul `D @ q` = cosine. Vector DBs do exactly this.

## BM25 vs dense vs hybrid

- **BM25** (keyword, TF-IDF-ish) wins on exact/rare terms: codes, names, error strings, jargon.
- **Dense** wins on paraphrase / no lexical overlap ("money back" → "refund").
- **Hybrid** via **Reciprocal Rank Fusion**: `score(d) = Σ_retrievers 1/(c + rank_r(d))`,
  `c≈60`. Combines *ranks*, not scores → no calibration needed. Production RAG default.

## ANN (approximate nearest neighbour)

Exact search is `O(N·d)` per query. ANN checks a fraction of vectors, trading recall for speed.
Toy LSH: `L` hash tables of `p` random-projection planes; candidates = union of the query's
buckets across tables.

- more planes → smaller buckets → faster, lower recall
- more tables → more buckets probed → recall back up, higher cost

(Toy sweep: recall 0.09 → 0.92 as tables 1 → 20.) Real structures: IVF, HNSW — Day 14.

## Code you will reuse

```python
D = model.encode(docs, normalize_embeddings=True)     # N x d, unit norm
def search(query, k=5):
    q = model.encode([query], normalize_embeddings=True)[0]
    return np.argsort(-(D @ q))[:k]                    # one matmul = cosine ranking
```

## What this does not cover

- Vector DB internals, metadata filtering, index choice — Day 14.
- Chunking documents for retrieval — Day 17 (Week 6).
- Rerankers (cross-encoders) — mentioned; used in Week 6.
