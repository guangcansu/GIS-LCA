# Regionalized-LCA-Adapter

`Regionalized-LCA-Adapter` is a lightweight adapter layer for adding geography-aware logic to LCA inventories.

It focuses on a practical gap in many workflows:

- the inventory says where the system is,
- but the model still uses generic or mismatched regional factors,
- and the fallback logic is rarely explicit.

This repository makes those decisions visible and machine-readable.

## Paper

- Whitepaper: [paper/whitepaper.md](paper/whitepaper.md)
- Bibliography: [paper/references.bib](paper/references.bib)
- Citation metadata: [CITATION.cff](CITATION.cff)

## Features

- normalize geography labels into canonical region codes
- resolve fallback chains when exact regional factors are unavailable
- apply example regional electricity and water-scarcity factors
- report whether each factor was exact or inherited from a broader region
- export a machine-readable adapted inventory

## Repository layout

```text
Regionalized-LCA-Adapter/
├── CITATION.cff
├── data/
│   ├── electricity_factors.json
│   └── water_scarcity_factors.json
├── docs/
│   └── research_brief.md
├── examples/
│   ├── manufacturing_inventory.csv
│   └── manufacturing_metadata.json
├── paper/
│   ├── references.bib
│   └── whitepaper.md
├── src/regionalized_lca_adapter/
│   ├── __init__.py
│   ├── __main__.py
│   ├── adapter.py
│   ├── cli.py
│   ├── factors.py
│   ├── geography.py
│   └── pipeline.py
├── tests/
│   └── test_adapter.py
├── LICENSE
├── pyproject.toml
└── README.md
```

## Quick start

```bash
cd /Users/alex/Documents/Codex/Regionalized-LCA-Adapter
python3 -m venv .venv
source .venv/bin/activate
pip install -e .
```

Run the example:

```bash
regionalized-lca adapt \
  --metadata examples/manufacturing_metadata.json \
  --inventory examples/manufacturing_inventory.csv \
  --output examples/manufacturing_adapted.json
```

## Why this repo matters

Regionalization is essential for electricity, water, transport, exposure-dependent impacts, and many policy-facing applications. Yet in practice, regionalized LCA still struggles with:

- inconsistent place names
- incompatible metadata formats
- missing exact regional factors
- hidden fallback assumptions

This repository aims to make those steps explicit and auditable.

## Verification

```bash
cd /Users/alex/Documents/Codex/Regionalized-LCA-Adapter
PYTHONPATH=src python3 -m unittest discover -s tests -v
```

## License

MIT
