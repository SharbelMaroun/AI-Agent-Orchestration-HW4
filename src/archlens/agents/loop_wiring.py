"""Production wiring for the improvement loop: assemble LoopDeps from the SDK (task 11.046).

Fix application and re-graphify delegate to the SDK — ``apply_fix`` is the single writer and
``run_graphify_pipeline`` the single Graphify entry point — so this convenience entry can
genuinely converge, not stall on a no-op. Irreversible refactors stay guardrail-gated inside the
SDK apply path (PRD_improvement_loop §10); branching, the test gate, and stop evaluation are real.
"""

from pathlib import Path

from ..graphops.errors import GraphSchemaError
from ..metrics.iteration_report import iteration_report
from ..shared.constants import GRAPH_JSON, GRAPHIFY_OUT_DIR
from ..shared.gitops import IterationBrancher
from .loop_controller import LoopDeps
from .stop_evaluator import StopConditionEvaluator
from .test_gate import TestGate

_EMPTY_GRAPH = {"nodes": [], "edges": []}


def _make_apply(sdk):
    """Apply the selected fix through the SDK (the single writer); returns whether a file changed."""
    def apply(fix, repo_path):
        return sdk.apply_fix(fix, str(repo_path), fix.get("graph_json"))
    return apply


def _snapshot_before(graph_path: Path):
    """Copy the current graph aside as the 'before' snapshot, or an empty graph if none exists."""
    if not graph_path.is_file():
        return _EMPTY_GRAPH
    backup = graph_path.with_name("graph.prev.json")
    backup.write_text(graph_path.read_text(encoding="utf-8"), encoding="utf-8")
    return str(backup)


def _make_regraph(sdk):
    """Re-run Graphify via the SDK and return real (before, after) graph snapshots for the diff."""
    def regraph(repo_path, iteration):
        graph_path = Path(repo_path) / GRAPHIFY_OUT_DIR / GRAPH_JSON
        before = _snapshot_before(graph_path)
        try:
            result = sdk.run_graphify_pipeline(str(repo_path))
            after = getattr(result, "graph_json", None) or str(graph_path)
        except (OSError, ValueError, RuntimeError, GraphSchemaError):
            after = before  # a failed re-graph yields no structural change this round
        return before, after
    return regraph


def _make_report(report_dir):
    def report(iteration, fix, conditions, result):
        rows = [{"metric": key, "before": "", "after": "", "sc": key} for key in conditions]
        decision = {"decision": result["verdict"].value, "condition": "",
                    "citation": fix.get("citation", "")}
        return iteration_report(report_dir, iteration, fix, rows, decision)
    return report


def build_loop_deps(sdk, repo_path=".", report_dir="reports") -> LoopDeps:
    """Assemble the production LoopDeps from SDK config and the Phase 11 components."""
    cfg = sdk._config().improvement_loop
    return LoopDeps(
        repo_path=repo_path,
        brancher=IterationBrancher(repo_path, cfg.branch_prefix),
        gate=TestGate(),
        evaluator=StopConditionEvaluator(cfg.max_iterations),
        apply=_make_apply(sdk),
        regraph=_make_regraph(sdk),
        report=_make_report(report_dir),
    )
