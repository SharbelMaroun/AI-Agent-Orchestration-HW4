"""With-vs-without-Graphify evaluation: real flow tokens AND LLM-judged quality, side by side.

Runs sdk.compare_graph_vs_code over the top bottlenecks: each is analysed once from the GRAPH
neighbourhood (with Graphify) and once from the full SOURCE module (without it); an LLM judge then
rates both 1-5. Token counts come from the gatekeeper ledger (the flow's real usage). Live key in
.env required.

    uv run python scripts/compare_graph_vs_code.py [graph.json] [repo_path] [top_k]
"""

import sys

from archlens.sdk.sdk import ArchLensSDK

_GRAPH = sys.argv[1] if len(sys.argv) > 1 else "runs/run/target/graphify-out/graph.json"
_REPO = sys.argv[2] if len(sys.argv) > 2 else "runs/run/target"
_TOP_K = int(sys.argv[3]) if len(sys.argv) > 3 else 3


def _run() -> None:
    report = ArchLensSDK().compare_graph_vs_code(_GRAPH, _REPO, _TOP_K)
    print(f"evaluated {len(report['rows'])} top bottlenecks (with vs without Graphify)\n")
    for row in report["rows"]:
        print(f"  {row['node']:32}  quality with={row['with_score']}  without={row['without_score']}")
    print("\n--- TOKENS (real, from the gatekeeper ledger) ---")
    print(f"  with Graphify   : {report['with_tokens']:6} tokens")
    print(f"  without Graphify: {report['without_tokens']:6} tokens")
    print(f"  token savings   : {report['token_savings_pct']}%")
    print("\n--- QUALITY (LLM judge, 1-5) ---")
    print(f"  with Graphify   : {report['with_quality']}")
    print(f"  without Graphify: {report['without_quality']}")
    print(f"\n(judge spent {report['judge_tokens']} tokens)")


if __name__ == "__main__":
    _run()
