"""Immutable analysis-result DTOs for the graph engine (task 6.007).

Every finding is traceable: the ``Citation`` value object carries the (relation, confidence,
source_file) evidence triple, and each result DTO is a frozen dataclass so analysis output can
never be mutated after it is produced.
"""

from dataclasses import dataclass


@dataclass(frozen=True)
class Citation:
    """The evidence triple behind a single finding."""

    relation: str
    confidence: float
    source_file: str


@dataclass(frozen=True)
class CentralityRow:
    """Degree and betweenness scores for one node, traceable to its source file."""

    node_id: str
    degree_in: int
    degree_out: int
    degree_total: int
    betweenness: float
    source_file: str


@dataclass(frozen=True)
class HubBottleneckVerdict:
    """HUB vs BOTTLENECK call for a node, with the rationale behind it."""

    node_id: str
    verdict: str
    degree_total: int
    betweenness: float
    bypass_count: int
    rationale: str
    source_file: str


@dataclass(frozen=True)
class BridgeReport:
    """Structural bridges and community connectors kept in separate sections."""

    structural: tuple[Citation, ...] = ()
    connector: tuple[Citation, ...] = ()


@dataclass(frozen=True)
class SpofFinding:
    """A single point of failure plus the per-hop citation chain it breaks."""

    node_id: str
    broken_paths: int
    citations: tuple[Citation, ...]


@dataclass(frozen=True)
class TriageItem:
    """One edge bucketed as EXTRACTED, INFERRED, or AMBIGUOUS."""

    src: str
    dst: str
    bucket: str
    citation: Citation


@dataclass(frozen=True)
class DuplicatePair:
    """Two nodes flagged as near-duplicates with their similarity score."""

    node_a: str
    node_b: str
    similarity: float
    citation: Citation


@dataclass(frozen=True)
class ReviewItem:
    """An edge routed to the human-review queue with the reason it was flagged."""

    src: str
    dst: str
    reason: str
    citation: Citation


@dataclass(frozen=True)
class FolderMismatch:
    """A node whose density community disagrees with its source-folder grouping."""

    node_id: str
    community_id: int
    folder: str
    dominant_folder: str
