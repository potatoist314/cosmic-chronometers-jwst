---
kind: experiment
id: e-nebular-grid
title: M1_210210 with nebular emission in the SSP grid
date: 2026-09-30
results_at: 2026-09-30T14:13:30+01:00
origin: new
status: results-ready
question: q-dust-index-railing
related_questions: q-emission-lines
follow_up: e-mask-all-ca
result_groups: results/m1-210210-nebular-2026-09-30
features: ssp_grid, emission_lines, emission_line_marginalisation, diffuse_delta, diffuse_Ebump
finding: M1_210210, wide / neb / neb_eline / neb_maskca: delta_dust −2.094 / −0.808 / −0.917 / −0.164; E_bump 7.88 / 10.56 / 10.42 / 3.53; mass fraction formed at 0–30 Myr 9.58e-4 / 4.84e-5 / 1.97e-6 / 1.96e-5.
---

## Context

M1_210210, LEGA-C DR2, \(z_{\mathrm{cat}} = 0.6542\).
`CSPBasis_afe`: no nebular emission.
Fit masks [O II] 3726, 3729, H\(\beta\) 4861.3, [O III] 4959, 5007 at ± 1500 km/s.

## Before delegation

```json
[
  {
    "date": "2026-09-30",
    "text": "what i'm surprised by for these results is that i expected: higher alpha / fe and metallicity, and certainly not such an extremely steep dust slope index and bump. are these assumptions sensible, and what in the model could be causing the mismatch.",
    "display_text": "What I'm surprised by for these results is that I expected higher alpha/Fe and metallicity, and certainly not such an extremely steep dust slope index and bump. Are these assumptions sensible, and what in the model could be causing the mismatch?",
    "source_ref": "Relayed by the Astronomy lead"
  },
  {
    "date": "2026-09-30",
    "text": "the most physically realistic fit that removes the young burst without manually zeroing it",
    "source_ref": "Relayed by the Astronomy lead"
  }
]
```

## Execution plan

- Comparison: `neb`, `neb_eline`, `neb_maskca` against `wide` of `e-dust-bump`; same seed. All three new arms: `diffuse_delta` Uniform(−3, 0.4), `diffuse_Ebump` Uniform(0, 12).
- Baseline: `results/m1-210210-kcbump-wide-2026-09-29/run/fits/wide/210210-M1_210210`; grid `amist_c3k_hr_krou_afe`, no nebular emission; same two priors.
- Data: LEGA-C DR2 M1_210210, \(z_{\mathrm{cat}} = 0.6542\); 28 photometric bands; seed 20260927; 14 SFH bins.
- Grid: `~/.ceridwen/grids/amist_c3k_hr_krou_afe_nebular.h5`, 612 MB, not in git; built by `scripts/build_nebular_grid.py` from `amist_c3k_hr_krou_afe`. FSPS CLOUDY lines and continuum (`ZAU_ND_mist.lines`, `ZAU_ND_mist.cont`, Ceridwen `NebularModel`) added at \(\log_{10}(\mathrm{age}/\mathrm{yr}) \le 7.30\): 47 of 107 age nodes, all 13 \([\mathrm{Fe}/\mathrm{H}]\) × 5 \([\alpha/\mathrm{Fe}]\) nodes.
- Grid physics: \(\log U = -2.5\); \(\log(Z_{\mathrm{gas}}/Z_\odot) = [\mathrm{Fe}/\mathrm{H}] + [\alpha/\mathrm{Fe}]\). Each SSP’s ionising photon rate \(Q\) from its own spectrum below 912 Å. Lines at grid resolution; stellar velocity dispersion applies. SHA256 `6fe00c55a177a93d5c74782e94d3a78418ce2ad856a4edfca8dcd8ed5e572a67`.
- Check: integrated H\(\beta\) and H\(\alpha\) flux in the added spectrum against CLOUDY line luminosity, every young SSP. Largest relative difference \(1.5\times10^{-5}\); script fails above \(10^{-4}\). Rebuild gives the same SHA256.
- Arms: `neb`: `emission_lines = [3726.0, 3728.8, 4958.9, 5006.8]`, H\(\beta\) 4861.3 leaves the mask. `neb_eline`: `emission_line_marginalisation = true`, \(z\) fixed, FSPS lines get free fluxes \(\ge 0\). `neb_maskca`: `emission_lines = [3726.0, 3728.8, 3934.77, 3969.59, 4958.9, 5006.8]`; as `neb`, plus Ca II K 3934.77 Å and H 3969.59 Å masked at ± 1500 km/s (vacuum, NIST ASD).
- Code: production defaults of `notebooks/ceridwen_integrated_photometry_spectra.ipynb` at project `4dd6c3a`; Ceridwen `ee68b5f`; sedpy_jax `9d8aa19`. Grid selected through `SETTINGS["ssp_grid"]` = path; no Ceridwen code change; SFH-basis fast path on. Default `ssp_grid` stays `amist_c3k_hr_krou_afe`.
- Hardware and outputs: Vast.ai RTX 5090, $1 cap; config `results/m1-210210-nebular-2026-09-30/experiment.json`; outputs `results/m1-210210-nebular-2026-09-30/run/fits/<arm>/210210-M1_210210/`.
- Run command: `python3 scripts/experiment.py run results/m1-210210-nebular-2026-09-30/experiment.json --gpu "RTX 5090" --output results/m1-210210-nebular-2026-09-30/run`; resumed through `results/m1-210210-nebular-2026-09-30/run_with_sps_home.py`, same arguments and `--max-attempts 8`.

