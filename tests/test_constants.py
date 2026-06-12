"""TDD tests for shared/constants.py (task 1.016)."""

from pathlib import Path

from archlens.shared import constants


def test_config_paths_are_path_objects():
    assert isinstance(constants.CONFIG_DIR, Path)
    assert constants.SETUP_FILE == constants.CONFIG_DIR / "setup.json"
    assert constants.RATE_LIMITS_FILE == constants.CONFIG_DIR / "rate_limits.json"
    assert constants.LOGGING_CONFIG_FILE == constants.CONFIG_DIR / "logging_config.json"


def test_line_cap_is_150():
    assert constants.LINE_CAP == 150


def test_max_loop_iterations_is_5():
    assert constants.MAX_LOOP_ITERATIONS == 5
