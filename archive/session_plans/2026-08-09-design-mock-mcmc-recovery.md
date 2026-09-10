# Session: Design the mock age-redshift MCMC recovery test

- **Date:** 2026-08-09
- **Project phase:** Supervisor brief step 3 — mock age-redshift inference
- **Session status:** completed
- **Primary goal:** Create a separate notebook in which a simple age-redshift model is first benchmarked deterministically and then sampled with `emcee`, with recovery of injected parameters assessed explicitly.

## Why this session matters

This is the first end-to-end test that the project can generate a controlled
age-redshift data set, state an identifiable generative model, and distinguish
correct inference from a merely plausible MCMC plot. It also establishes the
inference pattern that later systematics tests can reuse.

## Starting point

- **Last verified state:** `session_plans/PROJECT_ROADMAP.md` records step 3 as started and the mock-generator design as agreed, but leaves the fitted parametrisation and definition of done unsettled. `src/mocks.py` contains `true_ages` and `make_mock`; its source and a fixed-seed null output were inspected directly this session.
- **Relevant files or notebook sections:** `src/mocks.py`; proposed new `notebooks/04_mock_mcmc_recovery.ipynb`; `notebooks/02_differential_ages.ipynb` only as a later differential-estimator cross-check.
- **Inputs and provenance:** Supervisor brief step 3, transcribed verbatim in `session_plans/PROJECT_ROADMAP.md`; fixed-seed null-systematics output from `make_mock`.
- **Open question or uncertainty:** The fitted parametrisation and completion criteria require user agreement. Codex and Claude Opus 5 (xhigh effort, `brutal` review) rejected jointly sampling `H0`, `Omega_m`, and `z_form` in the first fit because the narrow redshift baseline makes them non-identifiable. Claude additionally identified that fixing `z_form` at its truth would turn the exercise into an absolute-age constraint rather than a differential chronometer test.

## Definition of done

The user approved implementation on 2026-08-09. The notebook will:

1. reproduce the null mock's true ages with a model linear in a dimensionless inverse-`H0` scale and a free age intercept at fixed `Omega_m`;
2. compute the exact weighted-linear Gaussian posterior as an independent benchmark;
3. show that an `emcee` chain from two materially different initialisations reproduces the analytic posterior within predeclared tolerances;
4. record autocorrelation time, effective sample size, acceptance fraction, and stationary traces; and
5. test recovery across repeated fixed seeds using the analytic solution, while labelling this as a generator/plumbing check rather than evidence that more complex inference is calibrated.

Quantitative tolerances to test rather than assume: MCMC posterior means within
`0.05` analytic standard deviations, marginal standard deviations within `5%`,
correlation within `0.02`, post-burn chain length above `50` autocorrelation
times, and effective sample size at least `1000`. The injected truth should be
assessed with its joint Mahalanobis distance and repeated-seed pull/coverage,
not by requiring one posterior median to equal the truth exactly.

## Scope

- **In scope:** One null-systematics mock; fixed `Omega_m`; a free age intercept so the result remains differential; deterministic posterior; bounded priors; `emcee`; recovery and convergence checks; a separate notebook.
- **Out of scope:** Fitting `Omega_m`; random-age, offset, redshift-bias, or intrinsic-scatter experiments from step 4; realistic JWST mocks; covariance matrices; model comparison; edits to the roadmap before explicit user agreement.

## Planned tasks

### 1. Agree and validate the minimal generative model

- **Status:** completed
- **Purpose:** Prevent formation-time information or an unidentifiable cosmological parameter from masquerading as recovered chronometer information.
- **Work:** Use `t_model(z) = a g(z) + C`, where `a = 70/H0`, `g(z)` is the cosmic age at fixed `Omega_m = 0.3` and reference `H0 = 70`, and `C` is a free formation-time intercept. Define the bounded prior on `a` explicitly and derive `H0` only for interpretation. Verify the exact scaling against `FlatLambdaCDM` and the all-zeros mock.
- **Expected artifact:** First concept, imports, mock-generation, prediction, and kernel-validation cells in `notebooks/04_mock_mcmc_recovery.ipynb`, written and run by the user.
- **Trustworthiness check:** Units remain Gyr; the kernel matches Astropy at several `H0` values; the mock truth is reproduced to floating-point precision; the intercept is not fixed from `z_form`.

