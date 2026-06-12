"""Shared fixtures: temp copies of config files and environment stubs."""

import shutil
from pathlib import Path

import pytest

PROJECT_ROOT = Path(__file__).resolve().parents[1]
CONFIG_DIR = PROJECT_ROOT / "config"


@pytest.fixture()
def config_copy(tmp_path: Path) -> Path:
    """Mutable copy of the real config/ directory."""
    dest = tmp_path / "config"
    shutil.copytree(CONFIG_DIR, dest)
    return dest


@pytest.fixture()
def setup_json(config_copy: Path) -> Path:
    return config_copy / "setup.json"


@pytest.fixture()
def rate_limits_json(config_copy: Path) -> Path:
    return config_copy / "rate_limits.json"


@pytest.fixture()
def env_stub(monkeypatch: pytest.MonkeyPatch) -> None:
    """Dummy secrets so no test ever needs a real credential."""
    monkeypatch.setenv("ANTHROPIC_API_KEY", "sk-ant-dummy")
    monkeypatch.setenv("GITHUB_TOKEN", "ghp-dummy")
