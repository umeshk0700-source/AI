from platformops import EvalReport, ReleaseGate

BASE = EvalReport("bundle-1", {f"q{i}": 0.8 for i in range(10)})

def test_no_change_passes():
    v = ReleaseGate(BASE).check(EvalReport("b2", {f"q{i}": 0.8 for i in range(10)}))
    assert v.ok and abs(v.delta) < 1e-9

def test_aggregate_drop_blocks():
    cand = EvalReport("b2", {f"q{i}": 0.7 for i in range(10)})
    assert ReleaseGate(BASE, tolerance=0.03).check(cand).ok is False

def test_single_case_regression_blocks():
    scores = {f"q{i}": 0.8 for i in range(10)}
    scores["q3"] = 0.4                       # pass -> fail
    v = ReleaseGate(BASE, tolerance=0.5).check(EvalReport("b2", scores))
    assert v.ok is False and v.unexpected_regressions == ["q3"]

def test_allow_list_permits_known_regression():
    scores = {f"q{i}": 0.8 for i in range(10)}
    scores["q3"] = 0.4
    v = ReleaseGate(BASE, tolerance=0.5, allow_regress=("q3",)).check(EvalReport("b2", scores))
    assert v.ok is True
