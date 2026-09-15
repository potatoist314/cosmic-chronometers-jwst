---
title: Ceridwen common results board
date: 2026-09-04
section: Analyses
theme: Population results
tags: [ceridwen, results]
job: t_44b5da5c
old: _old/analyses/ceridwen-results.html
figures: [borghi2022-age-vs-z.png, calibration-polynomial-explainer.png, calibration-polynomial-mock-bias.png, calibration-polynomial-real-posteriors.png, calibration-polynomial-tilt-origin-ibands.png, calibration-polynomial-tilt-origin-photometry.png, calibration-polynomial-tilt-origin-posteriors.png, calibration-polynomial-tilt-origin-vectors.png, calibration-polynomial-vectors.png, distributions-1d.png, dt-vs-alpha.png, dt-vs-formation-epoch.png, dt-vs-mass.png, feature_windows_M5_172669.png, fit-quality.png, headline-age-redshift.png, mock_bias_vs_tilt.png, mock_width_ratio.png, real_targets_posteriors.png]
---

Ceridwen fits, figures, tables and benchmarks.

<details>
<summary>Calibration</summary>
<div id="corrected-calibration-science-authoritative-audit"></div>

**Flux ratio sign.** DR2 spectra are *brighter* than production COSMOS2015 3-arcsecond aperture photometry. In-band spectrum-to-photometry ratios range from 1.26 to 1.48 outside IA679. Production fits sample scale factors of 1.24 and 1.49.

**Tilt origin.** Corrected photometry drives scale factors to 0.99 and 0.92. This correction removes both scale offset and M4's polynomial tilt. Residual M4 tilt shifts from −20% to +0.4%. M5 retains a −20% tilt alongside a 0.3-mag optical-to-NIR model discrepancy.

</details>

<details>
<summary>Status at a glance</summary>

Results dated 2026-09-04.

</details>

| Analysis Domain | Key Scientific Finding | Primary Deliverables |
| --- | --- | --- |
| **187-Galaxy DR2 Sample** | Median mass-weighted age 3.02 Gyr. Median assembly interval Δt = 2.46 Gyr. Zero fit failures among 187 galaxies. | [Analysis Page](../dr2-quiescent-sample/) · [Summary CSV](/wiki/f/results/dr2-quiescent-summary.csv) · [Results Dir](/wiki/f/results/rtx-5060-dr2-quiescent-full-spectrum) |
| **Borghi+2022 Age vs z** | Ceridwen medians stay flat near 3.0 Gyr, averaging +0.26 Gyr above re-binned N=140 Borghi catalogue. Velocity dispersion split shows a weak gradient. | [Figure PNG](/wiki/f/results/figures/borghi2022-age-vs-z.png) · [Vector PDF](/wiki/f/results/figures/borghi2022-age-vs-z.pdf) · [Source Table](/wiki/f/data/processed/borghi2022_legac_dr2/borghi2022_legac_dr2_spectrum_matches copy.tsv) |
| **Absorption-Line Mask** | Masked and feature modes keep tilt bias and widen posteriors 1.0–1.6×. Shifts real targets up to 22σ. | [Analysis Page](../absorption-line-mask/) · [Summary CSV](/wiki/f/results/absorption-mask/summary.csv) · [Grid Results](/wiki/f/results/absorption-mask) |
| **Calibration & Tilt Origin** | Spectra are brighter than 3" photometry by 1.26–1.48. Corrected photometry eliminates M4 tilt (+0.4%). M5 retains a −20% tilt. | [Worktree Page](/wiki/f/tmp/worktrees/astro-calibration-polynomial/wiki/analyses/ceridwen-calibration-polynomial.html) · [Arms CSV](/wiki/f/tmp/worktrees/astro-calibration-polynomial/results/tilt-origin-2026-09-02/arms.csv) · [Tilt Results](/wiki/f/tmp/worktrees/astro-calibration-polynomial/results/tilt-origin-2026-09-02) |
| **Formation Timescales** | Median Δt is 2.46 Gyr. Flat across formation epoch. Spearman correlation with mass and [α/Fe] is 0.00 in 7-bin SFH. | [Epoch PNG](figures/dr2-quiescent-sample/dt-vs-formation-epoch.png) · [Mass PNG](figures/dr2-quiescent-sample/dt-vs-mass.png) · [Alpha PNG](figures/dr2-quiescent-sample/dt-vs-alpha.png) |
| **Fit Quality Diagnostics** | All 187 fits succeeded. Worst joint reduced χ²/ν values are 2.69 (139662), 2.55 (253688), and 2.34 (101089). | [Quality PNG](figures/dr2-quiescent-sample/fit-quality.png) · [Quality PDF](figures/dr2-quiescent-sample/fit-quality.pdf) |
| **Interactive Checkpoint Evolution** | Interactive view of the accepted prior predictive, last retained checkpoint, and converged rescue posterior (nested sampling solution after sampler convergence). | [Open interactive viewer](../ceridwen-checkpoint-spectrum-evolution/) · [Screenshots Dir](../../../../.claude/scripts/hermes-bridge/reports/ceridwen-checkpoint-animation/screenshots) |

<div id="scientific-terms-and-definitions"></div>

<details>
<summary>187-galaxy DR2 quiescent sample (final set)</summary>

Analysis page: [analyses/dr2-quiescent-sample.html](../dr2-quiescent-sample/). Master catalogue table: [results/dr2-quiescent-summary.csv](/wiki/f/results/dr2-quiescent-summary.csv) (187 galaxies, 49 columns including t20, t50, t80, Δt). Production run directory: [results/rtx-5060-dr2-quiescent-full-spectrum/](/wiki/f/results/rtx-5060-dr2-quiescent-full-spectrum) (187 individual target folders). Exploratory chronometer notebook: [ceridwen_cosmic_chronometer.ipynb](/wiki/f/results/rtx-5060-dr2-quiescent-full-spectrum/ceridwen_cosmic_chronometer.ipynb) and summary data: [ceridwen_cosmic_chronometer_summary.h5](/wiki/f/results/rtx-5060-dr2-quiescent-full-spectrum/ceridwen_cosmic_chronometer_summary.h5). Builders: [build_dr2_quiescent_summary.py](/wiki/f/scripts/build_dr2_quiescent_summary.py), [plot_dr2_headline_candidates.py](/wiki/f/archive/scripts/plot_dr2_headline_candidates.py).

</details>

