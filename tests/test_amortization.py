"""TDD tests for the amortization calculator (task 12.031)."""

from archlens.metrics.amortization import compute_amortization


def test_break_even_is_ceil_of_build_over_savings():
    assert compute_amortization(graph_build_tokens=1000, per_query_savings=300).break_even_queries == 4


def test_exact_division_break_even():
    assert compute_amortization(900, 300).break_even_queries == 3


def test_non_positive_savings_returns_none():
    assert compute_amortization(1000, 0).break_even_queries is None
    assert compute_amortization(1000, -5).break_even_queries is None