## Amendments

```json
[
  {
    "date": "2026-09-30",
    "text": "smooth extra light and hot old stars seem too unphysical.",
    "display_text": "Smooth extra light and hot old stars seem too unphysical.",
    "source_ref": "Relayed by the Astronomy lead"
  },
  {
    "date": "2026-09-30",
    "text": "can emission line marginalisation account for the h beta and zero the last bit of star formation?",
    "display_text": "Can emission line marginalisation account for the H beta and zero the last bit of star formation?",
    "source_ref": "Relayed by the Astronomy lead"
  },
  {
    "date": "2026-09-30",
    "text": "i think nebular is pretty important",
    "display_text": "I think nebular is pretty important.",
    "source_ref": "Relayed by the Astronomy lead"
  }
]
```

## Runs

```json
[
  {
    "id": "wide-run-53420896",
    "arm": "wide",
    "status": "complete",
    "target": "M1_210210",
    "artifacts": [
      {
        "label": "Executed fit · M1_210210",
        "path": "results/m1-210210-kcbump-wide-2026-09-29/run/fits/wide/210210-M1_210210/M1_210210_executed.ipynb"
      },
      {
        "label": "ceridwen_result.h5",
        "path": "results/m1-210210-kcbump-wide-2026-09-29/run/fits/wide/210210-M1_210210/ceridwen_result.h5"
      },
      {
        "label": "ceridwen_derived_outputs.h5",
        "path": "results/m1-210210-kcbump-wide-2026-09-29/run/fits/wide/210210-M1_210210/ceridwen_derived_outputs.h5"
      },
      {
        "label": "Executed analysis",
        "path": "results/m1-210210-kcbump-wide-2026-09-29/analysis.ipynb"
      }
    ],
    "code": "319524c",
    "model": "Ceridwen ee68b5f; sedpy_jax 9d8aa19; grid amist_c3k_hr_krou_afe",
    "config": "results/m1-210210-kcbump-wide-2026-09-29/run/manifest.json",
    "seed": 20260927,
    "data": "results/m1-210210-kcbump-wide-2026-09-29/run/manifest.json"
  },
  {
    "id": "neb-run-53520349",
    "arm": "neb",
    "status": "complete",
    "target": "M1_210210",
    "artifacts": [
      {
        "label": "Executed fit · M1_210210",
        "path": "results/m1-210210-nebular-2026-09-30/run/fits/neb/210210-M1_210210/M1_210210_executed.ipynb"
      },
      {
        "label": "ceridwen_result.h5",
        "path": "results/m1-210210-nebular-2026-09-30/run/fits/neb/210210-M1_210210/ceridwen_result.h5"
      },
      {
        "label": "ceridwen_derived_outputs.h5",
        "path": "results/m1-210210-nebular-2026-09-30/run/fits/neb/210210-M1_210210/ceridwen_derived_outputs.h5"
      },
      {
        "label": "53520349-fit-0.log",
        "path": "results/m1-210210-nebular-2026-09-30/run/53520349-fit-0.log"
      }
    ],
    "code": "4dd6c3a",
    "model": "Ceridwen ee68b5f; sedpy_jax 9d8aa19; grid amist_c3k_hr_krou_afe_nebular.h5 sha256 6fe00c55a177a93d5c74782e94d3a78418ce2ad856a4edfca8dcd8ed5e572a67",
    "config": "results/m1-210210-nebular-2026-09-30/run/manifest.json",
    "seed": 20260927,
    "data": "results/m1-210210-nebular-2026-09-30/run/manifest.json"
  },
  {
    "id": "neb-eline-run-53520349",
    "arm": "neb_eline",
    "status": "failed",
    "error": "fit-1 exited 1 after 30 s: ValueError: emission lines need FSPS's $SPS_HOME/data/emlines_info.dat, which needs $SPS_HOME; instance 53520349 (host 662751) destroyed; $0.129 billed",
    "target": "M1_210210",
    "artifacts": [
      {
        "label": "53520349-fit-1.log",
        "path": "results/m1-210210-nebular-2026-09-30/run/53520349-fit-1.log"
      },
      {
        "label": "manifest.json",
        "path": "results/m1-210210-nebular-2026-09-30/run/manifest.json"
      }
    ],
    "code": "4dd6c3a",
    "model": "Ceridwen ee68b5f; sedpy_jax 9d8aa19; grid amist_c3k_hr_krou_afe_nebular.h5 sha256 6fe00c55a177a93d5c74782e94d3a78418ce2ad856a4edfca8dcd8ed5e572a67",
    "config": "results/m1-210210-nebular-2026-09-30/run/manifest.json",
    "seed": 20260927,
    "data": "results/m1-210210-nebular-2026-09-30/run/manifest.json"
  },
  {
    "id": "neb-eline-run-53521924",
    "arm": "neb_eline",
    "status": "failed",
    "error": "fit finished; host closed SSH during retrieval, rsync exit 255 three times, result file not retrieved; instance 53521924 (host 142157) destroyed; $0.270 billed",
    "target": "M1_210210",
    "artifacts": [
      {
        "label": "53521924-fit-1.log",
        "path": "results/m1-210210-nebular-2026-09-30/run/53521924-fit-1.log"
      },
      {
        "label": "driver.log",
        "path": "results/m1-210210-nebular-2026-09-30/driver.log"
      },
      {
        "label": "manifest.json",
        "path": "results/m1-210210-nebular-2026-09-30/run/manifest.json"
      }
    ],
    "code": "4dd6c3a",
    "model": "Ceridwen ee68b5f; sedpy_jax 9d8aa19; grid amist_c3k_hr_krou_afe_nebular.h5 sha256 6fe00c55a177a93d5c74782e94d3a78418ce2ad856a4edfca8dcd8ed5e572a67",
    "config": "results/m1-210210-nebular-2026-09-30/run/manifest.json",
    "seed": 20260927,
    "data": "results/m1-210210-nebular-2026-09-30/run/manifest.json"
  },
  {
    "id": "neb-eline-run-53526532",
    "arm": "neb_eline",
    "status": "complete",
    "target": "M1_210210",
    "artifacts": [
      {
        "label": "Executed fit · M1_210210",
        "path": "results/m1-210210-nebular-2026-09-30/run/fits/neb_eline/210210-M1_210210/M1_210210_executed.ipynb"
      },
      {
        "label": "ceridwen_result.h5",
        "path": "results/m1-210210-nebular-2026-09-30/run/fits/neb_eline/210210-M1_210210/ceridwen_result.h5"
      },
      {
        "label": "ceridwen_derived_outputs.h5",
        "path": "results/m1-210210-nebular-2026-09-30/run/fits/neb_eline/210210-M1_210210/ceridwen_derived_outputs.h5"
      },
      {
        "label": "53526532-fit-1.log",
        "path": "results/m1-210210-nebular-2026-09-30/run/53526532-fit-1.log"
      }
    ],
    "code": "4dd6c3a",
    "model": "Ceridwen ee68b5f; sedpy_jax 9d8aa19; grid amist_c3k_hr_krou_afe_nebular.h5 sha256 6fe00c55a177a93d5c74782e94d3a78418ce2ad856a4edfca8dcd8ed5e572a67",
    "config": "results/m1-210210-nebular-2026-09-30/run/manifest.json",
    "seed": 20260927,
    "data": "results/m1-210210-nebular-2026-09-30/run/manifest.json"
  },
  {
    "id": "neb-maskca-run-53526532",
    "arm": "neb_maskca",
    "status": "complete",
    "target": "M1_210210",
    "artifacts": [
      {
        "label": "Executed fit · M1_210210",
        "path": "results/m1-210210-nebular-2026-09-30/run/fits/neb_maskca/210210-M1_210210/M1_210210_executed.ipynb"
      },
      {
        "label": "ceridwen_result.h5",
        "path": "results/m1-210210-nebular-2026-09-30/run/fits/neb_maskca/210210-M1_210210/ceridwen_result.h5"
      },
      {
        "label": "ceridwen_derived_outputs.h5",
        "path": "results/m1-210210-nebular-2026-09-30/run/fits/neb_maskca/210210-M1_210210/ceridwen_derived_outputs.h5"
      },
      {
        "label": "53526532-fit-2.log",
        "path": "results/m1-210210-nebular-2026-09-30/run/53526532-fit-2.log"
      }
    ],
    "code": "4dd6c3a",
    "model": "Ceridwen ee68b5f; sedpy_jax 9d8aa19; grid amist_c3k_hr_krou_afe_nebular.h5 sha256 6fe00c55a177a93d5c74782e94d3a78418ce2ad856a4edfca8dcd8ed5e572a67",
    "config": "results/m1-210210-nebular-2026-09-30/run/manifest.json",
    "seed": 20260927,
    "data": "results/m1-210210-nebular-2026-09-30/run/manifest.json"
  }
]
```

