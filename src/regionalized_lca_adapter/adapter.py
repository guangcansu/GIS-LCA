from __future__ import annotations

from typing import Any

from .factors import lookup_factor
from .geography import normalize_geography


def adapt_row(
    row: dict[str, Any],
    default_geography: str,
    electricity_table: dict[str, Any],
    water_table: dict[str, Any],
) -> dict[str, Any]:
    raw_geography = row.get("geography") or default_geography
    geography = normalize_geography(raw_geography)
    activity_type = str(row["activity_type"]).strip()
    amount = float(row["amount"])
    unit = str(row["unit"]).strip()

    if activity_type == "electricity_use":
        factor = lookup_factor(electricity_table, geography)
        return {
            **row,
            "resolved_geography": geography,
            "factor_name": electricity_table["factor_name"],
            "factor_unit": electricity_table["unit"],
            "factor_value": factor["value"],
            "factor_region_used": factor["region_code"],
            "match_type": factor["match_type"],
            "adapted_value": round(amount * factor["value"], 6),
            "adapted_unit": "kg CO2-eq",
            "factor_source": factor["source"],
        }

    if activity_type == "water_use":
        factor = lookup_factor(water_table, geography)
        return {
            **row,
            "resolved_geography": geography,
            "factor_name": water_table["factor_name"],
            "factor_unit": water_table["unit"],
            "factor_value": factor["value"],
            "factor_region_used": factor["region_code"],
            "match_type": factor["match_type"],
            "adapted_value": round(amount * factor["value"], 6),
            "adapted_unit": "m3 world-eq",
            "factor_source": factor["source"],
        }

    return {
        **row,
        "resolved_geography": geography,
        "factor_name": None,
        "factor_unit": None,
        "factor_value": None,
        "factor_region_used": None,
        "match_type": "not_applicable",
        "adapted_value": None,
        "adapted_unit": None,
        "factor_source": None,
    }
