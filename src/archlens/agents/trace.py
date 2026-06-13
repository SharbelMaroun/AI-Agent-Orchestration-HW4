"""Run-trace logger: one JSONL record per node transition (task 10.042).

The sink path is derived from the file handler in config/logging_config.json so the trace
honours the configured logging sink.
"""

import json
import time
from pathlib import Path

from archlens.shared.constants import LOGGING_CONFIG_FILE


def _trace_sink() -> str:
    config = json.loads(Path(LOGGING_CONFIG_FILE).read_text(encoding="utf-8"))
    base = config["handlers"]["file"]["filename"]
    return str(Path(base).with_suffix(".trace.jsonl"))


class TraceLogger:
    """Append one structured JSONL record per visited node."""

    def __init__(self, sink_path: str | Path | None = None) -> None:
        self.path = Path(sink_path or _trace_sink())
        self.path.parent.mkdir(parents=True, exist_ok=True)

    def record(self, node: str, loop_iteration: int = 0,
               duration_ms: float = 0.0, tokens: int = 0) -> None:
        entry = {"node": node, "loop_iteration": loop_iteration,
                 "duration_ms": duration_ms, "tokens": tokens}
        with self.path.open("a", encoding="utf-8") as sink:
            sink.write(json.dumps(entry) + "\n")

    def records(self) -> list[dict]:
        if not self.path.exists():
            return []
        return [json.loads(line) for line in self.path.read_text(encoding="utf-8").splitlines() if line]


def traced(node, name: str, logger: TraceLogger):
    """Wrap a node so each transition appends a trace record."""

    def wrapped(state: dict) -> dict:
        start = time.perf_counter()
        result = node(state)
        logger.record(name, loop_iteration=state.get("loop_iteration", 0),
                      duration_ms=round((time.perf_counter() - start) * 1000, 3))
        return result

    return wrapped
