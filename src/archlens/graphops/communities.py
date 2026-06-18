"""Community detection plus the graph.json cluster loader (tasks 6.013, 6.015, 7.004)."""

import json
from collections import Counter
from dataclasses import dataclass
from pathlib import Path

import networkx as nx
from networkx.algorithms.community import greedy_modularity_communities

from ..graphops.dto import FolderMismatch


@dataclass(frozen=True)
class LoadedCommunity:
    """One cluster parsed from a Graphify graph.json communities section."""

    community_id: str
    label: str
    members: tuple[str, ...]
    inter_community_edge_count: int


def load_communities(source: dict | str | Path) -> list[LoadedCommunity]:
    """Parse the cluster section of a graph.json into LoadedCommunity records.

    Supports both the canonical ``communities`` array and the NetworkX node-link format
    `graphify update` emits, where membership lives on each node's ``community`` field.
    """
    data = source if isinstance(source, dict) else json.loads(Path(source).read_text(encoding="utf-8"))
    explicit = data.get("communities")
    if explicit:
        return [
            LoadedCommunity(
                community_id=c["community_id"],
                label=c.get("label", c["community_id"]),
                members=tuple(c.get("node_ids", [])),
                inter_community_edge_count=c.get("inter_community_edge_count", 0),
            )
            for c in explicit
        ]
    return _communities_from_nodes(data.get("nodes", []))


def _communities_from_nodes(nodes: list[dict]) -> list[LoadedCommunity]:
    """Reconstruct communities from per-node ``community`` ids (node-link schema).

    Each cluster is labelled by the leaf of its members' dominant source directory plus the
    community id (kept unique), so the block diagram reads as folders rather than opaque ids.
    """
    groups: dict[object, list[tuple[str, str]]] = {}
    for node in nodes:
        cid = node.get("community")
        if cid is not None:
            groups.setdefault(cid, []).append((node["id"], node.get("source_file", "")))
    return [
        LoadedCommunity(
            community_id=str(cid),
            label=_community_label(cid, [sf for _, sf in members]),
            members=tuple(nid for nid, _ in members),
            inter_community_edge_count=0,
        )
        for cid, members in sorted(groups.items(), key=lambda kv: str(kv[0]))
    ]


def _community_label(community_id: object, source_files: list[str]) -> str:
    """Name a node-link community by the leaf of its dominant directory, suffixed with the id."""
    folders = Counter(_folder(sf) for sf in source_files if sf)
    if not folders:
        return f"community-{community_id}"
    dominant = min(folders, key=lambda folder: (-folders[folder], folder))
    leaf = dominant.rsplit("/", 1)[-1] if dominant != "." else "root"
    return f"{leaf} (c{community_id})"


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
