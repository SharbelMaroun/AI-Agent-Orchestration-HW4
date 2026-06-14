"""Graph-build amortization — charge the one-time Graphify cost against per-query savings (12.032).

The assisted protocol pays a one-time Graphify build cost; break_even_queries is how many queries
must run before the per-query token savings repay that build. Non-positive savings never break even.
"""

import math
from dataclasses import dataclass


@dataclass(frozen=True)
class Amortization:
    """One-time graph-build token cost amortized over per-query token savings."""

    graph_build_tokens: int
    per_query_savings: int
    break_even_queries: int | None


def compute_amortization(graph_build_tokens: int, per_query_savings: int) -> Amortization:
    """break_even_queries = ceil(build / per-query savings); None when savings are non-positive."""
    if per_query_savings <= 0:
        return Amortization(graph_build_tokens, per_query_savings, None)
    return Amortization(graph_build_tokens, per_query_savings,
                        math.ceil(graph_build_tokens / per_query_savings))
