"""TDD tests for the AssistedRunner (task 12.024)."""

from types import SimpleNamespace

from archlens.gatekeeper.gatekeeper import Gatekeeper
from archlens.metrics.assisted_runner import AssistedRunner
from archlens.metrics.questions import Question


class _CapturingExecutor:
    def __init__(self):
        self.contexts = []

    def execute(self, model, messages, **kwargs):
        self.contexts.append(messages[0]["content"])
        return SimpleNamespace(usage=SimpleNamespace(input_tokens=50, output_tokens=5))


def _vault(tmp_path):
    root = tmp_path / "vault"
    (root / "wiki").mkdir(parents=True)
    (root / "index.md").write_text("# Index hub", encoding="utf-8")
    (root / "wiki" / "community-1.md").write_text("modules and clusters", encoding="utf-8")
    return root


def _questions(n=10):
    return [Question(id=f"Q{i:02d}", text=f"Question {i} modules?", expected_evidence="hub")
            for i in range(1, n + 1)]


def test_runs_all_questions_tagged_assisted(tmp_path):
    gk = Gatekeeper(executor=_CapturingExecutor())
    ledger = AssistedRunner(gk, "m", _vault(tmp_path)).run(_questions(10))
    assert len(ledger.entries) == 10
    assert {e.protocol for e in ledger.entries} == {"assisted"}
    assert all(e.agent == "AssistedRunner" for e in ledger.entries)


def test_context_has_no_raw_full_source_dump(tmp_path):
    cap = _CapturingExecutor()
    AssistedRunner(Gatekeeper(executor=cap), "m", _vault(tmp_path)).run(_questions(2))
    assert cap.contexts
    for ctx in cap.contexts:
        assert "# FILE:" not in ctx
        assert "Index hub" in ctx
