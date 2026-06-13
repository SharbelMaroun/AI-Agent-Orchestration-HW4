"""TDD tests for the community block-model builder (tasks 7.005-7.006)."""

from pathlib import Path

from archlens.graphops.block_model import InterBlockEdge, build_block_model

FIXTURES = Path(__file__).resolve().parents[1] / "fixtures" / "graphify"


def test_block_model_has_one_block_per_community():
    model = build_block_model(FIXTURES / "full.json")
    assert {block.name for block in model.blocks} == {"payments", "auth"}


def test_block_member_counts_match_communities():
    blocks = {b.name: b for b in build_block_model(FIXTURES / "full.json").blocks}
    assert blocks["payments"].member_count == 4
    assert blocks["auth"].member_count == 2


def test_inter_block_edge_weight_is_aggregated_and_directed():
    model = build_block_model(FIXTURES / "full.json")
    assert model.edges == (InterBlockEdge("payments", "auth", 1),)
