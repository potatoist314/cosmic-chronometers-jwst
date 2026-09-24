# Ceridwen GPU benchmarks

Use `python3 scripts/benchmark.py run "RTX 5090" --spend-cap 1`.
Use `--dry-run` for local preflight without renting. Repeat with the printed
`--output` directory to resume the same source revision and accumulated budget.

Choose the lowest hourly price for the requested GPU type. Require reliability
above 99.5% and upload/download charges each below $10/TB. No hourly cap;
the experiment total cannot exceed $1 including retries.

The command owns setup, cached-grid transfer, measurement, reconnection,
result download, invoice collection and verified teardown. The run manifest
records tried offers and hosts. It excludes active hosts owned by other tasks.
No account-wide cleanup or external cap file is used.

`--help` lists the options. The maintained guide is
`wiki/notes/vast-ai-gpu-workflow.md`. Earlier benchmark evidence remains in
`results/gpu-benchmark-2026-09-23/`; its historical workload is not a new default.
