---
kind: experiment
id: e-emission-line-marginalisation
title: Emission-line marginalisation from upstream Ceridwen, integrated into the calibration solve
date: 2026-09-22
results_at:
origin: new
status: planned
question: q-emission-lines
follow_up:
---

## Context

Upstream Ceridwen `be852282` (v1.0.2) marginalises emission-line fluxes analytically. It refuses photometry with a sampled \(z\), and its joint likelihood bypasses the fork's `PolynomialCalibration`. The fork now puts the lines into the calibration solve instead.

## Before delegation

```json
[
  {
    "date": "2026-09-22",
    "text": "a new ceridwen update upstream has added marginalisation for accounting for emission lines - can you pull and add this feature while keeping all the speedups i have",
    "display_text": "A new Ceridwen update upstream has added marginalisation for accounting for emission lines. Can you pull and add this feature while keeping all the speedups I have?"
  },
  {
    "date": "2026-09-22",
    "text": "not just speedup, i would just like to integrate the extra marginalisation feature without changing anything else",
    "display_text": "Not just speedup; I would just like to integrate the extra marginalisation feature without changing anything else."
  },
  {
    "date": "2026-09-22",
    "text": "yeah, go ahead with compatibility work",
    "display_text": "Yeah, go ahead with compatibility work."
  },
  {
    "date": "2026-09-22",
    "text": "i just want the most seamless integration of emission line marginalisation",
    "display_text": "I just want the most seamless integration of emission line marginalisation."
  },
  {"date": "2026-09-23", "text": "just do a eline test right now, with higher spend"}
]
```

## Execution plan

- GPU test: `eline_off` and `eline_on` on M1_210210, same instance and seed 20260832.
- Defaults in both arms: COSMOS2025 photometry, Chebyshev order 10, constant prior 0.3, baked runtime.
- Controlled change: `eline_on` sets `SETTINGS["emission_line_marginalisation"]` to `True`.
- Compute: one RTX 5060 or 5060 Ti at up to $0.20/h, reliability above 99.5%, total cap $0.50.
- Compare fitted line fluxes, parameter shifts, Hbeta-region residuals, wall time, and likelihood calls.

- Model: \(y = P(a)\,\mu + \sum_k f_k L_k\). Coefficients \(a\) keep their priors (0.3 for \(a_0\), 0.1 for \(a_1 \ldots a_{10}\)). Line fluxes: flat prior on \(f_k \ge 0\).
- Marginal = unconstrained Gaussian integral \(\times\, P(f \ge 0)\) under the line-flux posterior. \(P\): product of \(\Phi(\hat f_k/\sigma_k)\); exact bivariate (Genz 2004) for blends with \(|\rho| > 0.5\).
- Posterior draws of \(f\): truncated at 0 (Gibbs, 1000 sweeps).
- Tied doublets (same upper level, ratio from FSPS `ZAU_ND_mist.lines`): [O III] 5007/4959 = 3.010, [Ne III] 3869/3968 = 3.318; also [N II] 6584/6548 = 2.951, [O I] 6300/6363 = 3.136, [S III] 9532/9069 = 2.480 when in range. One flux per doublet, \(\ge 0\).
- [O II] 3726/3729 and [S II] 6716/6731 stay free: their ratios depend on gas density (1.33–1.38 for [O II] across the FSPS grid).
- Option on: \(z\) fixed at \(z_{\mathrm{cat}}\); the same line fluxes enter the photometry (band flux of each line, sedpy normalisation) and one solve covers spectrum and photometry.
- \(L_k\): unit-flux Gaussian in \(\ln\lambda\) at the FSPS vacuum rest wavelength times \(1+z\). Width \(\sqrt{\sigma_{\mathrm{gas}}^2 + \sigma_{\mathrm{inst}}^2}\); \(\sigma_{\mathrm{gas}}\) is the sampled \(\sigma_\star\), as upstream.
- Lines: FSPS `emlines_info.dat` lines 3\(\sigma\) inside the spectrum, 3 or more unmasked pixels within 2\(\sigma\), tested at \(z_{\mathrm{cat}}\). Upstream tests the \(z\)-prior ends; at \(z_{\mathrm{cat}}+0.1\), [O III] 5007 falls past the last unmasked pixel.
- A \(10^{-12}\) ridge on each line's precision keeps the solve finite for a line with no unmasked pixels.
- Lines are added after the polynomial. The fractional noise term uses \(\mu\) without the lines.
- Setting `emission_line_marginalisation`, default `False`. When `True`, modelled lines leave the emission mask.
- Code: `ceridwen/ceridwen/likelihood/emission_lines.py`, `PolynomialCalibration.calibrate_with_lines`, `DiagonalGaussianLikelihood(emission_lines=...)`; ceridwen `6fc7539`, positivity `7f18311`, ties and photometry `0f0895f`.
- First GPU fit: M1_210210 with the option on; waits for Liu Hao's approval.

