from platformops import SignalAggregator
from trace_helpers import make_stream

def test_window_is_bounded():
    agg = SignalAggregator(window=100)
    for e in make_stream(500):
        agg.observe(e)
    assert agg.signals().n == 100

def test_quality_signal_drops_when_corpus_misses_topic():
    healthy = SignalAggregator(1000)
    for e in make_stream(1000, topic_mix=(0.7, 0.3)):
        healthy.observe(e)
    degraded = SignalAggregator(1000)
    for e in make_stream(1000, topic_mix=(0.3, 0.7)):
        degraded.observe(e)
    assert degraded.signals().grounded_rate < healthy.signals().grounded_rate - 0.1
    # infra signal barely moves
    assert abs(degraded.signals().error_rate - healthy.signals().error_rate) < 0.02
