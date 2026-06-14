"""TDD tests for the LoopController improvement-loop subgraph (task 11.045)."""

from types import SimpleNamespace

from archlens.agents.loop_controller import LoopController, LoopDeps, build_loop_subgraph
from archlens.agents.loop_wiring import build_loop_deps
from archlens.agents.stop_evaluator import StopConditionEvaluator
from archlens.sdk.sdk import ArchLensSDK
from archlens.shared.constants import LoopVerdict


def _graph(nodes, edges):
    return {
        "nodes": [{"id": n, "type": "code", "source_file": f"{n}.py"} for n in nodes],
        "edges": [{"from": a, "to": b, "relation": "calls", "type": "EXTRACTED",
                   "confidence": 0.8, "source_file": f"{a}.py"} for a, b in edges],
    }


_BOTTLENECK = _graph(["t", "a", "b", "c", "m"], [("a", "t"), ("b", "t"), ("c", "t"), ("t", "m")])


def _never(path, iteration):
    return _BOTTLENECK, _BOTTLENECK


def _deps(regraph, reports):
    return LoopDeps(
        repo_path="repo",
        brancher=SimpleNamespace(create=lambda i, slug: f"fix/iter-{i:02d}-{slug}"),
        gate=SimpleNamespace(verdict=lambda path: "PASS"),
        evaluator=StopConditionEvaluator(),
        apply=lambda fix, path: None,
        regraph=regraph,
        report=lambda i, fix, conds, result: reports.append(i) or f"r{i}",
    )


def test_build_subgraph_has_the_four_loop_nodes():
    nodes = set(build_loop_subgraph(_deps(_never, [])).get_graph().nodes)
    assert {"select_fix", "apply_fix", "regraph_diff", "evaluate"} <= nodes


def test_loop_halts_at_hard_cap_when_never_converging():
    reports = []
    candidates = [{"fix_id": f"f{i}", "node_id": "t"} for i in range(8)]
    result = LoopController(_deps(_never, reports)).run(candidates)
    assert result.iterations == 5
    assert result.stop_reason == "hard_cap"
    assert len(reports) == 5


def test_loop_exits_when_queue_empties():
    reports = []
    result = LoopController(_deps(_never, reports)).run([{"fix_id": "only", "node_id": "t"}])
    assert result.stop_reason == "queue_empty"
    assert result.iterations == 1


def test_sdk_run_improvement_loop_delegates_to_controller():
    deps = _deps(_never, [])
    result = ArchLensSDK().run_improvement_loop(candidates=[{"fix_id": "x", "node_id": "t"}], deps=deps)
    assert result.iterations == 1
    assert result.stop_reason == "queue_empty"


def test_build_loop_deps_assembles_real_components(tmp_path):
    deps = build_loop_deps(ArchLensSDK(), tmp_path, tmp_path)
    assert isinstance(deps, LoopDeps)
    assert deps.evaluator.__class__.__name__ == "StopConditionEvaluator"
    before, after = deps.regraph(tmp_path, 1)
    assert before == after  # no structural change without an applied fix
    assert deps.apply({"fix_id": "x"}, tmp_path) is None
    report = deps.report(1, {"fix_id": "x"}, {"SC-1": True}, {"verdict": LoopVerdict.STOP})
    assert report.name == "iteration_01.md"
