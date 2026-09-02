# Ceridwen GPU benchmarks

Measured runs from 25 August 2026. Times are not directly comparable unless
the likelihood data and sampler settings match.

## Reproducible short benchmark

Run the maintained benchmark after `bash scripts/bootstrap_vast_ai.sh`. Replace
the example price, host, and instance values with the current Vast offer:

```bash
.venv-ceridwen-gpu/bin/python \
  scripts/benchmark_ceridwen_vast.py run \
  --output-root benchmarks/ceridwen/runs \
  --price-usd-per-hour 0.670 \
  --vast-host 148498 \
  --vast-instance 48652928
```

The fixed workload is `m1_210210_joint_full_v1`: 11 photometric bands,
3,523 fitted spectral pixels, the published schema-2.1 high-resolution grid,
and BlackJAX NSS with 300 live points, 40 inner steps, and 25 deletions. The
runner excludes one compiled warm-up step. It then measures five steps, or
5,000 likelihood calls.

Store these pure benchmark runs under `benchmarks/ceridwen/runs/`, never under
`results/`. Each benchmark run directory contains `benchmark.json`,
`benchmark.csv`, and `benchmark.log`. The JSON includes input checksums, code
and software versions, GPU metadata, memory use, raw step times, throughput,
and cost per 100,000 likelihood calls. The short run measures hardware
performance. It does not produce a converged posterior or scientific parameter
estimates.

Rank copied benchmark files with:

```bash
.venv-ceridwen-gpu/bin/python \
  scripts/benchmark_ceridwen_vast.py summarize \
  benchmarks/ceridwen/runs/ceridwen_vast_*_benchmark_complete_*/benchmark.json
```

The summary command stops when workload, input, code, or software fingerprints
differ. Use only one fingerprint in a comparison table.

## Static smoothing A/B (1 September 2026)

One RTX 5060 (published dense TF32 peak 47 TFLOP/s) ran the fixed workload
twice on the same rental: first with the chained LOSVD and instrumental
convolutions, then with the single combined Gaussian that ceridwen builds when
every width is known at setup. Grid schema 2.1.

| Smoothing | Calls/s | Median step | Resident JAX memory | Peak memory |
| --- | ---: | ---: | ---: | ---: |
| Chained | 915 | 1.101 s | 619 MiB | 1,589 MiB |
| Combined | 3,825 | 0.263 s | 316 MiB | 1,589 MiB |

The combined form is 4.18 times faster. Peak memory is unchanged because a
transient inside the sampler step sets it. The combined form is now the
installed default. Record:
`benchmarks/ceridwen/runs/static_smoothing_gpu_verification_20260901T110236Z.json`.

## Likelihood micro-optimisations and concurrency (1 September 2026)

One RTX 5060 Ti ran the fixed workload for three ceridwen states in one boot,
then a concurrency test. Boot-to-boot variance on shared Vast hosts reached
66% for identical code, so only same-boot numbers are comparable.

| State | Calls/s |
| --- | ---: |
| `a38982a` (combined smoother) | 5,548 |
| + flux-factor hoist, compare-all searchsorted, fewer host syncs | 5,570 |
| + banded direct-space smoother | 5,566 |

The kernel-count reductions (42 -> 19 fusions per call, verified bit-identical
on 64 fixed prior draws) do not move GPU throughput at 25 vmapped lanes; the
step is bound by the smoothing gather and the float64 pixel likelihood. The
banded smoother matched the FFT chain in float64 and float32 forms and was not
adopted.

Concurrent independent runs of this benchmark on the same GPU scale linearly:

| Benchmark runs per GPU | Aggregate calls/s |
| ---: | ---: |
| 1 | 5,531 |
| 2 | 10,857 |
| 3 | 16,457 |

Setup per fit also fell from ~150 s to ~27 s on the rental after the sedpy
filter-construction path moved to NumPy. That sedpy_jax fork is the
`external/sedpy_jax` submodule; the bootstrap and the Modal image install it
from the tree.
Record: `benchmarks/ceridwen/runs/likelihood_kernel_ab_and_concurrency_20260901.json`.

## Concurrent production fits on 8 GB (1 September 2026)

The linear scaling above does not transfer to production fits. One RTX 4060 Ti
(8 GB, 32 effective host cores) ran the DR2 shard runner in one boot: target
M5_172669 alone, then M5_172669, M9_232005, and M11_214430 with
`--fits-per-gpu 3` (each worker `XLA_CLIENT_MEM_FRACTION = 0.28`). Production
settings: 500 live points, 65 inner steps, 100 deletions, seeds
`20260830 + manifest_index`.

