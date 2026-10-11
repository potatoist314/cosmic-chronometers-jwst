# Ceridwen upstream merge (2026-10-10)

## What merged

- ceridwen `upstream-merge` **729fba6** (origin, potatoist314/ceridwen): upstream/main cc8ac9d merged
  into local `speedups` 2d5edc9 (merge c307b54), then:
  - ports of the local speed work onto upstream code (c032d0b, 17d486c, 5cfb739, 852b239);
  - `upstream-merge-fix-core` 6d07e37 (merge ba57bbf): KC13 Noll bump, NumPy FilterSet,
    `Photometry(filter_directory=)` + MegaCam U.MP9302, `SSPData.load(axis_meaning=)`;
  - `upstream-merge-fix-spectrum` b0f7130 (merge 4b1f1a6) and 192fd25 (merge c661d46):
    `Spectrum(projector="chain")` = the local LOSVD + LSF chain, `select_absorption_features`,
    `EmissionLineColumns.from_spectrum(sigma_gas_kms=, sigma_key=, zred_key=)`;
  - b61e998 local spectrum tests on the merged API; 54a0d13 `sedpy-jax>=0.1.1` declared;
  - 729fba6 `blackjax>=1.6.dev98`: a local deviation from upstream's `>=1.6` (lead decision), so the
    pinned Vast image passes `uv pip check` (New dependencies).
- Per-commit decisions and evidence: `LEDGER.md`.
- Parent `ceridwen-upstream-merge`: ceridwen pinned to 729fba6. fb7bc4c moves to the merged API:
  - `notebooks/ceridwen_integrated_photometry_spectra.ipynb`;
  - `scripts/per_galaxy_diagnostics.py` and `scripts/plot_prior_kl.py`;
  - 4 parent tests that pin notebook text.
- Production notebook on the merged API:

| item | before (2d5edc9) | merged |
|---|---|---|
| metallicity key | `Z` = log10 Z | `logzsol` = log10(Z/Z_sun) = [Fe/H] on this grid; grid loaded with `SSPDataAfe.load(path, zsun=0.0185, axis_meaning="feh")` (grid attr `fsps_kwargs_json`: `zsun_reference` 0.0185) |
| per-bin metallicity | `zh` | `logzsol_hist` |
| spectrum | `resolution=, smoothtype="R", res_convention="fwhm", sigma_losvd=, fit_sigma_smooth=, free_z=, baked_runtime=` | `instrument=Instrument.R_fwhm(R)`, `projector="chain"` (`"fft"` only when zred is sampled) |
| kinematics | on Spectrum | `SedModel(kinematics=Kinematics(sigma_gal="sigma_smooth", sigma_max=<prior top>), broaden_photometry=False)` |
| CSP | `sigma_losvd_kms=0.0` | `cosmo=Cosmology.planck18()` |
| filters | sedpy_jax curves | same curves via `Photometry(filter_directory=external/sedpy_jax/sedpy_jax/data/filters)` |
| lines | `from_spectrum(spec, z)` | `from_spectrum(spec, z, sigma_gas_kms=sigma_star, sigma_key="sigma_smooth")` |
| flux factor | `flux_factor_maggies(z)` | `flux_factor_cgs(z, cosmo)` |
| setting | `baked_runtime` | removed (no switch on the merged code) |

## Tests

### Ceridwen full CPU suite

CPU, float64, `-n` ≤ 3. Logs: `tmp/ceridwen-upstream-merge/integrator-tests/{upstream,merged,speedups}.log`.

| tree | failed | passed | skipped | errors | wall |
|---|---|---|---|---|---|
| upstream cc8ac9d | 8 | 755 | 70 | 23 | 33:38 |
| upstream-merge b61e998 | 8 | 914 | 70 | 23 | 20:56 |
| speedups 2d5edc9 | 7 | 284 | 6 | 10 | - |

- **Merge-only failures: none.** Every merged failure and error fails the same way on upstream cc8ac9d:
  - 23 errors in `tests/regression/test_regression.py`: no FSPS installed;
  - `test_from_fsps_records_provenance`: no FSPS;
  - 4 `test_eline_marginalisation` afe tests: `~/.ceridwen/grids/amist_c3k_lr_chab_afe.h5`
    is a pre-schema-2.0 file, which upstream refuses;
  - `test_noise_calibration` ×2 and `test_outlier_model::test_wiring_sampled_spec_only`: numerical
    tolerance; upstream gets the same values.
