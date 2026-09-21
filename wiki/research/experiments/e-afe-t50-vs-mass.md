---
kind: experiment
id: e-afe-t50-vs-mass
title: \([\alpha/\mathrm{Fe}]\) and \(t_{50}\) against stellar mass, bulk DR2 fit
date: 2026-09-21
origin: new
status: results-ready
question: q-population-results
follow_up:
---

## Context

The most recent bulk fit, `results/dr2-quiescent-new-defaults`, contains 187 quiescent LEGA-C DR2 galaxies fitted during 2026-09-07–2026-09-10 with code `eb6ebc6`. Roadmap priority: `alpha-fe-t50-vs-mass`.

## Before delegation

```json
[
  {
    "date": "2026-09-21",
    "text": "can you add a plot of [alpha/fe] and t50 against log stellar mass for the most recent bulk dr2 fit (these are with older settings - do note what settings are old)"
  }
]
```

## Execution plan

Plot \([\alpha/\mathrm{Fe}]\) and \(t_{50}\) against \(\log_{10}(M_\star/M_\odot)\) from `results/dr2-quiescent-new-defaults-summary.csv`, without new sampling, using `scripts/plot_dr2_afe_t50_vs_mass.py`.

Output `wiki/analyses/dr2-quiescent-sample/afe-t50-vs-mass.png`: two panels sharing mass, per-galaxy posterior medians with 16–84% bars on both axes, and orange medians of posterior medians in 10 equal-count mass bins.

## Amendments

```json
[
  {
    "date": "2026-09-21",
    "text": "let me approve the plot first then add it to the checkin"
  }
]
```

## Runs

```json
[
  {
    "id": "dr2-new-defaults-bulk",
    "arm": "bulk-dr2-older-settings",
    "status": "complete",
    "config": "results/dr2-quiescent-new-defaults/shard_0_manifest.json",
    "code": "eb6ebc6",
    "model": "C3K v2.3 high-res (c3k_hr), MIST v2.5 alpha-variable isochrones, Kroupa (2001) IMF, grid schema 2.1",
    "data": "results/dr2-quiescent-new-defaults/targets.json",
    "seed": 20260830,
    "seed_rule": "20260830 + manifest_index per target",
    "artifacts": [
      {
        "label": "Population notebook",
        "path": "results/dr2-quiescent-new-defaults/ceridwen_new_defaults_comparison.ipynb"
      },
      {
        "label": "Second shard manifest",
        "path": "results/dr2-quiescent-new-defaults/shard_1_manifest.json"
      },
      {
        "label": "Summary table",
        "path": "results/dr2-quiescent-new-defaults-summary.csv"
      },
      {
        "label": "Plot script",
        "path": "scripts/plot_dr2_afe_t50_vs_mass.py"
      }
    ]
  }
]
```

## Figures

```json
[
  {
    "path": "wiki/analyses/dr2-quiescent-sample/afe-t50-vs-mass.png",
    "view": "Posteriors",
    "target": "",
    "caption": "\\([\\alpha/\\mathrm{Fe}]\\) and \\(t_{50}\\) versus stellar mass; shading lies outside the \\(\\mathrm{Uniform}(-0.2,0.6)\\) abundance prior; dotted lines mark 3 and 5 Gyr SFH bin edges."
  }
]
```

## Results

Spearman correlations with log mass are \(-0.49\) (\(p=10^{-12}\)) for \([\alpha/\mathrm{Fe}]\) and \(+0.17\) (\(p=0.018\)) for \(t_{50}\). Lowest/highest mass-bin medians are respectively \(\log_{10}(M_\star/M_\odot)=10.90/11.78\), \([\alpha/\mathrm{Fe}]=+0.05/-0.12\), and \(t_{50}=4.05/5.18\,\mathrm{Gyr}\).

Of 187 \([\alpha/\mathrm{Fe}]\) medians, 22 lie within \(0.02\,\mathrm{dex}\) of prior edges: 20 near \(-0.2\), two near \(0.6\). Eighteen \(t_{50}\) medians occupy \(3.00\)–\(3.25\,\mathrm{Gyr}\). \(t_{50}\) is lookback time from observation before which 50% of stellar mass formed.

Source: [summary table](results/dr2-quiescent-new-defaults-summary.csv), [plot script](scripts/plot_dr2_afe_t50_vs_mass.py).

## Caveats

Fit settings versus current notebook defaults: calibration order 3 versus 10; \(\tau_{\rm dust}\sim\mathrm{Uniform}(0,2)\) versus \(\mathrm{Uniform}(0,1)\); \(z\) fixed at \(z_{\rm cat}\) versus free within \(z_{\rm cat}\pm0.1\); \(\sigma_\star\) fixed at DR2 versus free within DR2 \(\pm3\,\mathrm{err}\). Photometry, masks, SFH prior and sampler are identical.

## References

- [Roadmap priority 8](wiki/research/direction.md)
- [e-dr2-revised](wiki/research/experiments/e-dr2-revised.md)
- [Current settings cell](notebooks/ceridwen_integrated_photometry_spectra.ipynb)
- [dr2-quiescent-sample · source note](wiki/notes/dr2-quiescent-sample.md)

## Your interpretation

```json
[]
```

## Next decision

```json
[]
```
