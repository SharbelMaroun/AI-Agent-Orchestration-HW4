"""Logging bootstrap: apply dictConfig from config/logging_config.json."""

import json
import logging
import logging.config
from pathlib import Path

from archlens.shared.constants import LOGGER_NAME, LOGGING_CONFIG_FILE


def setup_logging(path: str | Path = LOGGING_CONFIG_FILE) -> logging.Logger:
    source = Path(path)
    if not source.is_file():
        raise FileNotFoundError(f"logging config not found: {source}")
    logging.config.dictConfig(json.loads(source.read_text(encoding="utf-8")))
    return logging.getLogger(LOGGER_NAME)
