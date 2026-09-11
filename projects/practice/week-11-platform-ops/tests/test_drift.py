import numpy as np
from platformops import psi, categorical_psi, ks_drift, DriftMonitor

def test_psi_near_zero_for_same_distribution():
    rng = np.random.default_rng(0)
    a, b = rng.normal(0, 1, 4000), rng.normal(0, 1, 2000)
    assert psi(a, b) < 0.1

def test_psi_flags_a_real_shift():
    rng = np.random.default_rng(0)
    a, b = rng.normal(0, 1, 4000), rng.normal(0.8, 1.2, 2000)
    assert psi(a, b) > 0.25

def test_ks_detects_shift():
    rng = np.random.default_rng(1)
    a, b = rng.normal(0, 1, 3000), rng.normal(0.5, 1, 1500)
    assert ks_drift(a, b)["drift"] is True

def test_categorical_psi():
    ref = ["a"] * 70 + ["b"] * 30
    cur = ["a"] * 35 + ["b"] * 65
    assert categorical_psi(ref, cur) > 0.25

def test_monitor_assess():
    rng = np.random.default_rng(2)
    mon = DriftMonitor(rng.normal(0, 1, 3000))
    assert mon.assess(rng.normal(0, 1, 1500))["drift"] is False
    assert mon.assess(rng.normal(1.0, 1.3, 1500))["drift"] is True