<figure>
<img src="figures/dr2-quiescent-sample/headline-age-redshift.png" alt="DR2 age-redshift headline PNG. Ceridwen infers median mass-weighted age near 3.0 Gyr across 187 galaxies. Points carry 16th to 84th percentile bars. Squares show NMAD binned medians. The residual strip compares the 68-galaxy overlap sample against Borghi+2022 catalogue ages. ">
<figcaption><strong>DR2 age-redshift headline PNG.</strong> Ceridwen infers median mass-weighted age near 3.0 Gyr across 187 galaxies.</figcaption>
<details>
<summary>Details</summary>
<p>Points carry 16th to 84th percentile bars. Squares show NMAD binned medians. The residual strip compares the 68-galaxy overlap sample against Borghi+2022 catalogue ages. </p>
</details>
</figure>

<figure>
<img src="figures/dr2-quiescent-sample/distributions-1d.png" alt="DR2 parameter distributions PNG. Parameter distributions show median redshift 0.73 and median mass-weighted age 3.02 Gyr across 187 galaxies. Each histogram marks the sample median with an orange line and labels the median and the galaxy count. The panels compare eight physical quantities across the same 187 galaxies. The spread of each histogram shows the sample range. Fits assume a fixed-grid star formation history.">
<figcaption><strong>DR2 parameter distributions PNG.</strong> Parameter distributions show median redshift 0.73 and median mass-weighted age 3.02 Gyr across 187 galaxies.</figcaption>
<details>
<summary>Details</summary>
<p>Each histogram marks the sample median with an orange line and labels the median and the galaxy count. The panels compare eight physical quantities across the same 187 galaxies. The spread of each histogram shows the sample range. Fits assume a fixed-grid star formation history.</p>
</details>
</figure>

<details>
<summary>Details</summary>

The coarse 7-bin SFH basis limits fine temporal resolution. Mass-weighted ages reflect non-parametric composite populations. These values do not directly match Borghi SSP-equivalent Lick ages.

</details>

<details>
<summary>Borghi+2022 age versus redshift comparison</summary>

Standalone figure: [results/figures/borghi2022-age-vs-z.png](/wiki/f/results/figures/borghi2022-age-vs-z.png) (and [PDF](/wiki/f/results/figures/borghi2022-age-vs-z.pdf)). Source data table: [borghi2022_legac_dr2_spectrum_matches copy.tsv](/wiki/f/data/processed/borghi2022_legac_dr2/borghi2022_legac_dr2_spectrum_matches copy.tsv). Generation script: [scripts/plot_borghi2022_age_vs_z.py](/wiki/f/scripts/plot_borghi2022_age_vs_z.py).

</details>

<figure>
<img src="/wiki/f/results/figures/borghi2022-age-vs-z.png" alt="Borghi-style median age versus redshift PNG. Median mass-weighted age stays near 3.0 Gyr across redshift for 187 galaxies. Ceridwen medians average +0.26 Gyr above the re-binned N=140 Borghi+2022 reference sample. Points carry 16th to 84th percentile bars on the left and NMAD errors on the right. The grey band marks ages older than the Universe, not an uncertainty range. The velocity dispersion comparison shows a weak gradient. ">
<figcaption><strong>Borghi-style median age versus redshift PNG.</strong> Median mass-weighted age stays near 3.0 Gyr across redshift for 187 galaxies.</figcaption>
<details>
<summary>Details</summary>
<p>Ceridwen medians average +0.26 Gyr above the re-binned N=140 Borghi+2022 reference sample. Points carry 16th to 84th percentile bars on the left and NMAD errors on the right. The grey band marks ages older than the Universe, not an uncertainty range. The velocity dispersion comparison shows a weak gradient. </p>
</details>
</figure>

<details>
<summary>Details</summary>

**Finding.** Ceridwen mass-weighted ages stay flat near 3.0 Gyr from z=0.6 to z=0.9. They average +0.26 Gyr above re-binned Borghi values. The velocity dispersion split (σ < 215 km/s versus σ ≥ 215 km/s) shows a smaller difference than the gradient in Borghi+2022.

</details>

<details>
<summary>Absorption-line mask experiment</summary>

Draft analysis page: [analyses/absorption-line-mask.html](../absorption-line-mask/). Results summary: [results/absorption-mask/summary.csv](/wiki/f/results/absorption-mask/summary.csv) and [summary.json](/wiki/f/results/absorption-mask/summary.json). Target Fisher analysis: [fisher_M5_172669.json](/wiki/f/results/absorption-mask/fisher_M5_172669.json). 45-fit execution directory: [results/absorption-mask/](/wiki/f/results/absorption-mask). Analysis scripts: [absorption_mask_analysis.py](/wiki/f/scripts/absorption_mask_analysis.py), [absorption_mask_report.py](/wiki/f/scripts/absorption_mask_report.py).

</details>

<figure>
<img src="figures/absorption-mask/feature_windows_M5_172669.png" alt="Absorption feature windows PNG. The spectrum plot shows observed-frame flux for target galaxy M5_172669. The orange line traces kept feature pixels inside plus-or-minus 1000 km/s line windows against the grey full fitted spectrum. The mask keeps 1389 of 3602 fitted pixels and excludes 2213 (61.4 percent). ">
<figcaption><strong>Absorption feature windows PNG.</strong> The spectrum plot shows observed-frame flux for target galaxy M5_172669.</figcaption>
<details>
<summary>Details</summary>
<p>The orange line traces kept feature pixels inside plus-or-minus 1000 km/s line windows against the grey full fitted spectrum. The mask keeps 1389 of 3602 fitted pixels and excludes 2213 (61.4 percent). </p>
</details>
</figure>

<figure>
<img src="figures/absorption-mask/real_targets_posteriors.png" alt="Absorption-mask real-target posteriors PNG. Posterior medians compare six stellar parameters across three real DR2 galaxy targets. Masked pixel modes shift parameter medians by up to 22 full-spectrum sigma relative to baseline posteriors. Bars show the 16th to 84th percentile range for each sample object. ">
<figcaption><strong>Absorption-mask real-target posteriors PNG.</strong> Posterior medians compare six stellar parameters across three real DR2 galaxy targets.</figcaption>
<details>
<summary>Details</summary>
<p>Masked pixel modes shift parameter medians by up to 22 full-spectrum sigma relative to baseline posteriors. Bars show the 16th to 84th percentile range for each sample object. </p>
</details>
</figure>

