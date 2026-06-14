"""Boundary tests for the four knowledge-quality scorers (tasks 14.032-14.035)."""

from archlens.metrics.knowledge_scorers import (
    correct_file_identification,
    correct_tool_timing,
    noise_reduction,
    source_traceability,
)


def test_source_traceability_boundaries():
    assert source_traceability(0, 10) == 0
    assert source_traceability(10, 10) == 10
    assert source_traceability(0, 0) == 0


def test_noise_reduction_boundaries():
    assert noise_reduction(100, 100) == 0      # no reduction
    assert noise_reduction(100, 0) == 10       # full reduction
    assert noise_reduction(0, 0) == 0


def test_correct_file_identification_boundaries():
    assert correct_file_identification({"a", "b"}, {"a", "b"}) == 10   # perfect match
    assert correct_file_identification({"x"}, {"a"}) == 0              # zero overlap
    assert correct_file_identification(set(), {"a"}) == 0


def test_correct_tool_timing_boundaries():
    assert correct_tool_timing(["a", "b", "c"], ["a", "b", "c"]) == 10   # exact sequence
    assert correct_tool_timing(["c", "a", "b"], ["a", "b", "c"]) == 0    # fully wrong order
    assert correct_tool_timing([], ["a"]) == 0
    assert correct_tool_timing(["a"], []) == 0                           # no expected sequence
