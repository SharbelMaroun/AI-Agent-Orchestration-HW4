"""GraphifyConfig — typed view of the setup.json 'graphify' block (tasks 4.005-4.010)."""

import json
from pathlib import Path

from pydantic import BaseModel, ConfigDict, field_validator

from archlens.graphops.errors import TokenBudgetExceededError
from archlens.shared.constants import ANALYSIS_DEPTHS, GRAPHIFY_STAGES, SETUP_FILE

_SEMANTIC_DEPTHS = ("semantic", "full")


class GraphifyConfig(BaseModel):
    """Graphify wrapper settings; unknown keys rejected, every value sourced from setup.json."""

    model_config = ConfigDict(extra="forbid")

    binary: str
    stages: list[str]
    output_root: str
    timeout_s: int
    analysis_depth: str
    token_budget: int

    @field_validator("analysis_depth")
    @classmethod
    def _known_depth(cls, value: str) -> str:
        if value not in ANALYSIS_DEPTHS:
            raise ValueError(f"analysis_depth must be one of {ANALYSIS_DEPTHS}: {value}")
        return value

    @field_validator("stages")
    @classmethod
    def _canonical_stages(cls, value: list[str]) -> list[str]:
        if tuple(value) != GRAPHIFY_STAGES:
            raise ValueError(f"stages must be exactly {GRAPHIFY_STAGES}: {value}")
        return value

    @property
    def semantic_enabled(self) -> bool:
        """structural depth is AST-only (zero LLM calls); semantic/full enable inference."""
        return self.analysis_depth in _SEMANTIC_DEPTHS


def load_graphify(path: str | Path = SETUP_FILE) -> GraphifyConfig:
    data = json.loads(Path(path).read_text(encoding="utf-8"))
    return GraphifyConfig.model_validate(data["graphify"])


def enforce_token_budget(spent: int, cfg: GraphifyConfig) -> None:
    """Raise before launching a semantic pass that would exceed the budget (task 4.010)."""
    if cfg.semantic_enabled and spent > cfg.token_budget:
        raise TokenBudgetExceededError(f"token spend {spent} exceeds budget {cfg.token_budget}")