## Figures

```json
[
  {
    "notebook": "results/m1-210210-kcbump-wide-2026-09-29/run/fits/wide/210210-M1_210210/M1_210210_executed.ipynb",
    "cell": 14,
    "output": 2,
    "run": "wide-run-53420896",
    "target": "M1_210210",
    "arm": "wide",
    "view": "Fits",
    "caption": "M1_210210 · Spectrum · wide, reference."
  },
  {
    "notebook": "results/m1-210210-kcbump-wide-2026-09-29/run/fits/wide/210210-M1_210210/M1_210210_executed.ipynb",
    "cell": 14,
    "output": 0,
    "run": "wide-run-53420896",
    "target": "M1_210210",
    "arm": "wide",
    "view": "Fits",
    "caption": "M1_210210 · Photometry · wide, reference."
  },
  {
    "notebook": "results/m1-210210-nebular-2026-09-30/run/fits/neb/210210-M1_210210/M1_210210_executed.ipynb",
    "cell": 14,
    "output": 2,
    "run": "neb-run-53520349",
    "target": "M1_210210",
    "arm": "neb",
    "view": "Fits",
    "caption": "M1_210210 · Spectrum · neb: nebular grid, H-beta unmasked; otherwise as wide."
  },
  {
    "notebook": "results/m1-210210-nebular-2026-09-30/run/fits/neb/210210-M1_210210/M1_210210_executed.ipynb",
    "cell": 14,
    "output": 0,
    "run": "neb-run-53520349",
    "target": "M1_210210",
    "arm": "neb",
    "view": "Fits",
    "caption": "M1_210210 · Photometry · neb: nebular grid, H-beta unmasked; otherwise as wide."
  },
  {
    "notebook": "results/m1-210210-nebular-2026-09-30/run/fits/neb_eline/210210-M1_210210/M1_210210_executed.ipynb",
    "cell": 14,
    "output": 2,
    "run": "neb-eline-run-53526532",
    "target": "M1_210210",
    "arm": "neb_eline",
    "view": "Fits",
    "caption": "M1_210210 · Spectrum · neb_eline: nebular grid, line marginalisation on, redshift fixed; otherwise as wide."
  },
  {
    "notebook": "results/m1-210210-nebular-2026-09-30/run/fits/neb_eline/210210-M1_210210/M1_210210_executed.ipynb",
    "cell": 14,
    "output": 0,
    "run": "neb-eline-run-53526532",
    "target": "M1_210210",
    "arm": "neb_eline",
    "view": "Fits",
    "caption": "M1_210210 · Photometry · neb_eline: nebular grid, line marginalisation on, redshift fixed; otherwise as wide."
  },
  {
    "notebook": "results/m1-210210-nebular-2026-09-30/run/fits/neb_maskca/210210-M1_210210/M1_210210_executed.ipynb",
    "cell": 14,
    "output": 2,
    "run": "neb-maskca-run-53526532",
    "target": "M1_210210",
    "arm": "neb_maskca",
    "view": "Fits",
    "caption": "M1_210210 · Spectrum · neb_maskca: nebular grid, Ca H+K masked; otherwise as wide."
  },
  {
    "notebook": "results/m1-210210-nebular-2026-09-30/run/fits/neb_maskca/210210-M1_210210/M1_210210_executed.ipynb",
    "cell": 14,
    "output": 0,
    "run": "neb-maskca-run-53526532",
    "target": "M1_210210",
    "arm": "neb_maskca",
    "view": "Fits",
    "caption": "M1_210210 · Photometry · neb_maskca: nebular grid, Ca H+K masked; otherwise as wide."
  },
  {
    "notebook": "results/m1-210210-kcbump-wide-2026-09-29/run/fits/wide/210210-M1_210210/M1_210210_executed.ipynb",
    "cell": 20,
    "output": 3,
    "run": "wide-run-53420896",
    "target": "M1_210210",
    "arm": "wide",
    "view": "SFH",
    "caption": "M1_210210 · SFH · wide, reference."
  },
  {
    "notebook": "results/m1-210210-nebular-2026-09-30/run/fits/neb/210210-M1_210210/M1_210210_executed.ipynb",
    "cell": 20,
    "output": 3,
    "run": "neb-run-53520349",
    "target": "M1_210210",
    "arm": "neb",
    "view": "SFH",
    "caption": "M1_210210 · SFH · neb: nebular grid, H-beta unmasked; otherwise as wide."
  },
  {
    "notebook": "results/m1-210210-nebular-2026-09-30/run/fits/neb_eline/210210-M1_210210/M1_210210_executed.ipynb",
    "cell": 20,
    "output": 3,
    "run": "neb-eline-run-53526532",
    "target": "M1_210210",
    "arm": "neb_eline",
    "view": "SFH",
    "caption": "M1_210210 · SFH · neb_eline: nebular grid, line marginalisation on, redshift fixed; otherwise as wide."
  },
  {
    "notebook": "results/m1-210210-nebular-2026-09-30/run/fits/neb_maskca/210210-M1_210210/M1_210210_executed.ipynb",
    "cell": 20,
    "output": 3,
    "run": "neb-maskca-run-53526532",
    "target": "M1_210210",
    "arm": "neb_maskca",
    "view": "SFH",
    "caption": "M1_210210 · SFH · neb_maskca: nebular grid, Ca H+K masked; otherwise as wide."
  },
  {
    "notebook": "results/m1-210210-kcbump-wide-2026-09-29/run/fits/wide/210210-M1_210210/M1_210210_executed.ipynb",
    "cell": 20,
    "output": 0,
    "run": "wide-run-53420896",
    "target": "M1_210210",
    "arm": "wide",
    "view": "Posteriors",
    "caption": "M1_210210 · Posteriors · wide, reference."
  },
  {
    "notebook": "results/m1-210210-nebular-2026-09-30/run/fits/neb/210210-M1_210210/M1_210210_executed.ipynb",
    "cell": 20,
    "output": 0,
    "run": "neb-run-53520349",
    "target": "M1_210210",
    "arm": "neb",
    "view": "Posteriors",
    "caption": "M1_210210 · Posteriors · neb: nebular grid, H-beta unmasked; otherwise as wide."
  },
  {
    "notebook": "results/m1-210210-nebular-2026-09-30/run/fits/neb_eline/210210-M1_210210/M1_210210_executed.ipynb",
    "cell": 20,
    "output": 0,
    "run": "neb-eline-run-53526532",
    "target": "M1_210210",
    "arm": "neb_eline",
    "view": "Posteriors",
    "caption": "M1_210210 · Posteriors · neb_eline: nebular grid, line marginalisation on, redshift fixed; otherwise as wide."
  },
  {
    "notebook": "results/m1-210210-nebular-2026-09-30/run/fits/neb_maskca/210210-M1_210210/M1_210210_executed.ipynb",
    "cell": 20,
    "output": 0,
    "run": "neb-maskca-run-53526532",
    "target": "M1_210210",
    "arm": "neb_maskca",
    "view": "Posteriors",
    "caption": "M1_210210 · Posteriors · neb_maskca: nebular grid, Ca H+K masked; otherwise as wide."
  }
]
```

