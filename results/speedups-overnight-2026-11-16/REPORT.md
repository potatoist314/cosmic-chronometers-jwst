# Speedups overnight, 16–17 Nov 2026

One first-time production fit of M1_210210 in the window-194 arms (`results/legac-dr3-2026-11-11/window-194/experiment.json`),
A100-SXM4-40GB on Modal, 2 cores, $0.000647 per s. Details, per-run tables and commands: `LEDGER.md`.

Pins: Astro branch `speedups-overnight-2026-11-16` (code head baa81fbd); ceridwen branch `speedups-overnight-2026-11-16`
(3b5177f) in potatoist314/ceridwen. The Astro ceridwen pin is not moved.

## Total

Base (production build) against the kept build, one container (run 15), empty compile cache:

| arm | process | cost per fit | sampler | ln L per s |
|---|---|---|---|---|
| dr3_cn_free_w | 176.4 -> 108.1 s (1.63x, -39 %) | $0.114 -> $0.070 | 98.5 -> 52.9 s | 56 k -> 102 k |
| dr3_plain_w | 113.1 -> 85.1 s (1.33x, -25 %) | $0.073 -> $0.055 | 49.8 -> 37.0 s | 98 k -> 130 k |

## Attempts

Gain: A100, same container, against the build before. Delta ln L: max over M1 dead points, CPU (exact float32 products)
and A100 (TF32 products).

| # | attempt | A100 gain | max delta ln L, CPU / A100 | kept |
|---|---|---|---|---|
| 1 | C/N factor: one gather of the 4 used terms; tables cut to alf coverage (ceridwen e7bb70e) | cn_free sampler 99.0 -> 90.7 s (-8 %) | 0 / 0 | yes |
| 2 | C/N factor: one matrix product for base and differential (ceridwen d03884c) | cn_free sampler 99.4 -> 71.4 s (-28 %) | 2.9e-11 / - | yes |
| N1 | `predict_jit` in notebook cell 3 (Astro 49de1f3f) | cn_free 147.1 -> 138.0 s (-6 %) | 0 / 0 | yes |
| N2 | output warm-up starts after the kernel compile (Astro 19e7a012) | cn_free 138.0 -> 135.8 s (-2 %) | 0 / 0 | yes |
| H1 | closed-over arrays become program arguments, `JAX_USE_SIMPLIFIED_JAXPR_CONSTANTS` (Astro 7ba8577d) | cn_free 135.8 -> 120.6 s (-11 %); cache 250 -> 3 MB | 2.4e-4 / - | yes |
| F2 | C/N tables stay float32, products at full precision (ceridwen c7aba78, 3b5177f) | against float64 tables: cn_free sampler 57.4 -> 52.9 s (-8 %, 2 of 2 pairs) | 2.2e-4 / 4.1e-3 (kept build) | yes |
| F3 | likelihood on the fitted pixels 1563 to 3192 only (ceridwen d03f336) | cn_free 116.2 -> 108.0 s (-7 %), sampler -15 %; plain sampler -21 % | 2.9e-11 / 5.3e-5 | yes |
| F4 | C/N table split into base and differential matrices (ceridwen 8ef5c8c) | cn_free sampler -2.6 % (process inside scatter) | 0 / 0 | yes |
| F5 | no sequential search loop in ln L (ceridwen 90bb0c7, fa4a7b1) | cn_free sampler -11 %, process -6.9 s; plain sampler -12 %, process -4.5 s | 0 / 1.5e-11 | yes |
| T1 | Triton GEMM off, `--xla_gpu_enable_triton_gemm=false` (Astro baa81fbd) | cn_free 104.7 -> 98.8 s (-5.7 %, 4 of 4 pairs); plain -2.5 % | - / 2.1e-3 | yes |
| F1 | SFH basis: one float32 matrix product (ceridwen ba88af2, reverted in 719b1b0) | TF32: plain sampler -10 %, cn_free -4 % | 3.6e-4 / 0.539 | no: his decision |
| F2t | F2 with TF32 products (ceridwen c7aba78 alone) | cn_free 140.0 -> 116.2 s (-17 %) | 2.2e-4 / 0.494 | no: his decision |
| F1h | F1 product at full precision (ceridwen 5f31bce, 18ff96c) | none: cn_free -1.7 s, plain -1.3 s, scatter 2.3 s (run 14) | - / 6.6e-3 | no |
| | cuBLASLt on, Triton GEMM for all products | no change (same ln Z, calls, programs) | - / 0 | no |
| | compile cache off; cache only compiles over 1 s | 135.8 -> 124.0 s, no gain; both superseded by H1 | 0 / 0 | no |
| P1 | all float32 products at full precision, `JAX_DEFAULT_MATMUL_PRECISION=highest` | cn_free +19.2 s (sampler +25 %); plain +6.9 s | - / A100 = CPU to 2.1e-4 | no: his decision |
| P3 | six bf16 passes on the F1 and F2 products (ceridwen c41bfcf) | cn_free +24.9 s (sampler +55 %); plain +15.4 s | - / top 30: 0.071 cn_free, 0.083 plain | no: slower |

