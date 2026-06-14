"""Generate analysis charts from a real Graphify graph.json (Phase 15 visualization).

Reads runs/eval/httpie/graphify-out/graph.json (a real 2033-node / 4306-edge / 138-community
graph) and writes PNG charts into docs/diagrams/: community-size distribution, top hubs by
degree, node file-type mix, and a rendered subgraph of the top hubs and their neighbours.
"""

import json
from collections import Counter
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402  (backend must be set before pyplot import)
import networkx as nx  # noqa: E402

ROOT = Path(__file__).resolve().parents[1]
GRAPH = ROOT / "runs" / "eval" / "httpie" / "graphify-out" / "graph.json"
OUT = ROOT / "docs" / "diagrams"


def load_graph(path: Path) -> nx.DiGraph:
    data = json.loads(path.read_text(encoding="utf-8"))
    graph: nx.DiGraph = nx.DiGraph()
    for node in data["nodes"]:
        graph.add_node(node["id"], label=node.get("label") or node["id"],
                       community=node.get("community"), file_type=node.get("file_type") or "?")
    for link in data["links"]:
        graph.add_edge(link["source"], link["target"])
    return graph


def _bar(labels, counts, color, title, ylabel, path, horizontal=False):
    plt.figure(figsize=(10, 5))
    if horizontal:
        plt.barh(labels[::-1], counts[::-1], color=color)
        plt.xlabel(ylabel)
    else:
        plt.bar(labels, counts, color=color)
        plt.ylabel(ylabel)
    plt.title(title)
    plt.tight_layout()
    plt.savefig(path, dpi=120)
    plt.close()


def chart_communities(graph: nx.DiGraph, path: Path) -> None:
    sizes = Counter(graph.nodes[n]["community"] for n in graph.nodes).most_common(20)
    _bar([str(c) for c, _ in sizes], [n for _, n in sizes], "#4c72b0",
         "httpie - top 20 communities by member count", "nodes", path)


def chart_hubs(graph: nx.DiGraph, path: Path) -> None:
    top = sorted(graph.degree, key=lambda kv: kv[1], reverse=True)[:15]
    _bar([graph.nodes[n]["label"][:30] for n, _ in top], [d for _, d in top], "#dd8452",
         "httpie - top 15 hubs by total degree", "degree (in + out)", path, horizontal=True)


def chart_filetypes(graph: nx.DiGraph, path: Path) -> None:
    mix = Counter(graph.nodes[n]["file_type"] for n in graph.nodes).most_common()
    _bar([str(t) for t, _ in mix], [n for _, n in mix], "#55a868",
         "httpie - node file-type mix", "nodes", path)


def chart_subgraph(graph: nx.DiGraph, path: Path) -> None:
    hubs = [n for n, _ in sorted(graph.degree, key=lambda kv: kv[1], reverse=True)[:6]]
    nodes = set(hubs)
    for hub in hubs:
        nodes.update(list(graph.successors(hub))[:8])
        nodes.update(list(graph.predecessors(hub))[:8])
    sub = graph.subgraph(nodes)
    pos = nx.spring_layout(sub, seed=7, k=0.5)
    plt.figure(figsize=(10, 8))
    nx.draw_networkx_edges(sub, pos, alpha=0.2, arrowsize=5)
    nx.draw_networkx_nodes(sub, pos, node_color=["#c44e52" if n in hubs else "#bbbbbb"
                                                 for n in sub.nodes],
                           node_size=[320 if n in hubs else 60 for n in sub.nodes])
    nx.draw_networkx_labels(sub, pos, {h: graph.nodes[h]["label"][:18] for h in hubs}, font_size=8)
    plt.title("httpie - top-hub neighbourhood subgraph")
    plt.axis("off")
    plt.tight_layout()
    plt.savefig(path, dpi=120)
    plt.close()


def main() -> int:
    if not GRAPH.is_file():
        print(f"no graph.json at {GRAPH} - run `graphify update runs/eval/httpie` first")
        return 1
    graph = load_graph(GRAPH)
    OUT.mkdir(parents=True, exist_ok=True)
    chart_communities(graph, OUT / "analysis_communities.png")
    chart_hubs(graph, OUT / "analysis_hubs.png")
    chart_filetypes(graph, OUT / "analysis_filetypes.png")
    chart_subgraph(graph, OUT / "analysis_subgraph.png")
    print(f"wrote 4 analysis charts to {OUT} from {graph.number_of_nodes()} nodes")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
