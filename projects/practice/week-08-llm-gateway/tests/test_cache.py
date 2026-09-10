import numpy as np
from gateway.cache import SemanticCache


class ToyEmbedder:
    provider = "toy"

    def __init__(self):
        self.vocab = None

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


def test_empty_cache_is_a_miss():
    c = SemanticCache(ToyEmbedder(), threshold=0.9)
    assert c.get("anything") is None
    assert c.misses == 1 and c.hits == 0


def test_exact_repeat_hits():
    c = SemanticCache(ToyEmbedder(), threshold=0.9)
    c.put("how do I reset my password", "click forgot password")
    assert c.get("how do I reset my password") == "click forgot password"
    assert c.hits == 1


def test_near_duplicate_hits_below_exact():
    c = SemanticCache(ToyEmbedder(), threshold=0.6)
    c.put("how do I reset my password today", "click forgot password")
    # shares 5/6 words -> cosine ~0.9 -> hit at threshold 0.6
    assert c.get("how do I reset my password") == "click forgot password"


def test_unrelated_prompt_misses():
    c = SemanticCache(ToyEmbedder(), threshold=0.7)
    c.put("how do I reset my password", "x")
    assert c.get("what are your support hours") is None


def test_eviction():
    c = SemanticCache(ToyEmbedder(), threshold=0.99, max_entries=2)
    for i in range(3):
        c.put(f"prompt number {i}", str(i))
    assert len(c._keys) == 2 and c._keys[0] == "prompt number 1"
