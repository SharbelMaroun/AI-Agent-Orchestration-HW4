"""Thin ArchLens CLI shim — delegates to archlens.__main__ (zero business logic)."""

from archlens.__main__ import main

if __name__ == "__main__":
    raise SystemExit(main())
