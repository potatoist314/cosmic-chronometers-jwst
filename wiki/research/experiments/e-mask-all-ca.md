---
kind: experiment
id: e-mask-all-ca
title: M1_210210 with every Ca feature masked
date: 2026-09-30
results_at: 2026-09-30T16:39:13+01:00
origin: new
status: results-ready
question: q-dust-index-railing
related_questions: q-fitting-choices
follow_up:
result_groups: results/m1-210210-maskallca-2026-09-30, results/m1-210210-neb-eline-ca-2026-09-30, results/m1-210210-neb-eline-ca-nohe-2026-09-30
features: emission_lines, emission_line_marginalisation, ssp_grid
finding: M1_210210, neb_maskca / neb_maskallca / neb_eline_ca / neb_eline_ca_nohe: delta_dust −0.164 / −0.154 / −0.183 / −0.184; E_bump 3.53 / 3.02 / 2.15 / 2.47; mass fraction formed at 0–30 Myr 1.96e-5 / 1.37e-5 / 5.87e-7 / 1.33e-6.
---

## Context

M1_210210, LEGA-C DR2, \(z_{\mathrm{cat}} = 0.6542\). Fitted rest-frame range 3747.6–5220.2 Å (observed 6199–8635 Å). All wavelengths below vacuum unless marked air.

Grid `amist_c3k_hr_krou_afe`: α-MC (Park et al. 2025, arXiv:2410.21375, Sec. 1). The \([\alpha/\mathrm{Fe}]\) axis scales O, Ne, Mg, Si, S, Ar, Ca and Ti uniformly at fixed \([\mathrm{Fe}/\mathrm{H}]\); model \([\mathrm{Ca}/\mathrm{Fe}] = [\mathrm{Mg}/\mathrm{Fe}]\). Conroy, Graves & van Dokkum 2014 (arXiv:1303.6629, Sec. 5.2), SDSS early-type galaxy stacks: "Ca tracks Fe closely over the full sample".

Arm `neb_maskca` of `e-nebular-grid` masks Ca II K 3934.77 Å and Ca II H 3969.59 Å at ±1500 km/s. At those unfitted pixels, summed (observed − posterior-median model)/model within ±7 Å rest of each centre: +18.8% (K), +14.9% (H). Model lines deeper than data. Source: `results/m1-210210-nebular-2026-09-30/run/fits/neb_maskca/210210-M1_210210/ceridwen_derived_outputs.h5`; datasets `spectrum/observed` and `spectrum/posterior_q50`.

Same ratio in velocity shells \(|\Delta v|\) 0–500 / 500–1000 / 1000–1500 km/s: K +19.4% / +4.0% / +0.5%; H +15.5% / +4.7% / +1.7%. In 1500–2000 km/s: K −1.0%, H −0.7%. Arm `neb` (Ca fitted): same ±7 Å ratio +1.6% (K), +7.5% (H).

Ca II absorption by gas in the galaxy adds to the observed stellar line; sign opposite to the residual. Sardane, Turnshek & Rao 2015 (arXiv:1504.02029, abstract): SDSS Ca II absorbers, sample threshold \(W_0(3934) \ge 0.16\) Å, two populations divided at 0.7 Å. Milky Way Ca II at observed 3934.77 and 3969.59 Å, outside the fitted observed range.

Hε 3971.20 Å (NIST ASD): 1.6 Å from Ca II H, inside the H window. K window: no Balmer line.

\([\mathrm{Ca}/\mathrm{Fe}]\) near solar while \([\mathrm{Mg}/\mathrm{Fe}]\) rises with \(\sigma\): Conroy, Graves & van Dokkum 2014 (arXiv:1303.6629, Sec. 5.2, Fig. 13); Johansson, Thomas & Maraston 2012 (arXiv:1112.0322, Sec. 5.9, Fig. 13; Sec. 7: flat, 0.1–0.2 dex below \([\mathrm{Mg}/\mathrm{Fe}]\)); Parikh et al. 2019 (arXiv:1812.02753, Sec. 4.3, Fig. 9: Ca follows Fe); Graves et al. 2007 (arXiv:0707.1523, abstract).

Beverage et al. 2023 (arXiv:2303.03412, Sec. 7): Mg enhanced, Si/Ca/Ti solar at \(z \sim 0.7\) and 0. Prochaska, Rose & Schiavon 2005 (arXiv:astro-ph/0509764, Sec. 6): Ca4227r index raises \([\mathrm{Ca}/\mathrm{Fe}]\) 0.3 dex; Lick Ca4227 CN-contaminated. Bensby et al. 2014 (arXiv:1309.2631, Fig. 15): MW \([\mathrm{X}/\mathrm{Fe}]\) plateaus. Iwamoto et al. 1999 (arXiv:astro-ph/0002337, Sec. 5, Table 3): SNIa W7 Si–Ca; SNII O/Mg-rich.

