"""TDD tests for manifest persistence, history linking, and re-run isolation (4.021, 4.038-4.039)."""

from pathlib import Path

from archlens.graphops.layout import RunLayout
from archlens.graphops.manifest import Manifest, extend_history, load_manifest, save_manifest
from archlens.graphops.stages import PipelineStage, StageResult, StageStatus


def _manifest(run_id: str, history: list[str]) -> Manifest:
    stage = StageResult(stage=PipelineStage.EXPORT, status=StageStatus.OK)
    return Manifest(run_id=run_id, analysis_depth="structural", stages=[stage], history=history)


def test_save_and_load_round_trip(tmp_path: Path):
    layout = RunLayout(tmp_path, "run-1")
    save_manifest(layout, _manifest("run-1", ["run-1"]))
    loaded = load_manifest(layout.manifest)
    assert loaded.run_id == "run-1"
    assert loaded.stages[0].stage is PipelineStage.EXPORT


def test_extend_history_preserves_order():
    assert extend_history(["run-1"], "run-2") == ["run-1", "run-2"]


def test_rerun_uses_new_dir_and_leaves_first_run_untouched(tmp_path: Path):
    first = RunLayout(tmp_path, "run-1").create()
    first.graph_json.write_text('{"nodes": []}', encoding="utf-8")
    before = first.graph_json.read_text(encoding="utf-8")
    second = RunLayout(tmp_path, "run-2")
    save_manifest(second, _manifest("run-2", extend_history(["run-1"], "run-2")))
    assert first.graph_json.read_text(encoding="utf-8") == before
    assert load_manifest(second.manifest).history == ["run-1", "run-2"]
    assert first.run_dir != second.run_dir
