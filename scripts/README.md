# Scripts

## Shared modules (imported, not run)

| script | does |
|---|---|
| spectral_figures.py | Shared absorption-feature marking for every figure with a wavelength axis. |
| per_galaxy_diagnostics.py | Per-galaxy chi-squared and star-formation-timescale diagnostics for Ceridwen fits. |
| absorption_mask_analysis.py | Analysis helpers for the absorption-line pixel-mask experiment. |

## Production run

| script | does |
|---|---|
| run_ceridwen_vast_multi_gpu.py | Run a deterministic Ceridwen DR2 target shard on one Vast GPU. |
| bootstrap_vast_ai.sh | Build the CUDA JAX environment on a fresh Vast box. |
| build_dr2_quiescent_summary.py | Build a tidy one-row-per-galaxy summary of the DR2 quiescent run. |
| build_borghi2022_legac_dr2_subset.py | Join Borghi et al. (2022) Table 4 to matching LEGA-C DR2 spectra. |

## Vast drivers (rent a GPU, run an experiment, pull results)

| script | does |
|---|---|
| calibration_arms_vast.py | Run the single-fit accuracy arms. |
| absorption_mask_vast.py | Run the absorption-mask grid. |
| absorption_mask_grid.py | Run the absorption-line pixel-mask experiment as a grid of notebook fits. |
| absorption_mask_report.py | Summarise the absorption-mask experiment: tables and figures. |
| per_galaxy_diagnostics_vast.py | Verify the per-galaxy diagnostics on one Vast.ai RTX 5060. |
| benchmark_ceridwen_vast.py | Run and compare short, fixed Ceridwen GPU benchmarks on Vast.ai. |
| sweep_ceridwen_vast_gpus.py | Rent one Vast.ai GPU per model. |
| validate_ceridwen_speedups.py | Measure complete production NSS fits. |
| watch_claude_vast_benchmarks.zsh | Poll the Herdr pane that runs the Vast GPU benchmarks. |

## Figures

| script | does |
|---|---|
| plot_dr2_stacked_pull.py | Stacked pull diagnostics for large DR2 runs. |
| plot_dr2_distributions_quality.py | Sample distributions and fit-quality panels for the DR2 quiescent run. |
| plot_dr2_formation_timescale.py | Formation-timescale (delta-t) plots for the DR2 quiescent sample. |
| plot_sfms_quiescent.py | Star-forming sequence for the DR2 quiescent runs. |
| plot_borghi2022_age_vs_z.py | Recreate Borghi+2022a Fig. 9 (median age vs redshift) with our sample. |
| plot_ceridwen_checkpoint_evolution.py | Build a standalone Ceridwen checkpoint spectrum animation. |

## Data download and serving

| script | does |
|---|---|
| download_legac_dr2_spectra.py | Download the LEGA-C DR2 1D spectra listed in the DR2 catalogue. |
| download_legac_dr2_aperture_photometry.py | Download multi-aperture COSMOS2015 and total UltraVISTA photometry for LEGA-C DR2. |
| download_cosmos2015_legac_dr2_photometry.py | Download COSMOS2015 photometry matched to the LEGA-C DR2 catalogue. |
| download_hst_cutouts.py | Download HST ACS F814W cutouts for the production DR2 quiescent targets. |
| serve_wiki.py | HTTP server for the Astro lab notebook and the project deliverables. |
| build_ceridwen_results_board.py | Build the Ceridwen common results board from the validated audit manifest. |

## Notes

- `scripts/` is a plain directory, not a package; callers add it to `sys.path`.
- `sweep_ceridwen_vast_gpus.py`’s `BENCHMARK_SCRIPT_SHA256` no longer matches `benchmark_ceridwen_vast.py`; the sweep pins commit `63b4296` for the benchmark.
- Inactive scripts live in `archive/scripts/`; see `archive/README.md`.