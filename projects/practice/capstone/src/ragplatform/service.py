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
        # TODO: refill tokens by (now - self.ts) * rate up to capacity; if >= 1 consume one
        # and return True, else False.
        raise NotImplementedError


def create_app(platform, *, api_key: str, rate: float = 5.0, burst: int = 10) -> FastAPI:
    app = FastAPI()
    bucket = TokenBucket(rate, burst)

    @app.get("/healthz")
    def healthz():
        return {"ok": True}

    @app.post("/ask")
    def ask(payload: dict, x_api_key: str = Header(default="")):
        # TODO: 401 if x_api_key != api_key; 429 if not bucket.allow();
        #   return {"answer": platform.ask(payload["question"], agentic=payload.get("agentic", False))}
        raise NotImplementedError

    return app
