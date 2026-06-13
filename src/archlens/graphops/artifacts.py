"""Artifact handler: copy graph.html into the run dir with a checksum (tasks 4.034-4.035)."""

import hashlib
import shutil
from pathlib import Path

from archlens.graphops.layout import RunLayout
from archlens.graphops.manifest import ArtifactRef
from archlens.shared.constants import GRAPH_HTML


def sha256_file(path) -> str:
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def register_graph_html(layout: RunLayout, source) -> ArtifactRef:
    """Copy graph.html into the run dir, checksum it, and return a manifest ArtifactRef."""
    layout.create()
    shutil.copyfile(source, layout.graph_html)
    return ArtifactRef(
        name=GRAPH_HTML, path=str(layout.graph_html), sha256=sha256_file(layout.graph_html)
    )
