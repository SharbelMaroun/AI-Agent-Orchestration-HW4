"""TDD tests for ArchLensSDK.validate_config (tasks 8.028-8.029)."""

import pytest

from archlens.sdk.sdk import ArchLensSDK
from archlens.shared.exceptions import ConfigError


def test_valid_config_passes():
    assert ArchLensSDK().validate_config() is True


def test_missing_setup_keys_raises_naming_the_file(tmp_path):
    bad = tmp_path / "setup.json"
    bad.write_text('{"version": "1.00"}', encoding="utf-8")
    with pytest.raises(ConfigError) as exc:
        ArchLensSDK().validate_config(setup_path=str(bad))
    assert "setup.json" in (exc.value.source_context or "")


def test_bad_rate_limits_raises_naming_the_file(tmp_path):
    bad = tmp_path / "rl.json"
    bad.write_text('{"version": "1.00"}', encoding="utf-8")
    with pytest.raises(ConfigError) as exc:
        ArchLensSDK().validate_config(rate_limits_path=str(bad))
    assert "rate_limits" in (exc.value.source_context or "")


def test_absent_env_example_raises(tmp_path):
    with pytest.raises(ConfigError) as exc:
        ArchLensSDK().validate_config(env_example=str(tmp_path / "nope"))
    assert ".env-example" in (exc.value.source_context or "")
