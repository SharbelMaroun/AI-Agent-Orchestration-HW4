"""Tests for the §3.1 rate-limit key-name constants and config integrity (tasks 9.004, 9.005)."""

import json

from archlens.gatekeeper import Gatekeeper
from archlens.shared.constants import (
    QUEUE_KEYS,
    RATE_LIMITS_FILE,
    RATE_LIMITS_SCHEMA_KEYS,
    SERVICE_LIMIT_KEYS,
    VERSION_KEY,
)


def test_schema_key_constants_cover_all_eight_keys():
    assert len(RATE_LIMITS_SCHEMA_KEYS) == 8
    assert VERSION_KEY in RATE_LIMITS_SCHEMA_KEYS
    assert set(SERVICE_LIMIT_KEYS) | set(QUEUE_KEYS) | {VERSION_KEY} == set(RATE_LIMITS_SCHEMA_KEYS)


def test_rate_limits_json_matches_the_schema_keys():
    data = json.loads(RATE_LIMITS_FILE.read_text(encoding="utf-8"))
    default = data["rate_limits"]["services"]["default"]
    assert set(default) == set(SERVICE_LIMIT_KEYS)
    assert set(data["queue"]) == set(QUEUE_KEYS)
    assert VERSION_KEY in data


def test_gatekeeper_exported_from_package():
    assert Gatekeeper().limits is not None
