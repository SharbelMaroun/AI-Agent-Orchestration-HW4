"""TDD tests for the ARCHITECTURE.md generator (tasks 7.036-7.037)."""

from pathlib import Path

from archlens.vault.arch_doc import render_architecture, write_architecture

FULL = Path(__file__).resolve().parents[1] / "fixtures" / "graphify" / "full.json"


def test_has_version_header():
    assert "Version: 1.00" in render_architecture(FULL, "1.00")


def test_embeds_a_fenced_mermaid_flowchart():
    text = render_architecture(FULL, "1.00")
    assert "```mermaid" in text
    assert "flowchart" in text


def test_has_community_table_and_evidence_tagged_narrative():
    text = render_architecture(FULL, "1.00")
    assert "| Community | Members |" in text
    assert "[EXTRACTED]" in text


def test_write_produces_architecture_file(tmp_path):
    path = write_architecture(FULL, tmp_path, "1.00")
    assert path.name == "ARCHITECTURE.md"
    assert "```mermaid" in path.read_text(encoding="utf-8")
