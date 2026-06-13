"""Build PRD->Module->Test traceability chains with per-link confidence (task 7.030)."""

import json
from dataclasses import dataclass
from pathlib import Path

from archlens.graphops.req_matcher import Match


@dataclass(frozen=True)
class TraceChain:
    """A requirement linked to a module and the tests that reference it."""

    req_id: str
    module: str
    module_confidence: float
    tests: tuple[str, ...]
    test_confidence: float


def build_traceability(matches: list[Match], graph_source: dict | str | Path) -> list[TraceChain]:
    """Link each matched module to the test nodes that touch it, with per-link confidence."""
    data = graph_source if isinstance(graph_source, dict) else json.loads(
        Path(graph_source).read_text(encoding="utf-8"))
    node_type = {n["id"]: n.get("type") for n in data.get("nodes", [])}
    chains: list[TraceChain] = []
    for match in matches:
        tests: list[str] = []
        test_confidence = 1.0
        for edge in data.get("edges", []):
            endpoints = (edge.get("from"), edge.get("to"))
            if match.module in endpoints:
                other = endpoints[1] if endpoints[0] == match.module else endpoints[0]
                if node_type.get(other) == "test":
                    tests.append(other)
                    test_confidence = edge.get("confidence", 1.0)
        chains.append(TraceChain(
            match.req_id, match.module, match.confidence,
            tuple(sorted(set(tests))), test_confidence))
    return chains
