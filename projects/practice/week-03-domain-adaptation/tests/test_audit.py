from adapt.audit import DatasetAudit

TRAIN = [
    {"id": "a", "prompt": "vacation policy?", "completion": "Answer: 1.75 days/month."},
    {"id": "b", "prompt": "expense limit?", "completion": "Answer: receipts over $75."},
    {"id": "c", "prompt": "remote days?", "completion": "Answer: up to 3/week."},
]


def test_flags_duplicate():
    rows = TRAIN + [dict(TRAIN[0])]
    assert DatasetAudit().duplicates(rows) == [(0, 3)]


def test_flags_leakage():
    test = [{"id": "x", "prompt": "vacation policy?", "completion": "..."},
            {"id": "y", "prompt": "new question", "completion": "..."}]
    assert DatasetAudit().leakage(TRAIN, test) == ["x"]


def test_format_consistency():
    bad = TRAIN + [{"id": "d", "prompt": "q", "completion": "no template here"}]
    assert DatasetAudit().format_consistency(TRAIN) == 1.0
    assert DatasetAudit().format_consistency(bad) == 0.75


def test_run_ok_and_not_ok():
    assert DatasetAudit().run(TRAIN, []).ok
    dirty = TRAIN + [dict(TRAIN[1])]
    assert not DatasetAudit().run(dirty, []).ok
