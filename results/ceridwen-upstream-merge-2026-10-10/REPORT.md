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
- Later parent commits: the pin to 729fba6; the `scripts/bootstrap_vast_ai.sh` grid probe loads with
  `zsun=0.0185, axis_meaning="feh"` (as the notebook), because the merged code refuses the nebular
  grid without them.
- 4f2fc99 and fc7994a: the parent scripts, tests and `wiki/fit_settings.py` on the merged API
  (Parent scripts below).
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

CPU, float64, `-n` ≤ 3. Logs: `tmp/ceridwen-upstream-merge/integrator-tests/{upstream,merged,merged-729fba6,speedups}.log`.

| tree | failed | passed | skipped | errors | wall |
|---|---|---|---|---|---|
| upstream cc8ac9d | 8 | 755 | 70 | 23 | 33:38 |
| upstream-merge 729fba6 | 8 | 915 | 70 | 23 | 11:27 |
| upstream-merge b61e998 | 8 | 914 | 70 | 23 | 20:56 |
| speedups 2d5edc9 | 7 | 284 | 6 | 10 | - |

- **Merge-only failures: none.** The 729fba6 failures and errors are the same 31 tests as on b61e998
  and upstream cc8ac9d (the extra pass is the test c661d46 adds). Each fails the same way on upstream:
  - 23 errors in `tests/regression/test_regression.py`: no FSPS installed;
  - `test_from_fsps_records_provenance`: no FSPS;
  - 4 `test_eline_marginalisation` afe tests: `~/.ceridwen/grids/amist_c3k_lr_chab_afe.h5`
    is a pre-schema-2.0 file, which upstream refuses;
  - `test_noise_calibration` ×2 and `test_outlier_model::test_wiring_sampled_spec_only`: numerical
    tolerance; upstream gets the same values.
- The full runs deselected the 2 `tests/likelihood/test_poly_marginal.py` NS-fit tests. Upstream's
  full run stalled more than 3.5 h at that point (`upstream-hung.log`). Run alone with
  `CERIDWEN_TEST_SSP` set:
  - merged 729fba6: 2 passed in 68 s (`merged-729fba6-polymarg-fits.log`); 54a0d13: 2 passed in 35 s;
  - upstream cc8ac9d: not finished at the 30 min cap (`upstream-polymarg-fits-gridenv.log`).

### Parent ceridwen tests (17 files)

Logs: `integrator-tests/parent-merged-fc7994a.log`, `parent-merged-54a0d13.log`, `parent-speedups.log`.

| tree | failed | passed | skipped | errors |
|---|---|---|---|---|
| parent fc7994a + ceridwen 729fba6 | 9 | 201 | 8 | 15 |
| parent + ceridwen 54a0d13 | 10 | 200 | 8 | 15 |
| baseline: parent 7354c90 + ceridwen 2d5edc9 | 7 | 203 | 8 | 15 |

The 54a0d13 failures also occur on b61e998.

- Merged-only (2), waiting on decision 4:
  - `test_per_galaxy_diagnostics::RebuildCalibratedModel`, `RebuildFreeDustModel`: these rebuild
    old base-grid fits. After Z → logzsol, upstream refuses the cell logzsol (+0.25, +0.50] ×
    [α/Fe] (+0.4, +0.6] of the base grid.
- `test_calibration_arms::test_sampler_validation_passes_without_derived_outputs` passes on fc7994a:
  it validates a copy converted by `ceridwen.fit.convert_result`.
- `test_regenerate_fit_notebooks::test_regen_matches_the_gpu_executed_notebook` fails on both trees
  with the same error: reshape 186200 → (26600, 14). The stored eline_off fit has fewer SFH bins than
  the notebook. On fc7994a the converted fit loads (cell 10) and the error comes in cell 12.
- Fail on both trees:
  - `test_ceridwen_results_board` (15 errors) and `test_plot_ceridwen_checkpoint_evolution` ×2:
    `wiki/analyses/ceridwen-results.html` and related wiki html are missing;
  - `test_notebook_uses_production_model_and_sampler_contract`: `CERIDWEN_PLOTS` is not in the
    expected env list;
  - `test_constant_calibration_active_assembly_and_exports`: NameError `mass_mapped_beta`;
  - `test_dust_bump` notebook tests ×2: NameError `metallicity_init`.
