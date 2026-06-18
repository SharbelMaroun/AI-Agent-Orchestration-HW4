"""ArchLens console entry point — argparse only; every action delegates to the SDK."""

import argparse

from .repo_picker import pick_repo
from .sdk.sdk import ArchLensSDK
from .shared.dotenv import load_dotenv
from .shared.errors import RepoError

_EXAMPLES = """Examples:
  uv run python src/main.py start          # pick a repo, clone it, then analyze
  uv run python src/main.py --version
  uv run python src/main.py vault runs/run/target/graphify-out/graph.json
  uv run python src/main.py deliverables --graph graph.json --src src --prd docs/PRD.md
  uv run python src/main.py analyze
  uv run python src/main.py tokens
  uv run python src/main.py debug-demo
  uv run python src/main.py submission-demo
"""


def run_start(sdk, input_fn=input, output_fn=print) -> int:
    """Interactive entry: pick a repo (suggested or a URL), clone it, report, then analyze it."""
    url = pick_repo(sdk.suggested_repos(), input_fn, output_fn)
    if not url:
        output_fn("No valid choice — nothing to clone.")
        return 1
    output_fn(f"Cloning {url} ...")
    try:
        path = sdk.clone_url(url)
    except (RepoError, ValueError) as exc:
        output_fn(f"Could not clone {url}: {exc}")
        return 1
    output_fn(f"Cloned to {path}. Building the graph and analyzing ...")
    sdk.reset_run_state()
    output_fn(str(sdk.analyze(repo_path=str(path))))
    return 0


def _build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="archlens",
        description="ArchLens — multi-agent, graph-based reverse engineering of Python codebases.",
        epilog=_EXAMPLES, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--version", action="store_true", help="print the ArchLens version")
    parser.add_argument("--loop", action="store_true", help="run the Phase 11 improvement loop")
    sub = parser.add_subparsers(dest="command")
    vault = sub.add_parser("vault", help="build the Obsidian vault from a graph.json")
    vault.add_argument("graph", help="path to a Graphify graph.json")
    deliv = sub.add_parser("deliverables", help="generate reverse-engineering deliverables")
    deliv.add_argument("--graph", default="graphify-out/graph.json", help="canonical graph.json")
    deliv.add_argument("--src", default="src", help="target source root for the class schema")
    deliv.add_argument("--prd", default="docs/PRD.md", help="PRD markdown for the alignment audit")
    deliv.add_argument("--out", default=None, help="output directory (defaults to config)")
    sub.add_parser("start", help="interactively pick a repo, clone it, then analyze it")
    sub.add_parser("analyze", help="run Repo->Graph->Analyst and print the analysis report")
    sub.add_parser("debug-demo", help="run the EX04 graph-guided bug-localization demo")
    sub.add_parser("submission-demo", help="print the full EX04 submission evidence summary")
    sub.add_parser("loop", help="run the improvement loop and print the result")
    sub.add_parser("tokens", help="print the token-savings report")
    return parser


def main(argv: list[str] | None = None, sdk=None) -> int:
    load_dotenv()  # read .env so a pasted API key enables live LLM mode without extra flags
    args = _build_parser().parse_args(argv)
    sdk = sdk or ArchLensSDK()
    if args.version:
        print(sdk.version())
        return 0
    if args.loop:
        print(sdk.run_improvement_loop())
        return 0
    if args.command == "vault":
        print(sdk.build_vault(args.graph).root)
        return 0
    if args.command == "deliverables":
        for path in sdk.generate_deliverables(args.graph, args.src, args.prd, args.out):
            print(path)
        return 0
    if args.command == "start":
        return run_start(sdk)
    if args.command == "analyze":
        print(sdk.analyze())
        return 0
    if args.command == "debug-demo":
        print(sdk.debug_demo())
        return 0
    if args.command == "submission-demo":
        print(sdk.submission_demo())
        return 0
    if args.command == "loop":
        print(sdk.run_loop())
        return 0
    if args.command == "tokens":
        print(sdk.measure_tokens())
        return 0
    _build_parser().print_help()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
