from quality.schemas import EvalCase
from quality.scorers import Contains
from quality.suite import EvalSuite

CASES = [
    EvalCase(id="a", inputs={"q": "vacation days?"}, must_contain=["1.75"], tags=["hr", "easy"]),
    EvalCase(id="b", inputs={"q": "meal per diem?"}, must_contain=["$90"], tags=["hr"]),
    EvalCase(id="c", inputs={"q": "password rotation?"}, must_contain=["90 days"], tags=["security"]),
]


def test_run_aggregates_by_scorer_and_tag():
    # a system that answers 'a' correctly, others not
    def sut(q):
        return {"vacation days?": "1.75 days", "meal per diem?": "some amount",
                "password rotation?": "often"}[q]
    rep = EvalSuite(CASES, [Contains()]).run(sut)
    assert rep.n == 3
    assert rep.by_scorer["contains"] == 1 / 3
    assert rep.by_tag["hr"]["contains"] == 0.5      # a right, b wrong
    assert rep.by_tag["security"]["contains"] == 0.0
    assert len(rep.rows) == 3
