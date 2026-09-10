
"""Retrieval metrics over a labelled query set."""
from __future__ import annotations


def recall_at_k(retrieved: list[int], relevant: set[int], k: int) -> float:
    # TODO: fraction of `relevant` that appears in the first k of `retrieved`.
    top = set(retrieved[:k])
    return len(top & relevant) / len(relevant) if relevant else 1.0


def mrr(retrieved: list[int], relevant: set[int]) -> float:
    # TODO: reciprocal rank of the FIRST relevant hit (1-indexed); 0 if none.
    for i, doc in enumerate(retrieved, start=1):
        if doc in relevant:
            return 1.0 / i
    return 0.0


def evaluate(retriever, queries: list[dict], k: int = 5) -> dict:
    """queries: [{"q": str, "relevant": [doc_id, ...]}]"""
    rs, ms = [], []
    for item in queries:
        got = retriever.search(item["q"], k=max(k, 10))
        rel = set(item["relevant"])
        rs.append(recall_at_k(got, rel, k))
        ms.append(mrr(got, rel))
    return {"recall_at_%d" % k: sum(rs) / len(rs), "mrr": sum(ms) / len(ms), "n": len(queries)}
