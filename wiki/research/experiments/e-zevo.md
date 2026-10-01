---
kind: experiment
id: e-zevo
title: M1_210210 with metallicity evolution on production defaults
date: 2026-09-30
results_at: 2026-09-30T18:46:00+01:00
origin: new
status: results-ready
question: q-metallicity-evolution
related_questions: q-dust-index-railing
follow_up:
result_groups: results/m1-210210-neb-eline-ca-nohe-zevo-2026-09-30
features: metallicity_evolution, zh_beta_unit
finding: M1_210210, neb_eline_ca_nohe_zevo minus neb_eline_ca_nohe: ln Z +8.3; beta 0.714; [Fe/H] −0.160 to −0.114; t_MW 3.37 to 3.44 Gyr.
---

## Context

- M1_210210, LEGA-C DR2, \(z_{\mathrm{cat}}=0.6542\). Fitted rest-frame range 3747.6–5220.2 Å (observed 6199–8635 Å). Same data as [e-mask-all-ca](wiki/research/experiments/e-mask-all-ca.md).
- Reference arm: `neb_eline_ca_nohe` of [e-mask-all-ca](wiki/research/experiments/e-mask-all-ca.md). Nebular grid, emission-line marginalisation, split Ca II H mask, fixed redshift. Priors: `diffuse_delta` Uniform(−3, 0.4), `diffuse_Ebump` Uniform(0, 12). Results: `results/m1-210210-neb-eline-ca-nohe-2026-09-30/`.
- Metallicity evolution: \(Z(m)=Z_f-(Z_f-Z_0)(1-m)^\alpha\), with formed-mass fraction \(m\), \(\beta=1/(1+\alpha)\), and \(Z_0=\min(Z_\odot/50,\langle Z\rangle)\). Parameter `Z` becomes \(\log_{10}(\langle Z\rangle/Z_\odot)\). Source: `notebooks/ceridwen_integrated_photometry_spectra.ipynb`, Gallazzi+26 Table 1 comment. Implemented in Ceridwen `ee68b5f`, included in pinned `0a3bd51`.
- Precedent: `wide` / `zevo` in [e-dust-bump](wiki/research/experiments/e-dust-bump.md), without the nebular grid. \(\ln Z\): 231508.68 / 231525.02. `zevo` \(\beta\): 0.664 [0.596, 0.701]. Source: `results/m1-210210-kcbump-wide-zevo-2026-09-29/`.
- Production base: `notebooks/ceridwen_integrated_photometry_spectra.ipynb` at `dc1dbec`. Nebular grid, `emission_line_marginalisation = true`, `emission_lines = [3934.77, 3966.6, 3973.3, 4227.92]`, masks at ±1500 km/s, fixed redshift.

## Before delegation

```json
[
  {
    "date": "2026-09-30",
    "text": "the metallicity-evolution slope (ZH beta, the zevo arm of wiki/research/experiments/e-dust-bump.md) should be part of the production default",
    "display_text": "The metallicity-evolution slope (ZH beta, the zevo arm of e-dust-bump) should be part of the production default.",
    "source_ref": "Relayed by the Astronomy lead"
  },
  {
    "date": "2026-09-30",
    "text": "this could go in a separate result as a comparison of the effects of z evo",
    "display_text": "This could go in a separate result as a comparison of the effects of z evo.",
    "source_ref": "Relayed by the Astronomy lead"
  }
]
```

## Execution plan

- Comparison: `neb_eline_ca_nohe_zevo` against `neb_eline_ca_nohe` for M1_210210. One new arm, one target.
- Baseline: reference configuration from `results/m1-210210-neb-eline-ca-nohe-2026-09-30/`, including wide dust priors.
- Data and seed: same data, 3607 fitted pixels, 14 SFH bins, seed 20260927.
- Model: `~/.ceridwen/grids/amist_c3k_hr_krou_afe_nebular.h5`. Priors: `diffuse_delta` Uniform(−3, 0.4), `diffuse_Ebump` Uniform(0, 12), notebook-default `zh_beta_unit` Uniform(0, 1).
- Controlled change: `metallicity_evolution = true`. Other configuration unchanged. Sample `zh_beta_unit` only with metallicity evolution. Config: `results/m1-210210-neb-eline-ca-nohe-zevo-2026-09-30/experiment.json`.
- Hardware: Vast.ai RTX 5090, $1 cap. Command: `python3 scripts/experiment.py run results/m1-210210-neb-eline-ca-nohe-zevo-2026-09-30/experiment.json --gpu "RTX 5090" --output results/m1-210210-neb-eline-ca-nohe-zevo-2026-09-30/run`.
- Run outputs: `results/m1-210210-neb-eline-ca-nohe-zevo-2026-09-30/run/fits/neb_eline_ca_nohe_zevo/210210-M1_210210/`.
- Analysis: `results/m1-210210-neb-eline-ca-nohe-zevo-2026-09-30/analysis.ipynb` writes `comparison.csv`, `sfh-M1_210210.png`, and `corner-M1_210210.png`. Corner parameters: `logmass`, `Z`, `afe`, `tau_dust`, `dust_index`, `ebump`, `dust_ratio`, \(\beta\), \(t_{\mathrm{MW}}\). The \(\beta\) panel contains only the metallicity-evolution arm.
- Requested outputs: this comparison record, then `metallicity_evolution` enabled in production defaults. Files: `notebooks/ceridwen_integrated_photometry_spectra.ipynb`, `wiki/fit_settings.py`, `wiki/notes/model.md`, and tests.

