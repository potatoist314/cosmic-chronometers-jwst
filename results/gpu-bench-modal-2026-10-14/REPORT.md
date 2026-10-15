# Modal datacentre GPU benchmark, 2026-10-14

- Every Modal datacentre GPU type was measured on one build (`ce9752c`): the same M1_210210 fit and seed, 4 containers × 2 fits per card, 88 fits.
- Sampling speed relative to L40S: B200 3.5×, H200 3.0×, H100 2.9×, A100-80GB 1.9×, A100-40GB 1.8×, RTX PRO 6000 1.35×, B300 1.0×, A10 0.42×, L4 0.39×, T4 0.12×. Container-to-container spread is 1–12% (Vast was 66%).
- **Cheapest card per fit: A100-40GB** ($0.063 of sampling; $0.149 for a one-fit container). H100 and A100-80GB cost 11–12% more per sampled fit. B300 costs 3.4× L40S per fit because it samples no faster than L40S.
- The cards agree: fits that take the same sampler path match to float rounding on every card. Across the 7 paths seen, ln Z spans 0.61 (median σ 0.24), and posterior medians vary by at most 0.44σ.
- The same-build RTX 5090 fit (Vast, DR2 refit) is 1.53× L40S. The older consumer table (e-gpu-price-benchmark) is a different build and workload, so it cannot be tied.

## Relative speed and cost per fit

Reference: **L40S**, chosen before the run. Modal's GPU guide calls it the "suggested starting point" (48 GB). It sits mid-price ($1.95/h for the GPU), and it is the example card of the `modal-gpu` backend.

| Card | Relative sampling speed (median; container range) | Relative cost per fit, sampling | Relative cost per fit, one-fit container | Sampling s, median (range), 8 fits | Calls/s | $/h | $/fit, sampling | $/fit, one-fit container |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| B200 | 3.53 (3.49–3.55) | 0.84 | 1.77 | 50.3 (48.2–52.1) | 106,468 | 6.47 | 0.0904 | 0.2851 |
| H200 | 2.96 (2.90–3.06) | 0.74 | 1.40 | 60.0 (56.9–61.6) | 89,821 | 4.76 | 0.0793 | 0.2247 |
| H100 (`H100!`) | 2.91 (2.74–3.08) | 0.66 | 1.14 | 61.1 (56.4–66.3) | 88,206 | 4.17 | 0.0708 | 0.1832 |
| A100-80GB | 1.91 (1.84–2.01) | 0.65 | 1.12 | 92.8 (87.0–96.5) | 57,426 | 2.72 | 0.0701 | 0.1796 |
| **A100-40GB** | 1.82 (1.70–1.87) | **0.59** | **0.93** | 97.8 (94.8–105.2) | 54,418 | 2.32 | **0.0631** | **0.1489** |
| RTX PRO 6000 | 1.35 (1.28–1.39) | 1.11 | 1.30 | 131.2 (127.4–138.6) | 40,834 | 3.25 | 0.1185 | 0.2087 |
| B300 | 1.00 (1.00–1.01) | 3.36 | 3.94 | 177.2 (173.7–178.2) | 30,244 | 7.32 | 0.3603 | 0.6329 |
| L40S | 1.00 (0.99–1.03) | 1.00 | 1.00 | 177.6 (171.5–179.6) | 30,233 | 2.17 | 0.1072 | 0.1607 |
| A10 | 0.42 (0.41–0.46) | 1.45 | 1.19 | 423.3 (389.4–429.8) | 12,688 | 1.32 | 0.1557 | 0.1916 |
| L4 | 0.39 (0.39–0.40) | 1.19 | 1.07 | 450.0 (447.6–454.9) | 11,893 | 1.02 | 0.1277 | 0.1712 |
| T4 | 0.12 (0.12–0.12) | 3.10 | 2.24 | 1470.3 (1457.9–1537.3) | 3,603 | 0.81 | 0.3319 | 0.3594 |

- Sampling time is the nested-sampling wall time (`wall_time_s` in `ceridwen_result.h5`). JIT compile is not included.
- Relative speed = L40S median sampling time / card median. The range uses each container's mean, min to max over the 4 containers.
- $/h = Modal's per-second GPU price + 2 CPU cores + 16 GiB memory (the `modal_gpu` container request). All prices are from https://modal.com/pricing, read 2026-10-14, and agree with `modal billing rates`.
- One-fit container = setup + grid read + bootstrap + one full fit stage (notebook start to finish) + packing. Queue wait is not included.
- Sampler paths differ by up to 1.7% in likelihood calls (below). Relative calls/s agrees with relative sampling speed to 0.02 on every card (`relative_calls_per_s` in `summary.json`).

## Stages (medians over containers or fits)