- Other affected tests on fc7994a: `tests/test_benchmark.py`, `test_vast.py`, `test_experiment.py`,
  `test_formation_times.py` and `wiki/tests/test_fit_settings.py` give 115 passed
  (`parent-extra-fc7994a.log`).

## Quick production notebook run

`CERIDWEN_NOTEBOOK_QUICK=1`, M1_210210, CPU, ceridwen 729fba6, parent 7e68407.

- Passes in 65 s with no cell errors and no warnings. ln Z = 235056.778 ± 0.201.
- The 54a0d13 run gives the same samples, ln Z, likelihood calls and χ²; its ln Z error is ± 0.291.
  The error is the spread of anesthetic `logZ(12)` (`ceridwen/sampler/nested.py:1031`), which draws
  volumes with unseeded `np.random.rand` (`anesthetic/samples.py:1220`).
- SFH-basis fast path: `joint_csp.sfh_basis_fastpath` True, `_use_sfh_basis(theta)` True.
- Wavelength support: photometry (1569, 10187); spectrum (2355, 6259).
- Parameter block: `instrument R_fwhm = 2500; projector 'chain'; stellar sigma_gal sampled as
  sigma_smooth; photometry broadened: False`.

## Equivalence verdict: ceridwen 729fba6, notebook b891d1a, vs speedups 2d5edc9

- Harness and method: `tmp/ceridwen-upstream-merge/equivalence/` (`harness.py`, `VERDICT.md`). The
  merge-equivalence worker committed both on parent branch `ceridwen-upstream-merge-equivalence`.
- Run: `equivalence/runs/upstream-merge-729fba6/`.
- Inputs: 10 targets × 21 points (max-L sample + 20 posterior draws); CPU, float64.
- Mapping: `--rename Z=logzsol --shift logzsol=1.7328282715969863`.
- The notebook is unchanged since fb7bc4c.

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
- Every saved output array of this run equals the 54a0d13 and b61e998 runs (60 of 60 files each).
- `baked_off`: no switch on the merged code. On 2d5edc9, `baked_off` equals `production` to
  5.8e-11 in lnL (VERDICT.md).

## Speed check

- CPU, production lnL, M1_210210, batch 128, 20 interleaved rounds × 5 calls. Ratio = 54a0d13 /
  2d5edc9 per batch:

| merged commit | reference ms | merged ms | ratio |
|---|---|---|---|
| 729fba6 | 203.6 | 159.8 | 0.785 |
| 54a0d13 | 123.0 | 109.1 | 0.887 |
| b61e998 | 188.6 | 172.5 | 0.914 |

- GPU: the per-fit NS wall times (step H) come from different hosts, so they are not a speed comparison.

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

- Settings:
  - RTX 5090, image `e1c8846c`, nebular grid sha256 6fe00c55…, seed 20260832;
  - production notebook defaults (`experiment.json`, `experiment-ten.json`);
  - settings and priors equal those of the 1 Oct run (`results/quiescent-test-set-speedups-2026-10-01`),
    except the removed `baked_runtime`.
- Runs (all instances destroyed; `vastai show instances` lists none):

| run | source | outcome | billed |
|---|---|---|---|
| `run/` | b891d1a | bootstrap: `uv pip check` passed with `blackjax>=1.6.dev98`; the grid probe then refused the nebular grid, fixed in 4ca0b64; instance 55330097 | $0.016 |
| `run-2/` | 4ca0b64 | M1_210210 complete on instance 55330634 (host 43746): 559 s at $0.416/h | $0.049 |
| `run-ten/` | 4ca0b64 | 10/10 complete on instance 55335713 (host 617499, on-demand, $0.604/h, 1683 s); M1 came from instance 55332978 (host 568360) before it became unavailable | $0.358 |

- Total billed: $0.423.
- Failed rentals:
  - Two stalled image loads and two bid instances that became unavailable (SSH closed by the
    remote host) were replaced by the runner.
  - Create calls on 13 bid offers failed with "vastai returned no JSON". vastai 1.5.5 writes its error
    JSON to stderr and exits 0, and `scripts/vast.py` reads stdout only, so the cause is not recorded.
  - No instance was created by a failed call (checked by label and with `vastai show instances`).
