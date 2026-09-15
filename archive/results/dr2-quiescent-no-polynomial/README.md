# DR2 quiescent run without a calibration polynomial

Archived at `archive/results/dr2-quiescent-no-polynomial`.
Moved from `results/rtx-5060-dr2-quiescent-full-spectrum` on 2026-09-15 with `dr2-quiescent-summary.csv`.
Run on 2026-08-30: 187 LEGA-C DR2 quiescent galaxies, two Vast.ai RTX 5060 GPUs.
One folder per target: `ceridwen_result.h5`, `ceridwen_derived_outputs.h5`, executed notebook, `execution.log`, `diagnostics/`.
Configuration: no calibration polynomial (spectrophotometric calibration order 0), aperture photometry, dust index fixed at -0.7.
Superseded on 2026-09-07 by `results/dr2-quiescent-new-defaults`.
Replacement: marginalised order-3 calibration polynomial, `cosmos_total` photometry, free dust index, Student-t SFH prior.
Same 187 galaxies and seeds; replacement log-evidence higher for all 187.
Without the polynomial, the model cannot absorb the DR2 continuum-shape mismatch; ages, metallicities and dust are not trustworthy.
Kept only as the old side of the comparison in `results/dr2-quiescent-new-defaults/ceridwen_new_defaults_comparison.ipynb` and `wiki/notes/dr2-new-defaults.md`.
Do not use this run for new results.
Trace Git history with `git log --follow`.