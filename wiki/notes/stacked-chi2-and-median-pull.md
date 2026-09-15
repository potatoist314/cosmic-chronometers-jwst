---
title: Stacked χ², five stacking recipes and the per-feature pull
display_title: Stacked \(\chi^2\), five stacking recipes and the per-feature pull
date: 2026-09-10
section: Analyses
theme: Population results
tags: [dr2-quiescent-sample, ceridwen, diagnostics]
job: t_6417df23
figures: [M11_216899-spectrum.png, M12_184916-spectrum.png, stacked-pull.png, stacked-pull-recipes.png, stacked-pull-by-feature.png]
---

Sample
: 187 galaxies, `results/dr2-quiescent-new-defaults`
Rest-frame grid
: 2 \(\text{\AA}\) bins, 1089 of 1526 bins carry ≥ 10 galaxies
Median per-galaxy reduced \(\chi^2\)
: 1.086, native pixels
Median stacked mean \(\mathrm{pull}^2\)
: 1.149, null expectation 1
Peak bin with ≥ 93 galaxies
: 3972 \(\text{\AA}\), mean \(\mathrm{pull}^2\) 2.46, 159 galaxies
Bootstrap
: 400 galaxy resamples, seed 20260909
Commit
: `c0b1841` · `origin/absorption-mask`

\(\mathrm{pull}=(\mathrm{observed}-\mathrm{posterior\_q50})/\mathrm{effective\_uncertainty}\), over the fitted native spectrum pixels. The script interpolates nothing and rescales no error.

<figure>
<img src="figures/dr2-quiescent-sample/stacked-pull.png" alt="Three panels: mean pull-squared with the null line at 1, median pull with a 16-84 percent band, and a reduced chi-squared histogram">
<figcaption><code>stacked-pull.png</code> · <code>scripts/plot_dr2_stacked_pull.py</code> · vector <code>stacked-pull.pdf</code></figcaption>
</figure>

<figure>
<img src="figures/dr2-quiescent-sample/M11_216899-spectrum.png" alt="M11_216899: saved revised spectrum, posterior fit and native-pixel pulls">
<figcaption><a href="/wiki/f/results/dr2-quiescent-new-defaults/216899-M11_216899/M11_216899_executed.ipynb">M11_216899</a>: revised fit; contributes 79% of summed \(\mathrm{pull}^2\) in the 3672 \(\text{\AA}\) rest-frame bin (about 6234 \(\text{\AA}\) observed).</figcaption>
</figure>

<figure>
<img src="figures/dr2-quiescent-sample/M12_184916-spectrum.png" alt="M12_184916: saved revised spectrum, posterior fit and native-pixel pulls">
<figcaption><a href="/wiki/f/results/dr2-quiescent-new-defaults/184916-M12_184916/M12_184916_executed.ipynb">M12_184916</a>: revised fit; contributes 86% of summed \(\mathrm{pull}^2\) in the 5566 \(\text{\AA}\) rest-frame bin (about 9348 \(\text{\AA}\) observed).</figcaption>
</figure>

<details>
<summary>Native-pixel stack</summary>
<div id="why-the-null-line-at-1-now-means-something"></div>

The earlier stack interpolated each spectrum onto a 2 \(\text{\AA}\) grid and multiplied \(\sigma\) by \(\sqrt{2/0.32}\). Mean \(\mathrm{pull}^2\) was near 0.16. The current stack bins native pixels without that rescaling.

Every fitted native pixel enters its rest-frame bin. Mean \(\mathrm{pull}^2\) is 1.149; median per-galaxy reduced \(\chi^2\) is 1.086.

Two quantities carry different nulls.

- Mean \(\mathrm{pull}^2\) per bin averages \(\mathrm{pull}^2\) over all native pixels of all galaxies in the bin. Its null expectation is exactly 1 for any pixel-to-pixel noise correlation.
- Mean pull per bin averages a galaxy's own native pulls in the bin. Its null expectation is 0. Its null width depends on how strongly neighbouring pixels correlate.

LEGA-C samples one resolution element with about five pixels, so neighbouring pixels correlate and no fixed width applies. The width comes from a bootstrap over galaxies instead. Galaxies are independent objects, so that resample absorbs both the noise and the pixel correlation. The median 1\(\sigma\) is 0.065 for the mean recipe.