- Both full runs deselected the 2 `tests/likelihood/test_poly_marginal.py` NS-fit tests. Upstream's
  full run stalled more than 3.5 h at that point (`upstream-hung.log`). Run alone with
  `CERIDWEN_TEST_SSP` set:
  - merged 54a0d13: 2 passed in 35 s (`merged-polymarg-fits-gridenv.log`);
  - upstream cc8ac9d: not finished at the 30 min cap (`upstream-polymarg-fits-gridenv.log`).
- After b61e998, c661d46 adds one test and 54a0d13 changes only `pyproject.toml` and a comment.
  On 54a0d13 the chain, line, smoothing and speedups tests give 50 passed.

### Parent ceridwen tests (17 files)

Logs: `integrator-tests/parent-merged-54a0d13.log`, `parent-speedups.log`.

| tree | failed | passed | skipped | errors |
|---|---|---|---|---|
| parent + ceridwen 54a0d13 | 10 | 200 | 8 | 15 |
| baseline: parent 7354c90 + ceridwen 2d5edc9 | 7 | 203 | 8 | 15 |

The same failures occur on b61e998.

- Merged-only (3). All come from upstream behaviour on stored pre-merge results:
  - `test_calibration_arms::test_sampler_validation_passes_without_derived_outputs`:
    `load_result_h5` refuses stored `Z` ("convert with `ceridwen.fit.convert_result`").
  - `test_per_galaxy_diagnostics::RebuildCalibratedModel`, `RebuildFreeDustModel`: these rebuild
    old base-grid fits. After Z → logzsol, upstream refuses the cell logzsol (+0.25, +0.50] ×
    [α/Fe] (+0.4, +0.6] of the base grid (decision 4 below).
- `test_regenerate_fit_notebooks::test_regen_matches_the_gpu_executed_notebook` fails on both trees:
  - merged: the stored `Z` refusal;
  - baseline: reshape 186200 → (26600, 14) stored-fit mismatch.
- Fail on both trees:
  - `test_ceridwen_results_board` (15 errors) and `test_plot_ceridwen_checkpoint_evolution` ×2:
    `wiki/analyses/ceridwen-results.html` and related wiki html are missing;
  - `test_notebook_uses_production_model_and_sampler_contract`: `CERIDWEN_PLOTS` is not in the
    expected env list;
  - `test_constant_calibration_active_assembly_and_exports`: NameError `mass_mapped_beta`;
  - `test_dust_bump` notebook tests ×2: NameError `metallicity_init`.
- `wiki/tests/test_fit_settings.py`: 3 failures with the migrated notebook. The cause is the `Z` key,
  labels, AXES and the hidden `baked_runtime` in `wiki/fit_settings.py`. The wiki was not edited.

## Quick production notebook run

`CERIDWEN_NOTEBOOK_QUICK=1`, M1_210210, CPU, ceridwen 54a0d13.

- Passes in 58 s with no cell errors and no warnings. ln Z = 235056.778 ± 0.291.
- SFH-basis fast path: `joint_csp.sfh_basis_fastpath` True, `_use_sfh_basis(theta)` True.
- Wavelength support: photometry (1569, 10187); spectrum (2355, 6259).
- Parameter block: `instrument R_fwhm = 2500; projector 'chain'; stellar sigma_gal sampled as
  sigma_smooth; photometry broadened: False`.

## Equivalence verdict: ceridwen 54a0d13, notebook fb7bc4c, vs speedups 2d5edc9

- Harness and method: `tmp/ceridwen-upstream-merge/equivalence/` (`harness.py`, `VERDICT.md`). The
  merge-equivalence worker committed both on parent branch `ceridwen-upstream-merge-equivalence`.
- Run: `equivalence/runs/upstream-merge-54a0d13/`.
- Inputs: 10 targets × 21 points (max-L sample + 20 posterior draws); CPU, float64.
- Mapping: `--rename Z=logzsol --shift logzsol=1.7328282715969863`.
- fb7bc4c is the notebook in this branch's final commit.

| config | targets | verdict | max \|dlnL\| | max rel output diff |
|---|---|---|---|---|
| production | 10/10 | bitwise | 0 | 0 |
| elines_off | 10/10 | bitwise | 0 | 0 |
| zevo_off | 10/10 | bitwise | 0 | 0 |
| afe_grid | 10/10 | bitwise | 0 | 0 |
| cal_order0 | 10/10 | bitwise | 0 | 0 |
| free_z | 10/10 | differs | 17.9 | 0.88 (calibrated spectrum) |
| baked_off | 0/10 | not available: setting removed | - | - |

