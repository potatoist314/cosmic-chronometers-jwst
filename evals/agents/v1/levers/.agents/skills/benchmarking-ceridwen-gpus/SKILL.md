---
name: benchmarking-ceridwen-gpus
description: Run Ceridwen likelihood throughput benchmarks on Vast.ai with one command. Use for GPU speed and cost comparisons, not full experiment fits.
---

# Benchmark Ceridwen GPUs

New runs use the compact dependency image pinned in `scripts/vast.py`, selected
input files, and cached grids. Do not replace it with a generic CUDA image.
Use `--image` only for an explicitly requested override. Saved runs keep their image.

Run from the project root with the requested GPUs:

```bash
python3 scripts/benchmark.py run "RTX 5090" --spend-cap 1
```

- Offers must have reliability above 99.5% (fall back to above 96% only if no
  offers pass all filters), and upload/download charges each below $10/TB. No hourly price cap.
- The command ranks offers as in the running-ceridwen-experiments skill: host
  record in `scripts/vast_hosts.csv` first (`good`, no row, `poor`), then the lowest
  cost per fit, then the lowest hourly price.
- The experiment cap is $1 including retries; `--spend-cap` can only reduce it.
- Add more GPU names as positional arguments. Use `--hosts 2` for repeated hosts.
- Use `--dry-run` for local preflight without rentals.
- Defaults use committed HEAD, pinned submodules and the verified local grid.
  Commit intended changes first, or select a committed `--revision`.
- Repeat with `--output <printed-directory>` to resume the same task and budget.
  Never manually rent a replacement for a run with an unresolved owned instance.
- The command handles setup, progress, reconnects, results, charges and teardown.
  Report the measured throughput and output directory. This is not time to convergence.
- **Record hosts.** List the hosts that started an instance:
  ```bash
  python3 -c "import json; [print(a['offer']['host_id'], a['offer']['gpu_name'], a['status'], a.get('calls_per_second', ''), a.get('error', '')) for a in json.load(open('<output>/manifest.json'))['attempts'] if a.get('instance_id')]"
  ```
  Add one row for each host to the end of `scripts/vast_hosts.csv`, with the
  columns `host_id,outcome,gpu,date,run,reason`. The latest row sets the outcome.
  - Write `good` when the benchmark finished on the host. Write the measured rate
    in the reason as `<N> calls/s`, for example `finished the benchmark; 27754 calls/s`.
    The ranking reads this value.
  - Write `poor` when the host failed. Examples: the boot stalled, the instance
    became unavailable, or the host closed SSH.
  - Do not add a row for an offer that did not start an instance.
  - Do not add a row for a failure that our code or inputs caused.
  - Do not add a row when the records do not show the cause.
  Commit the new rows.

No historical cap file, agent watchdog, or memory lookup is required.
Experiment fits use the running-ceridwen-experiments skill.

Local SSH errors stop before rental. Use an execution environment authorized to run
SSH; waiting for the GPU cannot fix a local user-ID error. The shared upload
includes HST cutouts and the emission-line table. A nonzero remote stage exit
saves its log, destroys the owned rental and stops. Diagnose the log before
repeating the command; do not rent a replacement for the same code or input error.
