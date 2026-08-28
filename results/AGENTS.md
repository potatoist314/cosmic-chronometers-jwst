# Scientific result directories

- Store only fits whose sampler reached its configured convergence condition.
- A clean process exit, checkpoint, or `complete` name does not prove convergence.
- Do not store benchmarks, smoke tests, trials, checkpoints, or incomplete fits here.
- Store pure 5,000-call hardware runs under `benchmarks/ceridwen/runs/`.
- Include the executed analysis notebook with saved final fit, spectrum or SED,
  SFH or age-history, and corner-plot outputs.
- Keep generated reader-facing plot files beside the executed notebook.
- HDF5 posteriors, timing metadata, and logs may accompany these readable outputs.
- Name every top-level result directory for a human reader.
- Use `ceridwen_<environment>_<hardware>_<analysis>_complete_<YYYY-MM-DD>` only
  after convergence.
- Do not use `batch-*`, opaque timestamps, or raw run IDs as directory names.
- Keep exact timestamps and run IDs inside timing JSON or HDF5 metadata.
- Name nested directories by contents, such as `posterior_outputs`.
- Before renaming results, update path references and verify expected files exist.

Example:

- `ceridwen_modal_a100_feature_spectrum_complete_2026-08-25`
