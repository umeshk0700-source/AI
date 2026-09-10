import numpy as np
from kbsearch.index import IVFIndex, FlatIndex, BM25

rng = np.random.default_rng(0)


def _clustered(n_clusters=20, per=40, dim=32, noise=0.12):
    centers = rng.standard_normal((n_clusters, dim))
    centers /= np.linalg.norm(centers, axis=1, keepdims=True)
    labels = np.repeat(np.arange(n_clusters), per)
    X = centers[labels] + noise * rng.standard_normal((n_clusters * per, dim))
    X /= np.linalg.norm(X, axis=1, keepdims=True)
    return X, centers


def test_ivf_recall_matches_flat():
    X, centers = _clustered()
    flat = FlatIndex(X)
    ivf = IVFIndex(X).build(nlist=24)
    hit = 0
    for _ in range(60):
        q = centers[rng.integers(len(centers))] + 0.15 * rng.standard_normal(centers.shape[1])
        q /= np.linalg.norm(q)
        gt = set(flat.search(q, 10))
        got = set(ivf.search(q, k=10, nprobe=4))
        hit += len(gt & got) / 10
    assert hit / 60 >= 0.9, f"IVF recall@10 = {hit/60:.2f} (want >= 0.90)"


def test_ivf_handles_empty_probe():
    X, _ = _clustered(n_clusters=4, per=5)
    ivf = IVFIndex(X).build(nlist=4)
    assert isinstance(ivf.search(X[0], k=3, nprobe=1), list)


def test_bm25_exact_term():
    corpus = [
        "The dashboard renders slowly on large datasets sometimes",
        "Error E4021 is returned when the auth token has expired",
        "Refunds are processed within five business days",
    ]
    bm = BM25().index(corpus)
    assert bm.search("E4021", k=1)[0] == 1
    assert bm.search("refunds processed business days", k=1)[0] == 2
