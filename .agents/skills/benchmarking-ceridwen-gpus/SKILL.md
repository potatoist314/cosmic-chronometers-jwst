---
name: benchmarking-ceridwen-gpus
description: Run Ceridwen likelihood throughput benchmarks on Vast.ai with one command. Use for GPU speed and cost comparisons, not full experiment fits.
---

# Benchmark Ceridwen GPUs

Run from the project root with the requested GPUs:

```bash
python3 scripts/benchmark.py run "RTX 5090" --spend-cap 1
```

- Choose the lowest hourly price for each requested GPU type, reliability above
  99.5% (fall back to above 96% only if no offers pass all filters), and upload/download charges each below $10/TB. No hourly price cap.
- The experiment cap is $1 including retries; `--spend-cap` can only reduce it.
- Add more GPU names as positional arguments. Use `--hosts 2` for repeated hosts.
- Use `--dry-run` for local preflight without rentals.
- Defaults use committed HEAD, pinned submodules and the verified local grid.
  Commit intended changes first, or select a committed `--revision`.
- Repeat with `--output <printed-directory>` to resume the same task and budget.
  Never manually rent a replacement for a run with an unresolved owned instance.
- The command handles setup, progress, reconnects, results, charges and teardown.
  Report the measured throughput and output directory. This is not time to convergence.

No historical cap file, agent watchdog, or memory lookup is required.
Experiment fits use the running-ceridwen-experiments skill.

Local SSH errors stop before rental. Use an execution environment authorized to run
SSH; waiting for the GPU cannot fix a local user-ID error. The shared upload
includes HST cutouts and the emission-line table. A nonzero remote stage exit
saves its log, destroys the owned rental and stops. Diagnose the log before
repeating the command; do not rent a replacement for the same code or input error.
