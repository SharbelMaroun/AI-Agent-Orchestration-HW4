"""SDK-level integration: analyze -> build_vault -> measure_tokens end-to-end (task 8.048)."""

from types import SimpleNamespace

from _orch_sdk import OrchSDK


def test_full_sdk_flow_against_stub_gatekeeper(tmp_path):
    class _FlowSDK(OrchSDK):
        def build_vault(self, graph_source, raw_sources=None):
            return SimpleNamespace(root="/vault")

    sdk = _FlowSDK()
    report = sdk.analyze(db_path=str(tmp_path / "a.sqlite"))
    assert report.node_count == 10
    assert sdk.build_vault("g.json").root == "/vault"
    assert sdk.measure_tokens().savings_pct == 70.0
