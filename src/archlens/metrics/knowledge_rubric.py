"""4-metric knowledge-quality rubric model (task 14.031).

Metrics (Part B): source_traceability, noise_reduction, correct_file_identification,
correct_tool_timing. Each scores an integer 0-10 with a mandatory rationale; a rubric must score
exactly the four metrics.
"""

from dataclasses import dataclass

from ..shared.constants import RUBRIC_MAX_SCORE, RUBRIC_METRICS, RUBRIC_MIN_SCORE


@dataclass(frozen=True)
class MetricScore:
    """One metric's integer 0-10 score plus a mandatory rationale."""

    metric: str
    score: int
    rationale: str

    def __post_init__(self) -> None:
        if self.metric not in RUBRIC_METRICS:
            raise ValueError(f"unknown metric: {self.metric}")
        if not (RUBRIC_MIN_SCORE <= self.score <= RUBRIC_MAX_SCORE):
            raise ValueError(f"score out of range [0,10]: {self.score}")
        if not self.rationale.strip():
            raise ValueError("rationale is required")


@dataclass(frozen=True)
class RubricScore:
    """A complete rubric covering exactly the four knowledge-quality metrics."""

    scores: tuple[MetricScore, ...]

    def __post_init__(self) -> None:
        metrics = sorted(score.metric for score in self.scores)
        if metrics != sorted(RUBRIC_METRICS):
            raise ValueError("rubric must score exactly the 4 metrics")

    def total(self) -> int:
        """Sum of the four metric scores (0-40)."""
        return sum(score.score for score in self.scores)

    def as_dict(self) -> dict[str, int]:
        """Map of metric name -> score."""
        return {score.metric: score.score for score in self.scores}