## Amendments

```json
[
  {
    "date": "2026-09-23",
    "text": "make it strictly positive, negative absorption should already be modelled no",
    "display_text": "Make it strictly positive; negative absorption should already be modelled, no?"
  },
  {
    "date": "2026-09-23",
    "text": "yeah, tie the oxygen lines. i'm okay to fix redshift.",
    "display_text": "Yeah, tie the oxygen lines. I'm okay to fix redshift."
  }
]
```

## Runs

```json
[
  {
    "id": "m1-210210-lines-off",
    "arm": "eline_off",
    "status": "planned",
    "target": "M1_210210"
  },
  {
    "id": "m1-210210-lines-on",
    "arm": "eline_on",
    "status": "planned",
    "target": "M1_210210"
  }
]
```

## Figures

```json
[]
```

## Measurements

| Check | Measurement |
| --- | --- |
| Option off against the code before it, joint \(\ln L\) at 20 M1_210210 posterior draws | bit-identical (`tests/test_emission_line_marginalisation.py`) |
| Zero line columns against the polynomial marginalisation | equal to \(10^{-8}\) in \(\ln L\) (`ceridwen/tests/test_emission_line_columns.py`) |
| Joint marginal against quadrature over \(f \ge 0\), one line | equal to \(10^{-6}\) in \(\ln L\) |
| Injected positive lines on a synthetic spectrum | recovered within 3\(\sigma\); redshift to \(10^{-4}\) |
| Synthetic pure stellar absorption, also twice too deep in the data | flux draws \(\ge 0\), mean below 1.5\(\sigma\) |
| Lines fitted for M1_210210 | 24 lines, 22 free fluxes, 3798–5200 \(\text{\AA}\) rest; blended pairs [O II] 3867/[Ne III] 3869, He I 3889/H8 |
| Tied ratio in 200 truncated posterior draws | [O III] 5007/4959 = 3.010, [Ne III] 3869/3968 = 3.318, to \(10^{-12}\) |
| Band flux per line against the narrow-line AB formula | within 0.2 % (1 km s\(^{-1}\) width) |
| Band change from the lines, median over 20 draws | r+ 0.30 %, i+ 0.19 %, z+ 0.03 %, other bands 0.000 % |
| Spectrum and photometry sharing one flux, against quadrature | equal to \(10^{-6}\) in \(\ln L\) |
| Fitted pixels, off / on | 3523 / 3926 |
| Free parameters, off / on | 9 / 8 (\(z\) fixed) |
| \(\ln P(f \ge 0)\), exact (scipy, 22-d) over 20 draws | median −46.9, range −57.7 to −44.3 |
| Implemented minus exact \(\ln P\) | mean −0.57, standard deviation 0.07, max \(\lvert\Delta\rvert\) 0.76 |
| Plain product of \(\Phi\) minus exact | mean +1.05, standard deviation 0.27 |
| Line-dependent noise minus \(\mu\)-only noise, \(\Delta\ln L\) over 20 draws | mean −0.39, standard deviation 0.12, max \(\lvert\Delta\rvert\) 0.57 |
| CPU time, 20 draws per `jit(vmap)` call, off / on | 4.0 / 11.1 ms (Apple CPU, jax x64) |

## Caveats

- With the flat prior, \(\ln Z\) changes by a constant per line; do not compare the evidence with masked fits.
- The implemented \(\ln P\) ignores the weak correlations (0.05–0.12) outside the blended pairs; this gives the −0.57 offset.
- FSPS "[O II] 3867" (3868.16 \(\text{\AA}\), zero Cloudy flux, no NIST line) is excluded (ceridwen `1fae781`): 21 free fluxes, blend He I 3889/H8 only; implemented minus exact \(\ln P\) −0.60 ± 0.07.

## References

- Upstream: [Espe13/ceridwen be852282](https://github.com/Espe13/ceridwen/commit/be8522829e0cfde7c2c8f99af80b5ec1147fb5ae), `ceridwen/likelihood/eline_marginal.py`
- Fork: [potatoist314/ceridwen 6fc7539](https://github.com/potatoist314/ceridwen/commit/6fc7539383c725e1de037dfb8d035955cc0f2c3b)
- Notebook: `notebooks/ceridwen_integrated_photometry_spectra.ipynb`
- Reference draws: `results/m1-210210-reference/tau-1/poly10/210210-M1_210210/ceridwen_result.h5`
- Question: [q-emission-lines](wiki/research/questions/q-emission-lines.md)

## Your interpretation

```json
[]
```

## Next decision

```json
[]
```
