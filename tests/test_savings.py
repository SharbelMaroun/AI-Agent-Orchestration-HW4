"""TDD tests for the savings calculator (task 12.029)."""

import pytest

from archlens.metrics.savings import compute_savings


def test_savings_percentage_formula():
    assert compute_savings(1000, 250).savings_pct == pytest.approx(75.0)


def test_target_met_at_seventy_percent_threshold():
    assert compute_savings(100, 30).target_met is True   # exactly 70%
    assert compute_savings(100, 31).target_met is False  # 69%


def test_custom_target_threshold():
    assert compute_savings(100, 20, target_pct=75.0).target_met is True   # 80% >= 75
    assert compute_savings(100, 30, target_pct=75.0).target_met is False  # 70% < 75


def test_zero_baseline_is_guarded():
    savings = compute_savings(0, 0)
    assert savings.savings_pct == 0.0
    assert savings.target_met is False
