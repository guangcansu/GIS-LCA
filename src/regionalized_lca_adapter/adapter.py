from __future__ import annotations

from typing import Any

from .factors import lookup_factor
from .geography import normalize_geography

# ---------------------------------------------------------------------------
# Sentinel for transport: Phase 2 will resolve mode + distance + region.
# ---------------------------------------------------------------------------
_TRANSPORT_STUB_NOTE = (
    "transport_factor is a Phase-2 stub. "
    "Row recorded with geography only; no adapted_value computed yet."
)


def adapt_row(
    row: dict[str, Any],
    default_geography: str,
    electricity_table: dict[str, Any],
    water_table: dict[str, Any],
    transport_table: dict[str, Any] | None = None,
) -> dict[str, Any]:
    """Adapt a single inventory row by resolving geography and applying regional factors.

    Supported activity_type values:
      - electricity_use  → applies grid_climate_factor (kg CO2-eq / kWh)
      - water_use        → applies water_scarcity_factor (m3 world-eq / m3)
      - transport        → STUB: recorded but not adapted until Phase 2
      - direct_emission  → passed through as-is (amount already in impact units)

    All other types are marked 'not_applicable'.

    Args:
        row:               Dict with at minimum 'activity_type', 'amount', 'unit'.
        default_geography: Product-level geography used when row has no geography.
        electricity_table: Loaded JSON factor table for electricity.
        water_table:       Loaded JSON factor table for water scarcity.
        transport_table:   Loaded JSON factor table for transport (optional stub).

    Returns:
        Enriched dict with audit columns appended.
    """
    raw_geography = row.get("geography") or default_geography
    geography = normalize_geography(raw_geography)
    activity_type = str(row.get("activity_type", "")).strip()
    amount = float(row.get("amount", 0))
    unit = str(row.get("unit", "")).strip()

    # ------------------------------------------------------------------ #
    # Electricity                                                           #
    # ------------------------------------------------------------------ #
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

    # ------------------------------------------------------------------ #
    # Water                                                                 #
    # ------------------------------------------------------------------ #
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

    # ------------------------------------------------------------------ #
    # Transport (Phase-2 stub)                                              #
    # ------------------------------------------------------------------ #
    if activity_type == "transport":
        return {
            **row,
            "resolved_geography": geography,
            "factor_name": "transport_climate_factor",
            "factor_unit": "kg CO2-eq/tonne-km",
            "factor_value": None,
            "factor_region_used": None,
            "match_type": "not_adapted_phase2_stub",
            "adapted_value": None,
            "adapted_unit": None,
            "factor_source": _TRANSPORT_STUB_NOTE,
        }

    # ------------------------------------------------------------------ #
    # Direct emission (already in impact units, pass through)              #
    # ------------------------------------------------------------------ #
    if activity_type == "direct_emission":
        return {
            **row,
            "resolved_geography": geography,
            "factor_name": "direct_emission",
            "factor_unit": unit,
            "factor_value": 1.0,
            "factor_region_used": "N/A",
            "match_type": "direct",
            "adapted_value": round(amount, 6),
            "adapted_unit": unit,
            "factor_source": row.get("notes", "direct process emission"),
        }

    # ------------------------------------------------------------------ #
    # Unknown activity type                                                 #
    # ------------------------------------------------------------------ #
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
