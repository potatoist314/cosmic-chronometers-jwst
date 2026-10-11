# Merge equivalence verdict

Question: does the merged ceridwen give the same likelihood and model outputs as the
local code it replaces, ceridwen `speedups` 2d5edc9?

Committed copy: parent branch `ceridwen-upstream-merge-equivalence` (origin),
`results/ceridwen-upstream-merge-2026-10-10/equivalence/` (harness.py, VERDICT.md). Run outputs
stay in the coordination directory `tmp/ceridwen-upstream-merge/equivalence/runs/`.

## Method

- Harness: `harness.py` (this directory). The model is built by executing the production
  notebook's own cells (settings, data, observations, model, likelihood assignments); the
  harness only edits `SETTINGS`/`PRIORS` per configuration.
- Reference notebook: parent a6fba80 `notebooks/ceridwen_integrated_photometry_spectra.ipynb`,
  the notebook the ten-galaxy run executed with ceridwen 2d5edc9
  (`results/quiescent-test-set-speedups-2026-10-01/run/manifest.json`). Its model cells equal
  those of parent `speedups` 7f704cc. Data and the notebook's helper scripts come from the main
  checkout (`data/raw`, `scripts/`).
- Targets: the ten galaxies in `results/quiescent-test-set-speedups-2026-10-01/run/fits/fit/`.
- Points (`points.h5`, seed 20261010): per target, row 0 = the max-likelihood sample of its
  `ceridwen_result.h5`; rows 1-20 = `default_rng(20261010).choice(n, 20, p=softmax(log_weights))`.
  `free_z` adds `zred = z_cat + dv (1 + z_cat)/c`, dv = 0 for row 0 and U(-200, 200) km/s from the
  same generator for rows 1-20.
- Configurations: `production` (notebook defaults); one switch each: `elines_off`
  (emission-line marginalisation off, redshift fixed), `zevo_off` (metallicity evolution off),
  `afe_grid` (`~/.ceridwen/grids/amist_c3k_hr_krou_afe.h5`, no nebular), `free_z` (line
  marginalisation off, redshift sampled), `baked_off` (`baked_runtime=False`), `cal_order0`
  (calibration order 0, a_0 only).
- Outputs per point, CPU, float64, `jit(vmap(...))` over the 21 points:
  lnL = `run_sampler`'s own `loglike_fn`; uncalibrated model spectrum and photometry
  (`model.predict`); the calibration polynomial P(x), its coefficients, the line fluxes and the
  calibrated model, from the same `calibrate_with_lines` / `calibrate` call the likelihood makes;
  photometry plus line fluxes.
- Relative output difference: per point max|a - b| / max|a| over the output array, then the
  maximum over the 21 points.
- Rounding floor: each run also evaluates every point one at a time (a second XLA
  compilation of the same code). Floor = max |batched - single| for lnL, and the same relative
  measure for each output. Verdict per configuration and target: `bitwise` (every difference 0,
  same observations and line list), `rounding` (every difference at most 10 x the larger floor of
  the two runs; minimum floors 1e-8 for lnL and 1e-12 relative), `differs` (anything else).

## Reference: ceridwen speedups 2d5edc9 (2026-10-10 22:59)

- Run: `runs/reference-2d5edc9/` (exact command lines in `commands.txt`), 70/70 jobs built.
- Harness fidelity: the observations equal the stored ones in each `ceridwen_result.h5` (photometry
  uncertainty to 1 ulp, from `np.hypot` on macOS versus the Linux GPU host). CPU lnL versus the lnL the
  GPU run stored for the same rows: max |d| 0.013-0.099 per target (relative 4e-7).
- Rounding floor of the reference code (max over the ten targets):