One \([\alpha/\mathrm{Fe}]\) axis scales \(\alpha\) elements for isochrone and opacity consistency: α-MC (arXiv:2410.21375, Sec. 2.1; Sec. 1 caveat); MILES (Vazdekis et al. 2015, arXiv:1504.08032, Sec. 2.3.2, +0.4); sMILES (Knowles et al. 2023, arXiv:2306.05942, Sec. 2.1.2, lockstep for atmosphere consistency). Separate Ca exists: TMJ11 index tables (arXiv:1010.4569, Sec. 3.5, \([\mathrm{X}/\alpha]\) including Ca); alf spectra (arXiv:1205.6473, Sec. 3).

Existing artefacts: alf code and models (github.com/cconroy20/alf; manual Sec. 1.1: ~100 CPU-hr per converged fit; continuum-normalized only); sMILES SSPs public (miles.iac.es) but lockstep; TMJ tables public (indices only); index analyses use Mgb plus Fe4383 without Ca (Bevacqua et al. 2023, arXiv:2308.03441).

That ISM term is small: quiescent \(A_V < 0.5\) (Kriek & Conroy 2013, arXiv:1308.1099); ISM Na D 0.1–0.5 Å at \(E(B-V)\) 0.02–0.05 against ~4 Å stellar (Poznanski et al. 2012, arXiv:1206.6107, Eq. 9); Ca II absorbers split at 0.7 Å with dust depletion (arXiv:1504.02029).

Jonah Powley meeting, 2026-09-17: “Ca I can be masked because of potential IGM contamination” (see References). The ISM check covers host-galaxy ISM absorption (sign, size) and Milky Way foreground position; it does not cover intervening IGM absorbers on the sightline.

## Before delegation

```json
[
  {
    "date": "2026-09-30",
    "text": "tell me more about Ca tracking Fe instead of being like other alpha elements. is this well known? if so, why does all the alpha enhanced ssp grids just treat it together?",
    "display_text": "Tell me more about Ca tracking Fe instead of being like other alpha elements. Is this well known? If so, why do all the alpha-enhanced SSP grids just treat it together?",
    "source_ref": "Relayed by the Astronomy lead"
  },
  {
    "date": "2026-09-30",
    "text": "what about the impact of ISM? someone mentioned Ca might be contaminated by ISM but they were very unsure",
    "display_text": "What about the impact of ISM? Someone mentioned Ca might be contaminated by ISM but they were very unsure.",
    "source_ref": "Relayed by the Astronomy lead"
  },
  {
    "date": "2026-09-30",
    "text": "i was told to mask all Ca",
    "display_text": "I was told to mask all Ca.",
    "source_ref": "Relayed by the Astronomy lead"
  }
]
```

## Execution plan

