# Archive

Everything here was moved with `git mv` on 2026-09-10, with contents untouched. Nothing here is imported or run by the active Ceridwen pipeline. History is under the old path via `git log --follow`.

## scripts

- `scripts/modal_ceridwen.py` – Modal GPU runner replaced by Vast.
- `scripts/refit_static_smoothing_vast.py` – Superseded static-smoother refits.
- `scripts/ab_loglike_ceridwen.py` – Log-likelihood A/B benchmark.
- `scripts/plot_dr2_headline_candidates.py` – Headline-figure layout bake-off.
- `scripts/backfill_hst_cutout_cell.py` – One-off notebook cell backfill.
- `scripts/wiki_convert_html_to_notes.py` – One-off HTML to notes conversion.

## notebooks

- `notebooks/03_sed_fitting_AI_written.ipynb` – Prospector-era SED fitting notebook.
- `notebooks/03_sed_fitting_prospector.ipynb` – Prospector-era SED fitting notebook.
- `notebooks/ceridwen_feature_spectrum_posterior_report.ipynb` – Modal feature-spectrum report.
- `notebooks/figures/` – PNGs for the Modal feature-spectrum report.
- `notebooks/practice/` – Fits-viewer practice notebook.

## src

- `src/lick_inference.py` – Lick-index inference from the inactive branch.

## session_plans

- `session_plans/` – Twelve dated plans plus `PROJECT_ROADMAP.md`, `README.md`, and `TEMPLATE.md`.

## results

- `results/a100-feature-spectrum/` – Modal A100 feature-spectrum run.
- `results/a100-integrated-fit-notebook/` – Modal A100 integrated-fit notebook run.
- `results/rtx-5090-integrated-fit/` – Single integrated fit.
- `results/calibration-polynomial-2026-09-02/` – Local calibration snapshots superseded by `results/calibration-polynomial-dr2`.
- `results/refit-static-smoothing/` – Static-smoother refits.

## Still in results/ but superseded

- `results/rtx-5060-dr2-quiescent-full-spectrum` – Pinned by `tests/test_chronometer.py`.
- `results/rtx-4070-super-four-galaxy-fits` – Pinned by `tests/test_plot_ceridwen_checkpoint_evolution.py`.
- `results/rtx-5060-production-speedup` – `RESULT_ROOT` of `scripts/validate_ceridwen_speedups.py`.