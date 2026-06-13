"""Detect shared flows (modules serving 2+ requirements) and duplicate flows (task 7.027)."""

from collections import defaultdict
from dataclasses import dataclass
from pathlib import Path

from archlens.graphops.dto import DuplicatePair
from archlens.graphops.duplicates import find_duplicates
from archlens.graphops.loader import load_graph
from archlens.graphops.req_matcher import Match


@dataclass(frozen=True)
class SharedFlow:
    """A module that serves two or more requirements."""

    module: str
    req_ids: tuple[str, ...]


def detect_shared_flows(matches: list[Match]) -> list[SharedFlow]:
    """Modules matched by two or more distinct requirements, sorted by module id."""
    by_module: dict[str, set[str]] = defaultdict(set)
    for match in matches:
        by_module[match.module].add(match.req_id)
    flows = [SharedFlow(module, tuple(sorted(reqs)))
             for module, reqs in by_module.items() if len(reqs) >= 2]
    flows.sort(key=lambda f: f.module)
    return flows


def detect_duplicate_flows(graph_source: dict | str | Path) -> list[DuplicatePair]:
    """Duplicate-logic candidates: semantically-similar edges at the configured threshold."""
    return find_duplicates(load_graph(graph_source))
