---
title: M1_210210 refit with COSMOS2020 Classic and COSMOS2025 photometry
date: 2026-09-21
section: Analyses
theme: Single-fit accuracy
tags: [ceridwen, photometry, cosmos2020, cosmos2025, reference-galaxy]
job:
figures: [spectrum-cosmos2015-M1_210210.png, photometry-cosmos2015-M1_210210.png, spectrum-cosmos2020_classic-M1_210210.png, photometry-cosmos2020_classic-M1_210210.png, spectrum-cosmos2025-M1_210210.png, photometry-cosmos2025-M1_210210.png, corner-M1_210210.png, sfh-M1_210210.png]
---

<figure>
<img src="figures/cosmos-photometry-refit/spectrum-cosmos2015-M1_210210.png" alt="LEGA-C spectrum of M1_210210 with the joint Ceridwen posterior median and pull, COSMOS2015 reference, 12 bands fit">
<figcaption><code>spectrum-cosmos2015-M1_210210.png</code> · COSMOS2015 reference, 12 bands: LEGA-C M1_210210 spectrum over fitted pixels; joint Ceridwen posterior median and 16–84% band; lower-panel pull at fitted noise floor; shaded fitted-filter wavelength ranges</figcaption>
</figure>

<figure>
<img src="figures/cosmos-photometry-refit/photometry-cosmos2015-M1_210210.png" alt="Photometry of M1_210210 with the joint Ceridwen posterior median per band and pull, COSMOS2015 reference, 12 bands fit">
<figcaption><code>photometry-cosmos2015-M1_210210.png</code> · COSMOS2015 reference, 12 bands: M1_210210 observed total band fluxes ± fitted uncertainties; joint Ceridwen per-band posterior medians (16–84%); median model continuum; LEGA-C spectral range; band-name rail; lower-panel per-band pulls</figcaption>
</figure>

<figure>
<img src="figures/cosmos-photometry-refit/spectrum-cosmos2020_classic-M1_210210.png" alt="LEGA-C spectrum of M1_210210 with the joint Ceridwen posterior median and pull, COSMOS2020 Classic, 30 bands fit">
<figcaption><code>spectrum-cosmos2020_classic-M1_210210.png</code> · COSMOS2020 Classic, 30 bands: LEGA-C M1_210210 spectrum over fitted pixels; joint Ceridwen posterior median and 16–84% band; lower-panel pull at fitted noise floor; shaded fitted-filter wavelength ranges</figcaption>
</figure>

<figure>
<img src="figures/cosmos-photometry-refit/photometry-cosmos2020_classic-M1_210210.png" alt="Photometry of M1_210210 with the joint Ceridwen posterior median per band and pull, COSMOS2020 Classic, 30 bands fit">
<figcaption><code>photometry-cosmos2020_classic-M1_210210.png</code> · COSMOS2020 Classic, 30 bands: M1_210210 observed total band fluxes ± fitted uncertainties; joint Ceridwen per-band posterior medians (16–84%); median model continuum; LEGA-C spectral range; band-name rail; lower-panel per-band pulls</figcaption>
</figure>

<figure>
<img src="figures/cosmos-photometry-refit/spectrum-cosmos2025-M1_210210.png" alt="LEGA-C spectrum of M1_210210 with the joint Ceridwen posterior median and pull, COSMOS2025, 28 bands fit">
<figcaption><code>spectrum-cosmos2025-M1_210210.png</code> · COSMOS2025, 28 bands: LEGA-C M1_210210 spectrum over fitted pixels; joint Ceridwen posterior median and 16–84% band; lower-panel pull at fitted noise floor; shaded fitted-filter wavelength ranges</figcaption>
</figure>

<figure>
<img src="figures/cosmos-photometry-refit/photometry-cosmos2025-M1_210210.png" alt="Photometry of M1_210210 with the joint Ceridwen posterior median per band and pull, COSMOS2025, 28 bands fit">
<figcaption><code>photometry-cosmos2025-M1_210210.png</code> · COSMOS2025, 28 bands: M1_210210 observed total band fluxes ± fitted uncertainties; joint Ceridwen per-band posterior medians (16–84%); median model continuum; LEGA-C spectral range; band-name rail; lower-panel per-band pulls</figcaption>
</figure>

<figure>
<img src="figures/cosmos-photometry-refit/corner-M1_210210.png" alt="Corner plot of physical-parameter posteriors for the COSMOS2015, COSMOS2020 Classic and COSMOS2025 fits of M1_210210">
<figcaption><code>corner-M1_210210.png</code> · Physical-parameter posteriors with \(1\sigma\) contours for the COSMOS2015 reference, COSMOS2020 Classic and COSMOS2025 fits of M1_210210</figcaption>
</figure>

