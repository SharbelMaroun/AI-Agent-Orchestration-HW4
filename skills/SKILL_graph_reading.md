---
name: graph-reading
description: Read the ArchLens dependency graph and Obsidian vault to answer architecture questions with cited evidence. Read-only.
allowed-tools: [Read, Grep, Glob]
triggers: [which module imports, what depends on, rank hot nodes, hot.md triage, find the hub, which are the bottlenecks, single point of failure]
disable-model-invocation: false
---

# When to use

Use this skill for read-only questions about a codebase's structure, answered from the graph and
vault rather than by reading raw source. Sharp trigger phrases:

- "which module imports X" / "what depends on Y"
- "rank hot nodes" (highest-degree / highest-betweenness modules)
- "hot.md triage" — start from the vault's `hot.md` entry point
- "find the hub" of a community
- "which modules are the bottlenecks / single points of failure"

Problem patterns this fits:

1. **Triage** — start at `index.md`, then `hot.md`, then 2–3 `wiki/` pages; never dump full source.
2. **Dependency tracing** — follow `imports`/`calls` edges from a node to its dependents.
3. **Community/cluster questions** — read the `wiki/community-*.md` page for the relevant cluster.

# Procedure

Every claim MUST cite evidence in the order **relation → confidence → source_file** (the citation
triple). Read `index.md` first, follow at most 2–3 wiki links, and quote the graph edge backing
each statement. Never assert a dependency that is not present as an edge in `graph.json`.

Worked example (a real edge from `runs/eval/httpie/graphify-out/graph.json`):

> `contributors_fetch` **contains** `contributors_fetch_debug` —
> relation: `contains`, confidence: `EXTRACTED`, source_file: `docs/contributors/fetch.py`.

Report the answer as: claim, then the citation triple, then the 1–2 wiki pages consulted. If the
graph has no edge supporting a claim, say so explicitly rather than inferring from source.
