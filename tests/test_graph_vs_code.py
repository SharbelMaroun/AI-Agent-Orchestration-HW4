"""Tests for the with/without-Graphify evaluation (token + quality comparison)."""

import networkx as nx

from archlens.metrics.graph_vs_code import _parse_scores, compare
from archlens.sdk.sdk import ArchLensSDK


def test_parse_scores_reads_the_two_ratings():
    assert _parse_scores("WITH: 4 WITHOUT: 3") == (4, 3)
    assert _parse_scores("WITH: 5 only") == (5, 0)
    assert _parse_scores("no numbers here") == (0, 0)


def _graph(tmp_path):
    g = nx.DiGraph()
    g.add_edge("a", "hub")
    g.add_edge("b", "hub")           # hub has the highest in-degree
    g.add_node("hub", source_file="hub.py")
    (tmp_path / "hub.py").write_text("class Hub:\n    pass\n", encoding="utf-8")
    return g


def test_compare_evaluates_both_modes_and_aggregates(tmp_path):
    # mock mode (autouse) -> deterministic token counts and canned answers.
    report = compare(ArchLensSDK(), _graph(tmp_path), str(tmp_path), top_k=1)
    assert len(report["rows"]) == 1 and report["rows"][0]["node"] == "hub"
    assert report["with_tokens"] > 0 and report["without_tokens"] > 0
    assert "token_savings_pct" in report
    assert "with_quality" in report and "without_quality" in report


def test_sdk_entry_point_delegates(tmp_path, monkeypatch):
    graph_json = tmp_path / "g.json"
    graph_json.write_text("{}", encoding="utf-8")  # load_analysis_graph is monkeypatched below
    sdk = ArchLensSDK()
    monkeypatch.setattr(sdk, "load_analysis_graph", lambda _src: _graph(tmp_path))
    report = sdk.compare_graph_vs_code(str(graph_json), str(tmp_path), top_k=1)
    assert report["rows"][0]["node"] == "hub"
