import pytest
from triage.schemas import Priority, Ticket, TriageResult
from datetime import datetime, timezone


def test_priority_sla_and_bump():
    assert Priority.p3.sla_hours == 24
    assert Priority.p3.bump() == Priority.p2
    assert Priority.p1.bump() == Priority.p1          # can't go higher


def test_ticket_rejects_empty_body():
    with pytest.raises(Exception):
        Ticket(id="1", subject="x", body="   ")


def test_sla_from():
    created = datetime(2024, 1, 1, 9, 0, tzinfo=timezone.utc)
    due = TriageResult.sla_from(created, Priority.p2)
    assert (due - created).total_seconds() == 4 * 3600
