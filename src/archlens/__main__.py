"""ArchLens console entry point — argparse only; every action delegates to the SDK."""

import argparse

from .sdk.sdk import ArchLensSDK


def _build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="archlens", description="ArchLens command line")
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
    sub.add_parser("analyze", help="run Repo->Graph->Analyst and print the analysis report")
    sub.add_parser("loop", help="run the improvement loop and print the result")
    sub.add_parser("tokens", help="print the token-savings report")
    return parser


def main(argv: list[str] | None = None, sdk=None) -> int:
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
    if args.command == "analyze":
        print(sdk.analyze())
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
