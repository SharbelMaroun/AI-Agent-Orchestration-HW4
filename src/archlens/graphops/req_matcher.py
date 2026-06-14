"""Match requirements to graph modules via symbol/keyword evidence (task 7.021)."""

import json
import re
from dataclasses import dataclass
from pathlib import Path

from ..graphops.req_parser import Requirement
from ..shared.config import load_setup

_STOP = {
    "the", "and", "for", "with", "that", "this", "from", "into", "every",
    "system", "shall", "process", "subsystem", "report", "route", "through",
}


@dataclass(frozen=True)
class Match:
    """A requirement linked to a module with a bounded confidence (0.55-0.95)."""

    req_id: str
    module: str
    confidence: float


def keywords(title: str) -> set[str]:
    return {w for w in re.findall(r"[a-z]+", title.lower()) if len(w) >= 4 and w not in _STOP}


def _modules(graph_source: dict | str | Path) -> dict[str, str]:
    data = graph_source if isinstance(graph_source, dict) else json.loads(
        Path(graph_source).read_text(encoding="utf-8"))
    return {n["id"]: f"{n['id']} {n.get('source_file', '')}".lower() for n in data.get("nodes", [])}


def match_requirements(
    requirements: list[Requirement], graph_source: dict | str | Path, threshold: float | None = None
) -> list[Match]:
    """Emit (req_id, module, confidence) matches whose keyword confidence meets the threshold."""
    if threshold is None:
        threshold = load_setup().deliverables.match_confidence_threshold
    modules = _modules(graph_source)
    matches: list[Match] = []
    for req in requirements:
        words = keywords(req.title)
        for module, text in modules.items():
            hits = sum(1 for word in words if word in text)
            confidence = round(min(0.95, 0.55 + 0.1 * hits), 2)
            if hits and confidence >= threshold:
                matches.append(Match(req.id, module, confidence))
    return matches
