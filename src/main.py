"""Thin ArchLens CLI — argparse only; every action is delegated to the SDK."""

import argparse

from archlens.sdk.sdk import ArchLensSDK


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(prog="archlens", description="ArchLens command line")
    parser.add_argument("--version", action="store_true", help="print the ArchLens version")
    args = parser.parse_args(argv)
    if args.version:
        print(ArchLensSDK().version())
        return 0
    parser.print_help()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
