"""End-to-end wiki integrity: every page reachable from index within 2 hops, 0 orphans (14.029)."""

from archlens.sdk.sdk import ArchLensSDK


def _sources(tmp_path, n):
    out = []
    for i in range(n):
        src = tmp_path / f"s{i}.txt"
        src.write_text(f"content {i}", encoding="utf-8")
        out.append(src)
    return out


def test_every_wiki_page_reachable_no_orphans(tmp_path):
    topics = {"alpha": ["s0", "s1", "s2"], "beta": ["s3", "s4", "s5"]}
    root = ArchLensSDK().build_wiki(_sources(tmp_path, 6), topics, tmp_path / "vault")
    index = (root / "index.md").read_text(encoding="utf-8")
    wiki_pages = sorted(page.stem for page in (root / "wiki").glob("*.md"))
    linked = [name for name in wiki_pages if f"wiki/{name}.md" in index]
    assert linked == wiki_pages


def test_full_build_writes_log_entry_per_stage(tmp_path):
    root = ArchLensSDK().build_wiki(_sources(tmp_path, 1), {"t": ["s0"]}, tmp_path / "vault")
    log = (root / "log.md").read_text(encoding="utf-8")
    assert "raw | ingest" in log
    assert "wiki | build" in log
    assert "index | build" in log