<figure>
<img src="figures/absorption-mask/mock_bias_vs_tilt.png" alt="Absorption-mask mock bias PNG. Mock tests evaluate recovered stellar population parameter bias. The sample holds 12 synthetic configurations in three pixel modes. The panels compare feature-only and down-weighted continuum modes against true input age and mass values. Error bars indicate the 16th to 84th percentile posterior uncertainty range. Masked modes fail to remove continuum tilt bias. Synthetic mocks assume idealized Gaussian noise without sky-subtraction artifacts.">
<figcaption><strong>Absorption-mask mock bias PNG.</strong> Mock tests evaluate recovered stellar population parameter bias.</figcaption>
<details>
<summary>Details</summary>
<p>The sample holds 12 synthetic configurations in three pixel modes. The panels compare feature-only and down-weighted continuum modes against true input age and mass values. Error bars indicate the 16th to 84th percentile posterior uncertainty range. Masked modes fail to remove continuum tilt bias. Synthetic mocks assume idealized Gaussian noise without sky-subtraction artifacts.</p>
</details>
</figure>

<figure>
<img src="figures/absorption-mask/mock_width_ratio.png" alt="Absorption-mask posterior-width PNG. The figure compares posterior uncertainty width values. The sample holds 12 synthetic configurations in three pixel modes. Masked and feature-only modes give 1.0 to 1.6 times the full-spectrum width for mass, age, metallicity, alpha enhancement, and dust. Ratios compare each mode against the baseline fit. Bars carry the median ratio as a label. ">
<figcaption><strong>Absorption-mask posterior-width PNG.</strong> The figure compares posterior uncertainty width values.</figcaption>
<details>
<summary>Details</summary>
<p>The sample holds 12 synthetic configurations in three pixel modes. Masked and feature-only modes give 1.0 to 1.6 times the full-spectrum width for mass, age, metallicity, alpha enhancement, and dust. Ratios compare each mode against the baseline fit. Bars carry the median ratio as a label. </p>
</details>
</figure>


<details>
<summary>Calibration polynomial and tilt origin</summary>

Worktree analysis page (pushed on branch `origin/calibration-polynomial` at commit `85c1e4a`): [ceridwen-calibration-polynomial.html](/wiki/f/tmp/worktrees/astro-calibration-polynomial/wiki/analyses/ceridwen-calibration-polynomial.html). Analysis notebook: [tilt-origin-2026-09-02/analysis.ipynb](/wiki/f/tmp/worktrees/astro-calibration-polynomial/results/tilt-origin-2026-09-02/analysis.ipynb). Quantitative summaries: [arms.csv](/wiki/f/tmp/worktrees/astro-calibration-polynomial/results/tilt-origin-2026-09-02/arms.csv) and [ibands.csv](/wiki/f/tmp/worktrees/astro-calibration-polynomial/results/tilt-origin-2026-09-02/ibands.csv). Completed tilt run directory: [results/tilt-origin-2026-09-02/](/wiki/f/tmp/worktrees/astro-calibration-polynomial/results/tilt-origin-2026-09-02). Superseded local snapshot: [results/calibration-polynomial-2026-09-02/](/wiki/f/archive/results/calibration-polynomial-2026-09-02). Experiment scripts: [calibration_polynomial_experiment.py](/wiki/f/tmp/worktrees/astro-calibration-polynomial/scripts/calibration_polynomial_experiment.py), [download_legac_dr2_aperture_photometry.py](/wiki/f/tmp/worktrees/astro-calibration-polynomial/scripts/download_legac_dr2_aperture_photometry.py), [tilt_origin_runner.py](/wiki/f/tmp/worktrees/astro-calibration-polynomial/scripts/tilt_origin_runner.py), [tilt_origin_vast.py](/wiki/f/tmp/worktrees/astro-calibration-polynomial/scripts/tilt_origin_vast.py).

</details>

<figure>
<img src="/wiki/f/tmp/worktrees/astro-calibration-polynomial/wiki/analyses/calibration-polynomial-explainer.png" alt="Calibration-polynomial explainer PNG. Diagram shows how a multiplicative polynomial maps spectrum flux calibration onto broadband photometry. The top panel compares mock, true, and calibrated spectra against true and mock photometry points with error bars. The mock mimics one LEGA-C galaxy observation with a 4 percent tilt plus 2 percent curvature at z = 0.604. The bottom panel compares the data-to-model ratio against the injected distortion, the recovered order-3 polynomial, and a scalar-only model. ">
<figcaption><strong>Calibration-polynomial explainer PNG.</strong> Diagram shows how a multiplicative polynomial maps spectrum flux calibration onto broadband photometry.</figcaption>
<details>
<summary>Details</summary>
<p>The top panel compares mock, true, and calibrated spectra against true and mock photometry points with error bars. The mock mimics one LEGA-C galaxy observation with a 4 percent tilt plus 2 percent curvature at z = 0.604. The bottom panel compares the data-to-model ratio against the injected distortion, the recovered order-3 polynomial, and a scalar-only model. </p>
</details>
</figure>

<figure>
<img src="/wiki/f/tmp/worktrees/astro-calibration-polynomial/wiki/analyses/calibration-polynomial-mock-bias.png" alt="Calibration-polynomial mock bias PNG. Mock tests compare pull and posterior half-width across 12 fit variants with order-1, order-3, and order-5 polynomials. The sample covers tilted and untilted cases for mass, metallicity, alpha enhancement, dust, and mass-weighted age. The left panel compares median-minus-truth pull against zero. The right panel compares half-width against the untilted baseline. Polynomial arms remove the injected tilt bias. Each point is one arm value, so no error bars appear. ">
<figcaption><strong>Calibration-polynomial mock bias PNG.</strong> Mock tests compare pull and posterior half-width across 12 fit variants with order-1, order-3, and order-5 polynomials.</figcaption>
<details>
<summary>Details</summary>
<p>The sample covers tilted and untilted cases for mass, metallicity, alpha enhancement, dust, and mass-weighted age. The left panel compares median-minus-truth pull against zero. The right panel compares half-width against the untilted baseline. Polynomial arms remove the injected tilt bias. Each point is one arm value, so no error bars appear. </p>
</details>
</figure>

<figure>
<img src="/wiki/f/tmp/worktrees/astro-calibration-polynomial/wiki/analyses/calibration-polynomial-vectors.png" alt="Calibration-polynomial vectors PNG. The plot displays recovered calibration polynomial flux curves versus wavelength for mock and real galaxy arms. Each mock panel compares the recovered profiled band against the dashed injected distortion. Shaded envelopes show 68% credible interval uncertainty ranges for each sample arm. Real panels show the recovered band only. ">
<figcaption><strong>Calibration-polynomial vectors PNG.</strong> The plot displays recovered calibration polynomial flux curves versus wavelength for mock and real galaxy arms.</figcaption>
<details>
<summary>Details</summary>
<p>Each mock panel compares the recovered profiled band against the dashed injected distortion. Shaded envelopes show 68% credible interval uncertainty ranges for each sample arm. Real panels show the recovered band only. </p>
</details>
</figure>