- All 11 results pass `scripts.experiment.validate_result`, with diagnostics passed.
- The two merged M1_210210 fits ran on hosts 43746 and 568360:
  - dead points are bitwise equal (16,700 samples, 5,375,929 likelihood calls);
  - log likelihoods differ by at most 3.0e-7.
- Against the 1 Oct fit, the merged dead points differ (16,900 samples). CPU lnL is bitwise equal at
  the 21 points per target (equivalence above); GPU lnL was not compared point by point.

M1_210210, 1 Oct → merged (`run-2/`):
- ln Z: 236003.520 ± 0.213 → 236003.678 ± 0.362.
- Wall: 95.6 s → 125.3 s. The hosts differ: Ryzen 7 9800X3D (1 Oct), EPYC 9135 (merged).
- Every summary median moves by at most 0.45 of the 1 Oct half-width (q84 − q16)/2, the largest being
  `logsfr_ratios[7]`. Excluding the SFH ratios, the largest is 0.35 (calibration a_0).
- [Fe/H] is −0.120 [−0.151, −0.091] → −0.121 [−0.153, −0.091]; sigma_smooth is 260.3 [257.1, 263.3]
  → 260.5 [257.4, 263.7] km/s.

Ten galaxies, 1 Oct → merged (`run-ten/`):
- Medians [q16, q84]; logzsol = [Fe/H]; the 1 Oct `Z` is shifted by −log10(0.0185).
- Max |Δq50|/hw is the largest median shift over all summary rows, in 1 Oct half-widths.
- Wall is the NS wall time.
- Hosts: 1 Oct on host 383511 (Ryzen 7 9800X3D); merged M1 on host 568360 (EPYC 7402P), the other nine
  on host 617499 (EPYC 4564P).

