"""StopConditionEvaluator — the 5 Part C stop conditions plus the 5-iteration cap (task 11.042).

Composes the Phase 11 graph-diff and load-shift signals into a per-condition verdict vector and
returns CONTINUE/STOP. The loop stops when all conditions are met (converged) or the cap is hit.
"""

from ..metrics.graph_diff import modularity_improved, new_isolated_components
from ..metrics.load_shift import dependencies_lost
from ..shared.constants import MAX_LOOP_ITERATIONS, LoopVerdict, StopCondition


class StopConditionEvaluator:
    """Evaluates SC-1..SC-5 over consecutive snapshots and applies the iteration hard cap."""

    def __init__(self, max_iterations: int = MAX_LOOP_ITERATIONS):
        self._cap = max_iterations

    def conditions(self, before, after, target, tests_green, ruff_zero) -> dict[str, bool]:
        """Return the SC-1..SC-5 verdict vector for one before/after iteration."""
        return {
            StopCondition.DEPENDENCIES_LOST.value: dependencies_lost(before, after, target),
            StopCondition.MODULARITY_IMPROVED.value: modularity_improved(before, after),
            StopCondition.NO_NEW_ISOLATES.value: not new_isolated_components(before, after),
            StopCondition.TESTS_GREEN.value: bool(tests_green),
            StopCondition.RUFF_ZERO.value: bool(ruff_zero),
        }

    def decide(self, conditions: dict[str, bool], iteration: int) -> dict:
        """Map a condition vector and iteration count to a STOP/CONTINUE verdict."""
        met = all(conditions.values())
        at_cap = iteration >= self._cap
        verdict = LoopVerdict.STOP if (met or at_cap) else LoopVerdict.CONTINUE
        return {"verdict": verdict, "conditions": conditions, "met": met, "at_cap": at_cap}

    def evaluate(self, before, after, target, tests_green, ruff_zero, iteration) -> dict:
        """Compute the conditions from snapshots and decide STOP/CONTINUE in one call."""
        return self.decide(self.conditions(before, after, target, tests_green, ruff_zero), iteration)
