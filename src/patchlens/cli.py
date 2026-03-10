"""CLI entry point for patchlens."""

from __future__ import annotations

import argparse

from patchlens.formatters import format_details, format_summary
from patchlens.scanners import AptScanner, FlatpakScanner, SnapScanner
from patchlens.service import PatchLensService


def build_parser() -> argparse.ArgumentParser:
    """Build the command-line parser."""
    parser = argparse.ArgumentParser(
        prog="patchlens",
        description="Scan Linux sources for pending updates.",
    )
    subparsers = parser.add_subparsers(dest="command", required=True)

    scan_parser = subparsers.add_parser("scan", help="Scan update sources")
    scan_parser.add_argument(
        "--details",
        action="store_true",
        help="Show detailed package-level updates",
    )
    return parser


def main() -> int:
    """Run patchlens CLI."""
    parser = build_parser()
    args = parser.parse_args()

    if args.command != "scan":
        parser.print_help()
        return 1

    service = PatchLensService([AptScanner(), FlatpakScanner(), SnapScanner()])
    results = service.scan_all()

    if args.details:
        print(format_details(results))
    else:
        print(format_summary(results))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
