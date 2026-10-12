# Ceridwen upstream merge ledger (2026-10-10)

ceridwen `upstream-merge` = upstream/main cc8ac9d merged into local `speedups` 2d5edc9 (merge
c307b54), plus the commits below. Decisions: **port** = local change re-applied on upstream code;
**carry** = local file or feature kept; **adopt** = upstream's version replaces the local one;
**drop** = duplicate; **upstream-only** = upstream change with no local counterpart.

Commits on `upstream-merge` after the merge:

| commit | content |
|---|---|
| c032d0b | SFH-basis fast path, per-bin `logzsol_hist`, host flux cube, `compare_all` on `CSPBasis_afe` |
| 17d486c | fixed-distance flux-factor hoist on `SedModel` / `CSPBasis._flux_factor` |
| 5cfb739 | wavelength support (`CSPBasis_afe.predict` override) |
| 852b239 | `grid_fetch` comment in logzsol terms |
| ba57bbf | merge of upstream-merge-fix-core: 192eb07 Noll bump (KC13), d16f1ce NumPy FilterSet, be1b6e6 `filter_directory` + MegaCam U.MP9302, 46e8d8d `SSPData.load(axis_meaning=)`, 1069f0c |
| 4b1f1a6 | merge of upstream-merge-fix-spectrum: b0f7130 `Spectrum(projector="chain")`, `select_absorption_features`, `EmissionLineColumns.from_spectrum(sigma_gas_kms=, sigma_key=, zred_key=)` |
| b61e998 | local spectrum tests on the merged API |
| c661d46 | merge of upstream-merge-fix-spectrum 192fd25: line widths follow the Spectrum projector (test) |
| 54a0d13 | `sedpy-jax>=0.1.1` declared (`projector="chain"` imports it in `observation/_smoothing.py`) |
| 729fba6 | `blackjax>=1.6.dev98` (local deviation from upstream's `>=1.6`; lead decision 2026-10-11) |
| d7c0536 | Liu Hao's notes of 2026-10-11, comments only (`scripts_afe/build_afe_hr_grid.py`, `ssps/ssp_data_afe.py`); also branch `liuhao-notes-2026-10-11` 35a46d8 on 37f04b0 |

Equivalence evidence below: production inputs of M1_210210 (max-likelihood sample + 200 or 20
posterior draws) on CPU, float64, unless stated.

## Local commits (speedups, 42)

| commit | change | decision | evidence | on upstream-merge |
|---|---|---|---|---|
| fe65b14 | `StellarIndices` observation | carry | not used by production; inner projector = chain; `tests/test_stellar_indices.py` passes | c307b54, 4b1f1a6 |
| 611a855 268291c afe37fe 37f04b0 | SFH-basis fast path | port | production SED and photometry bitwise = speedups at 200 points; 0.36 s vs 16.2 s (general path), 200 points jit+vmap | c032d0b |
| a38982a | static smoothing in one Gaussian | carry (inside chain) | fixed sigma only; `tests/test_static_smoothing.py` passes | 4b1f1a6 |
| 341a76b | fixed-z flux-factor hoist | port | photometry bitwise = speedups at 200 points; injected constant 3.24327742e-24 | 17d486c |
| d89553f | `searchsorted(method="compare_all")` | port | same indices | c032d0b |
| 5826e8f | FilterSet cache, one logZ read per iteration | drop | upstream `_FILTERSET_CACHE` and one logZ read | c307b54 (upstream's) |
| fdcd75d | float64 flux cube on host | port | memory only; `SSPDataAfe._flux_on_host` | c032d0b |
| f9ff605 | absorption-feature pixel selection | carry | `air2vac` from `observation/filters.py`, same code as sedpy_jax | c307b54, 4b1f1a6 |
| 859eca1 | spectrum checkpoint frames | carry | moved to `ceridwen/checkpoint_plotting.py`; `tests/test_checkpoint_spectrum.py` passes | c307b54 |
| 0e8ef3e | marginal calibration polynomial | carry | upstream `poly_marginal_loglike`: same lnL to 9.3e-10 (10 points), but refuses lines with the polynomial | c307b54 |
| b70e743 | no-smoothing weighted gathers | carry (inside chain) | not production; `tests/test_observation_speedups.py` passes | 4b1f1a6 |
| 36cf922 | batched calibration reductions; logical call count | carry | toy NS: 41,218 logical calls reported (upstream estimate 8,352) | c307b54 |
| f711662 c862cae | grid documentation | adopt (`ssp_data_afe.py`); carry `grid_fetch` comment | docs only | 852b239, 1069f0c |
| 30cc016 | order-10 marginal = closed form (test) | carry | test passes | c307b54 |
| 56505a6 | Gram matrix from Chebyshev moments | carry | 0.158 ms/call vs 0.503 ms (upstream kernel), same lnL | c307b54 |
| c540bc7 | free redshift for Spectrum | adopt | upstream projector rms 1.0e-5 to 1.9e-5 vs local 3.5e-4 to 5.2e-4 against a projector rebuilt at each z; chain refuses sampled z | c307b54 (upstream's) |
| b419fd1 | NS progress JSON lines | carry | toy NS bitwise = speedups | c307b54 |
| 6707c05 5f2c316 | baked runtime (sigma_smooth, zred) | carry for sigma_smooth (inside chain); zred part goes with c540bc7 | production projection bitwise; `tests/test_baked_runtime.py` | 4b1f1a6 |
| 6fc7539 | emission lines as free-flux columns | carry | upstream `marginalize_elines` cannot combine with the marginal polynomial | c307b54, 4b1f1a6 |
| 7f18311 | flat prior f >= 0 | carry | upstream flat-on-R prior moves production posteriors up to 0.87 sd (afe) | c307b54 |
| 0f0895f | tied doublets, lines shared with photometry | carry | untied: shifts up to 0.21 sd (sigma_smooth) | c307b54 |
| 1fae781 | exclude FSPS [O II] 3867 | carry | zero Cloudy flux; no NIST ASD line 3860-3875 A | c307b54 |
| ee68b5f | mass-mapped metallicity | port | per-bin `logzsol_hist` SED bitwise = speedups | c307b54, c032d0b |
| f973c10 16c7a90 8161d3d a935a99 e8b7643 ea91453 | NSS stepping-out carry, lane kernel | carry | toy NS (60 live, 756 dead): dead points, logL, births bitwise = speedups; logZ -9.864932730743856 | c307b54 |
| 0a3bd51 | LOSVD FFT pad for the sigma_smooth prior top | carry (chain reads `Kinematics.sigma_max`) | notebook sets `sigma_max` = prior top; projection bitwise | 4b1f1a6 |
| 7c4db5e | sparse filter-grid interpolation | adopt | upstream `setup_for_model` `_T` bitwise | c307b54 (upstream's) |
| f44eb32 decead1 e47f619 2d5edc9 | line-column windows, tie gather, triangular solve | carry | bitwise per their tests | c307b54 |
| a60f1f8 | step kernel compiled during init | carry | toy NS bitwise | c307b54 |
| 578b310 | wavelength support | port | photometry on slice 1569:10187 of 10,992 pixels, bitwise = speedups; chain sets `model_support` | 5cfb739, 4b1f1a6 |

sedpy_jax commits used by production (upstream vendored sedpy_jax's filters and dust laws):

| commit | change | decision | evidence | on upstream-merge |
|---|---|---|---|---|
| 9d8aa19 | Noll bump at Kriek & Conroy (2013) 2175 A, 350 A FWHM | carry | production SED bitwise = speedups; upstream bump (x0 4.59, gamma 0.90): top-20 dlnL median -0.019 | 192eb07 |
| 754a118 | FilterSet grids in NumPy | port | 92 s -> 3.7 s (28 filters); band predictions bitwise | d16f1ce |
| 482429b | CFHT MegaCam U.MP9302 curve | carry | parent "u" band | be1b6e6 |

## Upstream changes touching likelihood, defaults or API

| commit | change | production effect | decision |
|---|---|---|---|
| a6f2625 | metallicity key `logzsol` = log10(Z/Z_sun); `Z`/`zh` refused | notebook keys renamed; grid loads with `zsun=0.0185, axis_meaning="feh"`; stored pre-merge results refused by `load_result_h5` until `convert_result` | adopt |
| 7940959 (B1-022) | [alpha/Fe] folded into SSP weights (`_contract`) | fallback path only (production uses the fast path) | adopt |
| a7b613c | Kinematics on SedModel; `sigma_losvd_kms` removed; photometry broadened by default | notebook passes `Kinematics(...)` and `broaden_photometry=False` (bitwise = speedups) | adopt; production opts out |
| a7b613c | `broadening.SpectralProjector` | production keeps the local chain (`projector="chain"`); fft used for sampled z | carry local chain; Liu Hao 2026-10-11: "no i think you can keep the local convolve." |
| b69412c 051808d | vendored filters and dust laws | Noll bump differs from production; curves: 8 of 28 production bands change by ≤ 2.2e-4 relative, \|dlnL\| ≤ 6.3e-3 (ten galaxies, 210 points) | adopt with 9d8aa19 bump; curves adopted (Liu Hao 2026-10-11: "bring in extra or changed filter curves."): production reads ceridwen's library, no `filter_directory` |
| grid metadata | CHASH table, zsun provenance, refused cell logzsol (+0.25, +0.50] x afe (+0.4, +0.6] | base HR grid refuses priors that reach the cell; nebular grid has no refused cells | upstream-only; kept (Liu Hao 2026-10-11: "keep refuse as upstream does."); parent base-grid builders cap logzsol at +0.25 |
| cosmo | `cosmo=` required | age, D_L, flux factor at M1 z bitwise | adopt |
| 7bbe66e | `PolyMarginalGaussianLikelihood`, `Spectrum(polynomial_mode=)` | none (production uses the local class) | upstream-only |
| 3396d97 | profiled polynomial `Spectrum(polynomial_order=)` | none (default off) | upstream-only |
| be85228 dc2e894 | `Spectrum(marginalize_elines=True)` | none | upstream-only |
| 5cf8f6e (B2-016) | NS weights from `ns_weights.nested_log_weights` | final live points only: weight change <= 8.7e-5, posterior means <= 1.7e-5 (10 stored fits) | upstream-only |
| 1155a76 (B2-002) | prior draws `(n, *shape)` | production prior draws bitwise | upstream-only |
| 882f9fa 9be95cd | resumable NS | none unless `resume_from` | upstream-only |
| 0e37d72 9fea53a 27948ff 0e39c9b 3c7e5c6 aac7b3a f15afdc e406d24 | zred-tracked SFH mass, linear SFH top, frac_obrun, nebular cloudy_dust, young MIST surviving mass | none: production uses fixed z, step SFH, no nebular model, no surviving mass | upstream-only |
| eb5bc6f bac259a 680037b bf3de0a | IGM order, IGM on lines, dust emission energy balance | none: no IGM, no dust emission | upstream-only |
| b730693 | NUTS | not used | upstream-only |
| pyproject | dependency floors: blackjax>=1.6, jax>=0.9, numpy>=2, astropy>=8, h5py>=3.16, tfp>=0.25, anesthetic>=2.14; sedpy-jax dropped | Vast image blackjax 1.6.dev98+gf73e12956 fails `uv pip check` against `>=1.6` (PEP 440: 1.6.dev98 < 1.6) | adopt floors except blackjax; **local deviation** 729fba6: `blackjax>=1.6.dev98` (upstream's comment: 1.6's `blackjax/ns/` is byte-identical to commit f73e12956, the image's build; PyPI 1.6+ still satisfies it); sedpy-jax re-declared (54a0d13) |

## Phase 3 (2026-10-11): decisions 1, 3, 4

- Parent pin d7c0536. Filter curves: production likelihood change, REPORT.md "Filter curves".
- Equivalence harness, production, ten galaxies × 21 points, CPU, against the 729fba6 run: spectrum
  bitwise; photometry ≤ 2.2e-4 relative (vista_vircam_Y; 8 of 28 bands change); dlnL median -1.1e-3,
  range -6.3e-3 to +4.3e-3 (floor ≤ 2.2e-4).
- Base-grid builders with logzsol ≤ +0.25: build with the refusal on; lnL and predictions bitwise equal
  to the phase-2 builds made with the refusal off.

| parent tests (17 files) | failed | passed | skipped | errors |
|---|---|---|---|---|
| phase 3 + ceridwen d7c0536 | 7 | 203 | 8 | 15 |
| fc7994a + ceridwen 729fba6 | 9 | 201 | 8 | 15 |
| baseline: parent 7354c90 + ceridwen 2d5edc9 | 7 | 203 | 8 | 15 |

Phase 3 fails only tests that also fail on the baseline. The other affected parent tests give 115 passed.
