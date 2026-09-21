---
kind: experiment
id: e-no-emission-mask
title: M1_210210 fit without the emission-line mask
date: 2026-09-21
results_at: 2026-09-21T12:27:44+01:00
origin: new
status: results-ready
question: q-fitting-choices
related_questions: q-emission-lines
source_notes: no-emission-mask
result_groups: results/no-emission-mask
follow_up:
---

## Context

The production fit masks ±1500 km/s around rest-frame 3726.0, 3728.8 ([O II]), 4861.3 (H-beta), 4958.9 and 5006.8 ([O III]) Å: about 190 Å, covering the H-beta age feature and Fe5015. The DR2 quiescent sample is selected on |EW/sigma_EW| < 3 for [O II] and [O III].

## Before delegation

```json
[
  {
    "date": "2026-09-21",
    "text": "but without the mask this could offer better fitting / parameter constraints, no?",
    "display_text": "But without the mask this could offer better fitting / parameter constraints, no?"
  },
  {
    "date": "2026-09-21",
    "text": "yes, put a worker on the fit",
    "display_text": "Yes, put a worker on the fit."
  }
]
```

## Execution plan


- Comparison: fit M1_210210 without an emission-line mask against the stored masked fit, using the same seed.
- Baseline: `results/m1-210210-reference/tau-1/poly10/210210-M1_210210`, not re-run; calibration order 10; `tau_dust` Uniform(0, 1); free `zred` and `sigma_star`; seed 20260832; ceridwen `c540bc7`; config `results/m1-210210-reference/tau-1/vast_run_2026-09-17T175951+0000.json`.
- Data: LEGA-C DR2 spectrum M1_210210; joint fit with COSMOS2015 `cosmos_total` photometry, 12 bands.
- Model: `notebooks/ceridwen_integrated_photometry_spectra.ipynb`; grid `amist_c3k_hr_krou_afe`; ceridwen `b419fd1` (`c540bc7` plus per-iteration progress logging in `sampler/nested.py`, no sampling change); Student-t SFH prior; free dust index; BlackJAX NSS: `num_live=500`, `num_inner_steps=65`, `num_delete=100`.
- Controlled change: `SETTINGS['emission_lines'] = []` only; telluric mask 7590–7660 Å air kept; arm `no_emission_mask` of `scripts/calibration_arms_vast.py` sets `CERIDWEN_SETTINGS_OVERRIDE={"emission_lines": []}`; `scripts/run_ceridwen_vast_multi_gpu.py` merges it into `SETTINGS` in the executed copy; template default unchanged.
- Analysis: `results/no-emission-mask/analysis.ipynb`; shift of each sampled parameter in units of the baseline posterior half-width; posterior-width change; KL bits from the prior for both arms; derived mass-weighted age included; comparison figure designed by the designer agent.
- Hardware and outputs: one Vast.ai RTX 5060 or 5060 Ti under $0.11/h, reliability above 99.5%, bandwidth under $5/TB; `results/no-emission-mask/no_emission_mask/210210-M1_210210/` with the executed notebook (fit, SFH, corner, KL figure); a wiki note.

## Amendments

```json
[]
```

## Runs

```json
[
  {
    "id": "no-emission-mask-m1-210210",
    "arm": "no_emission_mask",
    "status": "complete",
    "target": "M1_210210",
    "artifacts": [
      {
        "label": "Executed fit · M1_210210",
        "path": "results/no-emission-mask/no_emission_mask/210210-M1_210210/M1_210210_executed.ipynb"
      },
      {
        "label": "ceridwen_result.h5",
        "path": "results/no-emission-mask/no_emission_mask/210210-M1_210210/ceridwen_result.h5"
      },
      {
        "label": "execution.log",
        "path": "results/no-emission-mask/no_emission_mask/210210-M1_210210/execution.log"
      },
      {
        "label": "Executed analysis",
        "path": "results/no-emission-mask/analysis.ipynb"
      },
      {
        "label": "Vast driver log",
        "path": "results/no-emission-mask/vast_run.log"
      }
    ],
    "code": "92e203c; ceridwen working tree uploaded with results/no-emission-mask/ceridwen-worktree.patch",
    "model": "Ceridwen b419fd1; grid amist_c3k_hr_krou_afe",
    "config": "results/no-emission-mask/vast_run_2026-09-21T110044+0000.json",
    "data": "results/no-emission-mask/cells.json",
    "seed": 20260832
  }
]
```

