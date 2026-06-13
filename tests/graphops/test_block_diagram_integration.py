"""End-to-end block-diagram pipeline test on a fixture graph.json (task 7.009)."""

from pathlib import Path

from archlens.graphops.block_model import build_block_model
from archlens.graphops.communities import load_communities
from archlens.graphops.mermaid_blocks import render_block_diagram

FIXTURES = Path(__file__).resolve().parents[1] / "fixtures" / "graphify"


def test_every_community_appears_exactly_once_as_a_mermaid_node():
    graph = FIXTURES / "full.json"
    rendered = render_block_diagram(build_block_model(graph))
    for community in load_communities(graph):
        assert rendered.count(f'["{community.label} (') == 1


def test_pipeline_emits_a_fenced_diagram_with_an_edge():
    rendered = render_block_diagram(build_block_model(FIXTURES / "full.json"))
    assert rendered.startswith("```mermaid")
    assert "-->" in rendered
