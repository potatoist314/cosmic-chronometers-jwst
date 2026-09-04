---
title: DR2 quiescent sample
date: 2026-09-03
section: Analyses
tags: [dr2-quiescent-sample, ceridwen, figures]
job: t_d0d3a321
old: _old/analyses/dr2-quiescent-sample.html
---

Paper-quality figure set for the 187 LEGA-C DR2 quiescent full-spectrum Ceridwen fits: the age–redshift headline against Borghi+22, formation timescales, parameter distributions, and fit quality. Every plot renders from one tidy table, [results/dr2-quiescent-summary.csv](/wiki/f/results/dr2-quiescent-summary.csv).

### Headline: ages against redshift

<figure>
<img src="figures/dr2-quiescent-sample/headline-age-redshift.png" alt="Mass-weighted age against redshift for 187 galaxies with binned medians, plus a Ceridwen-minus-Borghi residual strip for the 68-galaxy overlap">
<figcaption>Top: mass-weighted age with 16–84 intervals for all 187 galaxies, coloured by velocity-dispersion group (split 215 km/s), with binned medians (NMAD/sqrt(N)). Bottom: Ceridwen minus Borghi+22 SSP age for the 68 overlap galaxies. Vector version: <code>headline-age-redshift.pdf</code>.</figcaption>
</figure>

`scripts/plot_dr2_headline_candidates.py:147-182` · `layout_b_single_with_residual`

### Formation timescale

tX is the lookback younger than which X% of the formed mass was made; Δt = t80−t20 is the 20th-to-80th mass-assembly interval. Median Δt is 2.46 Gyr, flat against mass, [α/Fe] and observed redshift; 65% of values sit at 2.2–2.7 Gyr because the 7-bin SFH (2-Gyr bins at 1–5 Gyr) quantises Δt, so treat values as resolution-limited.

<figure>
<img src="figures/dr2-quiescent-sample/dt-vs-formation-epoch.png" alt="Formation timescale against t50 lookback, Planck18 formation redshift, and observed redshift">
<figcaption>Δt against formation epoch (t50 lookback, Planck18 formation redshift from age(z_obs)−t50, observed redshift) with running medians.</figcaption>
</figure>

<figure>
<img src="figures/dr2-quiescent-sample/dt-vs-mass.png" alt="Formation timescale against stellar mass">
<figcaption>Δt against stellar mass. No trend (Spearman 0.00).</figcaption>
</figure>

<figure>
<img src="figures/dr2-quiescent-sample/dt-vs-alpha.png" alt="Formation timescale against alpha enhancement">
<figcaption>Δt against [α/Fe]. No trend (Spearman 0.00).</figcaption>
</figure>

`scripts/build_dr2_quiescent_summary.py:33-62` · `formation_times`; `scripts/plot_dr2_formation_timescale.py`

### Distributions

<figure>
<img src="figures/dr2-quiescent-sample/distributions-1d.png" alt="One-dimensional histograms of redshift, mass, age, metallicity, alpha, dust, t50 and delta-t">
<figcaption>Sample medians: z 0.73, log M⋆ 11.11, age 3.02 Gyr, log Z −1.76 (absolute), [α/Fe] 0.05, τ_dust 0.27, t50 3.02 Gyr, Δt 2.46 Gyr. N=187 in every panel.</figcaption>
</figure>

`scripts/plot_dr2_distributions_quality.py:48-72`

### Fit quality

<figure>
<img src="figures/dr2-quiescent-sample/fit-quality.png" alt="Histograms of likelihood calls, evidence, and chi-squared plus a spectrum-versus-photometry chi-squared scatter">
<figcaption>All 187 diagnostics passed. Calls span 0.96–1.5M. Worst joint χ²/ν: 139662 (2.69), 253688 (2.55), 101089 (2.34), labelled by object id. No rerun folders exist (187 directories for 187 targets).</figcaption>
</figure>

`scripts/plot_dr2_distributions_quality.py:74-108`

### Comparison with Borghi+2022

<figure>
<img src="/wiki/f/results/figures/borghi2022-age-vs-z.png" alt="Individual and binned median ages against redshift in Borghi+2022 bins with tabulated Borghi ages overlaid">
<figcaption>Median mass-weighted age (<code>age_q50</code>) per Δz=0.075 bin over 0.6&lt;z&lt;0.9 split at σ⋆=215 km/s, as in Borghi+2022 (their 140 bona fide passive galaxies, NUVrJ + emission-line/visual selected, with SSP-equivalent Lick ages; ours 187 clean-photometry quiescent with mass-weighted SFH ages), plotted at mean bin redshift with NMAD/√N errors and x-bars spanning the bin edges, the 737 flat-ΛCDM cosmic age (grey is unphysical), and labelled pure-passive tracks for z_form=1, 1.5, 2.5, 5; open diamonds re-bin the tabulated Borghi+22 catalogue ages (N=140) in the same edges using LEGA-C DR2 σ⋆ (69 low / 71 high), not digitized from their Figure 9. Our medians average +0.26 Gyr above theirs but stay flat near 3.0 Gyr while theirs decline with redshift (high-σ 3.69→2.77, low-σ 2.99→2.15 Gyr), so our high-σ top bin exceeds theirs by 1.3 Gyr — most likely mass-weighted SFH ages evolving less steeply than SSP-equivalent Lick ages, plus small-number scatter in the top bins.</figcaption>
</figure>

`scripts/plot_borghi2022_age_vs_z.py` · `results/figures/borghi2022-age-vs-z.pdf`

### Evidence

- Data: `results/dr2-quiescent-summary.csv` (187 rows), built by `scripts/build_dr2_quiescent_summary.py` from `results/rtx-5060-dr2-quiescent-full-spectrum/*/ceridwen_{result,derived_outputs}.h5`.
- Figures: `wiki/analyses/dr2-quiescent-sample/` (PNG + PDF). Superseded candidates A/C stay in the bridge reports folder; replaced chronometer figures are kept under `wiki/analyses/_old/`.
- Tests: `tests/test_formation_times.py` (burst/uniform limiting cases).
