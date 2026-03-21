from __future__ import annotations

import tempfile
import unittest
from pathlib import Path

from regionalized_lca_adapter.geography import fallback_chain, normalize_geography
from regionalized_lca_adapter.pipeline import adapt_inventory


class GeographyTests(unittest.TestCase):
    def test_normalize_geography(self) -> None:
        self.assertEqual(normalize_geography("China East"), "CN-EAST")
        self.assertEqual(normalize_geography("Illinois"), "US-IL")

    def test_fallback_chain(self) -> None:
        self.assertEqual(fallback_chain("CN-EAST"), ["CN-EAST", "CN", "GLO"])


class AdapterTests(unittest.TestCase):
    def test_adapt_inventory(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            tmp = Path(tmpdir)
            metadata = tmp / "meta.json"
            inventory = tmp / "inventory.csv"
            metadata.write_text('{"study_id":"demo","geography":"China East"}', encoding="utf-8")
            inventory.write_text(
                "process,activity_type,amount,unit,geography,notes\n"
                "forming,electricity_use,10,kWh,,demo\n"
                "cooling,water_use,2,m3,,demo\n",
                encoding="utf-8",
            )
            result = adapt_inventory(metadata, inventory)

        self.assertEqual(result["summary"]["total_rows"], 2)
        self.assertEqual(result["rows"][0]["factor_region_used"], "CN-EAST")
        self.assertGreater(result["rows"][0]["adapted_value"], 0)


if __name__ == "__main__":
    unittest.main()
