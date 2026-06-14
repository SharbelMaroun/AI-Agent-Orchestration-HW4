"""Shared field validators reused across pydantic models (DRY, task 8.036)."""

from .constants import CONFIDENCE_MAX, CONFIDENCE_MIN


def bounded_confidence(value: float) -> float:
    """Return value if within the evidence-ladder confidence band, else raise ValueError."""
    if not CONFIDENCE_MIN <= value <= CONFIDENCE_MAX:
        raise ValueError(f"confidence {value} outside [{CONFIDENCE_MIN}, {CONFIDENCE_MAX}]")
    return value