| Card | Queue s | Boot s | Unpack + grid s | Bootstrap s | Model + grid cell s | JIT compile s | Sampling s | Post-fit cells s | Retrieval s |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| B200 | 1668 | 7.3 | 1.6 | 25.7 | 15.4 | 19.9 | 50.3 | 17.5 | 3.5 |
| H200 | 953 | 7.4 | 1.6 | 23.5 | 18.3 | 19.9 | 60.0 | 15.4 | 3.6 |
| H100 | 1432 | 3.4 | 1.6 | 17.8 | 17.6 | 18.2 | 61.1 | 15.0 | 1.6 |
| A100-80GB | 1996 | 3.7 | 3.6 | 29.8 | 23.7 | 26.9 | 92.8 | 22.3 | 2.2 |
| A100-40GB | 446 | 5.0 | 3.0 | 25.8 | 22.9 | 24.8 | 97.8 | 20.7 | 2.3 |
| RTX PRO 6000 | 1676 | 3.2 | 1.0 | 14.6 | 12.6 | 25.1 | 131.2 | 17.8 | 2.2 |
| B300 | 1738 | 3.4 | 1.7 | 28.6 | 22.2 | 22.8 | 177.2 | 21.3 | 2.1 |
| L40S | 1751 | 2.9 | 1.7 | 16.2 | 13.9 | 17.6 | 177.6 | 17.0 | 1.8 |
| A10 | 591 | 4.8 | 1.7 | 16.8 | 14.3 | 18.0 | 423.3 | 17.7 | 2.6 |
| L4 | 2021 | 5.2 | 3.3 | 26.4 | 24.0 | 30.1 | 450.0 | 27.1 | 2.0 |
| T4 | 61 | 5.2 | 2.9 | 24.1 | 18.8 | 19.0 | 1470.3 | 13.8 | 6.0 |

- Container start = queue + boot. Queue runs from spawn to function entry, minus boot. Boot is sandbox uptime at entry (`/proc/uptime`).
- The workspace ran about 10 GPU containers at once across all apps. hillclimb used 3–5 of them, so queue waits reflect this account's limit on the night, not Modal's GPU supply.
- Bootstrap installs the pinned source into the image environment. "Model + grid cell" is notebook cell 8 (model build and grid load). Retrieval is packing to the archive arriving on the Mac.

## Spread

| Card | Container spread, (max − min)/median of container means | Largest fit-0 vs fit-1 difference in one container |
| --- | ---: | ---: |
| B200 | 1.6% | 7.9% |
| H200 | 5.3% | 4.3% |
| H100 | 11.8% | 4.7% |
| A100-80GB | 8.8% | 3.1% |
| A100-40GB | 9.5% | 4.0% |
| RTX PRO 6000 | 8.3% | 3.2% |
| B300 | 1.3% | 2.0% |
| L40S | 4.1% | 0.9% |
| A10 | 9.2% | 0.4% |
| L4 | 1.2% | 1.0% |
| T4 | 5.4% | 0.2% |

- On A100-40GB, the two containers that compiled faster (about 21 s against 29–31 s) also sampled about 9% faster (95 s against 100–105 s).
- Modal's `A10` type gave 3 NVIDIA A10 (150 W) containers and 1 NVIDIA A10G (300 W) container. The A10G sampled 8% faster (390 s against 423–430 s).
- One L40S container reported 49,140 MiB instead of 46,068 MiB. It sampled 3.5% faster (171.5 s).
- Drivers were 610.57.04, except 2 A10 containers and one container each on H100, B200 and B300, which had 580.95.05 (`hardware.txt`).

## Agreement across cards

| Likelihood calls (sampler path) | ln Z | Fits per card |
| ---: | ---: | --- |
| 5,297,129 | 236003.6016 | T4 8 |
| 5,319,472 | 236003.5798 | A100-80GB 3, A100-40GB 5, L40S 2 |
| 5,333,420 | 236003.8137 | L4 1 |
| 5,335,119 | 236003.6177 | A100-80GB 5, A100-40GB 3 |
| 5,355,535 | 236003.2691 | B200 7, H200 1, H100 1, RTX PRO 6000 8, B300 6 |
| 5,369,047 | 236003.7051 | L40S 1, A10 3 |
| 5,370,929 | 236003.7049 | L40S 5, A10 5, L4 7 |
| 5,386,004 | 236003.2025 | B200 1, H200 7, H100 7, B300 2 |

- On one path, ln Z agrees to 4×10⁻⁹ and posterior medians agree to 2.4×10⁻¹³ (relative), across cards and containers. That is float rounding.
- The path is not fixed per card. It can change between containers, and between the two fits in one container (A100-40GB, A10, B200, H100, L4).
- Across paths, ln Z spans 236003.2025–236003.8137 (0.61). The median ln Z error is 0.24.

