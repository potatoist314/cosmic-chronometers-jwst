# Session: Prospector full-spectrum age for one LEGA-C galaxy

- **Date:** 2026-08-06
- **Project phase:** Exploratory SED-fitting branch, alongside Step 2's Lick-index sub-project
- **Session status:** completed
- **Primary goal:** Fit the LEGA-C DR2 spectrum of OBJECT 207825 with Prospector/FSPS under a
  single-burst SFH, and compare the resulting SSP-equivalent age with the Lick-index answer and with
  Borghi's published value.

## Why this session matters

Notebook 02's Lick route reproduces Borghi's age for this galaxy (1.92 against 1.94 Gyr) but with
reduced chi-squared 18.2 on ten indices, so the model does not fit within the quoted errors and the age
agreement is not validation. Fitting the same galaxy's actual spectrum is an independent route to the
same quantity: a different SPS library (FSPS with MIST isochrones and MILES spectra, rather than
alpha-MILES through `milespy`), a different data vector (3722 pixels rather than 10 pre-measured index
numbers), and a different set of systematics.

## Starting point

- **Last verified state:** `notebooks/03_sed_fitting_AI_written.ipynb` ended at cell `caff961a` with a
  validated `load_spectrum` (cell `0c0d3e7e`). Notebook 02 was re-executed clean earlier the same day.
- **Relevant files or notebook sections:** `notebooks/03_sed_fitting_AI_written.ipynb` after `caff961a`.
- **Inputs and provenance:** `data/raw/legac_dr2/sp/legac_M1_207825_v2.0.fits`; DR2 catalogue `z` and
  `SIGMA_STARS_PRIME`; FSPS 0.4.8 via `astro-prospector` 1.4.1.
- **Open question or uncertainty:** whether the poor Lick chi-squared reflects the SPS model or the
  catalogue index measurements.

## Definition of done

An `emcee` posterior on `tage`, `logzsol` and `sigma_smooth` for OBJECT 207825, a reduced chi-squared
over unmasked pixels quoted next to the Lick fit's 18.2, and a synthetic-recovery test that separates
forward-model error from data-model mismatch.

## Scope

- **In scope:** spectroscopy only, single-burst SSP, one galaxy, the `_AI_written` notebook.
- **Out of scope:** photometry, the other 242 galaxies, any `H(z)` recomputation, delayed-tau SFHs, and
  `notebooks/03_sed_fitting.ipynb`.

## Predictions before calculation

`sigma_smooth` should come back near `sqrt(sigma*^2 + sigma_inst^2 - sigma_MILES^2)` = 223 km/s. That
single number tests units, redshifting, the wavelength convention and the LSF treatment at once.

## Working log

- **Data conventions —** The FITS header gives `SPEC_RES = 2500`, not the 3500 notebook 02 assumed for
  the Lick broadening. `SPEC_BIN = 0.6` A/pixel, `EXPTIME = 76800 s`, `TOT_FLUX = False`.
- **Air/vacuum, measured not assumed —** Centroided Ca II K, Ca II H, H-beta and Mg b in an FSPS SSP
  against both conventions. Residuals from *air* grow monotonically with wavelength
  (+0.34, +0.79, +1.00, +1.36 A); residuals from *vacuum* do not (-0.78, -0.33, -0.36, -0.09 A).
  **FSPS is on a vacuum scale.** LEGA-C `WAVE` is air, so the notebook applies
  `specutils.utils.wcs_utils.air_to_vac`: +1.74 A at 6283 A rising to +2.40 A at 8735 A, roughly 3-4
  pixels. It is not a constant velocity offset, so a fixed `zred` cannot absorb it.
- **Performance, the load-bearing discovery —** Prospector smooths on the *observed* wavelength grid,
  and with no window `smooth_vel_fft` resamples the entire FSPS array (91 A to 1e8 A) onto a uniform
  log grid at every likelihood call. Setting `min_wave_smooth`/`max_wave_smooth` to bracket the
  observed coverage takes one `model.predict` from **2830 ms to 1.6 ms** with a **bit-identical**
  output spectrum (max difference exactly 0), while smoothing remains active (sigma = 60 vs 350 km/s
  differ by 5.7% rms). The window must be in the observed frame; a rest-frame window silently excludes
  all the data and is fast for the wrong reason. Also measured: `zcontinuous=1` costs ~30 s on the
  first call and ~30 s on the first metallicity change and is free afterwards, whereas `zcontinuous=0`
  costs ~14 s on *every* metallicity change. `FastSSPBasis` was benchmarked at ~580 ms and rejected.
- **First run, and a prior mistaken for a model limit —** With `mass` free and Prospector's default
  `logzsol` prior the chain railed at the ceiling `logzsol = 0.19` and returned age 2.18 Gyr. Checking
  `fsps.StellarPopulation().zlegend` shows the MIST grid actually spans `logzsol` **-2.5 to +0.5**;
  0.19 is prospector's default prior, not the library edge. `mass` was also fixed, since the
  calibration polynomial rescales the model at every call and makes it exactly degenerate; it was the
  worst-mixing parameter (tau = 123, n_tau = 24).