<figure>
<img src="/wiki/f/tmp/worktrees/astro-calibration-polynomial/wiki/analyses/calibration-polynomial-real-posteriors.png" alt="Calibration-polynomial real-target posteriors PNG. Posterior medians compare seven stellar and calibration parameters for sample galaxies M4_108989 and M5_172669. Points compare baseline and polynomial arms, with bars showing the 16th to 84th percentile range. M4 mass-weighted age moves from 4.65 Gyr at baseline to 3.02 Gyr with the order-3 polynomial. The spread across arms shows sensitivity to the calibration model choice. ">
<figcaption><strong>Calibration-polynomial real-target posteriors PNG.</strong> Posterior medians compare seven stellar and calibration parameters for sample galaxies M4_108989 and M5_172669.</figcaption>
<details>
<summary>Details</summary>
<p>Points compare baseline and polynomial arms, with bars showing the 16th to 84th percentile range. M4 mass-weighted age moves from 4.65 Gyr at baseline to 3.02 Gyr with the order-3 polynomial. The spread across arms shows sensitivity to the calibration model choice. </p>
</details>
</figure>

<figure>
<img src="/wiki/f/tmp/worktrees/astro-calibration-polynomial/wiki/analyses/calibration-polynomial-tilt-origin-ibands.png" alt="Tilt-origin in-band flux ratios PNG. In-band flux ratios compare LEGA-C DR2 spectrum flux against photometric measurements for sample galaxies M4 and M5. Ratios indicate spectra are brighter than production 3-arcsecond aperture fluxes by 1.26 to 1.48. Ratios stay near flat against corrected aperture photometry and UltraVISTA total fluxes. Lines connect five bands with no error bars. 26 to 1.48 range.">
<figcaption><strong>Tilt-origin in-band flux ratios PNG.</strong> In-band flux ratios compare LEGA-C DR2 spectrum flux against photometric measurements for sample galaxies M4 and M5.</figcaption>
<details>
<summary>Details</summary>
<p>Ratios indicate spectra are brighter than production 3-arcsecond aperture fluxes by 1.26 to 1.48. Ratios stay near flat against corrected aperture photometry and UltraVISTA total fluxes. Lines connect five bands with no error bars. 26 to 1.48 range.</p>
</details>
</figure>

<figure>
<img src="/wiki/f/tmp/worktrees/astro-calibration-polynomial/wiki/analyses/calibration-polynomial-tilt-origin-photometry.png" alt="Tilt-origin photometric residuals PNG. Residual plots compare photometric flux values against synthetic model photometry across the fitted bands for sample galaxies M4 and M5. Corrected photometry removes M4 calibration tilt. Target M5 retains a 0.3-mag optical-to-NIR model discrepancy. Error bars mark photometric measurement uncertainty ranges. ">
<figcaption><strong>Tilt-origin photometric residuals PNG.</strong> Residual plots compare photometric flux values against synthetic model photometry across the fitted bands for sample galaxies M4 and M5.</figcaption>
<details>
<summary>Details</summary>
<p>Corrected photometry removes M4 calibration tilt. Target M5 retains a 0.3-mag optical-to-NIR model discrepancy. Error bars mark photometric measurement uncertainty ranges. </p>
</details>
</figure>

<figure>
<img src="/wiki/f/tmp/worktrees/astro-calibration-polynomial/wiki/analyses/calibration-polynomial-tilt-origin-vectors.png" alt="Tilt-origin polynomial vectors PNG. Vector panels track recovered calibration polynomial flux curves versus wavelength for sample galaxies M4 and M5. Curves compare uncorrected and corrected photometry runs against the flat baseline. Shaded bands show 68% credible interval uncertainty ranges. Target M5 variants retain a minus-16 to minus-24 percent tilt. Only the corrected-photometry M4 curves stay flat near tilt +0 percent. The other M4 variants retain minus-11 to minus-20 percent tilts. ">
<figcaption><strong>Tilt-origin polynomial vectors PNG.</strong> Vector panels track recovered calibration polynomial flux curves versus wavelength for sample galaxies M4 and M5.</figcaption>
<details>
<summary>Details</summary>
<p>Curves compare uncorrected and corrected photometry runs against the flat baseline. Shaded bands show 68% credible interval uncertainty ranges. Target M5 variants retain a minus-16 to minus-24 percent tilt. Only the corrected-photometry M4 curves stay flat near tilt +0 percent. The other M4 variants retain minus-11 to minus-20 percent tilts. </p>
</details>
</figure>

<figure>
<img src="/wiki/f/tmp/worktrees/astro-calibration-polynomial/wiki/analyses/calibration-polynomial-tilt-origin-posteriors.png" alt="Tilt-origin posterior comparison PNG. Dot plots show posterior age and stellar mass values for sample galaxies M4 and M5 across all 23 calibration variants each. The panels compare arms with production aperture photometry against arms with corrected aperture photometry. Bars show the 16th to 84th percentile range per arm. ">
<figcaption><strong>Tilt-origin posterior comparison PNG.</strong> Dot plots show posterior age and stellar mass values for sample galaxies M4 and M5 across all 23 calibration variants each.</figcaption>
<details>
<summary>Details</summary>
<p>The panels compare arms with production aperture photometry against arms with corrected aperture photometry. Bars show the 16th to 84th percentile range per arm. </p>
</details>
</figure>


<details>
<summary>Formation timescales (Δt)</summary>

Analysis script: [scripts/plot_dr2_formation_timescale.py](/wiki/f/scripts/plot_dr2_formation_timescale.py). The mass assembly interval Δt equals t20 − t80. This value measures the lookback time interval during which the middle 60% of stellar mass formed.

</details>

