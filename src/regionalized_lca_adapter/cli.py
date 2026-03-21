from __future__ import annotations

import argparse

from .pipeline import adapt_inventory, render_summary, save_json


def _build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="regionalized-lca",
        description="Normalize geographies and apply regional factor lookups for LCA inventories.",
    )
    subparsers = parser.add_subparsers(dest="command", required=True)

    adapt = subparsers.add_parser("adapt", help="Adapt an inventory to region-specific factors.")
    adapt.add_argument("--metadata", required=True, help="Path to metadata JSON.")
    adapt.add_argument("--inventory", required=True, help="Path to inventory CSV.")
    adapt.add_argument("--output", help="Optional JSON output path.")

    return parser


def main() -> None:
    parser = _build_parser()
    args = parser.parse_args()

    if args.command == "adapt":
        data = adapt_inventory(args.metadata, args.inventory)
        print(render_summary(data))
        if args.output:
            save_json(data, args.output)
            print(f"Saved adapted inventory to {args.output}")
