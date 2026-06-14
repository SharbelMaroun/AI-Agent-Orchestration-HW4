"""Token-savings calculator: savings_pct = (1 - assisted/baseline) * 100 (task 12.030)."""

from dataclasses import dataclass

from ..shared.constants import SAVINGS_TARGET_PCT


@dataclass(frozen=True)
class Savings:
    """Baseline vs assisted token comparison and whether the savings target was met."""

    baseline_tokens: int
    assisted_tokens: int
    savings_pct: float
    target_met: bool


def compute_savings(baseline_tokens: int, assisted_tokens: int,
                    target_pct: float = SAVINGS_TARGET_PCT) -> Savings:
    """Percentage of tokens the assisted protocol saves; a zero baseline is guarded to 0%."""
    if baseline_tokens <= 0:
        return Savings(baseline_tokens, assisted_tokens, 0.0, False)
    pct = (1 - assisted_tokens / baseline_tokens) * 100
    return Savings(baseline_tokens, assisted_tokens, pct, pct >= target_pct)
