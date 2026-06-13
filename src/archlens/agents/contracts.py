"""Pydantic handoff payload models for each agent transition (task 10.004)."""

from pydantic import BaseModel, ConfigDict


class _Payload(BaseModel):
    """Base handoff payload: unknown keys are rejected so contracts stay strict."""

    model_config = ConfigDict(extra="forbid")


class RepoManifest(_Payload):
    """RepoAgent -> supervisor: the cloned target repository."""

    local_path: str
    url: str
    commit: str
    env_ready: bool


class GraphSnapshotRef(_Payload):
    """GraphAgent -> supervisor: a reference to the latest Graphify outputs."""

    graph_json: str
    node_count: int
    edge_count: int
    report_md: str
    snapshot_id: int


class FindingBatch(_Payload):
    """Analyst/BugHunter -> supervisor: a batch of findings."""

    findings: list[dict]


class PatchPlan(_Payload):
    """RefactorAgent -> supervisor: a proposed change before any write."""

    target: str
    action: str
    rationale: str = ""


class QAReport(_Payload):
    """QAAgent -> supervisor: test/coverage/lint outcome."""

    tests_green: bool
    coverage_pct: float
    ruff_violations: int


class MetricsDelta(_Payload):
    """MetricsAgent -> supervisor: token accounting delta."""

    baseline_tokens: int
    assisted_tokens: int
    savings_pct: float
