"""LoopController — the Phase 11 improvement-loop LangGraph subgraph (tasks 11.045-11.046).

Wires select_fix -> apply_fix -> regraph_diff -> evaluate with a conditional loop-back until the
stop conditions are met or the 5-iteration cap is hit. All heavy work (Graphify, git, the target
suite) is injected via LoopDeps so the loop is testable in mock mode (Guidelines V3 §6).
"""

from collections.abc import Callable
from dataclasses import dataclass
from typing import TypedDict

from langgraph.graph import END, START, StateGraph

from ..sdk.dto_loop import LoopResult
from ..shared.constants import LoopVerdict

_RECURSION_LIMIT = 100


@dataclass
class LoopDeps:
    """Injected components the loop nodes call (real in production, mocked in tests)."""

    brancher: object
    gate: object
    evaluator: object
    apply: Callable
    regraph: Callable
    report: Callable
    repo_path: object = "."


class LoopGraphState(TypedDict, total=False):
    """Mutable state threaded through the loop subgraph."""

    queue: list
    current: dict
    iteration: int
    branch: str
    test_verdict: str
    before: dict
    after: dict
    conditions: dict
    verdict: str
    reports: list
    stop_reason: str


def _select_fix(deps):
    def select_fix(state):
        queue = list(state.get("queue", []))
        if not queue:
            return {"verdict": LoopVerdict.STOP.value, "stop_reason": "queue_empty"}
        return {"current": queue[0], "queue": queue[1:]}
    return select_fix


def _apply_fix(deps):
    def apply_fix(state):
        iteration = state.get("iteration", 0) + 1
        fix = state["current"]
        branch = deps.brancher.create(iteration, fix["fix_id"])
        deps.apply(fix, deps.repo_path)
        return {"iteration": iteration, "branch": branch,
                "test_verdict": deps.gate.verdict(deps.repo_path)}
    return apply_fix


def _regraph_diff(deps):
    def regraph_diff(state):
        before, after = deps.regraph(deps.repo_path, state["iteration"])
        return {"before": before, "after": after}
    return regraph_diff


def _evaluate(deps):
    def evaluate(state):
        fix = state["current"]
        green = state.get("test_verdict") == "PASS"
        conditions = deps.evaluator.conditions(
            state["before"], state["after"], fix.get("node_id", ""), green, green)
        result = deps.evaluator.decide(conditions, state["iteration"])
        path = deps.report(state["iteration"], fix, conditions, result)
        return {"verdict": result["verdict"].value, "conditions": conditions,
                "reports": [*state.get("reports", []), str(path)]}
    return evaluate


def _after_select(state):
    return END if state.get("verdict") == LoopVerdict.STOP.value else "apply_fix"


def _after_evaluate(state):
    return END if state.get("verdict") == LoopVerdict.STOP.value else "select_fix"


def build_loop_subgraph(deps: LoopDeps):
    """Compile the improvement-loop StateGraph with the four loop nodes and the loop-back edge."""
    builder = StateGraph(LoopGraphState)
    builder.add_node("select_fix", _select_fix(deps))
    builder.add_node("apply_fix", _apply_fix(deps))
    builder.add_node("regraph_diff", _regraph_diff(deps))
    builder.add_node("evaluate", _evaluate(deps))
    builder.add_edge(START, "select_fix")
    builder.add_conditional_edges("select_fix", _after_select, {"apply_fix": "apply_fix", END: END})
    builder.add_edge("apply_fix", "regraph_diff")
    builder.add_edge("regraph_diff", "evaluate")
    builder.add_conditional_edges("evaluate", _after_evaluate, {"select_fix": "select_fix", END: END})
    return builder.compile()


def _result(final: dict) -> LoopResult:
    conditions = final.get("conditions") or {}
    if final.get("stop_reason") == "queue_empty":
        reason = "queue_empty"
    elif conditions and all(conditions.values()):
        reason = "stop_conditions_met"
    else:
        reason = "hard_cap"
    diffs = tuple(f"{key}={value}" for key, value in conditions.items())
    return LoopResult(final.get("iteration", 0), reason, diffs)


class LoopController:
    """Runs the improvement-loop subgraph and returns a LoopResult."""

    def __init__(self, deps: LoopDeps):
        self._deps = deps

    def run(self, candidates) -> LoopResult:
        """Execute the loop over the candidate queue (<= MAX_LOOP_ITERATIONS iterations)."""
        graph = build_loop_subgraph(self._deps)
        initial = {"queue": list(candidates), "iteration": 0, "reports": []}
        return _result(graph.invoke(initial, {"recursion_limit": _RECURSION_LIMIT}))
