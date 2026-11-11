# LEGA-C DR3 against DR2

Liu Hao, 2026-11-11 11:14: "yeah do all 3"

Phases from the overseer-astronomy brief (card t_5440a254).

## Download and cross-match

- `scripts/download_legac_dr3.py`: ESO Phase 3 collection LEGA-C, release description 185 (van der Wel et al. 2021, ApJS 256, 44). `legac_DR3.fits` (4081 rows) and 4081 1D spectra, 626.6 MB, in `data/raw/legac_dr3/` (spectra gitignored). Notes: `data/raw/legac_dr3/README.md`.
- COSMOS matches for DR3 spectra (`--release dr3` of `scripts/download_cosmos2015_legac_dr2_photometry.py` and `scripts/download_cosmos2020_cosmos2025_legac_dr2_photometry.py`, through the VizieR mirror `vizier.idia.ac.za`; CDS VizieR returned 404 on 2026-11-11): COSMOS2015 4057, COSMOS2020 Classic 3961, Farmer 3397, COSMOS2025 1677 matched spectra.
- DR2 135 (chronometer sample): 135 of 135 in DR3 with the same `SPECT_ID` and `OBJECT`, separation 0.0″. Max |Δz| 0.0029 (c|Δz|/(1+z) ≤ 487 km/s), median 35 km/s.
- Test set (`results/quiescent-test-set/targets.json`): 10 of 10, same `SPECT_ID` and `OBJECT`, separation 0.0″, max |Δz| 0.00053 (≤ 93 km/s).
- Per galaxy: `crossmatch.csv`.

## Notebook and runner

- `notebooks/ceridwen_integrated_photometry_spectra.ipynb`: `SETTINGS["data_source"] = "legac_dr3"` reads the DR3 catalogue row and spectrum by `SPECT_ID`, with no DR2 selection. Default `legac_dr2` unchanged.
- Default-off check: M1_210210, notebook cells 0–8 at HEAD and in the working tree; 19 observation and prediction arrays (eager and JIT, 3 parameter points) bitwise equal (`default-off-check.py`, `default-off-check.log`).
- `scripts/experiment.py` builds DR3 target metadata (`OBJECT`, `SN`, `Filename`, catalogue row) from `legac_DR3.fits`; `scripts/vast.py` `selected_inputs` uploads the DR3 catalogue and spectrum for DR3 cells (`tests/test_experiment.py`).
- Photometry in these fits: the same COSMOS2025 rows as DR2 (keyed by `SPECT_ID`; DR2 match files).

## Spectra, 10 test galaxies

- Good pixel: `QUAL` 0, `ERR` > 0, finite flux, outside 7590–7660 Å (air). Ratios over pixels good in both releases.
- Flux ratio shape: order-5 Legendre fit to DR3/DR2 flux; peak-to-peak over its median.
- χ: (DR3 − shape × DR2) / combined error. DR2 telluric ranges: 6865–6960, 7160–7330, 7580–7710, 8070–8400, 8900–9200 Å (Straatman et al. 2018, Sect. 2 step 5).
- Error ratio / flux ratio: median of (ERR3/ERR2)/(FLUX3/FLUX2). S/N ratio: median of (S/N)3/(S/N)2.
- `FLAG_SPEC` 0 and `FLAG_MORPH` 0 for all 10. Header `WAVELMIN`/`WAVELMAX` differ; pixel grids are identical.

| galaxy | grid | good px DR2 / DR3 | flux ratio median | ratio shape peak-to-peak | χ std (in / out of DR2 telluric ranges) | error ratio / flux ratio | S/N ratio | σ★ DR2 → DR3 [km/s] | σ★ error DR2 → DR3 [km/s] |
|---|---|---|---|---|---|---|---|---|---|
| M1_210210 | same | 4053 / 4053 | 0.860 | 12% | 1.05 (1.15 / 0.99) | 1.05 | 0.95 | 259.5 → 256.9 | 6.5 → 4.9 |
| M8_150848 | same | 4099 / 4119 | 0.941 | 18% | 0.70 (0.83 / 0.58) | 1.06 | 0.94 | 270.5 → 256.1 | 9.2 → 4.7 |
| M5_238314 | same | 4061 / 4052 | 1.086 | 15% | 0.85 (0.95 / 0.81) | 1.03 | 0.97 | 201.5 → 205.8 | 7.1 → 5.8 |
| M3_120308 | same | 4064 / 4045 | 0.871 | 32% | 0.66 (0.83 / 0.45) | 1.00 | 1.00 | 222.7 → 225.0 | 9.0 → 7.5 |
| M2_134021 | same | 4097 / 3915 | 0.828 | 21% | 1.05 (1.04 / 1.06) | 0.63 | 1.58 | 239.4 → 254.2 | 11.2 → 9.6 |
| M7_146213 | same | 4074 / 4056 | 1.021 | 13% | 0.62 (0.79 / 0.51) | 1.01 | 0.99 | 165.7 → 171.3 | 9.3 → 7.2 |
| M3_117010 | same | 3989 / 3985 | 0.881 | 14% | 0.44 (0.48 / 0.42) | 1.02 | 0.98 | 163.4 → 162.1 | 8.2 → 6.9 |
| M4_107370 | same | 4056 / 4076 | 0.864 | 26% | 0.79 (0.87 / 0.68) | 1.12 | 0.90 | 181.8 → 168.8 | 11.2 → 8.4 |
| M14_37219 | same | 4041 / 4056 | 0.889 | 21% | 0.57 (0.55 / 0.58) | 0.97 | 1.03 | 182.1 → 185.0 | 9.0 → 7.2 |
| M8_161113 | same | 4042 / 4044 | 1.123 | 8% | 0.57 (0.70 / 0.51) | 1.11 | 0.90 | 212.6 → 218.8 | 10.0 → 7.8 |

