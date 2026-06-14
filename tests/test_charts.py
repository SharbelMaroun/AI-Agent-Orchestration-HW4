"""TDD tests for token-savings chart generation (task 12.042)."""

from archlens.metrics.charts import BAR_PNG, WATERFALL_PNG, generate_charts


def test_both_charts_created_non_empty(tmp_path, synthetic_ledger):
    baseline = synthetic_ledger(n=10)
    assisted = synthetic_ledger(n=10)
    bar, waterfall = generate_charts(baseline, assisted, tmp_path)
    assert bar.name == BAR_PNG
    assert waterfall.name == WATERFALL_PNG
    assert bar.is_file() and bar.stat().st_size > 0
    assert waterfall.is_file() and waterfall.stat().st_size > 0