## Full-fit check on 3 galaxies (M1, M9, M10; both arms)

Kept build against the production fit. ln L of the kept build at every stored sample on the CPU; samples reweighted by
exp(delta ln L). Limits: 0.05 sigma, 5 %, ln Z error 0.17 to 0.24.

| arm | galaxy | delta ln L max / rms | max median shift | max width change | delta ln Z |
|---|---|---|---|---|---|
| plain | M1 | 1.2e-4 / 3.4e-5 | 1.3e-6 sigma | 7.9e-5 % | -2.5e-5 |
| plain | M9 | 4.1e-5 / 1.1e-5 | 1.6e-6 sigma | 2.6e-5 % | -2.9e-6 |
| plain | M10 | 4.4e-5 / 8.9e-6 | 2.0e-6 sigma | 8.6e-5 % | +4.8e-6 |
| cn_free | M1 | 2.1e-4 / 5.4e-5 | 1.9e-6 sigma | 2.1e-4 % | -1.9e-5 |
| cn_free | M9 | 8.3e-5 / 2.2e-5 | 1.3e-6 sigma | 3.6e-4 % | -3.5e-6 |
| cn_free | M10 | 6.7e-5 / 1.5e-5 | 8.1e-7 sigma | 5.6e-5 % | +5.3e-6 |

On the A100, kept build against production, M1, points with ln L > 9e4 (run 14 against run 9):

| arm | points | max | rms | mean | relative max | implied median shift (top 30) |
|---|---|---|---|---|---|---|
| cn_free | 710 | 4.1e-3 | 6.3e-4 | +1.8e-4 | 4.5e-8 | 5.0e-5 sigma |
| plain | 613 | 7.6e-3 | 8.2e-4 | +1.0e-4 | 8.4e-8 | 4.2e-5 sigma |

- Pass in all 6 on the CPU; on the A100 the difference is 1/13 of the 0.1 limit.
- The A100 difference correlates with one parameter at 0.30 to 0.32 (`log_f_calib`, `logmass`). Production against
  itself in another container differs by 6e-11 and correlates with `logzsol` at 0.38; white noise of the same size
  gives 0.06 to 0.10.
- Not run: the A100 all-sample check of the kept build on 3 galaxies (about $0.25). The launch was refused: spend is
  above the $10 budget.

## Needs his decision

1. TF32 on the A100. XLA runs float32 matrix products in TF32 by default. Production already carries it (A100 against
   exact float32: rms 0.023, max 0.071 in the top 30 of ln L). Options:
   (a) F1 and F2 with TF32 products: about -9 s cn_free and -7 s plain per fit more (run 12, t5 against t6b and t6a);
   A100 delta ln L against production 0.54 (max), correlation 0.11 with `afe`, run 8 check passes (shift 0.028 sigma);
   (b) all products at full precision (P1): A100 = CPU to 2e-4, +19.2 s cn_free and +6.9 s plain per fit.
2. Line profile window (`sigma_max_kms`, not set in production): a truncation. Not measured in this run.
3. SFH-basis per-group bin truncation: 30 Sep 2026, max delta ln L 0.035 on the CPU. Not measured in this run.
4. Sampler settings (`num_delete` batch, live points, inner steps, logZ_tol): not measured; declined 25 Oct 2026.

## What I would try next

1. One compile cache for all galaxies of a run: 308 of 481 programs are the same for every galaxy; reading them
   saves 9.5 s per fit (run 3). The cache key now holds the cell.
2. C/N factor and model prediction on the fitted pixels only: the spectrum C/N table has 12332 columns, the model
   predicts 6166 pixels, 1392 are fitted. Estimate 0.2 to 0.3 ms of 1.4 ms per batch of 100.
3. 4-core container: the cell-4 compile (about 72 s cn_free) runs on 2 cores.
4. FilterSet setup: 45 eager compiles per fit (`filters/photometry.py:89,94`).

## Noticed, not done

- The default XLA path gave two ln Z for one build and seed (run 6 step 4; run 3 steps 2 and 5): autotuning picks
  kernels by timing. With Triton off the GEMM picks repeat.
- The quoted ln Z error (0.17 to 0.24) is up to 4 times smaller than the seed-to-seed ln Z scatter (run 5: -0.82 to +0.63).
- An A100-80GB container (run 11) ran the same fits 5 to 10 % slower than the 40 GB cards.
- Test change: `tests/test_emission_line_columns.py` all-constant column assertion is `assert_allclose(rtol=1e-14,
  atol=1e-300)` (XLA folds the constant program); the windowed against full assertion stays bitwise.

## Spend

15 A100 runs and one stopped launch on Modal, app `speedups-overnight-ab`, profile `liuhaoo3-14`: billed $10.84
(`modal billing report`), against about $10. No container left running.
