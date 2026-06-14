"""TDD tests for the 4-metric knowledge rubric model (task 14.030)."""

import pytest

from archlens.metrics.knowledge_rubric import MetricScore, RubricScore
from archlens.shared.constants import RUBRIC_METRICS


def _full_scores():
    return tuple(MetricScore(metric, 7, "ok") for metric in RUBRIC_METRICS)


def test_valid_rubric_has_four_metrics_and_total():
    rubric = RubricScore(_full_scores())
    assert len(rubric.scores) == 4
    assert rubric.total() == 28
    assert set(rubric.as_dict()) == set(RUBRIC_METRICS)


def test_score_out_of_range_rejected():
    with pytest.raises(ValueError):
        MetricScore("noise_reduction", 11, "too high")
    with pytest.raises(ValueError):
        MetricScore("noise_reduction", -1, "too low")


def test_missing_rationale_rejected():
    with pytest.raises(ValueError):
        MetricScore("noise_reduction", 5, "")


def test_unknown_metric_rejected():
    with pytest.raises(ValueError):
        MetricScore("made_up_metric", 5, "rationale")


def test_rubric_requires_exactly_the_four_metrics():
    with pytest.raises(ValueError):
        RubricScore(_full_scores()[:3])
