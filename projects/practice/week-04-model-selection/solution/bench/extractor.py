
"""Extract structured fields from one invoice with a given model."""
from __future__ import annotations

import time

from llmlab import LLMClient, span

from .schemas import Extraction

SYSTEM = (
    "You extract fields from vendor invoices. Return ONLY the schema. "
    "total is a number without a currency symbol. currency is a 3-letter ISO code. "
    "due_date is yyyy-mm-dd, or an empty string if the invoice has no due date. "
    "line_item_count is the number of billable line items."
)
_SCHEMA = Extraction.model_json_schema()


class Extractor:
    def __init__(self, llm: LLMClient, *, max_tokens: int = 300):
        self.llm = llm
        self.max_tokens = max_tokens

    def extract(self, invoice_text: str) -> tuple[Extraction, float]:
        # TODO: call self.llm.chat([user=invoice_text], system=SYSTEM,
        #       json_schema=_SCHEMA, max_tokens=self.max_tokens) inside span("extract").
        #       Return (Extraction parsed from resp.json, latency_seconds).
        with span("extract", kind="llm"):
            t0 = time.perf_counter()
            resp = self.llm.chat([{"role": "user", "content": invoice_text}], system=SYSTEM,
                                 json_schema=_SCHEMA, max_tokens=self.max_tokens)
            dt = time.perf_counter() - t0
        return Extraction.model_validate(resp.json), dt
