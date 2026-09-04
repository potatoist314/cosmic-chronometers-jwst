---
title: Ceridwen GPU benchmarks
date: 2026-09-01
section: Archive
tags: [gpu, benchmarks]
job: t_d89d040c
status: obsolete
old: _old/analyses/ceridwen-gpu-benchmarks.html
---

This page compares forty-six measured GPU runs on Ceridwen likelihood work.

### Measured runs

One row shows one measured run. A short benchmark is not a complete posterior fit.

Select a column heading to sort the table. Select it again to reverse the order.

A price with the ≈ sign is the lowest Vast offer on 26 August 2026. That run did not record its own price.

| GPU | Published dense TF32 peak | Provider | Test | Ceridwen schema | Timed steps / calls | Calls/s | Vast price | Cost per 1,000,000 calls |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| GeForce RTX 5060 | 19.2 TFLOP/s | Vast | Converged fit, fast SFH basis A | 2.1 | 542 / 542,000 | 547.6 | $0.0844/h | $0.043 |
| B200 | 1,125 TFLOP/s | Vast | Joint fit benchmark, 50% pool | 2.1 | 5 / 5,000 | 743.9 | $5.3138/h | $1.984 |
| RTX PRO 6000 Blackwell Server Edition | 234 TFLOP/s | Vast | Joint fit benchmark, 50% pool | 2.1 | 5 / 5,000 | 444.9 | $1.3327/h | $0.832 |
| H100 SXM | 494 TFLOP/s | Vast | Joint fit benchmark, earlier fingerprint | 2.1 | 5 / 5,000 | 431.3 | $1.7422/h | $1.122 |
| RTX PRO 6000 Blackwell Max-Q Workstation Edition | 219.5 TFLOP/s | Vast | Joint fit benchmark, 50% pool | 2.1 | 5 / 5,000 | 409.3 | $1.2290/h | $0.834 |
| GeForce RTX 5090 | 104.8 TFLOP/s | Vast | Complete integrated fit | 2.1 | 514 / 514,000 | 393.1 | $0.4139/h | $0.292 |
| RTX PRO 5000 Blackwell | 65 TFLOP/s | Vast | Joint fit benchmark, 50% pool | 2.1 | 5 / 5,000 | 364.6 | $0.5619/h | $0.428 |
| GeForce RTX 5080 | 56.3 TFLOP/s | Vast | Joint fit benchmark, 50% pool | 2.1 | 5 / 5,000 | 253.1 | $0.1608/h | $0.177 |
| RTX PRO 4500 Blackwell | 51 TFLOP/s | Vast | Joint fit benchmark, 50% pool | 2.1 | 5 / 5,000 | 247.4 | $0.3081/h | $0.346 |
| GeForce RTX 4090 | 82.6 TFLOP/s | Vast | Joint fit benchmark, earlier fingerprint | 2.1 | 5 / 5,000 | 187.0 | $0.3052/h | $0.453 |
| RTX 6000 Ada Generation | 91.1 TFLOP/s | Vast | Joint fit benchmark, 50% pool | 2.1 | 5 / 5,000 | 196.0 | $0.6013/h | $0.852 |
| GeForce RTX 5070 | 30.8 TFLOP/s | Vast | Joint fit benchmark, 50% pool | 2.1 | 5 / 5,000 | 180.6 | $0.1206/h | $0.185 |
| RTX PRO 4000 Blackwell | 37 TFLOP/s | Vast | Joint fit benchmark, 50% pool | 2.1 | 5 / 5,000 | 168.8 | $0.2023/h | $0.333 |
| RTX 5000 Ada Generation | 65.3 TFLOP/s | Vast | Joint fit benchmark, 50% pool | 2.1 | 5 / 5,000 | 139.2 | $0.4281/h | $0.854 |
| A100 SXM4 | 156 TFLOP/s | Modal | Kernel trace | 2.1 | 1 / 1,000 | 127.5 |  |  |
| A100 SXM4 | 156 TFLOP/s | Vast | Matched full-spectrum step | 2.0 | 1 / 1,000 | 126.6 | ≈$0.5361/h | ≈$1.176 |
| A100 PCIe 40 GB | 156 TFLOP/s | Vast | Joint fit benchmark, 50% pool, 250 W host | 2.1 | 5 / 5,000 | 124.4 | $0.8009/h | $1.789 |
| A100 SXM4 | 156 TFLOP/s | Vast | Complete integrated fit | 2.0 | 488 / 488,000 | 118.6 | ≈$0.5361/h | ≈$1.256 |
| A100 40 GB | 156 TFLOP/s | Modal | Smoke test | 2.1 | 7 / 112 | approximately 112 |  |  |
| GeForce RTX 4080 | 49 TFLOP/s | Vast | Joint fit benchmark, 50% pool, 270 W host | 2.1 | 5 / 5,000 | 125.1 | $0.1881/h | $0.417 |
| A100 40 GB | 156 TFLOP/s | Modal | Complete feature-spectrum fit | 2.1 | 190 / 1,140,000 | 105.8 |  |  |
| A100 40 GB | 156 TFLOP/s | Modal | Full-spectrum checkpoint fit | 2.1 | 145 / 870,000 | 102.5 |  |  |
| GeForce RTX 5070 Ti | 43.9 TFLOP/s | Vast | Joint fit benchmark, 50% pool, 250 W host | 2.1 | 5 / 5,000 | 116.8 | $0.1147/h | $0.273 |
| GeForce RTX 5060 Ti | 23.7 TFLOP/s | Vast | Joint fit benchmark, earlier fingerprint | 2.1 | 5 / 5,000 | 111.6 | $0.0814/h | $0.203 |
| GeForce RTX 4070 Ti SUPER | 44 TFLOP/s | Vast | Joint fit benchmark, 50% pool, 256 W host | 2.1 | 5 / 5,000 | 107.0 | $0.1347/h | $0.350 |
| GeForce RTX 5060 | 19.2 TFLOP/s | Vast | Joint fit benchmark, 50% pool | 2.1 | 5 / 5,000 | 107.0 | $0.1028/h | $0.267 |
| GeForce RTX 5060 | 19.2 TFLOP/s | Vast | Converged fit, baseline SFH basis | 2.1 | 566 / 566,000 | 100.9 | $0.0844/h | $0.233 |
| GeForce RTX 4070 Super | 35.5 TFLOP/s | Vast | Joint fit benchmark, earlier fingerprint | 2.1 | 5 / 5,000 | 89.7 | $0.1018/h | $0.315 |
| CMP 170HX | Not published | Vast | Joint fit benchmark, 50% pool | 2.1 | 5 / 5,000 | 93.4 | $0.4014/h | $1.194 |
| GeForce RTX 4070 Ti | 40 TFLOP/s | Vast | Joint fit benchmark, 50% pool | 2.1 | 5 / 5,000 | 89.2 | $0.0890/h | $0.277 |
| GeForce RTX 3090 Ti | 40.0 TFLOP/s | Vast | Joint fit benchmark, 50% pool | 2.1 | 5 / 5,000 | 85.0 | $0.2281/h | $0.745 |
| RTX A6000 | 38.7 TFLOP/s | Vast | Joint fit benchmark, 50% pool | 2.1 | 5 / 5,000 | 74.0 | $0.4457/h | $1.673 |
| GeForce RTX 3080 Ti | 34.1 TFLOP/s | Vast | Joint fit benchmark, earlier fingerprint | 2.1 | 5 / 5,000 | 82.5 | $0.1348/h | $0.454 |
| GeForce RTX 3080 | 29.8 TFLOP/s | Vast | Joint fit benchmark, 50% pool, 220 W host | 2.1 | 5 / 5,000 | 69.3 | $0.0738/h | $0.296 |
| GeForce RTX 3070 Ti | 21.7 TFLOP/s | Vast | Joint fit benchmark, 50% pool | 2.1 | 5 / 5,000 | 68.6 | $0.1281/h | $0.519 |
| GeForce RTX 3070 | 20.3 TFLOP/s | Vast | Joint fit benchmark, 50% pool | 2.1 | 5 / 5,000 | 65.5 | $0.0614/h | $0.260 |
| GeForce RTX 3070 | 20.3 TFLOP/s | Vast | Joint fit benchmark, on demand | 2.1 | 5 / 5,000 | 65.3 | $0.0614/h | $0.261 |
| GeForce RTX 3090 | 35.6 TFLOP/s | Vast | Joint fit benchmark, earlier fingerprint | 2.1 | 5 / 5,000 | 80.3 | $0.1444/h | $0.500 |
| GeForce RTX 4060 Ti | 22 TFLOP/s | Vast | Joint fit benchmark, 50% pool | 2.1 | 5 / 5,000 | 55.3 | $0.0934/h | $0.469 |
| RTX A4000 | 19.2 TFLOP/s | Vast | Joint fit benchmark, 50% pool | 2.1 | 5 / 5,000 | 54.3 | $0.1214/h | $0.621 |
| A10 | 62.5 TFLOP/s | Vast | Joint fit benchmark, 50% pool | 2.1 | 5 / 5,000 | 54.1 | $0.2417/h | $1.242 |
| L4 | 60 TFLOP/s | Vast | Joint fit benchmark, 50% pool | 2.1 | 5 / 5,000 | 53.5 | $0.3347/h | $1.739 |
| GeForce RTX 3060 Ti | 16.2 TFLOP/s | Vast | Joint fit benchmark, 50% pool | 2.1 | 5 / 5,000 | 53.4 | $0.0807/h | $0.420 |
| V100 SXM2 | Not supported | Vast | Matched full-spectrum step | 2.0 | 1 / 1,000 | 42.9 | ≈$0.1090/h | ≈$0.706 |
| GeForce RTX 3060 | 13.0 TFLOP/s | Vast | Joint fit benchmark, earlier fingerprint | 2.1 | 5 / 5,000 | 34.0 | $0.0596/h | $0.487 |
| GeForce RTX 3050 | 9.1 TFLOP/s | Vast | Joint fit benchmark, 50% pool | 2.1 | 5 / 5,000 | 21.5 | $0.1420/h | $1.839 |

