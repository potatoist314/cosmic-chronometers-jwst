# Session: Make the one-galaxy fit diagnostic explicit

- **Date:** 2026-08-03
- **Project phase:** Step 2, Lick-index age inference sub-project
- **Session status:** completed
- **Primary goal:** Rewrite the `best_parameters` cell so it clearly distinguishes computational completion, parameter estimates, measurement errors, and goodness of fit.

## Why this session matters

The existing residual table is mathematically useful but its names make large pulls look like parameter errors, and it does not report the poor overall chi-squared.

## Starting point

- **Last verified state:** Object 207825's minimum native-grid chi-squared is 127.75 for ten indices and three fitted parameters; its largest pull is 6.04.
- **Relevant files or notebook sections:** `notebooks/02_differential_ages.ipynb`, markdown cell `47db735e` and code cell `a65ad168`.
- **Inputs and provenance:** The direct native-grid likelihood immediately above the diagnostic; Borghi Equation 7's independent Gaussian-index assumption.
- **Open question or uncertainty:** None; this is a clarity and diagnostic-output change.

## Definition of done

The cell selects the minimum-chi-squared grid model explicitly, labels measurement errors unambiguously, prints chi-squared, degrees of freedom, and reduced chi-squared, and retains the per-index pull table. Notebook JSON and all code cells must parse.

## Scope

- **In scope:** The explanatory markdown and one diagnostic code cell.
- **Out of scope:** Changing the likelihood, MCMC worker, model grid, sample, or scientific acceptance threshold.

## Planned tasks

### 1. Rewrite and verify the diagnostic

- **Status:** completed
- **Purpose:** Make the cell's role and failure signal immediately understandable.
- **Work:** Rename variables and columns, use `argmin(chi2)`, calculate chi-squared per degree of freedom, and verify the original numerical result is preserved.
- **Expected artifact:** One clearer markdown/code pair in the notebook.
- **Trustworthiness check:** Recover age 2.0 Gyr, chi-squared 127.75, seven degrees of freedom, and reduced chi-squared about 18.25 for the same galaxy.

## Predictions before calculation

The selected row should remain 594 because the previous maximum-posterior-mass cell was also the minimum-chi-squared cell for this galaxy.

## Working log

- **Start —** Inspected the notebook and worker. The whole-sample runner records posterior quantiles and autocorrelation time but no goodness-of-fit statistic; `243/243 completed` therefore means execution success only.
- **Implementation —** Replaced `best_parameters` with `best_model_parameters`, selected the explicit minimum-chi-squared native-grid row, renamed the table columns to `observed`, `measurement_error`, and `model_prediction`, and added chi-squared, degrees of freedom, and reduced chi-squared outputs.
- **Verification —** Executed the notebook in memory through the revised cell. It preserved row 594 and parameters `(age, [Z/H], [alpha/Fe]) = (2.0, 0.15, 0.0)`, and now reports chi-squared 127.75 for seven degrees of freedom, reduced chi-squared 18.25.

## Session close-out

- **Final status:** completed
- **Accomplished:** Made the one-galaxy diagnostic self-explanatory and exposed its absolute goodness of fit.
- **Key results and interpretation:** The implementation change does not alter the chosen model. It makes visible that the example's apparently plausible age accompanies an unacceptable reduced chi-squared of 18.25.
- **Files changed or created:** `notebooks/02_differential_ages.ipynb`; `session_plans/2026-08-03-improve-fit-diagnostic-5.md`.
- **Not completed:** Diagnosing the physical or data-processing source of the poor fit remains outstanding.
- **Plan deviations:** None.
- **Decisions made:** Treat this cell as a native-grid goodness-of-fit check, not as a summary of the whole-sample MCMC.
- **Exact next starting point:** Compare the public-DR2 indices and forward-broadened MILES predictions for object 207825, beginning with CN1 and H-gamma-A.
- **Recommended next-session goal:** Determine whether the large pulls originate in index conventions, resolution handling, or missing model/systematic variance.
