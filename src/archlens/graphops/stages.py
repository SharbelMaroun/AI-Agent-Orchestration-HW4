"""Pipeline stage ordering and per-stage result records (tasks 4.014-4.017)."""

from enum import Enum

from pydantic import BaseModel, ConfigDict

from archlens.shared.constants import GRAPHIFY_STAGES


class PipelineStage(str, Enum):
    """The five ordered Graphify stages (PRD_graph_pipeline §3.1)."""

    DETECT = "detect"
    EXTRACT = "extract"
    BUILD = "build"
    CLUSTER = "cluster"
    EXPORT = "export"


class StageStatus(str, Enum):
    """Per-stage execution outcome recorded in the run manifest."""

    OK = "ok"
    FAILED = "failed"
    SKIPPED = "skipped"


class StageResult(BaseModel):
    """Outcome of one stage; serialized into manifest.json."""

    model_config = ConfigDict(extra="forbid")

    stage: PipelineStage
    status: StageStatus
    message: str = ""


def ordered_stages() -> list[PipelineStage]:
    """Return the canonical detect->extract->build->cluster->export order."""
    return [PipelineStage(name) for name in GRAPHIFY_STAGES]


def stage_index(stage: PipelineStage) -> int:
    return ordered_stages().index(stage)
