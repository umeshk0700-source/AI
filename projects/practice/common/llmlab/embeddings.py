"""Provider-neutral text embeddings.

    from llmlab import get_embedder
    emb = get_embedder("openai")        # or "voyage", or "local"
    vecs = emb.embed(["hello", "world"])   # -> np.ndarray (2, dim), L2-normalised
"""
from __future__ import annotations

import numpy as np

from .config import settings
from .cost import CostTracker, price
from .trace import span


def _l2(x: np.ndarray) -> np.ndarray:
    n = np.linalg.norm(x, axis=1, keepdims=True)
    return x / np.where(n == 0, 1, n)


class Embedder:
    provider = "base"
    dim: int = 0

    def __init__(self, cost: CostTracker | None = None):
        from .client import default_cost
        self.cost = cost or default_cost()

    def embed(self, texts: list[str]) -> np.ndarray:
        with span("embed", kind="embedder", provider=self.provider, n=len(texts)) as s:
            v = _l2(np.asarray(self._embed(list(texts)), dtype=np.float32))
            s.outputs = {"shape": list(v.shape)}
            return v

    def _embed(self, texts: list[str]) -> np.ndarray:
        raise NotImplementedError


class OpenAIEmbedder(Embedder):
    provider = "openai"

    def __init__(self, model: str | None = None, cost: CostTracker | None = None):
        super().__init__(cost)
        from openai import OpenAI
        if not settings.openai_api_key:
            raise RuntimeError("OPENAI_API_KEY not set")
        self.model = model or settings.embed_model_openai
        self._c = OpenAI(timeout=settings.request_timeout_s)
        self.dim = 1536 if "small" in self.model else 3072

    def _embed(self, texts):
        r = self._c.embeddings.create(model=self.model, input=texts)
        self.cost.record(self.model, r.usage.total_tokens, 0)
        return [d.embedding for d in r.data]


class VoyageEmbedder(Embedder):
    provider = "voyage"

    def __init__(self, model: str = "voyage-3", cost: CostTracker | None = None):
        super().__init__(cost)
        import voyageai
        if not settings.voyage_api_key:
            raise RuntimeError("VOYAGE_API_KEY not set")
        self.model = model
        self._c = voyageai.Client()
        self.dim = 1024

    def _embed(self, texts):
        r = self._c.embed(texts, model=self.model, input_type="document")
        self.cost.record(self.model, r.total_tokens, 0)
        return r.embeddings


class LocalEmbedder(Embedder):
    """Offline fallback — sentence-transformers all-MiniLM-L6-v2 (384-dim). Free, no key."""

    provider = "local"
    dim = 384

    def __init__(self, cost: CostTracker | None = None):
        super().__init__(cost)
        from sentence_transformers import SentenceTransformer
        self._m = SentenceTransformer("all-MiniLM-L6-v2")

    def _embed(self, texts):
        return self._m.encode(texts, normalize_embeddings=False)


def get_embedder(provider: str = "local", **kw) -> Embedder:
    return {
        "openai": OpenAIEmbedder, "voyage": VoyageEmbedder, "local": LocalEmbedder,
    }[provider.lower()](**kw)
