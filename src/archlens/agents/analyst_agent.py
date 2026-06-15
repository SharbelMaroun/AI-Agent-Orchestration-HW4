"""AnalystAgent node — append typed analysis findings into state via the SDK (task 10.018).

After the deterministic graph metrics, it asks the LLM (through the SDK, so it stays provider-
agnostic and never imports a client) for a short architectural reading of the top hubs.
"""


def _interpretation(sdk, top_rows, communities: int) -> dict:
    """An LLM-authored one-paragraph reading of the graph's top hubs (offline mock when no key)."""
    hubs = ", ".join(f"{row.node_id} (degree {row.degree_total})" for row in top_rows) or "none"
    prompt = (
        "You are a software architect reverse-engineering a codebase from its dependency graph. "
        f"It has {communities} communities; the highest-degree hubs are: {hubs}. In 2-3 sentences, "
        "explain the architectural risk these hubs pose and what to investigate first.")
    system = ("You are a software architect reading a dependency graph during reverse engineering; "
              "be concrete about coupling and single-points-of-failure risk.")
    return {"from": "analyst", "category": "llm_summary",
            "text": sdk.ask_llm(prompt, system=system, agent="AnalystAgent")}


def make_analyst_node(sdk):
    """Factory: bind the SDK and return the analyst node (state in -> findings delta out)."""

    def analyst_node(state: dict) -> dict:
        graph = sdk.load_analysis_graph(state["graph_snapshot"]["graph_json"])
        communities = sdk.density_communities(graph)
        centrality = sdk.node_centrality(graph)
        findings: list[dict] = [
            {"from": "analyst", "category": "community_count", "count": len(communities)},
        ]
        for row in centrality[:5]:
            findings.append({"from": "analyst", "category": "centrality",
                             "node": row.node_id, "degree": row.degree_total,
                             "betweenness": row.betweenness})
        for verdict in sdk.classify_nodes(graph):
            findings.append({"from": "analyst", "category": "hub_vs_bottleneck",
                             "node": verdict.node_id, "verdict": verdict.verdict})
        for bucket, items in sdk.triage_edges(graph).items():
            findings.append({"from": "analyst", "category": "triage",
                             "bucket": bucket, "count": len(items)})
        findings.append(_interpretation(sdk, centrality[:5], len(communities)))
        return {"findings": findings}

    return analyst_node
