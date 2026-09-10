import numpy as np
from llmlab import FakeLLM
from rag.pipeline import RAGPipeline
from rag.schemas import REFUSAL


class ToyEmbedder:
    provider = "toy"

    def __init__(self):
        self.vocab = None

    def embed(self, texts):
        toks = [set(t.lower().replace("?", "").split()) for t in texts]
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


DOCS = {
    "Time Off": "Full-time staff accrue 1.75 vacation days per month up to a maximum of 30 days.",
    "Expenses": "Expenses of 75 dollars or more require an itemised receipt within 14 days.",
    "Security": "Laptops lock after five minutes of inactivity and use full disk encryption.",
}


def _pipe(llm):
    return RAGPipeline(ToyEmbedder(), llm, k=2, min_score=0.05).ingest(DOCS)


def test_gate_refuses_without_calling_llm():
    llm = FakeLLM(text="should never be used")
    p = RAGPipeline(ToyEmbedder(), llm, k=2, min_score=0.99).ingest(DOCS)
    a = p.answer("how many vacation days do I accrue")
    assert a.gated is True and a.text == REFUSAL and a.sources == []
    assert llm.calls == []          # the model was never called


def test_prompt_has_context_and_rules():
    p = _pipe(FakeLLM(text="ok"))
    chunks = p._retrieve("vacation days per month")
    msgs = p._build_prompt("vacation days per month", chunks)
    assert "1.75 vacation days" in msgs[0]["content"]
    assert "[1]" in msgs[0]["content"] and "Question:" in msgs[0]["content"]


def test_answer_attributes_sources():
    llm = FakeLLM(text="Full-time staff accrue 1.75 vacation days per month.")
    p = _pipe(llm)
    a = p.answer("how many vacation days per month")
    assert a.gated is False
    assert a.sources == ["Time Off"]
    assert "1.75" in a.text


def test_faithfulness_flags_unsupported_claim():
    from rag.evaluate import faithfulness
    ctx = ["Full-time staff accrue 1.75 vacation days per month up to 30 days."]
    good = "Staff accrue 1.75 vacation days per month."
    bad = "Staff get unlimited vacation and a free car."
    assert faithfulness(good, ctx) == 1.0
    assert faithfulness(bad, ctx) < 0.5
    assert faithfulness(REFUSAL, ctx) == 1.0
