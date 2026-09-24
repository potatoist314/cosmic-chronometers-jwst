---
title: GPU benchmark 2026-09-23: failures and fixes
date: 2026-09-23
section: Guides
theme: Compute
tags: [gpu, vast-ai, benchmark]
---

Batched likelihood, current code, 2026-09-23.

| Card | Speed (x RTX 5060 Ti) | Price paid ($/h) | Cost per unit of work ($/h / speed) |
| --- | ---: | ---: | ---: |
| RTX 5060 Ti | 1.00 | 0.17-0.20 | 0.17-0.20 |
| RTX 5070 | 1.33 | 0.21 | 0.16 |
| RTX 5080 | 2.39 | 0.35 | 0.15 |
| RTX 5090 | 4.49 | 0.49-0.55 | 0.11-0.12 |

What went wrong in the 2026-09-23 GPU price benchmark and what fixed it. Record: `wiki/research/experiments/e-gpu-price-benchmark.md`. Results: `results/gpu-benchmark-2026-09-23/`.

<details>
<summary>Price caps</summary>

- Hard price caps blocked GPU rentals. Caps $0.11/h and $5/TB left no qualifying supply 14:33-15:48; first rental 15:48, first measurement 16:06 (`driver.log:3-10`, `24`, `286-287`, `387`). Fix: caps are loose guards ($0.40/h, $25/TB); rent cheapest cost per unit of work (memory `vast-price-rules-are-guards.md`; `scripts/sweep_ceridwen_vast_gpus.py:59-84`; commit `0ee5c05`).

</details>

<details>
<summary>Driver</summary>

- A new driver crashed. First worker wrote `scripts/bench_gpu_prices_vast.py` instead of the existing scripts (`BENCHMARK_CHECK.md:4-6`). It retried gone offer 48484148 eleven times: nine empty replies, then HTTP 400, then 410 (`driver.log:127-259`; eleven `vast_fail` files). It crashed writing summary twice: missing shlex import (`driver.log:297-320`), None price cap (`driver.log:398-411`). Fix: use the existing sweep; never retry a gone offer (`BENCHMARK_CHECK.md:26`, `29`).

</details>

<details>
<summary>SSH waits</summary>

- Hosts without SSH died on a fixed timer. Hosts 166757 and 605466 died at the 8-minute SSH wait (`driver.log:393-397`). Fix: compare remaining cost with a fresh rental instead (`AGENTS.md:72-77`; `BENCHMARK_CHECK.md:8`).

</details>

<details>
<summary>Units</summary>

- Batched calls/s is not fit throughput. Timing files show 27,754-148,930 calls/s (`sol/summary.json`). A real fit does about 9,450 calls/s (`eline_off` `ns_progress.jsonl` tail: 8,424,501 calls, 891 s). The fixed NSS workload does 5,042 calls/s on RTX 5060 (`benchmark.json` timings). Liu Hao: "better unit is time to convergence i think" (task brief 2026-09-23).

</details>

<details>
<summary>Host spread</summary>

- Speed varies between hosts. RTX 5090: 94,294 vs 148,930 calls/s (`sol/summary.json:48-66`). One host swung 66% across boots before (`vast-benchmark-methodology.md:13`). Liu Hao: "it boggles the mind how it can vary so much. something must be wrong" (diagnostic brief, pane `gpu-bench-sol`, 2026-09-23).
- Diagnostic on 5090 host 622869: 150,937 calls/s at batch 500 with 96% GPU use; dispatch 0.196 ms of a 3.224 ms call; plateau through batch 8,000. CPU dispatch not the bottleneck there; the slow host stays unexplained (`diagnostic/summary.json`; pane `gpu-bench-sol`; commit `646dfb1`).

</details>

<details>
<summary>Spend</summary>

- Spend counters were account-wide. `matrix.json` repeats credit 9.739 across failures; other jobs shared the account. Fix: per-instance invoices; $0.981 total incl. failures (`sol/summary.json:73-96`; `BENCHMARK_CHECK.md:10`).

</details>
