<p align="center">
  <img src="assets/logo.svg" alt="GIS-LCA logo" width="124">
</p>

# 🌐 GIS-LCA — Put LCA Back on the Map

[![Python](https://img.shields.io/badge/python-3.11+-blue.svg)](https://python.org)
[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)
[![Status](https://img.shields.io/badge/status-research%20prototype-orange.svg)](paper/whitepaper.md)

> **Because “where” can matter as much as “what” in life cycle assessment.**

Electricity, water, transport, and many impact pathways are deeply location-sensitive. But in practice, regional metadata are often fuzzy, inconsistent, or silently collapsed into generic averages.

**GIS-LCA** makes those geography decisions explicit. It normalizes place names, applies regional factor lookups, reveals fallback behavior, and turns location handling into something transparent and auditable.

---

## ✨ Key Features

| Feature | What it does |
|---------|--------------|
| Geography normalization | Converts labels like `China East`, `EU`, or `Illinois` into canonical region codes |
| Fallback logic | Falls back from subregion to country to global when exact factors are unavailable |
| Regional factor lookup | Applies example electricity and water-scarcity factors |
| Match provenance | Tells you whether a factor was exact or inherited |
| Machine-readable output | Saves an adapted inventory with region and factor metadata |

---

## 🚀 Quick Start

```bash
cd /Users/alex/Documents/Codex/GIS-LCA
python3 -m venv .venv
source .venv/bin/activate
pip install -e .
```

Run the example:

```bash
gis-lca adapt \
  --metadata examples/manufacturing_metadata.json \
  --inventory examples/manufacturing_inventory.csv \
  --output examples/manufacturing_adapted.json
```

---

## 🗺️ Why It Matters

Regionalized LCA often fails quietly, not loudly. The model runs, but:

- the geography label was ambiguous
- the exact regional factor was missing
- the workflow silently used a national average
- nobody recorded the fallback

This repository surfaces that hidden logic and makes it part of the output.

---

## 📦 Example Output

The adapter records:

- resolved geography code
- factor name and factor unit
- factor region actually used
- exact vs fallback match type
- adapted result value

Example file:

- [examples/manufacturing_adapted.json](examples/manufacturing_adapted.json)

---

## 📄 Paper

- Whitepaper: [paper/whitepaper.md](paper/whitepaper.md)
- Bibliography: [paper/references.bib](paper/references.bib)
- Citation metadata: [CITATION.cff](CITATION.cff)

The project is motivated by regionalized LCA literature and data-system challenges, including work by Mutel et al. (2019), UNEP GLAD, and Xu et al. (2025).

---

## 🌍 Included Demo Factors

- electricity climate factors
- water scarcity factors

The included factors are synthetic demo values so the adapter can run out of the box. They are meant as placeholders for future integration with real regional datasets and software bridges.

---

## 🗺️ Roadmap

- [x] Geography alias normalization
- [x] Fallback-chain logic
- [x] Regional electricity demo factors
- [x] Regional water-scarcity demo factors
- [ ] Province/state-level coverage expansion
- [ ] Transport regionalization
- [ ] Brightway/openLCA adapter layer
- [ ] Spatial metadata quality scoring

---

## 🔗 Best With

- `dynlca` for time-varying regional electricity workflows
- `LCA-Harmonizer` for upstream evidence cleanup
- future GIS-aware or policy-facing LCA studies

---

## ✅ Verification

```bash
cd /Users/alex/Documents/Codex/GIS-LCA
PYTHONPATH=src python3 -m unittest discover -s tests -v
```

---

## 📄 License

MIT