- `free_z` (sampled redshift; not production) differs because of upstream a7b613c:
  - the photometry is re-projected at the sampled z;
  - upstream's `SpectralProjector` is used for a sampled z (LEDGER row c540bc7: upstream rms
    1.0e-5 to 1.9e-5, local 3.5e-4 to 5.2e-4, each against a projector rebuilt at that z).
  - Per-target max |dlnL| is 4.7 to 17.9 and correlates with |dv| (0.83–0.97).
- Every saved output array of this run equals the b61e998 run (`runs/upstream-merge-b61e998/`;
  60 of 60 files).
- `baked_off`: no switch on the merged code. On 2d5edc9, `baked_off` equals `production` to
  5.8e-11 in lnL (VERDICT.md).

## Speed check

- CPU, production lnL, M1_210210, batch 128, 20 interleaved rounds × 5 calls. Ratio = 54a0d13 /
  2d5edc9 per batch:

| merged commit | reference ms | merged ms | ratio |
|---|---|---|---|
| 54a0d13 | 123.0 | 109.1 | 0.887 |
| b61e998 | 188.6 | 172.5 | 0.914 |

- GPU: not measured (step H below).

## New dependencies

- The table compares the merged `pyproject.toml` floors with the Vast image in `scripts/vast.py`
  `DEFAULT_IMAGE` (`ghcr.io/potatoist314/ceridwen-gpu@sha256:e1c8846c…`, created 2026-09-24T16:19Z).
