"""Tests for the SDK KnowledgeMixin entry points (lifts sdk package coverage >= 95%)."""

from pathlib import Path

from archlens.sdk.sdk import ArchLensSDK

SKILLS = Path(__file__).resolve().parents[1] / "skills"


def test_sdk_validate_skill_and_guardrail():
    sdk = ArchLensSDK()
    assert sdk.validate_skill(SKILLS / "SKILL_graph_reading.md") == []
    assert sdk.skill_guardrail(SKILLS / "SKILL_graph_reading.md") == "auto"
    assert sdk.skill_guardrail(SKILLS / "SKILL_refactor.md") == "human_only"


def test_sdk_route_skill_uses_configured_skills_dir():
    assert ArchLensSDK().route_skill("which module imports auth?") == "graph-reading"
    assert ArchLensSDK().route_skill("tell me a joke") is None


def test_sdk_run_knowledge_eval():
    result = ArchLensSDK().run_knowledge_eval(assisted=True)
    assert result["mode"] == "assisted"
    assert len(result["tasks"]) == 10
