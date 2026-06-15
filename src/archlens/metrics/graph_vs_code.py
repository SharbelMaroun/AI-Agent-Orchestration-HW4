"""With-vs-without-Graphify evaluation: same bug analysis two ways, measuring tokens AND quality.

For each top bottleneck the agents find, we ask the model the SAME question once from the graph
neighbourhood (with Graphify) and once from the full source module (without it), then have an
LLM judge score both analyses 1-5 for correctness/specificity. Token usage is read back from the
gatekeeper ledger (tagged per call), so the numbers are the flow's real usage, not estimates.
"""

import re

from ..agents.bughunter_agent import _graph_context
from ..agents.source_reader import read_source_excerpt

_QUESTION = ("What is the main architectural problem with this component, and what refactor would "
             "relieve it? Answer in 3-4 sentences.")
_ARCH = ("You are a senior software architect. Name the main architectural problem and the refactor "
         "that relieves it. Be concrete and brief.")
_JUDGE = ("Two analyses of the SAME component below. Rate each 1-5 for correctness and specificity "
          "(5 = best). Reply EXACTLY in the form 'WITH: <n> WITHOUT: <n>'.\n\n"
          "WITH:\n{a}\n\nWITHOUT:\n{b}")


def _parse_scores(text: str) -> tuple[int, int]:
    """Pull the two 1-5 ratings from a judge reply like 'WITH: 4 WITHOUT: 3'."""
    nums = [int(n) for n in re.findall(r"[1-5]", text)]
    return (nums[0] if nums else 0, nums[1] if len(nums) > 1 else 0)


def _top_bottlenecks(graph, k: int) -> list[str]:
    return sorted(graph.nodes, key=lambda n: graph.in_degree(n), reverse=True)[:k]


def _evaluate_node(sdk, graph, node: str, repo_path: str) -> dict:
    source_file = graph.nodes[node].get("source_file", "")
    with_ans = sdk.ask_llm(f"{_graph_context(graph, node)}\n\n{_QUESTION}",
                           system=_ARCH, agent=f"with:{node}")
    code = read_source_excerpt(repo_path, source_file, max_chars=20000)
    without = sdk.ask_llm(f"Source of the module:\n```python\n{code}\n```\n\n{_QUESTION}",
                          system=_ARCH, agent=f"without:{node}", max_tokens=500)
    with_score, without_score = _parse_scores(
        sdk.ask_llm(_JUDGE.format(a=with_ans, b=without), agent=f"judge:{node}", max_tokens=20))
    return {"node": node, "source_file": source_file, "with_answer": with_ans,
            "without_answer": without, "with_score": with_score, "without_score": without_score}


def _aggregate(sdk, rows: list[dict]) -> dict:
    entries = sdk._gk().usage_ledger.entries
    total = lambda p: sum(e.input_tokens + e.output_tokens for e in entries if e.agent.startswith(p))  # noqa: E731
    with_tok, without_tok = total("with:"), total("without:")
    avg = lambda key: round(sum(r[key] for r in rows) / len(rows), 2) if rows else 0.0  # noqa: E731
    return {"rows": rows, "with_tokens": with_tok, "without_tokens": without_tok,
            "judge_tokens": total("judge:"),
            "with_quality": avg("with_score"), "without_quality": avg("without_score"),
            "token_savings_pct": round(100 * (1 - with_tok / without_tok), 1) if without_tok else 0.0}


def compare(sdk, graph, repo_path: str, top_k: int = 3) -> dict:
    """Evaluate the top_k bottlenecks with vs without Graphify; return tokens + quality aggregate."""
    rows = [_evaluate_node(sdk, graph, node, repo_path)
            for node in _top_bottlenecks(graph, top_k)]
    return _aggregate(sdk, rows)
