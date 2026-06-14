"""Production wiring for the improvement loop: assemble LoopDeps from the SDK (task 11.046).

Fix application defaults to a no-op here: irreversible refactors require human approval
(PRD_improvement_loop §10) and run through the guardrail-gated RefactorAgent path, not this
convenience entry point. Branching, the test gate, stop evaluation, and reporting are real.
"""

from ..metrics.iteration_report import iteration_report
from ..shared.gitops import IterationBrancher
from .loop_controller import LoopDeps
from .stop_evaluator import StopConditionEvaluator
from .test_gate import TestGate


def _no_apply(fix, repo_path):
    """Default fix application: no auto-write — refactors await guardrail approval (PRD §10)."""
    return None


def _unchanged_regraph(repo_path, iteration):
    """Re-graph placeholder: structure is unchanged until a guardrail-approved fix is applied."""
    snapshot = {"nodes": [], "edges": []}
    return snapshot, snapshot


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
        apply=_no_apply,
        regraph=_unchanged_regraph,
        report=_make_report(report_dir),
    )
