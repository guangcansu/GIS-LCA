from __future__ import annotations

import csv
import json
from pathlib import Path
from typing import Any

from .adapter import adapt_row
from .factors import load_factor_table


def adapt_inventory(metadata_path: str | Path, inventory_path: str | Path) -> dict[str, Any]:
    root = Path(__file__).resolve().parents[2]
    electricity_table = load_factor_table(root / "data" / "electricity_factors.json")
    water_table = load_factor_table(root / "data" / "water_scarcity_factors.json")

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
        )
        for row in rows
    ]

    return {
        "metadata": metadata,
        "summary": {
            "total_rows": len(adapted_rows),
            "exact_matches": len([row for row in adapted_rows if row["match_type"] == "exact"]),
            "fallback_matches": len([row for row in adapted_rows if row["match_type"] == "fallback"]),
        },
        "rows": adapted_rows,
    }


def save_json(data: dict[str, Any], output_path: str | Path) -> None:
    path = Path(output_path)
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8") as handle:
        json.dump(data, handle, indent=2, ensure_ascii=True)
        handle.write("\n")


def render_summary(data: dict[str, Any]) -> str:
    summary = data["summary"]
    return "\n".join(
        [
            f"Study: {data['metadata'].get('study_id', 'unknown')}",
            f"Rows adapted: {summary['total_rows']}",
            f"Exact matches: {summary['exact_matches']}",
            f"Fallback matches: {summary['fallback_matches']}",
        ]
    )
