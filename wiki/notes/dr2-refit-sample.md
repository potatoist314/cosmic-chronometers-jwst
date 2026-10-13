---
title: DR2 quiescent refit, October defaults
date: 2026-10-13
section: Analyses
theme: Sample and data
tags: [dr2-quiescent-sample, ceridwen, figures]
figures: [formation-times-vs-age.png, headline-age-redshift.png, borghi2022-age-vs-z.png, old-vs-new.png, dt-vs-formation-epoch.png, dt-vs-mass.png, dt-vs-alpha.png, distributions-1d.png, fit-quality.png]
---

<figure>
<img src="figures/dr2-refit-sample/formation-times-vs-age.png" alt="Formation times t80, t50 and t20 against mass-weighted age">
<figcaption>Per-galaxy posterior medians of \(t_{80}\), \(t_{50}\) and \(t_{20}\) against mass-weighted age, with 16–84 intervals, running medians in 10 equal-count bins and a 1:1 line; median \(t_{80}-\mathrm{age}\): 1.46 Gyr, median \(\mathrm{age}-t_{20}\): 1.38 Gyr.</figcaption>
</figure>

- Fitted: 135; diagnostics passed: 135.
- Medians: age 4.04 Gyr; \(\Delta t\) 2.74 Gyr.
- September shifts: age −0.60 Gyr; \(\Delta t\) +0.27 Gyr.

<figure>
<img src="figures/dr2-refit-sample/headline-age-redshift.png" alt="Mass-weighted age against redshift by velocity dispersion, with Ceridwen minus Borghi age residuals">
<figcaption>Mass-weighted age against redshift with binned medians, split at \(\sigma_\star=215\ \mathrm{km\,s^{-1}}\) (80 low, 55 high; age–\(z\) Spearman −0.17), above Ceridwen minus Borghi+22 ages for the 48 overlap galaxies.</figcaption>
</figure>

<figure>
<img src="figures/dr2-refit-sample/borghi2022-age-vs-z.png" alt="Ceridwen and re-binned Borghi catalogue ages against redshift">
<figcaption>Ceridwen and re-binned Borghi+22 catalogue ages (\(N=140\)) in \(\Delta z=0.075\) bins over 0.6–0.9, split at \(215\ \mathrm{km\,s^{-1}}\); bin medians span 3.56–4.66 and 2.15–3.69 Gyr respectively, with mean offset +1.21 Gyr and offsets 0.23–2.17 Gyr.</figcaption>
</figure>

<figure>
<img src="figures/dr2-refit-sample/old-vs-new.png" alt="October versus September ages, formation times, stellar mass, abundances and dust">
<figcaption>October refit against the September run reference arm for the same 135 galaxies, with intervals on both axes and a 1:1 line: median shifts in age, \(t_{50}\), \(\Delta t\), \(\log M_\star\), \([\mathrm{Fe}/\mathrm{H}]\), \([\alpha/\mathrm{Fe}]\) and \(\tau\) are −0.60 Gyr, −0.82 Gyr, +0.27 Gyr, −0.02, −0.09, −0.01 and +0.06 respectively; dust parameters use different laws, Noll in October and Kriek &amp; Conroy in September.</figcaption>
</figure>

<figure>
<img src="figures/dr2-refit-sample/dt-vs-formation-epoch.png" alt="Formation timescale against t50, formation redshift and observed redshift">
<figcaption>\(\Delta t=t_{80}-t_{20}\) against \(t_{50}\), \(z_{\mathrm{form}}\) and \(z_{\mathrm{obs}}\), with running medians; median \(\Delta t\): 2.74 Gyr, Spearman with \(t_{50}\): −0.34.</figcaption>
</figure>

<figure>
<img src="figures/dr2-refit-sample/dt-vs-mass.png" alt="Formation timescale against stellar mass">
<figcaption>\(\Delta t\) against \(\log M_\star\), with running medians; Spearman −0.29.</figcaption>
</figure>

<figure>
<img src="figures/dr2-refit-sample/dt-vs-alpha.png" alt="Formation timescale against alpha enhancement">
<figcaption>\(\Delta t\) against \([\alpha/\mathrm{Fe}]\), with running medians; Spearman 0.32.</figcaption>
</figure>

