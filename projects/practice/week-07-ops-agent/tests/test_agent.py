from llmlab import FakeLLM
from opsagent.tools import default_registry, INCIDENTS
from opsagent.agent import Agent


def test_completes_a_two_tool_task():
    # scripted planner: search, then answer
    script = [
        ("tool", "search_runbook", {"query": "payments outage"}),
        None,  # -> final answer
    ]
    calls = iter(script)

    def responder(messages, **kw):
        nxt = next(calls, None)
        return nxt if nxt else "Roll back the recent payments release, then verify /healthz."

    run = Agent(FakeLLM(responder=responder), default_registry()).run("payments API is 5xxing")
    assert run.aborted is None
    assert [c["name"] for c in run.tool_calls] == ["search_runbook"]
    assert "roll back" in run.answer.lower()


def test_loop_guard_aborts_a_stuck_planner():
    llm = FakeLLM(responder=lambda m, **k: ("tool", "search_runbook", {"query": "same thing"}))
    run = Agent(llm, default_registry(), max_repeats=2, max_steps=10).run("go")
    assert run.aborted == "loop"


def test_tool_budget_guard():
    seq = iter(range(100))
    llm = FakeLLM(responder=lambda m, **k: ("tool", "search_runbook", {"query": f"q{next(seq)}"}))
    run = Agent(llm, default_registry(), tool_budget=3, max_repeats=99, max_steps=99).run("go")
    assert run.aborted == "tool_budget"
    assert len([c for c in run.tool_calls]) <= 3


def test_destructive_tool_needs_approval():
    n0 = len(INCIDENTS)
    llm = FakeLLM(responder=lambda m, **k: ("tool", "create_incident",
                                            {"title": "x", "severity": "SEV2"}))
    run = Agent(llm, default_registry(), approver=lambda n, a: False, max_steps=1).run("file it")
    assert len(INCIDENTS) == n0                       # nothing was created
    assert run.tool_calls[0]["result"].get("_denied") is True


def test_unknown_tool_is_handled():
    a = Agent(FakeLLM(), default_registry())
    assert a._execute("does_not_exist", {}) == {"error": "unknown tool does_not_exist"}
