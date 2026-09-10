"""A tiny span tracer (the Day 27 model) for instrumenting lab pipelines.

    with span("retrieve", query=q) as s:
        s.outputs = {"n_hits": len(hits)}

Or as a decorator:  @traced("llm")
"""
from __future__ import annotations

import contextvars
import functools
import json
import time
import uuid
from contextlib import contextmanager
from dataclasses import dataclass, field

_current: contextvars.ContextVar["Span | None"] = contextvars.ContextVar("span", default=None)


@dataclass
class Span:
    name: str
    kind: str = "op"
    id: str = field(default_factory=lambda: uuid.uuid4().hex[:8])
    parent: "Span | None" = None
    children: list["Span"] = field(default_factory=list)
    inputs: dict = field(default_factory=dict)
    outputs: dict = field(default_factory=dict)
    metadata: dict = field(default_factory=dict)
    status: str = "ok"
    error: str | None = None
    start: float | None = None
    end: float | None = None

    @property
    def duration_ms(self) -> float | None:
        return None if self.end is None else (self.end - self.start) * 1000

    def to_dict(self) -> dict:
        return {
            "trace_id": _root(self).id, "span_id": self.id,
            "parent": self.parent.id if self.parent else None,
            "name": self.name, "kind": self.kind, "status": self.status,
            "duration_ms": round(self.duration_ms, 2) if self.duration_ms else None,
            "inputs": self.inputs, "outputs": self.outputs, "metadata": self.metadata,
        }


def _root(s: Span) -> Span:
    while s.parent:
        s = s.parent
    return s


@contextmanager
def span(name: str, kind: str = "op", **inputs):
    s = Span(name=name, kind=kind, parent=_current.get(), inputs=inputs)
    if s.parent:
        s.parent.children.append(s)
    s.start = time.perf_counter()
    tok = _current.set(s)
    try:
        yield s
    except Exception as e:  # noqa: BLE001
        s.status, s.error = "error", repr(e)
        raise
    finally:
        s.end = time.perf_counter()
        _current.reset(tok)


def traced(kind: str = "op"):
    def deco(fn):
        @functools.wraps(fn)
        def wrapper(*a, **kw):
            with span(fn.__name__, kind=kind) as s:
                r = fn(*a, **kw)
                s.outputs = {"return_type": type(r).__name__}
                return r
        return wrapper
    return deco


def flatten(root: Span) -> list[dict]:
    out: list[dict] = []
    def walk(s: Span):
        out.append(s.to_dict())
        for c in s.children:
            walk(c)
    walk(root)
    return out


def render(root: Span, indent: int = 0) -> None:
    d = f"{root.duration_ms:7.1f}ms" if root.duration_ms is not None else "    --   "
    mark = "  " if root.status == "ok" else "!!"
    io = json.dumps({"in": root.inputs, "out": root.outputs}, default=str)
    print(f"{'  ' * indent}{mark} {root.name:<22} {d}  {io[:90]}")
    for c in root.children:
        render(c, indent + 1)