## DR2 calibration choices checked against DR3

Choices from `wiki/notes/model.md` (Sample and data; Calibration, noise and sampler). W21: van der Wel et al. 2021. S18: Straatman et al. 2018.

| choice | DR2 | DR3 | test set |
|---|---|---|---|
| Pixel validity: `QUAL` 0, `ERR` > 0, finite | `QUAL` nonzero bad | same columns; `QUAL` 1 with `ERR` 0 | good pixels 3915–4119 (DR2 3989–4099); M2_134021 loses 197 |
| Units: air to vacuum; 10⁻¹⁹ erg s⁻¹ cm⁻² Å⁻¹ | `TUNIT2` 10⁻¹⁹ erg cm⁻² s⁻¹ Å⁻¹; `TUCD1` `em.wl;obs.atmos` | same units and UCD | same conversion |
| Resolution: `SPEC_RES` | 2500 | 2500 | same |
| Extraction | Gaussian, then Moffat refit (W21 Sect. 2.2.1) | HST Sérsic profile convolved with a fitted Moffat, through a 1″ slit (W21 Sect. 2.2.1) | not separable from the flux ratio |
| Telluric mask 7590–7660 Å air | per-mask blue-star correction (W21 Sect. 2.2.2; S18 step 5) | H₂O and O₂ templates per mask, wavelength shift and smoothing per galaxy, 6000–9300 Å (W21 Sect. 2.2.2) | A band stays masked; χ std inside DR2 ranges 0.48–1.15, outside 0.42–1.06 |
| Calibration polynomial: Chebyshev order 10, σ(a₀) 0.3, σ(a₁…a₁₀) 0.1 | FAST template fits, 5th-order polynomial (S18 Sect. 2) | bagpipes fits to UltraVISTA BVrizYJ, revised zero points, 5th-order Legendre on spectrum and variance (W21 Sect. 2.2.3) | flux ratio 0.83–1.12, shape 8–32%; fitted polynomial ratio follows it to 0.7–2.2% rms (M4_107370 full range: 4.0%) |
| Noise floor f_calib, 1–10% | `ERR` | `ERR` scaled with the flux (W21 Sect. 2.2.3) | error ratio / flux ratio 0.97–1.12 in 9 of 10; M2_134021 0.63 |
| Redshift fixed at catalogue `z` | DR2 `z` | DR3 `Z` | ≤ 93 km/s |
| σ★ prior Normal(catalogue, error) | DR2 σ★, error | DR3 σ★ −14 to +15 km/s; error 0.51–0.86 × DR2 | narrower prior |
| Catalogue uncertainties | duplicate scatter 1.25 ± 0.25 × noise (S18 Sect. 3.2) | rescaled 1.25–2 from duplicates (W21 Appendix C) | enters the σ★ prior and the emission-line cuts |
| Photometry: COSMOS2025, else Classic | keyed by `SPECT_ID` | same rows for shared `SPECT_ID` | identical photometry |
| Selection flags | `f_use` 1, `f_ppxf` 0, `f_z` 0, `f_int` 0 | `FLAG_PRIMARY` 1, `FLAG_SPEC` 0, `FLAG_MORPH` 0 (W21 Sect. 4.2) | 10 of 10 pass |
| Weak [O II]: EW > −5 Å | emission EW negative | emission EW positive; DR3/DR2 median −0.97 over shared spectra | DR3 cut: EW < 5 Å |

## Paired fits, 10 test galaxies

| arm | settings | fits | reference |
|---|---|---|---|
| `dr3_full` | `data_source` `legac_dr3`; production defaults | 10 | test-set baseline, `results/afe-ladder-floor-2026-11-10` `free_afe` (9b189a36 / Ceridwen a0b1f6ed), 10 |
| `dr3_window` | as `dr3_full`, `rest_range` [4074.5, 4666.1] | 10 | chronometer arm (i), `results/chronometer-135-2026-11-10/baseline-w110` (99c179ba / Ceridwen 13791e0e), 8 |

