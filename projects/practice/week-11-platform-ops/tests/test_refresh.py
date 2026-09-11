from platformops import RefreshTrigger, Signals

def _sig(grounded=0.85, td=0.05):
    return Signals(n=500, p95_ms=1600, error_rate=0.01, grounded_rate=grounded,
                   thumbs_down_rate=td, cost_per_req_usd=0.001)

def test_single_reason_does_not_fire():
    d = RefreshTrigger().decide(psi_value=0.4, signals=_sig(), eval_score=0.83, baseline_eval=0.83)
    assert d.refresh is False and len(d.reasons) == 1

def test_two_reasons_fire():
    d = RefreshTrigger().decide(psi_value=0.4, signals=_sig(grounded=0.55),
                                eval_score=0.83, baseline_eval=0.83)
    assert d.refresh is True and len(d.reasons) == 2

def test_all_four_reasons():
    d = RefreshTrigger().decide(psi_value=0.5, signals=_sig(grounded=0.5, td=0.3),
                                eval_score=0.70, baseline_eval=0.85)
    assert d.refresh is True and len(d.reasons) == 4
