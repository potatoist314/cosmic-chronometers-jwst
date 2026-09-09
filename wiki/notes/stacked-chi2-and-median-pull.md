---
title: Stacked χ², five stacking recipes and the per-feature pull
date: 2026-09-10
section: Analyses
tags: [dr2-quiescent-sample, ceridwen, diagnostics]
job: t_6417df23
figures: [stacked-pull.png, stacked-pull-recipes.png, stacked-pull-by-feature.png]
---

Sample
: 187 galaxies, `results/dr2-quiescent-new-defaults`
Rest-frame grid
: 2 Å bins, 1089 of 1526 bins carry ≥ 10 galaxies
Median per-galaxy reduced χ²
: 1.086, native pixels
Median stacked mean pull²
: 1.149, null expectation 1
Peak bin with ≥ 93 galaxies
: 3972 Å, mean pull² 2.46, 159 galaxies
Bootstrap
: 400 galaxy resamples, seed 20260909
Commit
: `34be307` · `origin/absorption-mask`

pull = (observed − posterior_q50) / effective_uncertainty, over the fitted native spectrum pixels. The script interpolates nothing and rescales no error.

<figure>
<img src="figures/dr2-quiescent-sample/stacked-pull.png" alt="Three panels: mean pull-squared with the null line at 1, median pull with a 16-84 percent band, and a reduced chi-squared histogram">
<figcaption><code>stacked-pull.png</code> · <code>scripts/plot_dr2_stacked_pull.py</code> · vector <code>stacked-pull.pdf</code></figcaption>
</figure>

<details>
<summary>Why the null line at 1 now means something</summary>

The previous version interpolated each spectrum onto the 2 Å grid and multiplied sigma by sqrt(2 / 0.32). Interpolation blends two neighbouring pixels. It does not average independent pixels, so it earns no reduction in noise. The rescaled sigma claimed an average that never happened. Mean pull² sat near 0.16 and the line at 1 meant nothing.

Every fitted native pixel now goes into the rest-frame bin that contains it. Mean pull² per native pixel is 1.149 against a per-galaxy reduced χ² of 1.086, so the two agree.

Two quantities carry different nulls.

- Mean pull² per bin averages pull² over all native pixels of all galaxies in the bin. Its null expectation is exactly 1 for any pixel-to-pixel noise correlation.
- Mean pull per bin averages a galaxy's own native pulls in the bin. Its null expectation is 0. Its null width depends on how strongly neighbouring pixels correlate.

LEGA-C samples one resolution element with about five pixels, so neighbouring pixels correlate and no fixed width applies. The width comes from a bootstrap over galaxies instead. Galaxies are independent objects, so that resample absorbs both the noise and the pixel correlation. The median 1σ is 0.065 for the mean recipe.

Wavelengths shift to rest frame, observed divided by 1+z, because template mismatch lives in rest frame. Sky-subtraction residuals live in observed frame and wash out in this stack.

</details>

<figure>
<img src="figures/dr2-quiescent-sample/stacked-pull-recipes.png" alt="Five stacked panels of mean pull against rest wavelength, one per stacking recipe, each with a grey bootstrap one-sigma band and shaded absorption windows">
<figcaption><code>stacked-pull-recipes.png</code> · <code>scripts/plot_dr2_stacked_pull.py</code> · vector <code>stacked-pull-recipes.pdf</code></figcaption>
</figure>

<details>
<summary>The five recipes</summary>

Five recipes stack the same per-galaxy bin averages.

1. Mean, equal weight for each galaxy.
2. Median, equal weight for each galaxy.
3. Inverse-variance weighted mean. The weight is n_pix / χ²_red for each galaxy and bin, the inverse of the estimated variance of that bin average.
4. Sigma-clipped mean, 3 sigma and 5 iterations, `astropy.stats.sigma_clipped_stats`.
5. Biweight location, Beers, Flynn & Gebhardt (1990), AJ 100, 32, `astropy.stats.biweight_location` with c = 6.

The five curves agree over the whole range. Maximum |stacked pull| by recipe:

- mean 1.32
- sigma-clipped mean 1.32
- inverse-variance mean 1.16
- median 0.95
- biweight location 0.92

The residual is coherent across galaxies, so no recipe averages the features away. The robust recipes only trim the most extreme bins.

Bins covered by fewer than MIN_COVER = 10 galaxies are NaN. The peak of mean pull² over all covered bins is 7.76 at 5566 Å, but only 10 galaxies reach that bin. Read the red edge with care.

</details>

| Window | N | Mean pull | Reading |
|---|---|---|---|
| Continuum | 187 | −0.022 ± 0.002 | — |
| Ca K | 151 | −0.149 ± 0.022 | model under-absorbs |
| Ca H+Hε | 165 | +0.245 ± 0.024 | model over-absorbs |
| Hδ | 184 | −0.124 ± 0.020 | model under-absorbs |
| G | 184 | +0.218 ± 0.021 | model over-absorbs |
| Hγ | 183 | +0.312 ± 0.019 | model over-absorbs |
| Fe4383 | 182 | +0.220 ± 0.022 | model over-absorbs |
| Hβ | 0 | masked in the fits | — |
| Mg b | 84 | −0.314 ± 0.035 | model under-absorbs |
| Fe5270 | 63 | −0.080 ± 0.042 | model under-absorbs |

<figure>
<img src="figures/dr2-quiescent-sample/stacked-pull-by-feature.png" alt="Points of stacked pull per absorption window and for the continuum, five recipes per window, with bootstrap error bars and a zero line">
<figcaption><code>stacked-pull-by-feature.png</code> · <code>scripts/plot_dr2_stacked_pull.py</code> · vector <code>stacked-pull-by-feature.pdf</code></figcaption>
</figure>

<details>
<summary>Windows, continuum and the masked Hβ</summary>

The table gives the mean recipe with its bootstrap 1σ. Every window sits far from the continuum level of −0.022. Mg b and Ca K run the most negative, so the model puts too little absorption there. Hγ, Ca H+Hε, G and Fe4383 run positive, so the model puts too much absorption there. All five recipes give the same value for each window inside the error bars.

The fits mask the rest-frame Hβ and [O III] regions, so the Hβ window holds no fitted pixel in any galaxy.

A feature window needs 5 fitted native pixels before a galaxy contributes to it. The continuum holds every fitted pixel between 2900 Å and 5950 Å that no window contains.

Grey columns on every rest-frame panel are the nine major absorption features at z = 0 (`scripts/spectral_figures.py`). The names sit under the bottom panel of each figure. The histogram carries no wavelength axis, so it stays bare.

</details>

```
ceridwen/.venv/bin/python scripts/plot_dr2_stacked_pull.py [--run-dir DIR] [--summary CSV] [--out-dir DIR] [--n-boot N]
ceridwen/.venv/bin/python -m pytest tests/test_stacked_pull.py -q
```

## Thread

**Q** 2026-09-04 · Mean pull-squared sits below 1. By roughly what factor are the effective uncertainties inflated, and did you check that against the per-galaxy reduced chi-squared?

**A** Roughly a factor of 2.5 in sigma, so about 6 in variance — the stacked baseline sits near 0.15–0.2 while the null line is at 1. And yes, I checked it against the histogram: median per-galaxy reduced chi-squared on native pixels is 1.12, so the fits themselves are fine. The depression comes almost entirely from the prescribed error scaling, since 2 Å bins over ~0.32 Å native pixels inflates sigma by sqrt(2/0.32) ≈ 2.5, while interpolation doesn't average independent pixels the way true rebinning would.