- Comparison: `neb_maskallca`, `neb_eline_ca` and `neb_eline_ca_nohe` for M1_210210 against `neb_maskca` and `neb_eline` of `e-nebular-grid`. Further arm `neb_maskallca_eline` configured.
- Ca4455 band stays in the fit (Liu Hao, 2026-09-30).
- Baseline: same data, seed 20260927, 14 SFH bins; SFH-basis fast path on.
- Model: nebular grid `~/.ceridwen/grids/amist_c3k_hr_krou_afe_nebular.h5`; priors `diffuse_delta` Uniform(−3, 0.4) and `diffuse_Ebump` Uniform(0, 12).
- Controlled change, `neb_maskallca`: `emission_lines = [3726.0, 3728.8, 3934.77, 3969.59, 4227.92, 4958.9, 5006.8]`; notebook masks each entry at ±1500 km/s (`dv=1500.0`, cell 6). No code change.
- Controlled change, `neb_eline_ca`: `emission_line_marginalisation = true`; `emission_lines = [3934.77, 3966.6, 3973.3, 4227.92]`. [O II], Hβ and [O III] unmasked; modelled by nebular grid plus free non-negative line fluxes.
- Controlled change, `neb_maskallca_eline`: `emission_line_marginalisation = true`; `emission_lines = [3726.0, 3728.8, 3934.77, 3966.6, 3973.3, 4227.92, 4958.9, 5006.8]`.
- Controlled change, `neb_eline_ca_nohe`: `neb_eline_ca` settings; project commit `762f49f` (branch `drop-masked-line-columns`). Notebook cell 6 rebuilds `EmissionLineColumns` after `mask_lines`; lines with fewer than 3 unmasked pixels within \(2\sigma\) get no free flux. Hε and the [Ne III] 3968 component leave the columns.
- Mask with marginalisation: notebook cell 6 removes a mask entry within 2 Å of a line with a free flux (`EmissionLineColumns.covers`, `tol=2.0`).
- Mask with marginalisation: entry 3969.59 lies within 2 Å of [Ne III] 3968.65 Å and Hε 3971.26 Å (FSPS `emlines_info.dat`, vacuum); entry leaves the mask; 96 of 109 pixels in the Ca II H window fitted.
- Mask with marginalisation: entries 3966.6 and 3973.3 replace it: masked 3946.7–3993.2 Å, 0 fitted pixels in 3949.7–3989.5 Å.
- Mask list: NIST ASD vacuum wavelength; lower level; window. Ca II K 3934.77 Å; ground level; 3915.1–3954.5 Å.
- Mask list: Ca II H 3969.59 Å; ground level; 3949.7–3989.5 Å.
- Mask list: Ca I 4227.92 Å (4226.73 Å air); ground level; 4206.8–4249.1 Å. Window contains Lick Ca4227 band 4222.250–4234.750 Å air = 4223.44–4235.94 Å vacuum (Trager et al. 1998, arXiv:astro-ph/9712258, Table 2: measures Ca, (C)).
- Width: at \(\sigma = 263\) km/s, Gaussian FWHM 619 km/s, 8.1 Å at 3934.77 Å; ±1500 km/s is ±19.7 Å, \(\pm 5.7\sigma\). Shell ratios fall to +0.5% (K) and +1.7% (H) at 1000–1500 km/s.
- Fitted pixels: 3657 in `neb`; 3452 in `neb_maskca`; 3335 in `neb_maskallca`; 3594 in `neb_maskallca_eline`; 3607 in `neb_eline_ca`; 3607 in `neb_eline_ca_nohe`.
- Not in the list: Lick Ca4455 band 4452.125–4474.625 Å air = 4453.37–4475.88 Å vacuum. Trager et al. 1998 Table 2: measures (Fe), (C), Cr. Thomas, Maraston & Bender 2003 (arXiv:astro-ph/0209250, Sec. 3.1.3): "Ca4455 is insensitive to Ca abundance", with Fe and Cr the dominant contributors. Masking at ±1500 km/s about 4464.63 Å removes 123 more pixels.
- Not in the list: Ca I lines from excited levels, NIST ASD lower level 15,158–23,652 cm⁻¹: 4284.22–4319.86 Å (inside Lick G4300 band 4281.375–4316.375 Å air; Trager Table 2: measures C, (O)), 4426.68–4457.86, 4579.83–4587.25, 4879.49, 5043.03, 5190.30 Å.
- Not in the list: Ca II 3737.96 Å, lower level 25,414 cm⁻¹; centre below fitted range.
- Not in the list: Ca II triplet near 8500–8662 Å; outside fitted range.
- Hardware and outputs: Vast.ai RTX 5090; $1 cap per run. Configs: `results/m1-210210-maskallca-2026-09-30/experiment.json` (arms `neb_maskallca`, `neb_maskallca_eline`), `results/m1-210210-neb-eline-ca-2026-09-30/experiment.json` (arm `neb_eline_ca`), `results/m1-210210-neb-eline-ca-nohe-2026-09-30/experiment.json` (arm `neb_eline_ca_nohe`); outputs under each directory’s `run/fits/<arm>/210210-M1_210210/`.
- Run command for each directory: `python3 scripts/experiment.py run results/<dir>/experiment.json --gpu "RTX 5090" --output results/<dir>/run`; `--revision 762f49f` for `neb_eline_ca_nohe`.

## Amendments

```json
[
  {
    "date": "2026-09-30",
    "text": "nebular + marginalisation + ca mask + oiii/oii/h beta unmasked seems good",
    "display_text": "Nebular + marginalisation + Ca mask + [O III]/[O II]/Hβ unmasked seems good.",
    "source_ref": "Relayed by the Astronomy lead"
  },
  {
    "date": "2026-09-30",
    "text": "in this case, it makes sense to drop h epsilon",
    "display_text": "In this case, it makes sense to drop Hε.",
    "source_ref": "Relayed by the Astronomy lead"
  }
]
```

## Runs