- Seed 20260832 in every fit. Modal A100-40GB, revision ed3d4f1b / Ceridwen 13791e0e. 20 of 20 valid (`validate_result`). Modal cost estimate $1.86. App stopped.
- M5_238314 and M8_161113 are not in arm (i): their DR2 spectra do not cover the window.
- Δ = DR3 − DR2 posterior median. σ = half the DR2 16–84 range. Width ratio: DR3/DR2 half-widths.

| arm | parameter | galaxies | median Δ | median Δ/σ | max abs Δ/σ | median width ratio DR3/DR2 |
|---|---|---|---|---|---|---|
| full | age [Gyr] | 10 | -0.033 | -0.08 | 3.53 | 1.02 |
| full | [α/Fe] | 10 | -0.010 | -0.24 | 5.14 | 0.94 |
| full | [Fe/H] | 10 | +0.177 | +3.58 | 8.13 | 0.97 |
| full | τ_dust | 10 | -0.044 | -1.22 | 2.21 | 1.03 |
| full | f_calib [%] | 10 | +0.118 | +0.66 | 20.52 | 1.01 |
| full | σ★ [km/s] | 10 | -1.417 | -0.31 | 3.38 | 0.91 |
| window | age [Gyr] | 8 | +0.102 | +0.21 | 2.68 | 1.05 |
| window | [α/Fe] | 8 | -0.009 | -0.08 | 5.48 | 0.92 |
| window | [Fe/H] | 8 | +0.143 | +2.22 | 5.11 | 0.92 |
| window | τ_dust | 8 | -0.042 | -0.97 | 3.15 | 1.01 |
| window | f_calib [%] | 8 | +0.279 | +1.74 | 13.54 | 0.90 |
| window | σ★ [km/s] | 8 | +1.089 | +0.22 | 2.00 | 0.93 |

| arm | galaxy | z | age DR2 → DR3 (Δ/σ) | [α/Fe] DR2 → DR3 (Δ/σ) | [Fe/H] DR2 → DR3 (Δ/σ) | τ_dust Δ/σ | f_calib [%] DR2 → DR3 | photometry pull rms DR2 / DR3 |
|---|---|---|---|---|---|---|---|---|
| full | M1_210210 | 0.654 | 3.47 → 4.46 (+2.4) | +0.13 → +0.06 (-5.1) | -0.12 → -0.09 (+0.9) | +0.0 | 2.38 → 2.19 | 1.21 / 1.20 |
| full | M8_150848 | 0.701 | 3.63 → 3.92 (+0.7) | +0.04 → -0.02 (-2.9) | -0.07 → +0.07 (+4.1) | -1.4 | 2.26 → 2.11 | 4.71 / 4.72 |
| full | M5_238314 | 0.732 | 4.22 → 3.67 (-2.8) | -0.07 → -0.11 (-1.4) | -0.46 → -0.20 (+8.1) | -1.9 | 2.30 → 3.61 | 1.18 / 1.25 |
| full | M3_120308 | 0.728 | 4.47 → 3.43 (-2.4) | +0.01 → -0.08 (-2.2) | -0.08 → +0.09 (+3.8) | +0.1 | 2.95 → 2.94 | 1.13 / 1.15 |
| full | M2_134021 | 0.749 | 3.31 → 4.05 (+1.5) | +0.10 → +0.10 (+0.2) | -0.36 → -0.18 (+2.9) | -1.0 | 2.91 → 4.71 | 1.21 / 1.20 |
| full | M7_146213 | 0.688 | 4.53 → 4.49 (-0.1) | +0.09 → +0.10 (+0.3) | -0.17 → +0.01 (+3.4) | -2.2 | 3.94 → 5.15 | 1.22 / 1.26 |
| full | M3_117010 | 0.677 | 4.35 → 4.32 (-0.1) | -0.05 → -0.07 (-0.4) | -0.53 → -0.32 (+5.1) | -2.0 | 3.79 → 4.35 | 1.39 / 1.41 |
| full | M4_107370 | 0.844 | 4.32 → 3.17 (-3.5) | -0.16 → +0.01 (+4.9) | -0.72 → -0.33 (+7.5) | -2.1 | 6.28 → 4.50 | 1.27 / 1.14 |
| full | M14_37219 | 0.735 | 3.54 → 3.47 (-0.2) | -0.06 → -0.06 (-0.0) | -0.24 → -0.18 (+1.3) | -0.8 | 3.34 → 3.16 | 1.18 / 1.21 |
| full | M8_161113 | 0.891 | 4.21 → 4.22 (+0.0) | -0.20 → -0.19 (+0.4) | -0.29 → -0.17 (+2.5) | -1.1 | 4.23 → 4.48 | 1.39 / 1.36 |
| window | M1_210210 | 0.654 | 5.18 → 5.30 (+0.3) | +0.23 → -0.01 (-5.5) | -0.45 → -0.24 (+3.9) | -0.5 | 2.11 → 2.29 | 1.21 / 1.16 |
| window | M8_150848 | 0.701 | 4.75 → 5.53 (+1.7) | +0.08 → -0.03 (-1.7) | -0.37 → -0.33 (+0.7) | -0.5 | 1.93 → 2.02 | 4.70 / 4.70 |
| window | M3_120308 | 0.728 | 5.38 → 4.37 (-2.7) | +0.02 → +0.03 (+0.1) | -0.62 → -0.26 (+5.1) | -2.8 | 1.90 → 2.67 | 1.16 / 1.14 |
| window | M2_134021 | 0.749 | 4.41 → 4.84 (+0.7) | +0.10 → +0.10 (-0.0) | -0.47 → -0.40 (+0.9) | -0.8 | 1.93 → 4.63 | 1.15 / 1.15 |
| window | M7_146213 | 0.688 | 5.04 → 5.74 (+1.4) | +0.03 → +0.07 (+0.4) | -0.41 → -0.38 (+0.3) | -1.2 | 3.60 → 3.82 | 1.23 / 1.25 |
| window | M3_117010 | 0.677 | 4.62 → 4.52 (-0.2) | +0.16 → +0.17 (+0.1) | -0.53 → -0.21 (+4.1) | -3.2 | 3.41 → 3.74 | 1.39 / 1.39 |
| window | M4_107370 | 0.844 | 3.96 → 3.17 (-1.7) | +0.28 → +0.26 (-0.1) | -0.75 → -0.36 (+3.5) | -2.4 | 4.54 → 3.78 | 1.16 / 1.11 |
| window | M14_37219 | 0.735 | 4.32 → 4.40 (+0.1) | +0.20 → +0.16 (-0.6) | -0.37 → -0.30 (+0.8) | -0.6 | 2.96 → 3.57 | 1.23 / 1.23 |

