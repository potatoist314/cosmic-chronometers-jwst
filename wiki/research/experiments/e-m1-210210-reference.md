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
  },
  {
    "date": "2026-09-21",
    "text": "i don't like the use of bars, takes up too much visual space, use points instead.",
    "display_text": "I don't like the use of bars; it takes up too much visual space. Use points instead."
  },
  {
    "date": "2026-09-21",
    "text": "Two reference marks on the KL figure, relayed by the orchestrator: a shaded band at the estimator noise floor, measured from prior-only draws with the posterior weights and the same bin count as marginal_kl_bits, 200 repeats, band top at the 95th percentile; and a dashed line at 1 bit labelled as a factor-two narrowing of the prior. Both chosen by Liu Hao; there is no consensus threshold. He picked the log-axis treatment from two designer variants.",
    "display_text": "Two reference marks on the KL figure: a shaded band at the measured estimator noise floor (200 prior-only draws with the posterior weights, band top at the 95th percentile), and a dashed line at 1 bit, a factor-two narrowing of the prior. The band is a measurement; the 1-bit line is a stated convention, not a standard. Log-axis treatment picked from two designer variants."
  },
  {
    "date": "2026-09-21",
    "text": "remove B for this and from other diagrams - tau dust less than 0.2 was a mistake and has no basis being compared against as a result",
    "display_text": "Remove B for this and from other diagrams. tau_dust less than 0.2 was a mistake and has no basis for being compared against as a result. (Run poly10-tau0p2-seed20260832 is kept on disk and marked excluded from comparison.)"
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
    "seed": 20260832,
    "comparison": "excluded",
    "excluded_on": "2026-09-21",
    "exclusion_reason": "Liu Hao, 2026-09-21: remove B for this and from other diagrams - tau dust less than 0.2 was a mistake and has no basis being compared against as a result"
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
    "caption": "M1_210210. Spectrum, calibration polynomial over fitted pixels with 16-84% band, and photometry; posterior medians of fits A and C."
  },
  {
    "path": "results/m1-210210-reference/sfh-M1_210210.png",
    "view": "SFH",
    "target": "M1_210210",
    "caption": "M1_210210. Star-formation history and cumulative mass fraction, fits A and C."
  },
  {
    "path": "results/m1-210210-reference/corner-M1_210210.png",
    "view": "Posteriors",
    "target": "M1_210210",
    "caption": "M1_210210. Physical-parameter posteriors, 1-sigma contours, fits A and C."
  },
  {
    "path": "wiki/analyses/m1-210210-reference/kl-M1_210210.png",
    "view": "Comparison",
    "target": "M1_210210",
    "caption": "M1_210210. KL divergence of each sampled parameter's posterior from its prior, in bits, sorted by fit C. Each fit is compared with its own prior."
  }
]
```

## Measurements

| Quantity | A | C |
| --- | --- | --- |
| Calibration order | 3 | 10 |
| \(\tau_{\mathrm{dust}}\) prior | Uniform(0, 2) | Uniform(0, 1) |
| \(z\), \(\sigma_\star\) | fixed | sampled |
| \(\ln Z\) | 230683.02 ± 0.38 | 231153.16 ± 0.35 |
| Spectral \(\chi^2\), catalogue uncertainties | 13970.3 | 10773.3 |
| Spectral \(\chi^2\) at fit A's floor | 3692.8 | 2857.2 |
| Photometric \(\chi^2\) | 90.0 | 55.0 |
| \(\log_{10}(M_\star/M_\odot)\) | 11.551 ± 0.018 | 11.650 ± 0.013 |
| \([\mathrm{Fe}/\mathrm{H}]\) | +0.146 ± 0.019 | -0.159 ± 0.022 |
| \([\alpha/\mathrm{Fe}]\) | -0.022 ± 0.007 | +0.060 ± 0.010 |
| \(\tau_{\mathrm{dust}}\) | 0.443 ± 0.012 | 0.405 ± 0.013 |
| \(\delta_{\mathrm{dust}}\) | -0.992 ± 0.009 | -0.987 ± 0.014 |
| \(t_{\mathrm{MW}}\) [Gyr] | 3.92 ± 0.18 | 5.19 ± 0.12 |
| \(t_{50}\) [Gyr] | 3.83 ± 0.18 | 5.32 ± 0.17 |
| \(f_{\mathrm{calib}}\) [%] | 3.08 ± 0.05 | 2.52 ± 0.05 |
| \(z\) | 0.6542 | 0.654219 ± 0.000015 |
| \(\sigma_\star\) [km/s] | 259.5 | 263.4 ± 3.1 |
| ESS | 4094 | 4923 |
| Likelihood calls | 8 706 256 | 10 455 667 |
| Sampler wall time [s] | 488 | 1502 |
| Vast instance, spend | | 51331110, $0.086 |

Fit A is the stored production fit `results/dr2-quiescent-new-defaults/210210-M1_210210`. Both fits use seed 20260832, 3523 spectral pixels and 12 bands.

KL divergence of the posterior from the prior, bits, `scripts/plot_prior_kl.py`:

| Parameter | A | C |
| --- | --- | --- |
| \(z\) | | 11.57 |
| \(\log_{10}(M_\star/M_\odot)\) | 6.23 | 6.61 |
| \(\log[\mathrm{SFR}(0)/\mathrm{SFR}(0.03\,\mathrm{Gyr})]\) | 6.89 | 5.84 |
| \([\mathrm{Fe}/\mathrm{H}]\) | 5.14 | 5.11 |
| \(\log[\mathrm{SFR}(1)/\mathrm{SFR}(3\,\mathrm{Gyr})]\) | 7.75 | 5.02 |
| \(\delta_{\mathrm{dust}}\) | 5.60 | 4.98 |
| \(\log f_{\mathrm{calib}}\) | 5.01 | 4.92 |
| \([\alpha/\mathrm{Fe}]\) | 4.72 | 4.33 |
| \(\tau_{\mathrm{dust}}\) | 5.33 | 4.17 |
| Spectrum scaling | 3.23 | 3.26 |
| \(\log[\mathrm{SFR}(3)/\mathrm{SFR}(5\,\mathrm{Gyr})]\) | 1.96 | 2.80 |
| \(\sigma_\star\) | | 0.79 |
| \(\log[\mathrm{SFR}(5)/\mathrm{SFR}(7.57\,\mathrm{Gyr})]\) | 0.50 | 0.74 |
| \(\log[\mathrm{SFR}(0.03)/\mathrm{SFR}(0.1\,\mathrm{Gyr})]\) | 0.09 | 0.20 |
| \(\log[\mathrm{SFR}(0.3)/\mathrm{SFR}(1\,\mathrm{Gyr})]\) | 0.04 | 0.14 |
| \(\log[\mathrm{SFR}(0.1)/\mathrm{SFR}(0.3\,\mathrm{Gyr})]\) | 0.06 | 0.09 |
| Sum of marginals | 52.5 | 60.6 |
| Joint, \((\langle\ln L\rangle - \ln Z)/\ln 2\) | 66.1 | 77.1 |

Bootstrap half-widths are 0.03 bits or less.

[Executed comparison](results/m1-210210-reference/analysis.ipynb) · [Comparison table](results/m1-210210-reference/comparison.csv) · [KL table](wiki/analyses/m1-210210-reference/kl-M1_210210.csv)

## Results

Fit C uses the production defaults of commit cc983ce. Its \(\ln Z\) exceeds A by 470.1. From A to C, \([\mathrm{Fe}/\mathrm{H}]\) moves from +0.146 to -0.159, \(t_{\mathrm{MW}}\) from 3.92 to 5.19 Gyr and \(\log_{10} M_\star\) from 11.551 to 11.650.

\(\tau_{\mathrm{dust}}\) is 0.443 ± 0.012 in A and 0.405 ± 0.013 in C. \(\delta_{\mathrm{dust}}\) sits at the -1 bound in both fits.

In C the largest KL divergences are \(z\) (11.6 bits), \(\log_{10} M_\star\) (6.6), \(\log_{10}\) SFR in the 0-0.03 Gyr bin (5.6) and \([\mathrm{Fe}/\mathrm{H}]\) (5.1). \(\sigma_\star\) has 0.8 bits. SFR bins between 0.03 and 1 Gyr have 1.6 to 1.8 bits.

## Caveats

- Run poly10-tau0p2-seed20260832 (\(\tau_{\mathrm{dust}}\) Uniform(0, 0.2), branch 55ff5f4) stays on disk but is excluded from comparison since 2026-09-21. Liu Hao: "tau dust less than 0.2 was a mistake and has no basis being compared against".
- A and C differ in the \(\tau_{\mathrm{dust}}\) prior and the calibration order. A fixes \(z\) and \(\sigma_\star\); C samples them. No pair of fits isolates the order.
- Each KL value is against that fit's own prior. The \(\tau_{\mathrm{dust}}\) prior widths are 2 for A and 1 for C.
- The youngest SFR ratio has posterior median +3.2 dex in fit A; the Student-t prior has scale 0.3.
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