| Level | Target | Likelihood calls | Sampler wall | Calls/s |
| --- | --- | ---: | ---: | ---: |
| 1 fit | M5_172669 | 1,183,000 | 187 s | 6,315 |
| 3 fits | M5_172669 | 1,183,000 | 588 s | 2,010 |
| 3 fits | M9_232005 | 1,202,500 | 617 s | 1,950 |
| 3 fits | M11_214430 | 1,404,000 | 646 s | 2,174 |

The three concurrent fits sum to 6,134 calls/s, the same as one fit alone. All
fits completed and validated; whole-GPU memory peaked at 7,552 of 8,188 MiB.
Processes share a GPU by time-slicing, and a production step batches 100 lanes
(`num_delete`) against the benchmark's 25, so one production fit already keeps
the GPU busy. `scripts/run_ceridwen_vast_multi_gpu.py` therefore defaults to
`--fits-per-gpu 1`; the shard manifest records `fits_per_gpu`. Cost of the
measurement: $0.034.
Record: `benchmarks/ceridwen/runs/fits_per_gpu_production_8gb_20260901.json`.

## Concurrency and allocator levels on 8 GB (2 September 2026)

One RTX 3070 (8 GB) repeated the same production fit of M5_172669 in one boot
at seven levels: one, two, and three concurrent fits with the runner's default
`XLA_CLIENT_MEM_FRACTION = 0.85/N`, then one fit with smaller pools and with
preallocation off. Each level used one runner process per fit. The RTX 3070 is
slower than the RTX 4060 Ti above, so only ratios within this table transfer.

| Level | Pool per fit | Sampler wall per fit | Calls per fit | Aggregate calls/s | GPU peak |
| --- | ---: | ---: | ---: | ---: | ---: |
| 1 fit, default | 5,880 MiB | 269.5 s | 1,189,500 | 4,414 | 6,263 MiB |
| 2 fits, 0.42 | 3,294 MiB | 562.3, 561.4 s | 1,189,500 | 4,234 | 7,337 MiB |
| 3 fits, 0.28 | 2,196 MiB | 831.8, 835.3, 839.5 s | 1,189,500 | 4,271 | 7,700 MiB |
| 1 fit, 0.14 | 1,098 MiB | 267.2 s | 1,183,000 | 4,427 | 1,481 MiB |
| 1 fit, 0.10 | 819 MiB | failed at compile | | | 977 MiB |
| 3 fits, 0.14 | 1,098 MiB | 834.6, 840.2, 837.5 s | 1,183,000 | 4,238 | 4,406 MiB |
| 1 fit, preallocate off | on demand | 267.4 s | 1,183,000 | 4,424 | 2,469 MiB |

Two or three concurrent fits sum to 0.96 to 0.97 of one fit, so the default
stays `--fits-per-gpu 1`. The JAX working set of one production fit
(`peak_bytes_in_use`) is 826 to 989 MiB; the default preallocation reserves
75 percent of the card. A 1,098 MiB pool runs at full speed, an 819 MiB pool
fails in Triton GEMM autotuning before sampling starts, and
`XLA_PYTHON_CLIENT_PREALLOCATE=false` runs at full speed in 2.4 GB. Every fit
with the 1,098 MiB pool or with preallocation off stopped at 1,183,000 calls,
one outer iteration before the default fit, as did the RTX 4060 Ti fit above:
the pool size changes the autotuned kernels and shifts the float64 sampler
path by one iteration, with ln Z agreeing within one sigma (232730.87 ± 0.38
against 232730.98 ± 0.26). Memory therefore never limits concurrency on 8 GB;
time-slicing does. Cost of the measurement: $0.16.
Record: `benchmarks/ceridwen/runs/fits_per_gpu_production_8gb_20260902.json`.

## Blackwell concurrency on 8, 12, and 16 GB (2 September 2026)

Three Blackwell cards each ran one, two, and three concurrent production
fits in one boot with the DR2 shard runner
(`scripts/run_ceridwen_vast_multi_gpu.py`: 500 live points, 65 inner steps,
100 deletions, logZ_tol -5, full_spectrum, seeds 20260830 + manifest_index,
one runner process per fit, `XLA_CLIENT_MEM_FRACTION = 0.85/N` for N > 1 and
the default preallocation for N = 1). The single fit is M5_172669, which
stopped at 1,157,000 likelihood calls on every card and level; two fits add
M4_108989 and three fits run M5_172669 with M9_232005 and M11_214430, so the
aggregate sums calls per second over targets whose cost per call differs.
Hosts: RTX 5060 8 GB in the United Kingdom (host 166946, 24 EPYC cores,
$0.1028/h), RTX 5070 12 GB in South Korea (host 454863, 12 Ryzen cores,
$0.1192/h), RTX 5060 Ti 16 GB in Vietnam (host 81456, 28 Xeon cores,
$0.0881/h). Prices are the offer `dph_total` at rental; the level cost is that
price times the wall from launching the level to the last fit's exit.