### Calibration polynomial

- Posterior-median polynomial ratio DR3/DR2 on pixels fitted in both, against the smooth flux ratio on the same pixels.
- rms: polynomial ratio minus flux ratio, each normalised to its median.

| arm | galaxy | polynomial ratio DR3/DR2, median | polynomial ratio peak-to-peak | flux ratio peak-to-peak | rms (polynomial ratio − flux ratio) | DR2 polynomial half-width |
|---|---|---|---|---|---|---|
| full | M1_210210 | 0.855 | 13% | 11% | 1.1% | 1.3% |
| full | M8_150848 | 0.939 | 15% | 15% | 0.7% | 1.4% |
| full | M5_238314 | 1.071 | 10% | 14% | 2.1% | 1.3% |
| full | M3_120308 | 0.856 | 27% | 31% | 1.8% | 1.5% |
| full | M2_134021 | 0.824 | 18% | 21% | 1.4% | 1.5% |
| full | M7_146213 | 1.021 | 19% | 13% | 1.8% | 1.6% |
| full | M3_117010 | 0.887 | 13% | 14% | 1.4% | 1.5% |
| full | M4_107370 | 0.835 | 61% | 26% | 4.0% | 1.5% |
| full | M14_37219 | 0.882 | 17% | 20% | 1.3% | 1.3% |
| full | M8_161113 | 1.131 | 7% | 8% | 1.9% | 1.6% |
| window | M1_210210 | 0.855 | 10% | 3% | 1.8% | 1.3% |
| window | M8_150848 | 0.929 | 6% | 6% | 0.9% | 1.4% |
| window | M3_120308 | 0.847 | 7% | 3% | 0.9% | 1.5% |
| window | M2_134021 | 0.805 | 8% | 5% | 1.2% | 1.5% |
| window | M7_146213 | 0.981 | 9% | 9% | 1.4% | 1.6% |
| window | M3_117010 | 0.855 | 5% | 6% | 1.5% | 1.5% |
| window | M4_107370 | 0.834 | 9% | 5% | 2.2% | 1.7% |
| window | M14_37219 | 0.875 | 4% | 3% | 0.9% | 1.5% |

### Feature-band pulls

- Band pull: Σ pull / √n over fitted pixels in each band (`feature_windows`). Bands fitted in both fits.

