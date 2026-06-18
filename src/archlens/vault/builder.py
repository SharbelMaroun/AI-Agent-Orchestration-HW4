"""VaultBuilder — orchestrates every generator behind build_vault (tasks 5.037-5.040)."""

from ..graphops.parser import Graph
from ..vault.community_pages import write_community_pages
from ..vault.config import VaultConfig
from ..vault.hot_page import render_hot
from ..vault.index_page import render_index
from ..vault.layout import VaultLayout
from ..vault.log_journal import append_entry
from ..vault.raw_ingest import ingest_raw


def build_vault(graph: Graph, cfg: VaultConfig, raw_sources: list | None = None) -> VaultLayout:
    """Run layout -> raw_ingest -> community_pages -> hot -> index -> log in one call.

    Regenerated notes (wiki/, hot.md, index.md) are deterministic; log.md is append-only,
    so a rebuild yields byte-identical pages while the journal grows by one entry.
    """
    layout = VaultLayout(cfg).create()
    if raw_sources:
        ingest_raw(layout, raw_sources)
    write_community_pages(graph, layout)
    artifacts = sorted(p.name for p in layout.raw_dir.iterdir() if p.is_file())
    layout.hot_md.write_text(render_hot(graph, cfg), encoding="utf-8")
    layout.index_md.write_text(render_index(graph, cfg, artifacts=artifacts), encoding="utf-8")
    append_entry(layout.log_md, "vault-build", f"{len(graph.nodes)} nodes")
    return layout
