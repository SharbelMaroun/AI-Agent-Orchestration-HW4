# Hot — Bug-Investigation Hotspot

The nodes to look at first, ranked by **graph centrality** on the buggy-python import graph
(`archlens` `node_centrality`), not by reading every file.

| Rank | Node | Degree | Role in the failure |
|---|---|---|---|
| 1 | **`snippets/__init__.py`** (`snippets_init`) | **9** | re-export **hub** — every imported symbol routes through it; the import failure originates here |
| 2 | `main.py` | 6 | entry point / test harness (do **not** modify) |
| 3 | `snippets/io.py` | 6 | leaf module (BOTTLENECK) — loan calculations, multiple defects |
| 4 | `snippets/foobar.py` | 3 | leaf module — mutable-default bug |
| 5 | `snippets/loop.py` | — | lambda array — JS-ism bugs |

→ The hub is the #1 centrality node **and** the first failure site, so the investigation starts at
[[suspects#1-snippetsinitpy--the-re-export-hub-primary|snippets/__init__.py]].
