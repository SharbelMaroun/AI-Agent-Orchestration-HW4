"""TDD tests for the QAAgent orchestration node (tasks 10.023-10.024)."""

from types import SimpleNamespace

from archlens.agents.qa_agent import make_qa_node


class _SDK:
    def run_quality_gates(self, repo_path=None):
        return SimpleNamespace(tests_green=True, coverage_pct=97.0, ruff_violations=0)


def test_qa_node_writes_stop_eval_inputs():
    stop_eval = make_qa_node(_SDK())({})["stop_eval"]
    assert stop_eval["tests_green"] is True
    assert stop_eval["ruff_zero"] is True
    assert stop_eval["coverage_pct"] == 97.0


def test_qa_node_flags_ruff_violations():
    class _Bad(_SDK):
        def run_quality_gates(self, repo_path=None):
            return SimpleNamespace(tests_green=False, coverage_pct=80.0, ruff_violations=3)

    stop_eval = make_qa_node(_Bad())({})["stop_eval"]
    assert stop_eval["tests_green"] is False
    assert stop_eval["ruff_zero"] is False
