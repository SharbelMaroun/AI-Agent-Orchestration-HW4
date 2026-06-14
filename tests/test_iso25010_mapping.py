"""TDD tests for the ISO/IEC 25010 quality mapping (task 15.011)."""

from archlens.metrics.iso25010_mapping import iso25010_table


def test_table_covers_at_least_six_characteristics():
    table = iso25010_table({"coverage_pct": 97, "modularity": 138,
                            "token_savings_pct": 97.6, "ruff_violations": 0})
    rows = [line for line in table.splitlines()
            if line.startswith("| ") and "Characteristic" not in line and "---" not in line]
    assert len(rows) >= 6
    assert "ISO/IEC 25010" in table


def test_measured_values_are_filled_from_metrics():
    table = iso25010_table({"coverage_pct": 97})
    assert "97" in table
