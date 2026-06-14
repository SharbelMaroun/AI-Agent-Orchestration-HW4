"""TDD tests for the naive baseline context builder (task 12.017)."""

from pathlib import Path

from archlens.metrics.baseline_context import (
    build_baseline_context,
    collect_python_sources,
    estimate_tokens,
)

FIXTURE = Path(__file__).resolve().parent / "fixtures" / "mini_repo"


def test_collects_all_python_sources_sorted():
    sources = collect_python_sources(FIXTURE)
    assert len(sources) >= 2
    assert all(p.suffix == ".py" for p in sources)
    assert sources == sorted(sources)


def test_context_concatenates_every_module():
    context = build_baseline_context(FIXTURE)
    for path in collect_python_sources(FIXTURE):
        assert path.read_text(encoding="utf-8") in context


def test_estimate_tokens_scales_with_length():
    assert estimate_tokens("") == 0
    assert estimate_tokens("x" * 400) == 100


def test_context_build_is_deterministic():
    assert build_baseline_context(FIXTURE) == build_baseline_context(FIXTURE)
