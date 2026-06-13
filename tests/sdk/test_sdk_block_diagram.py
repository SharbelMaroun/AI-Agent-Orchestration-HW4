"""SDK-level test for block-diagram generation (task 7.010)."""

from pathlib import Path

from archlens.sdk.sdk import ArchLensSDK

FIXTURES = Path(__file__).resolve().parents[1] / "fixtures" / "graphify"


def test_sdk_generates_block_diagram_from_graph_json():
    rendered = ArchLensSDK().generate_block_diagram(FIXTURES / "full.json")
    assert rendered.startswith("```mermaid")
    assert "flowchart TD" in rendered
    assert "payments" in rendered and "auth" in rendered


def test_sdk_block_diagram_honors_explicit_direction():
    rendered = ArchLensSDK().generate_block_diagram(FIXTURES / "full.json", direction="LR")
    assert "flowchart LR" in rendered
