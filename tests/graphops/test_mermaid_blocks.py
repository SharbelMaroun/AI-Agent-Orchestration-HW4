"""TDD tests for the mermaid block-diagram (flowchart) renderer (tasks 7.007-7.008)."""

from pathlib import Path

from archlens.graphops.block_model import build_block_model
from archlens.graphops.mermaid_blocks import render_block_diagram

FIXTURES = Path(__file__).resolve().parents[1] / "fixtures" / "graphify"


def _render(direction: str = "TD") -> str:
    return render_block_diagram(build_block_model(FIXTURES / "full.json"), direction=direction)


def test_render_is_a_fenced_mermaid_flowchart():
    out = _render()
    assert out.startswith("```mermaid")
    assert out.rstrip().endswith("```")
    assert "flowchart TD" in out


def test_one_node_per_block_with_member_counts():
    out = _render()
    assert "payments" in out and "auth" in out
    assert "(4)" in out and "(2)" in out


def test_one_edge_per_inter_block_dependency():
    assert _render().count("-->") == 1


def test_configured_direction_is_honored():
    assert "flowchart LR" in _render(direction="LR")
