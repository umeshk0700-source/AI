from llmlab import FakeLLM
from bench.schemas import Extraction
from bench.bench import ModelBench

GOLD = [
    {"text": "ACME Corp invoice 88-A total 1240.00 USD due 2024-05-01, 3 items",
     "fields": {"vendor": "ACME Corp", "invoice_number": "88-A", "total": 1240.0,
                "currency": "USD", "due_date": "2024-05-01", "line_item_count": 3}},
    {"text": "Globex #Z9 EUR 55.5 no due date, 1 item",
     "fields": {"vendor": "Globex", "invoice_number": "Z9", "total": 55.5,
                "currency": "EUR", "due_date": "", "line_item_count": 1}},
]


def _fake(answer: dict):
    return FakeLLM(responder=lambda m, **k: answer)


def test_score_one():
    b = ModelBench(GOLD)
    perfect = Extraction(**GOLD[0]["fields"])
    fa, ok = b._score_one(perfect, GOLD[0]["fields"])
    assert fa == 1.0 and ok is True
    wrong = perfect.model_copy(update={"total": 9.99, "vendor": "WRONG"})
    fa2, ok2 = b._score_one(wrong, GOLD[0]["fields"])
    assert fa2 == 4 / 6 and ok2 is False


def test_run_and_select_prefers_cheaper_when_tied():
    b = ModelBench(GOLD)
    good = _fake({"vendor": "ACME Corp", "invoice_number": "88-A", "total": 1240.0,
                  "currency": "USD", "due_date": "2024-05-01", "line_item_count": 3})
    res = b.run({"cheap": good, "pricey": good})
    for r in res:
        assert 0.0 <= r.field_accuracy <= 1.0
    memo = b.select(res, min_accuracy=0.5)
    assert memo.recommended in {"cheap", "pricey"}
    assert len(memo.table) == 2 and memo.min_accuracy == 0.5


def test_select_flags_when_nobody_clears_bar():
    b = ModelBench(GOLD)
    bad = _fake({"vendor": "x", "invoice_number": "x", "total": 0.0, "currency": "x",
                 "due_date": "x", "line_item_count": 0})
    memo = b.select(b.run({"m": bad}), min_accuracy=0.9)
    assert "no model cleared" in " ".join(memo.rationale).lower()
