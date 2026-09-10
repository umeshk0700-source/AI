
"""Tiny load test — run against a deployed URL:  python loadtest.py http://localhost:8000
Prints throughput and p50/p95/p99 latency."""
from __future__ import annotations

import statistics
import sys
import time

import httpx

KEY = "demo-key-123"
QUESTIONS = ["how many vacation days do I accrue", "what is the meal per diem",
             "how often are passwords rotated", "can I work from home"]


def main(n: int = 200, concurrency: int = 10):
    URL = sys.argv[1] if len(sys.argv) > 1 else "http://localhost:8000"
    lat: list[float] = []
    errors = 0
    start = time.perf_counter()
    with httpx.Client(base_url=URL, headers={"x-api-key": KEY}, timeout=30) as c:
        for i in range(n):
            q = QUESTIONS[i % len(QUESTIONS)]
            t0 = time.perf_counter()
            try:
                r = c.post("/ask", json={"question": q})
                r.raise_for_status()
            except Exception:  # noqa: BLE001
                errors += 1
                continue
            lat.append((time.perf_counter() - t0) * 1000)
    wall = time.perf_counter() - start
    q = statistics.quantiles(lat, n=100) if len(lat) > 1 else [0] * 99
    print(f"{n} requests in {wall:.1f}s  ->  {n / wall:.1f} req/s   errors={errors}")
    print(f"latency ms  p50={q[49]:.0f}  p95={q[94]:.0f}  p99={q[98]:.0f}")


if __name__ == "__main__":
    main()
