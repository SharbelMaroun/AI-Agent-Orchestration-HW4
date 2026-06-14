"""TDD tests for the cost table generator (task 12.033)."""

from archlens.metrics.cost_tables import render_cost_table, write_cost_table


def test_table_has_required_columns(synthetic_ledger):
    table = render_cost_table(synthetic_ledger(n=10))
    for column in ("model", "input tokens", "output tokens", "$/MTok in", "$/MTok out", "total $"):
        assert column in table


def test_totals_row_is_last(synthetic_ledger):
    table = render_cost_table(synthetic_ledger(n=10))
    table_rows = [line for line in table.splitlines() if line.startswith("|")]
    assert "TOTAL" in table_rows[-1]
    assert "TOTAL" not in "\n".join(table_rows[:-1])


def test_write_creates_file(tmp_path, synthetic_ledger):
    out = tmp_path / "COST_TABLES.md"
    write_cost_table(synthetic_ledger(n=10), path=out)
    assert out.is_file()
    assert "TOTAL" in out.read_text(encoding="utf-8")