## Figures

```json
[
  {
    "path": "results/no-emission-mask/fit-M1_210210.png",
    "view": "Fits",
    "target": "M1_210210",
    "caption": "M1_210210. Spectrum, calibration polynomial and photometry with posterior medians of the masked and no-mask fits."
  },
  {
    "path": "results/no-emission-mask/sfh-M1_210210.png",
    "view": "SFH",
    "target": "M1_210210",
    "caption": "M1_210210. SFH and cumulative mass fraction, both fits."
  },
  {
    "path": "results/no-emission-mask/corner-M1_210210.png",
    "view": "Posteriors",
    "target": "M1_210210",
    "caption": "M1_210210. Grey shapes are the fit with emission lines masked and red outlines the fit with no mask, each the \\(1\\sigma\\) contour with the 1D posteriors on the diagonal: an offset between a red outline and its grey shape means those parameters moved, and a smaller red outline means a tighter constraint."
  },
  {
    "notebook": "results/no-emission-mask/no_emission_mask/210210-M1_210210/M1_210210_executed.ipynb",
    "cell": 22,
    "output": 0,
    "run": "no-emission-mask-m1-210210",
    "target": "M1_210210",
    "arm": "no_emission_mask",
    "view": "Comparison",
    "caption": "M1_210210. KL divergence of each sampled parameter from its prior in the no-mask fit, from the executed fit notebook."
  }
]
```

## Measurements

| Quantity | Masked | No mask |
| --- | --- | --- |
| Emission-line mask | 5 lines, \(\pm1500\,\mathrm{km\,s^{-1}}\) | none |
| Fitted spectral pixels | 3523 | 3939 |
| \(\ln Z\) | 231153.16 ± 0.35 | 258237.78 ± 0.45 |
| Spectral \(\chi^2\), catalogue uncertainties, own pixels | 10772.1 | 12368.4 |
| Spectral \(\chi^2\), catalogue uncertainties, 3523 common pixels | 10772.1 | 10955.5 |
| Photometric \(\chi^2\) | 55.0 | 50.9 |
| \(\log_{10}(M_\star/M_\odot)\) | 11.650 ± 0.013 | 11.645 ± 0.013 |
| \([\mathrm{Fe}/\mathrm{H}]\) | -0.159 ± 0.022 | -0.153 ± 0.019 |
| \([\alpha/\mathrm{Fe}]\) | +0.060 ± 0.010 | +0.045 ± 0.010 |
| \(\tau_{\mathrm{dust}}\) | 0.405 ± 0.013 | 0.398 ± 0.015 |
| \(\delta_{\mathrm{dust}}\) | -0.987 ± 0.014 | -0.987 ± 0.015 |
| \(t_{\mathrm{MW}}\) [Gyr] | 5.19 ± 0.12 | 5.18 ± 0.10 |
| \(t_{50}\) [Gyr] | 5.32 ± 0.17 | 5.35 ± 0.17 |
| \(f_{\mathrm{calib}}\) [%] | 2.52 ± 0.05 | 2.55 ± 0.05 |
| \(z\) | 0.654219 ± 0.000015 | 0.654207 ± 0.000016 |
| \(\sigma_\star\) [km/s] | 263.4 ± 3.1 | 266.0 ± 2.9 |
| ESS | 4923 | 4862 |
| Likelihood calls | 10 455 667 | 10 215 612 |
| Sampler wall time [s] | 1502 | 1475 |
| Vast instance, spend | 51331110, $0.086 | 51896980, $0.082 |

Posterior median and half the 16-84% width. Shift: no-mask median minus masked median, in masked half-widths. KL from each fit's own prior, `kl_table` in `scripts/plot_prior_kl.py`.

