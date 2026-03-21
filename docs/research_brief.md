# Research Brief

## Problem

Regionalized LCA is valuable, but still difficult in day-to-day workflows because:

- place names and codes are inconsistent
- exact regional factors are often missing
- fallback assumptions are not always explicit
- many tools do not expose geography-resolution logic clearly

## Why this repository

`Regionalized-LCA-Adapter` is designed as a practical adapter layer that normalizes geographies, applies factor lookups, and records whether each match is exact or inherited.

## MVP scope

- geography alias normalization
- fallback chains
- example electricity and water-scarcity factors
- machine-readable adapted output

## Planned phase 2

- richer geocoding support
- province/state-level grids
- transport and logistics regionalization
- Brightway/openLCA adapters
- spatial metadata quality scoring
