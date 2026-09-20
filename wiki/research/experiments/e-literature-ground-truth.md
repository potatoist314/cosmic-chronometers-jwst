---
kind: experiment
id: e-literature-ground-truth
title: Literature review of local and z~0.7 quiescent-galaxy measurements to compare against
date: 2026-09-21
origin: new
status: planned
question: q-external-validation
follow_up:
---

## Context

Literature review of candidate comparison samples on 2026-09-21. No catalogue data fetched, fits run or compute rented.

## Before delegation

```json
[
  {
    "date": "2026-09-21",
    "text": "so you know the output parameters, I don't have a good ground truth to compare against right now. And I think similar ground truth, so to speak, from the literature, also from SED fitting. I would kind of like to look at local elliptical galaxies or like local passive quiescent galaxies where these parameters are directly measured, and compare against those to see if I'm getting sensible output parameters. Do you know where I can find such results? Can you search online extensively for and do like a literature review?"
  }
]
```

## Execution plan

- Comparison: Ceridwen DR2 fit outputs against published values; comparisons not yet run.
- Baseline: `results/dr2-quiescent-new-defaults-summary.csv`, 187 galaxies.
- Data: local early types with index-based and full-spectrum measurements; direct measurements from dynamical and lensing masses, resolved-star SFHs and star-cluster integrated spectra; samples at \(z=0.4\)–\(0.8\).
- Per source: selection, redshift, parameters, method, abundance and IMF assumptions, catalogue access and definition differences.
- Each comparison tagged as a method test or as mixed with evolution.
- Output: wiki note `external-comparison-samples`.

## Amendments

```json
[]
```

## Runs

```json
[]
```

## Figures

```json
[]
```

## Measurements

## Results

- Same-object LEGA-C dynamical-mass tables: Cappellari (2023), Table 1, 3197 spectra; DR3 `LOG_MVIR`, 3100; van Houdt et al. (2021), 797.
- Same-object LEGA-C abundance and age tables: Bevacqua et al. (2023), 183; Bevacqua et al. (2024), 637, CDS; Borghi et al. (2022a), 140; Gallazzi et al. (2026), 552.
- `alf` values from Beverage et al. (2021, 2023) and Cheng et al. (2025) are published in figures only.
- Beverage et al. (2023): approximately 0.2 dex differences in \([\mathrm{Fe}/\mathrm{H}]\) and \([\mathrm{Mg}/\mathrm{H}]\) between DR2 and DR3 spectra of the same 65 galaxies; \([\mathrm{Mg}/\mathrm{Fe}]\) and age are consistent.
- Choi et al. (2014), Table 1: `alf` stack values at \(z=0.55\)–\(0.7\), independent of LEGA-C.

## Caveats

- Ceridwen reports formed mass, \([\mathrm{Fe}/\mathrm{H}]\) and mass-weighted age; most sources report surviving mass, total \([\mathrm{Z}/\mathrm{H}]\) and SSP-equivalent or light-weighted age.
- Comparisons at \(z\approx0\) include evolution since \(z=0.7\).
- Resolved-star SFHs exist only for M32 and a halo field of NGC 5128.

## References

- [external-comparison-samples](wiki/notes/external-comparison-samples.md)
- Roadmap task `literature-comparison`, [direction](wiki/research/direction.md)

## Your interpretation

```json
[]
```

## Next decision

```json
[]
```
