from __future__ import annotations

import argparse
import sys

from .pipeline import adapt_inventory, adapt_product_inventory, render_summary, save_csv, save_json
from .products import PRODUCT_REGISTRY
from .geography import list_known_regions


# ---------------------------------------------------------------------------
# Subcommand: adapt (original CSV/JSON workflow)                             #
# ---------------------------------------------------------------------------

def _cmd_adapt(args: argparse.Namespace) -> None:
    data = adapt_inventory(args.metadata, args.inventory)
    print(render_summary(data))
    if args.output:
        save_json(data, args.output)
        print(f"\nSaved JSON → {args.output}")
    if args.csv:
        save_csv(data, args.csv)
        print(f"Saved CSV  → {args.csv}")


# ---------------------------------------------------------------------------
# Subcommand: product (new MVP workflow)                                     #
# ---------------------------------------------------------------------------

def _cmd_product(args: argparse.Namespace) -> None:
    product_key = args.product.strip().lower()
    if product_key not in PRODUCT_REGISTRY:
        print(
            f"Error: unknown product '{product_key}'.\n"
            f"Available: {', '.join(sorted(PRODUCT_REGISTRY.keys()))}",
            file=sys.stderr,
        )
        sys.exit(1)

    geography = args.geography.strip() if args.geography else "GLO"
    inventory_fn = PRODUCT_REGISTRY[product_key]
    product_inv = inventory_fn(geography=geography)

    data = adapt_product_inventory(product_inv)
    print(render_summary(data))

    if args.output:
        save_json(data, args.output)
        print(f"\nSaved JSON → {args.output}")
    if args.csv:
        save_csv(data, args.csv)
        print(f"Saved CSV  → {args.csv}")


# ---------------------------------------------------------------------------
# Subcommand: products (list available products)                             #
# ---------------------------------------------------------------------------

def _cmd_products(_args: argparse.Namespace) -> None:
    print("Available products:")
    for key in sorted(PRODUCT_REGISTRY.keys()):
        inv = PRODUCT_REGISTRY[key]()
        print(f"  {key:<20} {inv.functional_unit:<18} {inv.description}")


# ---------------------------------------------------------------------------
# Subcommand: regions (list known region codes)                              #
# ---------------------------------------------------------------------------

def _cmd_regions(_args: argparse.Namespace) -> None:
    print("Known region codes (with explicit fallback chains):")
    for code in list_known_regions():
        print(f"  {code}")


# ---------------------------------------------------------------------------
# Argument parser                                                             #
# ---------------------------------------------------------------------------

def _build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="gis-lca",
        description=(
            "GIS-LCA: geography-aware life cycle assessment adapter.\n"
            "Normalizes geographies, applies regional factor lookups, "
            "and exposes auditable adapted inventories."
        ),
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=(
            "Examples:\n"
            "  gis-lca product bottled_water --geography 'China East'\n"
            "  gis-lca product methanol --geography Texas --output methanol_TX.json --csv methanol_TX.csv\n"
            "  gis-lca product sulfuric_acid --geography Germany\n"
            "  gis-lca products\n"
            "  gis-lca regions\n"
            "  gis-lca adapt --metadata meta.json --inventory inventory.csv\n"
        ),
    )
    subparsers = parser.add_subparsers(dest="command", required=True)

    # ---- adapt (legacy CSV interface) ----
    adapt = subparsers.add_parser(
        "adapt",
        help="Adapt an inventory CSV + metadata JSON to regional factors.",
    )
    adapt.add_argument("--metadata", required=True, help="Path to metadata JSON.")
    adapt.add_argument("--inventory", required=True, help="Path to inventory CSV.")
    adapt.add_argument("--output", help="Optional JSON output path.")
    adapt.add_argument("--csv", help="Optional CSV output path.")

    # ---- product (new MVP interface) ----
    product = subparsers.add_parser(
        "product",
        help="Run GIS-LCA on a built-in product model.",
    )
    product.add_argument(
        "product",
        help=f"Product key. Available: {', '.join(sorted(PRODUCT_REGISTRY.keys()))}",
    )
    product.add_argument(
        "--geography",
        default="GLO",
        help="Geography label for the product system (e.g. 'China East', 'Texas', 'DE'). Default: GLO",
    )
    product.add_argument("--output", help="Optional JSON output path.")
    product.add_argument("--csv", help="Optional CSV output path.")

    # ---- products (list) ----
    subparsers.add_parser("products", help="List all available built-in products.")

    # ---- regions (list) ----
    subparsers.add_parser("regions", help="List all known region codes.")

    return parser


# ---------------------------------------------------------------------------
# Entry point                                                                 #
# ---------------------------------------------------------------------------

def main() -> None:
    parser = _build_parser()
    args = parser.parse_args()

    dispatch = {
        "adapt": _cmd_adapt,
        "product": _cmd_product,
        "products": _cmd_products,
        "regions": _cmd_regions,
    }
    dispatch[args.command](args)


if __name__ == "__main__":
    main()
