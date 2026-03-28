"""Base data models for product inventory in GIS-LCA MVP."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any


@dataclass
class ProcessRow:
    """One row in the product LCI (life-cycle inventory).

    Fields:
        process:        Human-readable process name (e.g. "water extraction").
        activity_type:  Machine-readable type used for factor dispatch:
                        'electricity_use' | 'water_use' | 'transport' | 'direct_emission'
        amount:         Numerical quantity.
        unit:           Physical unit of amount (kWh, m3, tonne-km, kg CO2-eq, ...).
        geography:      Optional override geography for this row; if None the
                        product-level geography is used.
        notes:          Free-text annotation for auditing.
        supplier_site:  Optional label for the supplier or site name (informational).
        extra:          Catch-all dict for future fields without breaking old code.
    """

    process: str
    activity_type: str
    amount: float
    unit: str
    geography: str | None = None
    notes: str = ""
    supplier_site: str | None = None
    extra: dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> dict[str, Any]:
        d: dict[str, Any] = {
            "process": self.process,
            "activity_type": self.activity_type,
            "amount": self.amount,
            "unit": self.unit,
            "geography": self.geography or "",
            "notes": self.notes,
            "supplier_site": self.supplier_site or "",
        }
        d.update(self.extra)
        return d


@dataclass
class ProductInventory:
    """Top-level container for a single product LCA study.

    Fields:
        product:        Short product identifier (e.g. "bottled_water").
        description:    Human-readable name and scope.
        functional_unit: What the study is per (e.g. "1 L").
        geography:      Default geography for the whole product system.
        supplier_site:  Optional label for the main production site.
        rows:           Ordered list of ProcessRow objects.
        notes:          Free-text annotation.
        references:     List of data sources cited in the inventory.
    """

    product: str
    description: str
    functional_unit: str
    geography: str
    rows: list[ProcessRow] = field(default_factory=list)
    supplier_site: str | None = None
    notes: str = ""
    references: list[str] = field(default_factory=list)

    # ------------------------------------------------------------------ #
    # Serialisation helpers                                                 #
    # ------------------------------------------------------------------ #

    def to_metadata_dict(self) -> dict[str, Any]:
        return {
            "study_id": f"{self.product}_gis_lca",
            "product": self.product,
            "description": self.description,
            "functional_unit": self.functional_unit,
            "geography": self.geography,
            "supplier_site": self.supplier_site or "",
            "notes": self.notes,
            "references": self.references,
        }

    def to_inventory_rows(self) -> list[dict[str, Any]]:
        return [r.to_dict() for r in self.rows]

    def validate(self) -> list[str]:
        """Return list of validation errors (empty = OK)."""
        errors: list[str] = []
        allowed_types = {"electricity_use", "water_use", "transport", "direct_emission"}
        for i, row in enumerate(self.rows):
            if not row.process.strip():
                errors.append(f"Row {i}: 'process' must not be empty.")
            if row.activity_type not in allowed_types:
                errors.append(
                    f"Row {i} ({row.process!r}): unknown activity_type {row.activity_type!r}. "
                    f"Allowed: {sorted(allowed_types)}"
                )
            if row.amount <= 0:
                errors.append(f"Row {i} ({row.process!r}): amount must be > 0, got {row.amount}.")
            if not row.unit.strip():
                errors.append(f"Row {i} ({row.process!r}): 'unit' must not be empty.")
        if not self.geography.strip():
            errors.append("ProductInventory: 'geography' must not be empty.")
        return errors
