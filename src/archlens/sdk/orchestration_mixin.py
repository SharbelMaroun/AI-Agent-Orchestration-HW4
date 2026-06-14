"""Phase 8 orchestration facade: analyze, run_loop, measure_tokens (8.021, 8.025, 8.027).

These run the LangGraph orchestration built in Phase 10, keeping the SDK the single entry point.
"""

from ..agents.metrics_agent import make_metrics_node
from ..agents.runner import make_runner
from ..sdk.dto_core import AnalysisReport
from ..sdk.dto_loop import LoopResult, TokenReport


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

    def analyze(self, db_path: str | None = None, thread_id: str = "analyze") -> AnalysisReport:
        """Run RepoAgent -> GraphAgent -> AnalystAgent and return an AnalysisReport."""
        graph = make_runner(self, db_path=db_path, interrupt_after=["AnalystAgent"])
        config = {"configurable": {"thread_id": thread_id}}
        graph.invoke({}, config)
        return _analysis_report(graph.get_state(config).values)

    def run_loop(self, db_path: str | None = None, thread_id: str = "loop") -> LoopResult:
        """Run the full improvement loop under the Part C stop conditions and 5-iteration cap."""
        graph = make_runner(self, db_path=db_path)
        config = {"configurable": {"thread_id": thread_id}, "recursion_limit": 100}
        graph.invoke({}, config)
        state = graph.get_state(config).values
        stop = state.get("stop_eval") or {}
        reason = "stop_conditions_met" if stop.get("met") else "hard_cap"
        diffs = tuple(f"{key}={value}" for key, value in stop.items() if key != "met")
        return LoopResult(state.get("loop_iteration", 0), reason, diffs)

    def measure_tokens(self) -> TokenReport:
        """Delegate to MetricsAgent token accounting; flag explanation when savings < 70%."""
        ledger = make_metrics_node(self)({}).get("token_ledger", {})
        baseline = ledger.get("baseline_tokens", 0)
        assisted = ledger.get("assisted_tokens", 0)
        savings = ledger.get("savings_pct", 0.0)
        return TokenReport(baseline, assisted, savings, explanation_required=savings < 70.0)