```json
[
  {
    "id": "neb-maskallca-run-53539531",
    "arm": "neb_maskallca",
    "status": "complete",
    "target": "M1_210210",
    "artifacts": [
      {
        "label": "Executed fit · M1_210210",
        "path": "results/m1-210210-maskallca-2026-09-30/run/fits/neb_maskallca/210210-M1_210210/M1_210210_executed.ipynb"
      },
      {
        "label": "ceridwen_result.h5",
        "path": "results/m1-210210-maskallca-2026-09-30/run/fits/neb_maskallca/210210-M1_210210/ceridwen_result.h5"
      },
      {
        "label": "ceridwen_derived_outputs.h5",
        "path": "results/m1-210210-maskallca-2026-09-30/run/fits/neb_maskallca/210210-M1_210210/ceridwen_derived_outputs.h5"
      },
      {
        "label": "53539531-fit-0.log",
        "path": "results/m1-210210-maskallca-2026-09-30/run/53539531-fit-0.log"
      }
    ],
    "code": "ec6eab3",
    "model": "Ceridwen 0a3bd51; sedpy_jax 9d8aa19; grid amist_c3k_hr_krou_afe_nebular.h5 sha256 6fe00c55a177a93d5c74782e94d3a78418ce2ad856a4edfca8dcd8ed5e572a67",
    "config": "results/m1-210210-maskallca-2026-09-30/run/manifest.json",
    "seed": 20260927,
    "data": "results/m1-210210-maskallca-2026-09-30/run/manifest.json"
  },
  {
    "id": "neb-maskallca-eline-run-53539531",
    "arm": "neb_maskallca_eline",
    "status": "failed",
    "error": "host 370354 refused SSH during the fit at 14:45:53 UTC; rsync exit 255 three times; instance 53539531 unavailable, destroyed; $0.088 billed",
    "target": "M1_210210",
    "artifacts": [
      {
        "label": "driver.log",
        "path": "results/m1-210210-maskallca-2026-09-30/driver.log"
      },
      {
        "label": "manifest.json",
        "path": "results/m1-210210-maskallca-2026-09-30/run/manifest.json"
      }
    ],
    "code": "ec6eab3",
    "model": "Ceridwen 0a3bd51; sedpy_jax 9d8aa19; grid amist_c3k_hr_krou_afe_nebular.h5 sha256 6fe00c55a177a93d5c74782e94d3a78418ce2ad856a4edfca8dcd8ed5e572a67",
    "config": "results/m1-210210-maskallca-2026-09-30/run/manifest.json",
    "seed": 20260927,
    "data": "results/m1-210210-maskallca-2026-09-30/run/manifest.json"
  },
  {
    "id": "neb-maskallca-eline-run-53541141",
    "arm": "neb_maskallca_eline",
    "status": "failed",
    "error": "instance 53541141 (host 571938) unavailable 6 s after running; no fit started; destroyed; $0.012 billed",
    "target": "M1_210210",
    "artifacts": [
      {
        "label": "driver.log",
        "path": "results/m1-210210-maskallca-2026-09-30/driver.log"
      },
      {
        "label": "manifest.json",
        "path": "results/m1-210210-maskallca-2026-09-30/run/manifest.json"
      }
    ],
    "code": "ec6eab3",
    "model": "Ceridwen 0a3bd51; sedpy_jax 9d8aa19; grid amist_c3k_hr_krou_afe_nebular.h5 sha256 6fe00c55a177a93d5c74782e94d3a78418ce2ad856a4edfca8dcd8ed5e572a67",
    "config": "results/m1-210210-maskallca-2026-09-30/run/manifest.json",
    "seed": 20260927,
    "data": "results/m1-210210-maskallca-2026-09-30/run/manifest.json"
  },
  {
    "id": "neb-eline-ca-run-53540122",
    "arm": "neb_eline_ca",
    "status": "complete",
    "target": "M1_210210",
    "artifacts": [
      {
        "label": "Executed fit · M1_210210",
        "path": "results/m1-210210-neb-eline-ca-2026-09-30/run/fits/neb_eline_ca/210210-M1_210210/M1_210210_executed.ipynb"
      },
      {
        "label": "ceridwen_result.h5",
        "path": "results/m1-210210-neb-eline-ca-2026-09-30/run/fits/neb_eline_ca/210210-M1_210210/ceridwen_result.h5"
      },
      {
        "label": "ceridwen_derived_outputs.h5",
        "path": "results/m1-210210-neb-eline-ca-2026-09-30/run/fits/neb_eline_ca/210210-M1_210210/ceridwen_derived_outputs.h5"
      },
      {
        "label": "53540122-fit-0.log",
        "path": "results/m1-210210-neb-eline-ca-2026-09-30/run/53540122-fit-0.log"
      }
    ],
    "code": "ec6eab3",
    "model": "Ceridwen 0a3bd51; sedpy_jax 9d8aa19; grid amist_c3k_hr_krou_afe_nebular.h5 sha256 6fe00c55a177a93d5c74782e94d3a78418ce2ad856a4edfca8dcd8ed5e572a67",
    "config": "results/m1-210210-neb-eline-ca-2026-09-30/run/manifest.json",
    "seed": 20260927,
    "data": "results/m1-210210-neb-eline-ca-2026-09-30/run/manifest.json"
  },
  {
    "id": "neb-eline-ca-nohe-run-53545621",
    "arm": "neb_eline_ca_nohe",
    "status": "complete",
    "target": "M1_210210",
    "artifacts": [
      {
        "label": "Executed fit · M1_210210",
        "path": "results/m1-210210-neb-eline-ca-nohe-2026-09-30/run/fits/neb_eline_ca_nohe/210210-M1_210210/M1_210210_executed.ipynb"
      },
      {
        "label": "ceridwen_result.h5",
        "path": "results/m1-210210-neb-eline-ca-nohe-2026-09-30/run/fits/neb_eline_ca_nohe/210210-M1_210210/ceridwen_result.h5"
      },
      {
        "label": "ceridwen_derived_outputs.h5",
        "path": "results/m1-210210-neb-eline-ca-nohe-2026-09-30/run/fits/neb_eline_ca_nohe/210210-M1_210210/ceridwen_derived_outputs.h5"
      },
      {
        "label": "53545621-fit-0.log",
        "path": "results/m1-210210-neb-eline-ca-nohe-2026-09-30/run/53545621-fit-0.log"
      }
    ],
    "code": "762f49f",
    "model": "Ceridwen 0a3bd51; sedpy_jax 9d8aa19; grid amist_c3k_hr_krou_afe_nebular.h5 sha256 6fe00c55a177a93d5c74782e94d3a78418ce2ad856a4edfca8dcd8ed5e572a67",
    "config": "results/m1-210210-neb-eline-ca-nohe-2026-09-30/run/manifest.json",
    "seed": 20260927,
    "data": "results/m1-210210-neb-eline-ca-nohe-2026-09-30/run/manifest.json"
  }
]
```

