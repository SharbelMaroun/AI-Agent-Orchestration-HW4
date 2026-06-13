"""TDD tests for community detection and the COMMUNITY != FOLDER comparator (6.012-6.015)."""

from fixtures import build_two_community

from archlens.graphops.communities import community_folder_mismatches, detect_communities
from archlens.graphops.loader import load_graph


def test_detect_finds_the_known_two_block_partition():
    graph = load_graph(build_two_community())
    blocks = {frozenset(community) for community in detect_communities(graph)}
    assert blocks == {
        frozenset({"x0", "x1", "x2"}),
        frozenset({"y0", "y1", "y2"}),
    }


def _folder_graph() -> dict:
    return {
        "nodes": [
            {"id": "a1", "type": "code", "source_file": "pkga/a1.py"},
            {"id": "a2", "type": "code", "source_file": "pkga/a2.py"},
            {"id": "b1", "type": "code", "source_file": "pkgb/b1.py"},
            {"id": "b2", "type": "code", "source_file": "pkgb/b2.py"},
        ],
        "edges": [],
    }


def test_folder_mismatch_lists_node_with_community_id_and_folder():
    graph = load_graph(_folder_graph())
    communities = [{"a1", "a2", "b1"}, {"b2"}]
    mismatches = community_folder_mismatches(graph, communities)
    assert len(mismatches) == 1
    odd = mismatches[0]
    assert odd.node_id == "b1"
    assert odd.community_id == 0
    assert odd.folder == "pkgb"


def test_folder_mismatch_empty_when_communities_match_folders():
    graph = load_graph(_folder_graph())
    communities = [{"a1", "a2"}, {"b1", "b2"}]
    assert community_folder_mismatches(graph, communities) == []
