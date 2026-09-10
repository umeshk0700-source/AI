
"""The FastAPI app. `create_app(rag, api_keys, limiter)` -> ASGI app."""
from __future__ import annotations

import json
import time
import uuid

from fastapi import Depends, FastAPI, Header, HTTPException, Request
from fastapi.responses import JSONResponse

from .models import AskRequest, AskResponse
from .ratelimit import TokenBucket

DEFAULT_KEYS = {"demo-key-123": "acme", "demo-key-456": "globex"}


def _log(**fields):
    print(json.dumps({"ts": round(time.time(), 3), **fields}))


def _to_http_error(exc: Exception) -> tuple[int, str]:
    # TODO: map an exception raised by the RAG pipeline to (status_code, message).
    #   - TimeoutError / a name containing "Timeout" / "APIConnection"  -> (504, "upstream timeout")
    #   - a name containing "RateLimit"                                 -> (503, "upstream rate limited")
    #   - ValueError                                                    -> (400, str(exc))
    #   - anything else                                                 -> (503, "upstream error")
    #   NEVER return 500 with a stack trace.
    name = type(exc).__name__
    if isinstance(exc, TimeoutError) or "Timeout" in name or "APIConnection" in name:
        return 504, "upstream timeout"
    if "RateLimit" in name:
        return 503, "upstream rate limited"
    if isinstance(exc, ValueError):
        return 400, str(exc)
    return 503, "upstream error"


def create_app(rag, *, api_keys: dict[str, str] | None = None,
               limiter: TokenBucket | None = None) -> FastAPI:
    keys = api_keys if api_keys is not None else DEFAULT_KEYS
    limiter = limiter or TokenBucket(rate_per_sec=5, burst=10)
    app = FastAPI(title="Policy Assistant API")

    def require_api_key(x_api_key: str | None = Header(default=None)) -> str:
        # TODO: if x_api_key is missing or not in `keys` -> raise HTTPException(401, "invalid api key").
        #   otherwise return the tenant name keys[x_api_key].
        if not x_api_key or x_api_key not in keys:
            raise HTTPException(status_code=401, detail="invalid api key")
        return keys[x_api_key]

    @app.get("/healthz")
    def healthz():
        return {"status": "ok", "checks": {"rag": rag is not None}}

    @app.post("/ask", response_model=AskResponse)
    def ask(req: AskRequest, request: Request, tenant: str = Depends(require_api_key)):
        # TODO:
        #   trace_id = uuid4().hex[:16]
        #   rate limit: if not limiter.allow(tenant) -> raise HTTPException(429, ...,
        #       headers={"Retry-After": "1"})
        #   413: if len(req.question) > 2000 -> HTTPException(413, "question too long")
        #       (the pydantic model already caps it, but keep a guard)
        #   t0 = time.perf_counter()
        #   try: ans = rag.answer(req.question)
        #   except Exception as e: status, msg = _to_http_error(e);
        #       _log(evt="ask_error", trace_id=..., tenant=..., error=repr(e))
        #       raise HTTPException(status, msg)
        #   latency_ms = round((perf_counter()-t0)*1000, 1)
        #   _log(evt="ask", trace_id, tenant, q_len=len(req.question), gated=ans.gated,
        #        n_sources=len(ans.sources), latency_ms=latency_ms)
        #   return AskResponse(answer=ans.text, sources=ans.sources, gated=ans.gated,
        #                      confidence=ans.confidence, trace_id=trace_id, latency_ms=latency_ms)
        trace_id = uuid.uuid4().hex[:16]
        if not limiter.allow(tenant):
            raise HTTPException(status_code=429, detail="rate limit exceeded",
                                headers={"Retry-After": "1"})
        if len(req.question) > 2000:
            raise HTTPException(status_code=413, detail="question too long")
        t0 = time.perf_counter()
        try:
            ans = rag.answer(req.question)
        except Exception as e:  # noqa: BLE001
            status, msg = _to_http_error(e)
            _log(evt="ask_error", trace_id=trace_id, tenant=tenant, error=repr(e), status=status)
            raise HTTPException(status_code=status, detail=msg)
        latency_ms = round((time.perf_counter() - t0) * 1000, 1)
        _log(evt="ask", trace_id=trace_id, tenant=tenant, q_len=len(req.question),
             gated=ans.gated, n_sources=len(ans.sources), latency_ms=latency_ms)
        return AskResponse(answer=ans.text, sources=list(ans.sources), gated=ans.gated,
                           confidence=float(ans.confidence), trace_id=trace_id,
                           latency_ms=latency_ms)

    @app.exception_handler(HTTPException)
    async def _http_exc(request: Request, exc: HTTPException):
        return JSONResponse(status_code=exc.status_code,
                            content={"error": exc.detail, "trace_id": uuid.uuid4().hex[:16]},
                            headers=getattr(exc, "headers", None))

    return app