| Parameter | Shift [masked half-widths] | Width, no mask / masked | KL masked [bits] | KL no mask [bits] |
| --- | --- | --- | --- | --- |
| \([\mathrm{Fe}/\mathrm{H}]\) | +0.34 | 0.92 | 5.11 | 5.20 |
| \([\alpha/\mathrm{Fe}]\) | -1.72 | 1.01 | 4.33 | 4.32 |
| \(\delta_{\mathrm{dust}}\) | +0.01 | 1.10 | 4.98 | 4.82 |
| \(\tau_{\mathrm{dust}}\) | -0.65 | 1.11 | 4.17 | 4.05 |
| \(\log f_{\mathrm{calib}}\) | +0.29 | 0.96 | 4.92 | 5.00 |
| \(\log_{10}(M_\star/M_\odot)\) | -0.37 | 0.94 | 6.61 | 6.69 |
| \(\log[\mathrm{SFR}(0)/\mathrm{SFR}(0.03\,\mathrm{Gyr})]\) | +0.11 | 1.18 | 5.84 | 5.69 |
| \(\log[\mathrm{SFR}(0.03)/\mathrm{SFR}(0.1\,\mathrm{Gyr})]\) | -0.09 | 1.07 | 0.20 | 0.13 |
| \(\log[\mathrm{SFR}(0.1)/\mathrm{SFR}(0.3\,\mathrm{Gyr})]\) | -0.05 | 0.98 | 0.09 | 0.09 |
| \(\log[\mathrm{SFR}(0.3)/\mathrm{SFR}(1\,\mathrm{Gyr})]\) | -0.05 | 1.04 | 0.14 | 0.13 |
| \(\log[\mathrm{SFR}(1)/\mathrm{SFR}(3\,\mathrm{Gyr})]\) | -0.14 | 1.05 | 5.02 | 6.16 |
| \(\log[\mathrm{SFR}(3)/\mathrm{SFR}(5\,\mathrm{Gyr})]\) | +0.56 | 0.88 | 2.80 | 2.53 |
| \(\log[\mathrm{SFR}(5)/\mathrm{SFR}(7.57\,\mathrm{Gyr})]\) | -0.33 | 0.96 | 0.74 | 0.47 |
| \(\sigma_\star\) | +0.87 | 0.97 | 0.79 | 1.32 |
| spectrum scaling | -0.44 | 1.02 | 3.26 | 3.25 |
| \(z\) | -0.63 | 1.00 | 11.57 | 11.58 |
| \(t_{\mathrm{MW}}\) | -0.08 | 0.86 |  |  |

Residual pull in the no-mask fit, (observed − posterior-median model) / total uncertainty with the fitted calibration floor:

| Line | Window [km/s] | Pixels | Mean pull | \(1/\sqrt{N}\) | RMS pull |
| --- | --- | --- | --- | --- | --- |
| \([\mathrm{O\,II}]\) 3726 | ±1500 | 5 | -1.83 | 0.45 | 0.68 |
| \([\mathrm{O\,II}]\) 3726 | ±300 | 0 | | | |
| \([\mathrm{O\,II}]\) 3729 | ±1500 | 13 | -1.40 | 0.28 | 1.11 |
| \([\mathrm{O\,II}]\) 3729 | ±300 | 0 | | | |
| \(\mathrm{H}\beta\) | ±1500 | 134 | +0.05 | 0.09 | 0.53 |
| \(\mathrm{H}\beta\) | ±300 | 27 | +0.09 | 0.19 | 0.53 |
| \([\mathrm{O\,III}]\) 4959 | ±1500 | 137 | +0.30 | 0.09 | 1.26 |
| \([\mathrm{O\,III}]\) 4959 | ±300 | 27 | +0.85 | 0.19 | 1.18 |
| \([\mathrm{O\,III}]\) 5007 | ±1500 | 138 | +0.08 | 0.09 | 0.72 |
| \([\mathrm{O\,III}]\) 5007 | ±300 | 28 | +0.57 | 0.19 | 0.68 |

