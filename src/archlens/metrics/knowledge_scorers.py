"""The four knowledge-quality scorers, each mapping evidence to a 0-10 integer (14.032-14.035)."""

from collections.abc import Sequence

from ..shared.constants import RUBRIC_MAX_SCORE


def _scale(ratio: float) -> int:
    return round(max(0.0, min(1.0, ratio)) * RUBRIC_MAX_SCORE)


def source_traceability(cited_claims: int, total_claims: int) -> int:
    """0-10 from the fraction of claims carrying a relation->confidence->source_file citation."""
    if total_claims <= 0:
        return 0
    return _scale(cited_claims / total_claims)


def noise_reduction(tokens_before: int, tokens_after: int) -> int:
    """0-10 from the fraction of irrelevant context tokens removed by using the wiki."""
    if tokens_before <= 0:
        return 0
    return _scale((tokens_before - tokens_after) / tokens_before)


def correct_file_identification(opened: set, relevant: set) -> int:
    """0-10 from the F1 of opened files versus the ground-truth relevant files."""
    if not opened or not relevant:
        return 0
    true_positives = len(opened & relevant)
    if true_positives == 0:
        return 0
    precision = true_positives / len(opened)
    recall = true_positives / len(relevant)
    return _scale(2 * precision * recall / (precision + recall))


def correct_tool_timing(invoked: Sequence, expected: Sequence) -> int:
    """0-10 from the fraction of tool-sequence positions matching the expected order."""
    if not expected:
        return 0
    matches = sum(1 for actual, want in zip(invoked, expected, strict=False) if actual == want)
    return _scale(matches / len(expected))