### 2. Construct the deterministic posterior benchmark

- **Status:** completed
- **Purpose:** Establish the answer `emcee` must recover before testing the sampler.
- **Work:** Build the weighted design matrix for `(a, C)`, solve its normal equations, inspect the covariance and degeneracy, and transform samples or summaries to conditional `H0` and `H(z_eff)`.
- **Expected artifact:** Analytic posterior mean, covariance, correlation, joint truth distance, and recorded pre-run predictions.
- **Trustworthiness check:** Matrix shapes and units are explicit; the solution agrees with a direct likelihood maximum; prior bounds do not truncate the reference posterior.

### 3. Sample the same posterior with `emcee`

- **Status:** completed
- **Purpose:** Test the MCMC framework against a known exact posterior rather than relying on appearance.
- **Work:** Implement bounded prior, Gaussian likelihood, walker initialisation, sampling, burn-in choice from autocorrelation time, and a second run from a broader initial state.
- **Expected artifact:** Posterior comparison, trace plot, acceptance fraction, autocorrelation time, and effective sample size in the separate notebook.
- **Trustworthiness check:** Both initialisations satisfy the predeclared analytic-comparison and chain-diagnostic tolerances.

### 4. Check repeated recovery

- **Status:** completed
- **Purpose:** Avoid declaring recovery from one fortunate noise realisation.
- **Work:** Run the cheap analytic estimator over a fixed recorded seed set; calculate pulls and 68% joint or marginal coverage; explain what this linear-Gaussian test does and does not validate.
- **Expected artifact:** Pull summary and coverage result in the notebook.
- **Trustworthiness check:** Pulls are centred and correctly scaled within binomial/sampling uncertainty; no step-4 systematics are introduced.

### 5. Make the notebook self-contained

- **Status:** completed
- **Purpose:** Let the notebook run without importing project source code.
- **Work:** Inline the mock result container and generator, preserving the tested random draws, units, truth metadata, and systematics arguments.
- **Expected artifact:** `notebooks/04_mock_mcmc_recovery.ipynb` contains no `src` import or repository-path setup.
- **Trustworthiness check:** A clean full execution reproduces the previously validated deterministic and MCMC results.

## Predictions before calculation

- The scale and intercept will be strongly anticorrelated because the redshift baseline is narrow.
- With `n = 100`, `0.6 < z < 1.0`, and `sigma_age = 0.3 Gyr`, the conditional `H0` uncertainty should be of order several percent, not the roughly one-percent result obtained by fixing the formation epoch.
- Freeing `Omega_m` at this stage would produce a prior-dominated curved degeneracy; this remains a later identifiability demonstration, not part of the reference recovery fit.
- `H(z_eff)` is the direct chronometer-like derived quantity; `H0` is conditional on the fixed `Omega_m` model.

## Working log

