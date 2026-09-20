---
kind: experiment
id: e-m1-210210-reference
title: M1_210210 reference fit at calibration order 10
date: 2026-09-17
origin: new
status: results-ready
question: q-fitting-choices
follow_up:
---

## Context

M1_210210 was chosen on 17 Sep 2026 for fitting under roadmap item strong-spectrum: LEGA-C DR2, \(z = 0.6542\), \(\sigma_\star = 260\,\mathrm{km/s}\), catalogue S/N 62.2, ranking third by S/N among 187 quiescent galaxies. It has Dn4000 1.817, HdeltaA 0.418 and Fe4383 3.455, and belongs to the Borghi et al. 2022 overlap. The production fit at `results/dr2-quiescent-new-defaults/210210-M1_210210` used Chebyshev calibration order 3; order 10 became the default on 17 Sep 2026, and no order-10 fit exists for this galaxy.

## Before delegation

```json
[
  {
    "date": "2026-09-17",
    "text": "i want to fix on a single high S/N galaxy with strong absorption features from now on as well (210210?) - this is the current roadmap trajectoy.",
    "display_text": "I want to fix on a single high S/N galaxy with strong absorption features from now on as well (210210?) - this is the current roadmap trajectory."
  },
  {
    "date": "2026-09-17",
    "text": "order 10 has speedups implmented and should be the default for future fits.",
    "display_text": "Order 10 has speed-ups implemented and should be the default for future fits."
  }
]
```

## Execution plan

- Comparison: fit order 10 against the stored order-3 production fit of M1_210210, using the same seed.
- Baseline: `results/dr2-quiescent-new-defaults/210210-M1_210210`; order 3; seed 20260832.
- Data: LEGA-C DR2 spectrum M1_210210; COSMOS2015 `cosmos_total` photometry, 12 bands.
- Model: `notebooks/ceridwen_integrated_photometry_spectra.ipynb`; grid `amist_c3k_hr_krou_afe`; ceridwen `56505a6`; Student-t SFH prior; free dust index; BlackJAX NSS: `num_live=500`, `num_inner_steps=65`, `num_delete=100`.
- Controlled change: `CERIDWEN_CALIBRATION_ORDER=10`, arm `poly10` of `scripts/calibration_arms_vast.py`.
- Hardware and outputs: one Vast.ai RTX 5060 or 5060 Ti under $0.11/h, reliability above 99.5%; `results/m1-210210-reference/poly10/210210-M1_210210/` with the executed notebook; a wiki note.

## Amendments

```json
[
  {
    "date": "2026-09-17",
    "text": "In the meantime, can you help plan a plot of kl divergence of different parameters from the prior to see which parameters are most constrained by the model. ask me appropriate questions",
    "display_text": "In the meantime, can you help plan a plot of KL divergence of different parameters from the prior, to see which parameters are most constrained by the model? Ask me appropriate questions."
  },
  {
    "date": "2026-09-17",
    "text": "Scope: M1_210210 only. Parameters: Sampled parameters. Data: Joint fit only. Figure: Sorted bar chart."
  },
  {
    "date": "2026-09-17",
    "text": "i feel like KL could be separate from the notebook - it just has to go on the wiki",
    "display_text": "I feel like KL could be separate from the notebook - it just has to go on the wiki."
  },
  {
    "date": "2026-09-20",
    "text": "I want it to plot KLD versions with the different parameters on the x axis, and KLD divergence on the y axis. So at a glance, I can see which parameters are well constrained. This should be part of the notebook. But don't do a GPU run again - just make the plot and have it regenerated in the output since the data is already there.",
    "display_text": "I want it to plot KLD versions with the different parameters on the x axis and KL divergence on the y axis, so at a glance I can see which parameters are well constrained. This should be part of the notebook. But don't do a GPU run again; just make the plot and have it regenerated in the output, since the data is already there. (Supersedes the 2026-09-17 message that KL could be separate from the notebook.)"
  }
]
```

## Runs

```json
[
  {
    "id": "poly10-tau0p2-seed20260832",
    "arm": "poly10",
    "status": "complete",
    "target": "M1_210210",
    "artifacts": [
      {
        "label": "Executed fit · M1_210210",
        "path": "results/m1-210210-reference/tau-0p2/poly10/210210-M1_210210/M1_210210_executed.ipynb"
      },
      {
        "label": "ceridwen_result.h5",
        "path": "results/m1-210210-reference/tau-0p2/poly10/210210-M1_210210/ceridwen_result.h5"
      },
      {
        "label": "execution.log",
        "path": "results/m1-210210-reference/tau-0p2/poly10/210210-M1_210210/execution.log"
      }
    ],
    "code": "55ff5f4",
    "model": "Ceridwen 56505a6",
    "config": "results/m1-210210-reference/tau-0p2/vast_run_2026-09-17T172226+0000.json",
    "data": "results/m1-210210-reference/tau-0p2/cells.json",
    "seed": 20260832
  },
  {
    "id": "poly10-tau1-freez-seed20260832",
    "arm": "poly10",
    "status": "complete",
    "target": "M1_210210",
    "artifacts": [
      {
        "label": "Executed fit · M1_210210",
        "path": "results/m1-210210-reference/tau-1/poly10/210210-M1_210210/M1_210210_executed.ipynb"
      },
      {
        "label": "ceridwen_result.h5",
        "path": "results/m1-210210-reference/tau-1/poly10/210210-M1_210210/ceridwen_result.h5"
      },
      {
        "label": "execution.log",
        "path": "results/m1-210210-reference/tau-1/poly10/210210-M1_210210/execution.log"
      }
    ],
    "code": "cc983ce",
    "model": "Ceridwen c540bc7",
    "config": "results/m1-210210-reference/tau-1/vast_run_2026-09-17T175951+0000.json",
    "data": "results/m1-210210-reference/tau-1/cells.json",
    "seed": 20260832
  }
]
```

