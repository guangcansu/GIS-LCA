"""Product model: 1 tonne methanol via steam methane reforming (SMR) route.

Functional unit: 1 tonne methanol (CH3OH) at plant gate.
System boundary: natural gas feed + fuel -> SMR + CO shift -> methanol synthesis ->
                 distillation -> storage/loading.

LCI basis (per tonne methanol):
- Electricity: 0.218 MWh/t  (Ecoinvent 3.9 'methanol production, from natural gas')
- Process water: 0.75 m3/t  (IEA 2019 methanol technology review)
- NG feedstock CO2: 423 kg CO2-eq/t  (Ecoinvent 3.9 SMR direct; GREET 2023)
- NG fuel CO2:  265 kg CO2-eq/t  (Ecoinvent 3.9)
- Transport feedstock (NG pipeline, 300 km): 0.030 tonne-km/t  (stub Phase 2)

Notes:
- Route = natural gas SMR only. Coal-based (methanol-to-olefins route common in CN)
  would yield ~3× higher GHG. Phase 2 should allow route selection.
- CCS option not modelled.
"""

from __future__ import annotations

from .base import ProcessRow, ProductInventory


def get_inventory(geography: str = "GLO") -> ProductInventory:
    """Return the Phase-1 LCI for 1 tonne methanol (SMR) at the given geography."""

    rows = [
        ProcessRow(
            process="smr_and_synthesis_electricity",
            activity_type="electricity_use",
            amount=218.0,
            unit="kWh",
            notes="Electricity for compressors, pumps, control systems; Ecoinvent 3.9",
        ),
        ProcessRow(
            process="process_water_boiler_feed",
            activity_type="water_use",
            amount=0.75,
            unit="m3",
            notes="Boiler feed water for steam generation; IEA Methanol Technology 2019",
        ),
        ProcessRow(
            process="natural_gas_feedstock_combustion_co2",
            activity_type="direct_emission",
            amount=423.0,
            unit="kg CO2-eq",
            notes="Direct CO2 from NG feedstock carbon in SMR reactor; GREET 2023 / Ecoinvent 3.9",
        ),
        ProcessRow(
            process="natural_gas_fuel_combustion_co2",
            activity_type="direct_emission",
            amount=265.0,
            unit="kg CO2-eq",
            notes="Direct CO2 from NG fuel burned for process heat; Ecoinvent 3.9",
        ),
        ProcessRow(
            process="ng_feedstock_pipeline_transport",
            activity_type="transport",
            amount=0.030,
            unit="tonne-km",
            notes="Pipeline transport of NG feedstock ~300 km; stub Phase 2",
        ),
    ]

    return ProductInventory(
        product="methanol",
        description="1 tonne methanol (CH3OH) via SMR route, cradle-to-gate",
        functional_unit="1 tonne methanol",
        geography=geography,
        supplier_site=None,
        notes=(
            "Route: natural gas SMR only. CN coal-based route excluded (Phase 2). "
            "GHG scope: direct emissions + electricity. Upstream NG extraction excluded Phase 1."
        ),
        references=[
            "Ecoinvent 3.9: methanol production, from natural gas, RER.",
            "IEA (2019) The Future of Hydrogen. Technology annex: methanol.",
            "GREET 2023: methanol pathway from NG.",
        ],
        rows=rows,
    )
