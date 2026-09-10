import numpy as np
from kbsearch.retriever import HybridRetriever
from kbsearch.evaluate import recall_at_k, mrr


class ToyEmbedder:
    """deterministic bag-of-words embedder so retriever tests don't need a model/key."""
    provider = "toy"
    dim = 0

    def __init__(self, vocab=None):
        self.vocab = vocab

    def embed(self, texts):
        toks = [set(t.lower().split()) for t in texts]
        if self.vocab is None:
            self.vocab = sorted({w for s in toks for w in s})
        vi = {w: i for i, w in enumerate(self.vocab)}
        V = np.zeros((len(texts), len(self.vocab)))
        for r, s in enumerate(toks):
            for w in s:
                if w in vi:
                    V[r, vi[w]] = 1
        n = np.linalg.norm(V, axis=1, keepdims=True)
        return V / np.where(n == 0, 1, n)


DOCS = [
    "how to reset your password from the sign in page",
    "the export button produces a CSV of the current report",
    "billing invoices can be downloaded as PDF from the account page",
    "error code X17 means the API rate limit was exceeded",
    "our support hours are monday to friday nine to five",
]


def test_recall_and_mrr_helpers():
    assert recall_at_k([3, 1, 4], {1, 4}, k=3) == 1.0
    assert recall_at_k([3, 1, 4], {1, 4}, k=1) == 0.0
    assert mrr([3, 1, 4], {1}) == 0.5
    assert mrr([3, 1, 4], {9}) == 0.0


def test_hybrid_uses_lexical_for_exact_code():
    emb = ToyEmbedder()
    r = HybridRetriever(emb, DOCS)
    # "X17" is an exact token BM25 nails; dense (bag of words) has it too but weaker
    assert r.search("what does error X17 mean", k=1)[0] == 3


def test_hybrid_returns_k_results_and_blends():
    r = HybridRetriever(ToyEmbedder(), DOCS)
    top = r.search("download the report as a file", k=3)
    assert len(top) == 3 and len(set(top)) == 3
    assert top[0] == 1       # "export button produces a CSV of the current report"
