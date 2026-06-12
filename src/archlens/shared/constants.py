"""Centralized named constants — the only sanctioned home for magic values."""

from pathlib import Path

CONFIG_DIR = Path("config")
SETUP_FILE = CONFIG_DIR / "setup.json"
RATE_LIMITS_FILE = CONFIG_DIR / "rate_limits.json"
LOGGING_CONFIG_FILE = CONFIG_DIR / "logging_config.json"

LINE_CAP = 150
MAX_LOOP_ITERATIONS = 5

LOGGER_NAME = "archlens"
