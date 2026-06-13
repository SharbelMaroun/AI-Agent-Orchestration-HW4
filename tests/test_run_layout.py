"""TDD tests for run-id generation and the run-scoped artifact layout (tasks 4.018-4.020)."""

from pathlib import Path

from archlens.graphops.layout import RunLayout, new_run_id


def test_run_ids_unique_and_lexicographically_sorted():
    ids = [new_run_id() for _ in range(100)]
    assert len(set(ids)) == 100
    assert ids == sorted(ids)


def test_run_id_uses_injected_clock():
    assert new_run_id(now=1700000000.0).startswith("run-")


def test_layout_paths_under_run_dir(tmp_path: Path):
    layout = RunLayout(tmp_path, "run-xyz")
    assert layout.run_dir == tmp_path / "run-xyz"
    assert layout.graph_json.name == "graph.json"
    assert layout.graph_html.name == "graph.html"
    assert layout.report_md.name == "REPORT.md"
    assert layout.manifest.name == "manifest.json"


def test_layout_create_makes_directory(tmp_path: Path):
    layout = RunLayout(tmp_path, "run-1").create()
    assert layout.run_dir.is_dir()
