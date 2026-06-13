"""ArchLens console entry point — argparse only; every action delegates to the SDK."""

import argparse

from archlens.sdk.sdk import ArchLensSDK


def _build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="archlens", description="ArchLens command line")
    parser.add_argument("--version", action="store_true", help="print the ArchLens version")
    sub = parser.add_subparsers(dest="command")
    vault = sub.add_parser("vault", help="build the Obsidian vault from a graph.json")
    vault.add_argument("graph", help="path to a Graphify graph.json")
    return parser


def main(argv: list[str] | None = None) -> int:
    args = _build_parser().parse_args(argv)
    if args.version:
        print(ArchLensSDK().version())
        return 0
    if args.command == "vault":
        layout = ArchLensSDK().build_vault(args.graph)
        print(layout.root)
        return 0
    _build_parser().print_help()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
