"""Tests for GIS-LCA MVP product inventory models and pipeline.

Coverage:
  - Geography normalization (extended aliases)
  - Fallback chain behaviour
  - ProductInventory validation
  - All three Phase-1 products: bottled_water, methanol, sulfuric_acid
  - adapt_product_inventory(): exact match, fallback, direct_emission, transport stub
  - CLI-accessible products registry
"""

from __future__ import annotations

import unittest

from regionalized_lca_adapter.geography import fallback_chain, normalize_geography
from regionalized_lca_adapter.pipeline import adapt_product_inventory
from regionalized_lca_adapter.products import PRODUCT_REGISTRY
from regionalized_lca_adapter.products.base import ProcessRow, ProductInventory
from regionalized_lca_adapter.products.bottled_water import get_inventory as bw_inv
from regionalized_lca_adapter.products.methanol import get_inventory as me_inv
from regionalized_lca_adapter.products.sulfuric_acid import get_inventory as sa_inv


# ============================================================
# Geography normalization
# ============================================================

class TestGeographyNormalization(unittest.TestCase):

    def test_china_east(self):
        self.assertEqual(normalize_geography("China East"), "CN-EAST")

    def test_illinois(self):
        self.assertEqual(normalize_geography("Illinois"), "US-IL")

    def test_texas(self):
        self.assertEqual(normalize_geography("Texas"), "US-TX")

    def test_germany(self):
        self.assertEqual(normalize_geography("Germany"), "DE")

    def test_guangdong(self):
        self.assertEqual(normalize_geography("Guangdong"), "CN-GD")

    def test_shenzhen_city_alias(self):
        self.assertEqual(normalize_geography("Shenzhen"), "CN-GD")

    def test_france(self):
        self.assertEqual(normalize_geography("France"), "FR")

    def test_saudi_arabia(self):
        self.assertEqual(normalize_geography("Saudi Arabia"), "SA")

    def test_indonesia(self):
        self.assertEqual(normalize_geography("Indonesia"), "ID")

    def test_unknown_passthrough(self):
        # Unknown labels are upper-cased and passed through
        self.assertEqual(normalize_geography("XYZ-UNKNOWN"), "XYZ-UNKNOWN")

    def test_none_returns_glo(self):
        self.assertEqual(normalize_geography(None), "GLO")

    def test_empty_returns_glo(self):
        self.assertEqual(normalize_geography(""), "GLO")

    def test_case_insensitive(self):
        self.assertEqual(normalize_geography("CHINA EAST"), "CN-EAST")
        self.assertEqual(normalize_geography("china east"), "CN-EAST")


# ============================================================
# Fallback chain
# ============================================================

class TestFallbackChain(unittest.TestCase):

    def test_cn_east_chain(self):
        self.assertEqual(fallback_chain("CN-EAST"), ["CN-EAST", "CN", "GLO"])

    def test_cn_gd_chain(self):
        self.assertEqual(fallback_chain("CN-GD"), ["CN-GD", "CN", "GLO"])

    def test_us_tx_chain(self):
        self.assertEqual(fallback_chain("US-TX"), ["US-TX", "US", "GLO"])

    def test_de_chain(self):
        self.assertEqual(fallback_chain("DE"), ["DE", "EU", "GLO"])

    def test_fr_chain(self):
        self.assertEqual(fallback_chain("FR"), ["FR", "EU", "GLO"])

    def test_glo_chain(self):
        self.assertEqual(fallback_chain("GLO"), ["GLO"])

    def test_unknown_gets_glo_fallback(self):
        chain = fallback_chain("UNKNOWN-XYZ")
        self.assertIn("GLO", chain)


# ============================================================
# ProductInventory validation
# ============================================================

