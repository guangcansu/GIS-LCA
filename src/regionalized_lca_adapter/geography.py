from __future__ import annotations

import re

# ---------------------------------------------------------------------------
# Alias map: normalised input label -> canonical region code
# ---------------------------------------------------------------------------
ALIASES: dict[str, str] = {
    # Global
    "glo": "GLO",
    "global": "GLO",
    "row": "GLO",
    "rest of world": "GLO",
    # China – national
    "china": "CN",
    "cn": "CN",
    "prc": "CN",
    "peoples republic of china": "CN",
    # China – macro-regions
    "china east": "CN-EAST",
    "cn-east": "CN-EAST",
    "east china": "CN-EAST",
    # China – provinces / municipalities
    "guangdong": "CN-GD",
    "cn-gd": "CN-GD",
    "guangzhou": "CN-GD",
    "shenzhen": "CN-GD",
    "jiangsu": "CN-JS",
    "cn-js": "CN-JS",
    "nanjing": "CN-JS",
    "suzhou": "CN-JS",
    "shanghai": "CN-SH",
    "cn-sh": "CN-SH",
    "beijing": "CN-BJ",
    "cn-bj": "CN-BJ",
    "shanxi": "CN-SX",
    "cn-sx": "CN-SX",
    "xinjiang": "CN-XJ",
    "cn-xj": "CN-XJ",
    "sichuan": "CN-SC",
    "cn-sc": "CN-SC",
    "chengdu": "CN-SC",
    "zhejiang": "CN-ZJ",
    "cn-zj": "CN-ZJ",
    "hangzhou": "CN-ZJ",
    # European Union
    "european union": "EU",
    "eu": "EU",
    "europe": "EU",
    # EU member states
    "germany": "DE",
    "deutschland": "DE",
    "de": "DE",
    "france": "FR",
    "fr": "FR",
    "netherlands": "NL",
    "nl": "NL",
    "belgium": "BE",
    "be": "BE",
    "spain": "ES",
    "es": "ES",
    "poland": "PL",
    "pl": "PL",
    "italy": "IT",
    "it": "IT",
    # United States – national
    "united states": "US",
    "us": "US",
    "usa": "US",
    "united states of america": "US",
    # United States – states
    "illinois": "US-IL",
    "us-il": "US-IL",
    "evanston il": "US-IL",
    "texas": "US-TX",
    "us-tx": "US-TX",
    "houston": "US-TX",
    "california": "US-CA",
    "us-ca": "US-CA",
    "los angeles": "US-CA",
    "san francisco": "US-CA",
    "new york": "US-NY",
    "us-ny": "US-NY",
    "ohio": "US-OH",
    "us-oh": "US-OH",
    # Other major economies
    "japan": "JP",
    "jp": "JP",
    "south korea": "KR",
    "korea": "KR",
    "kr": "KR",
    "india": "IN",
    "in": "IN",
    "brazil": "BR",
    "br": "BR",
    "australia": "AU",
    "au": "AU",
    "canada": "CA",
    "ca": "CA",
    "russia": "RU",
    "ru": "RU",
    "mexico": "MX",
    "mx": "MX",
    # Middle East / North Africa
    "saudi arabia": "SA",
    "sa": "SA",
    "ksa": "SA",
    "iran": "IR",
    "ir": "IR",
    "united arab emirates": "AE",
    "uae": "AE",
    "ae": "AE",
    # Southeast Asia
    "indonesia": "ID",
    "id": "ID",
    "malaysia": "MY",
    "my": "MY",
    "thailand": "TH",
    "th": "TH",
    "vietnam": "VN",
    "vn": "VN",
    # Africa
    "south africa": "ZA",
    "za": "ZA",
}

# ---------------------------------------------------------------------------
# Fallback chains: region_code -> ordered list of candidates (most specific first)
# ---------------------------------------------------------------------------
FALLBACKS: dict[str, list[str]] = {
    # China macro-regions -> CN -> GLO
    "CN-EAST": ["CN-EAST", "CN", "GLO"],
    # China provinces -> CN -> GLO
    "CN-GD": ["CN-GD", "CN", "GLO"],
    "CN-JS": ["CN-JS", "CN", "GLO"],
    "CN-SH": ["CN-SH", "CN", "GLO"],
    "CN-BJ": ["CN-BJ", "CN", "GLO"],
    "CN-SX": ["CN-SX", "CN", "GLO"],
    "CN-XJ": ["CN-XJ", "CN", "GLO"],
    "CN-SC": ["CN-SC", "CN", "GLO"],
    "CN-ZJ": ["CN-ZJ", "CN", "GLO"],
    "CN": ["CN", "GLO"],
    # EU member states -> EU -> GLO
    "EU": ["EU", "GLO"],
    "DE": ["DE", "EU", "GLO"],
    "FR": ["FR", "EU", "GLO"],
    "NL": ["NL", "EU", "GLO"],
    "BE": ["BE", "EU", "GLO"],
    "ES": ["ES", "EU", "GLO"],
    "PL": ["PL", "EU", "GLO"],
    "IT": ["IT", "EU", "GLO"],
    # US states -> US -> GLO
    "US": ["US", "GLO"],
    "US-IL": ["US-IL", "US", "GLO"],
    "US-TX": ["US-TX", "US", "GLO"],
    "US-CA": ["US-CA", "US", "GLO"],
    "US-NY": ["US-NY", "US", "GLO"],
    "US-OH": ["US-OH", "US", "GLO"],
    # Other countries -> GLO
    "JP": ["JP", "GLO"],
    "KR": ["KR", "GLO"],
    "IN": ["IN", "GLO"],
    "BR": ["BR", "GLO"],
    "AU": ["AU", "GLO"],
    "CA": ["CA", "GLO"],
    "RU": ["RU", "GLO"],
    "MX": ["MX", "GLO"],
    "SA": ["SA", "GLO"],
    "IR": ["IR", "GLO"],
    "AE": ["AE", "GLO"],
    "ID": ["ID", "GLO"],
    "MY": ["MY", "GLO"],
    "TH": ["TH", "GLO"],
    "VN": ["VN", "GLO"],
    "ZA": ["ZA", "GLO"],
    # Global baseline
    "GLO": ["GLO"],
}


def _clean(text: str | None) -> str:
    if not text:
        return ""
    text = text.strip().lower()
    text = re.sub(r"[^a-z0-9\- ]+", " ", text)
    return re.sub(r"\s+", " ", text).strip()


def normalize_geography(label: str | None) -> str:
    """Convert a free-text geography label to a canonical region code."""
    cleaned = _clean(label)
    return ALIASES.get(cleaned, cleaned.upper() if cleaned else "GLO")


def fallback_chain(region_code: str) -> list[str]:
    """Return the ordered fallback list for a region code."""
    return FALLBACKS.get(region_code, [region_code, "GLO"] if region_code else ["GLO"])


def list_known_regions() -> list[str]:
    """Return all canonical region codes that have an explicit fallback chain."""
    return sorted(FALLBACKS.keys())