## Figures

```json
[
  {
    "notebook": "results/m1-210210-maskallca-2026-09-30/run/fits/neb_maskallca/210210-M1_210210/M1_210210_executed.ipynb",
    "cell": 14,
    "output": 2,
    "run": "neb-maskallca-run-53539531",
    "target": "M1_210210",
    "arm": "neb_maskallca",
    "view": "Fits",
    "caption": "M1_210210 · Spectrum · neb_maskallca: nebular grid, H-beta unmasked, Ca H+K and Ca I 4227 masked; otherwise as wide."
  },
  {
    "notebook": "results/m1-210210-maskallca-2026-09-30/run/fits/neb_maskallca/210210-M1_210210/M1_210210_executed.ipynb",
    "cell": 14,
    "output": 0,
    "run": "neb-maskallca-run-53539531",
    "target": "M1_210210",
    "arm": "neb_maskallca",
    "view": "Fits",
    "caption": "M1_210210 · Photometry · neb_maskallca: nebular grid, H-beta unmasked, Ca H+K and Ca I 4227 masked; otherwise as wide."
  },
  {
    "notebook": "results/m1-210210-neb-eline-ca-2026-09-30/run/fits/neb_eline_ca/210210-M1_210210/M1_210210_executed.ipynb",
    "cell": 14,
    "output": 2,
    "run": "neb-eline-ca-run-53540122",
    "target": "M1_210210",
    "arm": "neb_eline_ca",
    "view": "Fits",
    "caption": "M1_210210 · Spectrum · neb_eline_ca: nebular grid, line marginalisation on, redshift fixed, mask holds only Ca H+K and Ca I 4227; otherwise as wide."
  },
  {
    "notebook": "results/m1-210210-neb-eline-ca-2026-09-30/run/fits/neb_eline_ca/210210-M1_210210/M1_210210_executed.ipynb",
    "cell": 14,
    "output": 0,
    "run": "neb-eline-ca-run-53540122",
    "target": "M1_210210",
    "arm": "neb_eline_ca",
    "view": "Fits",
    "caption": "M1_210210 · Photometry · neb_eline_ca: nebular grid, line marginalisation on, redshift fixed, mask holds only Ca H+K and Ca I 4227; otherwise as wide."
  },
  {
    "notebook": "results/m1-210210-neb-eline-ca-nohe-2026-09-30/run/fits/neb_eline_ca_nohe/210210-M1_210210/M1_210210_executed.ipynb",
    "cell": 14,
    "output": 2,
    "run": "neb-eline-ca-nohe-run-53545621",
    "target": "M1_210210",
    "arm": "neb_eline_ca_nohe",
    "view": "Fits",
    "caption": "M1_210210 · Spectrum · neb_eline_ca_nohe: H-epsilon column removed; otherwise as neb_eline_ca."
  },
  {
    "notebook": "results/m1-210210-neb-eline-ca-nohe-2026-09-30/run/fits/neb_eline_ca_nohe/210210-M1_210210/M1_210210_executed.ipynb",
    "cell": 14,
    "output": 0,
    "run": "neb-eline-ca-nohe-run-53545621",
    "target": "M1_210210",
    "arm": "neb_eline_ca_nohe",
    "view": "Fits",
    "caption": "M1_210210 · Photometry · neb_eline_ca_nohe: H-epsilon column removed; otherwise as neb_eline_ca."
  },
  {
    "notebook": "results/m1-210210-maskallca-2026-09-30/run/fits/neb_maskallca/210210-M1_210210/M1_210210_executed.ipynb",
    "cell": 20,
    "output": 3,
    "run": "neb-maskallca-run-53539531",
    "target": "M1_210210",
    "arm": "neb_maskallca",
    "view": "SFH",
    "caption": "M1_210210 · SFH · neb_maskallca: nebular grid, H-beta unmasked, Ca H+K and Ca I 4227 masked; otherwise as wide."
  },
  {
    "notebook": "results/m1-210210-neb-eline-ca-2026-09-30/run/fits/neb_eline_ca/210210-M1_210210/M1_210210_executed.ipynb",
    "cell": 20,
    "output": 3,
    "run": "neb-eline-ca-run-53540122",
    "target": "M1_210210",
    "arm": "neb_eline_ca",
    "view": "SFH",
    "caption": "M1_210210 · SFH · neb_eline_ca: nebular grid, line marginalisation on, redshift fixed, mask holds only Ca H+K and Ca I 4227; otherwise as wide."
  },
  {
    "notebook": "results/m1-210210-neb-eline-ca-nohe-2026-09-30/run/fits/neb_eline_ca_nohe/210210-M1_210210/M1_210210_executed.ipynb",
    "cell": 20,
    "output": 3,
    "run": "neb-eline-ca-nohe-run-53545621",
    "target": "M1_210210",
    "arm": "neb_eline_ca_nohe",
    "view": "SFH",
    "caption": "M1_210210 · SFH · neb_eline_ca_nohe: H-epsilon column removed; otherwise as neb_eline_ca."
  },
  {
    "notebook": "results/m1-210210-maskallca-2026-09-30/run/fits/neb_maskallca/210210-M1_210210/M1_210210_executed.ipynb",
    "cell": 20,
    "output": 0,
    "run": "neb-maskallca-run-53539531",
    "target": "M1_210210",
    "arm": "neb_maskallca",
    "view": "Posteriors",
    "caption": "M1_210210 · Posteriors · neb_maskallca: nebular grid, H-beta unmasked, Ca H+K and Ca I 4227 masked; otherwise as wide."
  },
  {
    "notebook": "results/m1-210210-neb-eline-ca-2026-09-30/run/fits/neb_eline_ca/210210-M1_210210/M1_210210_executed.ipynb",
    "cell": 20,
    "output": 0,
    "run": "neb-eline-ca-run-53540122",
    "target": "M1_210210",
    "arm": "neb_eline_ca",
    "view": "Posteriors",
    "caption": "M1_210210 · Posteriors · neb_eline_ca: nebular grid, line marginalisation on, redshift fixed, mask holds only Ca H+K and Ca I 4227; otherwise as wide."
  },
  {
    "notebook": "results/m1-210210-neb-eline-ca-nohe-2026-09-30/run/fits/neb_eline_ca_nohe/210210-M1_210210/M1_210210_executed.ipynb",
    "cell": 20,
    "output": 0,
    "run": "neb-eline-ca-nohe-run-53545621",
    "target": "M1_210210",
    "arm": "neb_eline_ca_nohe",
    "view": "Posteriors",
    "caption": "M1_210210 · Posteriors · neb_eline_ca_nohe: H-epsilon column removed; otherwise as neb_eline_ca."
  }
]
```

