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