- **Second run —** With `logzsol` free to +0.5 and `mass` fixed, the age moved from **2.18 to 1.44 Gyr**
  and `logzsol` settled at **+0.37**. Convergence is now adequate: n_tau 72-81 across all three
  parameters, against 11.5 for the Lick emcee run.
- **Synthetic recovery —** A spectrum generated at `logzsol = -0.10, tage = 2.50, sigma = 200`, put on
  this galaxy's own wavelength grid and mask with its own per-pixel errors, refits to
  `-0.110 +/- 0.008`, `2.522 +/- 0.03`, `198.3 +/- 2.0`; pulls -1.17, +0.82, -1.32, and
  chi-squared per pixel 1.00. **The forward model is correct.** Units, air-to-vacuum, redshifting,
  smoothing, the polynomial calibration and the sampler all check out.

## Session close-out

- **Final status:** completed
- **Accomplished:** the full one-galaxy Prospector fit, its comparison against both Lick numbers, and a
  passing synthetic-recovery test. Notebook re-executed headless and saved with in-order execution
  counts 1-26 and zero errors.
- **Key results and interpretation:**
  - **The age is prior-dependent at the 50% level.** Capping `logzsol` at prospector's default 0.19
    gives **2.18 Gyr**; allowing the full FSPS/MIST range to +0.5 gives **1.44 Gyr** at
    `logzsol = +0.37`. Borghi's published value is 1.94 Gyr and notebook 02's alpha-MILES Lick grid
    gives 1.92 (+0.19/-0.13). The Lick answer sits between the two Prospector answers. The
    age-metallicity degeneracy is running away toward very metal-rich, super-solar models, and where it
    stops is set by a prior nobody in this project has yet justified. **This is the headline result and
    it matters for `H(z)`**, because a systematic age shift of this size propagates directly.
  - **`logzsol = +0.37` is outside where MILES has stars.** The empirical library thins out above
    [Fe/H] ~ +0.2, so the preferred model is extrapolating. The fit is telling us the model family is
    wrong, not that the galaxy is 2.3x solar metallicity.
  - **Reduced chi-squared is 3.23 over 3722 pixels.** Better than the Lick fit's 18.2 but still a clear
    misfit, and the synthetic test proves it is not a bug in the machinery. So the poor Lick
    chi-squared is *not* mainly an artefact of the index measurements or their errors: an independent
    SPS model fitting the raw pixels also fails, if less badly. The remaining suspects are the
    single-burst SFH and the absence of an [alpha/Fe] axis in MIST.
  - **The quoted uncertainties are meaningless.** +/-0.02 Gyr on an age, with chi-squared per pixel of
    3.23, is the classic full-spectrum-fitting pathology: 3722 pixels and no model-systematics term.
    Do not propagate these into anything.
  - **`sigma_smooth` = 255 km/s against 223 predicted**, a 14% excess that is highly significant
    against its +/-1 km/s formal error. It is not a bug — the synthetic test recovers 198 from an input
    of 200. The model is absorbing a real mismatch into extra broadening, most plausibly because a
    single burst has narrower effective absorption features than a composite population.
- **Files changed or created:** `notebooks/03_sed_fitting_AI_written.ipynb` (nine cells after
  `caff961a`); this record.
- **Not completed:** nothing planned. The metallicity-prior sensitivity was found, not resolved.
- **Plan deviations:** two. The plan proposed bounding `tage` at the age of the universe; instead no
  age-of-universe prior is imposed at all, to keep the chain free of a cosmological assumption in a
  measurement whose whole point is model independence — `t_U(0.6968) = 7.18 Gyr` is printed for
  reference and the posterior does not approach it. The plan also budgeted ~5.3 h of sampling; the
  smoothing-window discovery reduced the real fit to 265 s.
- **Decisions made:** spectroscopy-only with a degree-10 calibration polynomial; `dust2` and `mass`
  fixed because both are degenerate with that polynomial; `logzsol` bounded by the FSPS grid rather
  than prospector's default prior; emission lines masked at +-3 sigma* in the observed frame.
- **Exact next starting point:** `notebooks/03_sed_fitting_AI_written.ipynb` after cell `9bb10adc`,
  with `obs`, `model`, `sps` and a validated forward model in memory.
- **Recommended next-session goal:** resolve the metallicity-prior sensitivity before anything is
  scaled up — scan `tage` against a sequence of `logzsol` ceilings (0.19, 0.3, 0.4, 0.5) to map how
  strongly the age depends on it, and decide the defensible cap from MILES' actual stellar coverage.
  Until that is settled, neither Prospector age should be carried into an `H(z)` estimate.
