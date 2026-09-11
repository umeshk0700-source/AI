"""FastAPI wrapper: POST /ask with an API key + a token-bucket rate limit."""
from __future__ import annotations

import time

from fastapi import FastAPI, Header, HTTPException


class TokenBucket:
    def __init__(self, rate: float, burst: int):
        self.rate, self.capacity = rate, burst
        self.tokens = float(burst)
        self.ts = time.monotonic()

    def allow(self) -> bool:
        now = time.monotonic()
        self.tokens = min(self.capacity, self.tokens + (now - self.ts) * self.rate)
        self.ts = now
        if self.tokens >= 1:
            self.tokens -= 1
            return True
        return False


def create_app(platform, *, api_key: str, rate: float = 5.0, burst: int = 10) -> FastAPI:
    app = FastAPI()
    bucket = TokenBucket(rate, burst)

    @app.get("/healthz")
    def healthz():
        return {"ok": True}

    @app.post("/ask")
    def ask(payload: dict, x_api_key: str = Header(default="")):
        if x_api_key != api_key:
            raise HTTPException(status_code=401, detail="bad api key")
        if not bucket.allow():
            raise HTTPException(status_code=429, detail="rate limited")
        return {"answer": platform.ask(payload["question"],
                                       agentic=payload.get("agentic", False))}

    return app
