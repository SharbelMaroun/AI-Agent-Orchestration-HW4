"""Phase 8 orchestration facade: analyze, run_loop, measure_tokens (8.021, 8.025, 8.027).

These run the LangGraph orchestration built in Phase 10, keeping the SDK the single entry point.
"""

import json
from pathlib import Path

from ..agents.contracts import QAReport
from ..agents.metrics_agent import make_metrics_node
from ..agents.quality_gates import run_quality_gates
from ..agents.runner import make_runner
from ..sdk.dto_core import AnalysisReport
from ..sdk.dto_loop import LoopResult, TokenReport
from ..sdk.sandbox import SandboxManager
from ..shared.config import RepoBlock


def _analysis_report(state: dict) -> AnalysisReport:
    snapshot = state.get("graph_snapshot") or {}
    findings = state.get("findings") or []
    hubs = tuple(f["node"] for f in findings if f.get("category") == "centrality")
    bottlenecks = tuple(f["node"] for f in findings
                        if f.get("category") == "hub_vs_bottleneck" and f.get("verdict") == "BOTTLENECK")
    spofs = tuple(f["node_id"] for f in findings if f.get("category") == "SPOF")
    communities = next((f["count"] for f in findings if f.get("category") == "community_count"), 0)
    return AnalysisReport(snapshot.get("node_count", 0), snapshot.get("edge_count", 0),
                          communities, hubs, bottlenecks, spofs)


class OrchestrationMixin:
    """Single-entry SDK methods that drive the multi-agent orchestration graph."""

    def analyze(self, db_path: str | None = None, thread_id: str = "analyze",
                repo_path: str | None = None) -> AnalysisReport:
        """Run RepoAgent -> GraphAgent -> AnalystAgent and return an AnalysisReport.

        ``repo_path`` injects an already-cloned checkout so the run skips RepoAgent and graphs that
        repo directly (used by the interactive ``start`` flow after the user picked + cloned a repo).
        """
        graph = make_runner(self, db_path=db_path, interrupt_after=["AnalystAgent"])
        config = {"configurable": {"thread_id": thread_id}}
        initial = {"target_repo": {"local_path": repo_path, "validated": True}} if repo_path else {}
        graph.invoke(initial, config)
        return _analysis_report(graph.get_state(config).values)

    def suggested_repos(self) -> list:
        """Repos offered in the interactive picker (lecturer's suggestions + approved targets)."""
        return self._config().suggested_repos

    def clone_url(self, url: str, run_id: str = "manual") -> Path:
        """Clone an arbitrary git URL (default branch) into the sandbox; raise RepoError on failure."""
        base = self._config().target_repo
        repo = RepoBlock(url=url, branch="", pinned_commit="", workdir_root=base.workdir_root,
                         clone_depth=base.clone_depth, timeout_s=base.timeout_s,
                         max_size_mb=base.max_size_mb)
        sandbox = SandboxManager(repo.workdir_root)
        sandbox.create_run_dir(run_id)
        return self._gk().git_clone(repo, sandbox.fresh_target(run_id))

    def reset_run_state(self) -> None:
        """Delete the LangGraph checkpoint DB so a fresh interactive run does not resume a prior one."""
        db = Path(self._config().sdk.checkpoint_db)
        if db.exists():
            db.unlink()

    def run_loop(self, db_path: str | None = None, thread_id: str = "loop") -> LoopResult:
        """Run the full improvement loop under the Part C stop conditions and 5-iteration cap."""
        graph = make_runner(self, db_path=db_path)
        config = {"configurable": {"thread_id": thread_id}, "recursion_limit": 100}
        graph.invoke({}, config)
        state = graph.get_state(config).values
        stop = state.get("stop_eval") or {}
        reason = "stop_conditions_met" if stop.get("met") else "hard_cap"
        diffs = tuple(f"{key}={value}" for key, value in stop.items() if key != "met")
        tokens = (state.get("token_ledger") or {}).get("total_tokens", 0)
        return LoopResult(state.get("loop_iteration", 0), reason, diffs, tokens)

    def run_improvement_loop(self, candidates=None, deps=None) -> LoopResult:
        """Run the Phase 11 improvement loop (the single SDK entry point) and return its result."""
        from ..agents.loop_controller import LoopController
        from ..agents.loop_wiring import build_loop_deps
        loop_deps = deps if deps is not None else build_loop_deps(self)
        return LoopController(loop_deps).run(candidates or [])

    def run_quality_gates(self, repo_path=None) -> QAReport:
        """Run the dependency-free QA gate over a cloned repo (parse every module)."""
        return run_quality_gates(repo_path)

    def measure_tokens(self) -> TokenReport:
        """Delegate to MetricsAgent token accounting; flag explanation when savings < 70%."""
        ledger = make_metrics_node(self)({}).get("token_ledger", {})
        baseline = ledger.get("baseline_tokens", 0)
        assisted = ledger.get("assisted_tokens", 0)
        savings = ledger.get("savings_pct", 0.0)
        if baseline or assisted:
            return TokenReport(baseline, assisted, savings, explanation_required=savings < 70.0)
        cfg = self._config()
        path = Path(cfg.metrics.output_dir) / cfg.metrics.metrics_json
        if path.is_file():
            data = json.loads(path.read_text(encoding="utf-8"))
            saved = data.get("savings", {})
            target_met = bool(data.get("target_met", saved.get("target_met", False)))
            return TokenReport(
                saved.get("baseline_tokens", 0),
                saved.get("assisted_tokens", 0),
                saved.get("savings_pct", 0.0),
                explanation_required=not target_met,
            )
        return TokenReport(baseline, assisted, savings, explanation_required=savings < 70.0)
