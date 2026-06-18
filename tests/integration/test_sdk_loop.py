"""SDK-level integration: run_loop hard cap and stop-condition early exit (task 8.049)."""

from types import SimpleNamespace

from _orch_sdk import OrchSDK


def test_run_loop_reaches_hard_cap_when_stop_never_met(tmp_path):
    result = OrchSDK().run_loop(db_path=str(tmp_path / "l.sqlite"))
    assert result.iterations == 5
    assert result.stop_reason == "hard_cap"
    assert result.tokens_used == 130  # real token total surfaced from the MetricsAgent ledger


def test_run_loop_exits_early_when_stop_conditions_met(tmp_path):
    class _MetSDK(OrchSDK):
        def run_graphify_pipeline(self, repo):
            return SimpleNamespace(
                graph_json="g.json", node_count=10, edge_count=8, report_md="R.md",
                # SC-1 converges when the bottleneck shed dependencies (dependency_loss > 0).
                diff={"dependency_loss": 1, "modularity_improved": True, "new_isolates": False},
            )

    result = _MetSDK().run_loop(db_path=str(tmp_path / "m.sqlite"))
    assert result.stop_reason == "stop_conditions_met"
    assert result.iterations < 5
