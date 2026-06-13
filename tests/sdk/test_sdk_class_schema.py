"""SDK-level test for class-schema extraction on a multi-file fixture package (task 7.017)."""

from pathlib import Path

from archlens.sdk.sdk import ArchLensSDK

FIXTURE = Path(__file__).resolve().parents[1] / "fixtures" / "classes_pkg"


def test_sdk_extracts_class_model_and_diagram():
    schema = ArchLensSDK().extract_class_schema(FIXTURE)
    names = {c.name for c in schema["classes"]}
    assert {"Shape", "Circle", "Color", "Repository", "Service"} <= names
    assert schema["diagram"].startswith("```mermaid")
    assert "classDiagram" in schema["diagram"]
    assert "Shape <|-- Circle" in schema["diagram"]
    assert any(r.kind == "composition" for r in schema["relations"])
