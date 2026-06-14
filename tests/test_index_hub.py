"""TDD tests for the index.md hub generator (task 14.025)."""

from archlens.vault.index_builder import build_index


def test_index_links_two_to_three_wiki_pages_per_topic(tmp_path):
    topics = {"retrieval": ["client", "session", "auth"], "rendering": ["output", "format"]}
    index = build_index(tmp_path / "index.md", topics)
    text = index.read_text(encoding="utf-8")
    assert "## retrieval" in text and "## rendering" in text
    for pages in topics.values():
        for name in pages:
            assert f"wiki/{name}.md" in text


def test_index_caps_topic_links_at_three(tmp_path):
    topics = {"big": ["a", "b", "c", "d", "e"]}
    text = build_index(tmp_path / "index.md", topics).read_text(encoding="utf-8")
    assert text.count("wiki/") == 3


def test_index_is_read_first_hub(tmp_path):
    text = build_index(tmp_path / "index.md", {"t": ["a", "b"]}).read_text(encoding="utf-8")
    assert "read first" in text.lower()
