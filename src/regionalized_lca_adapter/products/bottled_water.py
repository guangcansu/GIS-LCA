"""Product model: 1 L PET bottled water.

Functional unit: 1 litre of PET-bottled still water delivered to point of sale.
System boundary: water extraction -> purification -> PET preform moulding ->
                 filling & capping -> labelling -> transport to warehouse.

LCI basis:
- Electricity for pumping, UV/ozone treatment, bottling line: ~0.21 kWh/L
  (Amienyo et al. 2013; Kendall & Diaconu 2007 range 0.16–0.27 kWh/L)
- Process water input (incl. rinse losses): ~1.35 L/L product
  (typical bottling line loss factor 1.2–1.5)
- Transport (full truck, ~200 km regional average): 0.000200 tonne-km / L
  [0.001 t product * 200 km = 0.20 tonne-km]
- Direct CO2-eq from boiler / small utilities: 0.0055 kg CO2-eq / L
  (Amienyo et al. 2013 Cradle-to-Gate ex-distribution)

Note: PET resin embodied carbon is NOT included in Phase 1
      (complex supply chain; flagged for Phase 2).
"""

from __future__ import annotations

from .base import ProcessRow, ProductInventory


def get_inventory(geography: str = "GLO") -> ProductInventory:
    """Return the Phase-1 LCI for 1 L bottled water at the given geography."""

    rows = [
        ProcessRow(
            process="water_extraction_and_pumping",
            activity_type="electricity_use",
            amount=0.045,
            unit="kWh",
            notes="Submersible pump electricity for spring/municipal intake; Amienyo 2013",
        ),
        ProcessRow(
            process="water_treatment_uv_ozone",
            activity_type="electricity_use",
            amount=0.035,
            unit="kWh",
            notes="UV + ozone purification; Kendall & Diaconu 2007",
        ),
        ProcessRow(
            process="bottling_line_electricity",
            activity_type="electricity_use",
            amount=0.110,
            unit="kWh",
            notes="PET preform stretch-blow, fill & cap, labeller; Amienyo 2013 range mid",
        ),
        ProcessRow(
            process="compressed_air_and_utilities",
            activity_type="electricity_use",
            amount=0.020,
            unit="kWh",
            notes="Compressed air, lighting, HVAC of bottling hall",
        ),
        ProcessRow(
            process="process_water_input",
            activity_type="water_use",
            amount=1.35,
            unit="m3",
            notes="Per 1000 L product (1.35 m3 / m3 product); includes rinse losses",
            extra={"amount_per_unit": "m3 per m3 product"},
        ),
        ProcessRow(
            process="outbound_transport_to_warehouse",
            activity_type="transport",
            amount=0.000200,
            unit="tonne-km",
            notes="200 km regional truck delivery; 1 L bottle ~1 kg gross; stub Phase 2",
        ),
        ProcessRow(
            process="direct_utilities_combustion",
            activity_type="direct_emission",
            amount=0.0055,
            unit="kg CO2-eq",
            notes="Small boiler / steam for label shrink; Amienyo 2013",
        ),
    ]

    return ProductInventory(
        product="bottled_water",
        description="1 L PET bottled still water, cradle-to-warehouse gate",
        functional_unit="1 litre",
        geography=geography,
        supplier_site=None,
        notes="Phase-1 MVP. PET resin embodied impact excluded (Phase 2).",
        references=[
            "Amienyo D et al. (2013) Life cycle environmental impacts of carbonated soft drinks. Int J LCA 18:77-92.",
            "Kendall A, Diaconu DC (2007) Life cycle of beverage container materials. UC Davis.",
            "Ecoinvent 3.9: market for water, deionised; tap water production.",
        ],
        rows=rows,
    )