## Measurements

## Results

- Order: `neb_maskca` (from `e-nebular-grid`) / `neb_maskallca` / `neb_eline_ca` / `neb_eline_ca_nohe`; posterior median [16, 84] from each arm’s `ceridwen_result.h5` and `ceridwen_derived_outputs.h5`.
- \(\ln Z\): 226751.06 ± 0.23 / 219048.30 ± 0.24 / 235960.51 ± 0.26 / 235993.06 ± 0.22.
- ESS: 4983 / 4815 / 3786 / 3947.
- Joint \(\chi^2\) / degrees of freedom: 3661.2/3480 / 3568.1/3363 / 3737.3/3635 / 3764.1/3635.
- Photometric \(\chi^2\) / 28 bands: 41.2 / 41.3 / 38.4 / 40.7.
- Mass fraction formed at 0–30 Myr: 1.96e-5 [9.26e-6, 2.83e-5] / 1.37e-5 [2.35e-6, 2.39e-5] / 5.87e-7 [6.25e-9, 6.44e-6] / 1.33e-6 [8.14e-8, 8.77e-6].
- Mass fraction formed at 30–100 Myr: 3.71e-5 [1.45e-5, 7.59e-5] / 2.58e-5 [3.24e-6, 5.83e-5] / 1.41e-6 [1.79e-8, 1.77e-5] / 3.68e-6 [2.43e-7, 2.33e-5].
- Mass fraction formed at 100–146 Myr: 1.82e-5 [5.94e-6, 4.92e-5] / 1.24e-5 [1.72e-6, 3.41e-5] / 1.15e-6 [1.48e-8, 1.22e-5] / 2.76e-6 [1.75e-7, 1.69e-5].
- Mass fraction formed at 146 Myr–1.4 Gyr: 6.86e-4 [1.45e-4, 2.71e-3] / 4.05e-4 [7.01e-5, 1.79e-3] / 1.83e-3 [2.54e-5, 2.89e-2] / 2.16e-3 [6.53e-5, 2.83e-2].
- \(\delta_{\mathrm{dust}}\) (`diffuse_delta`): −0.164 [−0.318, −0.029] / −0.154 [−0.309, −0.009] / −0.183 [−0.333, −0.043] / −0.184 [−0.334, −0.041].
- \(E_{\mathrm{bump}}\) (`diffuse_Ebump`): 3.53 [1.11, 7.06] / 3.02 [0.92, 6.37] / 2.15 [0.64, 4.86] / 2.47 [0.72, 5.58].
- \(\tau_{\mathrm{dust}}\) (`diffuse_tau_noll`): 0.316 [0.283, 0.350] / 0.311 [0.278, 0.345] / 0.306 [0.275, 0.339] / 0.299 [0.269, 0.332].
- \(\log_{10}(M_\star/M_\odot)\): 11.491 [11.471, 11.517] / 11.500 [11.476, 11.527] / 11.457 [11.437, 11.479] / 11.458 [11.437, 11.479].
- \([\mathrm{Fe}/\mathrm{H}]\): −0.237 [−0.279, −0.212] / −0.266 [−0.303, −0.223] / −0.158 [−0.177, −0.139] / −0.160 [−0.180, −0.140].
- \([\alpha/\mathrm{Fe}]\): 0.110 [0.097, 0.123] / 0.155 [0.138, 0.171] / 0.129 [0.114, 0.142] / 0.129 [0.115, 0.143].
- \(\sigma_\star\) [km/s]: 263.6 [260.3, 267.1] / 264.9 [261.9, 268.1] / 261.5 [258.4, 264.6] / 261.3 [258.1, 264.6].
- \(t_{\mathrm{MW}}\) [Gyr]: 3.58 / 3.72 / 3.31 / 3.37.
- \(P(\delta_{\mathrm{dust}} > −0.4)\): 0.930 / 0.936 / 0.923 / 0.921.
- \(P(E_{\mathrm{bump}} < 3)\): 0.430 / 0.498 / 0.643 / 0.574.
- Summed (observed − posterior-median model)/model within ±7 Å rest of each line centre, same order: Ca II K +18.8% / +21.8% / +21.5% / +21.5%; Ca II H +14.9% / +16.9% / −86.1% / +18.7%; Ca I 4227.92 Å +1.6% (pixels fitted) / +2.9% / +2.9% / +2.9%. Pixels unfitted unless marked.
- `neb_eline_ca` Hε free flux (`Ba-5 3970`): posterior model at rest 3970.69 Å: 98 [48, 158] µJy; observed 6.4 µJy. Excess rest-frame equivalent width over `neb_maskallca` median model in 3955–3990 Å: 124 [57, 204] Å. HSC r pull +0.66 in `neb_maskallca`, −0.59 in `neb_eline_ca`.
- `neb_eline_ca` free-flux columns: 21. Ba-8, Ba-7, [Ne III] 3869 (+3968), He I 3889, Ba-6, Ba-5 (Hε), [S II] 4070, 4078, Hδ, Hγ, [O III] 4363, He I 4471, He II 4686, [Ar IV] 4711, [Ne IV] 4720, [Ar IV] 4740, Hβ, [O III] 4931, [O III] 5007 (+4959), [Ar III] 5192, [N I] 5200.
- `neb_eline_ca` free-flux columns: no [O II] column; valid pixels start at rest 3742.8 Å.
- `neb_eline_ca_nohe`: no Hε column; maximum posterior-median model in 3955–3990 Å: 16.4 µJy; HSC r pull +0.73.
- `neb_eline_ca_nohe`: 20 free-flux columns; those of `neb_eline_ca` without Ba-5 (Hε); [Ne III] 3869 without the 3968 component.
- `neb_eline_ca_nohe` posterior mass outside notebook default priors `diffuse_delta` Uniform(−1, 0.4) and `diffuse_Ebump` Uniform(0, 6): \(P(\delta_{\mathrm{dust}} < -1) = 0.000\); \(P(E_{\mathrm{bump}} > 6) = 0.134\).
- Sampling wall time: 199.1 s in `neb_maskallca`; 600.6 s in `neb_eline_ca`; 594.5 s in `neb_eline_ca_nohe`.
- Validation: `scripts.experiment.validate_result` passes for `neb_maskallca`, `neb_eline_ca` and `neb_eline_ca_nohe`.
- Checks: figures built locally on CPU from stored posteriors with `scripts/regenerate_fit_notebooks.py`, Ceridwen `0a3bd51`, sedpy_jax `9d8aa19`; GPU `ceridwen_derived_outputs.h5` kept.
- Checks: `neb_eline_ca_nohe` figures built locally with notebook at `762f49f`; GPU `ceridwen_derived_outputs.h5` kept.
- Compute, `results/m1-210210-maskallca-2026-09-30`: $0.100 invoiced. Instance 53539531 (host 370354, interruptible bid): `neb_maskallca` finished; during `neb_maskallca_eline`, host refused SSH at 14:45:53 UTC, rsync exit 255 three times, instance unavailable; $0.088, destroyed. Instance 53541141 (host 571938, interruptible bid): image load 14 min, unavailable 6 s after `running`; $0.012, destroyed. `neb_maskallca_eline` not run.
- Compute, `results/m1-210210-neb-eline-ca-2026-09-30`: $0.095 invoiced. Instance 53540122 (host 81276): `neb_eline_ca` finished; destroyed.
- Compute, `results/m1-210210-neb-eline-ca-nohe-2026-09-30`: $0.093 invoiced. Six create calls returned no response and started no instance. Instance 53545621 (host 81276): `neb_eline_ca_nohe` finished; destroyed.