#### Fixed-workload sweep

Twenty-nine runs share the current comparison fingerprint. Seventeen new Ampere and Ada runs completed in the final sweep.

The RTX 6000 Ada and RTX 5000 Ada reached 196.0 and 139.2 calls/s. The RTX 4070 Ti cost $0.277 per million calls, the lowest cost among the new runs.

Rows marked earlier fingerprint remain as measured records. Do not treat them as part of the current controlled sweep.

<figure>
<figcaption>Likelihood calls per second for the seventeen added runs</figcaption>
</figure>

The table uses dense TF32 rates without sparsity. NVIDIA publishes the relevant values in the [GeForce comparison](https://www.nvidia.com/en-us/geforce/graphics-cards/compare/), [A10 specifications](https://www.nvidia.com/en-us/data-center/products/a10-gpu/), [L4 specifications](https://www.nvidia.com/en-us/data-center/l4/), and workstation GPU data sheets. NVIDIA does not publish a TF32 rate for CMP 170HX.

The B200 row uses JAX CUDA 13 and cuBLAS 13.6.1.10. A CUDA 12 diagnostic was excluded after XLA warned of possible silent corruption on B200.

#### RTX 5090 complete fit

The production nested-sampler run converged after 514 iterations and 514,000 likelihood calls. Sampling took 1,307.5 s, or 393.1 calls/s. The complete notebook took 1,386.1 s.

The actual Vast rate was $0.4139/h. Sampling cost $0.150, equivalent to $0.292 per million likelihood calls. The run used schema 2.1, 300 live points, 40 inner steps, 25 deletions, and `logZ_tol=-3`.

#### RTX 5060 fast SFH basis test

The paired runs used one galaxy, one seed, and the same nested-sampler settings. Fast basis A reached 547.6 calls/s; the baseline reached 100.9 calls/s. The measured sampler speedup was 5.67 times.

The posterior differences between the two bases are not larger than the differences between two baseline runs with different seeds (RTX 5090 seed-variation runs, one galaxy). The fixed-grid basis is the default in Ceridwen for the published grid.

#### RTX 5060 Ti same-boot state comparison and concurrency

One RTX 5060 Ti (published dense TF32 peak 24 TFLOP/s) ran three ceridwen states back to back in one boot: the combined-smoother baseline reached 5,548 likelihood calls per second; adding the hoisted flux factor, the compare-all searchsorted lowering, and fewer per-iteration host reads gave 5,570; a banded direct-space smoother gave 5,566. The three agree within run noise: after the smoothing collapse, kernel-count reductions no longer move the step time, which the smoothing gather and the float64 pixel likelihood dominate. The banded smoother was not adopted.

Boot-to-boot variance on shared hosts reached 66 percent for identical code on this instance. Only same-boot numbers are comparable.

Independent concurrent runs of the fixed benchmark on the same GPU scale linearly: one run 5,531, two runs 10,857, three runs 16,457 aggregate calls per second. Grid schema 2.1.

#### RTX 4060 Ti concurrent production fits

One 8 GB RTX 4060 Ti (published dense TF32 peak 22 TFLOP/s, 32 effective host cores) ran production DR2 fits through the shard runner in one boot: target M5_172669 alone, then targets M5_172669, M9_232005, and M11_214430 with `--fits-per-gpu 3`. Alone, M5_172669 sampled 1,183,000 likelihood calls in 187 s, or 6,315 calls per second. With two other fits running it took 588 s, or 2,010 calls per second; the three concurrent fits summed to 6,134 calls per second. All three fits completed and validated. Whole-GPU memory peaked at 7,552 MiB of 8,188 MiB. Grid schema 2.1; 500 live points, 65 inner steps, 100 deletions.

Concurrent processes share a GPU by time-slicing, so the linear scaling of the 25-lane benchmark does not transfer to production fits, which batch 100 lanes per step and keep the GPU busy on their own. The shard runner therefore runs one fit per GPU by default.

#### RTX 3070 concurrency and allocator levels

One 8 GB RTX 3070 (published dense TF32 peak 20 TFLOP/s) repeated the production fit of M5_172669 in one boot at seven levels. One fit with the default allocator sampled 1,189,500 likelihood calls in 269.5 s, or 4,414 calls per second, inside a 5,880 MiB preallocated pool while its JAX peak in use was 973 MiB. Two fits with `XLA_CLIENT_MEM_FRACTION=0.42` took 562 s each and summed to 4,234 calls per second; three fits at 0.28 took 832 to 840 s each and summed to 4,271. Whole-GPU memory peaked at 7,337 and 7,700 MiB. Concurrency therefore returns 0.96 to 0.97 of one fit, and the default stays one fit per GPU.

Smaller pools do not change speed. One fit at 0.14 (a 1,098 MiB pool) sampled in 267.2 s with a 1,481 MiB whole-GPU footprint; three fits at 0.14 took 835 to 840 s each inside 4,406 MiB; one fit with `XLA_PYTHON_CLIENT_PREALLOCATE=false` sampled in 267.4 s inside 2,469 MiB. A 0.10 fraction (819 MiB) failed before sampling with `Autotuning failed for HLO: gemm_fusion_dot`. Every fit with the 1,098 MiB pool or with preallocation off stopped at 1,183,000 calls, one outer iteration before the default fit, and the RTX 4060 Ti fit above stopped at the same count: the pool size changes the XLA autotuner's kernel choices, which shifts the float64 sampler path by one iteration; ln Z was 232730.870 ± 0.383 against 232730.981 ± 0.259. Grid schema 2.1; cost $0.16.

Evidence: `benchmarks/ceridwen/runs/fits_per_gpu_production_8gb_20260902.json`

#### Blackwell concurrency on the RTX 5060, RTX 5070, and RTX 5060 Ti

Three Blackwell cards each repeated one, two, and three concurrent production fits in one boot with the DR2 shard runner (`XLA_CLIENT_MEM_FRACTION = 0.85/N` for N > 1, one runner process per fit). One fit of M5_172669 sampled 1,157,000 likelihood calls on every card: 222.2 s or 5,207 calls per second on the 8 GB RTX 5060 (published dense TF32 peak 19 TFLOP/s), 154.2 s or 7,503 on the 12 GB RTX 5070 (31 TFLOP/s), and 198.8 s or 5,820 on the 16 GB RTX 5060 Ti (24 TFLOP/s), which is 274, 242, and 242 calls per second per TFLOP against 221 on the RTX 3070. Two fits (M5_172669 with M4_108989) summed to 5,341, 7,476, and 5,967 calls per second and three fits (with M9_232005 and M11_214430) to 5,357, 7,415, and 5,998, or 0.99 to 1.03 of one fit; M5_172669 itself ran 2.0 to 2.1 times slower beside one other fit and 3.0 to 3.1 times slower beside two. The default stays one fit per GPU on Blackwell.

Memory never limits the choice. The JAX peak in use is 1,005 MiB per fit on all three cards; the one-fit whole-GPU peaks of 6,162, 9,394, and 12,316 MiB are the default 75 percent preallocation, and three fits peaked at 7,617, 11,313, and 14,542 MiB. Mean nvidia-smi utilization rose from 68 to 74 percent at one fit to 86 to 88 percent at three without a throughput gain. M5_172669 stopped at 1,157,000 calls with ln Z 232732.02 (± 0.19 to 0.37) on every Blackwell card and level, against 1,189,500 calls and 232730.98 ± 0.26 on the RTX 3070. At the rented hosts' prices ($0.1028, $0.1192, and $0.0881 per hour) one fit's sampler time cost $0.0063, $0.0051, and $0.0049. Grid schema 2.1; cost $0.335.

Evidence: `benchmarks/ceridwen/runs/fits_per_gpu_production_blackwell_rtx5060_8gb_20260902.json`, `benchmarks/ceridwen/runs/fits_per_gpu_production_blackwell_rtx5070_12gb_20260902.json`, `benchmarks/ceridwen/runs/fits_per_gpu_production_blackwell_rtx5060ti_16gb_20260902.json`

#### Speed against published peak throughput

Both axes use a log scale. The vertical axis shows likelihood calls per second.

<figure>
<figcaption>CUDA FP32 peak (TFLOP/s, log scale)</figcaption>
</figure>

<figure>
<figcaption>CUDA FP64 peak (TFLOP/s, log scale)</figcaption>
</figure>

<figure>
<figcaption>FP64 tensor peak (TFLOP/s, log scale)</figcaption>
</figure>

<figure>
<figcaption>TF32 tensor peak (TFLOP/s, log scale)</figcaption>
</figure>

<figure>
<figcaption>FP16 tensor peak (TFLOP/s, log scale)</figcaption>
</figure>

<figure>
<figcaption>BF16 tensor peak (TFLOP/s, log scale)</figcaption>
</figure>

### GPU memory

The fixed-step benchmark calculation peak stayed between 1,460 MiB and 1,610 MiB across the retained sweep.

The RTX 3060, RTX 3080 Ti, and RTX 4070 Super each used a 1,519 MiB calculation peak. The recorded whole-process peaks were 9,260 MiB on the RTX 3080 Ti and 9,164 MiB on the RTX 4070 Super.

The 50% RTX 5070, RTX 5070 Ti, and RTX 5080 runs each used a 1,519 MiB calculation peak. Whole-process memory was 6,180 MiB, 8,278 MiB, and 8,304 MiB.

The seven new Blackwell runs each used about 1,519 MiB at the JAX calculation peak. Whole-process memory was 92,146 MiB on B200; 49,312 and 49,308 MiB on the RTX PRO 6000 editions; 24,668, 16,452, and 12,370 MiB on the RTX PRO 5000, 4500, and 4000; and 4,102 MiB on the RTX 5060.

The 8 GB RTX 3070 completed with both allocators. The 50% pool used 4,152 MiB process memory; on-demand allocation used 2,344 MiB.

A production fit on the 8 GB RTX 3070 holds 826 to 989 MiB at the JAX peak. The default preallocation shows 6,238 MiB per process in `nvidia-smi`; a 0.14 fraction shows 1,456 MiB and on-demand allocation 2,444 MiB, all at the same sampler speed.

The new recorded whole-process peaks were 32,884 MiB on CMP 170HX; 8,172 to 8,288 MiB on the RTX 4060 Ti, RTX 4070 Ti SUPER, and RTX 4080; and 6,212 MiB on the RTX 4070 Ti.

An RTX 5090 sampling snapshot showed 4,520 MiB process memory. This value is not a measured peak.

Evidence: `benchmarks/ceridwen/runs/ceridwen_vast_v100_memory_verification_complete_2026-08-26/`, `results/rtx-5090-integrated-fit/`, and the benchmark records above

### Modal A100 kernel trace

One kernel used 93.8% of the GPU event time. It ran 564 times inside one 7.843 s step. The GPU stream stayed active for 94.9% of that step. Matrix multiplication kernels used 0.047% of the GPU event time.

This pattern is consistent with the weighted sum over the SSP grid.

Evidence: `benchmarks/ceridwen/runs/ceridwen_modal_a100_kernel_trace_complete_2026-08-26/`