| Card | Fits | Sampler wall per fit | Aggregate calls/s | Relative to 1 fit | GPU peak | Level cost |
| --- | ---: | ---: | ---: | ---: | ---: | ---: |
| RTX 5060 8 GB | 1 | 222.2 s | 5,207 | 1.00 | 6,162 MiB | $0.0081 |
| RTX 5060 8 GB | 2 | 446.8, 474.8 s | 5,341 | 1.03 | 7,240 MiB | $0.0160 |
| RTX 5060 8 GB | 3 | 661.4, 698.5, 723.6 s | 5,357 | 1.03 | 7,617 MiB | $0.0232 |
| RTX 5070 12 GB | 1 | 154.2 s | 7,503 | 1.00 | 9,394 MiB | $0.0070 |
| RTX 5070 12 GB | 2 | 319.5, 340.6 s | 7,476 | 1.00 | 10,885 MiB | $0.0137 |
| RTX 5070 12 GB | 3 | 477.6, 504.1, 521.0 s | 7,415 | 0.99 | 11,313 MiB | $0.0193 |
| RTX 5060 Ti 16 GB | 1 | 198.8 s | 5,820 | 1.00 | 12,316 MiB | $0.0067 |
| RTX 5060 Ti 16 GB | 2 | 399.0, 415.3 s | 5,967 | 1.02 | 14,145 MiB | $0.0124 |
| RTX 5060 Ti 16 GB | 3 | 589.7, 623.8, 647.6 s | 5,998 | 1.03 | 14,542 MiB | $0.0182 |

Single fit of M5_172669 per card, costed on the sampler wall alone and on the
whole level including setup:

| Card | Price | Sampler wall | Calls/s | Cost per fit, sampler | Cost per fit, level | JAX peak in use |
| --- | ---: | ---: | ---: | ---: | ---: | ---: |
| RTX 5060 8 GB | $0.1028/h | 222.2 s | 5,207 | $0.0063 | $0.0081 | 1,005 MiB |
| RTX 5070 12 GB | $0.1192/h | 154.2 s | 7,503 | $0.0051 | $0.0070 | 1,005 MiB |
| RTX 5060 Ti 16 GB | $0.0881/h | 198.8 s | 5,820 | $0.0049 | $0.0067 | 1,005 MiB |

On every card two or three concurrent fits sum to 0.99 to 1.03 of one fit,
and M5_172669 itself runs 2.0 to 2.1 times slower beside one other fit and
3.0 to 3.1 times slower beside two, so the default stays `--fits-per-gpu 1`
on Blackwell as on Ampere and Ada. The 2 to 3 percent gains on the RTX 5060
and RTX 5060 Ti arrive with the changed target mix and are not headroom.
Mean nvidia-smi utilization rises from 68 to 74 percent at one fit to 86 to
88 percent at three without a matching gain, so the idle fraction at one fit
is not free capacity. Memory never limits: the JAX peak in use is 1,005 MiB
per fit on all three cards, the one-fit peaks are the 75 percent default
preallocation, and three fits leave 534 MiB free on the 8 GB card.
M5_172669 stops at 1,157,000 calls with ln Z 232732.02 (± 0.19 to 0.37) on
every Blackwell card and level, against 1,189,500 calls and 232730.98 ± 0.26
on the RTX 3070, so within a card every ratio compares identical work. For a
single fit the RTX 5070 is fastest, and at these hosts' prices the RTX 5060 Ti
is cheapest per fit with the RTX 5070 within 5 percent; that ordering follows
the hourly price, which varies by host, more than the speed. Cost of the
measurement: $0.335 over 3.3 billable hours, plus $0.006 for a first RTX 5060
Ti instance whose SSH never answered.
Records: `benchmarks/ceridwen/runs/fits_per_gpu_production_blackwell_rtx5060_8gb_20260902.json`,
`benchmarks/ceridwen/runs/fits_per_gpu_production_blackwell_rtx5070_12gb_20260902.json`,
`benchmarks/ceridwen/runs/fits_per_gpu_production_blackwell_rtx5060ti_16gb_20260902.json`.

## Completed runs

