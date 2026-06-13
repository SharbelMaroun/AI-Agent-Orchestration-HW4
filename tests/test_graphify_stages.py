"""TDD tests for the PipelineStage ordering and StageResult model (tasks 4.014-4.016)."""

from archlens.graphops.stages import StageResult, StageStatus, ordered_stages, stage_index


def test_canonical_stage_order():
    assert [s.value for s in ordered_stages()] == [
        "detect",
        "extract",
        "build",
        "cluster",
        "export",
    ]


def test_stage_index_is_monotonic():
    order = ordered_stages()
    assert [stage_index(s) for s in order] == [0, 1, 2, 3, 4]


def test_stage_result_serializes_to_json():
    result = StageResult(stage="update", status=StageStatus.OK)
    assert result.model_dump(mode="json") == {"stage": "update", "status": "ok", "message": ""}
