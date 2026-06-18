"""Block model: each community becomes a named block with weighted inter-block edges (7.006)."""

import json
from collections import Counter
from dataclasses import dataclass
from pathlib import Path

from ..graphops.communities import load_communities


@dataclass(frozen=True)
class Block:
    """One architectural block (a community) with its member count."""

    name: str
    member_count: int


@dataclass(frozen=True)
class InterBlockEdge:
    """A directed, weighted dependency from one block to another."""

    source: str
    target: str
    weight: int


@dataclass(frozen=True)
class BlockModel:
    """Blocks plus the aggregated directed dependencies between them."""

    blocks: tuple[Block, ...]
    edges: tuple[InterBlockEdge, ...]


def build_block_model(source: dict | str | Path) -> BlockModel:
    """Build the block model from a graph.json: one block per community, weighted cross-edges."""
    data = source if isinstance(source, dict) else json.loads(Path(source).read_text(encoding="utf-8"))
    communities = load_communities(data)
    node_block = {member: c.label for c in communities for member in c.members}
    blocks = tuple(Block(c.label, len(c.members)) for c in communities)

    weights: Counter = Counter()
    for edge in data.get("links", data.get("edges", [])):
        source_block = node_block.get(edge.get("source", edge.get("from")))
        target_block = node_block.get(edge.get("target", edge.get("to")))
        if source_block and target_block and source_block != target_block:
            weights[(source_block, target_block)] += 1
    edges = tuple(InterBlockEdge(a, b, w) for (a, b), w in sorted(weights.items()))
    return BlockModel(blocks=blocks, edges=edges)


def top_block_model(model: BlockModel, limit: int) -> BlockModel:
    """Reduce to the ``limit`` largest blocks (by member count) and the edges among them.

    Used to render a readable macro view when a graph has many fine-grained communities; the
    full community inventory is still reported separately. ``limit<=0`` returns the model intact.
    """
    if limit <= 0 or len(model.blocks) <= limit:
        return model
    kept = sorted(model.blocks, key=lambda b: (-b.member_count, b.name))[:limit]
    names = {b.name for b in kept}
    edges = tuple(e for e in model.edges if e.source in names and e.target in names)
    return BlockModel(blocks=tuple(kept), edges=edges)
