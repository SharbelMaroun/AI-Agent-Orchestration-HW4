# CLI UX — Nielsen 10-Heuristics Evaluation

Version: 1.00 | Course: AI Agent Orchestration — HW4 (EX04) | Task 16.026

Evaluation of the ArchLens CLI (`src/main.py`) and its generated outputs. Severity scale: 0 (none),
1 (cosmetic), 2 (minor), 3 (major), 4 (catastrophe). Evidence: `docs/screenshots/cli_run.png`.

| # | Heuristic | Verdict | Severity | Evidence |
| --- | --- | --- | --- | --- |
| 1 | Visibility of system status | Final result is printed for every command; long pipeline ops lack interim progress lines | 2 | cli_run.png |
| 2 | Match between system and real world | Subcommands use plain language (`vault`, `analyze`, `tokens`) | 1 | cli_run.png |
| 3 | User control and freedom | No destructive defaults; clone/output land under git-ignored `runs/` | 1 | — |
| 4 | Consistency and standards | Standard argparse conventions (`-h`, `--version`, subcommands) | 0 | cli_run.png |
| 5 | Error prevention | Invalid subcommand is rejected before any work runs | 1 | — |
| 6 | Recognition rather than recall | The usage line lists every subcommand | 2 | cli_run.png |
| 7 | Flexibility and efficiency of use | Flags (`--version`, `--loop`) plus subcommands | 1 | — |
| 8 | Aesthetic and minimalist design | Terse output, one result per command | 1 | cli_run.png |
| 9 | Help users recognize/recover from errors | Invalid choice lists the valid options | 2 | cli_run.png |
| 10 | **Help and documentation** | **`--help` had no usage examples** (only the README did) | **3** | cli_run.png |

## Findings requiring action (severity >= 3)

- **H10 (severity 3):** `archlens --help` showed the bare usage line with no example invocations, so
  a first-time user could not see how to call a subcommand without leaving the terminal. **Fixed** in
  16.028 by adding an examples epilog and a fuller description to the parser; covered by
  `tests/test_cli_usability.py`.

## Before / after (16.029)

| State | Screenshot | What changed |
| --- | --- | --- |
| Before | `docs/screenshots/cli_run.png` | `--help` had only the usage line and a one-line description |
| After (**resolved**) | `docs/screenshots/cli_help_after.png` | `--help` now lists a fuller description and an `Examples:` block with runnable invocations |

All severity >= 3 findings (one: H10) are resolved.

## Accessibility (Guidelines §10.2 / §17.5)

Accessibility for a terminal-first tool plus its generated graphics:

| Concern | How ArchLens addresses it |
| --- | --- |
| **Plain-text, screen-reader friendly** | All CLI output is plain ASCII/UTF-8 text with no ANSI color codes, box-drawing, or cursor control, so it is read verbatim by screen readers and pipes/`> file` cleanly. Results are one labelled line per command (no spatial/columnar layout a reader would scramble). |
| **No color-only signalling** | Status is conveyed by words (`PASS`/`FAIL`, `OK`, exit codes), never by color alone, so the CLI is fully usable with no color perception. |
| **Color-blind-safe charts** | The analysis charts use Matplotlib's **viridis** perceptually-uniform, color-blind-safe colormap (`chart_factory.heatmap_chart`) and rely on position/shape (markers, bar height, axis labels) rather than hue to carry meaning; every figure has a title, axis labels, a legend, and a markdown caption (alt-text) where embedded. |
| **Operability / no time limits** | The CLI is non-interactive and imposes no input time limits; long operations can be re-run idempotently. |
| **Documentation** | Every screen/state is documented with a screenshot and a text description (above), and `--help` carries runnable examples (H10 fix), so the interface is learnable without sighted exploration. |

Known limitation: the embedded `.svg` architecture diagrams encode labels in `<foreignObject>` (mermaid
default); the byte-identical inline-mermaid sources in [`docs/PLAN.md`](PLAN.md) are the accessible,
GitHub-rendered fallback.
