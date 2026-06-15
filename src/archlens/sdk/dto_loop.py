"""Frozen improvement-loop SDK DTOs: findings, plans, results, token report (task 8.011)."""

from dataclasses import dataclass


@dataclass(frozen=True)
class BugFinding:
    """An architectural bug (e.g. SPOF, bottleneck) with its evidence."""

    node_id: str
    kind: str
    severity: str
    rationale: str
    source_file: str


@dataclass(frozen=True)
class RefactorPlan:
    """A single proposed change to address a finding."""

    target: str
    action: str
    rationale: str


@dataclass(frozen=True)
class LoopResult:
    """The outcome of an improvement-loop run."""

    iterations: int
    stop_reason: str
    metric_diffs: tuple[str, ...]
    tokens_used: int = 0  # real LLM tokens the agents consumed this run (gatekeeper-recorded)


@dataclass(frozen=True)
class TokenReport:
    """Baseline vs Graphify-assisted token accounting."""

    baseline_tokens: int
    assisted_tokens: int
    savings_pct: float
    explanation_required: bool
