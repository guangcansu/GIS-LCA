from __future__ import annotations

import re

ALIASES = {
    "glo": "GLO",
    "global": "GLO",
    "china": "CN",
    "cn": "CN",
    "china east": "CN-EAST",
    "cn-east": "CN-EAST",
    "european union": "EU",
    "eu": "EU",
    "united states": "US",
    "us": "US",
    "usa": "US",
    "illinois": "US-IL",
    "us-il": "US-IL",
    "evanston il": "US-IL",
}

FALLBACKS = {
    "CN-EAST": ["CN-EAST", "CN", "GLO"],
    "CN": ["CN", "GLO"],
    "EU": ["EU", "GLO"],
    "US-IL": ["US-IL", "US", "GLO"],
    "US": ["US", "GLO"],
    "GLO": ["GLO"],
}


def _clean(text: str | None) -> str:
    if not text:
        return ""
    text = text.strip().lower()
    text = re.sub(r"[^a-z0-9\- ]+", " ", text)
    return re.sub(r"\s+", " ", text).strip()


def normalize_geography(label: str | None) -> str:
    cleaned = _clean(label)
    return ALIASES.get(cleaned, cleaned.upper() if cleaned else "GLO")


def fallback_chain(region_code: str) -> list[str]:
    return FALLBACKS.get(region_code, [region_code, "GLO"] if region_code else ["GLO"])
