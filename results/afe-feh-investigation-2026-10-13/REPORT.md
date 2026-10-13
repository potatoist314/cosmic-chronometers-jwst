# Why the DR2 refit gives [α/Fe] ≈ 0 falling with σ, and [Fe/H] rising with σ

Fits: `results/dr2-refit-2026-10-12/` (135 LEGA-C DR2 quiescent galaxies, October production defaults). Worker afe-research, 2026-10-13. No paid steps.

## Summary

The spectrum, not the photometry, sets [α/Fe], and it does so as a whole-spectrum compromise: the data have deeper Mg b and deeper C/N features (CN4150, C2 4668) than any model on the lockstep-α grid, and raising [α/Fe] on that grid deepens Mg b but weakens the many C- and Fe-sensitive pixels, so the fit settles near 0 with Mg b under-predicted by 3σ. High-σ galaxies have the strongest C/N excess, so they are pulled lowest; that makes the [α/Fe]–σ and [α/Fe]–mass trends and lifts [Fe/H] in compensation.
On top of this, rest-frame coverage drives a strong redshift trend (ρ = −0.47, the strongest correlate): Mg b and Fe5270 leave the VIMOS window above z ≈ 0.72 while the rest-UV enters, and the UV pixels prefer the −0.2 grid edge.
The [Fe/H]–σ trend has the literature sign and is partly real, but its amplitude is inflated by a within-galaxy σ–Z covariance and by the lower [α/Fe] at high σ.
Grid interpolation, grid edges, the resolution convention, free σ, calibration order and posterior degeneracy are ruled out as drivers. The reported [Fe/H] is a formed-mass-weighted iron abundance, so the published SSP-equivalent [Z/H] values are offset from it by construction.

## What the refit shows (135 fits)

| quantity | median | 16–84 | per-galaxy posterior half-width |
|---|---|---|---|
| [α/Fe] | −0.031 | −0.189 … +0.134 | 0.030 |
| [Fe/H] | −0.288 | −0.557 … −0.117 | 0.048 |

Spearman ρ (p):

| pair | ρ | partial ρ (controls) |
|---|---|---|
| [α/Fe] vs z | −0.47 (1e-8) | −0.45 (σ, mass; 4e-8) |
| [α/Fe] vs log σ | −0.32 (1e-4) | −0.15 (z, mass; 0.09) |
| [α/Fe] vs log M | −0.34 (4e-5) | −0.15 (z, σ; 0.08) |
| [α/Fe] vs [Fe/H] | −0.26 (2e-3) | |
| [Fe/H] vs log σ | +0.34 (4e-5) | +0.31 (z, mass; 2e-4) |
| [Fe/H] vs z | −0.18 (0.04) | −0.17 (σ, mass; 0.04) |

Median [α/Fe] by z bin (<0.65, 0.65–0.72, 0.72–0.80, >0.80; n 13/46/37/39): +0.10, +0.05, −0.04, −0.17.
Median [α/Fe] by σ bin (<175, 175–215, 215–250, >250 km/s; n 37/43/31/24): +0.02, +0.05, −0.04, −0.19.
30% of galaxies have [α/Fe] q16 below −0.18, i.e. the posterior touches the −0.2 grid edge.

Published comparison values for the same kind of galaxies: Bevacqua et al. 2023 (LEGA-C, σ-binned stacks and individual fits with Lick indices, nominal R ≈ 2500, §2) find mean [α/Fe] = +0.24 with 91% supersolar and no significant σ or mass trend (§4.1–4.2; per-galaxy errors ≈ 0.16 dex, comparable to the scatter 0.17, so trends are undetectable at that precision). Borghi et al. 2022a (LEGA-C DR2, Lick indices without Mg b, §2–3) find median [α/Fe] = +0.12 on the 48 galaxies in common. Beverage et al. 2023 (LEGA-C, alf full-spectrum fits, §3) find [Mg/Fe] ≈ 0.2–0.3 with a positive σ trend (§4).

## Ranked explanations

### 1. Lockstep-α model without free C/N, fitted over the whole spectrum — supported, primary

**Test.** (a) Conditional χ² profiles at the maximum-likelihood sample for all 135 galaxies, scanning [α/Fe] over the grid (−0.2…0.6) with everything else fixed, split into photometry, spectrum and eight rest-frame regions. (b) Weighted mean (obs − model)/model and summed pull/√n inside the Lick bandpasses of `ceridwen/observation/absorption_features.py` (Worthey et al. 1994; Trager et al. 1998 definitions) for all fits. (c) Maximum-a-posteriori refits from the joint ML sample with the likelihood restricted to spectrum-only, photometry-only, feature-pixels-only and continuum-pixels-only (8 galaxies, `map_fit`, 3000 steps).

