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
