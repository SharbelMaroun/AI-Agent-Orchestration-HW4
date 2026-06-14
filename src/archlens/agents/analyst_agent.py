"""AnalystAgent node — append typed analysis findings into state via the SDK (task 10.018)."""


def make_analyst_node(sdk):
    """Factory: bind the SDK and return the analyst node (state in -> findings delta out)."""

    def analyst_node(state: dict) -> dict:
        graph = sdk.load_analysis_graph(state["graph_snapshot"]["graph_json"])
        communities = sdk.density_communities(graph)
        findings: list[dict] = [
            {"from": "analyst", "category": "community_count", "count": len(communities)},
        ]
        for row in sdk.node_centrality(graph)[:5]:
            findings.append({"from": "analyst", "category": "centrality",
                             "node": row.node_id, "degree": row.degree_total,
                             "betweenness": row.betweenness})
        for verdict in sdk.classify_nodes(graph):
            findings.append({"from": "analyst", "category": "hub_vs_bottleneck",
                             "node": verdict.node_id, "verdict": verdict.verdict})
        for bucket, items in sdk.triage_edges(graph).items():
            findings.append({"from": "analyst", "category": "triage",
                             "bucket": bucket, "count": len(items)})
        return {"findings": findings}

    return analyst_node
