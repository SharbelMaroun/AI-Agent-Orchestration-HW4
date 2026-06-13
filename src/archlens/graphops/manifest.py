"""Run manifest persistence and re-run history linking (tasks 4.021, 4.038-4.039)."""

from pathlib import Path

from pydantic import BaseModel, ConfigDict

from archlens.graphops.layout import RunLayout
from archlens.graphops.stages import StageResult


class ArtifactRef(BaseModel):
    """A persisted artifact with its content checksum."""

    model_config = ConfigDict(extra="forbid")

    name: str
    path: str
    sha256: str


class Manifest(BaseModel):
    """Machine-readable record of one Graphify run, linked into a history chain."""

    model_config = ConfigDict(extra="forbid")

    run_id: str
    analysis_depth: str
    stages: list[StageResult] = []
    artifacts: list[ArtifactRef] = []
    history: list[str] = []


def extend_history(previous: list[str], run_id: str) -> list[str]:
    """Append the new run id to the prior history in execution order (task 4.039)."""
    return [*previous, run_id]


def save_manifest(layout: RunLayout, manifest: Manifest) -> Path:
    layout.create()
    layout.manifest.write_text(manifest.model_dump_json(indent=2), encoding="utf-8")
    return layout.manifest


def load_manifest(path: str | Path) -> Manifest:
    return Manifest.model_validate_json(Path(path).read_text(encoding="utf-8"))
