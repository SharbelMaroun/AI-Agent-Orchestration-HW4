# Savings Explanation

Version: 1.00 | Status: Generated | Course: AI Agent Orchestration — HW4 (EX04)

## Part A reality check — amortizing the Graphify build cost

The Graphify-assisted protocol achieved **{{savings_pct}}%** per-query token savings versus the
naive full-context baseline. Because this figure is below the 70% headline target, the result must
be read against the one-time cost of building the knowledge graph rather than taken at face value.

Building the graph cost approximately **{{graph_build_tokens}}** tokens up front. That investment is
amortized across queries: every query saves tokens relative to the baseline, so the graph pays for
itself after **{{break_even_queries}}** queries. Beyond that break-even point, each additional query
is pure savings.

In short, the initial graph-scan cost is not free — but it is a fixed cost paid once, while the
per-query savings recur for the life of the project. As the number of queries grows, the effective
savings converge toward the per-query figure quoted above.
