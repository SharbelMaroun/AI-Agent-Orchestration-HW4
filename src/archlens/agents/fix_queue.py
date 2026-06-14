"""Fix-candidate queue builder: evidence-gate then priority-sort (task 11.012)."""

from .evidence_gate import EvidenceGate
from .fix_policy import FixCandidate, FixPriorityPolicy


class FixQueueBuilder:
    """Combines the evidence gate and priority policy into one ordered fix queue."""

    def __init__(self, policy: FixPriorityPolicy, gate: EvidenceGate):
        self._policy = policy
        self._gate = gate

    @classmethod
    def from_config(cls, cfg) -> "FixQueueBuilder":
        """Build the queue builder from a SetupConfig."""
        return cls(FixPriorityPolicy.from_config(cfg), EvidenceGate.from_config(cfg))

    def build(self, candidates) -> list[FixCandidate]:
        """Return evidence-admitted candidates sorted P1 through P5 (ties by confidence desc)."""
        return self._policy.order(self._gate.filter(candidates))
