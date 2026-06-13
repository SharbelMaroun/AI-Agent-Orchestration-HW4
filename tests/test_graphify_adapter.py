"""TDD tests for the Graphify->canonical adapter (Phase 4 correction)."""

from archlens.graphops.adapter import load_graphify_graph
from archlens.graphops.parser import Graph
from archlens.shared.constants import EvidenceType, NodeType

NODELINK = {
    "directed": False,
    "multigraph": False,
    "graph": {},
    "nodes": [
        {"id": "a", "label": "a.py", "file_type": "code", "source_file": "a.py", "community": 0},
        {"id": "a_f", "label": "f()", "file_type": "code", "source_file": "a.py", "community": 0},
        {"id": "b", "label": "b.md", "file_type": "document", "source_file": "b.md", "community": 1},
        {"id": "a_r", "label": "why", "file_type": "rationale", "source_file": "a.py", "community": 0},
    ],
    "links": [
        {
            "source": "a",
            "target": "a_f",
            "relation": "contains",
            "confidence": "EXTRACTED",
            "confidence_score": 1.0,
            "source_file": "a.py",
        },
        {
            "source": "a_f",
            "target": "b",
            "relation": "references",
            "confidence": "INFERRED",
            "confidence_score": 0.7,
            "source_file": "a.py",
        },
    ],
    "hyperedges": [],
}


def test_loads_nodelink_format():
    graph = load_graphify_graph(NODELINK)
    assert isinstance(graph, Graph)
    assert len(graph.nodes) == 4
    assert len(graph.edges) == 2
    assert len(graph.communities) == 2


def test_maps_file_type_to_node_type():
    by_id = {n.id: n for n in load_graphify_graph(NODELINK).nodes}
    assert by_id["b"].type is NodeType.DOC
    assert by_id["a_r"].type is NodeType.RATIONALE
    assert by_id["a"].label == "a.py"


def test_maps_tier_and_pins_extracted_confidence():
    edges = {(e.src, e.dst): e for e in load_graphify_graph(NODELINK).edges}
    extracted = edges[("a", "a_f")]
    assert extracted.type is EvidenceType.EXTRACTED
    assert extracted.confidence == 0.95  # pinned from score 1.0
    assert extracted.relation == "contains"  # open vocabulary
    inferred = edges[("a_f", "b")]
    assert inferred.type is EvidenceType.INFERRED
    assert inferred.confidence == 0.7


def test_loads_canonical_from_to_format():
    canonical = {
        "nodes": [{"id": "x", "type": "code", "source_file": "x.py"}],
        "edges": [
            {
                "from": "x",
                "to": "x",
                "relation": "calls",
                "type": "EXTRACTED",
                "confidence": 0.95,
                "source_file": "x.py",
            }
        ],
        "communities": [{"community_id": "c1", "label": "core", "node_ids": ["x"]}],
    }
    graph = load_graphify_graph(canonical)
    assert graph.edges[0].src == "x"
    assert graph.edges[0].relation == "calls"
    assert graph.communities[0].label == "core"