## Figures

```json
[
  {
    "path": "results/m1-210210-reference/fit-M1_210210.png",
    "view": "Fits",
    "target": "M1_210210",
    "caption": "M1_210210. Spectrum, calibration polynomial over fitted pixels with 16-84% band, and photometry; posterior medians of fits A, B and C."
  },
  {
    "path": "results/m1-210210-reference/sfh-M1_210210.png",
    "view": "SFH",
    "target": "M1_210210",
    "caption": "M1_210210. Star-formation history and cumulative mass fraction, fits A, B and C."
  },
  {
    "path": "results/m1-210210-reference/corner-M1_210210.png",
    "view": "Posteriors",
    "target": "M1_210210",
    "caption": "M1_210210. Physical-parameter posteriors, 1-sigma contours, fits A, B and C."
  },
  {
    "path": "wiki/analyses/m1-210210-reference/kl-M1_210210.png",
    "view": "Comparison",
    "target": "M1_210210",
    "caption": "M1_210210. KL divergence of each sampled parameter's posterior from its prior, in bits, sorted by fit C. Each fit is compared with its own prior; fit B rails at its 0.2 bound on tau_dust."
  }
]
```

## Measurements

| Quantity | A | B | C |
| --- | --- | --- | --- |
| Calibration order | 3 | 10 | 10 |
| \(\tau_{\mathrm{dust}}\) prior | Uniform(0, 2) | Uniform(0, 0.2) | Uniform(0, 1) |
| \(z\), \(\sigma_\star\) | fixed | fixed | sampled |
| \(\ln Z\) | 230683.02 ± 0.38 | 231041.38 ± 0.37 | 231153.16 ± 0.35 |
| Spectral \(\chi^2\), catalogue uncertainties | 13970.3 | 11308.6 | 10773.3 |
| Spectral \(\chi^2\) at fit A's floor | 3692.8 | 3059.2 | 2857.2 |
| Photometric \(\chi^2\) | 90.0 | 89.9 | 55.0 |
| \(\log_{10}(M_\star/M_\odot)\) | 11.551 ± 0.018 | 11.561 ± 0.012 | 11.650 ± 0.013 |
| \([\mathrm{Fe}/\mathrm{H}]\) | +0.146 ± 0.019 | -0.273 ± 0.044 | -0.159 ± 0.022 |
| \([\alpha/\mathrm{Fe}]\) | -0.022 ± 0.007 | +0.036 ± 0.010 | +0.060 ± 0.010 |
| \(\tau_{\mathrm{dust}}\) | 0.443 ± 0.012 | 0.199 ± 0.001 | 0.405 ± 0.013 |
| \(\delta_{\mathrm{dust}}\) | -0.992 ± 0.009 | -0.995 ± 0.005 | -0.987 ± 0.014 |
| \(t_{\mathrm{MW}}\) [Gyr] | 3.92 ± 0.18 | 5.20 ± 0.14 | 5.19 ± 0.12 |
| \(t_{50}\) [Gyr] | 3.83 ± 0.18 | 5.37 ± 0.19 | 5.32 ± 0.17 |
| \(f_{\mathrm{calib}}\) [%] | 3.08 ± 0.05 | 2.62 ± 0.05 | 2.52 ± 0.05 |
| \(z\) | 0.6542 | 0.6542 | 0.654219 ± 0.000015 |
| \(\sigma_\star\) [km/s] | 259.5 | 259.5 | 263.4 ± 3.1 |
| ESS | 4094 | 4531 | 4923 |
| Likelihood calls | 8 706 256 | 8 415 066 | 10 455 667 |
| Sampler wall time [s] | 488 | 468 | 1502 |
| Vast instance, spend | | 51329179, $0.052 | 51331110, $0.086 |

Fit A is the stored production fit `results/dr2-quiescent-new-defaults/210210-M1_210210`. All three fits use seed 20260832, 3523 spectral pixels and 12 bands.

KL divergence of the posterior from the prior, bits, `scripts/plot_prior_kl.py`:

