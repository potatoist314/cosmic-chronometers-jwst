# Speedups overnight, 16–17 Nov 2026

One first-time production fit of M1_210210 in the window-194 arms (`results/legac-dr3-2026-11-11/window-194/experiment.json`),
A100-SXM4-40GB on Modal, 2 cores, $0.000647 per s. Details, per-run tables and commands: `LEDGER.md`.

Pins: Astro branch `speedups-overnight-2026-11-16` (code head baa81fbd); ceridwen branch `speedups-overnight-2026-11-16`
(fa4a7b1) in potatoist314/ceridwen. The Astro ceridwen pin is not moved.

## Total

Base (production build) against the kept build, one container (run 12), empty compile cache:

| arm | process | cost per fit | sampler | ln L per s |
|---|---|---|---|---|
| dr3_cn_free_w | 181.4 -> 94.6 s (1.92x, -48 %) | $0.117 -> $0.061 | 98.4 -> 44.6 s | 56 k -> 121 k |
| dr3_plain_w | 112.1 -> 79.8 s (1.40x, -29 %) | $0.073 -> $0.052 | 49.5 -> 34.6 s | 98 k -> 142 k |
## Attempts

Gain: A100, same container, against the build before. Delta ln L: max over M1 dead points, CPU (exact float32 products)
and A100 (TF32 products).

| # | attempt | A100 gain | max delta ln L, CPU / A100 | kept |
|---|---|---|---|---|
| 1 | C/N factor: one gather of the 4 used terms; tables cut to alf coverage (ceridwen e7bb70e) | cn_free sampler 99.0 -> 90.7 s (-8 %) | 0 / 0 | yes |
| 2 | C/N factor: one matrix product for base and differential (ceridwen d03884c) | cn_free sampler 99.4 -> 71.4 s (-28 %) | 2.9e-11 / - | yes |
| F1 | SFH basis: one float32 matrix product (ceridwen ba88af2) | plain sampler 50.4 -> 45.4 s (-10 %); cn_free -4 % | 3.6e-4 / 0.539 | yes |
| N1 | `predict_jit` in notebook cell 3 (Astro 49de1f3f) | cn_free 147.1 -> 138.0 s (-6 %) | 0 / 0 | yes |
| N2 | output warm-up starts after the kernel compile (Astro 19e7a012) | cn_free 138.0 -> 135.8 s (-2 %) | 0 / 0 | yes |
| H1 | closed-over arrays become program arguments, `JAX_USE_SIMPLIFIED_JAXPR_CONSTANTS` (Astro 7ba8577d) | cn_free 135.8 -> 120.6 s (-11 %); cache 250 -> 3 MB | 2.4e-4 / - | yes |
| F2 | C/N tables stay float32 (ceridwen c7aba78) | cn_free 140.0 -> 116.2 s (-17 %), sampler -16 % | 2.2e-4 / 0.494 | yes |
| F3 | likelihood on the fitted pixels 1563 to 3192 only (ceridwen d03f336) | cn_free 116.2 -> 108.0 s (-7 %), sampler -15 %; plain sampler -21 % | 2.9e-11 / 5.3e-5 | yes |
| F4 | C/N table split into base and differential matrices (ceridwen 8ef5c8c) | cn_free sampler -2.6 % (process inside scatter) | 0 / 0 | yes |
| F5 | no sequential search loop in ln L (ceridwen 90bb0c7, fa4a7b1) | cn_free sampler -11 %, process -6.9 s; plain sampler -12 %, process -4.5 s | 0 / 1.5e-11 | yes |
| T1 | Triton GEMM off, `--xla_gpu_enable_triton_gemm=false` (Astro baa81fbd) | cn_free 104.7 -> 98.8 s (-5.7 %, 4 of 4 pairs); plain -2.5 % | - / 2.1e-3 | yes |
| | cuBLASLt on, Triton GEMM for all products | no change (same ln Z, calls, programs) | - / 0 | no |
| | compile cache off; cache only compiles over 1 s | 135.8 -> 124.0 s, no gain; both superseded by H1 | 0 / 0 | no |
| P1 | float32 products at full precision, `JAX_DEFAULT_MATMUL_PRECISION=highest` | cn_free +19.2 s (sampler +25 %); plain +6.9 s | - / A100 = CPU to 2.1e-4 | no: his decision |
| P2 | full precision on the F1 and F2 products only (ceridwen 5f31bce, 18ff96c; branch `-precision`) | t6a (F1 only): cn_free +4.6 s (sampler +6 %), plain +7.2 s; t6b (F1 and C/N): cn_free +9.0 s | - / t6a top 30: 0.071 cn_free, 0.083 plain (production 0.071, 0.083) | no: his decision |
| P3 | six bf16 passes on the F1 and F2 products (ceridwen c41bfcf) | cn_free +24.9 s (sampler +55 %); plain +15.4 s | - / top 30: 0.071 cn_free, 0.083 plain | no: slower than P2 |

