---
title: Stacked χ² and median pull
date: 2026-09-04
section: Analyses
tags: [dr2-quiescent-sample, ceridwen, diagnostics]
job: t_ee8ca17a
---

Sample
: 187 galaxies, DR2 quiescent full-spectrum fits

Covered bins
: 1084

Median reduced χ²
: 1.12

Peak bin
: 3672 Å, mean pull² 1.9, 77 galaxies

Commit
: `cb88302` · `origin/absorption-mask`

<figure>
<img src="figures/dr2-quiescent-sample/stacked-pull.png" alt="Three panels: stacked mean pull-squared, median pull, reduced chi-squared histogram">
<figcaption><code>stacked-pull.png</code> · <code>scripts/plot_dr2_stacked_pull.py</code> · vector <code>stacked-pull.pdf</code></figcaption>
</figure>

pull = (observed − posterior_q50) / effective_uncertainty, over fitted spectrum pixels.

Each spectrum shifts to rest frame (observed wavelength divided by 1+z) and regrids onto one common uniform rest-frame grid by linear interpolation. Regridded errors scale by the square root of the bin-width ratio: sigma_new = sigma_old * sqrt(dlambda_new / dlambda_native), with each galaxy's median native rest spacing. Galaxies carry equal weight. A bin counts as covered only where the interpolated fitted-pixel mask exceeds 0.5. Bins covered by fewer than MIN_COVER galaxies are set to NaN.

Mean pull-squared sits below 1 across rest wavelength. That reflects conservative effective errors, not overfitting.

```
.venv/bin/python scripts/plot_dr2_stacked_pull.py [--run-dir DIR] [--out-dir DIR]
.venv/bin/python -m pytest tests/test_stacked_pull.py -q
```

## Thread

**Q** 2026-09-04 · Mean pull-squared sits below 1. By roughly what factor are the effective uncertainties inflated, and did you check that against the per-galaxy reduced chi-squared?

**A** Roughly a factor of 2.5 in sigma, so about 6 in variance — the stacked baseline sits near 0.15–0.2 while the null line is at 1. And yes, I checked it against the histogram: median per-galaxy reduced chi-squared on native pixels is 1.12, so the fits themselves are fine. The depression comes almost entirely from the prescribed error scaling, since 2 Å bins over ~0.32 Å native pixels inflates sigma by sqrt(2/0.32) ≈ 2.5, while interpolation doesn't average independent pixels the way true rebinning would.
