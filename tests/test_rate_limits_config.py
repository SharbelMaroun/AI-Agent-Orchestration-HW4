"""TDD tests for the RateLimitsConfig model (task 1.024) — PRD_api_gatekeeper §3.1 schema."""

import json
from pathlib import Path

import pytest
from pydantic import ValidationError

from archlens.shared.config import ConfigVersionError
from archlens.shared.rate_limits import RateLimitsConfig, load_rate_limits


def test_nested_schema_loads_with_exact_defaults(rate_limits_json: Path):
    cfg = load_rate_limits(rate_limits_json)
    assert isinstance(cfg, RateLimitsConfig)
    assert cfg.version == "1.00"
    default = cfg.rate_limits.services.default
    assert default.requests_per_minute == 30
    assert default.requests_per_hour == 500
    assert default.concurrent_max == 5
    assert default.retry_after_seconds == 30
    assert default.max_retries == 3
    assert cfg.queue.max_depth > 0
    assert 0 < cfg.queue.backpressure_warn_ratio < 1


def test_missing_file_raises(tmp_path: Path):
    with pytest.raises(FileNotFoundError):
        load_rate_limits(tmp_path / "missing.json")


def test_unknown_key_rejected(rate_limits_json: Path):
    data = json.loads(rate_limits_json.read_text(encoding="utf-8"))
    data["rate_limits"]["services"]["default"]["max_concurrent"] = 99
    rate_limits_json.write_text(json.dumps(data), encoding="utf-8")
    with pytest.raises(ValidationError):
        load_rate_limits(rate_limits_json)


def test_version_mismatch_raises(rate_limits_json: Path):
    data = json.loads(rate_limits_json.read_text(encoding="utf-8"))
    data["version"] = "2.00"
    rate_limits_json.write_text(json.dumps(data), encoding="utf-8")
    with pytest.raises(ConfigVersionError):
        load_rate_limits(rate_limits_json)
