"""raw/ ingestion: copy Graphify artifacts verbatim with checksums (tasks 5.029-5.030)."""

import hashlib
import shutil
from pathlib import Path

from ..vault.layout import VaultLayout
from ..vault.log_journal import append_entry


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
