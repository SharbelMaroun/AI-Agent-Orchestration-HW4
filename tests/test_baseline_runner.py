"""TDD tests for the BaselineRunner (task 12.019)."""

from pathlib import Path
from types import SimpleNamespace

from archlens.gatekeeper.gatekeeper import Gatekeeper
from archlens.metrics.baseline_runner import BaselineRunner
from archlens.metrics.questions import Question

FIXTURE = Path(__file__).resolve().parent / "fixtures" / "mini_repo"


class _StubExecutor:
    def execute(self, model, messages, **kwargs):
        return SimpleNamespace(usage=SimpleNamespace(input_tokens=100, output_tokens=5))


def _questions(n=10):
    return [Question(id=f"Q{i:02d}", text=f"Question {i}?", expected_evidence="hub")
            for i in range(1, n + 1)]


def test_runs_all_questions_tagged_baseline():
    gk = Gatekeeper(executor=_StubExecutor())
    ledger = BaselineRunner(gk, "claude-opus-4-8").run(FIXTURE, _questions(10))
    assert len(ledger.entries) == 10
    assert {e.protocol for e in ledger.entries} == {"baseline"}
    assert {e.question_id for e in ledger.entries} == {f"Q{i:02d}" for i in range(1, 11)}


def test_each_entry_uses_baseline_agent():
    gk = Gatekeeper(executor=_StubExecutor())
    ledger = BaselineRunner(gk, "m").run(FIXTURE, _questions(3))
    assert all(e.agent == "BaselineRunner" for e in ledger.entries)
