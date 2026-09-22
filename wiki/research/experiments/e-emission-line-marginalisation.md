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
  }
]
```

## Execution plan

- Model: \(y = P(a)\,\mu + \sum_k f_k L_k\). Coefficients \(a\) keep their priors (0.3 for \(a_0\), 0.1 for \(a_1 \ldots a_{10}\)). Line fluxes \(f_k\) have a flat prior, as upstream. One Gaussian integral covers both.
- \(L_k\): unit-flux Gaussian in \(\ln\lambda\) at the FSPS vacuum rest wavelength times \(1+z\). Width \(\sqrt{\sigma_{\mathrm{gas}}^2 + \sigma_{\mathrm{inst}}^2}\); \(\sigma_{\mathrm{gas}}\) is the sampled \(\sigma_\star\), as upstream.
- Lines: FSPS `emlines_info.dat` lines inside the spectrum at \(z_{\mathrm{cat}}\) and \(z_{\mathrm{cat}} \pm 0.1\), 3\(\sigma\) from the edges, with 3 or more unmasked pixels within 2\(\sigma\) (upstream rules).
- Lines are added after the polynomial. The fractional noise term uses \(\mu\) without the lines.
- Photometry has no lines. A 1 \(\text{\AA}\) equivalent-width line changes a filter over 1000 \(\text{\AA}\) wide by under 0.1 %; the floor is 5 %.
- Setting `emission_line_marginalisation`, default `False`. When `True`, modelled lines leave the emission mask.
- Code: `ceridwen/ceridwen/likelihood/emission_lines.py`, `PolynomialCalibration.calibrate_with_lines`, `DiagonalGaussianLikelihood(emission_lines=...)`; ceridwen `6fc7539`.
- First GPU fit: M1_210210 with the option on; waits for Liu Hao's approval.

## Amendments

```json
[]
```

## Runs

```json
[
  {
    "id": "m1-210210-lines-on",
    "arm": "emission-line-marginalisation",
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
| Joint marginal against quadrature over one line flux | equal to \(10^{-6}\) in \(\ln L\) |
| Injected lines on a synthetic spectrum | recovered within 3\(\sigma\); redshift recovered to \(10^{-4}\) |
| Lines fitted for M1_210210 | 10: [S II] 4070, 4078, H\(\delta\), [O III] 4363, He I 4471, He II 4686, [Ar IV] 4711, [Ne IV] 4720, [Ar IV] 4740, H\(\beta\) |
| Fitted pixels, off / on | 3523 / 3657 (H\(\beta\) unmasked) |
| Line-dependent noise minus \(\mu\)-only noise, \(\Delta\ln L\) over 20 draws | mean −0.41, standard deviation 0.05, max \(\lvert\Delta\rvert\) 0.49 |
| Rest-frame \(\lvert\mathrm{EW}\rvert\) of the solved lines | median 0.19 \(\text{\AA}\), max 0.47 \(\text{\AA}\) |
| CPU time, 20 draws per `jit(vmap)` call, off / on | 3.7 / 5.8 ms (Apple CPU, jax x64) |

## Caveats

- With the flat prior, \(\ln Z\) changes by a constant per line; do not compare the evidence with masked fits.
- The flat prior allows negative fluxes. H\(\delta\) and H\(\beta\) columns overlap the stellar Balmer absorption.

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