<figure>
<img src="figures/cosmos-photometry-refit/sfh-M1_210210.png" alt="Star-formation history and cumulative mass fraction for the three fits of M1_210210">
<figcaption><code>sfh-M1_210210.png</code> · Star-formation history with 16–84% band and cumulative mass fraction for the COSMOS2015 reference, COSMOS2020 Classic and COSMOS2025 fits of M1_210210</figcaption>
</figure>

<details>
<summary>Fits</summary>

Target
: M1_210210, \(z=0.6542\), seed 20260832

Reference
: COSMOS2015 `cosmos_total`, 12 bands · `results/m1-210210-reference/tau-1/poly10`

Arms
: `cosmos2020_classic`, 30 bands · `cosmos2025`, 28 bands · `results/cosmos-photometry-refit`

Totals
: `scripts/cosmos_photometry.py` · input comparison in note `cosmos-photometry-comparison`

Evaluation
: `results/cosmos-photometry-refit/analysis.ipynb`

Record
: experiment `e-cosmos-photometry-refit`

</details>

<details open>
<summary>Parameters</summary>

| Quantity | COSMOS2015 | COSMOS2020 Classic | COSMOS2025 |
| --- | --- | --- | --- |
| Photometry | COSMOS2015 `cosmos_total` | COSMOS2020 Classic | COSMOS2025 |
| Bands | 12 | 30 | 28 |
| Photometric \(\chi^2\) | 55.0 | 146.5 | 144.8 |
| Spectral \(\chi^2\), catalogue uncertainties | 10772.1 | 10880.6 | 10869.6 |
| Spectral \(\chi^2\) at the reference fit's floor | 3655.0 | 3694.0 | 3684.3 |
| \(\ln Z\) | 231153.16 ± 0.35 | 231476.73 ± 0.24 | 231426.50 ± 0.28 |
| \(\log_{10}(M_\star/M_\odot)\) | 11.650 ± 0.013 | 11.654 ± 0.011 | 11.597 ± 0.012 |
| \([\mathrm{Fe}/\mathrm{H}]\) | -0.159 ± 0.022 | -0.209 ± 0.024 | -0.201 ± 0.025 |
| \([\alpha/\mathrm{Fe}]\) | +0.060 ± 0.010 | +0.052 ± 0.010 | +0.051 ± 0.009 |
| \(\tau_{\mathrm{dust}}\) | 0.405 ± 0.013 | 0.407 ± 0.013 | 0.356 ± 0.013 |
| \(\delta_{\mathrm{dust}}\) | -0.987 ± 0.014 | -0.994 ± 0.007 | -0.994 ± 0.007 |
| \(t_{\mathrm{MW}}\) [Gyr] | 5.19 ± 0.12 | 5.12 ± 0.11 | 5.18 ± 0.13 |
| \(t_{20}\) [Gyr] | 3.77 ± 0.13 | 3.69 ± 0.11 | 3.75 ± 0.14 |
| \(t_{50}\) [Gyr] | 5.32 ± 0.17 | 5.25 ± 0.16 | 5.31 ± 0.17 |
| \(t_{80}\) [Gyr] | 6.67 ± 0.07 | 6.64 ± 0.07 | 6.66 ± 0.07 |
| \(f_{\mathrm{calib}}\) [%] | 2.52 ± 0.05 | 2.53 ± 0.05 | 2.54 ± 0.05 |
| \(z\) | 0.654219 ± 0.000015 | 0.654219 ± 0.000013 | 0.654220 ± 0.000015 |
| \(\sigma_\star\) [km/s] | 263.4 ± 3.1 | 267.1 ± 2.9 | 266.6 ± 3.2 |
| ESS | 4923 | 5499 | 5828 |
| Likelihood calls | 10 455 667 | 10 494 423 | 10 788 158 |
| Sampler wall time [s] | 1502 | 1025 | 1064 |
| Vast instance, spend | 51331110, $0.086 | 51958216, $0.180 for both |  |

</details>

<details>
<summary>Caveats</summary>

- \(\ln Z\) values are not comparable between fits: the photometric data differ, with 12, 30 and 28 bands.
- `cosmos2020_classic`: the sampler finished on the GPU; the notebook then stopped in the photometry figure on both attempts.
- `xerr` was negative for `hsc_i`: its `sedpy_jax` `red_edge` lies below `wave_eff`. Fixed in commit `066f614`.
- The executed notebook and `ceridwen_derived_outputs.h5` were regenerated on CPU from the stored posterior with `scripts/regenerate_fit_notebooks.py`; the sampler was not re-run.
- `cosmos2025`: attempt 1 was stopped by hand after 4 minutes so attempt 2 used the fixed notebook; same seed.
- COSMOS2025 has no zero-point offsets because none are published; its Milky Way extinction uses COSMOS2020 Classic \(E(B-V)=0.015\).
- One galaxy. The 5% error floor sets the photometric uncertainty in most bands.
- Liu Hao raised the price cap to $0.21/h for this rental only on 2026-09-21; the rule stays $0.11/h.

</details>
