"""Synthetic trace stream + measurement fns for the offline tests and the notebook."""
import numpy as np

def make_stream(n, *, seed=0, topic_mix=(0.7, 0.3), corpus_version="v7"):
    rng = np.random.default_rng(seed)
    out = []
    for _ in range(n):
        topic = rng.choice(["billing", "new_product"], p=topic_mix)
        covered = not (topic == "new_product" and corpus_version == "v7")
        hit = covered and rng.random() < 0.92
        grounded = hit and rng.random() < 0.95
        out.append(dict(topic=topic, latency_ms=float(rng.normal(1100, 250)),
                        error=bool(rng.random() < 0.01), retrieval_hit=hit, grounded=grounded,
                        tokens_in=int(rng.normal(1200, 200)), tokens_out=int(rng.normal(180, 40)),
                        thumbs_down=bool((not grounded) and rng.random() < 0.4)))
    return out

def measure_factory(profiles, seed=7):
    rng = np.random.default_rng(seed)
    def measure(version, n):
        p = profiles[version]
        rs = [(rng.random() < p["err"], max(0.05, rng.normal(p["lat"], 0.25))) for _ in range(n)]
        lat = sorted(x[1] for x in rs)
        errored = np.mean([x[0] for x in rs])
        q = 0.0 if False else max(0, min(1, rng.normal(p["q"], 0.03)))
        return {"p95_latency_s": round(lat[int(0.95 * n)], 2),
                "error_rate": round(float(errored), 3), "quality": round(float(q), 3)}
    return measure
