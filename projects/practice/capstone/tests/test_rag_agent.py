from ragplatform import chunk_doc, VectorIndex, RAGPipeline, Agent
from kb import DOCS
from helpers import kb_fake

def _rag():
    idx = VectorIndex()
    for k, v in DOCS.items():
        idx.add(chunk_doc(k, v))
    return RAGPipeline(idx, kb_fake())

def test_rag_answers_with_citation():
    a = _rag().answer("how long for a refund?")
    assert "30 days" in a.text and a.citations and a.grounded

def test_rag_refuses_when_out_of_scope():
    a = _rag().answer("what is the capital of France?")
    assert a.text.strip().lower().startswith("i don't know") and a.grounded

def test_agent_falls_back_to_direct_answer():
    # FakeLLM here never emits tool calls -> agent returns the model's text
    out = Agent(_rag(), kb_fake()).run("what is the minimum password length?")
    assert "12 characters" in out
