"""Fix-priority policy: map fix kinds to P1-P5 and order candidates (task 11.008).

The priority *order* is read from config (``improvement_loop.priority_order``), never hardcoded;
the kind->priority mapping is the fixed taxonomy of ADR-010 / PRD_improvement_loop §4.
"""

from pydantic import BaseModel, ConfigDict, field_validator

from ..shared.constants import FixPriority
from ..shared.validators import bounded_confidence

KIND_TO_PRIORITY: dict[str, FixPriority] = {
    "spof": FixPriority.P1,
    "bottleneck": FixPriority.P2,
    "oversized": FixPriority.P3,
    "duplicate": FixPriority.P4,
    "misalignment": FixPriority.P5,
}


class FixCandidate(BaseModel):
    """A proposed fix with its kind and evidence citation (relation, confidence, source_file)."""

    model_config = ConfigDict(extra="forbid")

    fix_id: str
    kind: str
    level: str
    relation: str
    confidence: float
    source_file: str
    node_id: str = ""

    @field_validator("kind")
    @classmethod
    def _known_kind(cls, value: str) -> str:
        if value not in KIND_TO_PRIORITY:
            raise ValueError(f"unknown fix kind {value!r}; expected {tuple(KIND_TO_PRIORITY)}")
        return value

    @field_validator("confidence")
    @classmethod
    def _bounded_confidence(cls, value: float) -> float:
        return bounded_confidence(value)


class FixPriorityPolicy:
    """Assigns P1-P5 to candidates and orders them by the configured priority sequence."""

    def __init__(self, priority_order: list[str]):
        self._order = list(priority_order)

    @classmethod
    def from_config(cls, cfg) -> "FixPriorityPolicy":
        """Build the policy from a SetupConfig (priority order via config, not hardcoded)."""
        return cls(cfg.improvement_loop.priority_order)

    def priority_of(self, candidate: FixCandidate) -> FixPriority:
        """Return the P1-P5 class for a candidate's fix kind."""
        return KIND_TO_PRIORITY[candidate.kind]

    def rank(self, candidate: FixCandidate) -> tuple[int, float]:
        """Sort key: configured priority index, then highest confidence first."""
        return self._order.index(self.priority_of(candidate).value), -candidate.confidence

    def order(self, candidates) -> list[FixCandidate]:
        """Return candidates sorted P1 through P5, ties broken by confidence descending."""
        return sorted(candidates, key=self.rank)