| arm | feature | galaxies | median pull DR2 | median pull DR3 | median Δ | max abs Δ |
|---|---|---|---|---|---|---|
| full | H10 | 6 | -1.40 | -2.25 | -0.53 | 1.79 |
| full | H9 | 7 | +0.63 | +0.42 | +0.10 | 1.74 |
| full | H8 | 8 | +1.51 | +1.13 | -0.36 | 2.27 |
| full | HdA | 10 | -0.60 | -1.37 | -0.90 | 2.11 |
| full | HgA | 10 | +1.53 | +1.54 | +0.45 | 3.17 |
| full | Hbeta | 9 | +0.57 | -0.02 | +0.03 | 3.25 |
| full | Ca4455 | 10 | +0.49 | +0.42 | +0.39 | 3.32 |
| full | CN4150 | 10 | -1.73 | -2.46 | -0.29 | 2.42 |
| full | G4300 | 10 | +1.20 | +0.07 | -1.79 | 3.68 |
| full | C4668 | 9 | -3.69 | -3.95 | -0.55 | 2.34 |
| full | Fe4383 | 10 | -0.35 | -0.56 | -0.00 | 2.89 |
| full | Fe4531 | 10 | +0.38 | -1.05 | -1.14 | 5.77 |
| full | Fe5015 | 9 | -0.28 | +0.12 | -0.15 | 4.10 |
| full | Mgb | 5 | -4.09 | -4.19 | -0.04 | 2.98 |
| full | Fe5270 | 3 | -3.55 | -1.88 | +1.56 | 3.59 |
| full | Fe5335 | 3 | +2.16 | -0.19 | -2.47 | 2.92 |
| full | Fe5406 | 1 | -1.46 | +0.16 | +1.62 | 1.62 |
| window | HdA | 8 | +0.18 | -0.25 | -0.00 | 1.08 |
| window | HgA | 8 | +0.72 | +1.47 | +0.64 | 1.22 |
| window | Ca4455 | 8 | +0.96 | +1.44 | +0.40 | 0.77 |
| window | CN4150 | 8 | -1.30 | -1.48 | -0.43 | 1.58 |
| window | G4300 | 8 | +0.76 | -0.51 | -1.24 | 3.60 |
| window | C4668 | 8 | -0.61 | -0.76 | -0.23 | 1.72 |
| window | Fe4383 | 8 | +0.48 | +0.56 | +0.45 | 2.87 |
| window | Fe4531 | 8 | +0.26 | -0.66 | -0.85 | 4.40 |

## Test set: likelihood and evidence

- ln Z and log L are for different data vectors and error bars: DR3 errors are rescaled (W21 Appendix C). The comparable numbers are the spectral χ² per pixel at raw catalogue errors and at one fixed f_calib.
- Model: posterior-median spectrum. Pixels fitted in both releases (`common`). Fixed f_calib: the DR2 fit's posterior median, for both. σ_eff² = σ² + (f_calib · model)² (`ceridwen/likelihood/noise_model.py`). No noise floor in any fit.
- Improves: higher ln Z or log L, lower χ².

| arm | quantity | pairs | median DR2 | median DR3 | median DR3 − DR2 | improves in DR3 |
|---|---|---|---|---|---|---|
| full | ln Z | 10 | 235552.1 | 234479.7 | -478.9 | 4 |
| full | max log L | 10 | 235582.0 | 234509.7 | -481.3 | 4 |
| full | posterior-median log L | 10 | 235576.8 | 234503.3 | -482.0 | 4 |
| full | spectral χ²/px, raw errors | 10 | 1.826 | 2.006 | +0.289 | 3 |
| full | spectral χ²/px, fixed f_calib | 10 | 1.073 | 1.183 | +0.117 | 3 |
| full | spectral χ²/px, own f_calib | 10 | 1.073 | 1.174 | +0.086 | 4 |
| full | photometry χ² | 10 | 41.3 | 42.2 | +1.3 | 4 |
| window | ln Z | 8 | 95506.0 | 93944.2 | -143.9 | 3 |
| window | max log L | 8 | 95531.8 | 93971.8 | -143.7 | 3 |
| window | posterior-median log L | 8 | 95526.4 | 93964.7 | -143.6 | 3 |
| window | spectral χ²/px, raw errors | 8 | 1.553 | 1.666 | +0.216 | 1 |
| window | spectral χ²/px, fixed f_calib | 8 | 1.011 | 1.181 | +0.131 | 0 |
| window | spectral χ²/px, own f_calib | 8 | 1.011 | 1.109 | +0.118 | 2 |
| window | photometry χ² | 8 | 41.4 | 39.9 | -0.5 | 5 |