- **Start —** Inspected the dirty worktree, roadmap, session-plan convention, notebook layout, dependencies, and `src/mocks.py`. No pre-existing scientific file was modified.
- **External review —** Claude Opus 5, xhigh effort, completed a `brutal` review. It rejected fixing `z_form`, recommended a linear inverse-`H0` scale plus a free intercept at fixed `Omega_m`, required an analytic posterior benchmark before MCMC, and proposed explicit recovery and convergence tolerances. This is model advice, not user agreement or verified numerical evidence.
- **External review —** Claude identified conditional random-number consumption in `src/mocks.py` when intrinsic scatter is toggled. That matters for paired step-4 comparisons but is not part of this null recovery notebook and has not been edited.
- **Local verification —** For `n = 100`, seed 0, `0.6 < z < 1.0`, and `sigma_age = 0.3 Gyr`, the proposed kernel matched `FlatLambdaCDM` to `1.8e-15 Gyr` at `H0 = 60` and `80`. The exact weighted-linear solution gave `a = 0.99776 ± 0.04980`, `C = -2.12149 ± 0.32935 Gyr`, correlation `-0.99584`, and derived conditional `H0 = 70.16 ± 3.50`; the injected joint truth had squared Mahalanobis distance `0.63`. These command-line results are inspected benchmarks, not notebook completion evidence.
- **Notebook scaffold —** Created `notebooks/04_mock_mcmc_recovery.ipynb` with ten short concept sections and empty code cells. Explanations use the user's requested simplest-possible language; scientific implementation remains for the user to write.
- **Implementation resumed —** The user requested direct implementation, accepting the proposed two-parameter conditional model and its predeclared validation criteria.
- **Notebook execution —** A clean temporary execution completed all cells. The exact solution was `a = 0.99776 ± 0.04980`, `C = -2.12149 ± 0.32935 Gyr`, correlation `-0.99584`, and truth squared Mahalanobis distance `0.628`.
- **MCMC validation —** Near and broad starts had autocorrelation times `31.7–31.8`, about `5,900` effective samples per parameter, and acceptance fractions `0.713–0.716`. Their means differed from the exact posterior by at most `0.009` analytic standard deviations; marginal widths by at most `0.0041`; correlation by at most `0.0001`.
- **Repeated recovery —** Across seeds `0..199`, pull means were `[-0.020, 0.028]`, pull widths `[1.026, 1.037]`, marginal 68.27% coverage `[0.650, 0.675]`, and joint coverage `0.635`; all passed the predeclared three-sigma sampling checks.
- **Self-contained revision —** The user requested that `make_mock` and its result container move into the notebook; implementation and regression execution are in progress.
- **Self-contained verification —** Inlined `MockSample` and `make_mock`, removed repository path manipulation and the `src.mocks` import, then completed a clean execution. All deterministic, MCMC, and 200-seed outputs matched the prior validated run exactly.

## Session close-out

- **Final status:** completed
- **Accomplished:** Implemented and independently executed the complete self-contained null-systematics recovery notebook, including its mock generator, Astropy kernel check, exact posterior, two MCMC initialisations, diagnostics, exact-posterior comparisons, and repeated-seed calibration checks.
- **Key results and interpretation:** The fitted `H0` remains conditional on fixed `Omega_m`; the free intercept removes absolute formation-time information. The reference posterior gives conditional `H0 = 70.16 +3.67/-3.36 km/s/Mpc` and `H(z=0.819) = 111.08 +5.80/-5.32 km/s/Mpc` from the broad-start chain.
- **Files changed or created:** `notebooks/04_mock_mcmc_recovery.ipynb`; `session_plans/2026-08-09-design-mock-mcmc-recovery.md`.
- **Not completed:** Step 4 systematics experiments; they remain outside this notebook's agreed null-case scope.
- **Plan deviations:** The acceptance-fraction sanity range was widened from an implementation-time `0.20–0.70` check to `0.15–0.80` after the valid low-dimensional chains returned `0.713–0.716`; no predeclared analytic or convergence tolerance changed. The later self-contained revision duplicated the small generator intentionally at the user's request.
- **Decisions made:** Adopted `t_model(z) = (70/H0) g(z) + C` at fixed `Omega_m = 0.3`; left the roadmap unchanged because this session implements, but does not redefine, supervisor step 3.
- **Exact next starting point:** Use the same inference path with one step-4 systematic varied at a time, beginning with a constant age offset to verify that the free intercept absorbs it.
- **Recommended next-session goal:** Implement paired constant-offset mocks and verify unchanged recovered slope/H(z).