| Provider | GPU | Likelihood | Grid | NSS settings | Iterations / dead points | Likelihood calls | Sampler wall | Calls/s | Result |
| --- | --- | --- | --- | --- | ---: | ---: | ---: | ---: | --- |
| Vast.ai | A100 SXM4 40 GB | 11 photometric bands + 3,523 native spectral pixels | schema 2.0, C3K HR, $R=6000$ | 300 live, 40 inner, 25 delete, $\log Z_{\rm tol}=-3$ | 489 / 12,225 | 489,000 | 4,138.2 s | 118.2 | $\ln Z=230642.517\pm0.472$; ESS 2,961.1; notebook retained, posterior HDF5 not retained |
| Modal | A100 40 GB; form factor unrecorded | 1,924 feature spectral pixels; no photometry | schema 2.1 | 500 live, 60 inner, 100 delete, $\log Z_{\rm tol}=-5$ | 191 / 19,100 | 1,146,000 | 10,857.6 s | 105.5 | $\ln Z=125739.808\pm0.176$; ESS 3,416.4; posterior and derived HDF5 retained |

The Modal notebook's complete outer wall time was 10,948.462 s. The Vast
sampler averaged 8.463 s per outer iteration; Modal averaged 56.846 s, but a
Modal outer iteration performed six times as many likelihood calls.

## Smoke and incomplete runs

| Provider | Workload | NSS settings | Progress | Measured wall | Derived calls/s | Status |
| --- | --- | --- | --- | ---: | ---: | --- |
| Vast.ai | Quick notebook | quick profile | complete | 142 s end-to-end | not available | User-reported compatibility run; no retained output artifact |
| Modal | Spectra-notebook smoke | 16 live, 2 inner, 8 delete | 8 iterations, 64 dead, 128 calls | 11.6 s sampler | 11.0 | Complete plumbing test; JIT-dominated, ESS 1.0, not a scientific fit |
| Modal | Feature spectrum, 1,924 pixels | 500 live, 60 inner, 100 delete, $\log Z_{\rm tol}=-5$ | 5 iterations, 500 dead, 30,000 calls | about 287.4 s sampler; 379.598 s outer | 104.4 | Incomplete; no checkpoint or posterior |
| Modal | Full spectrum, 3,523 pixels | 500 live, 60 inner, 100 delete, $\log Z_{\rm tol}=-5$ | 5 iterations, 500 dead, 30,000 calls | about 291.3 s sampler; 382.941 s outer | 103.0 | Incomplete; no checkpoint or posterior |
| Modal | Full spectrum, 3,523 pixels | 500 live, 60 inner, 100 delete, $\log Z_{\rm tol}=-5$ | 146 iterations, 14,600 dead, 876,000 calls | about 8,572 s sampler; 8,683.574 s outer | 102.2 | Failed before convergence at $\Delta\log Z=18.786$; checkpoint retained |

The two five-iteration Modal wrappers reported `completed`, but their sampler
outputs stopped without convergence or a final result. They are classified as
incomplete here. Approximate sampler times are sums of rounded per-iteration
times; incomplete-run call counts use
`iterations * num_delete * num_inner_steps`.

## Interpretation

- The Vast fit used joint photometry and a native-pixel spectrum. The completed
  Modal fit used a feature-only spectrum and a newer grid schema.
- Calls/s is derived from the recorded sampler wall time. It measures the whole
  likelihood path, not isolated FP32, FP64, or memory-bandwidth performance.
- The Modal smoke rate includes one-time JIT compilation and is not a
  steady-state throughput measurement.
- At the observed Vast price of $0.670/hour, its 4,138.2-second sampler cost
  about $0.77. This is dated price context, not a persistent provider price.

## Provenance

Converged scientific fits remain under `results/`. Incomplete and diagnostic
artifacts remain available under `benchmarks/ceridwen/runs/`.

- Vast completed fit:
  `results/a100-integrated-fit-notebook/ceridwen_integrated_photometry_spectra.ipynb`
- Modal completed feature fit:
  `results/a100-feature-spectrum/`
- Modal incomplete and checkpoint runs:
  `benchmarks/ceridwen/runs/ceridwen_modal_a100_feature_spectrum_incomplete_2026-08-25/`,
  `benchmarks/ceridwen/runs/ceridwen_modal_a100_full_spectrum_incomplete_2026-08-25/`,
  and `benchmarks/ceridwen/runs/ceridwen_modal_a100_full_spectrum_checkpoint_2026-08-25/`
- Modal smoke run: `batch-20260825T151156339684Z`
- Vast allocation: host `148498`, instance `48652928`, Croatia. JAX detected
  CUDA and verified float64 on the A100 SXM4 40 GB.
