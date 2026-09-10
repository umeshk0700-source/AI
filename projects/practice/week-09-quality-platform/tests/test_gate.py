from quality.schemas import Report
from quality.gate import RegressionGate


def _report(**metrics):
    return Report(n=10, by_scorer=metrics, by_tag={})


def test_passes_a_no_op_change():
    base = _report(judge=0.85, contains=0.9)
    cand = _report(judge=0.86, contains=0.9)
    v = RegressionGate(base).check(cand)
    assert v.passed and v.blocking == []


def test_fails_on_regression_and_names_the_metric():
    base = _report(judge=0.85, contains=0.9)
    cand = _report(judge=0.70, contains=0.9)          # judge dropped 0.15
    v = RegressionGate(base, tolerance=0.03).check(cand)
    assert not v.passed and "judge" in v.blocking
    assert v.deltas["judge"] < 0


def test_hard_assertion_short_circuits():
    base = _report(judge=0.85, contains=0.9)
    cand = _report(judge=0.90, contains=0.95)          # everything improved
    def no_injection(rep):
        return (False, "answered an injected 'ignore your context' prompt")
    v = RegressionGate(base, hard_assertions=[no_injection]).check(cand)
    assert not v.passed
    assert any(b.startswith("HARD:") for b in v.blocking)
