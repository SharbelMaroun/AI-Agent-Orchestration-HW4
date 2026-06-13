"""TDD tests for the graph.html artifact handler (tasks 4.034-4.035)."""

from pathlib import Path

from archlens.graphops.artifacts import register_graph_html, sha256_file
from archlens.graphops.layout import RunLayout

FIXTURES = Path(__file__).resolve().parent / "fixtures" / "graphify"


def test_register_copies_and_checksums_graph_html(tmp_path: Path):
    layout = RunLayout(tmp_path, "run-1")
    ref = register_graph_html(layout, FIXTURES / "graph.html")
    assert layout.graph_html.is_file()
    assert ref.name == "graph.html"
    assert ref.sha256 == sha256_file(FIXTURES / "graph.html")
    assert len(ref.sha256) == 64