| galaxy | logmass | logzsol | afe | sigma_smooth | mass-weighted age [Gyr] | max \|Δq50\|/hw (row) | ln Z 1 Oct → merged | wall s 1 Oct → merged |
|---|---|---|---|---|---|---|---|---|
| M4_107370 | 11.253 [11.226, 11.274] → 11.249 [11.224, 11.277] | -0.729 [-0.785, -0.671] → -0.731 [-0.777, -0.677] | -0.156 [-0.187, -0.106] → -0.161 [-0.189, -0.121] | 172.980 [166.806, 179.805] → 173.456 [167.411, 179.467] | 4.321 [4.063, 4.645] → 4.276 [3.999, 4.598] | 0.22 (logsfr_ratios[0]) | 233403.21 ± 0.27 → 233403.25 ± 0.22 | 80 → 95 |
| M3_117010 | 10.987 [10.962, 11.014] → 10.984 [10.960, 11.014] | -0.535 [-0.583, -0.496] → -0.537 [-0.587, -0.492] | -0.054 [-0.095, -0.014] → -0.054 [-0.097, -0.015] | 162.374 [157.755, 166.647] → 162.805 [157.870, 166.944] | 4.365 [4.058, 4.688] → 4.360 [4.059, 4.685] | 0.15 (logsfr_ratios[0]) | 233562.31 ± 0.25 → 233562.18 ± 0.19 | 85 → 102 |
| M3_120308 | 11.509 [11.472, 11.544] → 11.513 [11.477, 11.543] | -0.087 [-0.131, -0.042] → -0.092 [-0.138, -0.044] | 0.005 [-0.033, 0.044] → 0.015 [-0.030, 0.053] | 226.347 [221.685, 230.724] → 225.622 [221.169, 230.447] | 4.296 [3.835, 4.811] → 4.397 [3.864, 4.765] | 0.25 (afe) | 235264.76 ± 0.24 → 235265.45 ± 0.18 | 96 → 110 |
| M2_134021 | 11.233 [11.193, 11.274] → 11.237 [11.198, 11.271] | -0.356 [-0.419, -0.294] → -0.360 [-0.416, -0.298] | 0.097 [0.064, 0.131] → 0.094 [0.057, 0.132] | 247.616 [240.695, 253.742] → 246.483 [239.638, 252.151] | 3.266 [2.697, 3.734] → 3.282 [2.798, 3.705] | 0.20 (logsfr_ratios[0]) | 238872.35 ± 0.21 → 238872.08 ± 0.29 | 88 → 106 |
| M7_146213 | 11.138 [11.089, 11.181] → 11.133 [11.091, 11.174] | -0.172 [-0.227, -0.113] → -0.160 [-0.227, -0.116] | 0.093 [0.049, 0.130] → 0.086 [0.051, 0.128] | 159.990 [154.497, 165.376] → 159.954 [155.439, 165.718] | 4.438 [3.757, 4.983] → 4.340 [3.780, 4.861] | 0.28 (logsfr_ratios[4]) | 237378.23 ± 0.13 → 237378.85 ± 0.20 | 68 → 73 |
| M8_150848 | 11.262 [11.228, 11.293] → 11.266 [11.229, 11.295] | -0.071 [-0.108, -0.036] → -0.081 [-0.110, -0.046] | 0.045 [0.024, 0.068] → 0.048 [0.028, 0.069] | 262.144 [257.816, 267.461] → 261.253 [256.910, 265.367] | 3.593 [3.144, 4.037] → 3.669 [3.150, 4.052] | 0.29 (logzsol) | 248258.46 ± 0.28 → 248258.14 ± 0.23 | 82 → 92 |
| M8_161113 | 11.477 [11.444, 11.505] → 11.463 [11.433, 11.493] | -0.306 [-0.352, -0.257] → -0.285 [-0.345, -0.231] | -0.195 [-0.198, -0.187] → -0.195 [-0.199, -0.189] | 236.937 [232.840, 240.705] → 237.294 [232.778, 241.021] | 4.262 [3.956, 4.492] → 4.121 [3.837, 4.447] | 0.53 (mass-weighted age [Gyr]) | 234085.28 ± 0.21 → 234084.92 ± 0.26 | 84 → 90 |
| M1_210210 | 11.466 [11.436, 11.495] → 11.463 [11.432, 11.498] | -0.120 [-0.151, -0.091] → -0.120 [-0.153, -0.091] | 0.132 [0.120, 0.145] → 0.132 [0.117, 0.148] | 260.296 [257.068, 263.290] → 260.532 [257.412, 263.671] | 3.531 [3.079, 3.998] → 3.568 [3.070, 4.100] | 0.45 (logsfr_ratios[7]) | 236003.52 ± 0.21 → 236003.68 ± 0.29 | 96 → 125 |
| M5_238314 | 11.573 [11.554, 11.592] → 11.574 [11.551, 11.591] | -0.463 [-0.500, -0.431] → -0.463 [-0.497, -0.435] | -0.068 [-0.095, -0.043] → -0.067 [-0.095, -0.037] | 211.733 [208.031, 215.684] → 211.893 [208.581, 215.391] | 4.221 [4.043, 4.427] → 4.169 [4.014, 4.376] | 0.38 (logsfr_ratios[1]) | 235493.35 ± 0.19 → 235492.60 ± 0.24 | 93 → 118 |
| M14_37219 | 10.966 [10.939, 10.994] → 10.966 [10.944, 10.995] | -0.248 [-0.294, -0.203] → -0.249 [-0.290, -0.205] | -0.062 [-0.102, -0.022] → -0.064 [-0.107, -0.022] | 180.195 [175.053, 185.175] → 179.920 [176.037, 184.833] | 3.486 [3.195, 3.857] → 3.498 [3.175, 3.811] | 0.26 (logsfr_ratios[4]) | 235612.32 ± 0.19 → 235611.39 ± 0.25 | 83 → 102 |

- Largest median shift per galaxy: 0.15–0.53 half-widths.
- |Δ ln Z|: 0.04–0.93. The 1 Oct and merged NS error estimates are 0.13–0.36.
- Per-fit wall time: 1.07–1.31× the 1 Oct time on different hosts. This is not a same-boot A/B.

## Wiki pages needing updates

- Code, updated in 4f2fc99: `wiki/fit_settings.py` (`logzsol` key, [Fe/H] label, AXES, hidden
  `baked_runtime` for pre-merge runs) and `wiki/tests/test_fit_settings.py` (13 passed).
- Prose, not edited:
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

## Parent scripts

