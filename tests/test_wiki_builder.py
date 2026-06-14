"""TDD tests for the raw/ -> wiki/ builder (task 14.023)."""

from archlens.vault.raw_ingest import ingest_with_provenance
from archlens.vault.wiki_builder import build_wiki_pages


def _raw(tmp_path):
    sources = []
    for i in range(3):
        src = tmp_path / f"topic{i}.txt"
        src.write_text(f"summary line for topic {i}\nmore detail", encoding="utf-8")
        sources.append(src)
    ingest_with_provenance(tmp_path / "vault" / "raw", sources)
    return tmp_path / "vault"


def test_one_wiki_page_per_raw_note(tmp_path):
    vault = _raw(tmp_path)
    pages = build_wiki_pages(vault / "raw", vault / "wiki")
    assert len(pages) == 3


def test_every_wiki_page_backlinks_its_raw_source(tmp_path):
    vault = _raw(tmp_path)
    for page in build_wiki_pages(vault / "raw", vault / "wiki"):
        text = page.read_text(encoding="utf-8")
        assert f"../raw/{page.name}" in text
