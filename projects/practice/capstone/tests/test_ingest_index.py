from ragplatform import chunk_doc, VectorIndex
from kb import DOCS

def test_chunks_overlap_and_are_ordered():
    cs = chunk_doc("refunds", DOCS["refunds"], size=120, overlap=30)
    assert len(cs) >= 2
    assert [c.ord for c in cs] == list(range(len(cs)))
    assert cs[0].cite == "refunds#0"

def test_index_retrieves_the_right_doc():
    idx = VectorIndex()
    for k, v in DOCS.items():
        idx.add(chunk_doc(k, v))
    hits = idx.search("how many days for a refund", k=3)
    assert hits[0][0].doc_id == "refunds"
