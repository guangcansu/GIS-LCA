"""Product model: 1 tonne sulfuric acid (H2SO4, 98 wt%) via contact process.

Functional unit: 1 tonne H2SO4 (98 wt%) at plant gate.
System boundary: sulfur combustion -> SO2 oxidation (V2O5 catalyst) ->
                 absorption in oleum -> dilution to 98% -> storage.

LCI basis (per tonne H2SO4, 98%):
- Sulfur feedstock: 0.327 t elemental S/t H2SO4
  (stoichiometric: S + O2 -> SO2 -> SO3 + H2O -> H2SO4; molar ratio 32/98 * 1.03 loss)
- Electricity: 15.0 kWh/t  (Ecoinvent 3.9 'sulfuric acid production'; IHS 2019)
- Process water (dilution + cooling): 0.22 m3/t  (Ecoinvent 3.9)
- Direct SO2 fugitive emission: 0.28 kg SO2/t  (EU BREF 2017 BAT; modelled as kg CO2-eq via GWP100=0 but
  kept for future midpoint impact; we record it as direct_emission with unit kg SO2)
- Net energy: contact process is exothermic — steam EXPORT ~450 kg steam/t H2SO4;
  Phase 1 does not credit co-product steam (conservative boundary).
- Transport (sulfur rail/ship, ~500 km): 0.163 tonne-km/t  (stub Phase 2)

Notes:
- When sulfur is sourced from natural gas desulfurisation (Claus process byproduct),
  the upstream allocation for sulfur is near zero (it's a waste-derived feedstock).
  Phase 1 uses a generic sulfur factor placeholder.
- The process emits no CO2 directly; GHG comes entirely from electricity grid.
"""

from __future__ import annotations

from .base import ProcessRow, ProductInventory


def get_inventory(geography: str = "GLO") -> ProductInventory:
    """Return the Phase-1 LCI for 1 tonne H2SO4 (98%) at the given geography."""

    rows = [
        ProcessRow(
            process="contact_process_electricity",
            activity_type="electricity_use",
            amount=15.0,
            unit="kWh",
            notes="Fans, pumps, instrumentation; Ecoinvent 3.9 / IHS Markit 2019",
        ),
        ProcessRow(
            process="process_water_dilution_cooling",
            activity_type="water_use",
            amount=0.22,
            unit="m3",
            notes="Dilution water and cooling tower makeup; Ecoinvent 3.9",
        ),
        ProcessRow(
            process="fugitive_so2_emission",
            activity_type="direct_emission",
            amount=0.28,
            unit="kg SO2",
            notes=(
                "Fugitive SO2 stack emission (BAT-compliant contact process); "
                "EU BREF Inorganic Chemicals 2017. "
                "GWP100=0 but kept for acidification pathway in Phase 2."
            ),
        ),
        ProcessRow(
            process="sulfur_feedstock_transport",
            activity_type="transport",
            amount=0.163,
            unit="tonne-km",
            notes="Elemental S rail/ship ~500 km; 0.327 t S * 500 km; stub Phase 2",
        ),
    ]

    return ProductInventory(
        product="sulfuric_acid",
        description="1 tonne H2SO4 (98 wt%) via contact process, cradle-to-gate",
        functional_unit="1 tonne H2SO4 (98%)",
        geography=geography,
        supplier_site=None,
        notes=(
            "Contact process (double absorption). Steam export credit excluded (Phase 1). "
            "Sulfur feedstock upstream excluded (byproduct allocation boundary). "
            "SO2 emission tracked for acidification; GWP100 contribution is zero."
        ),
        references=[
            "Ecoinvent 3.9: sulfuric acid production, RER.",
            "EU BREF on Large Volume Inorganic Chemicals (2017), Section 4.3 BAT.",
            "IHS Markit (2019) Sulfuric Acid Process Economics Program.",
        ],
        rows=rows,
    )
