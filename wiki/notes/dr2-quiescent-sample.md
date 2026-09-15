---
title: DR2 quiescent sample
date: 2026-09-03
section: Analyses
theme: Sample and data
tags: [dr2-quiescent-sample, ceridwen, figures]
job: t_d0d3a321
old: _old/analyses/dr2-quiescent-sample.html
figures: [borghi2022-age-vs-z.png, distributions-1d.png, dt-vs-alpha.png, dt-vs-formation-epoch.png, dt-vs-mass.png, fit-quality.png, headline-age-redshift.png]
---

Paper-quality figure set for the 187 LEGA-C DR2 quiescent full-spectrum Ceridwen fits: the age–redshift headline against Borghi+22, formation timescales, parameter distributions, and fit quality. Every plot renders from one tidy table, [results/dr2-quiescent-new-defaults-summary.csv](/wiki/f/results/dr2-quiescent-summary.csv).

<figure>
<img src="figures/dr2-quiescent-sample/headline-age-redshift.png" alt="Mass-weighted age against redshift for 187 galaxies with binned medians, plus a Ceridwen-minus-Borghi residual strip for the 68-galaxy overlap">
<figcaption>Top: mass-weighted age with 16–84 intervals for all 187 galaxies, coloured by velocity-dispersion group (split 215 \(\mathrm{km\,s^{-1}}\)), with binned medians (\(\mathrm{NMAD}/\sqrt{N}\)).</figcaption>
<details>
<summary>Details</summary>
<p>Bottom: Ceridwen minus Borghi+22 SSP age for the 68 overlap galaxies. Vector version: <code>headline-age-redshift.pdf</code>.</p>
</details>
</figure>

<details>
<summary>Details</summary>

`archive/scripts/plot_dr2_headline_candidates.py:147-182` · `layout_b_single_with_residual`

</details>

<details>
<summary>Formation timescale</summary>

\(t_X\) is the lookback younger than which X% of the formed mass was made; \(\Delta t=t_{80}-t_{20}\) is the 20th-to-80th mass-assembly interval. Median \(\Delta t\): 2.55 Gyr; Spearman coefficients with \(t_{50}\), \(\log M_\star\) and \([\alpha/\mathrm{Fe}]\): −0.45, −0.21 and 0.04; 67% lie at 2.3–3.3 Gyr; the 7-bin SFH (2-Gyr bins at 1–5 Gyr) quantises \(\Delta t\), limiting its resolution.

</details>

<figure>
<img src="figures/dr2-quiescent-sample/dt-vs-formation-epoch.png" alt="Formation timescale against t50 lookback, Planck18 formation redshift, and observed redshift">
<figcaption>\(\Delta t\) against formation epoch (\(t_{50}\) lookback, Planck18 formation redshift from age(z_obs)−\(t_{50}\), observed redshift) with running medians.</figcaption>
</figure>

<figure>
<img src="figures/dr2-quiescent-sample/dt-vs-mass.png" alt="Formation timescale against stellar mass">
<figcaption>\(\Delta t\) against stellar mass, Spearman −0.21.</figcaption>
</figure>

<figure>
<img src="figures/dr2-quiescent-sample/dt-vs-alpha.png" alt="Formation timescale against alpha enhancement">
<figcaption>\(\Delta t\) against \([\alpha/\mathrm{Fe}]\), Spearman 0.04.</figcaption>
</figure>

<details>
<summary>Details</summary>

`scripts/build_dr2_quiescent_summary.py:33-62` · `formation_times`; `scripts/plot_dr2_formation_timescale.py`

</details>

<figure>
<img src="figures/dr2-quiescent-sample/distributions-1d.png" alt="One-dimensional histograms of redshift, mass, age, metallicity, alpha, dust, t50 and delta-t">
<figcaption>Sample medians: z 0.73, \(\log M_\star\) 11.34, age 4.81 Gyr, \([\mathrm{Fe}/\mathrm{H}]\) −0.18, \([\alpha/\mathrm{Fe}]\) −0.05, \(\tau_{\mathrm{dust}}\) 0.45, \(t_{50}\) 5.03 Gyr, \(\Delta t\) 2.55 Gyr; N=187 in every panel.</figcaption>
</figure>

<details>
<summary>Details</summary>

`scripts/plot_dr2_distributions_quality.py:48-72`

</details>

<figure>
<img src="figures/dr2-quiescent-sample/fit-quality.png" alt="Histograms of likelihood calls, evidence, and chi-squared plus a spectrum-versus-photometry chi-squared scatter">
<figcaption>All 187 diagnostics passed.</figcaption>
<details>
<summary>Details</summary>
<p>Calls span 4.9–11.2M; worst joint \(\chi^2\)/ν: 139662 (2.56), 253688 (2.52), 101089 (2.19), labelled by object ID; 187 directories for 187 targets.</p>
</details>
</figure>

<details>
<summary>Details</summary>

`scripts/plot_dr2_distributions_quality.py:74-108`

</details>

<figure>
<img src="/wiki/f/results/figures/borghi2022-age-vs-z.png" alt="Individual and binned median ages against redshift in Borghi+2022 bins with tabulated Borghi ages overlaid">
<figcaption>Median mass-weighted age (<code>age_q50</code>) per \(\Delta z\)=0.075 bin over 0.6&lt;z&lt;0.9 split at \(\sigma_\star\)=215 \(\mathrm{km\,s^{-1}}\), as in Borghi+2022 (their 140 bona fide passive galaxies, NUVrJ + emission-line/visual selected, with SSP-equivalent Lick ages; ours 187 clean-photometry quiescent with mass-weighted SFH ages), plotted at mean bin redshift with \(\mathrm{NMAD}/\sqrt{N}\) errors and x-bars spanning the bin edges, the 737 flat-\(\Lambda\mathrm{CDM}\) cosmic age (grey is unphysical), and labelled pure-passive tracks for \(z_{\mathrm{form}}\)=1, 1.5, 2.5, 5; open diamonds re-bin the tabulated Borghi+22 catalogue ages (N=140) in the same edges using LEGA-C DR2 \(\sigma_\star\) (69 low / 71 high), not digitized from their Figure 9.</figcaption>
<details>
<summary>Details</summary>
<p>Ceridwen medians by bin span 4.5–5.2 Gyr, averaging +1.95 Gyr above Borghi; Borghi medians decline with redshift: high-\(\sigma\) 3.69→2.77, low-\(\sigma\) 2.99→2.15 Gyr; offsets span 0.8–2.7 Gyr and peak in the low-\(\sigma\) 0.75–0.9 bins.</p>
</details>
</figure>

<details>
<summary>Details</summary>

`scripts/plot_borghi2022_age_vs_z.py` · `results/figures/borghi2022-age-vs-z.pdf`

</details>

<details>
<summary>Evidence</summary>

- Data: `results/dr2-quiescent-new-defaults-summary.csv` (187 rows), built by `scripts/build_dr2_quiescent_summary.py` from `results/dr2-quiescent-new-defaults/*/ceridwen_{result,derived_outputs}.h5`.
- Figures: `wiki/analyses/dr2-quiescent-sample/` (PNG + PDF). Superseded candidates A/C stay in the bridge reports folder; replaced chronometer figures are kept under `wiki/analyses/_old/`.
- Tests: `tests/test_formation_times.py` (burst/uniform limiting cases).

</details>
