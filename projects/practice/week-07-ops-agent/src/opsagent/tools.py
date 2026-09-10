
"""Given — the tool surface. `search_runbook` and `get_incident_status` are read-only;
`create_incident` mutates state and is marked destructive (needs approval)."""
from __future__ import annotations

from dataclasses import dataclass, field
from typing import Callable

from llmlab import ToolSpec

# --- a tiny fake ops world -------------------------------------------------
RUNBOOKS = {
    "payments-outage": ("Payments API 5xx runbook: 1) check the deploy dashboard for a recent "
                        "release. 2) if a release in the last 30 min, roll back with "
                        "`deploy rollback payments`. 3) verify /healthz returns 200. "
                        "4) post an update in #payments-oncall."),
    "db-failover": ("Primary DB failover runbook: 1) confirm the primary is unreachable. "
                    "2) promote the standby with `pg_ctl promote`. 3) update the connection "
                    "string secret. 4) restart the API pods."),
    "cert-expiry": ("TLS cert expiry runbook: 1) run `certbot renew`. 2) reload the load "
                    "balancer. 3) check the expiry date with `openssl x509 -enddate`."),
}
INCIDENTS: dict[str, dict] = {
    "INC-4102": {"status": "mitigated", "title": "Payments API elevated 5xx", "severity": "SEV2"},
}
_next_id = [4103]


def _search_runbook(query: str) -> dict:
    q = query.lower()
    hits = [{"key": k, "text": v} for k, v in RUNBOOKS.items()
            if any(w in k or w in v.lower() for w in q.split())]
    return {"matches": hits[:2]} if hits else {"matches": [], "note": "no runbook found"}


def _get_incident_status(incident_id: str) -> dict:
    return INCIDENTS.get(incident_id, {"error": f"unknown incident {incident_id}"})


def _create_incident(title: str, severity: str) -> dict:
    iid = f"INC-{_next_id[0]}"
    _next_id[0] += 1
    INCIDENTS[iid] = {"status": "open", "title": title, "severity": severity}
    return {"created": iid, "status": "open"}


@dataclass
class Tool:
    spec: ToolSpec
    fn: Callable[..., dict]
    destructive: bool = False


class ToolRegistry:
    def __init__(self, tools: list[Tool]):
        self._by_name = {t.spec.name: t for t in tools}

    def specs(self) -> list[ToolSpec]:
        return [t.spec for t in self._by_name.values()]

    def get(self, name: str) -> Tool | None:
        return self._by_name.get(name)


def default_registry() -> ToolRegistry:
    return ToolRegistry([
        Tool(ToolSpec("search_runbook", "Search the ops runbook library by keywords.",
                      {"type": "object", "properties": {"query": {"type": "string"}},
                       "required": ["query"]}), _search_runbook),
        Tool(ToolSpec("get_incident_status", "Look up the status of an incident by id (INC-####).",
                      {"type": "object", "properties": {"incident_id": {"type": "string"}},
                       "required": ["incident_id"]}), _get_incident_status),
        Tool(ToolSpec("create_incident", "File a NEW incident. Destructive — needs approval.",
                      {"type": "object",
                       "properties": {"title": {"type": "string"},
                                      "severity": {"type": "string", "enum": ["SEV1", "SEV2", "SEV3"]}},
                       "required": ["title", "severity"]}), _create_incident, destructive=True),
    ])