## Measurements

## Results

- Order: `wide` / `neb` / `neb_eline` / `neb_maskca`; values are posterior median [16, 84] from each arm’s `ceridwen_result.h5` and `ceridwen_derived_outputs.h5`.
- \(\ln Z\): 231508.68 ± 0.38 / 240178.15 ± 0.32 / 256972.82 ± 0.30 / 226751.06 ± 0.23.
- ESS: 4343 / 4957 / 4711 / 4983.
- Joint \(\chi^2\) / degrees of freedom: 3777.3/3551 / 3901.9/3685 / 4067.8/3954 / 3661.2/3480.
- Photometric \(\chi^2\) / 28 bands: 47.0 / 40.5 / 38.9 / 41.2.
- Mass fraction formed at 0–30 Myr: 9.58e-4 [8.91e-4, 1.04e-3] / 4.84e-5 [3.93e-5, 5.59e-5] / 1.97e-6 [3.31e-8, 1.23e-5] / 1.96e-5 [9.26e-6, 2.83e-5].
- Mass fraction formed at 30–100 Myr: 7.22e-6 [4.45e-7, 2.50e-5] / 1.79e-3 [1.65e-3, 1.92e-3] / 2.30e-3 [2.12e-3, 2.45e-3] / 3.71e-5 [1.45e-5, 7.59e-5].
- Mass fraction formed at 100–146 Myr: 3.48e-6 [2.66e-7, 1.24e-5] / 1.14e-3 [1.05e-3, 1.23e-3] / 1.53e-3 [1.44e-3, 1.62e-3] / 1.82e-5 [5.94e-6, 4.92e-5].
- Mass fraction formed at 146 Myr–1.4 Gyr: 1.48e-4 [1.85e-5, 7.53e-4] / 1.76e-4 [2.47e-5, 6.03e-4] / 5.72e-4 [1.14e-4, 2.02e-3] / 6.86e-4 [1.45e-4, 2.71e-3].
- \(\delta_{\mathrm{dust}}\) (`diffuse_delta`): −2.094 [−2.368, −1.856] / −0.808 [−0.987, −0.647] / −0.917 [−1.099, −0.747] / −0.164 [−0.318, −0.029].
- \(E_{\mathrm{bump}}\) (`diffuse_Ebump`): 7.88 [5.09, 10.40] / 10.56 [8.85, 11.59] / 10.42 [8.49, 11.54] / 3.53 [1.11, 7.06].
- \(\tau_{\mathrm{dust}}\) (`diffuse_tau_noll`): 0.161 [0.138, 0.184] / 0.264 [0.234, 0.295] / 0.255 [0.224, 0.286] / 0.316 [0.283, 0.350].
- \(\log_{10}(M_\star/M_\odot)\): 11.508 [11.491, 11.525] / 11.519 [11.502, 11.536] / 11.524 [11.505, 11.542] / 11.491 [11.471, 11.517].
- \([\mathrm{Fe}/\mathrm{H}]\): −0.101 [−0.123, −0.078] / −0.178 [−0.197, −0.160] / −0.158 [−0.178, −0.137] / −0.237 [−0.279, −0.212].
- \([\alpha/\mathrm{Fe}]\): 0.061 [0.051, 0.072] / 0.027 [0.017, 0.037] / 0.051 [0.040, 0.062] / 0.110 [0.097, 0.123].
- \(\sigma_\star\) [km/s]: 263.1 [260.1, 266.0] / 272.2 [269.1, 275.2] / 255.5 [252.4, 258.5] / 263.6 [260.3, 267.1].
- \(t_{\mathrm{MW}}\) [Gyr]: 4.52 / 4.35 / 4.43 / 3.58.
- \(P(\delta_{\mathrm{dust}} > -0.4)\): 0.000 / 0.006 / 0.001 / 0.930.
- \(P(E_{\mathrm{bump}} < 3)\): 0.031 / 0.000 / 0.000 / 0.430.
- Checks: remote executed notebooks embedded no figures; post-fit cells re-run locally on CPU from stored `ceridwen_result.h5` with `scripts/regenerate_fit_notebooks.py`, Ceridwen `f973c10` and sedpy_jax `9d8aa19`. `f973c10` differs from `ee68b5f` only in `ceridwen/sampler/nested.py` and its test.
- Validation: `scripts.experiment.validate_result` passes for the three arms.
- Compute: $0.61 invoiced total (`run/charges.json`). Instance 53520349 (host 662751): `neb` finished; `neb_eline` stopped after 30 s with `ValueError: emission lines need FSPS's $SPS_HOME/data/emlines_info.dat, which needs $SPS_HOME`; `scripts/experiment.py` did not export `SPS_HOME`; $0.129, destroyed.
- Compute: three create calls returned no response and started no instance. Instance 53521924 (host 142157): `neb_eline` fit finished; host closed SSH during retrieval, rsync exit 255 three times, result file not retrieved; $0.270, destroyed.
- Compute: instance 53526532 (host 58623): `neb_eline` and `neb_maskca` finished; $0.211, destroyed. `scripts/experiment.py` now sets `SPS_HOME` for the fit command.

## Caveats

- \(\ln Z\) and joint \(\chi^2\) not comparable between arms: fitted data differ; degrees of freedom 3551 / 3685 / 3954 / 3480.
- `neb_maskca` excludes Ca II H and K from the likelihood.
- `neb` and `neb_eline` \(E_{\mathrm{bump}}\) 84th percentiles, 11.59 and 11.54, near the 12 prior bound.
- Nebular emission only for SSPs with \(\log_{10}(\mathrm{age}/\mathrm{yr}) \le 7.30\); \(\log U\) and gas-metallicity rule fixed in the grid, not sampled.
- One galaxy.

## References

- [q-dust-index-railing](wiki/research/questions/q-dust-index-railing.md)
- [q-emission-lines](wiki/research/questions/q-emission-lines.md)
- [e-dust-bump](wiki/research/experiments/e-dust-bump.md)
- [e-emission-line-marginalisation](wiki/research/experiments/e-emission-line-marginalisation.md)
- [e-mask-all-ca](wiki/research/experiments/e-mask-all-ca.md)

## Your interpretation

```json
[]
```

## Next decision

```json
[]
```
