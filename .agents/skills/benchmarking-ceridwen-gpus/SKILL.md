---
name: benchmarking-ceridwen-gpus
description: Use when Liu Hao asks to benchmark Ceridwen likelihood speed on Vast.ai GPUs, or to set hourly price caps per card from measured speed.
---

# Benchmark Ceridwen GPUs

Written from the 2026-09-23 price-matrix run
(`results/gpu-benchmark-2026-09-23/sol/`).
Rules are in `AGENTS.md`, `BENCHMARK_CHECK.md` and memory. Read them. Do not copy them here.

## His words

- "how much faster are 5070ti, 5080, 5090 than 5060 - then assign a price times that multiple for each of them, to maintain same efficiency across different models" (`wiki/research/experiments/e-gpu-price-benchmark.md`, Before delegation, 2026-09-23).
- "be careful with unreliable machines that have issues like loading the images and such - they have a tendency to inflate cost too much" (same source).
- "yes, cheapest cost per unit of work is dominant" (memory `vast-price-rules-are-guards.md`, 2026-09-23).
- "holy shit, change the spend cap, to just pick the cheapest available one that fits availability rules. the rules were never meant to be ironclad, to just prevent a major fuckup" (same memory).
- "better unit is time to convergence i think" (task brief, 2026-09-23).
- "im sure existing benchmark tooling already exists" (task brief, 2026-09-23).

## Read before any paid rental

- `AGENTS.md`: read `BENCHMARK_CHECK.md` first. Compare remaining cost on the host with a fresh rental. Never destroy on elapsed time alone.
- `BENCHMARK_CHECK.md`: tried hosts and offers, failure checks, per-instance invoices.
- Memory `vast-benchmark-methodology.md`: same-boot comparisons only, own instances only, `destroy -y`.
- Memory `vast-price-rules-are-guards.md`: cheapest cost per unit of work, guards, total cap.
- Memory `understand-before-building.md`: reuse the scripts below.

## Steps

1. **Check the cap.** The sweep reads `~/.claude/scripts/workspace-overseers/caps/gpu-bench.json` (`scripts/sweep_ceridwen_vast_gpus.py:854`). The 2026-09-23 cap was $1.50 total.
2. **Rent and measure one host.**
   ```
   python3 -u scripts/sweep_ceridwen_vast_gpus.py price-matrix --max-attempts 1
   ```
   The worker ran this at 20:17 and 20:40 on 2026-09-23. It rented RTX 5070 host 511119 and RTX 5090 host 406325. It clones the pinned tree, uploads inputs, bootstraps CUDA, runs `scripts/benchmark_baked_runtime.py`, pulls the timing JSON and destroys the instance.
3. **Wait for supply when nothing qualifies.** The worker ran `price-matrix --wait-minutes 60 --max-attempts 1`.
4. **Resume a live instance after an SSH drop.** Check remote processes first. The worker resumed instance 52295242 with `price-matrix --attach-instance 52295242 --attach-offer-id 45669144`. It completed on the same box.
5. **Destroy with `-y` and check absence.**
   ```
   vastai destroy instance <id> -y
   vastai show instances
   ```
6. **Count spend from per-instance invoices.**
   ```
   vastai show invoices-v1 --charges --charge-type instance --start-date <day> --end-date <next> --limit 100 --raw
   ```
   Count a resumed instance once. The 2026-09-23 total was $0.981 including failures (`sol/summary.json`).
7. **Record.** Every attempt goes to `results/gpu-benchmark-2026-09-23/sol/manifest.json`. Ratios and caps go to `sol/summary.json`. Raw timings stay in `sol/timing-*.json`. Commit and push.