| arm | galaxy | fitted px DR2 / DR3 / common | Δ ln Z | Δ max log L | Δ median log L | χ²/px raw DR2 → DR3 | χ²/px fixed f_calib DR2 → DR3 | χ²/px own f_calib DR2 → DR3 | f_calib [%] DR2 → DR3 | photometry χ² DR2 → DR3 (n) |
|---|---|---|---|---|---|---|---|---|---|---|
| full | M1_210210 | 3607 / 3610 / 3599 | +578.6 ± 0.3 | +580.1 | +579.5 | 3.006 → 3.290 | 1.035 → 1.076 | 1.035 → 1.185 | 2.4 → 2.2 | 41.1 → 40.6 (28) |
| full | M8_150848 | 3785 / 3807 / 3771 | +1579.5 ± 0.3 | +1575.1 | +1578.3 | 2.004 → 1.875 | 1.108 → 1.081 | 1.108 → 1.137 | 2.3 → 2.1 | 620.3 → 624.3 (28) |
| full | M5_238314 | 3603 / 3588 / 3566 | -1934.0 ± 0.3 | -1936.8 | -1936.3 | 1.940 → 2.717 | 1.215 → 1.735 | 1.215 → 1.204 | 2.3 → 3.6 | 38.7 → 43.5 (28) |
| full | M3_120308 | 3604 / 3585 / 3565 | -1087.8 ± 0.3 | -1089.7 | -1089.4 | 1.843 → 2.136 | 1.076 → 1.269 | 1.076 → 1.273 | 3.0 → 2.9 | 36.0 → 37.1 (28) |
| full | M2_134021 | 3630 / 3451 / 3434 | -11813.4 ± 0.3 | -11814.9 | -11814.1 | 1.623 → 5.924 | 1.030 → 2.471 | 1.030 → 1.365 | 2.9 → 4.7 | 40.8 → 40.5 (28) |
| full | M7_146213 | 3618 / 3601 / 3559 | -1518.7 ± 0.3 | -1520.2 | -1518.6 | 1.809 → 2.315 | 1.145 → 1.400 | 1.145 → 1.115 | 3.9 → 5.2 | 41.5 → 44.1 (28) |
| full | M3_117010 | 3539 / 3531 / 3509 | -509.0 ± 0.3 | -509.5 | -510.2 | 1.531 → 1.860 | 1.069 → 1.311 | 1.069 → 1.212 | 3.8 → 4.3 | 54.3 → 55.8 (28) |
| full | M4_107370 | 3573 / 3589 / 3546 | +1379.3 ± 0.3 | +1378.4 | +1378.2 | 2.091 → 1.730 | 0.955 → 0.924 | 0.955 → 1.163 | 6.3 → 4.5 | 45.4 → 36.1 (28) |
| full | M14_37219 | 3578 / 3591 / 3570 | +1403.6 ± 0.3 | +1404.0 | +1403.9 | 1.334 → 1.336 | 1.070 → 1.036 | 1.070 → 1.058 | 3.3 → 3.2 | 38.7 → 40.9 (28) |
| full | M8_161113 | 3550 / 3553 / 3531 | -448.9 ± 0.3 | -453.1 | -453.8 | 1.506 → 1.414 | 1.095 → 1.096 | 1.095 → 1.071 | 4.2 → 4.5 | 54.5 → 52.1 (28) |
| window | M1_210210 | 1396 / 1392 / 1390 | -245.8 ± 0.3 | -245.7 | -245.6 | 2.705 → 3.817 | 0.975 → 1.239 | 0.975 → 1.111 | 2.1 → 2.3 | 40.8 → 37.5 (28) |
| window | M8_150848 | 1435 / 1434 / 1422 | -42.0 ± 0.3 | -41.7 | -41.7 | 1.564 → 1.624 | 1.056 → 1.122 | 1.056 → 1.091 | 1.9 → 2.0 | 619.0 → 618.0 (28) |
| window | M3_120308 | 1463 / 1455 / 1452 | -551.5 ± 0.2 | -549.3 | -550.6 | 1.256 → 1.709 | 0.971 → 1.320 | 0.971 → 1.107 | 1.9 → 2.7 | 37.4 → 36.6 (28) |
| window | M2_134021 | 1485 / 1391 / 1389 | -6336.2 ± 0.3 | -6334.6 | -6335.8 | 1.209 → 5.651 | 0.967 → 3.436 | 0.967 → 1.327 | 1.9 → 4.6 | 37.0 → 36.8 (28) |
| window | M7_146213 | 1416 / 1392 / 1375 | -1617.5 ± 0.2 | -1617.3 | -1617.0 | 1.568 → 1.588 | 1.086 → 1.107 | 1.086 → 1.064 | 3.6 → 3.8 | 42.6 → 43.8 (28) |
| window | M3_117010 | 1402 / 1407 / 1391 | +385.5 ± 0.2 | +388.0 | +386.6 | 1.541 → 1.791 | 1.082 → 1.255 | 1.082 → 1.184 | 3.4 → 3.7 | 53.9 → 54.4 (28) |
| window | M4_107370 | 1543 / 1563 / 1534 | +1360.0 ± 0.2 | +1359.5 | +1359.9 | 1.726 → 1.613 | 0.989 → 1.019 | 0.989 → 1.139 | 4.5 → 3.8 | 37.4 → 34.2 (28) |
| window | M14_37219 | 1461 / 1470 / 1459 | +756.0 ± 0.2 | +755.9 | +755.3 | 1.284 → 1.466 | 1.034 → 1.123 | 1.034 → 1.018 | 3.0 → 3.6 | 42.1 → 42.3 (28) |

- M2_134021: DR3 error/flux ratio 0.63 × DR2, S/N 1.58 × DR2 (spectra table above).

## DR3 sample

- Same cuts as the DR2 notebook selection; DR3 flags and EW sign as in the table above. COSMOS2015 matches of each release.
- Fittable photometry: COSMOS2025 `warn-flag` 0, else Classic `FlagCOMBINED` 0 (`scripts/cosmos_photometry.py` `fit_photometry`). DR2: 180 of 187, the DR2 135 are a subset.
- Covers window: valid rest-vacuum pixel range contains 4074.5–4666.1 Å. DR2: 110 of the 135, as in arm (i).