[Executed comparison](results/no-emission-mask/analysis.ipynb) · [Comparison table](results/no-emission-mask/comparison.csv) · [Parameter shifts](results/no-emission-mask/parameter-shifts.csv) · [Line residual pulls](results/no-emission-mask/line-residual-pulls.csv)

## Results

From masked to no mask, fitted pixels increase 3523→3939. Median shifts exceeding 0.5 masked half-widths: \([\alpha/\mathrm{Fe}]\) +0.060→+0.045 (−1.72); \(\sigma_\star\) 263.4→266.0 km/s (+0.87); \(\tau_{\mathrm{dust}}\) 0.405→0.398 (−0.65); \(z\) 0.654219→0.654207 (−0.63); \(\log[\mathrm{SFR}(3)/\mathrm{SFR}(5\,\mathrm{Gyr})]\) (+0.56). Every other sampled parameter and \(t_{\mathrm{MW}}\) move ≤0.44 half-widths; \(t_{\mathrm{MW}}\): \(5.19\pm0.12\rightarrow5.18\pm0.10\) Gyr. No-mask/masked width ratios span 0.86 (\(t_{\mathrm{MW}}\))–1.18 (youngest SFR ratio). KL changes exceeding 0.2 bits: \(\log[\mathrm{SFR}(1)/\mathrm{SFR}(3\,\mathrm{Gyr})]\) 5.02→6.16; \(\sigma_\star\) 0.79→1.32; \(\log[\mathrm{SFR}(3)/\mathrm{SFR}(5\,\mathrm{Gyr})]\) 2.80→2.53; \(\log[\mathrm{SFR}(5)/\mathrm{SFR}(7.57\,\mathrm{Gyr})]\) 0.74→0.47. Spectral \(\chi^2\) over 3523 common pixels: 10772.1→10955.5; photometric \(\chi^2\): 55.0→50.9.

In the no-mask fit, mean residual pulls within \(\pm300\,\mathrm{km/s}\) are \(+0.10\pm0.19\) at \(\mathrm{H}\beta\) (27 pixels), \(+0.85\pm0.19\) at \([\mathrm{O\,III}]\) 4959 (27 pixels) and \(+0.57\pm0.19\) at \([\mathrm{O\,III}]\) 5007 (28 pixels), with errors \(1/\sqrt{N}\). The \([\mathrm{O\,II}]\) 3726 and 3729 windows contain 5 and 13 fitted pixels at the blue end of the spectrum, none within \(\pm300\,\mathrm{km/s}\), with mean pulls −1.83 and −1.40 (`results/no-emission-mask/line-residual-pulls.csv`).

## Caveats

- \(\ln Z\) is 231153.16 masked and 258237.78 without the mask, over different pixel sets (3523 and 3939); these values are not compared.
- No seed repeat exists for M1_210210. Seed repeats of M4_108989 and M5_172669 under the new defaults differ in age by up to 0.34 error bars (`wiki/themes.md`, `new_default_rep1-2`).
- The no-mask arm uses ceridwen b419fd1; the baseline uses c540bc7. The difference is per-iteration progress logging in `ceridwen/sampler/nested.py`.
- The uploaded ceridwen working tree includes uncommitted edits saved in `results/no-emission-mask/ceridwen-worktree.patch`: one comment line in `ceridwen/ssps/ssp_data_afe.py`, and edits to `scripts_afe/build_afe_hr_grid.py`, which the fit does not import.
- Pull errors \(1/\sqrt{N}\) assume independent unit-variance pixels. The RMS pull at \(\mathrm{H}\beta\) is 0.53.

## References

- [Masked baseline fit](results/m1-210210-reference/tau-1/poly10/210210-M1_210210/M1_210210_executed.ipynb)
- [Baseline run configuration](results/m1-210210-reference/tau-1/vast_run_2026-09-17T175951+0000.json)
- [M1_210210 without the emission-line mask · note](wiki/notes/no-emission-mask.md)
- [M1_210210 reference fit · note](wiki/notes/m1-210210-reference.md)

## Your interpretation

```json
[]
```

## Next decision

```json
[]
```
