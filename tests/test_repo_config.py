"""TDD tests for the RepoBlock schema and SDK repo-config accessor (task 3.012)."""

import pytest
from pydantic import ValidationError

from archlens.sdk.repo_config import select_repo
from archlens.shared.config import RepoBlock, load_setup
from archlens.shared.constants import (
    DEFAULT_CLONE_DEPTH,
    DEFAULT_MAX_SIZE_MB,
    DEFAULT_TIMEOUT_S,
)

BASE = {
    "url": "https://github.com/org/repo",
    "branch": "main",
    "pinned_commit": "HEAD",
    "workdir_root": "runs",
}


def test_missing_required_keys_rejected():
    with pytest.raises(ValidationError):
        RepoBlock.model_validate({"url": BASE["url"], "branch": "main"})


def test_http_scheme_rejected():
    with pytest.raises(ValidationError):
        RepoBlock.model_validate({**BASE, "url": "http://github.com/org/repo"})


def test_ssh_scheme_rejected():
    with pytest.raises(ValidationError):
        RepoBlock.model_validate({**BASE, "url": "git@github.com:org/repo.git"})


def test_defaults_applied_for_optional_keys():
    repo = RepoBlock.model_validate(BASE)
    assert repo.clone_depth == DEFAULT_CLONE_DEPTH
    assert repo.timeout_s == DEFAULT_TIMEOUT_S
    assert repo.max_size_mb == DEFAULT_MAX_SIZE_MB


def test_unknown_key_rejected():
    with pytest.raises(ValidationError):
        RepoBlock.model_validate({**BASE, "surprise": 1})


def test_select_repo_primary_and_fallback(setup_json):
    cfg = load_setup(setup_json)
    assert select_repo(cfg) is cfg.target_repo
    assert select_repo(cfg, use_fallback=True) is cfg.fallback_repo
    assert cfg.target_repo.url != cfg.fallback_repo.url
