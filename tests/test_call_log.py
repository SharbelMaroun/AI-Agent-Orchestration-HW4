"""TDD tests for the structured per-call logger and API-key redaction (tasks 9.032, 9.034)."""

import json
import logging

from archlens.gatekeeper.call_log import log_call

_FIELDS = ("timestamp", "model", "input_tokens", "output_tokens", "latency_ms", "queue_depth")
_TS = "2026-01-01T00:00:00+00:00"


def test_call_record_has_all_six_fields():
    record = log_call(model="claude-opus-4-8", input_tokens=10, output_tokens=5,
                      latency_ms=42, queue_depth=3, timestamp=_TS)
    for field in _FIELDS:
        assert field in record


def test_exactly_one_json_record_emitted(caplog):
    caplog.set_level(logging.INFO)
    log_call(model="claude-opus-4-8", input_tokens=10, output_tokens=5,
             latency_ms=42, queue_depth=3, timestamp=_TS)
    records = [r for r in caplog.records if r.name.endswith("calls")]
    assert len(records) == 1
    parsed = json.loads(records[0].message)
    assert parsed["model"] == "claude-opus-4-8"
    assert parsed["queue_depth"] == 3


def test_api_key_value_is_redacted(caplog):
    caplog.set_level(logging.INFO)
    log_call(model="m-sk-secret", input_tokens=1, output_tokens=1, latency_ms=5,
             queue_depth=0, timestamp=_TS, secret="sk-secret")
    assert "sk-secret" not in caplog.text
    assert "***" in caplog.text
