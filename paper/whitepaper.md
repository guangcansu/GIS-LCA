# GIS-LCA Whitepaper

## Title

**GIS-LCA: A Lightweight Geography and Fallback Layer for Regionalized Life Cycle Assessment**

## Series context

`GIS-LCA` is part of the **Open LCA Systems Series**, a coordinated set of open-source research repositories:

- `LCA-Harmonizer` for evidence cleanup and comparability
- `LCA-Uncertainty` for uncertainty propagation and confidence analysis
- `GIS-LCA` for geography-aware factor selection and fallback logic
- `LCA-Benchmark` for evaluating AI-assisted LCA workflows

Within that stack, `GIS-LCA` is the repository that asks what changes when the inventory is anchored to place rather than generic averages.

## Abstract

The environmental impacts of electricity, water consumption, transport, and emissions often depend strongly on location. However, practical regionalized LCA remains difficult because inventories and factors use inconsistent geographies, missing metadata, and hidden fallback assumptions. `GIS-LCA` is an open-source toolkit that normalizes geography labels, applies regional factor lookups, records fallback provenance, and exports machine-readable outputs. The project is intended as a bridge between generic inventories and more spatially explicit LCA workflows.

## Motivation

Regionalized LCA is increasingly recognized as necessary for robust decision-making, yet implementation barriers remain substantial. Researchers often know that location matters, but still lack lightweight tools that:

- normalize location labels into consistent region codes,
- reveal when exact factors are unavailable,
- make fallback assumptions transparent,
- and produce outputs that can be reused downstream.

This repository addresses that operational gap.

## Repository role in the series

The Open LCA Systems Series is intentionally modular:

- `LCA-Harmonizer` answers: *Is this evidence clean enough to use?*
- `LCA-Uncertainty` answers: *How stable is the result under uncertain inputs?*
- `GIS-LCA` answers: *What changes when geography matters?*
- `LCA-Benchmark` answers: *How should AI support for these tasks be evaluated?*

`GIS-LCA` is the layer that makes spatial assumptions explicit rather than implicit.

## Project introduction

`GIS-LCA` currently includes:

- geography normalization rules
- fallback-chain logic
- example regional factor libraries for electricity and water scarcity
- machine-readable adapted outputs with provenance

The implementation is deliberately simple so that it can be expanded later into richer spatial adapters or linked to GIS-backed workflows.

## Interfaces with sibling repositories

- `LCA-Harmonizer` can provide normalized system descriptors and cleaner geography metadata.
- `LCA-Uncertainty` can quantify the variability of region-specific factors and fallback assumptions.
- `LCA-Benchmark` can evaluate AI systems that recommend geography-dependent factors or datasets.

## Future work

- higher-resolution spatial coverage
- impact-category-specific adapters
- integration with dynamic electricity data
- direct import/export bridges for LCA software

## References

The bibliography for this project is maintained in [references.bib](references.bib).