| config | lnL | spectrum | photometry | calibrated spectrum | P(x) | coefficients | line fluxes | photometry + lines |
|---|---|---|---|---|---|---|---|---|
| production | 2.2e-04 | 7.2e-09 | 1.7e-06 | 1.2e-07 | 1.2e-07 | 3.2e-08 | 3.0e-05 | 1.7e-06 |
| elines_off | 2.2e-04 | 7.2e-09 | 1.7e-06 | 2.8e-08 | 2.8e-08 | 2.3e-09 | - | 1.7e-06 |
| zevo_off | 2.5e-04 | 1.4e-08 | 2.0e-06 | 1.4e-07 | 9.7e-08 | 4.8e-08 | 2.8e-05 | 2.0e-06 |
| afe_grid | 1.7e-04 | 5.3e-09 | 1.9e-06 | 1.4e-07 | 1.4e-07 | 3.7e-08 | 9.6e-06 | 1.9e-06 |
| free_z | 1.9e-04 | 7.4e-09 | 1.7e-06 | 6.0e-08 | 6.4e-08 | 2.1e-09 | - | 1.7e-06 |
| baked_off | 2.2e-04 | 7.2e-09 | 1.7e-06 | 1.2e-07 | 1.2e-07 | 3.2e-08 | 3.0e-05 | 1.7e-06 |
| cal_order0 | 2.2e-04 | 7.2e-09 | 1.7e-06 | 5.9e-07 | 4.1e-10 | 1.1e-07 | 2.0e-06 | 1.7e-06 |

- The lnL floor (about 2e-4, the same with the lines off) is consistent with the model photometry,
  which changes by about 2e-6 relative between the two compilations; with the 5% photometric error
  floor that moves each band's chi by about 4e-5. The PLAN criterion |dlnL| <= 1e-8 is therefore below this likelihood's own rounding;
  only a bitwise result meets it.
- CPU timing noise: the reference against itself (`harness.py timing`, production, M1_210210,
  batch 128, 12 interleaved rounds x 5 calls) gives ratio 0.971 (median 0.231 s and 0.224 s per
  batch; quartiles 0.21-0.26 s, other workers loading the Mac). `runs/reference-2d5edc9/timing-self.json`.

## upstream-main-cc8ac9d: ceridwen upstream/main cc8ac9d (2026-10-10 23:22)

- No configuration exists there: the notebook stops at its imports (`EmissionLineColumns`,
  `emission_lines.read_fsps_line_list`, the marginalising `PolynomialCalibration`,
  `mass_mapped_beta`/`mass_mapped_zh` are absent). Every configuration also needs `Spectrum`
  arguments upstream removed in v3.0.0 (`resolution`, `smoothtype`, `res_convention`,
  `sigma_losvd`, `fit_sigma_smooth`, `free_z`, `baked_runtime`) and `CSPBasis_afe(sigma_losvd_kms=)`.
  `cal_order0` and `elines_off` still need the local calibration class; `zevo_off` the local lines
  and calibration. Run: `runs/upstream-main-cc8ac9d/` (70 jobs, all `unavailable`, reason per job).

## upstream-merge-c307b54: merge commit c307b54 (2026-10-10 23:22)

- No configuration builds: `TypeError: Spectrum(): 'resolution' is not an argument; use
  instrument=Instrument.<unit>(...)` (the merge took upstream's `observation/spectrum.py`; the local
  pieces are follow-up ports). Run: `runs/upstream-merge-c307b54/`.

## interim-4b1f1a6: upstream-merge 4b1f1a6 with a draft notebook migration (2026-10-11 03:11)

- Not the final commit: the official notebook migration had not landed. The notebook is the reference
  notebook migrated to the merged API by `runs/interim-4b1f1a6-draft-notebook/draft_migrate.py`
  (`draft-merged.ipynb`, sha256 22bf123d...): logzsol keys and priors (`--rename Z=logzsol --shift
  logzsol=1.7328282715969863`), `SSPDataAfe.load(zsun=0.0185, axis_meaning="feh")`, `cosmo=`,
  `Spectrum(instrument=Instrument.R_fwhm(R), projector="chain")`, `SedModel(kinematics=Kinematics(sigma_gal=
  "sigma_smooth", sigma_max=<sigma_smooth prior top>), broaden_photometry=False)`, `filter_directory`,
  `EmissionLineColumns.from_spectrum(sigma_gas_kms=, sigma_key=)`.
