from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from .geography import fallback_chain


def load_factor_table(path: str | Path) -> dict[str, Any]:
    with Path(path).open("r", encoding="utf-8") as handle:
        return json.load(handle)


def lookup_factor(table: dict[str, Any], region_code: str) -> dict[str, Any]:
    factors = table["factors"]
    for candidate in fallback_chain(region_code):
        if candidate in factors:
            return {
                "region_code": candidate,
                "value": factors[candidate]["value"],
                "source": factors[candidate]["source"],
                "match_type": "exact" if candidate == region_code else "fallback",
            }
    raise KeyError(f"No factor available for region {region_code}")
