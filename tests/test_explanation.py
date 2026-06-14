"""TDD tests for the savings-explanation flow (task 12.038)."""

from archlens.metrics.amortization import compute_amortization
from archlens.metrics.explanation import render_explanation, write_explanation_if_needed
from archlens.metrics.savings import compute_savings


def test_explanation_has_no_remaining_placeholders():
    savings = compute_savings(1000, 500)  # 50% < 70% target
    amort = compute_amortization(graph_build_tokens=2000, per_query_savings=500)
    text = render_explanation(savings, amort)
    assert "{{" not in text
    assert "50.00" in text
    assert "2000" in text


def test_writes_file_when_target_missed(tmp_path):
    savings = compute_savings(1000, 500)
    amort = compute_amortization(2000, 500)
    out = tmp_path / "SAVINGS_EXPLANATION.md"
    result = write_explanation_if_needed(savings, amort, path=out)
    assert result == out
    assert out.is_file()
    assert "{{" not in out.read_text(encoding="utf-8")


def test_no_file_when_target_met(tmp_path):
    savings = compute_savings(1000, 100)  # 90% >= 70%
    amort = compute_amortization(2000, 900)
    out = tmp_path / "SAVINGS_EXPLANATION.md"
    assert write_explanation_if_needed(savings, amort, path=out) is None
    assert not out.exists()
