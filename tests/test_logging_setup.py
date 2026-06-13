"""TDD test for the logging bootstrap (task 1.027)."""

import logging
from pathlib import Path

import pytest

from archlens.shared.logging_setup import setup_logging

PROJECT_ROOT = Path(__file__).resolve().parents[1]
LOGGING_CONFIG = PROJECT_ROOT / "config" / "logging_config.json"


def test_setup_logging_configures_archlens_logger(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
):
    monkeypatch.chdir(tmp_path)  # file handler must not write into the repo
    logger = setup_logging(LOGGING_CONFIG)
    assert logger.name == "archlens"
    assert logger.level == logging.INFO
    assert logger.handlers
    logger.info("bootstrap smoke message")
