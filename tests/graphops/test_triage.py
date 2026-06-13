"""TDD tests for edge triage buckets and the confidence policy (tasks 6.031-6.034)."""

from fixtures import build_composite

from archlens.graphops.loader import load_graph
from archlens.graphops.triage import confidence_policy, triage_edges


def test_triage_buckets_match_composite_evidence_counts():
    graph = load_graph(build_composite())
    buckets = triage_edges(graph)
    assert len(buckets["EXTRACTED"]) == 5
    assert len(buckets["INFERRED"]) == 2
    assert len(buckets["AMBIGUOUS"]) == 1


def test_triage_items_carry_citations():
    graph = load_graph(build_composite())
    buckets = triage_edges(graph)
    item = buckets["AMBIGUOUS"][0]
    assert item.src == "c3"
    assert item.dst == "sink"
    assert item.citation.confidence == 0.6


def test_confidence_at_floor_is_needs_validation():
    assert confidence_policy(0.55) == "needs_validation"


def test_confidence_at_or_above_strong_is_strong():
    assert confidence_policy(0.95) == "strong"
    assert confidence_policy(0.99) == "strong"


def test_confidence_below_floor_routed_to_human_review():
    assert confidence_policy(0.50) == "human_review"
    assert confidence_policy(0.5499) == "human_review"