<figure>
<img src="figures/dr2-quiescent-sample/dt-vs-formation-epoch.png" alt="Formation timescale versus epoch PNG. Median stellar mass assembly interval Delta-t is 2.46 Gyr for the sample of 187 galaxies. Points carry 16th to 84th percentile bars and compare individual galaxy values against formation epoch and observed redshift. The orange band shows the running 16th to 84th percentile spread. The trend stays flat across redshift. ">
<figcaption><strong>Formation timescale versus epoch PNG.</strong> Median stellar mass assembly interval Delta-t is 2.46 Gyr for the sample of 187 galaxies.</figcaption>
<details>
<summary>Details</summary>
<p>Points carry 16th to 84th percentile bars and compare individual galaxy values against formation epoch and observed redshift. The orange band shows the running 16th to 84th percentile spread. The trend stays flat across redshift. </p>
</details>
</figure>

<figure>
<img src="figures/dr2-quiescent-sample/dt-vs-mass.png" alt="Formation timescale versus mass PNG. The plot tracks mass assembly interval Delta-t against stellar mass for 187 galaxies. The Spearman rank correlation between mass and assembly time is 0.00. Points carry 16th to 84th percentile error bars. The orange band shows the running spread and compares low-mass and high-mass objects. ">
<figcaption><strong>Formation timescale versus mass PNG.</strong> The plot tracks mass assembly interval Delta-t against stellar mass for 187 galaxies.</figcaption>
<details>
<summary>Details</summary>
<p>The Spearman rank correlation between mass and assembly time is 0.00. Points carry 16th to 84th percentile error bars. The orange band shows the running spread and compares low-mass and high-mass objects. </p>
</details>
</figure>

<figure>
<img src="figures/dr2-quiescent-sample/dt-vs-alpha.png" alt="Formation timescale versus alpha enhancement PNG. The plot examines mass assembly interval Delta-t versus alpha enhancement for 187 galaxies. The Spearman rank correlation between alpha enhancement and assembly time is 0.00. Points carry 16th to 84th percentile error bars. The orange band shows the running spread and compares alpha-enhanced and solar-abundance objects. The model assumes a single alpha enhancement value per galaxy.">
<figcaption><strong>Formation timescale versus alpha enhancement PNG.</strong> The plot examines mass assembly interval Delta-t versus alpha enhancement for 187 galaxies.</figcaption>
<details>
<summary>Details</summary>
<p>The Spearman rank correlation between alpha enhancement and assembly time is 0.00. Points carry 16th to 84th percentile error bars. The orange band shows the running spread and compares alpha-enhanced and solar-abundance objects. The model assumes a single alpha enhancement value per galaxy.</p>
</details>
</figure>

<details>
<summary>Details</summary>

**Finding.** Median Δt is 2.46 Gyr across the sample. There is no significant correlation between Δt and stellar mass (Spearman 0.00) or [α/Fe] (Spearman 0.00). The coarse 7-bin SFH basis constrains timescale resolution.

</details>

<details>
<summary>Fit quality diagnostics</summary>

Diagnostic plotting script: [scripts/plot_dr2_distributions_quality.py](/wiki/f/scripts/plot_dr2_distributions_quality.py). Covers likelihood calls, Bayesian log-evidence (logZ, marginal likelihood), Effective Sample Size (ESS, independent posterior samples), and joint reduced χ²/ν across all 187 galaxies.

</details>

<figure>
<img src="figures/dr2-quiescent-sample/fit-quality.png" alt="DR2 fit-quality diagnostics PNG. Fit diagnostics show zero failures across all 187 galaxies in the sample. Histograms show likelihood calls, log-evidence, and joint reduced chi-squared values across objects. Each panel shows one value per galaxy, so no error bars appear. The dashed line marks a chi-squared of 1. The scatter panel compares photometry and spectrum values and labels the five worst objects. Worst joint reduced chi-squared value is 2.69. 69, so some spectra still miss the model.">
<figcaption><strong>DR2 fit-quality diagnostics PNG.</strong> Fit diagnostics show zero failures across all 187 galaxies in the sample.</figcaption>
<details>
<summary>Details</summary>
<p>Histograms show likelihood calls, log-evidence, and joint reduced chi-squared values across objects. Each panel shows one value per galaxy, so no error bars appear. The dashed line marks a chi-squared of 1. The scatter panel compares photometry and spectrum values and labels the five worst objects. Worst joint reduced chi-squared value is 2.69. 69, so some spectra still miss the model.</p>
</details>
</figure>

<details>
<summary>Details</summary>

**Finding.** Zero sampling failures (187/187 completed). The worst joint χ²/ν values are 2.69 (galaxy 139662), 2.55 (galaxy 253688), and 2.34 (galaxy 101089).

</details>

<details>
<summary>Checkpoint viewer</summary>
<div id="payload-preserving-interactive-viewer"></div>

The viewer displays checkpoint spectra, residuals, ESS, logZ and the final posterior.

The shaded band shows the 16th to 84th percentile range of noiseless model spectra across 128 deterministic equal-weight draws. It represents parameter uncertainty, not measurement noise.

[Open the hosted checkpoint viewer](../ceridwen-checkpoint-spectrum-evolution/). The underlying nested sampling implementation and test modules remain available in the codebase:

- Generator script: [scripts/plot_ceridwen_checkpoint_evolution.py](/wiki/f/scripts/plot_ceridwen_checkpoint_evolution.py)
- Verification captures: [reports/ceridwen-checkpoint-animation/screenshots/](../../../../.claude/scripts/hermes-bridge/reports/ceridwen-checkpoint-animation/screenshots)
- Test suites: [test_plot_ceridwen_checkpoint_evolution.py](/wiki/f/tests/test_plot_ceridwen_checkpoint_evolution.py), [test_checkpoint_spectrum.py](/wiki/f/ceridwen/tests/test_checkpoint_spectrum.py), [test_ns_checkpoint.py](/wiki/f/ceridwen/tests/test_ns_checkpoint.py)
- Core sampler modules: [ceridwen/plotting/checkpoint.py](/wiki/f/ceridwen/ceridwen/plotting/checkpoint.py), [ceridwen/sampler/nested.py](/wiki/f/ceridwen/ceridwen/sampler/nested.py)
- Four-galaxy fit directory: [results/rtx-4070-super-four-galaxy-fits/](/wiki/f/results/rtx-4070-super-four-galaxy-fits)

</details>

<details>
<summary>Related fit runs and exploratory suites</summary>

Exploratory and benchmark fit runs accessible at directory level:

