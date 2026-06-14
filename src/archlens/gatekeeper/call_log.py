"""Structured per-call logger for the gatekeeper (tasks 9.033, 9.034).

Emits exactly one JSON record per call (timestamp, model, input/output tokens, latency, queue
depth) through the archlens logger configured from config/logging_config.json. The API key is
redacted from the serialized record so it never appears in any log sink.
"""

import json
import logging
from datetime import datetime, timezone

from ..shared.constants import LOGGER_NAME

logger = logging.getLogger(f"{LOGGER_NAME}.gatekeeper.calls")

_REDACTED = "***"


def log_call(model, input_tokens, output_tokens, latency_ms, queue_depth,
             timestamp=None, secret=None) -> dict:
    """Build, redact, and emit one JSON call record; return the record dict."""
    record = {
        "timestamp": timestamp or datetime.now(timezone.utc).isoformat(),
        "model": model,
        "input_tokens": input_tokens,
        "output_tokens": output_tokens,
        "latency_ms": latency_ms,
        "queue_depth": queue_depth,
    }
    payload = json.dumps(record)
    if secret:
        payload = payload.replace(secret, _REDACTED)
    logger.info(payload)
    return record