## Amendments

```json
[]
```

## Runs

```json
[
  {
    "id": "zevo-prod-run-53558252",
    "arm": "neb_eline_ca_nohe_zevo",
    "status": "complete",
    "target": "M1_210210",
    "artifacts": [
      {
        "label": "Executed fit · M1_210210",
        "path": "results/m1-210210-neb-eline-ca-nohe-zevo-2026-09-30/run/fits/neb_eline_ca_nohe_zevo/210210-M1_210210/M1_210210_executed.ipynb"
      },
      {
        "label": "ceridwen_result.h5",
        "path": "results/m1-210210-neb-eline-ca-nohe-zevo-2026-09-30/run/fits/neb_eline_ca_nohe_zevo/210210-M1_210210/ceridwen_result.h5"
      },
      {
        "label": "ceridwen_derived_outputs.h5",
        "path": "results/m1-210210-neb-eline-ca-nohe-zevo-2026-09-30/run/fits/neb_eline_ca_nohe_zevo/210210-M1_210210/ceridwen_derived_outputs.h5"
      },
      {
        "label": "53558252-fit-0.log",
        "path": "results/m1-210210-neb-eline-ca-nohe-zevo-2026-09-30/run/53558252-fit-0.log"
      }
    ],
    "code": "dc1dbec",
    "model": "Ceridwen 0a3bd51; sedpy_jax 9d8aa19; grid amist_c3k_hr_krou_afe_nebular.h5 sha256 6fe00c55a177a93d5c74782e94d3a78418ce2ad856a4edfca8dcd8ed5e572a67",
    "config": "results/m1-210210-neb-eline-ca-nohe-zevo-2026-09-30/run/manifest.json",
    "seed": 20260927,
    "data": "results/m1-210210-neb-eline-ca-nohe-zevo-2026-09-30/run/manifest.json"
  }
]
```

## Figures

```json
[
  {
    "notebook": "results/m1-210210-neb-eline-ca-nohe-zevo-2026-09-30/run/fits/neb_eline_ca_nohe_zevo/210210-M1_210210/M1_210210_executed.ipynb",
    "cell": 14,
    "output": 2,
    "run": "zevo-prod-run-53558252",
    "target": "M1_210210",
    "arm": "neb_eline_ca_nohe_zevo",
    "view": "Fits",
    "caption": "M1_210210 · Spectrum · neb_eline_ca_nohe_zevo: metallicity evolution on; otherwise as neb_eline_ca_nohe."
  },
  {
    "notebook": "results/m1-210210-neb-eline-ca-nohe-zevo-2026-09-30/run/fits/neb_eline_ca_nohe_zevo/210210-M1_210210/M1_210210_executed.ipynb",
    "cell": 14,
    "output": 0,
    "run": "zevo-prod-run-53558252",
    "target": "M1_210210",
    "arm": "neb_eline_ca_nohe_zevo",
    "view": "Fits",
    "caption": "M1_210210 · Photometry · neb_eline_ca_nohe_zevo: metallicity evolution on; otherwise as neb_eline_ca_nohe."
  },
  {
    "path": "results/m1-210210-neb-eline-ca-nohe-zevo-2026-09-30/spectrum-neb_eline_ca_nohe-M1_210210.png",
    "view": "Comparison",
    "target": "M1_210210",
    "caption": "M1_210210 · Spectrum · neb_eline_ca_nohe (reference): nebular grid, line marginalisation without H-epsilon, Ca mask, slope prior U(-3, 0.4), bump prior U(0, 12)."
  },
  {
    "path": "results/m1-210210-neb-eline-ca-nohe-zevo-2026-09-30/photometry-neb_eline_ca_nohe-M1_210210.png",
    "view": "Comparison",
    "target": "M1_210210",
    "caption": "M1_210210 · Photometry · neb_eline_ca_nohe (reference): nebular grid, line marginalisation without H-epsilon, Ca mask, slope prior U(-3, 0.4), bump prior U(0, 12)."
  },
  {
    "path": "results/m1-210210-neb-eline-ca-nohe-zevo-2026-09-30/sfh-M1_210210.png",
    "view": "Comparison",
    "target": "M1_210210",
    "caption": "M1_210210 · SFH · neb_eline_ca_nohe / neb_eline_ca_nohe_zevo: SFR per formed mass against lookback time; right panel cumulative mass fraction."
  },
  {
    "path": "results/m1-210210-neb-eline-ca-nohe-zevo-2026-09-30/corner-M1_210210.png",
    "view": "Comparison",
    "target": "M1_210210",
    "caption": "M1_210210 · Posteriors · neb_eline_ca_nohe / neb_eline_ca_nohe_zevo: log M*, [Fe/H], [a/Fe], tau_dust, delta_dust, E_bump, dust ratio, beta_ZH, t_MW with 1-sigma contours; beta only in the zevo arm; zevo [Fe/H] is formed-mass-weighted."
  }
]
```

