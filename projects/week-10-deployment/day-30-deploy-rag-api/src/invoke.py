"""Invoke handler.handler locally with API-Gateway-HTTP-API-shaped events."""
import json
from handler import handler


def api_event(method="POST", path="/ask", body=None, headers=None):
    return {
        "version": "2.0",
        "routeKey": f"{method} {path}",
        "rawPath": path,
        "headers": headers or {"content-type": "application/json"},
        "requestContext": {"http": {"method": method, "path": path}},
        "body": json.dumps(body) if body is not None else None,
        "isBase64Encoded": False,
    }


class Ctx:
    aws_request_id = "req-local-0001"

    def get_remaining_time_in_millis(self):
        return 25000


if __name__ == "__main__":
    for name, ev in [
        ("valid", api_event(body={"question": "how long do refunds take"})),
        ("missing question", api_event(body={"foo": "bar"})),
        ("bad json", {**api_event(), "body": "{not json"}),
        ("out of scope", api_event(body={"question": "what is your stock price"})),
        ("CORS preflight", api_event(method="OPTIONS")),
    ]:
        r = handler(ev, Ctx())
        print(f"{name:18s} -> {r['statusCode']}  {r['body']}")
