"""TDD tests for provenance-stamped raw/ ingestion (task 14.021)."""

from archlens.vault.raw_ingest import ingest_with_provenance, provenance_header


def _sources(tmp_path):
    out = []
    for name, body in (("graph.json", '{"nodes": []}'), ("REPORT.md", "# Report"),
                       ("hot.md", "# Hot")):
        path = tmp_path / name
        path.write_text(body, encoding="utf-8")
        out.append(path)
    return out


def test_every_ingested_file_carries_provenance_header(tmp_path):
    written = ingest_with_provenance(tmp_path / "vault" / "raw", _sources(tmp_path))
    assert len(written) == 3
    for note in written:
        text = note.read_text(encoding="utf-8")
        assert text.startswith("<!-- provenance:")
        assert "source=" in text
        assert "ingested=" in text


def test_provenance_header_contains_source_and_timestamp():
    header = provenance_header("docs/x.py")
    assert "source=docs/x.py" in header
    assert "ingested=" in header