| cut | DR2 | DR3 |
|---|---|---|
| catalogue x COSMOS2015 | 1982 | 4057 |
| quality flags, z, S/N, NUV r J | 1328 | 2571 |
| NUVrJ quiescent | 609 | 1222 |
| [O II] EW below 5 A | 454 | 931 |
| no 3 sigma [O II], [O III] | 349 | 581 |
| clean COSMOS2015 photometry | 194 | 329 |
| one spectrum per OBJECT | 187 | 302 |
| fittable photometry | 180 | 284 |
| fittable, covers window | 144 | 208 |
| and finite σ★ error | 144 | 194 |

- DR3 302: 129 objects also in the DR2 187; 173 new.
- DR2 187 spectra not selected in DR3 (`dr2-only-galaxies.csv`): 47 a 3σ [O II] or [O III] line, 8 [O II] EW and a 3σ line, 3 `FLAG_MORPH` 1, 7 another spectrum of the same object selected (higher `SN`). Of the DR2 135: 33, 7, 2, 6.
- Finite σ★ error: the σ★ prior is Normal(catalogue, error). 14 of the 208 have a NaN `SIGMA_STARS_PRIME_ERR` (M26 5, M28 4, M31 4, M32 1); 13 of them lie outside the HST F814W mosaic. All DR3: 428 spectra with σ★ and no error; DR2: 0.
- 194 fitted: z 0.603–0.999, median 0.728; 99 with COSMOS2025, 95 with Classic; 69 are DR2 135 spectra; 73 objects fitted in chronometer arm (i).

## Phase 3: DR3 window sample, 194 galaxies

- Plain grid (`dr3_plain_w`) and C/N free (`dr3_cn_free_w`), `rest_range` [4074.5, 4666.1]. `window-194/experiment.json`, seed 20260832.
- Modal A100-40GB. Source dea84377, ceridwen 13791e0e, sedpy_jax 9d8aa190, image `ghcr.io/potatoist314/ceridwen-gpu@sha256:e1c8846c…`.
- Estimate before launch: 194 × ($0.081 + $0.120) = $39. Modal billing report: $37.39 (attempt 0) + $0.96 (attempt 1) = $38.35.
- Attempt 0, 10 containers, app `ap-fKRBuiwcxTzcWygvBP4UZC`: credits stopped at $251.20 at about 15:16; app stopped 15:20 (`modal app stop`). 310 fits returned by `experiment.py`. Containers 6 and 8 failed at the stop; 71 of their finished fits had been copied from the live containers (`modal container exec`, MD5-checked) and are in `manifest.json` `completed_cells` with a `recovered` note. 298 fits copied the same way and also returned by `experiment.py`: 1192 of 1192 files byte-identical. 7 cells not finished.
- Attempt 1, after the credit top-up (16:26): the same command with `--output window-194/run`; the 7 cells, 7 containers, all complete.
- Fit status per cell: `window-194-fit-status.csv`.
- DR2 references: chronometer arm (i) plain and arm (j) C/N free, the 73 window fits whose `OBJECT` is in the 194. DR2 overlap: `OBJECT` fitted in arm (i); new in DR3: the rest.

| arm | release | fits | valid |
|---|---|---|---|
| C/N free | DR2 | 73 | 73 |
| C/N free | DR3 | 194 | 194 |
| plain | DR2 | 73 | 73 |
| plain | DR3 | 194 | 194 |

- Slope: least-squares age against z; 16–84: 10000 bootstrap resamples of galaxies, seed 20261110.
- Planck18 line: the same fit to the age of the universe at each galaxy z (Planck 2018, Astropy `Planck18`).
- H = −1 / ((1 + z_med) dt/dz) (Jimenez & Loeb 2002, eq. 2).

| arm | release | galaxies | z range | z median | slope [Gyr per unit z] | bootstrap 16–84 | scatter [Gyr] | Planck18 line | H [km/s/Mpc] | H from 16–84 |
|---|---|---|---|---|---|---|---|---|---|---|
| plain, all | DR3 | 194 | 0.603–0.999 | 0.728 | -5.04 | -5.70 to -4.39 | 0.87 | -5.23 | 112 | 99–129 |
| C/N free, all | DR3 | 194 | 0.603–0.999 | 0.728 | -5.15 | -5.78 to -4.53 | 0.80 | -5.23 | 110 | 98–125 |
| plain, DR2 overlap | DR3 | 73 | 0.603–0.984 | 0.728 | -4.77 | -5.78 to -3.72 | 0.94 | -5.24 | 119 | 98–152 |
| plain, DR2 overlap | DR2 | 73 | 0.603–0.984 | 0.728 | -4.48 | -5.46 to -3.45 | 0.84 | -5.24 | 126 | 104–164 |
| C/N free, DR2 overlap | DR3 | 73 | 0.603–0.984 | 0.728 | -5.02 | -5.96 to -4.07 | 0.82 | -5.24 | 113 | 95–139 |
| C/N free, DR2 overlap | DR2 | 73 | 0.603–0.984 | 0.728 | -5.14 | -6.08 to -4.11 | 0.80 | -5.24 | 110 | 93–138 |
| plain, new in DR3 | DR3 | 121 | 0.603–0.999 | 0.733 | -5.20 | -6.04 to -4.39 | 0.84 | -5.22 | 108 | 93–128 |
| C/N free, new in DR3 | DR3 | 121 | 0.603–0.999 | 0.733 | -5.27 | -6.08 to -4.49 | 0.80 | -5.22 | 107 | 93–126 |

