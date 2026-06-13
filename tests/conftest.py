"""Shared fixtures: temp config copies, environment stubs, git fixture factory."""

import shutil
import subprocess
from pathlib import Path

import pytest

PROJECT_ROOT = Path(__file__).resolve().parents[1]
CONFIG_DIR = PROJECT_ROOT / "config"
FIXTURES = Path(__file__).resolve().parent / "fixtures"

collect_ignore_glob = ["fixtures/*"]


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


@pytest.fixture()
def git_repo_factory(tmp_path: Path):
    """Materialize a fixture directory as a real local git repository (task 3.020)."""

    def _make(source: Path, name: str = "repo") -> Path:
        dest = tmp_path / name
        shutil.copytree(source, dest)
        ident = ["-c", "user.email=fixtures@archlens.local", "-c", "user.name=Fixtures"]
        for args in (["init", "-q"], ["add", "-A"], [*ident, "commit", "-q", "-m", "fixture"]):
            subprocess.run(["git", "-C", str(dest), *args], check=True, capture_output=True)
        return dest

    return _make


@pytest.fixture()
def oversize_repo(tmp_path: Path) -> Path:
    """mini_repo clone with 60 extra generated modules — exceeds max_file_count (task 3.021)."""
    dest = tmp_path / "oversize"
    shutil.copytree(FIXTURES / "mini_repo", dest)
    for i in range(60):
        (dest / f"gen_{i}.py").write_text(f"VALUE_{i} = {i}\n", encoding="utf-8")
    return dest
