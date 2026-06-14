"""TDD tests for the Graphify-assisted retriever (task 12.022)."""

import json

from archlens.metrics.assisted_retriever import AssistedRetriever
from archlens.metrics.questions import Question


def _vault(tmp_path):
    root = tmp_path / "vault"
    (root / "wiki").mkdir(parents=True)
    (root / "index.md").write_text("# Index\nHub overview of communities.", encoding="utf-8")
    (root / "wiki" / "community-1.md").write_text(
        "bottleneck modules with high betweenness", encoding="utf-8")
    (root / "wiki" / "community-2.md").write_text("authentication and sessions", encoding="utf-8")
    (root / "wiki" / "community-3.md").write_text("hub god node central modules", encoding="utf-8")
    (root / "wiki" / "community-4.md").write_text("test coverage files", encoding="utf-8")
    return root


def _graph(tmp_path):
    graph = tmp_path / "graph.json"
    graph.write_text(json.dumps({"nodes": [
        {"label": "bottleneck_core.py"}, {"label": "auth.py"}, {"label": "client.py"}]}),
        encoding="utf-8")
    return graph


def _q(text="Which modules are bottlenecks with high betweenness?", ev="bottleneck"):
    return Question(id="Q04", text=text, expected_evidence=ev)


def test_index_is_read_first(tmp_path):
    ctx = AssistedRetriever(_vault(tmp_path)).retrieve(_q())
    assert "Hub overview" in ctx
    assert ctx.index("Hub overview") < ctx.index("# wiki:")


def test_wiki_pages_capped_at_three(tmp_path):
    retriever = AssistedRetriever(_vault(tmp_path), max_wiki_pages=3)
    assert len(retriever.select_wiki(_q())) == 3


def test_relevant_wiki_selected_by_keywords(tmp_path):
    retriever = AssistedRetriever(_vault(tmp_path), max_wiki_pages=1)
    assert retriever.select_wiki(_q())[0].name == "community-1.md"


def test_subgraph_includes_matching_nodes(tmp_path):
    ctx = AssistedRetriever(_vault(tmp_path)).retrieve(_q(), _graph(tmp_path))
    assert "bottleneck_core.py" in ctx


def test_no_raw_source_dump(tmp_path):
    ctx = AssistedRetriever(_vault(tmp_path)).retrieve(_q(), _graph(tmp_path))
    assert "# FILE:" not in ctx
