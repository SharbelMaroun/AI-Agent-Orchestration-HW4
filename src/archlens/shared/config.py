"""setup.json schema model and loader with runtime config-version validation."""

import json
from pathlib import Path

from pydantic import BaseModel, ConfigDict

from archlens.shared.constants import SETUP_FILE
from archlens.shared.version import VERSION


class ConfigVersionError(ValueError):
    """Raised when a config file's version key does not match the project version."""


class SetupConfig(BaseModel):
    """Typed view of config/setup.json; unknown keys are rejected."""

    model_config = ConfigDict(extra="forbid")

    version: str
    target_repo_url: str
    target_repo_branch: str
    fallback_repo_url: str
    clone_dir: str
    graphify_output_dir: str
    obsidian_vault_dir: str


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
