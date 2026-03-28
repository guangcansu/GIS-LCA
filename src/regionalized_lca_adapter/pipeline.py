from __future__ import annotations

import csv
import json
from pathlib import Path
from typing import Any

from .adapter import adapt_row
from .factors import load_factor_table


def _load_tables(root: Path) -> tuple[dict, dict, dict]:
    electricity_table = load_factor_table(root / "data" / "electricity_factors.json")
    water_table = load_factor_table(root / "data" / "water_scarcity_factors.json")
    transport_table = load_factor_table(root / "data" / "transport_factors.json")
    return electricity_table, water_table, transport_table


def _summarise(adapted_rows: list[dict[str, Any]]) -> dict[str, Any]:
    total = len(adapted_rows)
    exact = sum(1 for r in adapted_rows if r["match_type"] == "exact")
    fallback = sum(1 for r in adapted_rows if r["match_type"] == "fallback")
    direct = sum(1 for r in adapted_rows if r["match_type"] == "direct")
    stub = sum(1 for r in adapted_rows if "stub" in (r["match_type"] or ""))
    na = sum(1 for r in adapted_rows if r["match_type"] == "not_applicable")

    # Aggregate adapted values by unit
    totals_by_unit: dict[str, float] = {}
    for row in adapted_rows:
        v = row.get("adapted_value")
        u = row.get("adapted_unit")
        if v is not None and u:
            totals_by_unit[u] = round(totals_by_unit.get(u, 0.0) + v, 6)

    return {
        "total_rows": total,
        "exact_matches": exact,
        "fallback_matches": fallback,
        "direct_emission_rows": direct,
        "transport_stub_rows": stub,
        "not_applicable_rows": na,
        "totals_by_unit": totals_by_unit,
    }


# ---------------------------------------------------------------------------
# Public API: adapt from CSV / JSON files (original interface, unchanged)    #
# ---------------------------------------------------------------------------

def adapt_inventory(metadata_path: str | Path, inventory_path: str | Path) -> dict[str, Any]:
    """Adapt an LCA inventory from CSV + metadata JSON files.

    This preserves the original CLI interface.
    """
    root = Path(__file__).resolve().parents[2]
    electricity_table, water_table, transport_table = _load_tables(root)

    with Path(metadata_path).open("r", encoding="utf-8") as handle:
        metadata = json.load(handle)

    with Path(inventory_path).open("r", encoding="utf-8", newline="") as handle:
        rows = list(csv.DictReader(handle))

    adapted_rows = [
        adapt_row(
            row=row,
            default_geography=metadata.get("geography", "GLO"),
            electricity_table=electricity_table,
            water_table=water_table,
            transport_table=transport_table,
        )
        for row in rows
    ]

    return {
        "metadata": metadata,
        "summary": _summarise(adapted_rows),
        "rows": adapted_rows,
    }


# ---------------------------------------------------------------------------
# Public API: adapt from a ProductInventory object                           #
# ---------------------------------------------------------------------------

def adapt_product_inventory(product_inventory: Any) -> dict[str, Any]:
    """Adapt a ProductInventory object and return a full result dict.

    Args:
        product_inventory: A ProductInventory instance (from products module).

    Returns:
        Dict with keys: metadata, summary, rows.

    Raises:
        ValueError: if ProductInventory.validate() returns errors.
    """
    errors = product_inventory.validate()
    if errors:
        raise ValueError("ProductInventory validation failed:\n" + "\n".join(errors))

    root = Path(__file__).resolve().parents[2]
    electricity_table, water_table, transport_table = _load_tables(root)

    raw_rows = product_inventory.to_inventory_rows()
    adapted_rows = [
        adapt_row(
            row=row,
            default_geography=product_inventory.geography,
            electricity_table=electricity_table,
            water_table=water_table,
            transport_table=transport_table,
        )
        for row in raw_rows
    ]

    return {
        "metadata": product_inventory.to_metadata_dict(),
        "summary": _summarise(adapted_rows),
        "rows": adapted_rows,
    }


# ---------------------------------------------------------------------------
# I/O helpers                                                                #
# ---------------------------------------------------------------------------

def save_json(data: dict[str, Any], output_path: str | Path) -> None:
    path = Path(output_path)
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8") as handle:
        json.dump(data, handle, indent=2, ensure_ascii=True)
        handle.write("\n")


def save_csv(data: dict[str, Any], output_path: str | Path) -> None:
    """Save adapted rows to CSV for easy inspection in spreadsheets.

    Extra fields that appear only in some rows are included in the header
    but left blank for rows that don't have them.
    """
    rows = data.get("rows", [])
    if not rows:
        return
    # Collect union of all keys to handle extra per-row fields
    fieldnames: list[str] = []
    seen: set[str] = set()
    for row in rows:
        for k in row:
            if k not in seen:
                fieldnames.append(k)
                seen.add(k)
    path = Path(output_path)
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames, extrasaction="ignore")
        writer.writeheader()
        writer.writerows(rows)


def render_summary(data: dict[str, Any]) -> str:
    meta = data["metadata"]
    summary = data["summary"]
    lines = [
        f"Study:            {meta.get('study_id', 'unknown')}",
        f"Product:          {meta.get('product', meta.get('product_system', 'unknown'))}",
        f"Functional unit:  {meta.get('functional_unit', '—')}",
        f"Geography:        {meta.get('geography', '—')}",
        "─" * 52,
        f"Rows adapted:     {summary['total_rows']}",
        f"  Exact matches:  {summary['exact_matches']}",
        f"  Fallback:       {summary['fallback_matches']}",
        f"  Direct emit:    {summary.get('direct_emission_rows', 0)}",
        f"  Transport stub: {summary.get('transport_stub_rows', 0)}",
        f"  Not applicable: {summary.get('not_applicable_rows', 0)}",
        "─" * 52,
        "Impact totals:",
    ]
    for unit, total in summary.get("totals_by_unit", {}).items():
        lines.append(f"  {total:.4f}  {unit}")
    return "\n".join(lines)
