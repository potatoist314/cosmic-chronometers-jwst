# Project roadmap

Rules for editing this file: `AGENTS.md` → *Roadmap discipline*.

## The brief

Supervisor email, relayed by the user 2026-07-28 (send date not recorded).
Authoritative — the stages are this list. Verbatim:

> A good first set of steps would be:
>
> 1. Reproduce the main cosmic-chronometer calculation from the paper you have
>    been reading, starting from the published age measurements and recovering
>    the quoted H(z) constraints.
>
> 2. Make sure you understand and can implement the relation between
>    differential galaxy ages and H(z), including how the uncertainties
>    propagate.
>
> 3. Build a simple MCMC framework with emcee to fit a model to mock
>    age–redshift data. Start with a very simple parametrisation and check that
>    you can recover known input parameters.
>
> 4. Explore the effect of different assumptions about the stellar ages. In
>    particular, test what happens if you introduce:
>
>    random age uncertainties;
>    a systematic age offset;
>    redshift-dependent biases;
>    intrinsic scatter between galaxies.
>
> 5. Generate mock samples at z > 2 with properties roughly representative of
>    the massive quiescent galaxies now being found with JWST. The main question
>    is: what age precision, sample size and redshift baseline would be required
>    to obtain a useful H(z) measurement?
>
> 6. Once that framework is working, we can provide you with more realistic
>    stellar-age constraints from our JWST samples and investigate whether the
>    method is already competitive at high redshift.

## Status

- **1. Reproduce Borghi `H(z)`** — **complete**, inspected 2026-07-29. `notebooks/02_differential_ages.ipynb` gives `H(0.753) = 95.7 ± 30.9` against the paper's `98.8 ± 24.8`; all four individual estimates within 5%. Two inferred choices, neither published: the redshift bin edges (reconstructed by fitting Table 1) and the per-bin age estimator (NMAD/√N, no median correction).
- **2. Ages ↔ `H(z)` + uncertainty propagation** — statistical propagation **complete** (2026-07-29); binning variation for `σ_sys` outstanding. Scope `[agreed 2026-07-28]`:
  - **No covariance matrix.** Borghi 2022b §3.1 quotes a variance, not a covariance — one `H(z)` point. `external/CCcovariance/` is deferred to a later step.
  - Target: `σ_stat` from the variance-weighted average of the 4 independent `H(z)` estimates (their Table 1), `σ_sys` from the spread of analysis variants, combined in quadrature → `H(0.75) = 98.8 ± 33.6` (their Eq. 2).
  - Reproduce the **binning-variation** contribution to `σ_sys` (~1/4 of their budget). SPS model and SFH variations remain out of scope.
  - **Lick index variation added `[agreed 2026-07-28]`.** Reproducing Borghi 2022b Figure 2 needs an age–redshift relation per index combination. Paper I Appendix C / Table 6 defines the combinations but publishes only aggregate offsets, not per-galaxy ages, so this requires re-running the SPS fitting on the LEGA-C indices. Treat as its own sub-project, not a variant of the existing analysis.
    - **Method `[agreed 2026-07-31]`.** Per galaxy in the bona fide passive
      sample: flat priors spanning the model grid, Gaussian independent-index
      likelihood (Borghi 2022a Eq. 7), `emcee` → posteriors on age, `[Z/H]`,
      `[α/Fe]`. Prerequisite not yet implemented: correcting the LEGA-C indices
      to zero velocity dispersion, since the models carry none.
    - **SPS model substituted `[agreed 2026-07-31]`.** TMJ11 is used by Borghi
      as reference but could not be obtained — the Portsmouth and maraston.eu
      distributions are dead and it is not on VizieR. Using α-MILES (Vazdekis
      et al. 2015) instead, via `milespy`, which Borghi 2022b Appendix A adopts
      as their own cross-check. Two consequences: `[α/Fe]` is sampled at only
      0 and 0.4, so that parameter is weakly constrained (the paper reports the
      same limitation), and the IMF is bimodal 1.3 rather than TMJ11's
      Salpeter. Results are therefore our own baseline, not a reproduction of
      the paper's numbers.
- **3. emcee on mock age–redshift data** — starting 2026-07-31.
  - **Mock generator `[agreed 2026-07-31]`.** One function producing a mock
    age–redshift sample, with step 4's systematics present from the outset as
    parameters defaulting to zero — random age uncertainty, constant age
    offset, redshift-dependent bias, intrinsic scatter. Step 4 then varies
    arguments rather than rewriting the generator, and step 3's null case is
    the all-zeros call. Fixed recorded seeds per `AGENTS.md`.
  - Astropy's `FlatLambdaCDM` supplies the true age–redshift relation, so
    `src/cosmology.py` is not extended for this. `H_from_bins` is the only
    notebook estimator with no astropy equivalent.
  - Definition of done, exit criteria, and the parametrisation to fit: not
    settled, decide in discussion.
- **4. Systematics: scatter, offset, z-bias, intrinsic scatter** — not started
- **5. `z > 2` mocks → required precision / sample size / baseline** — not started
- **6. Real JWST constraints** — external gate, no date

Scope, sequencing, and definition of done per step: not settled, decide in discussion.

## Notes

- `notebooks/01_age_of_universe.ipynb` (Cimatti & Moresco 2023, absolute ages → `H0`) is not one of the six steps.
- Half-time availability; horizon early Oct 2026.
- Travel ~22 Aug – 4 Sep, **unconfirmed**.

Open questions, working notes, and reasoning go in the dated session records, not here.