## Caveats

- \(\ln Z\) and joint \(\chi^2\) not comparable between arms with different fitted data; degrees of freedom 3480 / 3363 / 3635 / 3635.
- `neb_eline_ca` only: Hε (`Ba-5 3970`) has free flux and 0 unmasked spectral pixels within \(2\sigma\) of the line; constrained only by photometry.
- `neb_eline_ca` only: [Ne III] 3968.65 Å has 0 unmasked pixels within \(2\sigma\); flux tied to [Ne III] 3869.92 Å (38 pixels) at ratio 3.318 (Ceridwen `TIED_RATIOS`).
- `neb_eline_ca` and `neb_eline_ca_nohe`: Ca II H mask spans 3946.7–3993.2 Å, wider than ±1500 km/s about 3969.59 Å (3949.7–3989.5 Å).
- `neb_maskallca_eline` has no result.
- Nebular emission only for SSPs with \(\log_{10}(\mathrm{age}/\mathrm{yr}) \leq 7.30\); \(\log U\) and gas-metallicity rule fixed in grid, not sampled.
- One galaxy.

## References

- [q-dust-index-railing](wiki/research/questions/q-dust-index-railing.md)
- [q-fitting-choices](wiki/research/questions/q-fitting-choices.md)
- [e-nebular-grid](wiki/research/experiments/e-nebular-grid.md)
- [Park et al. 2025](https://arxiv.org/abs/2410.21375)
- [Conroy, Graves & van Dokkum 2014](https://arxiv.org/abs/1303.6629)
- [Trager et al. 1998](https://arxiv.org/abs/astro-ph/9712258)
- [Thomas, Maraston & Bender 2003](https://arxiv.org/abs/astro-ph/0209250)
- [Sardane, Turnshek & Rao 2015](https://arxiv.org/abs/1504.02029)
- [NIST Atomic Spectra Database](https://physics.nist.gov/PhysRefData/ASD/lines_form.html)
- [Johansson, Thomas & Maraston 2012](https://arxiv.org/abs/1112.0322)
- [Parikh et al. 2019](https://arxiv.org/abs/1812.02753)
- [Beverage et al. 2023](https://arxiv.org/abs/2303.03412)
- [Graves et al. 2007](https://arxiv.org/abs/0707.1523)
- [Prochaska, Rose & Schiavon 2005](https://arxiv.org/abs/astro-ph/0509764)
- [Bensby et al. 2014](https://arxiv.org/abs/1309.2631)
- [Iwamoto et al. 1999](https://arxiv.org/abs/astro-ph/0002337)
- [Vazdekis et al. 2015](https://arxiv.org/abs/1504.08032)
- [Knowles et al. 2023](https://arxiv.org/abs/2306.05942)
- [Thomas, Maraston & Johansson 2011](https://arxiv.org/abs/1010.4569)
- [Conroy & van Dokkum 2012](https://arxiv.org/abs/1205.6473)
- [Poznanski, Prochaska & Bloom 2012](https://arxiv.org/abs/1206.6107)
- [Kriek & Conroy 2013](https://arxiv.org/abs/1308.1099)
- [Bevacqua et al. 2023](https://arxiv.org/abs/2308.03441)
- [alf](https://github.com/cconroy20/alf)
- [Meeting with Jonah Powley](wiki/notes/meeting-2026-09-17-jonah-powley.md)

## Your interpretation

```json
[]
```

## Next decision

```json
[]
```