class TestProductInventoryValidation(unittest.TestCase):

    def test_valid_inventory_passes(self):
        inv = bw_inv("GLO")
        errors = inv.validate()
        self.assertEqual(errors, [])

    def test_invalid_activity_type_caught(self):
        inv = ProductInventory(
            product="test",
            description="test",
            functional_unit="1 unit",
            geography="GLO",
            rows=[
                ProcessRow(
                    process="bad_row",
                    activity_type="banana",  # invalid
                    amount=1.0,
                    unit="kWh",
                )
            ],
        )
        errors = inv.validate()
        self.assertTrue(any("banana" in e for e in errors))

    def test_zero_amount_caught(self):
        inv = ProductInventory(
            product="test",
            description="test",
            functional_unit="1 unit",
            geography="GLO",
            rows=[
                ProcessRow(
                    process="zero_row",
                    activity_type="electricity_use",
                    amount=0.0,  # invalid
                    unit="kWh",
                )
            ],
        )
        errors = inv.validate()
        self.assertTrue(any("amount" in e for e in errors))

    def test_empty_geography_caught(self):
        inv = ProductInventory(
            product="test",
            description="test",
            functional_unit="1 unit",
            geography="",  # invalid
        )
        errors = inv.validate()
        self.assertTrue(any("geography" in e for e in errors))


# ============================================================
# Bottled water
# ============================================================

class TestBottledWater(unittest.TestCase):

    def test_product_registry_key(self):
        self.assertIn("bottled_water", PRODUCT_REGISTRY)

    def test_inventory_rows_positive(self):
        inv = bw_inv("GLO")
        self.assertGreater(len(inv.rows), 0)
        for r in inv.rows:
            self.assertGreater(r.amount, 0)

    def test_adapt_china_east_exact_electricity(self):
        inv = bw_inv("China East")
        result = adapt_product_inventory(inv)
        elec_rows = [r for r in result["rows"] if r["activity_type"] == "electricity_use"]
        self.assertTrue(len(elec_rows) > 0)
        for r in elec_rows:
            self.assertEqual(r["resolved_geography"], "CN-EAST")
            self.assertEqual(r["match_type"], "exact")
            self.assertGreater(r["adapted_value"], 0)
            self.assertEqual(r["adapted_unit"], "kg CO2-eq")

    def test_adapt_glo_fallback_on_unknown_region(self):
        inv = bw_inv("XYZ-NOWHERE")
        result = adapt_product_inventory(inv)
        elec_rows = [r for r in result["rows"] if r["activity_type"] == "electricity_use"]
        for r in elec_rows:
            self.assertEqual(r["factor_region_used"], "GLO")
            self.assertEqual(r["match_type"], "fallback")

    def test_adapt_water_rows_present(self):
        inv = bw_inv("GLO")
        result = adapt_product_inventory(inv)
        water_rows = [r for r in result["rows"] if r["activity_type"] == "water_use"]
        self.assertTrue(len(water_rows) > 0)
        for r in water_rows:
            self.assertIsNotNone(r["adapted_value"])
            self.assertEqual(r["adapted_unit"], "m3 world-eq")

    def test_adapt_transport_stub(self):
        inv = bw_inv("GLO")
        result = adapt_product_inventory(inv)
        transport_rows = [r for r in result["rows"] if r["activity_type"] == "transport"]
        for r in transport_rows:
            self.assertIn("stub", r["match_type"])
            self.assertIsNone(r["adapted_value"])

    def test_adapt_direct_emission_passthrough(self):
        inv = bw_inv("GLO")
        result = adapt_product_inventory(inv)
        de_rows = [r for r in result["rows"] if r["activity_type"] == "direct_emission"]
        for r in de_rows:
            self.assertEqual(r["match_type"], "direct")
            self.assertIsNotNone(r["adapted_value"])

    def test_summary_totals_by_unit_present(self):
        inv = bw_inv("GLO")
        result = adapt_product_inventory(inv)
        totals = result["summary"]["totals_by_unit"]
        self.assertIn("kg CO2-eq", totals)
        self.assertIn("m3 world-eq", totals)

    def test_audit_columns_all_present(self):
        inv = bw_inv("GLO")
        result = adapt_product_inventory(inv)
        required_keys = {
            "resolved_geography", "factor_name", "factor_value",
            "factor_region_used", "match_type", "adapted_value", "factor_source",
        }
        for row in result["rows"]:
            for key in required_keys:
                self.assertIn(key, row, msg=f"Missing audit column '{key}' in row: {row}")


