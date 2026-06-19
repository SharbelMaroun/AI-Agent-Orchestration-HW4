"""TDD tests for the graph-first bug localizer (EX04 §5.3)."""

from archlens.agents.bug_localizer import localize_import_failure, make_localizer_node
from archlens.sdk.sdk import ArchLensSDK

# Minimal node-link graph: entry `main` imports `thing` via the package hub `pkg/__init__.py`.
GRAPH = {
    "nodes": [
        {"id": "main", "label": "main.py", "file_type": "code", "source_file": "main.py", "community": 0},
        {"id": "pkg_init", "label": "__init__.py", "file_type": "code", "source_file": "pkg/__init__.py", "community": 0},
        {"id": "pkg_mod_thing", "label": "thing()", "file_type": "code", "source_file": "pkg/mod.py", "community": 1},
    ],
    "links": [
        {"source": "main", "target": "pkg_mod_thing", "relation": "imports",
         "confidence": "EXTRACTED", "confidence_score": 1.0, "source_file": "main.py"},
        {"source": "pkg_init", "target": "pkg_mod_thing", "relation": "imports",
         "confidence": "EXTRACTED", "confidence_score": 1.0, "source_file": "pkg/__init__.py"},
    ],
    "hyperedges": [],
}


def test_localizes_import_failure_to_the_reexport_hub():
    loc = localize_import_failure(GRAPH, "thing")
    assert loc.suspect == "pkg_init"
    assert loc.suspect_file == "pkg/__init__.py"   # the package re-export hub, not the leaf
    assert "main" in loc.importers
    assert "thing" in loc.root_cause and "ImportError" in loc.root_cause


def test_localizer_uses_an_llm_explanation_when_provided():
    seen = {}

    def explain(suspect_file, symbol, evidence):
        seen["file"] = suspect_file
        return f"ROOT CAUSE: {suspect_file} omits {symbol}"

    loc = localize_import_failure(GRAPH, "thing", explain=explain)
    assert seen["file"] == "pkg/__init__.py"
    assert loc.root_cause.startswith("ROOT CAUSE:")


def test_localizer_node_emits_localization_via_the_sdk_llm():
    class _SDK:
        def ask_llm(self, prompt, *, system=None, agent="orchestrator", max_tokens=512, **kwargs):
            return "graph-first explanation: fix pkg/__init__.py"

    out = make_localizer_node(_SDK())({"graph_json": GRAPH, "failing_symbol": "thing"})
    loc = out["localization"]
    assert loc["suspect_file"] == "pkg/__init__.py"
    assert loc["root_cause"].startswith("graph-first explanation")


def test_sdk_localize_bug_is_the_single_entry_point():
    loc = ArchLensSDK().localize_bug(GRAPH, "thing")
    assert loc.suspect_file == "pkg/__init__.py"


def test_localizer_runs_as_a_compiled_langgraph_node():
    # §5.3: make_localizer_node is executed through a real compiled StateGraph, not just called.
    from archlens.agents.localizer_graph import build_localizer_graph, run_localizer

    class _SDK:
        def ask_llm(self, prompt, *, system=None, agent="orchestrator", max_tokens=512, **kwargs):
            return "graph-first explanation: fix pkg/__init__.py"

    graph = build_localizer_graph(_SDK())
    assert "BugLocalizer" in set(graph.get_graph().nodes)  # genuinely a wired graph node
    loc = run_localizer(_SDK(), GRAPH, "thing")            # invoked via compiled graph
    assert loc["suspect_file"] == "pkg/__init__.py"
    assert loc["root_cause"].startswith("graph-first explanation")
