"""TDD tests for the ISO/IEC 25010 quality mapping (task 15.011)."""

from archlens.metrics.iso25010_mapping import iso25010_table

_ISO_8 = ("Functional Suitability", "Performance Efficiency", "Compatibility", "Usability",
          "Reliability", "Security", "Maintainability", "Portability")


def test_table_covers_all_eight_iso_characteristics():
    table = iso25010_table({"coverage_pct": 97, "modularity": 138,
                            "token_savings_pct": 97.6, "ruff_violations": 0})
    rows = [line for line in table.splitlines()
            if line.startswith("| ") and "Characteristic" not in line and "---" not in line]
    assert len(rows) == 8
    for characteristic in _ISO_8:
        assert characteristic in table


def test_measured_values_are_filled_from_metrics():
    table = iso25010_table({"coverage_pct": 97})
    assert "97" in table