**Numbers.**
- Spectrum χ² alone prefers the −0.2 edge in 92% of galaxies, and the median preferred [α/Fe] is −0.2 in every region except 5100–5400 Å (Mg b, Fe5270), where the median is 0.0. Photometry prefers [α/Fe] within 0.1 of the joint fit in 96% of galaxies. Moving +0.2 dex costs the spectrum +260 χ² and the photometry +45.
- Line residuals (negative = model too weak), medians over the fits with the line in range: Mg b −1.44% (16–84: −2.81 … −0.53; pull −3.28; n 61), C2 4668 −1.27% (pull −3.62; n 117), CN4150 −1.01% (pull −1.59; n 133), Fe5335 −0.40%, Fe4383 −0.24%. Model too deep in G4300 +1.06% (pull +1.70), H8 +1.47%, HγA +0.59%, Hβ +0.47%. Non-feature continuum pixels: +0.15% (pull +0.92).
- By σ tercile (low/mid/high): Mg b pull −2.1 / −3.0 / −4.2; C4668 pull −3.3 / −3.4 / −5.1; CN4150 depth −0.3% / −1.1% / −1.4%; partial ρ(carbon pull, log σ | z) = −0.26 (p 2e-3).
- Spectrum-only MAP reproduces the joint [α/Fe] (median |Δ| 0.005, 8 galaxies); photometry-only MAP is unconstrained (median Δ +0.10, hits bounds). Feature-only versus continuum-only MAPs are inconclusive (median |Δ| 0.16, both signs, dust at bounds).

**Why this gives the observed pattern.** On the grid in use ([Park 2025] aMIST + C3K models; grid attrs `~/.ceridwen/grids/amist_c3k_hr_krou_afe_nebular.h5`) all α elements move together and C and N are not varied (Park 2025 §2.4). Park 2025 §3.2.3 and conclusions 3–4 show that at fixed [Fe/H], raising α strengthens Ca4227, Mg b and TiO but weakens CN2, G4300, Fe4383, C2 4668, the Fe indices and the Balmer lines. The data need deeper Mg b and deeper CN/C2 at once; a lockstep model cannot do both, so the fit picks the [α/Fe] that minimises the total over thousands of pixels, leaving Mg b 3σ too shallow. Massive quiescent galaxies have enhanced C and N relative to Fe (Conroy, Graves & van Dokkum 2014 §5.1; Beverage et al. 2023 §4), so the carbon pull, and hence the downward push on [α/Fe], grows with σ. This reproduces the sign of the σ and mass trends and the near-zero mean. The published Ceridwen paper (Stoffers et al. 2026, §6.5) describes the α signature as a broad-band continuum depression of up to ~20% and reports mock [α/Fe] coverage of 0.50/0.72 with mean |pull| 1.06 and a Z–α posterior correlation of −0.56, so the method is known to be sensitive to the continuum shape, not to the Mg b line alone.

**Verdict.** Supported. The only test that would settle it is a refit with element response functions (free C, N, Mg) or a continuum-matched, Mg b-weighted likelihood; both change the model and were not run.

### 2. Rest-frame coverage changes with redshift — supported, primary for the z trend

**Test.** Per-galaxy rest-frame window from the stored fitted mask (`coverage.csv`); split by whether Mg b (5160–5193 Å) lies inside the fitted range; partial correlations; region-wise χ² preferences and the σ push per region.

**Numbers.**
- Mg b inside the fitted range: 60 galaxies, median [α/Fe] +0.087; outside: 75, median −0.16. At z 0.66–0.78, where both occur: +0.077 (43) vs −0.108 (34). Partial ρ([α/Fe], Mg b present | z, σ, mass) = +0.49 (p 2e-9).
- [α/Fe] vs the red edge of the window | z: ρ +0.29 to +0.35. The z trend persists at fixed coverage (partial −0.46), so coverage explains part, not all, of it.
- Regions entering at high z prefer the edge: <3700 Å median preference −0.2 (62 galaxies; χ² range 92), 3700–4000 Å −0.2 (107; range 248). The 5100–5400 Å region is the only one preferring 0.0 (66 galaxies).
- The σ push by region: the <3700 Å and 3700–4000 Å pixels want +30 and +20 km/s broader lines than the joint value; 5100–5400 Å wants −20 km/s. Both regions sit at the VIMOS window edges. Over the sample, (σ_fit − σ_DR2)/err has median +0.27, 15% above +2σ, and correlates with z (+0.47) and anticorrelates with [α/Fe] (−0.49).

