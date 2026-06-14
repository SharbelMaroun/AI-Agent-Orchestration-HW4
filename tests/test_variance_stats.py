"""TDD tests for variance statistics across repeated runs (task 15.007)."""

from archlens.metrics.variance_stats import variance_stats, write_summary_csv


def test_mean_std_cv_computed():
    runs = [{"tokens": 100}, {"tokens": 110}, {"tokens": 90}]
    stats = variance_stats(runs, ["tokens"])
    assert stats["tokens"]["mean"] == 100
    assert stats["tokens"]["std"] > 0
    assert stats["tokens"]["cv"] == stats["tokens"]["std"] / 100


def test_zero_mean_cv_is_guarded():
    assert variance_stats([{"x": 0}, {"x": 0}], ["x"])["x"]["cv"] == 0.0


def test_write_summary_csv_has_mean_std_cv_columns(tmp_path):
    stats = variance_stats([{"t": 1}, {"t": 3}], ["t"])
    out = write_summary_csv(stats, tmp_path / "summary.csv")
    text = out.read_text(encoding="utf-8")
    assert "metric,mean,std,cv" in text
    assert text.count("\n") >= 2
