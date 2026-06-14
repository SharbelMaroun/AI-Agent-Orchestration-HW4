"""TDD tests for the gatekeeper RateLimitConfig loader (tasks 9.008, 9.010)."""

import json

import pytest
from pydantic import ValidationError

from archlens.gatekeeper.rate_config import load_rate_config, service_limits
from archlens.shared.config import ConfigVersionError


def test_loads_default_config_values():
    limits = service_limits(load_rate_config())
    assert limits.requests_per_minute == 30
    assert limits.requests_per_hour == 500
    assert limits.concurrent_max == 5


def test_missing_file_raises(tmp_path):
    with pytest.raises(FileNotFoundError):
        load_rate_config(tmp_path / "absent.json")


def test_malformed_json_raises(tmp_path):
    bad = tmp_path / "rate_limits.json"
    bad.write_text("{ not json", encoding="utf-8")
    with pytest.raises(json.JSONDecodeError):
        load_rate_config(bad)


def test_missing_required_key_raises(tmp_path):
    incomplete = {"version": "1.00", "rate_limits": {"services": {"default": {
        "requests_per_minute": 30}}}, "queue": {"max_depth": 100, "backpressure_warn_ratio": 0.8}}
    path = tmp_path / "rate_limits.json"
    path.write_text(json.dumps(incomplete), encoding="utf-8")
    with pytest.raises(ValidationError):
        load_rate_config(path)


def test_config_version_mismatch_raises(rate_config_factory):
    with pytest.raises(ConfigVersionError):
        load_rate_config(rate_config_factory(version="0.99"))
