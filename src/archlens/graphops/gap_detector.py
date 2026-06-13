"""List requirements that no module implements above the match threshold (task 7.023)."""

from dataclasses import dataclass

from archlens.graphops.req_matcher import Match, keywords
from archlens.graphops.req_parser import Requirement


@dataclass(frozen=True)
class Gap:
    """An unimplemented requirement plus the keyword evidence that was searched for."""

    req_id: str
    title: str
    searched: tuple[str, ...]


def detect_gaps(requirements: list[Requirement], matches: list[Match]) -> list[Gap]:
    """Return requirements with zero matched modules, each carrying its searched keywords."""
    matched = {m.req_id for m in matches}
    return [
        Gap(req.id, req.title, tuple(sorted(keywords(req.title))))
        for req in requirements
        if req.id not in matched
    ]