**Verdict.** Supported. The LEGA-C window (6332–8900 Å nominal; per-mask extremes 6092–6754 Å blue edge, 8537–9229 Å red edge in these fits) puts Mg b beyond the red edge above z ≈ 0.72. Borghi et al. 2022a's [α/Fe] has no z trend on the same 48 galaxies (ρ −0.01), whereas (Ceridwen − Borghi) [α/Fe] falls with z (ρ −0.46, p 9e-4): the trend is in this fit, not in the galaxies. What would test it further: refit the 60 Mg b-covered galaxies with the window truncated to the high-z coverage and compare.

### 3. [Fe/H]–σ trend: partly real, amplitude inflated — supported

**Test.** Partial correlations; within-galaxy posterior covariance (weighted by nested-sampling `log_weights`) between logzsol and σ, mass, age; the September fixed-σ run on the same 135 galaxies.

**Numbers.**
- Partial ρ([Fe/H], log σ | z, mass) = +0.31 (p 2e-4). The literature sign is the same: Gallazzi et al. 2026a (LEGA-C, light-weighted, §5.2 and Table 1) find a Z–σ slope of 1.2 ± 0.2 with log⟨Z/Z☉⟩ = 0.42 at σ = 10^2.4 km/s; Nersesian et al. 2025 (§5) find ρ = 0.33 for quiescent galaxies; Beverage et al. 2023 (§4) find [Fe/H] rising with σ.
- Within a galaxy the posterior has r(logzsol, σ) = +0.25 and d[Fe/H]/dσ ≈ 0.0024 dex per km/s, r(logzsol, log M) = −0.53, r(logzsol, age) = −0.53. The sample-wide σ push (above) is itself positive and larger at high σ, so some of the across-sample [Fe/H]–σ slope is this covariance.
- [α/Fe] and [Fe/H] anticorrelate across the sample (−0.26) with a slope (−0.21) matching the within-galaxy direction (r −0.21, slope −0.18): where explanation 1 pulls [α/Fe] down, [Fe/H] rises to keep the metal-line strength.
- The September run (σ fixed to the DR2 value, constant Z, order-3 calibration, 187 galaxies, `results/dr2-quiescent-new-defaults-summary.csv`) gives [α/Fe] vs σ ρ −0.43 and vs [Fe/H] −0.49 on the same 135, so the trend does not come from free σ.

**Verdict.** Supported as partly real with inflated amplitude. What would test the amplitude: refit at σ fixed to DR2 with the October model, or compare light-weighted ⟨Z⟩ from the stored metallicity histories against Gallazzi's light-weighted values.

### 4. The reported [Fe/H] is not the published [Z/H] — supported, convention only

**Test.** Read the transforms and grid metadata; compare with Borghi et al. 2022a on the 48 overlapping galaxies.

**Numbers.**
- `ceridwen/model/transforms.py` (`mass_mapped_zh`, `mass_mapped_beta`): the metallicity history is Z(m) = Z_f − (Z_f − Z_0)(1 − m)^α (Gallazzi et al. 2026 Table 1 form); the reported `logzsol` is log10 of the formed-mass-weighted linear ⟨Z⟩, with Z_0 = min(Z☉/50, ⟨Z⟩). The grid axis is [Fe/H] (`feh_to_logZ` attribute: log10 Z = [Fe/H] + log10 Z☉, Z☉ = 0.0185), so the quantity is a mass-weighted [Fe/H].
- Total metallicity on this grid is [Z/H] = [Fe/H] + log10(1 − x + x·10^[α/Fe]) with x = 0.6875 (`ceridwen/ssps/grid_metadata.py`, `f_alpha`): +0.147 dex at [α/Fe] = +0.2, −0.127 at −0.2.
- Versus Borghi et al. 2022a (TMJ SSP-equivalent [Z/H], 48 galaxies): [Fe/H] ρ +0.36 (p 0.01), median offset −0.295; converted to [Z/H] the offset is −0.269 (ρ 0.18); age ρ +0.46, Ceridwen older by 0.79 Gyr; [α/Fe] ρ −0.26 (p 0.08), offset −0.157. Borghi's baseline index set lacks Mg b, and their Combo 3 test suggests their [α/Fe] is underestimated by ~0.1 (Appendix C, Fig. C1).

**Verdict.** Supported as a bookkeeping difference that explains the [Fe/H] offset, not the trends. Bevacqua et al. 2023 and Borghi et al. 2022a report SSP-equivalent [Z/H] from Lick indices; Beverage et al. 2023 report light-weighted alf abundances; none is the mass-weighted ⟨[Fe/H]⟩ Ceridwen reports.

### 5. Ruled out