| Parameter | A | B | C |
| --- | --- | --- | --- |
| \(z\) | | | 11.57 |
| \(\log_{10}(M_\star/M_\odot)\) | 6.23 | 6.60 | 6.61 |
| \(\log[\mathrm{SFR}(0)/\mathrm{SFR}(0.03\,\mathrm{Gyr})]\) | 6.89 | 0.95 | 5.84 |
| \([\mathrm{Fe}/\mathrm{H}]\) | 5.14 | 4.40 | 5.11 |
| \(\log[\mathrm{SFR}(1)/\mathrm{SFR}(3\,\mathrm{Gyr})]\) | 7.75 | 4.86 | 5.02 |
| \(\delta_{\mathrm{dust}}\) | 5.60 | 6.31 | 4.98 |
| \(\log f_{\mathrm{calib}}\) | 5.01 | 4.87 | 4.92 |
| \([\alpha/\mathrm{Fe}]\) | 4.72 | 4.26 | 4.33 |
| \(\tau_{\mathrm{dust}}\) | 5.33 | 6.06 | 4.17 |
| Spectrum scaling | 3.23 | 3.53 | 3.26 |
| \(\log[\mathrm{SFR}(3)/\mathrm{SFR}(5\,\mathrm{Gyr})]\) | 1.96 | 1.58 | 2.80 |
| \(\sigma_\star\) | | | 0.79 |
| \(\log[\mathrm{SFR}(5)/\mathrm{SFR}(7.57\,\mathrm{Gyr})]\) | 0.50 | 0.15 | 0.74 |
| \(\log[\mathrm{SFR}(0.03)/\mathrm{SFR}(0.1\,\mathrm{Gyr})]\) | 0.09 | 1.10 | 0.20 |
| \(\log[\mathrm{SFR}(0.3)/\mathrm{SFR}(1\,\mathrm{Gyr})]\) | 0.04 | 0.13 | 0.14 |
| \(\log[\mathrm{SFR}(0.1)/\mathrm{SFR}(0.3\,\mathrm{Gyr})]\) | 0.06 | 0.28 | 0.09 |
| Sum of marginals | 52.5 | 45.1 | 60.6 |
| Joint, \((\langle\ln L\rangle - \ln Z)/\ln 2\) | 66.1 | 58.1 | 77.1 |

Bootstrap half-widths are 0.03 bits or less.

[Executed comparison](results/m1-210210-reference/analysis.ipynb) · [Comparison table](results/m1-210210-reference/comparison.csv) · [KL table](wiki/analyses/m1-210210-reference/kl-M1_210210.csv)

## Results

Fit C, at the production defaults of commit cc983ce, has \(\ln Z\) 470.1 above fit A and 111.8 above fit B. From A to C, \([\mathrm{Fe}/\mathrm{H}]\) moves from +0.146 to -0.159, \(t_{\mathrm{MW}}\) from 3.92 to 5.19 Gyr and \(\log_{10} M_\star\) from 11.551 to 11.650. Fit B has \(\tau_{\mathrm{dust}}\) at its 0.2 prior bound; fit C gives 0.405 ± 0.013 under the (0, 1) bound. \(\delta_{\mathrm{dust}}\) sits at the -1 bound in all three fits. In fit C the largest KL divergences are \(z\) (11.6 bits), \(\log_{10} M_\star\) (6.6), the youngest SFR ratio (5.8) and \([\mathrm{Fe}/\mathrm{H}]\) (5.1); \(\sigma_\star\) has 0.8 bits and the SFR ratios between 0.03 and 1 Gyr have 0.2 bits or less.

## Caveats

- Run B cloned the branch at 55ff5f4, where the \(\tau_{\mathrm{dust}}\) prior was Uniform(0, 0.2). The default became Uniform(0, 1) in 3b33ccd and \(z\), \(\sigma_\star\) became sampled in cc983ce during the run, so run C repeats the fit at those defaults.
- Fit A differs from B and C in the \(\tau_{\mathrm{dust}}\) prior as well as in the calibration order; no pair of fits isolates the order.
- Each KL value is against that fit's own prior. The \(\tau_{\mathrm{dust}}\) rows have prior widths 2, 0.2 and 1.
- The youngest SFR ratio has posterior median +3.2 dex in fit A and +0.5 dex in fit B; the Student-t prior has scale 0.3.
- The stored calibration polynomial reaches 160 outside the fitted pixels, where \(|x| > 1\); the figure shows fitted pixels only.

## References

- [15 September 2026 · Meeting with MJ Park and Sandro](wiki/notes/meeting-2026-09-15-mj-park-sandro.md)
- [Calibration polynomial order · note](wiki/notes/calibration-order.md)
- [M1_210210 reference fit · note](wiki/notes/m1-210210-reference.md)
- [Order-3 production fit](results/dr2-quiescent-new-defaults/210210-M1_210210/M1_210210_executed.ipynb)

## Your interpretation

```json
[]
```

## Next decision

```json
[]
```
