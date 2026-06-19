"""Compile ``make_localizer_node`` into a real 1-node LangGraph StateGraph (EX04 §5.3).

So the graph-first BugLocalizer runs as a genuinely-executed, compiled LangGraph node — not merely a
bare function call. The debug flow drives this graph; ``make_localizer_node`` is therefore live, not
dead code w.r.t. the orchestration framework.
"""

from typing import TypedDict

from langgraph.graph import END, START, StateGraph

from ..agents.bug_localizer import make_localizer_node


class LocalizerState(TypedDict, total=False):
    """The localizer graph's channels: graph + failing symbol in, localization out."""

    graph_json: object
    graph_snapshot: dict
    failing_symbol: str
    localization: dict


def build_localizer_graph(sdk):
    """Compile a 1-node StateGraph (START -> BugLocalizer -> END) around the localizer node."""
    builder = StateGraph(LocalizerState)
    builder.add_node("BugLocalizer", make_localizer_node(sdk))
    builder.add_edge(START, "BugLocalizer")
    builder.add_edge("BugLocalizer", END)
    return builder.compile()


def run_localizer(sdk, graph_json, failing_symbol: str) -> dict:
    """Invoke the compiled localizer graph and return its localization payload."""
    graph = build_localizer_graph(sdk)
    state = graph.invoke({"graph_json": graph_json, "failing_symbol": failing_symbol})
    return state.get("localization", {})
