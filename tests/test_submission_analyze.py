"""Submission analyze path uses the committed buggy-python graph, not stale checkpoints."""

from archlens.sdk.sdk import ArchLensSDK


def test_default_analyze_uses_buggy_python_artifact():
    report = ArchLensSDK().analyze()
    assert report.node_count == 19
    assert report.edge_count == 28
    assert report.hubs[0] == "snippets_init"
