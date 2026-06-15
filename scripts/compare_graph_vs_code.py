"""With-vs-without-Graphify comparison: answer ONE architecture question two ways, count real tokens.

Same question, same model, same node — one prompt fed the node's GRAPH neighbourhood (with Graphify),
the other fed the node's full SOURCE module (without Graphify, the naive approach). Reports each
call's real token usage from the gatekeeper ledger and the savings. Run with a live key in .env:

    uv run python scripts/compare_graph_vs_code.py [graph.json] [repo_path]
"""

import sys

from archlens.agents.bughunter_agent import _graph_context
from archlens.agents.source_reader import read_source_excerpt
from archlens.sdk.sdk import ArchLensSDK

_GRAPH = sys.argv[1] if len(sys.argv) > 1 else "runs/run/target/graphify-out/graph.json"
_REPO = sys.argv[2] if len(sys.argv) > 2 else "runs/run/target"
_SYSTEM = ("You are a senior software architect. Name the main architectural problem and the "
           "refactor that relieves it. Be concrete and brief.")
_QUESTION = ("What is the main architectural problem with this component, and what refactor would "
             "relieve it? Answer in 3-4 sentences.")


def _run() -> None:
    sdk = ArchLensSDK()
    graph = sdk.load_analysis_graph(_GRAPH)
    node = max(graph.nodes, key=lambda n: graph.in_degree(n))  # the worst hub
    source_file = graph.nodes[node].get("source_file", "")
    print(f"target node: {node}  ({source_file})\n")

    with_graph = sdk.ask_llm(f"{_graph_context(graph, node)}\n\n{_QUESTION}",
                             system=_SYSTEM, agent="with_graphify")
    code = read_source_excerpt(_REPO, source_file, max_chars=20000)
    without = sdk.ask_llm(f"Source of the module:\n```python\n{code}\n```\n\n{_QUESTION}",
                          system=_SYSTEM, agent="without_graphify", max_tokens=500)

    rows = {e.agent: e for e in sdk._gk().usage_ledger.entries}
    g, c = rows["with_graphify"], rows["without_graphify"]
    gt, ct = g.input_tokens + g.output_tokens, c.input_tokens + c.output_tokens
    print(f"WITH Graphify   (graph context): {gt:5} tokens  (in {g.input_tokens}/out {g.output_tokens})")
    print(f"  -> {with_graph}\n")
    print(f"WITHOUT Graphify (full source) : {ct:5} tokens  (in {c.input_tokens}/out {c.output_tokens})")
    print(f"  -> {without}\n")
    saved = 100.0 * (1 - gt / ct) if ct else 0.0
    print(f"SAVINGS: {gt} vs {ct} tokens  =>  {saved:.1f}% fewer with Graphify (same question/answer)")


if __name__ == "__main__":
    _run()
