# Ceridwen GPU benchmarks

Use `python3 scripts/benchmark.py run "RTX 5090" --spend-cap <approved-USD>`.
Use `--dry-run` for local preflight without renting. Repeat with the printed
`--output` directory to resume the same source revision and accumulated budget.

The command owns setup, cached-grid transfer, measurement, reconnection,
result download, invoice collection and verified teardown. The run manifest
records tried offers and hosts. It excludes active hosts owned by other tasks.
No account-wide cleanup or external cap file is used.

`--help` lists the options. The maintained guide is
`wiki/notes/vast-ai-gpu-workflow.md`. Earlier benchmark evidence remains in
`results/gpu-benchmark-2026-09-23/`; its historical workload is not a new default.
