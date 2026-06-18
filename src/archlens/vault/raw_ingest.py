"""raw/ ingestion: copy Graphify artifacts verbatim with checksums (5.029-5.030); provenance (14.022)."""

import hashlib
import shutil
from datetime import datetime, timezone
from pathlib import Path

from ..shared.constants import GRAPHIFY_REPORT_MD
from ..vault.layout import VaultLayout
from ..vault.log_journal import append_entry


def default_graph_raw_sources(graph_path) -> list[str]:
    """Raw-layer provenance for a graph.json: the graph itself plus a sibling GRAPH_REPORT.md.

    Lets ``build_vault`` populate raw/ from a real Graphify run by default so the Karpathy
    raw -> wiki -> index -> log layer is demonstrated end-to-end, not left empty (Part B p5-8).
    """
    path = Path(graph_path)
    return [str(p) for p in (path, path.with_name(GRAPHIFY_REPORT_MD)) if p.is_file()]


def provenance_header(source, when: datetime | None = None) -> str:
    """An HTML-comment provenance header carrying the source path and ingest timestamp."""
    stamp = (when or datetime.now(timezone.utc)).isoformat()
    return f"<!-- provenance: source={source} ingested={stamp} -->\n"


def ingest_with_provenance(raw_dir, sources, when: datetime | None = None) -> list[Path]:
    """Write each source into raw/<stem>.md prefixed with a provenance header; return paths."""
    raw = Path(raw_dir)
    raw.mkdir(parents=True, exist_ok=True)
    written = []
    for source in sources:
        src = Path(source)
        dest = raw / f"{src.stem}.md"
        body = src.read_text(encoding="utf-8", errors="replace")
        dest.write_text(f"{provenance_header(src, when)}\n# Raw: {src.name}\n\n{body}\n",
                        encoding="utf-8")
        written.append(dest)
    return written


def _sha256(path) -> str:
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def ingest_raw(layout: VaultLayout, sources: list) -> dict[str, str]:
    """Copy each source into raw/ unmodified; return {name: sha256} and log each copy."""
    layout.create()
    digests: dict[str, str] = {}
    for source in sources:
        src = Path(source)
        dest = layout.raw_dir / src.name
        shutil.copyfile(src, dest)
        digests[src.name] = _sha256(dest)
        append_entry(layout.log_md, "raw-ingest", src.name)
    return digests