\(\lambda_{\mathrm{rest}}=\lambda_{\mathrm{obs}}/(1+z)\).

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
3. Inverse-variance weighted mean. The weight is \(n_{\mathrm{pix}}/\chi^2_{\mathrm{red}}\) for each galaxy and bin, the inverse of the estimated variance of that bin average.
4. Sigma-clipped mean, 3 \(\sigma\) and 5 iterations, `astropy.stats.sigma_clipped_stats`.
5. Biweight location, Beers, Flynn & Gebhardt (1990), AJ 100, 32, `astropy.stats.biweight_location` with \(c=6\).

The five curves agree over the whole range. Maximum \(|\mathrm{stacked\ pull}|\) by recipe:

- mean 1.32
- \(\sigma\)-clipped mean 1.32
- inverse-variance mean 1.16
- median 0.95
- biweight location 0.92

The five recipes retain the absorption-feature residuals.

Bins covered by fewer than MIN_COVER = 10 galaxies are NaN. The peak of mean \(\mathrm{pull}^2\) over all covered bins is 7.76 at 5566 \(\text{\AA}\), but only 10 galaxies reach that bin.

</details>

| Window | N | Mean pull | Reading |
|---|---|---|---|
| Continuum | 187 | −0.022 \(\pm\) 0.002 | — |
| Ca K | 151 | −0.149 \(\pm\) 0.022 | model under-absorbs |
| Ca H+\(\mathrm{H}\epsilon\) | 165 | +0.245 \(\pm\) 0.024 | model over-absorbs |
| \(\mathrm{H}\delta\) | 184 | −0.124 \(\pm\) 0.020 | model under-absorbs |
| G | 184 | +0.218 \(\pm\) 0.021 | model over-absorbs |
| \(\mathrm{H}\gamma\) | 183 | +0.312 \(\pm\) 0.019 | model over-absorbs |
| Fe4383 | 182 | +0.220 \(\pm\) 0.022 | model over-absorbs |
| \(\mathrm{H}\beta\) | 0 | masked in the fits | — |
| Mg b | 84 | −0.314 \(\pm\) 0.035 | model under-absorbs |
| Fe5270 | 63 | −0.080 \(\pm\) 0.042 | model under-absorbs |

<figure>
<img src="figures/dr2-quiescent-sample/stacked-pull-by-feature.png" alt="Points of stacked pull per absorption window and for the continuum, five recipes per window, with bootstrap error bars and a zero line">
<figcaption><code>stacked-pull-by-feature.png</code> · <code>scripts/plot_dr2_stacked_pull.py</code> · vector <code>stacked-pull-by-feature.pdf</code></figcaption>
</figure>

<details>
<summary>Windows, continuum and the masked \(\mathrm{H}\beta\)</summary>
<div id="windows-continuum-and-the-masked-h"></div>

The table gives the mean recipe with its bootstrap 1\(\sigma\). Every window sits far from the continuum level of −0.022. Mg b and Ca K run the most negative, so the model puts too little absorption there. \(\mathrm{H}\gamma\), Ca H+\(\mathrm{H}\epsilon\), G and Fe4383 run positive, so the model puts too much absorption there. All five recipes give the same value for each window inside the error bars.

The fits mask the rest-frame \(\mathrm{H}\beta\) and [O III] regions, so the \(\mathrm{H}\beta\) window holds no fitted pixel in any galaxy.

A feature window needs 5 fitted native pixels before a galaxy contributes to it. The continuum holds every fitted pixel between 2900 \(\text{\AA}\) and 5950 \(\text{\AA}\) that no window contains.

Coloured columns on every rest-frame panel mark the nine major absorption features at \(z=0\) (`scripts/spectral_figures.py`). Each feature keeps its colour across panels; the names appear in one legend on the right. The histogram carries no wavelength axis, so it stays bare.

</details>

```
ceridwen/.venv/bin/python scripts/plot_dr2_stacked_pull.py [--run-dir DIR] [--summary CSV] [--out-dir DIR] [--n-boot N]
ceridwen/.venv/bin/python -m pytest tests/test_stacked_pull.py -q
```

## Thread

**Q** 2026-09-04 · Mean pull-squared sits below 1. By roughly what factor are the effective uncertainties inflated, and did you check that against the per-galaxy reduced chi-squared?

**A** The earlier stack multiplied \(\sigma\) by \(\sqrt{2/0.32}\), about 2.5, and had mean \(\mathrm{pull}^2\) near 0.15–0.2. Median per-galaxy reduced chi-squared on native pixels was 1.12. That stack interpolated pixels without independent averaging.