## Measurements

## Results

- Order: `neb_eline_ca_nohe` / `neb_eline_ca_nohe_zevo`; posterior median [16, 84] from `results/m1-210210-neb-eline-ca-nohe-zevo-2026-09-30/comparison.csv`. Same fitted data (3607 pixels, 28 bands); \(\ln Z\) directly comparable.
- \(\ln Z\): 235993.06 ± 0.22 / 236001.31 ± 0.18.
- ESS: 3947 / 4142.
- Joint \(\chi^2\) / degrees of freedom: 3764.1/3635 / 3791.5/3635. Spectral \(\chi^2\) at the reference floor (2.39%): 3731.3 / 3716.5.
- Photometric \(\chi^2\) / 28 bands: 40.7 / 40.9. CFHT \(u^*\) pull: +0.90 / +0.86.
- \(\log_{10}(M_\star/M_\odot)\): 11.458 [11.436, 11.478] / 11.465 [11.436, 11.496].
- \([\mathrm{Fe}/\mathrm{H}]\): −0.160 [−0.178, −0.140] / −0.114 [−0.142, −0.089]; constant metallicity for `neb_eline_ca_nohe`, \(\log_{10}(\langle Z\rangle/Z_\odot)\) for `neb_eline_ca_nohe_zevo`.
- \(\beta\): 0.714 [0.651, 0.750]; \(Z_0\): \([\mathrm{Fe}/\mathrm{H}]=-1.699\), \(Z_\odot/50\) in all samples; \(Z_f\): \([\mathrm{Fe}/\mathrm{H}]=0.425\;[0.329,0.481]\).
- \([\alpha/\mathrm{Fe}]\): 0.129 [0.115, 0.141] / 0.133 [0.120, 0.147].
- \(\tau_{\mathrm{dust}}\) (`diffuse_tau_noll`): 0.299 [0.269, 0.332] / 0.323 [0.290, 0.353].
- \(\delta_{\mathrm{dust}}\) (`diffuse_delta`): −0.184 [−0.334, −0.041] / −0.138 [−0.281, −0.005].
- \(E_{\mathrm{bump}}\) (`diffuse_Ebump`): 2.47 [0.72, 5.58] / 2.15 [0.63, 5.04].
- \(r_{\mathrm{dust}}\) (`dust_ratio`): 1.013 [0.734, 1.315] / 0.982 [0.705, 1.290].
- \(\sigma_\star\) [km/s]: 261.2 [258.2, 264.8] / 261.0 [257.8, 264.3].
- \(t_{\mathrm{MW}}\) [Gyr]: 3.37 [3.05, 3.73] / 3.44 [3.07, 3.96]. \(t_{50}\) [Gyr]: 2.92 / 3.17.
- Mass fraction formed at 0.66–0.97 Gyr: 0.0001 / 0.0117 [0.0011, 0.0229]. At 0.97–1.41 Gyr: 0.0011 [0.0000, 0.0269] / 0.0450 [0.0191, 0.0673]. At 1.41–2.07 Gyr: 0.166 / 0.120. At 2.07–3.02 Gyr: 0.367 / 0.267. At 3.02–4.40 Gyr: 0.264 / 0.290. At 4.40–6.43 Gyr: 0.152 / 0.165. At 6.43–7.57 Gyr: 0.048 / 0.053. Below 0.66 Gyr: 0.000 in both.
- Sampler wall time: 594.5 s / 628.2 s. Likelihood calls: 5571353 / 5662158.
- Validation: `scripts.experiment.validate_result` passes for `neb_eline_ca_nohe_zevo`.
- Checks: figures rebuilt locally on CPU with `scripts/regenerate_fit_notebooks.py` under pinned Ceridwen `0a3bd51`; the working tree at `37f04b0` lacks `mass_mapped_beta`. GPU `ceridwen_derived_outputs.h5` kept byte-identical.
- Compute, `results/m1-210210-neb-eline-ca-nohe-zevo-2026-09-30`: $0.162 invoiced. Four create calls returned no JSON and started no instance. Instance 53558252 (host 146008): `neb_eline_ca_nohe_zevo` finished; destroyed.

## Caveats

- \(Z_f\) \([\mathrm{Fe}/\mathrm{H}]=0.425\;[0.329,0.481]\) approaches the grid top (0.5).
- One galaxy.

## References

- [q-metallicity-evolution](wiki/research/questions/q-metallicity-evolution.md)
- [q-dust-index-railing](wiki/research/questions/q-dust-index-railing.md)
- [e-mask-all-ca](wiki/research/experiments/e-mask-all-ca.md)
- [e-dust-bump](wiki/research/experiments/e-dust-bump.md)

## Your interpretation

```json
[]
```

## Next decision

```json
[]
```