| arm | group | release | galaxies | median [α/Fe] | ρ([α/Fe], z) | p | [α/Fe] slope per unit z (16–84) | median age [Gyr] | median [Fe/H] | median [C/Fe] | median [N/Fe] |
|---|---|---|---|---|---|---|---|---|---|---|---|
| plain | all | DR3 | 194 | +0.131 | -0.02 | 0.84 | +0.01 (-0.12 to +0.14) | 4.88 | -0.32 | — | — |
| plain | DR2 overlap | DR3 | 73 | +0.128 | +0.04 | 0.74 | -0.01 (-0.25 to +0.26) | 4.85 | -0.32 | — | — |
| plain | new in DR3 | DR3 | 121 | +0.132 | -0.03 | 0.72 | +0.01 (-0.13 to +0.16) | 4.94 | -0.31 | — | — |
| plain | DR2 overlap | DR2 | 73 | +0.203 | -0.11 | 0.36 | -0.39 (-0.61 to -0.12) | 4.85 | -0.51 | — | — |
| C/N free | all | DR3 | 194 | +0.160 | +0.06 | 0.43 | +0.09 (-0.04 to +0.22) | 4.88 | -0.32 | -0.03 | +0.24 |
| C/N free | DR2 overlap | DR3 | 73 | +0.167 | +0.09 | 0.43 | +0.11 (-0.12 to +0.38) | 4.86 | -0.33 | -0.03 | +0.22 |
| C/N free | new in DR3 | DR3 | 121 | +0.158 | +0.04 | 0.68 | +0.08 (-0.07 to +0.24) | 4.90 | -0.32 | -0.04 | +0.24 |
| C/N free | DR2 overlap | DR2 | 73 | +0.142 | -0.07 | 0.54 | -0.07 (-0.26 to +0.16) | 5.03 | -0.50 | -0.12 | +0.18 |

- [Fe/H] shift: DR3 − DR2 posterior median, each DR2-overlap galaxy. σ: half the DR2 16–84 range.

| arm | galaxies | higher in DR3 | median shift [dex] | 16–84 | median shift/σ | ρ(shift, z) | p | slope per unit z (16–84) | median age shift [Gyr] | median [α/Fe] shift | same spectrum |
|---|---|---|---|---|---|---|---|---|---|---|---|
| C/N free | 73 | 62 | +0.182 | +0.028 to +0.314 | +2.42 | -0.01 | 0.91 | -0.35 (-0.73 to +0.09) | -0.21 | +0.020 | 69 |
| plain | 73 | 62 | +0.211 | +0.022 to +0.340 | +2.36 | -0.04 | 0.77 | -0.35 (-0.74 to +0.09) | -0.05 | -0.052 | 69 |

| arm | spectrum | galaxies | higher in DR3 | median shift [dex] |
|---|---|---|---|---|
| C/N free | same SPECT_ID | 69 | 58 | +0.164 |
| C/N free | other SPECT_ID | 4 | 4 | +0.224 |
| plain | same SPECT_ID | 69 | 58 | +0.191 |
| plain | other SPECT_ID | 4 | 4 | +0.248 |

## Files

- `analysis.ipynb`: every table above.
- `crossmatch.csv`, `spectra-dr3-vs-dr2.csv`, `selection-counts.csv`, `selection-per-galaxy.csv`, `dr2-only-galaxies.csv`, `fits.csv`, `paired-changes.csv`, `paired-changes-per-galaxy.csv`, `calibration-polynomial.csv`, `band-pulls.csv`, `band-pulls-per-galaxy.csv`, `likelihood-evidence.csv`, `likelihood-evidence-per-galaxy.csv`.
- `test-set/experiment.json`, `test-set/run/` (fits, manifest, Modal logs), `test-set/run-driver.log`.
- `window-194-fits.csv`, `window-194-fit-status.csv`, `window-194-age-redshift-slopes.csv`, `window-194-afe-medians.csv`, `window-194-feh-shift.csv`, `window-194-feh-shift-per-galaxy.csv`.
- `window-194/experiment.json`, `window-194/run/` (fits, manifest, Modal logs), `window-194/run-driver.log`.
