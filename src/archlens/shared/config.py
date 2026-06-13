"""setup.json schema models and loader with runtime config-version validation."""

import json
from pathlib import Path

from pydantic import BaseModel, ConfigDict, Field, field_validator

from archlens.graphops.config import GraphifyConfig
from archlens.shared.constants import (
    ALLOWED_URL_SCHEMES,
    CONFIDENCE_MAX,
    CONFIDENCE_MIN,
    DEFAULT_CLONE_DEPTH,
    DEFAULT_MAX_SIZE_MB,
    DEFAULT_TIMEOUT_S,
    DELIVERABLES_DIR,
    DUPLICATE_SIMILARITY_THRESHOLD,
    SETUP_FILE,
)
from archlens.shared.version import VERSION
from archlens.vault.config import VaultConfig


class ConfigVersionError(ValueError):
    """Raised when a config file's version key does not match the project version."""


class RepoBlock(BaseModel):
    """One repository entry (target_repo / fallback_repo) — 7 keys, unknown keys rejected."""

    model_config = ConfigDict(extra="forbid")

    url: str
    branch: str
    pinned_commit: str
    workdir_root: str
    clone_depth: int = DEFAULT_CLONE_DEPTH
    timeout_s: int = DEFAULT_TIMEOUT_S
    max_size_mb: int = DEFAULT_MAX_SIZE_MB

    @field_validator("url")
    @classmethod
    def _allowed_scheme_only(cls, value: str) -> str:
        if not value.startswith(tuple(f"{s}://" for s in ALLOWED_URL_SCHEMES)):
            raise ValueError(f"URL scheme must be one of {ALLOWED_URL_SCHEMES}: {value}")
        return value


class ValidationBlock(BaseModel):
    """Thresholds for target-repo validation checks."""

    model_config = ConfigDict(extra="forbid")

    python_min_share: float
    min_file_count: int
    max_file_count: int


class AnalysisBlock(BaseModel):
    """Confidence and duplicate thresholds for the Phase 6 graph-analysis engine."""

    model_config = ConfigDict(extra="forbid")

    confidence_floor: float = CONFIDENCE_MIN
    confidence_strong: float = CONFIDENCE_MAX
    duplicate_similarity_threshold: float = DUPLICATE_SIMILARITY_THRESHOLD


class DeliverablesBlock(BaseModel):
    """Phase 7 reverse-engineering deliverable settings (no value hardcoded in code).

    The duplicate-similarity threshold is intentionally NOT duplicated here; the deliverable
    flow detector reads the single source of truth at ``analysis.duplicate_similarity_threshold``.
    """

    model_config = ConfigDict(extra="forbid")

    output_dir: str = DELIVERABLES_DIR
    mermaid_direction: str = "TD"
    match_confidence_threshold: float = CONFIDENCE_MIN


class SetupConfig(BaseModel):
    """Typed view of config/setup.json; unknown keys are rejected."""

    model_config = ConfigDict(extra="forbid")

    version: str
    target_repo: RepoBlock
    fallback_repo: RepoBlock
    graphify_output_dir: str
    obsidian_vault_dir: str
    validation: ValidationBlock
    graphify: GraphifyConfig
    vault: VaultConfig
    analysis: AnalysisBlock = Field(default_factory=AnalysisBlock)
    deliverables: DeliverablesBlock = Field(default_factory=DeliverablesBlock)


def _read_json(path: Path) -> dict:
    if not path.is_file():
        raise FileNotFoundError(f"config file not found: {path}")
    return json.loads(path.read_text(encoding="utf-8"))


def check_config_version(found: str, source: Path) -> None:
    if found != VERSION:
        raise ConfigVersionError(f"{source}: version {found!r} does not match {VERSION!r}")


def load_setup(path: str | Path = SETUP_FILE) -> SetupConfig:
    source = Path(path)
    cfg = SetupConfig.model_validate(_read_json(source))
    check_config_version(cfg.version, source)
    return cfg