## Full-fit check on 3 galaxies (M1, M9, M10; both arms)

Final build against the production fit, ln L of the final build on the A100 at every stored sample, samples
reweighted by exp(delta ln L). Limits: 0.05 sigma, 5 %, ln Z error 0.17 to 0.24.

| arm | galaxy | delta ln L max / rms | max median shift | max width change | delta ln Z |
|---|---|---|---|---|---|
| plain | M1 | 0.148 / 0.036 | 0.008 sigma | 0.38 % | +0.029 |
| plain | M9 | 0.217 / 0.027 | 0.008 sigma | 0.75 % | -0.017 |
| plain | M10 | 0.084 / 0.012 | 0.006 sigma | 0.24 % | +0.003 |
| cn_free | M1 | 0.148 / 0.032 | 0.009 sigma | 0.28 % | +0.024 |
| cn_free | M9 | 0.150 / 0.026 | 0.028 sigma | 0.66 % | -0.0004 |
| cn_free | M10 | 0.091 / 0.011 | 0.003 sigma | 0.12 % | -0.0005 |

- Pass in all 6. Triton off (T1) on top: shifts at most 9e-5 sigma, widths 4e-3 %. F5 is identical to 1.5e-11.
- Refits of the final build (run 6) differ from production by 0.068 to 0.099 sigma rms, the same as the unchanged
  build with another seed (0.083 to 0.098, run 5): a refit is another sampler realisation and cannot resolve 0.05 sigma.
- Delta ln L is relative 1e-6 and correlates 0.2 to 0.4 with `afe` or `logzsol`: the TF32 rounding below, not a
  float64 reordering.

## Needs his decision

1. TF32 on the A100. XLA runs float32 matrix products in TF32 by default. Production already carries it (A100 against
   exact float32: rms 0.023, max 0.071 in the top 30 of ln L; spectrum 1.2e-4); F1 and F2 put more of the model into
   float32 products (rms 0.040, max 0.131; spectrum 2.8e-4). Options: (a) accept, as now; (b) full precision
   everywhere, A100 = CPU to 2e-4, +19.2 s cn_free and +6.9 s plain per fit; (c) full precision on the F1 product only (t6a): the A100 error returns to the production
   level (rms 0.022 against 0.023), +4.6 s cn_free and +7.2 s plain per fit; (d) six bf16 passes
   (`BF16_BF16_F32_X6`) on the F1 and C/N products: the same error as (c) and slower, +24.9 s cn_free, +15.4 s plain.
2. Line profile window (`sigma_max_kms`, not set in production): a truncation. Not measured in this run.
3. SFH-basis per-group bin truncation: 30 Sep 2026, max delta ln L 0.035 on the CPU. Not measured in this run.
4. Sampler settings (`num_delete` batch, live points, inner steps, logZ_tol): not measured; declined 25 Oct 2026.

## What I would try next

1. One compile cache for all galaxies of a run: 308 of 481 programs are the same for every galaxy; reading them
   saves 9.5 s per fit (run 3). The cache key now holds the cell.
2. C/N factor and model prediction on the fitted pixels only: the spectrum C/N table has 12332 columns, the model
   predicts 6166 pixels, 1392 are fitted. Estimate 0.2 to 0.3 ms of 1.1 ms per batch of 100.
3. 4-core container: the cell-4 compile (about 64 s cn_free) runs on 2 cores.
4. FilterSet setup: 45 eager compiles per fit (`filters/photometry.py:89,94`).
5. A cheaper precision for the F1 product: `TF32_TF32_F32_X3` (3 TF32 passes) is not supported by `dot_general` on
   the CPU; a GPU-only switch would need a backend check.

## Noticed, not done

- The default XLA path gave two ln Z for one build and seed (run 6 step 4; run 3 steps 2 and 5): autotuning picks
  kernels by timing. With Triton off the GEMM picks repeat.
- The quoted ln Z error (0.17 to 0.24) is up to 4 times smaller than the seed-to-seed ln Z scatter (run 5: -0.82 to +0.63).
- An A100-80GB container (run 11) ran the same fits 5 to 10 % slower than the 40 GB cards.
- Test change: `tests/test_emission_line_columns.py` all-constant column assertion is `assert_allclose(rtol=1e-14,
  atol=1e-300)` (XLA folds the constant program); the windowed against full assertion stays bitwise.

## Spend

13 A100 runs on Modal, profile `liuhaoo3-14`: $9.68 of about $10. No container left running.
