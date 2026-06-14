"""TDD tests for the per-iteration report generator (task 11.043)."""

from archlens.metrics.iteration_report import iteration_report

_FIX = {"fix_id": "spof-ss", "priority": "P1", "branch": "fix/iter-01-spof", "evidence": "VALIDATED"}
_ROWS = [{"metric": "Target node degree", "before": 4, "after": 1, "sc": "SC-1"}]
_DECISION = {"decision": "ACCEPTED", "condition": "SC-1", "citation": "critical_path -> 0.95 -> ss.py"}


def test_report_writes_iteration_file_with_table_and_log(tmp_path):
    path = iteration_report(tmp_path, 1, _FIX, _ROWS, _DECISION)
    assert path.name == "iteration_01.md"
    text = path.read_text(encoding="utf-8")
    assert "| Metric | Before | After | Delta | Stop condition |" in text
    assert "## Decision Log" in text


def test_report_computes_numeric_delta(tmp_path):
    text = iteration_report(tmp_path, 2, _FIX, _ROWS, _DECISION).read_text(encoding="utf-8")
    assert "| Target node degree | 4 | 1 | -3 | SC-1 |" in text


def test_report_includes_decision_and_citation(tmp_path):
    text = iteration_report(tmp_path, 3, _FIX, _ROWS, _DECISION).read_text(encoding="utf-8")
    assert "ACCEPTED" in text
    assert "critical_path -> 0.95 -> ss.py" in text
