"""Feature A — depends on core; its compute_total is duplicated verbatim in feature_b."""

from core import serve


def compute_total(items):
    total = 0
    for item in items:
        total = total + item * 2
    return total


def run(items):
    return serve(compute_total(items))