<figure>
<img src="figures/dr2-refit-sample/distributions-1d.png" alt="Distributions of redshift, stellar mass, age, iron abundance, alpha enhancement, diffuse dust, t50 and formation timescale">
<figcaption>Distributions for 135 galaxies per panel; sample medians: \(z\) 0.73, \(\log M_\star\) 11.28, age 4.04 Gyr, \([\mathrm{Fe}/\mathrm{H}]\) −0.29, \([\alpha/\mathrm{Fe}]\) −0.03, \(\tau_{\mathrm{diffuse}}\) (Noll) 0.49, \(t_{50}\) 3.97 Gyr and \(\Delta t\) 2.74 Gyr.</figcaption>
</figure>

<figure>
<img src="figures/dr2-refit-sample/fit-quality.png" alt="Likelihood calls, evidence, joint chi-squared and spectrum versus photometry chi-squared">
<figcaption>Likelihood calls, \(\ln Z\), joint \(\chi^2/\nu\) and spectrum versus photometry \(\chi^2/\nu\); all 135 diagnostics passed, calls span 4.1–7.9 M, joint \(\chi^2/\nu\) median 1.09 and maximum 2.54 (253688), sampler wall time median 109 s.</figcaption>
</figure>

<details>
<summary>Details</summary>

| setting | September run | October refit |
|---|---|---|
| SSP grid | amist_c3k_hr_krou_afe | amist_c3k_hr_krou_afe_nebular |
| photometry | cosmos_total (COSMOS2015) | cosmos2025; cosmos2020_classic outside its footprint |
| filter curves | sedpy_jax | Ceridwen filter library |
| SFH bins | 7 (edges 0, 0.03, 0.1, 0.3, 1, 3, 5 Gyr, t_univ) | 14 (0-30, 30-100 Myr, log-spaced; last bin 0.85 t_univ to t_univ) |
| metallicity | constant Z | logzsol + metallicity evolution (Gallazzi+26 Table 1), zh_beta_unit Uniform(0, 1) |
| diffuse dust | Kriek & Conroy: tau Uniform(0, 2), index Uniform(-1.0, 0.4) | Noll: tau Uniform(0, 1), delta Uniform(-1.0, 0.4), Ebump Uniform(0, 6) |
| birth-cloud dust | off | dust_ratio ClippedNormal(1.0, 0.3, 0, 2), stars < 10 Myr |
| line mask (±1500 km/s) | [O II], Hbeta, [O III] | Ca II K, Ca II H, Ca I 4227.92 |
| emission lines | masked | FSPS line fluxes free >= 0 (marginalised) |
| calibration | order 3, spectrum_scaling ClippedNormal(1.0, 0.3, 0.2, 3.0) | order 10, constant a_0 fitted (sigma 0.3) |
| seed | 20260830 + manifest index | 20260832, all galaxies |
| GPU | 2 x RTX 5060 Ti | RTX 5090 |

Production defaults at absorption-mask `f273855`, Ceridwen `d7c0536` (SFH-basis fast path).

Starting sample: 187 September targets; 7 refused by production photometry, outside COSMOS2025 with COSMOS2020 Classic FlagCOMBINED = 1:

- M11_245252
- M11_226721
- M11_244738
- M5_241189
- M2_208364
- M10_228717
- M15_89153

180 fittable; 135 fitted; 45 not reached before the Vast credit floor, listed under `unfitted` in `targets.json`.

Fit order: seeded random (`20261013`), then from 22:59 UTC stratified by redshift tertile × September \(\log M_\star\) tertile.

| Quantity | KS p, fitted (135) vs unfitted (45) | Median, fitted | Median, all 180 |
|---|---|---|---|
| Redshift | 0.43 | 0.728 | 0.729 |
| September \(\log M_\star\) | 0.78 | 11.35 | 11.34 |
| S/N | 0.85 | 21.5 | 21.3 |

Vast: USD 5.65 billed over 13 instances; cap USD 10; 0 instances left.

Evidence:

- Summary: `results/dr2-refit-2026-10-12/dr2-refit-summary.csv`
- Targets: `results/dr2-refit-2026-10-12/targets.json`
- `scripts/build_dr2_quiescent_summary.py`
- `scripts/plot_dr2_distributions_quality.py`
- `scripts/plot_dr2_formation_timescale.py`
- `scripts/plot_borghi2022_age_vs_z.py`
- `archive/scripts/plot_dr2_headline_candidates.py`
- `scripts/plot_dr2_refit_figures.py`
- September reference: [DR2 quiescent sample](../dr2-quiescent-sample/)

</details>