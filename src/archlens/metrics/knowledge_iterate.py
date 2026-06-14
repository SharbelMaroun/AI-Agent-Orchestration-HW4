"""Knowledge iterate cycle: score -> fix weakest metric -> re-measure, max 3 cycles (task 14.042).

Stops when every metric meets the target, or after the cycle cap. Each cycle is reported (and can
be journaled to log.md by the caller). The corrector applies a targeted wiki/skill fix and returns
updated scores; it is injected so the cycle stays pure and testable.
"""

from ..shared.constants import RUBRIC_METRICS

DEFAULT_TARGET = 8
MAX_CYCLES = 3


def weakest_metric(scores: dict) -> str:
    """The metric with the lowest score (ties broken by the fixed metric order)."""
    return min(RUBRIC_METRICS, key=lambda metric: (scores[metric], RUBRIC_METRICS.index(metric)))


def _all_meet(scores: dict, target: int) -> bool:
    return all(scores[metric] >= target for metric in RUBRIC_METRICS)


def iterate(initial_scores: dict, corrector, target: int = DEFAULT_TARGET,
            max_cycles: int = MAX_CYCLES, log_fn=None) -> dict:
    """Run correction cycles until all metrics >= target or max_cycles is reached."""
    scores = dict(initial_scores)
    cycles = []
    while len(cycles) < max_cycles and not _all_meet(scores, target):
        metric = weakest_metric(scores)
        scores = corrector(scores, metric)
        cycles.append({"metric": metric, "score": scores[metric]})
        if log_fn is not None:
            log_fn(metric, scores[metric])
    stopped = "target_met" if _all_meet(scores, target) else "max_cycles"
    return {"final": scores, "cycles": cycles, "stopped": stopped}
