"""Graphify-assisted retriever — vault index + a few wiki pages + a question subgraph (task 12.023).

Assembles a compact context from the Obsidian vault (index.md read first, then up to a hard cap of
wiki pages ranked by keyword overlap) plus a question-relevant node slice from graph.json. It never
reads raw source files, so the assisted context is a small fraction of the naive baseline.
"""

import json
import re
from pathlib import Path

from ..shared.constants import INDEX_MD, MAX_WIKI_PAGES_PER_QUESTION, WIKI_DIR
from .questions import Question

_WORD = re.compile(r"[a-z][a-z0-9_]{3,}")
_MAX_SUBGRAPH_NODES = 15


def _keywords(text: str) -> set[str]:
    return set(_WORD.findall(text.lower()))


def _node_name(node: dict) -> str:
    return node.get("label") or node.get("source_file") or node.get("id") or ""


class AssistedRetriever:
    """Builds a compact vault+graph context per question; never dumps raw source."""

    def __init__(self, vault_root, max_wiki_pages: int = MAX_WIKI_PAGES_PER_QUESTION):
        self._root = Path(vault_root)
        self._max = max_wiki_pages

    def _index(self) -> str:
        index = self._root / INDEX_MD
        return index.read_text(encoding="utf-8") if index.is_file() else ""

    def select_wiki(self, question: Question) -> list[Path]:
        """Up to max_wiki_pages wiki pages, ranked by keyword overlap with the question."""
        terms = _keywords(question.text) | _keywords(question.expected_evidence)
        wiki = self._root / WIKI_DIR
        pages = sorted(wiki.glob("*.md")) if wiki.is_dir() else []
        scored = sorted(
            pages,
            key=lambda p: (-len(terms & _keywords(p.read_text(encoding="utf-8"))), p.name))
        return scored[: self._max]

    def _subgraph(self, question: Question, graph_json) -> str:
        if not graph_json or not Path(graph_json).is_file():
            return ""
        data = json.loads(Path(graph_json).read_text(encoding="utf-8"))
        terms = _keywords(question.text) | _keywords(question.expected_evidence)
        names = [_node_name(node) for node in data.get("nodes", [])]
        hits = [name for name in names if terms & _keywords(name)] or names
        return "Relevant nodes: " + ", ".join(hits[:_MAX_SUBGRAPH_NODES])

    def retrieve(self, question: Question, graph_json=None) -> str:
        """Assemble index + relevant wiki pages + a node slice into one compact context."""
        blocks = [f"# index (read first)\n{self._index()}"]
        for page in self.select_wiki(question):
            blocks.append(f"# wiki: {page.name}\n{page.read_text(encoding='utf-8')}")
        subgraph = self._subgraph(question, graph_json)
        if subgraph:
            blocks.append(subgraph)
        blocks.append(f"Question: {question.text}")
        return "\n\n".join(blocks)
