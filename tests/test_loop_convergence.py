"""End-to-end convergence test for the improvement loop on the fixture repo (task 11.049).

Per Guidelines V3 §6, Graphify and the target suite are mocked (regraph/gate injected); git
branching is real, and the StopConditionEvaluator and report generator are the production code.
"""

from pathlib import Path
from types import SimpleNamespace

from archlens.agents.loop_controller import LoopController, LoopDeps
from archlens.agents.stop_evaluator import StopConditionEvaluator
from archlens.metrics.iteration_report import iteration_report
from archlens.shared.gitops import IterationBrancher

FIXTURES = Path(__file__).resolve().parent / "fixtures"


def _graph(nodes, edges):
    return {
        "nodes": [{"id": n, "type": "code", "source_file": f"{n}.py"} for n in nodes],
        "edges": [{"from": a, "to": b, "relation": "calls", "type": "EXTRACTED",
                   "confidence": 0.8, "source_file": f"{a}.py"} for a, b in edges],
    }


_NODES = ["a", "b", "e", "c", "d", "f", "t"]
_TRI = [("a", "b"), ("b", "e"), ("e", "a"), ("c", "d"), ("d", "f"), ("f", "c")]
_BEFORE = _graph(_NODES, [*_TRI, ("a", "t"), ("b", "t"), ("t", "c"), ("t", "d")])
_AFTER = _graph(_NODES, [*_TRI, ("a", "t"), ("b", "c")])


def test_loop_convergence_within_five_iterations(git_repo_factory, tmp_path):
    repo = git_repo_factory(FIXTURES / "loop_target")
    report_dir = tmp_path / "reports"

    def regraph(path, iteration):
        return (_BEFORE, _AFTER) if iteration >= 2 else (_BEFORE, _BEFORE)

    def report(i, fix, conditions, result):
        rows = [{"metric": "Target node degree", "before": 4, "after": 1, "sc": "SC-1"}]
        decision = {"decision": result["verdict"].value, "condition": "SC-1",
                    "citation": "calls -> 0.95 -> t.py"}
        return iteration_report(report_dir, i, fix, rows, decision)

    deps = LoopDeps(
        repo_path=repo,
        brancher=IterationBrancher(repo, "fix/iter"),
        gate=SimpleNamespace(verdict=lambda path: "PASS"),
        evaluator=StopConditionEvaluator(),
        apply=lambda fix, path: None,
        regraph=regraph,
        report=report,
    )
    candidates = [
        {"fix_id": "spof-core", "node_id": "t", "kind": "spof"},
        {"fix_id": "dup-merge", "node_id": "t", "kind": "duplicate"},
    ]
    result = LoopController(deps).run(candidates)
    assert result.iterations <= 5
    assert result.iterations == 2
    assert result.stop_reason == "stop_conditions_met"
    assert (report_dir / "iteration_01.md").exists()
    assert (report_dir / "iteration_02.md").exists()