| Parameter | Median of the 88 fit medians | Range of fit medians | Median 1σ half-width | Range / half-width |
| --- | ---: | ---: | ---: | ---: |
| logmass | 11.4601 | 11.4539 – 11.4666 | 0.0289 | 0.44 |
| logzsol | -0.1180 | -0.1220 – -0.1168 | 0.0296 | 0.18 |
| afe | 0.1322 | 0.1301 – 0.1334 | 0.0144 | 0.23 |
| diffuse_tau_noll | 0.3233 | 0.3215 – 0.3287 | 0.0334 | 0.22 |
| sigma_smooth [km/s] | 260.52 | 260.13 – 260.63 | 3.17 | 0.15 |
| mass-weighted age [Gyr] | 3.460 | 3.367 – 3.560 | 0.461 | 0.42 |

## B300

- B300 runs the same paths as B200, with identical ln Z and posteriors, at 0.28× B200's sampling speed. The nvidia-smi snapshot after the fits shows zero thermal and power-brake slowdown counters on all 4 B300 containers. The container spread is 1.3%.
- NVIDIA's HGX table lists FP64 at 10 TFLOPS for HGX B300 and 296 TFLOPS for HGX B200. FP32 is 600 TFLOPS for both (https://www.nvidia.com/en-us/data-center/hgx/, 8-GPU systems). The fit runs in float64 ("float64 verified" in every container's `bootstrap.log`).
- Modal's GPU guide says "B300 requires CUDA version 13.1+". The pinned image has CUDA 12 (XLA reports cuBLAS 120902), and B300 started and finished every fit on it anyway.
- In every B200 and B300 container, and on no other card, XLA logs: "cuBLAS < 13.2 (120902 found) has a known issue where many kernels free TMEM buffers multiple times. Executing a cuBLAS kernel concurrently with another kernel (e.g. on another stream) can lead to silent data corruption." The B200 and B300 results agree with the other cards to the table above.

## Consumer cards

- **Tied, one fit:** DR2 refit part-02, M1_210210 on an RTX 5090 at Vast (host 665755, instance 55625700, `results/dr2-refit-2026-10-12/part-02/run`). It used the same notebook (blob `0455b097`), Ceridwen `d7c0536`, sedpy_jax `9d8aa19`, image `sha256:e1c8846c…`, grid `6fe00c55…` and seed 20260832. Project commit `85d3acb` differs from `ce9752c` only in launcher code (`experiment.py` Modal runner, `modal_gpu.py`, `benchmark_modal.py`). Sampling 116.39 s, 5,462,839 calls, 46,937 calls/s, so **1.53× L40S** (1.55× by calls/s). It is one container on one host, so it has no spread.
- **Not tied:** `e-gpu-price-benchmark` (2026-09-23, 5060 Ti–5090) ran commit `c869309` with Ceridwen `1fae781`, the old grid and the likelihood harness (`benchmark_baked_runtime.py`). That is a different build and a different workload.
- The likelihood-harness stage was dropped from this benchmark. On the production model, `benchmark_baked_runtime.py` fails with `ValueError: emission lines shared with photometry: evaluate through MultiObservationLikelihood.loglike`. A fix needs a change outside this task (proposed, not made).

## Not measured

- `B200+`: it may run on B300 and is billed as B200 (GPU guide), so it is covered by the B200 and B300 rows.
- `A100`: it may run on either A100 size, and both sizes are measured.
- `H100` without `!`: Modal may upgrade it to H200. `H100!` was used.
- AMD MI355X ($6.75/h in `modal billing rates`): it is not in the GPU guide, and the image is CUDA-only.

## Spend

- Measured run (`ce9752c`, 11 cards): $20.81, estimated from container seconds × rates in the run manifests.
- Earlier attempts: an H100 shakedown at `267a7b5^`, $0.28 estimated. The first full launch at `267a7b5` was aborted because Modal reused a warm L40S container (`FileExistsError` on the `/grids` symlink). Its files are in `aborted-267a7b5/`.
- Modal billed (after credits, `modal billing summary`): $0.00. Modal's billing report for these apps is in "Billed by Modal" below.

## Record

- Configuration: `experiment.json` (M1_210210, seed 20260832, production defaults). Driver: `scripts/benchmark_modal.py` at `ce9752c`; summary: `summary.json`.
- Per card: `<card>/manifest.json`, `<card>/.modal/0/calls.json` (spawn, pack and receive times) and `request.json`, `<card>/containers/<n>-<call>/` (`status.json`, `hardware.txt`, stage logs, executed notebooks, result files) and `<card>-driver.log`. `containers-seen.jsonl` holds Modal's container start times, polled every 5 s.
- Experiment record: `wiki/research/experiments/e-modal-gpu-benchmark.md`.

## Sources

- Prices: https://modal.com/pricing (read 2026-10-14). GPU types, H100!/B200+ and the B300 CUDA requirement: https://modal.com/docs/guide/gpu (read 2026-10-14/15).
- Card names, memory, clocks, power and driver: `nvidia-smi` in each container (`status.json`, `hardware.txt`).
- FP64 and FP32 for HGX B300 and B200: https://www.nvidia.com/en-us/data-center/hgx/ (read 2026-10-15).
