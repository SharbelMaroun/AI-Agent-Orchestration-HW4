"""Density-based community detection — never derived from folders (tasks 6.013, 6.015)."""

from collections import Counter

import networkx as nx
from networkx.algorithms.community import greedy_modularity_communities

from archlens.graphops.dto import FolderMismatch


def _folder(source_file: str) -> str:
    return source_file.rsplit("/", 1)[0] if "/" in source_file else "."


def detect_communities(graph: nx.DiGraph) -> list[frozenset[str]]:
    """Detect communities by greedy modularity on the undirected projection.

    Communities are density-based, not folder-based (Part C p8). Returned sorted by the
    smallest member id so the partition is deterministic across runs.
    """
    undirected = graph.to_undirected()
    communities = greedy_modularity_communities(undirected)
    blocks = [frozenset(community) for community in communities]
    blocks.sort(key=lambda block: min(block))
    return blocks


def community_folder_mismatches(
    graph: nx.DiGraph, communities: list[set[str]]
) -> list[FolderMismatch]:
    """Flag nodes whose community disagrees with their folder (COMMUNITY != FOLDER, Part C p8).

    Each community's dominant folder is the most common folder among its members (ties broken
    by folder name). A node mismatches when its own folder differs from that dominant folder.
    """
    mismatches: list[FolderMismatch] = []
    for community_id, members in enumerate(communities):
        folders = {node: _folder(graph.nodes[node].get("source_file", "")) for node in members}
        counts = Counter(folders.values())
        dominant = min(counts, key=lambda folder: (-counts[folder], folder))
        for node, folder in folders.items():
            if folder != dominant:
                mismatches.append(FolderMismatch(node, community_id, folder, dominant))
    mismatches.sort(key=lambda mismatch: mismatch.node_id)
    return mismatches
