import time
import pytest
from gateway.breaker import CircuitBreaker, CircuitOpen


def _fail():
    raise RuntimeError("boom")


def test_opens_after_threshold():
    cb = CircuitBreaker(failure_threshold=3, reset_timeout=100)
    for _ in range(3):
        with pytest.raises(RuntimeError):
            cb.call(_fail)
    assert cb.state == "open"
    with pytest.raises(CircuitOpen):
        cb.call(lambda: "would succeed")     # not even attempted


def test_half_open_then_close_on_success():
    cb = CircuitBreaker(failure_threshold=1, reset_timeout=0.05)
    with pytest.raises(RuntimeError):
        cb.call(_fail)
    assert cb.state == "open"
    time.sleep(0.06)
    assert cb.call(lambda: "ok") == "ok"     # probe succeeds
    assert cb.state == "closed" and cb.failures == 0


def test_half_open_failure_reopens():
    cb = CircuitBreaker(failure_threshold=1, reset_timeout=0.05)
    with pytest.raises(RuntimeError):
        cb.call(_fail)
    time.sleep(0.06)
    with pytest.raises(RuntimeError):
        cb.call(_fail)                        # probe fails
    assert cb.state == "open"
