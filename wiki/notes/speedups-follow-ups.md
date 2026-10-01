---
title: Rejected speedup options
date: 2026-10-01
section: Analyses
theme: Compute
tags: [ceridwen, compute, speedups]
job:
---

Rejected speedup options from the overnight run of 30 Sep 2026: ideas that changed results, showed no gain, were never tried, or need Liu Hao's decision. Accepted speedups are in [REPORT](https://github.com/potatoist314/cosmic-chronometers-jwst/blob/4fa1b1df0249548a7da8959edd6c8009395082f8/results/speedups-overnight-2026-09-30/REPORT.md).

Setup
: M1_210210 with the nebular grid, emission-line marginalisation, Ca mask and zevo; grid `amist_c3k_hr_krou_afe_nebular.h5` (schema-2.1 HR SSP); RTX 5090, jax 0.10.2. CPU dumps are 1,780-point step-10 subsamples of 17,800 dead points; GPU dumps are full 17,800.

Free
: Bitwise-identical on CPU; on GPU equal up to the float rounding the kernel shows between rentals.

## Proven numerical changes

| Option | Measured effect | Evidence | Open question |
|---|---|---|---|
| Doublet barrier on each dot (uncommitted patch) | 92 of 1,780 CPU \(\ln L\) differ, max \(7.0\times10^{-10}\); control trsm-s10 dump bitwise | [patch](https://github.com/potatoist314/cosmic-chronometers-jwst/blob/4fa1b1df0249548a7da8959edd6c8009395082f8/results/speedups-overnight-2026-09-30/integrate/cpu/emission-lines-barrier-dirty.patch), [dump](https://github.com/potatoist314/cosmic-chronometers-jwst/blob/4fa1b1df0249548a7da8959edd6c8009395082f8/results/speedups-overnight-2026-09-30/integrate/cpu/dump-bar-s10.npz), [control](https://github.com/potatoist314/cosmic-chronometers-jwst/blob/4fa1b1df0249548a7da8959edd6c8009395082f8/results/speedups-overnight-2026-09-30/integrate/cpu/dump-trsm-s10.npz), [compare](https://github.com/potatoist314/cosmic-chronometers-jwst/blob/4fa1b1df0249548a7da8959edd6c8009395082f8/results/speedups-overnight-2026-09-30/integrate/cpu/cmpstep.py) | Reason for the differences unresolved |
| SFH-basis per-group bin truncation (unapplied patch) | 231 of 1,780 CPU \(\ln L\) differ, max 0.035 | [patch](https://github.com/potatoist314/cosmic-chronometers-jwst/blob/4fa1b1df0249548a7da8959edd6c8009395082f8/results/speedups-overnight-2026-09-30/integrate/cpu/bins-truncation.patch), [dump](https://github.com/potatoist314/cosmic-chronometers-jwst/blob/4fa1b1df0249548a7da8959edd6c8009395082f8/results/speedups-overnight-2026-09-30/integrate/cpu/dump-bins-s10.npz) | Exactness question unresolved |
| Windowed line Gram | 2,560 of 17,800 GPU \(\ln L\) differ, max \(1.7\times10^{-8}\) | REPORT, Not free table | Reorders sums; no exact variant recorded |
| XLA f1: Triton GEMM off | All 17,800 GPU \(\ln L\) differ vs cand baseline | [job](https://github.com/potatoist314/cosmic-chronometers-jwst/blob/4fa1b1df0249548a7da8959edd6c8009395082f8/results/speedups-overnight-2026-09-30/integrate/gpu-lik/queue/02c-dump-f1.job), [dump](https://github.com/potatoist314/cosmic-chronometers-jwst/blob/4fa1b1df0249548a7da8959edd6c8009395082f8/results/speedups-overnight-2026-09-30/integrate/gpu-lik/dumps/dump-f1.npz), [baseline](https://github.com/potatoist314/cosmic-chronometers-jwst/blob/4fa1b1df0249548a7da8959edd6c8009395082f8/results/speedups-overnight-2026-09-30/integrate/gpu-lik/dumps/dump-cand.npz) | Cause unresolved |
| XLA f2: also cuBLASLt on | All 17,800 GPU \(\ln L\) differ vs cand baseline | [job](https://github.com/potatoist314/cosmic-chronometers-jwst/blob/4fa1b1df0249548a7da8959edd6c8009395082f8/results/speedups-overnight-2026-09-30/integrate/gpu-lik/queue/02c-dump-f2.job), [dump](https://github.com/potatoist314/cosmic-chronometers-jwst/blob/4fa1b1df0249548a7da8959edd6c8009395082f8/results/speedups-overnight-2026-09-30/integrate/gpu-lik/dumps/dump-f2.npz) | Cause unresolved |
| Doublet as elementwise sum | 1-ulp differences in 2 of 150,000 CPU column elements (FMA); GPU unmeasured | REPORT, Not free table | FMA contraction; no exact variant recorded |
| `jax.jit` of line columns | 1,049,770 elements differ on CPU, max \(4.0\times10^{-28}\) | REPORT, Not free table | No exact variant recorded |
| `jax.jit` of posterior draws | 3.89 → 1.64 s on CPU, but \(3\times10^{-10}\) relative differences | REPORT, Not free table | No exact variant recorded |
| Two 100-row batches per sampler round | CPU rounds 156/245 → 141/175, but GPU sampling 108.0 → 155.0 s, not bitwise (165 iterations, \(\ln Z\) 236003.45) | REPORT, Not free table | Slower and inexact as tried |
| Larger or compacted likelihood batch | Row count changes \(\ln L\) bits on CPU | REPORT, Not free table | No exact variant recorded |
| FilterSet numpy rewrite | 2.1 s, but changes rounding | REPORT, Not free table | None recorded beyond rounding |
| Shared KL histogram sort | Reorders sums | REPORT, Not free table | No exact variant recorded |

## Measured, not adopted

| Option | Measured effect | Evidence | Open question |
|---|---|---|---|
| Sampler micro-opts | Cholesky hoist nil (XLA hoists it); finalise ~0.1 s; host loop ~1 ms; free_moves 4/8/12 within 2% on GPU (109.8/109.9/111.9 s) | REPORT, Tried section | No gain found |
| Grid upload streams | 4 vs 8 streams equal (~47–48 s); 12 streams fail (sshd MaxStartups); Mac cap 13.2 MB/s | REPORT, Tried section | Link saturated |
| Lossless grid transform | Delta-age 0.775 → 0.732 (~26 MB, ~3 s); xz 0.711 at 20× pack time; gain under host spread, not built | REPORT, Not free table | Not built |
| Persistent XLA cache | Warm −2.2 s; new galaxy +3 s (executables embed data) | REPORT, Not free table | Net negative per new target |
| Catalogue YAML skip | ~1.9 s per read, but masked columns rely on the parse | REPORT, Not free table | Correctness blocker |
| Default K fits-per-gpu | 1.38× at K=4, +1.15× at K=8, bitwise; K=4 peaks at 21.3 GB RAM (unchecked), bid stop loses K cells | REPORT, Not free table | Not defaulted |
| Library removal | cuDNN required by the XLA compiler; cuSOLVER/cuSPARSE needed by solver create; six more libraries load in every job | REPORT, Tried section | Impossible as tried |

## Untested proposals

| Option | Measured effect | Evidence | Open question |
|---|---|---|---|
| Masked-row compaction | Unmeasured; grouped with the windowed Gram row in REPORT | REPORT, Not free table | Exact compaction untested |
| Parallel offer search | ~2.5 s estimate vs 5.6 s pre-rental total | REPORT, Not free table | Unbuilt; gain small |
| zstd image layers | −19.5% cuBLAS layer, ~18 s per cold host; needs Docker ≥ 23.0 | REPORT, Not free table | Vast Docker versions unknown |
| `log_evidence_err` RNG | Uses the numpy global RNG | REPORT, Not free table | Seed-handling change, not a speedup |
| Vmapped multi-fit sampler | Would change row counts and bits; MPS already gives the batch-500 gain | REPORT, Not free table | Not proposed |
| float32 or power-of-two FFT | Changes rounding | REPORT, Not free table | None recorded beyond rounding |

## Policy choices

| Option | Measured effect | Evidence | Open question |
|---|---|---|---|
| Prefer hosts with cached image | 42–77 s vs 106 s–7 min to running | REPORT, Not free table | Conflicts with the AGENTS.md host ranking; Liu Hao's rule |
| Grid fetched on box | Upload 473 MB at 8–11 MB/s is the setup critical path | REPORT, Not free table | Hosting for the required grid remains unbuilt; data-release decision |
| Grid hosted or in image | −1 to −3 min upload | REPORT, Not free table | Storage and image policy |
| GPU type | 30 Sep survey, solo fits: 5090 fastest and cheapest to ~$0.44/h; A100 1.30×, 4090 1.62×, 5060 Ti 3.41×, 3090 3.75×, V100 3.91× slower solo | REPORT, Not free table; [survey](https://github.com/potatoist314/cosmic-chronometers-jwst/tree/4fa1b1df0249548a7da8959edd6c8009395082f8/results/speedups-swarm-throughput-2026-09-30/types) | Liu Hao's choice on that survey |
| Rank offers by USD per fit | Record ranking paid 2.5–4× per fit vs a valid $0.153/h bid; 3 of 9 bid rentals stopped mid-job | REPORT, Not free table | Liu Hao's rental rule |

## Evidence

Sources
: [Overnight REPORT](https://github.com/potatoist314/cosmic-chronometers-jwst/blob/4fa1b1df0249548a7da8959edd6c8009395082f8/results/speedups-overnight-2026-09-30/REPORT.md) and the [preserved evidence tree](https://github.com/potatoist314/cosmic-chronometers-jwst/tree/4fa1b1df0249548a7da8959edd6c8009395082f8/results/speedups-overnight-2026-09-30/integrate), both pinned to the same commit. Patch, dump, job and compare-script links are in the tables.