# ============================================================
# Methanol
# ============================================================

class TestMethanol(unittest.TestCase):

    def test_product_registry_key(self):
        self.assertIn("methanol", PRODUCT_REGISTRY)

    def test_texas_electricity_exact(self):
        inv = me_inv("Texas")
        result = adapt_product_inventory(inv)
        elec_rows = [r for r in result["rows"] if r["activity_type"] == "electricity_use"]
        self.assertTrue(len(elec_rows) > 0)
        for r in elec_rows:
            self.assertEqual(r["resolved_geography"], "US-TX")
            self.assertEqual(r["match_type"], "exact")

    def test_direct_emission_total_positive(self):
        inv = me_inv("GLO")
        result = adapt_product_inventory(inv)
        de_rows = [r for r in result["rows"] if r["activity_type"] == "direct_emission"]
        total_kg = sum(r["adapted_value"] for r in de_rows if r["adapted_value"])
        # 423 NG feedstock + 265 NG fuel = 688 kg CO2-eq minimum
        self.assertGreaterEqual(total_kg, 600.0)

    def test_france_lower_electricity_than_china(self):
        inv_fr = me_inv("France")
        inv_cn = me_inv("China")
        res_fr = adapt_product_inventory(inv_fr)
        res_cn = adapt_product_inventory(inv_cn)

        def elec_co2(result):
            return sum(
                r["adapted_value"]
                for r in result["rows"]
                if r["activity_type"] == "electricity_use" and r["adapted_value"]
            )

        self.assertLess(elec_co2(res_fr), elec_co2(res_cn))


# ============================================================
# Sulfuric acid
# ============================================================

class TestSulfuricAcid(unittest.TestCase):

    def test_product_registry_key(self):
        self.assertIn("sulfuric_acid", PRODUCT_REGISTRY)

    def test_germany_electricity_exact(self):
        inv = sa_inv("Germany")
        result = adapt_product_inventory(inv)
        elec_rows = [r for r in result["rows"] if r["activity_type"] == "electricity_use"]
        for r in elec_rows:
            self.assertEqual(r["resolved_geography"], "DE")
            self.assertEqual(r["match_type"], "exact")

    def test_de_falls_back_from_de_to_eu_if_de_missing(self):
        # This tests the fallback chain logic: DE -> EU -> GLO
        chain = fallback_chain("DE")
        self.assertEqual(chain[0], "DE")
        self.assertEqual(chain[1], "EU")
        self.assertEqual(chain[2], "GLO")

    def test_so2_direct_emission_row(self):
        inv = sa_inv("GLO")
        result = adapt_product_inventory(inv)
        so2_rows = [
            r for r in result["rows"]
            if r["activity_type"] == "direct_emission" and "so2" in r.get("process", "").lower()
        ]
        self.assertTrue(len(so2_rows) > 0)
        for r in so2_rows:
            self.assertEqual(r["match_type"], "direct")

    def test_south_africa_higher_electricity_than_france(self):
        inv_za = sa_inv("South Africa")
        inv_fr = sa_inv("France")
        res_za = adapt_product_inventory(inv_za)
        res_fr = adapt_product_inventory(inv_fr)

        def elec_co2(result):
            return sum(
                r["adapted_value"]
                for r in result["rows"]
                if r["activity_type"] == "electricity_use" and r["adapted_value"]
            )

        self.assertGreater(elec_co2(res_za), elec_co2(res_fr))


if __name__ == "__main__":
    unittest.main()