- The image versions come from a re-resolution of `scripts/containers/requirements.txt`:
  - settings: uv 0.7.20 (the image's uv), Python 3.11, `x86_64-manylinux_2_28`,
    `--exclude-newer 2026-09-24T16:19:00Z`;
  - result: every version equals the one in the 1 Oct bootstrap log (image 6ca819ac,
    `results/quiescent-test-set-speedups-2026-10-01/run/53684057-bootstrap.log`).

| package | merged floor | image | meets floor |
|---|---|---|---|
| blackjax | >=1.6.dev98 (729fba6; upstream >=1.6; was git f73e12956) | 1.6.dev98+gf73e12956 | yes (`>=1.6` would fail: 1.6.dev98 < 1.6, PEP 440) |
| tensorflow-probability | >=0.25 (was >=0.23) | 0.25.0 (+ `tfp-nightly==0.26.0.dev20260810` files) | yes |
| sedpy-jax | >=0.1.1 (54a0d13; upstream dropped it) | 0.1.1 | yes |
| jax / jaxlib | >=0.9.0 | 0.10.2 | yes |
| numpy | >=2.0 | 2.4.6 | yes |
| scipy | >=1.13 | 1.17.1 | yes |
| h5py | >=3.16 | 3.16.0 | yes |
| astropy | >=8.0 | 8.0.1 | yes |
| anesthetic | >=2.14 | 2.16.0 | yes |
| optax | >=0.2.3 | 0.2.8 | yes |
| tqdm | >=4.65 | 4.70.1 | yes |
| pytest | >=7.0 | 9.1.1 | yes |
| fastprogress | dropped | - | - |

- `sedpy-jax`: `Spectrum(projector="chain")` imports its grid helpers (`observation/_smoothing.py`).
  `import ceridwen` and the fft projector work without it.
- `scripts/bootstrap_vast_ai.sh` with the merged code:
  - the probes pass locally on CPU: `make_static_smoother` import; `python -m ceridwen.check`
    (all ok, blackjax 1.6.dev98 included); base grid schema 2.1, shape (5, 13, 107, 10992);
  - `uv pip check` (line 67, under `set -euo pipefail`): checked with uv 0.7.20 on stand-in wheels
    (`blackjax 1.6.dev98+gf73e12956` plus a package that requires the floor). `>=1.6` gives "Found 1
    incompatibility" and the bootstrap stops; `>=1.6.dev98` gives "All installed packages are compatible".
- PyPI has blackjax 1.6, 1.6.1, 1.6.2, 1.7.0 and 1.7.1. All satisfy `>=1.6.dev98`.
- The local `ceridwen/.venv` also has blackjax 1.6.dev98.

## Step H: GPU check

- Not run. The bootstrap of the pinned image stops at `uv pip check` (blackjax, above).
- The brief records image findings only ("do not rebuild"), so the route is a lead decision.
- No Vast instance was rented; spend $0.

## Wiki pages needing updates (not edited)

- `wiki/fit_settings.py`, `wiki/tests/test_fit_settings.py`: `Z` key, labels, AXES, hidden
  `baked_runtime`.
- `wiki/notes/ceridwen-observations-model.md`: `sigma_losvd`, `fit_sigma_smooth`, `res_convention`,
  [Fe/H] offset.
- `wiki/notes/ceridwen-ssp-csp.md`, `wiki/notes/model.md`: [Fe/H] = Z + 1.7328283.
- `wiki/notes/default-fit-parameters.md`: `Z` key and offset.
- `wiki/notes/notebook-map.md`: `res_convention`.
- `wiki/notes/redshift-sigma-wiggle.md`: `free_z`.
- `wiki/research/experiments/e-birth-cloud-dust.md`, `e-gpu-price-benchmark.md`,
  `e-runtime-z-sigma-speed.md`: `baked_runtime`.
- `wiki/analyses/per-galaxy-diagnostics/M1_210210-model_parameters.txt`: `sigma_losvd` line. The
  new parameter block prints instrument, projector and sigma_gal.
- `wiki/log.md`, `wiki/index.md`: merge entry.

## Parent scripts still on the pre-merge API (not in the production path)

- `scripts/absorption_mask_analysis.py`, `scripts/benchmark_ceridwen_vast.py`,
  `scripts/benchmark_baked_runtime.py` (+ the `scripts/benchmark.py` preflight),
  `scripts/relabel_feh_notebooks.py`: old Spectrum or CSP arguments.
- `scripts/absorption_mask_report.py`, `scripts/build_dr2_quiescent_summary.py`: read stored `Z`.
- `scripts/regenerate_fit_notebooks.py` on stored pre-merge results: needs
  `ceridwen.fit.convert_result`.
- No change needed: `scripts/experiment.py`, `scripts/vast.py`, `scripts/run_ceridwen_vast_multi_gpu.py`.

## Decisions for Liu Hao

1. **Projector** (ledger-spectrum S-proj). Production keeps the local chain, bitwise equal to 2d5edc9.
   Upstream's `SpectralProjector` compared with a dense convolution:
   - accuracy: rms 8.5e-6 for upstream vs 4.2e-4 for the chain;
   - over 200 draws: dlnL +0.14 ± 0.43, sigma_smooth +1.01 km/s (+0.33 sd);
   - CPU: 3.0 ms per call vs 0.67 ms.
   Switch production to upstream's projector?
2. **Noll bump** (D-noll). The merge carries Kriek & Conroy (2013): 2175 Å, 350 Å FWHM. Upstream's
   bump uses x0 = 4.59, gamma = 0.90. With upstream's bump: top-20 dlnL median -0.019, photometry
   max rel 1.2e-2.
3. **Filter curves** (D-curves). Production keeps its curves through `filter_directory`.
   - Upstream's vendored curves: top-20 dlnL +0.001 to +0.002.
   - 77 files differ: JWST, VISTA, Gaia.
4. **Refused cell** (ledger-core decision 9). Upstream refuses logzsol (+0.25, +0.50] × [α/Fe]
   (+0.4, +0.6] on the base HR grid. The FSPS `isoc_feh_p050_afe_p6` file is byte-identical to `_p4`.
   - The nebular grid has no refused cells, so production is not refused.
   - With `logzsol_hist`, `SedModel._check_refused_alpha_cell` checks the transform at `theta_init`
     only (max +0.105 at M1). A base-grid fit with metallicity evolution is therefore not refused.
   - Options: keep, cap [α/Fe] at +0.4 for logzsol > +0.25, or rebuild the cell.
5. **Photometry broadening** (S-up-kin). Upstream's default broadens the photometry spectrum.
   Production opts out (`broaden_photometry=False`, bitwise = 2d5edc9). Turned on: dlnL -0.004 ±
   0.005, shifts < 0.003 sd.
6. **Polynomial marginal.** The local marginal calibration is kept. Upstream's
   `PolyMarginalGaussianLikelihood` gives the same lnL to 9.3e-10 but refuses lines with the polynomial.
7. **blackjax floor.** 729fba6 keeps `blackjax>=1.6.dev98` so that the current image works (lead
   decision). Return to upstream's `>=1.6` after an image rebuild from PyPI blackjax.
8. **Stored pre-merge results.** Convert them with `ceridwen.fit.convert_result` for diagnostics,
   regeneration and the calibration-arms test, or keep them read only on the old pin.
9. **`logz_0_cap`.** It keeps the old rounded offset: [Fe/H] = log10(1/50) − 2.84e-8. This gives
   unchanged numbers.
10. **Stale parent tests** (proposal). Add `mass_mapped_beta`, `mass_mapped_zh` and `metallicity_init`
    to the test envs of `test_constant_calibration_active_assembly_and_exports` and the
    `test_dust_bump` notebook tests.