Ported in 4f2fc99 and fc7994a. Stored pre-merge fits stay unchanged: readers that find `Z` in a stored
fit load a temporary copy converted by `ceridwen.fit.convert_result` on the base HR grid.

| script | change | check |
|---|---|---|
| `benchmark_ceridwen_vast.py` (`build_joint_workload`) | merged Spectrum, Kinematics, Cosmology, `filter_directory`, `logzsol` | lnL at theta_init -166785.99487293736 on both trees (refusal off, decision 4) |
| `absorption_mask_analysis.py` | same builder port; `load_stored_result`; Fisher truth `Z` → `logzsol` | predictions bitwise equal; Fisher matrix equal to 7.4e-12 relative; posterior and truth readers equal to 3e-17 |
| `benchmark_baked_runtime.py` + `benchmark.py` preflight | no `baked_runtime` switch: arms fixed / free sigma_smooth; speedup fields removed | runs with emission lines off (proposal 1); `tests/test_benchmark.py` passes |
| `absorption_mask_report.py` | reads cells through `load_stored_result`; `logzsol` row is [Fe/H] | 45 stored cells: equal to the stored `summary.json`, [Fe/H] to 2.84e-8 (`FEH_OFFSET` rounding) |
| `build_dr2_quiescent_summary.py` | `logzsol` → `feh`; stored `Z` + `FEH_OFFSET` | 187 stored fits: CSV byte-identical; merged M1 `feh_q50` = stored `logzsol` q50 |
| `regenerate_fit_notebooks.py` | notebook loads a converted copy when the stored fit has `Z` | converted fit loads (cell 10); the regen test then stops on the stored-fit bin mismatch (above) |
| `relabel_feh_notebooks.py` | none: imports no ceridwen code | runs unchanged; listed here before by mistake |

- Changed before: `scripts/bootstrap_vast_ai.sh` grid probe (above).
- No change needed: `scripts/experiment.py`, `scripts/vast.py`, `scripts/run_ceridwen_vast_multi_gpu.py`.
- Decision 4 also refuses the `benchmark_ceridwen_vast` fixed workload and
  `absorption_mask_analysis.build_notebook_model` on the base grid.
- Proposals (outside the phase-2 list, not done):
  1. `benchmark_ceridwen_vast._make_log_functions` evaluates each likelihood component alone. The
     production notebook shares emission lines with photometry (since 99e3091), and both 2d5edc9 and the
     merged code refuse that call, so `benchmark_baked_runtime.py` fails on the production notebook
     before and after the merge. Fix: evaluate through `likelihood.loglike(data, predictions, theta)`.
  2. `per_galaxy_diagnostics.rebuild_model` and its filter-curve panel do not pass `filter_directory`,
     so they use upstream's curves (77 files differ, VISTA among them).

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
   - Waiting on this decision: `test_per_galaxy_diagnostics` RebuildCalibratedModel and
     RebuildFreeDustModel, the `benchmark_ceridwen_vast` fixed workload and
     `absorption_mask_analysis.build_notebook_model` (all base grid).
5. **Photometry broadening** (S-up-kin). Upstream's default broadens the photometry spectrum.
   Production opts out (`broaden_photometry=False`, bitwise = 2d5edc9). Turned on: dlnL -0.004 ±
   0.005, shifts < 0.003 sd.
6. **Polynomial marginal.** The local marginal calibration is kept. Upstream's
   `PolyMarginalGaussianLikelihood` gives the same lnL to 9.3e-10 but refuses lines with the polynomial.
7. **blackjax floor.** 729fba6 keeps `blackjax>=1.6.dev98` so that the current image works (lead
   decision). Return to upstream's `>=1.6` after an image rebuild from PyPI blackjax.
8. **Stored pre-merge results.** Resolved (lead): files under `results/` and `archive/` stay as they are;
   the parent readers convert a temporary copy at load time with `ceridwen.fit.convert_result`.
9. **`logz_0_cap`.** It keeps the old rounded offset: [Fe/H] = log10(1/50) − 2.84e-8. This gives
   unchanged numbers.
10. **Stale parent tests** (proposal). Add `mass_mapped_beta`, `mass_mapped_zh` and `metallicity_init`
    to the test envs of `test_constant_calibration_active_assembly_and_exports` and the
    `test_dust_bump` notebook tests.
