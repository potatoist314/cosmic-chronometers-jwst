# Session: Audit the 243-versus-140 sample difference

- **Date:** 2026-08-03
- **Project phase:** Step 2, Lick-index age inference sub-project
- **Session status:** completed
- **Primary goal:** Identify the exact Borghi selection or fitting criteria absent from the notebook that increase the fitted baseline sample from 140 to 243 galaxies.

## Why this session matters

The new MCMC result cannot be compared directly with Borghi's V15 summary unless both analyses use the same galaxies and reliability criteria.

## Starting point

- **Last verified state:** The live notebook completed 243 of 243 baseline fits with no worker failures; the fitted-sample median age was 2.87 Gyr.
- **Relevant files or notebook sections:** `notebooks/02_differential_ages.ipynb`; Paper I Sections 2-3 and appendices; Paper II Appendix A; processed 140-object match table.
- **Inputs and provenance:** LEGA-C DR2 catalogue, COSMOS2015 match, Borghi Paper I selection and posterior-quality rules, and `data/processed/borghi2022_legac_dr2/`.
- **Open question or uncertainty:** Whether the difference comes from sample selection before fitting, rejected/edge posterior fits after fitting, repeat spectra, or a combination.

## Definition of done

Record both count pipelines with paper citations or inspected code and identify the first criterion that explains the divergence. Distinguish selection cuts from fit-quality exclusions.

## Scope

- **In scope:** Read-only audit of the paper, notebook, and local catalogues; exact object-count comparisons.
- **Out of scope:** Editing the scientific notebook, rerunning MCMC, or changing the roadmap.

## Planned tasks

### 1. Reconstruct Borghi's count pipeline

- **Status:** completed
- **Purpose:** Establish how Paper I reaches 140 published age measurements.
- **Work:** Extract every stated selection and posterior-reliability cut with intermediate counts.
- **Expected artifact:** Evidence-backed Borghi count sequence.
- **Trustworthiness check:** Separate parent/passive selection from failed or boundary-constrained fits.

### 2. Compare the notebook pipeline and object IDs

- **Status:** completed
- **Purpose:** Locate the missing or changed step.
- **Work:** Reproduce the notebook's 372 selected and 243 complete-baseline counts; compare them with the processed 140-object list.
- **Expected artifact:** Exact explanation of the 103 extra fitted objects.
- **Trustworthiness check:** Deduplicate by `OBJECT` and distinguish spectra from galaxies.

## Predictions before calculation

The notebook likely stops after passive-galaxy and complete-index cuts, whereas Borghi publishes only galaxies whose TMJ11 posteriors pass additional reliability or model-grid boundary criteria.

## Working log

- **Start —** Live VS Code output inspected read-only: 243 baseline fits completed in 268 seconds; no worker failures. The paper comparison uses 140 galaxies, so the samples are not yet like-for-like.
- **Borghi pipeline —** Paper I Table 1 and Sections 2.2/3.3 report 1622 parent sources, 658 photometric passive, 485 spectrophotometric passive, and 350 after visual emission-line inspection. Requiring one homogeneous baseline index set leaves 199 analyzed galaxies. Appendix B then excludes 59 posteriors that are prior-boundary-skewed, non-predictive/degenerate, or multimodal, leaving 140 robust constraints.
- **Notebook pipeline —** Reproduced the saved notebook cuts directly from the local LEGA-C and COSMOS files: 1617 parent spectra, 666 photometric, 492 spectrophotometric, 381 spectra after the automated emission-line S/N cut, 372 unique best-S/N objects, and 243 with finite positive errors for all ten public-DR2 baseline indices.
- **Object audit —** Of Borghi's 140 published objects, only 125 occur in the notebook's 243. Ten are removed by the notebook's automated OII/OIII S/N cut even though Borghi retained them after visual inspection; five lack a complete public-DR2 baseline vector selected by the notebook. Conversely, 118 notebook objects are not in Borghi's published 140.
- **Interpretation —** Worker success is not Borghi posterior reliability. The notebook fits all 243 eligible public-index objects and reports `tau_max`, but does not apply Borghi's formal convergence and manual posterior-shape exclusions. Borghi also measured indices from the spectra with PyLick rather than using the public DR2 catalogue values.

## Session close-out

- **Final status:** completed
- **Accomplished:** Reconstructed both count pipelines and compared the final object IDs against Borghi's published 140-object table.
- **Key results and interpretation:** Borghi's sequence is 350 selected, 199 fitted with the baseline indices, and 140 retained after posterior inspection. The notebook's sequence is 372 unique automated selections and 243 complete public-index fits. Only 125 objects overlap, so the 2.87 Gyr notebook median is not a like-for-like reproduction of Borghi's V15 mean.
- **Files changed or created:** `session_plans/2026-08-03-audit-borghi-sample-selection-4.md`
- **Not completed:** No notebook change was made. Reproducing the V15 summary still requires an agreed handling of the 15 published objects absent from the notebook sample and an explicit posterior-reliability rule.
- **Plan deviations:** None.
- **Decisions made:** Treat `fit_problems` as execution failures only, not as a convergence or scientific-quality filter.
- **Exact next starting point:** Build a count-only comparison using Borghi's published 140 IDs: 125 currently have complete notebook fits, ten fail the automated line cut, and five fail the public-index completeness requirement.
- **Recommended next-session goal:** Decide whether the target is Borghi's exact 140-object V15 rerun or an explicitly labelled public-DR2 analogue, then make the sample definition match that target.
