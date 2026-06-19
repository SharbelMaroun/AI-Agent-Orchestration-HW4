"""Graph-first bug localizer (EX04 §5.3): trace an import failure to its suspect node.

Given a failing symbol (e.g. from an ImportError) and the dependency graph, this localizes the defect
WITHOUT reading source: it resolves the symbol's definition node, finds the importers and the package
re-export hub they route through, nominates the hub as the prime suspect, and explains the root cause
from the graph neighbourhood (the SDK LLM when wired via the node; a deterministic fallback otherwise).
"""

from dataclasses import dataclass

from ..agents import prompt_loader
from ..graphops.loader import load_graph

# System prompt loaded by id+version from the prompt book — no inline literal (PRD §9 / FR-AO-13).
_PROMPT = "localizer"
_SYSTEM = prompt_loader.system_prompt(_PROMPT)
_PID = prompt_loader.prompt_id(_PROMPT)
_PVER = prompt_loader.version_of(_PROMPT)


@dataclass(frozen=True)
class BugLocalization:
    """A graph-derived localization of a failing symbol to a suspect node + root-cause narrative."""

    failing_symbol: str
    suspect: str
    suspect_file: str
    importers: tuple[str, ...]
    evidence: tuple[str, ...]
    root_cause: str


def _symbol_node(graph, symbol: str):
    """Resolve a symbol name to its graph node, by exact id, id suffix, or function label."""
    for node, data in graph.nodes(data=True):
        label = (data.get("label") or "").split("(")[0].strip()
        if node == symbol or node.endswith(f"_{symbol}") or label == symbol:
            return node
    return None


def _importers(graph, target: str) -> list[str]:
    return sorted(u for u, v, rel in graph.edges(data="relation")
                  if v == target and rel in ("imports", "re_exports"))


def _deterministic_cause(suspect_file: str, symbol: str) -> str:
    return (f"The re-export hub `{suspect_file}` does not expose `{symbol}`, so the "
            f"`from ... import {symbol}` at the entry point raises ImportError; restore the "
            "re-export (and fix the gated leaf module) to clear it.")


def localize_import_failure(graph_source, failing_symbol: str, explain=None) -> BugLocalization:
    """Localize an ImportError for ``failing_symbol`` to its re-export hub, graph-first.

    ``explain(suspect_file, symbol, evidence)`` is an optional callable (e.g. an LLM) returning the
    root-cause narrative from the graph evidence; without it a deterministic explanation is used.
    """
    graph = load_graph(graph_source)
    symbol = _symbol_node(graph, failing_symbol)
    importers = _importers(graph, symbol) if symbol else []
    hubs = [n for n in importers if n.endswith("_init") or n.endswith("__init__")]
    candidates = hubs or importers or ([symbol] if symbol else [])
    suspect = max(candidates, key=graph.degree, default=failing_symbol)
    suspect_file = graph.nodes[suspect].get("source_file", suspect) if graph.has_node(suspect) else ""
    degree = graph.degree(suspect) if graph.has_node(suspect) else 0
    evidence = (
        f"`{failing_symbol}` resolves to node `{symbol}`." if symbol
        else f"`{failing_symbol}` has no definition node reachable from the package hub.",
        f"Importers routing through the package: {importers}.",
        f"Prime suspect `{suspect}` (degree {degree}) is the package re-export hub every import must "
        "pass through — the natural origin of an ImportError for a package symbol.",
    )
    root_cause = (explain(suspect_file, failing_symbol, evidence) if explain
                  else _deterministic_cause(suspect_file, failing_symbol))
    return BugLocalization(failing_symbol, suspect, suspect_file, tuple(importers), evidence, root_cause)


def make_localizer_node(sdk):
    """LangGraph node: localize the failing symbol graph-first, then explain it via the SDK LLM."""

    def localizer_node(state: dict) -> dict:
        graph_json = (state.get("graph_snapshot") or {}).get("graph_json") or state.get("graph_json")
        symbol = state.get("failing_symbol", "")

        def _explain(suspect_file, sym, evidence):
            prompt = (f"An ImportError reports that `{sym}` cannot be imported. Using ONLY this "
                      f"dependency-graph evidence (no source code):\n- " + "\n- ".join(evidence) +
                      f"\n\nIn 2-3 sentences, name the file to fix (`{suspect_file}`) and the root cause.")
            return sdk.ask_llm(prompt, system=_SYSTEM, agent="BugLocalizer", max_tokens=200,
                               prompt_id=_PID, prompt_version=_PVER)

        loc = localize_import_failure(graph_json, symbol, explain=_explain if symbol else None)
        return {"localization": {
            "failing_symbol": loc.failing_symbol, "suspect": loc.suspect,
            "suspect_file": loc.suspect_file, "importers": list(loc.importers),
            "evidence": list(loc.evidence), "root_cause": loc.root_cause}}

    return localizer_node
