"""Evidence-level gate: admit only EXTRACTED/VALIDATED candidates with a full citation (11.010).

OBSERVED and INFERRED findings may enter the BugHunter queue but are blocked from execution
(PRD_improvement_loop §8); the allowed-level set is read from config, never hardcoded.
"""

from ..shared.constants import CONFIDENCE_MAX, CONFIDENCE_MIN
from .fix_policy import FixCandidate


class EvidenceGate:
    """Blocks OBSERVED/INFERRED fixes and any candidate missing its citation triple."""

    def __init__(self, allowed_levels):
        self._allowed = set(allowed_levels)

    @classmethod
    def from_config(cls, cfg) -> "EvidenceGate":
        """Build the gate from a SetupConfig (allowed levels via config, not hardcoded)."""
        return cls(cfg.improvement_loop.allowed_evidence_levels)

    def admits(self, candidate: FixCandidate) -> bool:
        """True when the candidate clears the level gate and cites relation/confidence/source."""
        return (
            candidate.level in self._allowed
            and bool(candidate.relation)
            and bool(candidate.source_file)
            and CONFIDENCE_MIN <= candidate.confidence <= CONFIDENCE_MAX
        )

    def filter(self, candidates) -> list[FixCandidate]:
        """Return only the admitted candidates, preserving input order."""
        return [c for c in candidates if self.admits(c)]
