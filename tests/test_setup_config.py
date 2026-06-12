"""TDD tests for the SetupConfig model and load_setup() (tasks 1.019, 1.021, 3.010, 3.011)."""

import json
from pathlib import Path

import pytest
from pydantic import ValidationError

from archlens.shared.config import ConfigVersionError, SetupConfig, load_setup

REPO_KEYS = {"url", "branch", "pinned_commit", "workdir_root", "clone_depth", "timeout_s", "max_size_mb"}


def test_load_success_returns_typed_model(setup_json: Path):
    cfg = load_setup(setup_json)
    assert isinstance(cfg, SetupConfig)
    assert cfg.version == "1.00"
    assert cfg.target_repo.url.startswith("https://")
    assert cfg.fallback_repo.url.startswith("https://")
    assert cfg.graphify_output_dir and cfg.obsidian_vault_dir
    assert 0 < cfg.validation.python_min_share < 1


def test_target_and_fallback_blocks_carry_identical_key_sets(setup_json: Path):
    data = json.loads(setup_json.read_text(encoding="utf-8"))
    assert set(data["target_repo"]) == REPO_KEYS
    assert set(data["fallback_repo"]) == REPO_KEYS


def test_missing_file_raises(tmp_path: Path):
    with pytest.raises(FileNotFoundError):
        load_setup(tmp_path / "does_not_exist.json")


def test_unknown_key_rejected(setup_json: Path):
    data = json.loads(setup_json.read_text(encoding="utf-8"))
    data["surprise_key"] = "nope"
    setup_json.write_text(json.dumps(data), encoding="utf-8")
    with pytest.raises(ValidationError):
        load_setup(setup_json)


def test_version_mismatch_raises_config_version_error(setup_json: Path):
    data = json.loads(setup_json.read_text(encoding="utf-8"))
    data["version"] = "0.99"
    setup_json.write_text(json.dumps(data), encoding="utf-8")
    with pytest.raises(ConfigVersionError):
        load_setup(setup_json)
