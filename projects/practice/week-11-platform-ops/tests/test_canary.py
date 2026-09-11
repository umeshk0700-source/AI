from platformops import CanaryController
from trace_helpers import measure_factory

GOOD = {"v1": dict(lat=0.9, err=0.01, q=0.82), "v2": dict(lat=1.2, err=0.015, q=0.83)}
BAD  = {"v1": dict(lat=0.9, err=0.01, q=0.82), "v2": dict(lat=2.7, err=0.18, q=0.70)}

def test_healthy_candidate_is_promoted():
    c = CanaryController(measure_factory(GOOD), stable="v1", candidate="v2")
    r = c.roll_out(n_per_step=400)
    assert r.outcome == "promoted" and r.final_pct == 100 and len(r.steps) == 4

def test_bad_candidate_rolls_back_at_first_step():
    c = CanaryController(measure_factory(BAD), stable="v1", candidate="v2")
    r = c.roll_out(n_per_step=400)
    assert r.outcome == "rolled_back" and r.final_pct == 0 and len(r.steps) == 1
    assert r.steps[0]["healthy"] is False
