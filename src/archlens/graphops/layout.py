"""Run-scoped artifact directory layout and run-id generation (tasks 4.018-4.021)."""

import itertools
import time
from dataclasses import dataclass
from pathlib import Path

from ..shared.constants import GRAPH_HTML, GRAPH_JSON, MANIFEST_JSON, REPORT_MD

_counter = itertools.count()


def new_run_id(now: float | None = None) -> str:
    """Lexicographically sortable, collision-free run id (timestamp + process counter)."""
    stamp = time.time() if now is None else now
    return f"run-{stamp:015.3f}-{next(_counter):05d}"


@dataclass
class RunLayout:
    """Paths for one Graphify run; create() materializes the directory."""

    root: Path
    run_id: str

    @property
    def run_dir(self) -> Path:
        return Path(self.root) / self.run_id

    @property
    def graph_json(self) -> Path:
        return self.run_dir / GRAPH_JSON

    @property
    def graph_html(self) -> Path:
        return self.run_dir / GRAPH_HTML

    @property
    def report_md(self) -> Path:
        return self.run_dir / REPORT_MD

    @property
    def manifest(self) -> Path:
        return self.run_dir / MANIFEST_JSON

    def create(self) -> "RunLayout":
        self.run_dir.mkdir(parents=True, exist_ok=True)
        return self
