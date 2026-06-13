"""TDD tests for GraphifyConfig, analysis depth, and the token-budget guard (tasks 4.005-4.010)."""

import pytest
from pydantic import ValidationError

from archlens.graphops.config import GraphifyConfig, enforce_token_budget, load_graphify
from archlens.graphops.errors import TokenBudgetExceededError
from archlens.shared.config import load_setup

BASE = {
    "binary": "graphify",
    "stages": ["detect", "extract", "build", "cluster", "export"],
    "output_root": "runs/graphify",
    "timeout_s": 600,
    "analysis_depth": "structural",
    "token_budget": 100000,
}


def test_load_graphify_from_real_setup(setup_json):
    cfg = load_graphify(setup_json)
    assert isinstance(cfg, GraphifyConfig)
    assert cfg.binary
    assert tuple(cfg.stages) == ("detect", "extract", "build", "cluster", "export")


def test_setup_config_embeds_graphify(setup_json):
    cfg = load_setup(setup_json)
    assert cfg.graphify.analysis_depth in ("structural", "semantic", "full")


def test_unknown_key_rejected():
    with pytest.raises(ValidationError):
        GraphifyConfig.model_validate({**BASE, "surprise": 1})


def test_invalid_depth_rejected():
    with pytest.raises(ValidationError):
        GraphifyConfig.model_validate({**BASE, "analysis_depth": "deep"})


def test_non_canonical_stages_rejected():
    with pytest.raises(ValidationError):
        GraphifyConfig.model_validate({**BASE, "stages": ["detect", "build"]})


def test_structural_skips_semantic_and_semantic_enables_it():
    structural = GraphifyConfig.model_validate(BASE)
    semantic = GraphifyConfig.model_validate({**BASE, "analysis_depth": "semantic"})
    assert structural.semantic_enabled is False
    assert semantic.semantic_enabled is True


def test_token_budget_guard_aborts_semantic_over_budget():
    semantic = GraphifyConfig.model_validate(
        {**BASE, "analysis_depth": "semantic", "token_budget": 10}
    )
    with pytest.raises(TokenBudgetExceededError):
        enforce_token_budget(11, semantic)


def test_token_budget_guard_ignores_structural_runs():
    structural = GraphifyConfig.model_validate({**BASE, "token_budget": 10})
    enforce_token_budget(9999, structural)  # structural makes no LLM calls -> never raises
