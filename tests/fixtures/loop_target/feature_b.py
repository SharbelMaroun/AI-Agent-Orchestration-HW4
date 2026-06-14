"""Feature B — depends on core; planted duplicate of feature_a.compute_total (similarity ~1.0)."""

from core import serve


def compute_total(items):
    total = 0
    for item in items:
        total = total + item * 2
    return total


def run(items):
    return serve(compute_total(items))