- Run: `runs/interim-4b1f1a6-draft-notebook/` (`verdict-section.md`, `compare.json`, `timing.json`, commands).
- CPU timing, production lnL, M1_210210, batch 128, 20 interleaved rounds x 5 calls: reference 161.2 ms,
  candidate 159.3 ms per batch; ratio candidate/reference 0.988 (reference against itself: 0.971).

| config | targets | verdict | max abs dlnL | max rel output diff | cause |
|---|---|---|---|---|---|
| production | 10/10 | 10 bitwise | 0 | 0 | - |
| elines_off | 10/10 | 10 bitwise | 0 | 0 | - |
| zevo_off | 10/10 | 10 bitwise | 0 | 0 | - |
| afe_grid | 10/10 | 10 bitwise | 0 | 0 | - |
| cal_order0 | 10/10 | 10 bitwise | 0 | 0 | - |
| baked_off | - | no switch | 5.8e-11 (via production) | 1.1e-12 (via production) | merged chain is always baked |
| free_z | 10/10 (fft projector) | 10 differs | 4.7-17.9 | spectrum 1.9e-3-1.7e-2, photometry 6.7e-4-9.6e-4 | upstream a7b613c (projector and photometry) |

- `baked_off`: the merged chain projector (local port b0f7130) carries the baked lookups of local 6707c05/5f2c316
  with no switch (ledger S-6707c05); the notebook cell raises `NotImplementedError`. In the reference,
  `baked_off` equals `production` to |dlnL| <= 5.8e-11 and relative outputs <= 1.1e-12 (all ten targets), and
  merged `production` equals reference `production` bitwise.
- `free_z`: `projector="chain"` refuses a sampled redshift (b0f7130; ledger S-c540bc7 adopt-upstream), so
  this row uses `projector="fft", zred_range=(z_cat - 0.1, z_cat + 0.1)` when zred is sampled
  (`runs/interim-4b1f1a6-fftz/`, `draft-merged-fftz.ipynb`). Two differences, both from upstream a7b613c
  ("v3.0.0: ... sampled redshift for every observation type"):
  - Photometry, 6.7e-4-9.6e-4: a7b613c `SedModel` sets `obs.free_z = zred_is_free` on Photometry
    (`ceridwen/model/model.py:515`), so `CSPBasis.predict` projects the bands at each sampled z
    (`Photometry.predict_at_redshift`); 2d5edc9 never sets `free_z` on Photometry, so the bands stay
    projected at the catalogue z and only the flux factor follows the sampled z. At M1_210210,
    dv = +192 km/s: reference/production - 1 = -0.0033 in all 28 bands, merged -0.0021 ... -0.0179 per band.
    Toggle (`toggle_photz.py`, `toggle-photometry-free_z.json`): merged with `free_z = False` on
    Photometry gives the reference photometry bitwise (M1_210210, M5_238314).
  - Spectrum, 1.9e-3-1.7e-2, and most of |dlnL| (M1 15.4 of 15.9, M5 17.7 of 17.9 with the photometry
    toggled): upstream `broadening.SpectralProjector` (a7b613c) instead of the local chain and the local
    free-z stretch (c540bc7). Toggle at fixed z (`runs/interim-4b1f1a6-fft-fixedz/`, `elines_off`,
    `projector="fft"`): spectrum 6.1e-4 (M1_210210) and 1.0e-3 (M5_238314), |dlnL| 3.4 and 6.0,
    photometry bitwise; the same config with `projector="chain"` is bitwise. Ledger rows S-proj and S-c540bc7
    compare both projectors with a dense convolution.

## Pending (2026-10-11 03:50)

- Final merged commit not yet verified: the official notebook migration is not yet committed on parent
  `ceridwen-upstream-merge`. When it lands, run on the final `upstream-merge` tip:
  `harness.py verify --ceridwen <worktree at tip> --label upstream-merge-<sha>
  --notebook ceridwen-upstream-merge:notebooks/ceridwen_integrated_photometry_spectra.ipynb
  --rename Z=logzsol --shift logzsol=1.7328282715969863`.