- [archive/results/refit-static-smoothing/](/wiki/f/archive/results/refit-static-smoothing) — Per-target refits using the static smoother.
- [archive/results/rtx-5090-integrated-fit/](/wiki/f/archive/results/rtx-5090-integrated-fit) — Executed single integrated photometry+spectra fit.
- [results/rtx-4070-super-four-galaxy-fits/](/wiki/f/results/rtx-4070-super-four-galaxy-fits) — Four-galaxy GPU validation run and checkpoint host.
- [archive/results/a100-feature-spectrum/](/wiki/f/archive/results/a100-feature-spectrum) — A100 feature spectrum test outputs.
- [archive/results/a100-integrated-fit-notebook/](/wiki/f/archive/results/a100-integrated-fit-notebook) — A100 integrated fit execution notebook.

</details>

<details>
<summary>Artifact catalog</summary>
<div id="complete-artifact-catalog-79-validated-items"></div>



</details>

| ID | Title / Deliverable | Category | Media Type | Wiki-Relative Link |
| --- | --- | --- | --- | --- |
| `board-current-html` | **Current Ceridwen results board** | board | `text/html` | [ceridwen-results.html](../ceridwen-results/) |
| `dr2-analysis-page` | **DR2 quiescent sample analysis** | analysis-page | `text/html` | [dr2-quiescent-sample.html](../dr2-quiescent-sample/) |
| `dr2-headline-png` | **DR2 age-redshift headline PNG** | final-figure | `image/png` | [dr2-quiescent-sample/headline-age-redshift.png](figures/dr2-quiescent-sample/headline-age-redshift.png) |
| `dr2-headline-pdf` | **DR2 age-redshift headline PDF** | final-figure | `application/pdf` | [dr2-quiescent-sample/headline-age-redshift.pdf](figures/dr2-quiescent-sample/headline-age-redshift.pdf) |
| `dr2-distributions-png` | **DR2 parameter distributions PNG** | final-figure | `image/png` | [dr2-quiescent-sample/distributions-1d.png](figures/dr2-quiescent-sample/distributions-1d.png) |
| `dr2-distributions-pdf` | **DR2 parameter distributions PDF** | final-figure | `application/pdf` | [dr2-quiescent-sample/distributions-1d.pdf](figures/dr2-quiescent-sample/distributions-1d.pdf) |
| `dr2-fit-quality-png` | **DR2 fit-quality diagnostics PNG** | final-figure | `image/png` | [dr2-quiescent-sample/fit-quality.png](figures/dr2-quiescent-sample/fit-quality.png) |
| `dr2-fit-quality-pdf` | **DR2 fit-quality diagnostics PDF** | final-figure | `application/pdf` | [dr2-quiescent-sample/fit-quality.pdf](figures/dr2-quiescent-sample/fit-quality.pdf) |
| `dr2-timescale-epoch-png` | **Formation timescale versus epoch PNG** | final-figure | `image/png` | [dr2-quiescent-sample/dt-vs-formation-epoch.png](figures/dr2-quiescent-sample/dt-vs-formation-epoch.png) |
| `dr2-timescale-epoch-pdf` | **Formation timescale versus epoch PDF** | final-figure | `application/pdf` | [dr2-quiescent-sample/dt-vs-formation-epoch.pdf](figures/dr2-quiescent-sample/dt-vs-formation-epoch.pdf) |
| `dr2-timescale-mass-png` | **Formation timescale versus mass PNG** | final-figure | `image/png` | [dr2-quiescent-sample/dt-vs-mass.png](figures/dr2-quiescent-sample/dt-vs-mass.png) |
| `dr2-timescale-mass-pdf` | **Formation timescale versus mass PDF** | final-figure | `application/pdf` | [dr2-quiescent-sample/dt-vs-mass.pdf](figures/dr2-quiescent-sample/dt-vs-mass.pdf) |
| `dr2-timescale-alpha-png` | **Formation timescale versus alpha enhancement PNG** | final-figure | `image/png` | [dr2-quiescent-sample/dt-vs-alpha.png](figures/dr2-quiescent-sample/dt-vs-alpha.png) |
| `dr2-timescale-alpha-pdf` | **Formation timescale versus alpha enhancement PDF** | final-figure | `application/pdf` | [dr2-quiescent-sample/dt-vs-alpha.pdf](figures/dr2-quiescent-sample/dt-vs-alpha.pdf) |
| `dr2-summary-csv` | **DR2 187-galaxy summary table** | data-summary | `text/csv` | [../../results/dr2-quiescent-summary.csv](/wiki/f/results/dr2-quiescent-summary.csv) |
| `dr2-production-results-dir` | **DR2 187-galaxy production result directory** | result-directory | `inode/directory` | [../../results/rtx-5060-dr2-quiescent-full-spectrum](/wiki/f/results/rtx-5060-dr2-quiescent-full-spectrum) |
| `chronometer-notebook` | **Ceridwen cosmic-chronometer notebook** | notebook | `application/x-ipynb+json` | [../../results/rtx-5060-dr2-quiescent-full-spectrum/ceridwen_cosmic_chronometer.ipynb](/wiki/f/results/rtx-5060-dr2-quiescent-full-spectrum/ceridwen_cosmic_chronometer.ipynb) |
| `chronometer-summary-h5` | **Ceridwen chronometer summary data** | data-summary | `application/x-hdf5` | [../../results/rtx-5060-dr2-quiescent-full-spectrum/ceridwen_cosmic_chronometer_summary.h5](/wiki/f/results/rtx-5060-dr2-quiescent-full-spectrum/ceridwen_cosmic_chronometer_summary.h5) |
| `dr2-summary-builder` | **DR2 summary-table builder** | analysis-script | `text/x-python` | [../../scripts/build_dr2_quiescent_summary.py](/wiki/f/scripts/build_dr2_quiescent_summary.py) |
| `dr2-headline-script` | **DR2 headline plotting script** | analysis-script | `text/x-python` | [../../archive/scripts/plot_dr2_headline_candidates.py](/wiki/f/archive/scripts/plot_dr2_headline_candidates.py) |
| `dr2-distribution-quality-script` | **DR2 distribution and quality plotting script** | analysis-script | `text/x-python` | [../../scripts/plot_dr2_distributions_quality.py](/wiki/f/scripts/plot_dr2_distributions_quality.py) |
| `dr2-timescale-script` | **DR2 formation-timescale plotting script** | analysis-script | `text/x-python` | [../../scripts/plot_dr2_formation_timescale.py](/wiki/f/scripts/plot_dr2_formation_timescale.py) |
| `borghi-age-redshift-png` | **Borghi-style median age versus redshift PNG** | final-figure | `image/png` | [../../results/figures/borghi2022-age-vs-z.png](/wiki/f/results/figures/borghi2022-age-vs-z.png) |
| `borghi-age-redshift-pdf` | **Borghi-style median age versus redshift PDF** | final-figure | `application/pdf` | [../../results/figures/borghi2022-age-vs-z.pdf](/wiki/f/results/figures/borghi2022-age-vs-z.pdf) |
| `borghi-source-table` | **Borghi DR2 matched age table** | source-data | `text/tab-separated-values` | [../../data/processed/borghi2022_legac_dr2/borghi2022_legac_dr2_spectrum_matches copy.tsv](/wiki/f/data/processed/borghi2022_legac_dr2/borghi2022_legac_dr2_spectrum_matches copy.tsv) |
| `borghi-plot-script` | **Borghi age-redshift plotting script** | analysis-script | `text/x-python` | [../../scripts/plot_borghi2022_age_vs_z.py](/wiki/f/scripts/plot_borghi2022_age_vs_z.py) |
| `absorption-analysis-page` | **Absorption-line mask analysis** | analysis-page | `text/html` | [absorption-line-mask.html](../absorption-line-mask/) |
| `absorption-feature-windows-png` | **Absorption feature windows PNG** | final-figure | `image/png` | [absorption-mask/feature_windows_M5_172669.png](figures/absorption-mask/feature_windows_M5_172669.png) |
| `absorption-mock-bias-png` | **Absorption-mask mock bias PNG** | final-figure | `image/png` | [absorption-mask/mock_bias_vs_tilt.png](figures/absorption-mask/mock_bias_vs_tilt.png) |
| `absorption-mock-width-png` | **Absorption-mask posterior-width PNG** | final-figure | `image/png` | [absorption-mask/mock_width_ratio.png](figures/absorption-mask/mock_width_ratio.png) |
| `absorption-real-posteriors-png` | **Absorption-mask real-target posteriors PNG** | final-figure | `image/png` | [absorption-mask/real_targets_posteriors.png](figures/absorption-mask/real_targets_posteriors.png) |
| `absorption-summary-csv` | **Absorption-mask numerical summary CSV** | data-summary | `text/csv` | [../../results/absorption-mask/summary.csv](/wiki/f/results/absorption-mask/summary.csv) |
| `absorption-summary-json` | **Absorption-mask numerical summary JSON** | data-summary | `application/json` | [../../results/absorption-mask/summary.json](/wiki/f/results/absorption-mask/summary.json) |
| `absorption-fisher-json` | **Absorption-mask Fisher analysis JSON** | data-summary | `application/json` | [../../results/absorption-mask/fisher_M5_172669.json](/wiki/f/results/absorption-mask/fisher_M5_172669.json) |
| `absorption-results-dir` | **Absorption-mask 45-fit result directory** | result-directory | `inode/directory` | [../../results/absorption-mask](/wiki/f/results/absorption-mask) |
| `absorption-analysis-script` | **Absorption-mask analysis script** | analysis-script | `text/x-python` | [../../scripts/absorption_mask_analysis.py](/wiki/f/scripts/absorption_mask_analysis.py) |
| `absorption-report-script` | **Absorption-mask report generator** | analysis-script | `text/x-python` | [../../scripts/absorption_mask_report.py](/wiki/f/scripts/absorption_mask_report.py) |
| `calibration-analysis-page` | **Calibration-polynomial and tilt-origin analysis** | analysis-page | `text/html` | [../../tmp/worktrees/astro-calibration-polynomial/wiki/analyses/ceridwen-calibration-polynomial.html](/wiki/f/tmp/worktrees/astro-calibration-polynomial/wiki/analyses/ceridwen-calibration-polynomial.html) |
| `calibration-explainer-png` | **Calibration-polynomial explainer PNG** | final-figure | `image/png` | [../../tmp/worktrees/astro-calibration-polynomial/wiki/analyses/calibration-polynomial-explainer.png](/wiki/f/tmp/worktrees/astro-calibration-polynomial/wiki/analyses/calibration-polynomial-explainer.png) |
| `calibration-mock-bias-png` | **Calibration-polynomial mock bias PNG** | final-figure | `image/png` | [../../tmp/worktrees/astro-calibration-polynomial/wiki/analyses/calibration-polynomial-mock-bias.png](/wiki/f/tmp/worktrees/astro-calibration-polynomial/wiki/analyses/calibration-polynomial-mock-bias.png) |
| `calibration-real-posteriors-png` | **Calibration-polynomial real-target posteriors PNG** | final-figure | `image/png` | [../../tmp/worktrees/astro-calibration-polynomial/wiki/analyses/calibration-polynomial-real-posteriors.png](/wiki/f/tmp/worktrees/astro-calibration-polynomial/wiki/analyses/calibration-polynomial-real-posteriors.png) |
| `calibration-vectors-png` | **Calibration-polynomial vectors PNG** | final-figure | `image/png` | [../../tmp/worktrees/astro-calibration-polynomial/wiki/analyses/calibration-polynomial-vectors.png](/wiki/f/tmp/worktrees/astro-calibration-polynomial/wiki/analyses/calibration-polynomial-vectors.png) |
| `tilt-origin-ibands-png` | **Tilt-origin in-band flux ratios PNG** | final-figure | `image/png` | [../../tmp/worktrees/astro-calibration-polynomial/wiki/analyses/calibration-polynomial-tilt-origin-ibands.png](/wiki/f/tmp/worktrees/astro-calibration-polynomial/wiki/analyses/calibration-polynomial-tilt-origin-ibands.png) |
| `tilt-origin-photometry-png` | **Tilt-origin photometric residuals PNG** | final-figure | `image/png` | [../../tmp/worktrees/astro-calibration-polynomial/wiki/analyses/calibration-polynomial-tilt-origin-photometry.png](/wiki/f/tmp/worktrees/astro-calibration-polynomial/wiki/analyses/calibration-polynomial-tilt-origin-photometry.png) |
| `tilt-origin-posteriors-png` | **Tilt-origin posterior comparison PNG** | final-figure | `image/png` | [../../tmp/worktrees/astro-calibration-polynomial/wiki/analyses/calibration-polynomial-tilt-origin-posteriors.png](/wiki/f/tmp/worktrees/astro-calibration-polynomial/wiki/analyses/calibration-polynomial-tilt-origin-posteriors.png) |
| `tilt-origin-vectors-png` | **Tilt-origin polynomial vectors PNG** | final-figure | `image/png` | [../../tmp/worktrees/astro-calibration-polynomial/wiki/analyses/calibration-polynomial-tilt-origin-vectors.png](/wiki/f/tmp/worktrees/astro-calibration-polynomial/wiki/analyses/calibration-polynomial-tilt-origin-vectors.png) |
| `tilt-origin-results-dir` | **Tilt-origin fit records** | result-directory | `inode/directory` | [../../tmp/worktrees/astro-calibration-polynomial/results/tilt-origin-2026-09-02](/wiki/f/tmp/worktrees/astro-calibration-polynomial/results/tilt-origin-2026-09-02) |
| `tilt-origin-analysis-notebook` | **Tilt-origin executed analysis notebook** | notebook | `application/x-ipynb+json` | [../../tmp/worktrees/astro-calibration-polynomial/results/tilt-origin-2026-09-02/analysis.ipynb](/wiki/f/tmp/worktrees/astro-calibration-polynomial/results/tilt-origin-2026-09-02/analysis.ipynb) |
| `tilt-origin-arms-csv` | **Tilt-origin fit-arm summary CSV** | data-summary | `text/csv` | [../../tmp/worktrees/astro-calibration-polynomial/results/tilt-origin-2026-09-02/arms.csv](/wiki/f/tmp/worktrees/astro-calibration-polynomial/results/tilt-origin-2026-09-02/arms.csv) |
| `tilt-origin-ibands-csv` | **Tilt-origin in-band flux-ratio CSV** | data-summary | `text/csv` | [../../tmp/worktrees/astro-calibration-polynomial/results/tilt-origin-2026-09-02/ibands.csv](/wiki/f/tmp/worktrees/astro-calibration-polynomial/results/tilt-origin-2026-09-02/ibands.csv) |
| `calibration-experiment-script` | **Calibration-polynomial experiment script** | analysis-script | `text/x-python` | [../../tmp/worktrees/astro-calibration-polynomial/scripts/calibration_polynomial_experiment.py](/wiki/f/tmp/worktrees/astro-calibration-polynomial/scripts/calibration_polynomial_experiment.py) |
| `calibration-photometry-download-script` | **LEGA-C aperture-photometry download script** | analysis-script | `text/x-python` | [../../tmp/worktrees/astro-calibration-polynomial/scripts/download_legac_dr2_aperture_photometry.py](/wiki/f/tmp/worktrees/astro-calibration-polynomial/scripts/download_legac_dr2_aperture_photometry.py) |
| `tilt-origin-runner-script` | **Tilt-origin runner script** | analysis-script | `text/x-python` | [../../tmp/worktrees/astro-calibration-polynomial/scripts/tilt_origin_runner.py](/wiki/f/tmp/worktrees/astro-calibration-polynomial/scripts/tilt_origin_runner.py) |
| `tilt-origin-vast-script` | **Tilt-origin Vast launcher** | analysis-script | `text/x-python` | [../../tmp/worktrees/astro-calibration-polynomial/scripts/tilt_origin_vast.py](/wiki/f/tmp/worktrees/astro-calibration-polynomial/scripts/tilt_origin_vast.py) |
| `calibration-local-superseded-dir` | **Superseded local calibration-polynomial snapshots** | result-directory | `inode/directory` | [../../archive/results/calibration-polynomial-2026-09-02](/wiki/f/archive/results/calibration-polynomial-2026-09-02) |
| `static-smoothing-refits-dir` | **Static-smoothing refit results** | result-directory | `inode/directory` | [../../archive/results/refit-static-smoothing](/wiki/f/archive/results/refit-static-smoothing) |
| `rtx5090-integrated-fit-dir` | **RTX 5090 integrated fit result** | result-directory | `inode/directory` | [../../archive/results/rtx-5090-integrated-fit](/wiki/f/archive/results/rtx-5090-integrated-fit) |
| `rtx4070-four-fit-dir` | **RTX 4070 Super four-galaxy fits** | result-directory | `inode/directory` | [../../results/rtx-4070-super-four-galaxy-fits](/wiki/f/results/rtx-4070-super-four-galaxy-fits) |
| `a100-feature-spectrum-dir` | **A100 feature-spectrum result** | result-directory | `inode/directory` | [../../archive/results/a100-feature-spectrum](/wiki/f/archive/results/a100-feature-spectrum) |
| `a100-integrated-notebook-dir` | **A100 integrated-fit notebook result** | result-directory | `inode/directory` | [../../archive/results/a100-integrated-fit-notebook](/wiki/f/archive/results/a100-integrated-fit-notebook) |
| `checkpoint-interactive-html` | **Interactive checkpoint spectrum evolution** | interactive-html | `text/html` | [checkpoint-animation/ceridwen-checkpoint-spectrum-evolution.html](../ceridwen-checkpoint-spectrum-evolution/) |
| `checkpoint-screenshots-dir` | **Interactive checkpoint browser screenshots** | validation-evidence | `inode/directory` | [../../../../.claude/scripts/hermes-bridge/reports/ceridwen-checkpoint-animation/screenshots](../../../../.claude/scripts/hermes-bridge/reports/ceridwen-checkpoint-animation/screenshots) |
| `checkpoint-generator-script` | **Checkpoint spectrum animation generator** | analysis-script | `text/x-python` | [../../scripts/plot_ceridwen_checkpoint_evolution.py](/wiki/f/scripts/plot_ceridwen_checkpoint_evolution.py) |
| `checkpoint-generator-test` | **Checkpoint viewer output tests** | validation-test | `text/x-python` | [../../tests/test_plot_ceridwen_checkpoint_evolution.py](/wiki/f/tests/test_plot_ceridwen_checkpoint_evolution.py) |
| `checkpoint-prediction-module` | **Ceridwen checkpoint prediction module** | implementation | `text/x-python` | [../../ceridwen/ceridwen/plotting/checkpoint.py](/wiki/f/ceridwen/ceridwen/plotting/checkpoint.py) |
| `checkpoint-sampler-module` | **Ceridwen nested-sampler checkpoint serialization** | implementation | `text/x-python` | [../../ceridwen/ceridwen/sampler/nested.py](/wiki/f/ceridwen/ceridwen/sampler/nested.py) |
| `checkpoint-spectrum-test` | **Checkpoint spectrum correctness tests** | validation-test | `text/x-python` | [../../ceridwen/tests/test_checkpoint_spectrum.py](/wiki/f/ceridwen/tests/test_checkpoint_spectrum.py) |
| `checkpoint-serialization-test` | **Nested-sampler checkpoint compatibility tests** | validation-test | `text/x-python` | [../../ceridwen/tests/test_ns_checkpoint.py](/wiki/f/ceridwen/tests/test_ns_checkpoint.py) |
