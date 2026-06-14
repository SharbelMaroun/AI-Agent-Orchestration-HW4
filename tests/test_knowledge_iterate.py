"""TDD tests for the knowledge iterate cycle (task 14.042)."""

from archlens.metrics.knowledge_iterate import iterate, weakest_metric
from archlens.shared.constants import RUBRIC_METRICS


def _scores(values):
    return dict(zip(RUBRIC_METRICS, values, strict=True))


def _bump(scores, metric, amount=5):
    updated = dict(scores)
    updated[metric] = min(10, updated[metric] + amount)
    return updated


def test_weakest_metric_picks_lowest():
    assert weakest_metric(_scores([9, 3, 8, 7])) == RUBRIC_METRICS[1]


def test_stops_when_target_met():
    result = iterate(_scores([9, 3, 9, 9]), _bump, target=8)
    assert result["stopped"] == "target_met"
    assert len(result["cycles"]) == 1


def test_stops_after_max_cycles():
    result = iterate(_scores([1, 1, 1, 1]), lambda s, m: s, target=8, max_cycles=3)
    assert result["stopped"] == "max_cycles"
    assert len(result["cycles"]) == 3


def test_cycle_logs_each_correction():
    logged = []
    iterate(_scores([9, 3, 9, 9]), _bump, target=8, log_fn=lambda m, s: logged.append(m))
    assert logged == [RUBRIC_METRICS[1]]
