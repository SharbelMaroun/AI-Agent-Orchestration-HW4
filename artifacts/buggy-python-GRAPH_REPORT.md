# Graph Report - buggy-python  (2026-06-18)

## Corpus Check
- 7 files · ~578 words
- Verdict: corpus is large enough that graph structure adds value.

## Summary
- 19 nodes · 28 edges · 4 communities (2 shown, 2 thin omitted)
- Extraction: 100% EXTRACTED · 0% INFERRED · 0% AMBIGUOUS
- Token cost: 0 input · 0 output

## Graph Freshness
- Built from commit: `88700933`
- Run `git rev-parse HEAD` and compare to check if the graph is stale.
- Run `graphify update .` after code changes (no API cost).

## Community Hubs (Navigation)
- [[_COMMUNITY_Community 0|Community 0]]
- [[_COMMUNITY_Community 1|Community 1]]
- [[_COMMUNITY_Community 2|Community 2]]
- [[_COMMUNITY_Community 3|Community 3]]

## God Nodes (most connected - your core abstractions)
1. `Buggy Python` - 4 edges
2. `foo()` - 3 edges
3. `read_file()` - 3 edges
4. `calculate_unpaid_loans()` - 3 edges
5. `calculate_paid_loans()` - 3 edges
6. `average_paid_loans()` - 3 edges
7. `lambda_array()` - 3 edges
8. `The purpose of this snippet is to test your knowledge of default arguments for f` - 1 edges
9. `Simple python script to read a json file of loan then add perform some calculati` - 1 edges
10. `Simple array of lambda functions that is used to calculate the addition of a num` - 1 edges

## Surprising Connections (you probably didn't know these)
- None detected - all connections are within the same source files.

## Import Cycles
- None detected.

## Communities (4 total, 2 thin omitted)

### Community 0 - "Community 0"
Cohesion: 0.50
Nodes (5): average_paid_loans(), calculate_paid_loans(), calculate_unpaid_loans(), Simple python script to read a json file of loan then add perform some calculati, read_file()

### Community 1 - "Community 1"
Cohesion: 0.40
Nodes (4): Buggy Python, Description, Instructions, Requirements

## Knowledge Gaps
- **3 isolated node(s):** `Description`, `Requirements`, `Instructions`
  These have ≤1 connection - possible missing edges or undocumented components.
- **2 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `foo()` connect `Community 2` to `Community 0`?**
  _High betweenness centrality (0.014) - this node is a cross-community bridge._
- **Why does `lambda_array()` connect `Community 3` to `Community 0`?**
  _High betweenness centrality (0.014) - this node is a cross-community bridge._
- **What connects `The purpose of this snippet is to test your knowledge of default arguments for f`, `Simple python script to read a json file of loan then add perform some calculati`, `Simple array of lambda functions that is used to calculate the addition of a num` to the rest of the system?**
  _6 weakly-connected nodes found - possible documentation gaps or missing edges._