| explanation | test | numbers | verdict |
|---|---|---|---|
| Grid interpolation or duplicate planes | Interpolation error of the linear afe interpolation at 0.2 spacing vs the size of the afe effect; checked plane hashes | 0.2% rms error vs ~10% rms afe signal; no duplicate planes; the only refused cell on the base grid is logzsol (+0.25, +0.5] × afe (+0.4, +0.6] (`results/ceridwen-upstream-merge-2026-10-10/REPORT.md`), far from the fits; Park 2025's low-mass isochrone copying affects only M < 0.5 M☉ at [Fe/H] ≥ +0.25 | ruled out |
| Resolution convention (header R = 2500 vs the R ≈ 3500 quoted by Gallazzi 2026a §2, Borghi 2022a §2, Nersesian 2025 §2) | Joint MAP at R = 2500 and R = 3500, 8 galaxies spanning z 0.61–0.97 | Δ[α/Fe] median +0.0001, max 0.005; Δlogzsol −0.0006, max 0.014; Δσ +0.35 km/s, max 1.3 (the broadening kernel `sigma_cont² = sigma_gal² + sigma_inst² − sigma_lib²`, `ceridwen/broadening.py`, absorbs the difference into σ) | ruled out |
| Posterior degeneracy | Weighted within-fit correlations | r([α/Fe], logzsol) −0.21, r([α/Fe], σ) −0.06, r([α/Fe], age) −0.03, r([α/Fe], τ) −0.08; posterior half-widths 0.03 ([α/Fe]) and 0.05 ([Fe/H]) are far smaller than the 0.3-dex across-sample spread | ruled out as a driver |
| Free σ | September fixed-σ run on the same galaxies | same trends (σ ρ −0.43; z ρ −0.33); Oct − Sept median Δ[α/Fe] −0.007; rank correlation 0.74 | ruled out |
| Calibration polynomial order | Sept order 3 vs Oct order 10 | same [α/Fe] within 0.007 median | ruled out |
| Upstream Z convention (logzsol vs [Fe/H]) | Bitwise checks in the merge ledger | Z→logzsol = [Fe/H] on this grid; no shift in afe (`results/ceridwen-upstream-merge-2026-10-10/LEDGER.md`) | ruled out |
| Prior edge pile-up as cause rather than symptom | Fraction of posterior mass below −0.19 | 15% of galaxies have >50% mass below −0.19; the uniform prior spans the grid, so the edge truncates, it does not pull | symptom of 1–2 |
| Photometry driving [α/Fe] | photometry-only MAP and photometry χ² profile | unconstrained MAP; photometry χ² range 500 vs spectrum 1351, and photometry prefers the joint value | ruled out |

### 6. Untested, and what would test them

- **Free C/N (or Mg) response functions.** Fit with alf-style element responses or a C/N-enhanced grid; prediction: Mg b residual closes, [α/Fe] rises to ≈ +0.2 and the σ trend flattens or reverses. Needs a model change (not granted).
- **Continuum-normalised, line-weighted likelihood.** Weight or restrict to the Lick bandpasses with the marginalised calibration polynomial fixed; the feature-only MAP here was inconclusive because dust hit its bounds. Needs a likelihood change.
- **Coverage control refit.** Refit the 60 Mg b-covered galaxies with their red edge truncated to 5100 Å rest; prediction: [α/Fe] drops by ≈ 0.2. Ten short CPU MAPs would show the direction; full posteriors need GPU.
- **Hierarchical stack.** Stack the posteriors in σ bins and compare with Bevacqua et al. 2023's stacked values at matched σ.
- **Light-weighted ⟨Z⟩.** Compute from the stored metallicity histories and compare with Gallazzi et al. 2026a's Z–σ relation directly.

## Evidence

Inputs read: `results/dr2-refit-2026-10-12/*/run/fits/fit/*/ceridwen_result.h5` and `ceridwen_derived_outputs.h5`; `results/dr2-refit-2026-10-12/dr2-refit-summary.csv`; `results/dr2-quiescent-new-defaults-summary.csv`; `data/processed/borghi2022_legac_dr2/`; `wiki/notes/absorption-line-mask.md`; `wiki/notes/model.md`; `results/ceridwen-upstream-merge-2026-10-10/`; `~/.ceridwen/grids/amist_c3k_hr_krou_afe_nebular.h5` attributes; `ceridwen/ceridwen/{model/transforms.py,broadening.py,csp/csp_afe.py,ssps/grid_metadata.py,observation/absorption_features.py}`; local paper texts in `papers/` (Park 2025; Bevacqua et al. 2023, 2024; Beverage et al. 2021, 2023; Gallazzi et al. 2026a; Conroy, Graves & van Dokkum 2014; Borghi et al. 2022a; Nersesian et al. 2025; Stoffers et al. 2026).

Computations were local CPU only (per-pixel χ² at stored samples, weighted posterior statistics, 48 short MAP refits across 8 galaxies). Scratch scripts and CSVs are not committed.
