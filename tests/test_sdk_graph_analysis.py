"""TDD tests for the Phase 6 analysis facade on ArchLensSDK (tasks 6.051-6.052)."""

from pathlib import Path

from archlens.sdk.sdk import ArchLensSDK

FIXTURES = Path(__file__).resolve().parent / "fixtures" / "graphify"

ANALYSIS_METHODS = [
    "load_analysis_graph",
    "node_centrality",
    "classify_nodes",
    "density_communities",
    "folder_mismatches",
    "modularity_score",
    "bridge_report",
    "critical_paths",
    "single_points_of_failure",
    "triage_edges",
    "duplicate_review_queue",
    "macro_view",
    "meso_view",
    "micro_view",
    "query_graph",
    "shortest_path",
    "explain_edge",
    "diff_analysis_graphs",
]


def _auth_graph() -> dict:
    chain = [
        ("controller", "validator", "validates"),
        ("validator", "session_store", "writes_session"),
        ("session_store", "policy", "checks_policy"),
    ]
    nodes = [{"id": n, "type": "code", "source_file": f"{n}.py"}
             for n in ("controller", "validator", "session_store", "policy")]
    edges = [{"from": u, "to": v, "relation": r, "type": "EXTRACTED",
              "confidence": 0.95, "source_file": f"{u}.py"} for u, v, r in chain]
    return {"nodes": nodes, "edges": edges}


def test_sdk_exposes_every_phase6_analysis_method():
    for name in ANALYSIS_METHODS:
        assert callable(getattr(ArchLensSDK, name, None)), name


def test_end_to_end_analysis_on_full_fixture():
    sdk = ArchLensSDK()
    graph = sdk.load_analysis_graph(FIXTURES / "full.json")
    macro = sdk.macro_view(graph)
    assert macro.node_count == 6
    assert macro.edge_count == 5
    assert sdk.node_centrality(graph)[0].degree_total >= 1
    communities = sdk.density_communities(graph)
    assert len(communities) >= 1
    assert isinstance(sdk.bridge_report(graph, communities).structural, tuple)
    buckets = sdk.triage_edges(graph)
    assert sum(len(items) for items in buckets.values()) == 5


def test_sdk_detects_session_store_spof():
    sdk = ArchLensSDK()
    graph = sdk.load_analysis_graph(_auth_graph())
    assert "session_store" in {f.node_id for f in sdk.single_points_of_failure(graph)}
