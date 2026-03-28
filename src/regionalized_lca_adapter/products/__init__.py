"""Product inventory models for GIS-LCA MVP.

Phase-1 supported products:
- bottled_water   (1 L PET bottled water)
- methanol        (1 tonne methanol, natural-gas route)
- sulfuric_acid   (1 tonne H2SO4, contact process)

Each product module exposes a single function:
    get_inventory(geography: str) -> ProductInventory
"""

from .base import ProcessRow, ProductInventory
from .bottled_water import get_inventory as bottled_water_inventory
from .methanol import get_inventory as methanol_inventory
from .sulfuric_acid import get_inventory as sulfuric_acid_inventory

PRODUCT_REGISTRY: dict[str, callable] = {
    "bottled_water": bottled_water_inventory,
    "methanol": methanol_inventory,
    "sulfuric_acid": sulfuric_acid_inventory,
}

__all__ = [
    "ProcessRow",
    "ProductInventory",
    "PRODUCT_REGISTRY",
    "bottled_water_inventory",
    "methanol_inventory",
    "sulfuric_acid_inventory",
]
