# Session: Review the MilesPy inference section for simplification

- **Date:** 2026-08-03
- **Project phase:** Step 2, Lick-index age inference sub-project
- **Session status:** completed
- **Primary goal:** Identify a simpler, scientifically trustworthy learning path through the cells after the first `line_strength_index(...)` forward calculation in `notebooks/02_differential_ages.ipynb`.

## Why this session matters

The current post-forward-model section was added externally and is difficult for the user to read. The inference should expose the physical sequence—model parameters to predicted indices to likelihood—before introducing performance optimizations or MCMC.

## Starting point

- **Last verified state:** The saved notebook was inspected read-only. Cell 33 constructs one V15 SSP and measures the baseline Lick indices; cells 34 onward begin a partly commented prior and a vectorized `RegularGridInterpolator` setup.
- **Relevant files or notebook sections:** `notebooks/02_differential_ages.ipynb`, from the code beginning `mask = (~np.isnan(V15.models.meta['alpha']))` onward; `session_plans/PROJECT_ROADMAP.md` Step 2.
- **Inputs and provenance:** alpha-MILES/V15 through `milespy`; Borghi 2022a Appendix C/Table 6 index combinations; the project roadmap's agreed Gaussian independent-index likelihood.
- **Open question or uncertainty:** Which abstractions and optimizations are genuinely required before the user can understand and validate a one-galaxy age fit?

## Definition of done

Produce an evidence-based review that identifies correctness problems, explains the minimum conceptual pipeline, and proposes a smaller cell sequence. Do not edit scientific implementation cells without explicit authorization.

## Scope

- **In scope:** Readability, dependency order, unnecessary abstraction, scientific checks, and bugs in cells after the shown forward-model cell.
- **Out of scope:** Editing the notebook, running a full per-galaxy MCMC, reproducing Figure 2, or changing the agreed roadmap.

## Planned tasks

### 1. Trace the post-forward-model code

- **Status:** completed
- **Purpose:** Determine what every later cell contributes to the eventual likelihood.
- **Work:** Inspect all saved cells and outputs after the cutoff, including incomplete code and dependencies.
- **Expected artifact:** A dependency-ordered map of essential versus premature work.
- **Trustworthiness check:** Each retained step must connect model parameters and measured indices to a dimensionally and statistically valid likelihood.

### 2. Challenge the proposed simplification

- **Status:** completed
- **Purpose:** Avoid replacing complicated code with an easier but scientifically invalid shortcut.
- **Work:** Request a configured Claude Opus 5 `brutal` review, then compare it with the inspected notebook.
- **Expected artifact:** A concise recommended cell structure with disagreements or caveats surfaced.
- **Trustworthiness check:** Preserve the grid bounds, alpha-grid limitation, index units, observational errors, and velocity-dispersion prerequisite.

### 3. Close the review

- **Status:** completed
- **Purpose:** Give the user an actionable next step without implementing for them.
- **Work:** Rank changes by impact and record the exact restart point.
- **Expected artifact:** Review findings in chat and a completed session close-out.
- **Trustworthiness check:** Distinguish inspected evidence from proposals; make no completion claim about the inference itself.

## Predictions before calculation

The full 17-index interpolator is probably useful only as a later speed optimization. A single-index-combination forward function and one-galaxy likelihood should make the science visible before MCMC or multi-combination batching.

## Working log

- **Start —** Inspected repository status, roadmap, plan conventions, and saved notebook cells through the first part of the interpolation-grid construction. The notebook is already modified; no implementation edits are authorized in this review.
- **Review —** Inspected all saved cells after the cutoff. Only the 3-D grid-construction cell has saved output; the velocity-broadening, fitting, sample loop, and age-redshift regression cells are unexecuted.
- **Method check —** Inspected Borghi 2022a Sections 3.2-3.3 and Appendices B-C, Borghi 2022b Section 3.1/Figure 2, and the local LEGA-C DR2 catalog. The paper requires one fixed complete index set per fit and posterior reliability screening. The notebook instead permits any four finite indices and selects 372 unique candidates; only 243 have every baseline catalog index. Its public-catalog/model-broadening route is an explicitly different baseline from Borghi's remeasured, zero-dispersion-corrected indices.
- **Simplification —** A direct likelihood over the native 53 x 12 x 2 model grid provides a transparent deterministic benchmark before interpolation or MCMC. The velocity-dispersion effect should first be demonstrated on one spectrum and one galaxy before constructing a 4-D cache.
- **External review —** Claude Opus 5 at xhigh effort completed a `brutal` review. It agreed that the native-grid likelihood should replace the current interpolation/MCMC section here, while retaining model broadening. It additionally identified that the current fit permits redshift-dependent missing-index subsets, skips the paper's posterior-reliability rejection, pools the two velocity-dispersion populations, and does not fully seed `emcee`.

## Session close-out

- **Final status:** completed
- **Accomplished:** Reviewed every post-cutoff cell, checked the relevant paper methods and local catalog structure, verified the saved execution state, and obtained the required external critical review.
- **Key results and interpretation:** The section is over-engineered and not yet scientifically safe. The simplest trustworthy route is: baseline-only flat model table; index-versus-age diagnostic; one-galaxy broadening demonstration; direct native-grid likelihood and marginalized posterior; recovery/published-age validation; only then fixed-set sample fitting and `H(z)`. Require the complete combo per galaxy, screen posterior reliability, and retain separate low/high velocity-dispersion relations.
- **Files changed or created:** `session_plans/2026-08-03-review-milespy-inference-section.md`
- **Not completed:** No notebook implementation cells were edited or executed; changes require the user's explicit authorization.
- **Plan deviations:** None.
- **Decisions made:** Recommend replacing the current post-cutoff pipeline rather than incrementally explaining it. Preserve the absence of a cosmological age prior, the unweighted regression choice, and forward broadening of the model spectra.
- **Exact next starting point:** Replace cell 34's dead commented prior and cell 35's 17-index interpolator with a baseline-only `(1272, 10)` native model-index table, then plot a few index responses to age before writing a likelihood.
- **Recommended next-session goal:** Implement and validate the one-galaxy native-grid posterior through a synthetic recovery check, without scaling to the full sample.
