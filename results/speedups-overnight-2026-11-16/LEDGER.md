# Speedups overnight 2026-11-16: ledger

Card t_2fac5263. Branch `speedups-overnight-2026-11-16` in both repos (Astro worktree
`tmp/worktrees/speedups-overnight`, ceridwen worktree inside it, from pin 13791e0).
Keep rule (lead's correction, 2026-11-17): the ln L difference is floating-point rounding of any precision
(float32 level included: relative 1e-7 to 1e-6, no trend), a real same-container A100 gain, and the full-fit
check on 3 galaxies (medians within 0.05 sigma, widths within 5%, ln Z within its error). Dropped terms,
truncation, coarser grids and sampler settings go to 'Needs his decision'.

## Baseline (no GPU spend; from `results/legac-dr3-2026-11-11/window-194/run/`)

| quantity | dr3_cn_free_w | dr3_plain_w |
|---|---|---|
| fits read | 153 | 164 |
| sampler wall, median | 94.4 s | 47.6 s |
| likelihood calls, median | 4.87 M | 4.48 M |
| likelihood calls per s, median | 51,600 | 94,100 |
| container time per fit (both arms mixed, 38-39 fits per container) | 137-149 s | same containers |
| billed per fit (container cost split evenly) | $0.094 | $0.094 |

- All 310 first-time fits ran mode `alone`: 795 programs compiled and about 870 fusions autotuned per fit.
- Fixed overhead outside the sampler: about 147 - (94.4 + 47.6) / 2 = 76 s per fit.
- The C/N response path costs 94.4 - 47.6 = 47 s of sampler time per C/N-free fit.
- Window: 1392 of 6166 native pixels fitted (M1_210210); every per-pixel step runs on all 6166.
- Local CPU (M1_210210, cn_free): 0.228 s per 100 likelihoods; CPU ln L against the GPU dead points
  differs by 0.02 median (float32 CPU against GPU), so every check compares CPU before against CPU after.

## Tools

- `lnl_check.py dump OUT.npz --settings JSON --dead ns_raw_dead.pkl`: builds the fit up to the sampler
  call, times each notebook cell, evaluates ln L at every 20th dead point (800 points).
- `lnl_check.py compare A.npz B.npz`: max |delta ln L| and the timing change.
- Dead points: `results/legac-dr3-2026-11-11/window-194/run/fits/dr3_cn_free_w/210210-M1_210210/ns_raw_dead_355.pkl`.

## Attempts

Delta ln L: CPU, 800 dead points of M1_210210 cn_free (every 20th), after against before. "Fit range" is the
710 points with ln L > 9e4 (the posterior bulk; ln L there is about 9.17e4).

| # | idea | change | CPU per 100 ln L | A100 (same container) | delta ln L, max / rms | kept | why |
|---|---|---|---|---|---|---|---|
| 1 | C/N `factor` gathered 9 terms and used 4; grid ratio computed on 10992 points, 7215 inside alf | ceridwen e7bb70e: one gather of the 4 used terms; tables cut to alf coverage, ratio padded with ones | 0.228 -> 0.198 s | run 1: cn_free sampler 99.0 -> 90.7 s (-8%), process 171 -> 162.7 s | 0 / 0 (0 of 800 differ) | KEPT | bit-identical on CPU and on the A100 (same ln Z and call count as the unchanged build) |
| 2 | C/N `factor` built two gathers of (4 terms, bins, groups, wavelengths) per parameter vector | ceridwen d03884c: base and summed differential from one float64 matrix product, coefficients (2, 9 x 4 x bins) | 0.198 -> 0.057 s (factor grid 56.2 -> 10.4 ms, factor spectrum 39.0 -> 9.0 ms) | run 2: cn_free sampler 99.4 -> 71.4 s (-28%), process 177.1 -> 151.5 s (-14%) | 2.9e-11 / 4.4e-12 (60 of 800 differ; relative rms 1.9e-16) | KEPT | float64 reordering; `tests/csp/test_cn_response.py` 7 passed |
| F1 | Main SFH basis read 4 corner gathers of (groups, bins, pixels) | ceridwen ba88af2 (branch `speedups-overnight-2026-11-16-f32`, on d03884c): one float32 matrix product, rows (afe, z, bin) | 0.057 -> 0.050 s (get_spectrum 23.8 -> 7.7 ms) | run 2, against a2: cn_free sampler 71.4 -> 68.5 s (-4%), process 151.5 -> 151.1 s; against base: plain sampler 50.4 -> 45.4 s (-10%), process 114.5 -> 108.0 s (-6%) | A100, 710 points: 0.539 / 0.063, mean +0.022 (TF32 products: "ln L on the A100"); CPU fit range 3.6e-4 / 8.7e-5 (relative 3.9e-9 / 9.5e-10, mean +1.6e-7, correlation with ln L -0.04); all 800: relative 9.2e-7 / 4.2e-8 | KEPT | float32 reordering on the CPU; on the A100 TF32 rounding, full-fit check passes (run 8); `tests/csp` 35 passed, 59 skipped |
| N1 | Notebook cell 3 called the un-jitted `joint_model.predict` once: 318 single-operation compiles | Astro 49de1f3f: `predict_jit` | CPU cell 3: 7.34 -> 3.89 s; compiles before the sampler 491 -> about 158 | run 3, against f1: cn_free process 147.1 -> 138.0 s (-6%), cell 3 26.6 -> 19.8 s | 0 / 0 (ln L untouched; the value only sets the initial `logmass`, printed value unchanged; same ln Z and call count on the A100) | KEPT | fewer compiles before the sampler |
| N2 | The output-cell warm-up thread compiled beside the sampler-kernel compile on a 2-core container | Astro 19e7a012: the thread waits for `ns_progress.jsonl` | not measurable on CPU | run 3, against N1: cn_free process 138.0 -> 135.8 s (-2%); plain f1 -> N2 103.4 -> 96.8 s (-6%, N1 and N2 together) | 0 / 0 (no change to ln L) | KEPT | small, and it stacks with N1 |
| F2 | C/N `factor` multiplied float32 tables by float64 coefficients: the 504x14430 and 504x12332 tables were promoted to float64 | ceridwen c7aba78: tables stay float32, coefficients cast to float32 | ln L 49.9 -> 43.7 ms per 100 (noisy machine); the factor times did not move on CPU | run 4, against N2: cn_free process 140.0 -> 116.2 s (-17%), sampler 69.9 -> 58.5 s (-16%), 77.5 k -> 92.8 k ln L per s; ln L batch of 100 in run 4: 1.70 ms | A100, 710 points: 0.494 / 0.021; CPU against F1, fit range: 2.2e-4 / 4.4e-5 (mean +2.0e-7, relative max 2.5e-9, correlation with ln L -0.03) | KEPT | float32 rounding (TF32 on the A100), full-fit check passes (run 8); `tests/csp/test_cn_response.py` passes |
| F3 | The likelihood (noise, order-10 calibration polynomial, 6 line profiles, 17x17 joint solve) ran on all 6166 native pixels; 1392 are fitted, inside pixels 1563 to 3192 | ceridwen d03f336: `run_sampler` cuts data, calibration basis and line columns to the first-to-last fitted pixel (`on_fitted_pixels`, 1630 pixels); predictions and stored outputs keep 6166 pixels | ln L 43.7 -> 39.6 ms per 100 | run 4, against F2: cn_free process 116.2 -> 108.0 s (-7%), sampler 58.5 -> 49.9 s (-15%), 109.3 k ln L per s, batch of 100 1.70 -> 1.37 ms; against N2, plain: process 97.8 -> 89.2 s (-9%), sampler 46.9 -> 37.2 s (-21%), 104.5 k -> 132.0 k ln L per s | against F2, fit range: 2.9e-11 / 1.1e-11 (269 of 710 differ, mean +3.3e-13) | KEPT | float64 reordering only: the cut pixels are masked; new test `test_loglike_on_the_fitted_pixels_equals_the_full_loglike` (rtol 1e-13, with and without line windows); 180 passed in the touched suites |
| F4 | The C/N coefficient matrix (2, 1008) is half zeros: the base product reads only the base term (112 rows), the differential only the 8 differential terms (896 rows) | ceridwen 8ef5c8c: two tables, base (112 x W) and differential (896 x W); 1008 x W multiply-adds per product pair, was 2016 x W | ln L 39.6 -> 37.3 ms per 100 (factor grid 12.1 -> 11.2, factor spectrum 10.6 -> 9.5 ms) | run 6, against F3 with N1, N2, H1: cn_free sampler 49.75 -> 48.45 s (-2.6 %), loglike part 1.361 -> 1.306 ms; process 99.65 -> 100.2 s (inside the scatter) | against F3: 0 / 0 (0 of 800 differ), CPU and A100 | KEPT | bit-identical (the removed products were with exact zeros); `tests/csp/test_cn_response.py` 7 passed |
| H1 | JAX wrote every closed-over array (SSP grid, C/N tables, projector tables) into each compiled program as a literal: 250 MB of programs per fit to compile, serialise and write | Astro 7ba8577d: `JAX_USE_SIMPLIFIED_JAXPR_CONSTANTS=True` in the fit kernel environment (`_worker_environment`, all backends); closed-over arrays become program arguments (JAX docs, internals/constants) | not a CPU cost | run 3, against N2: cn_free process 135.8 -> 120.6 s (-11%), plain 96.8 -> 93.8 s (-3%); compile cache 250 -> 3 MB, `save` 10.1 -> 3.0 s; sampler rate unchanged | against F4, fit range: 2.4e-4 / 4.0e-5 (mean -2.2e-5, relative max 2.6e-9) | KEPT | another compiled program, float rounding; reweighting on 6 fits passes (below); `tests/test_experiment.py` 39 passed |
| F5 | The lowered ln L ran 2 sequential search loops in every call: C/N `searchsorted` on 4 knots, line LSF `jnp.interp` on 6166 pixels (13 steps) | ceridwen 90bb0c7, fa4a7b1: LSF at the fixed line centres as a numpy constant (as `_window`), 4-knot search by comparison; no loop left in either arm | ln L identical (0 of 800 differ) | run 10, against final: cn_free sampler 48.8 -> 43.5 s (-11 %), process 104.6 -> 97.7 s (-6.6 %); plain sampler 39.4 -> 34.6 s (-12 %), process 89.7 -> 85.2 s (-5.0 %) | A100: 1.5e-11 / 5e-13, spectra identical; CPU 0 / 0 | KEPT | bit-identical on the A100 up to 1.5e-11; one test assertion relaxed to rtol 1e-14 (run 10) |
| T1 | XLA compiles most matrix products to Triton kernels and autotunes them for each new galaxy | Astro baa81fbd: `XLA_FLAGS` adds `--xla_gpu_enable_triton_gemm=false` in `_worker_environment` (appended to any flags already set) | not a CPU cost | runs 7, 8, against final: cn_free process 104.7 -> 98.8 s (-5.7 %, 4 of 4 pairs), sampler +1.4 s; plain 89.4 -> 87.1 s (-2.5 %, 2 of 3 pairs) | A100, every stored sample of 3 galaxies x 2 arms: max 2.1e-3, rms 1.4e-4 to 2.2e-4, relative max 2.3e-8; median shift max 9e-5 sigma, width 4e-3 % | KEPT | compile time; the same ln Z from compile to compile (the default gave two ln Z for one build and seed) |
| P1 | TF32 rounding of float32 products on the A100 | `JAX_DEFAULT_MATMUL_PRECISION=highest` (run 11, step environment) | none | run 11: cn_free process +19.2 s (sampler +25 %), plain +6.9 s (sampler +12 %) | A100 against CPU: 2.1e-4 / 7.9e-5 (was 0.131 / 0.040) | NOT KEPT | slower; a precision choice: Needs his decision |

## A100 run 1 (`runs/01-profile-a1/`, A100-SXM4-40GB, 2 cores, one container, $0.91)

| step | build | cell | process s | sampler s | calls M | ln Z | programs compiled |
|---|---|---|---|---|---|---|---|
| 0 | base | cn_free M1 | 177.5 | 98.8 | 5.521 | 91777.8563 | 795 |
| 1 | a1 | cn_free M1 | 164.3 | 91.5 | 5.530 | 91777.8772 | 800 |
| 2 | base | cn_free M1 | 171.8 | 99.5 | 5.530 | 91777.8772 | 795 |
| 3 | base | cn_free M1 | 169.7 | 98.5 | 5.521 | 91777.8563 | 795 |
| 4 | a1 | cn_free M1 | 161.0 | 89.9 | 5.521 | 91777.8563 | 800 |
| 5 | base | plain M1 | 109.1 | 50.1 | 4.860 | 91772.4911 | 648 |
| 6 | base | plain M1 | 110.2 | 50.1 | 4.860 | 91772.4911 | 648 |
| 7 | base | cn_free M9, cn_free M10, plain M9 in one kernel | 347.8 | 93.7, 85.0, 45.9 | 4.715, 4.438, 4.276 | 96413.1352, 104125.0366, 96414.2173 | 993 |

- The unchanged build gives two outcomes for one seed (steps 0/3 and step 2): production fits are not
  bitwise repeatable between runs. These two are the scatter reference for the full-fit check.
- Where an alone cn_free fit spends 170 s: imports and data 12 s; model build (notebook cell 3) 26 s, of which
  20 s is 497 small compiles; sampler cell 124 s = 99 s sampling + 25 s outside the sampler loop; output 2 s.
- Plain: cell 3 17 s (348 compiles, 13 s); sampler cell 72 s = 50 s sampling + 22 s outside.
- One kernel for several fits: the second cn_free fit takes 115 s of cells against 165 s alone; the third
  (plain) 66 s against 102 s.
- Compile sites before the sampler (CPU profile): 318 of about 490 came from one un-jitted `predict` call
  (N1). The other about 240 are single eager JAX operations in setup code: `filters/photometry.py:89,94` 45,
  `model/model.py:185,259` 61, `likelihood/emission_lines.py:268` 31, `cosmology.py:293-304` 39,
  `csp/csp_afe.py:132-273` 62.

## A100 run 2 (`runs/02-a2-f1/`, A100-SXM4-40GB, driver 620.70.06, 2 cores, one container, $0.90)

| step | build | cell | process s | sampler s | calls M | ln Z | programs compiled | cache MB |
|---|---|---|---|---|---|---|---|---|
| 0 | base | cn_free M1 | 177.1 | 99.4 | 5.521 | 91777.8563 | 795 | 176 |
| 1 | a2 | cn_free M1 | 152.9 | 72.7 | 5.530 | 91777.8772 | 789 | 191 |
| 2 | f1 | cn_free M1 (profiled) | 152.8 | 68.6 | 5.432 | 91777.7723 | 785 | 191 |
| 3 | a2 | cn_free M1 | 150.1 | 70.1 | 5.521 | 91777.8563 | 789 | 191 |
| 4 | f1 | cn_free M1 | 149.4 | 68.5 | 5.432 | 91777.7723 | 785 | 191 |
| 5 | base | plain M1 | 114.5 | 50.4 | 4.834 | 91772.3994 | 648 | 92 |
| 6 | f1 | plain M1 | 109.2 | 45.6 | 4.905 | 91772.1843 | 644 | 92 |
| 7 | f1 | plain M1 | 106.7 | 45.3 | 4.889 | 91772.0046 | 644 | 92 |

- a2 reproduces both outcomes of the unchanged build (ln Z ...8563 and ...8772): its 1e-11 differences do not
  change the sampler path. f1 gives a new path (ln Z 91777.7723, twice). The plain arm gives a new ln Z on each
  of 4 runs (base 91772.4911 twice in run 1, 91772.3994; f1 91772.1843, 91772.0046): run-to-run scatter 0.1 to 0.5.
- The sampler gain is larger than the process gain: the sampler cell's compiles took 75.6 s summed over threads
  (f1) against 59.0 s (base, run 1). The ln L compile alone: 9.3 s (base) -> 14.0 s (f1).

A100 seconds per batch of ln L (ms, batch of 100; `lnl_check.py parts` on the GPU, steps 8 to 11):

| part | base cn_free | f1 cn_free | f1 cn_free, batch 400 | f1 plain |
|---|---|---|---|---|
| ln L | 3.49 | 2.08 | 5.98 | 1.29 |
| predict | 2.59 | 1.20 | 3.97 | 0.50 |
| likelihood given the prediction | 0.78 | 0.92 | 2.18 | 0.83 |
| transforms | 0.20 | 0.22 | 0.31 | 0.18 |
| get_spectrum | 0.45 | 0.21 | 0.62 | 0.19 |
| C/N factor, model grid | 1.27 | 0.44 | 1.21 | |
| C/N factor, spectrum | 0.82 | 0.39 | 1.09 | |

- After f1 the likelihood given the prediction (calibration polynomial and noise on all 6166 native pixels) is
  the largest part: 0.92 of 2.08 ms (cn_free), 0.83 of 1.29 ms (plain).

## Kernel program (CPU, f1, cn_free M1)

- The sampler step kernel is lowered with its data inside: 351 MB of program text, constants 910x17236 f32
  (63 MB), 504x14430 f64 (58 MB), 504x12332 f64 (50 MB).
- `JAX_USE_SIMPLIFIED_JAXPR_CONSTANTS=True` (JAX 0.10.2 `docs/internals/constants.md`) passes them as
  arguments: 1.4 MB of text, CPU compile 4.1 -> 3.2 s. ln L changes at float32 rounding: fit range max 2.4e-4,
  rms 4.0e-5, mean -2.2e-5; all 800 relative max 3.7e-7, rms 2.1e-8.
- With the constants out, the kernels of M1 and M9 have the same 16362 lines and differ in array shapes (SSP
  support 8618 against 8693 wavelengths, native pixels 6166 against 5742, bands 28 against 30) and in 44 scalar
  constants. One compiled kernel for all galaxies needs padded shapes and scalar arguments.

## Production compile cache (read from `scripts/experiment.py` `cache_key`, `scripts/modal_gpu.py`)

- The cache key holds the cell (target and seed): a saved cache is read again only when the same cell is fit
  again at the same pins. Each first-time fit writes about 800 programs (176 to 191 MB cn_free, 92 MB plain),
  tars them to the cache Volume and commits.
- Production containers: container seconds minus the fit processes leaves 3.4 to 12.9 s per fit (8 containers
  of 38 to 39 fits) for bootstrap, `save`, `keep` and the commits.

## Where a batch of ln L goes on the A100 (f1, cn_free M1, run 2 parts at batch 100 and 400)

- t = a + b n: ln L 0.78 ms of host dispatch per call plus 1.3 ms per 100 points. Inside the sampler kernel
  one batch of 100 takes 1.26 ms (68.5 s / 5.43 M calls x 100): the sampler loop is bound by GPU throughput,
  not by the host.
- Per 100 points (ms): likelihood given the prediction 0.42; C/N factor on the model grid 0.26; projection,
  photometry and the rest of `predict` 0.26; C/N factor on the spectrum 0.23; `get_spectrum` 0.14;
  transforms 0.03.

## Likelihood of the window fits (cn_free M1)

- 6166 native pixels, 1392 fitted, all inside pixels 1563 to 3192 (1630 pixels). 6 free emission lines
  (`EmissionLineColumns`, no `sigma_max_kms`: each profile was evaluated on all 6166 pixels).
  `PolynomialCalibration(order=10, fit_constant=True, marginalize=True)`; `joint_model._eline_system` is
  None, so ln L goes through `likelihood.loglike` -> `calibrate_with_lines`;
  `DiagonalNoiseModel(use_fractional=True)`; projector "chain".
- F3 cuts the likelihood side. The model side still predicts 6166 pixels and the C/N spectrum table has
  12332 columns: cutting those needs the projector to keep its full grids and a sampler-only prediction
  path. Not built; estimate 0.2 to 0.3 ms of 1.3 per batch.

## Part A rows against the current code (ceridwen 13791e0)

| row of `wiki/notes/speedups-follow-ups.md` | state in the current code | action |
|---|---|---|
| doublet barrier per dot | in the code: `emission_lines.py` `columns` ends in `optimization_barrier` | none |
| doublet as elementwise sum | not measured; the columns now span 1630 pixels (F3) | open, small |
| windowed line Gram | production sets no `sigma_max_kms`: each profile ran on every pixel | F3 cuts the pixels; a profile window is a truncation (his decision) |
| `jax.jit` of line columns | the sampler builds the columns inside the jitted ln L | none |
| `jax.jit` of posterior draws | in the code | none |
| larger likelihood batch | the batch is `num_delete`, a sampler setting | his decision |
| compacted likelihood batch; masked-row compaction | 4774 of 6166 rows were masked | F3 |
| FilterSet numpy rewrite | `filters/photometry.py:89,94`: 45 eager compiles per fit | open |
| shared KL histogram sort | not in the sampler loop | none |
| XLA GEMM settings | measured in runs 7 and 8 (Triton GEMM off, cuBLASLt, `triton_gemm_any`) and run 11 (float32 matmul precision) | see those runs |
| float32 or power-of-two FFT | the lowered ln L has 4 FFTs, complex128, at lengths 4608 = 2^9 3^2 and 18432 = 2^11 3^2: the lengths are already smooth | float32 FFT open, not measured; C/N tables float32 in F2 |

## Full-fit check: one refit cannot meet 0.05 sigma

`compare_fits.py` on fits of one galaxy, one seed (max |median shift| in sigma of the reference fit, max
width change, delta ln Z; effective samples 4150 to 4700; quoted ln Z error 0.24 cn_free, 0.20 plain):

| pair | median shift max / rms | width change max | delta ln Z |
|---|---|---|---|
| cn_free M1, production against run-2 base (same build, same host class) | 0 | 0 | 0 |
| cn_free M1, base against a2 (delta ln L 1e-11) | 0.110 (`logsfr_ratios[13]`) / 0.059 | 19.3 % | +0.021 |
| cn_free M1, base against f1 | 0.307 (`logsfr_ratios[1]`) / 0.089 | 70.4 % | -0.084 |
| cn_free M1, a2 against f1 | 0.391 / 0.100 | 94.4 % | -0.105 |
| plain M1, production against run-2 base (same build and seed, another host) | 0.111 / 0.049 | 10.7 % | -0.092 |
| plain M1, production against f1 | 0.266 (`sigma_smooth`) / 0.110 | 17.7 % | -0.307 |

- A difference of 1e-11 in ln L changes a slice-sampling accept somewhere and the run becomes an independent
  realisation: 0.11 sigma and 19 % between two builds that agree to 1e-11. The unchanged build on another
  host gives the same scatter. The 0.05 sigma and 5 % limits are below the scatter of the sampler itself
  (about 1/sqrt(4500) = 0.015 per parameter in the mean, larger in the tails of 26 parameters and in the
  prior-dominated SFH ratios).
- The check is therefore done two ways. (1) Without sampler noise: ln L of the base build and of the final
  build at every stored sample of the production fit; the samples get the weight w exp(delta ln L)
  (`reweight.py`); medians, widths and ln Z follow. (2) Refits of the final build against the scatter of
  base refits with another seed (run 5).

### Reweighting, base against F3 (all kept changes), CPU float64 path

| fit | samples with weight | delta ln L max / rms / mean | largest correlation with a parameter | delta ln Z | median shift max | width change max |
|---|---|---|---|---|---|---|
| plain M1 | 9210 | 3.6e-4 / 8.4e-5 / -1.5e-6 | 0.021 | -6.9e-7 | 4.8e-6 sigma | 2.0e-4 % |
| plain M9 | 8587 | 1.4e-4 / 2.8e-5 / +1.4e-7 | 0.029 | +2.1e-7 | 5.4e-7 sigma | 9.7e-5 % |
| plain M10 | 8733 | 1.2e-4 / 2.4e-5 / -4.1e-7 | 0.021 | -3.7e-7 | 6.7e-6 sigma | 1.4e-4 % |
| cn_free M1 | 10133 | 3.9e-4 / 9.2e-5 / -1.8e-6 | 0.019 | -1.1e-6 | 4.1e-6 sigma | 6.2e-4 % |
| cn_free M9 | 9061 | 1.8e-4 / 3.6e-5 / -3.7e-7 | 0.047 (`nfe`) | -4.4e-7 | 9.0e-7 sigma | 1.1e-3 % |
| cn_free M10 | 9269 | 1.2e-4 / 2.6e-5 / +3.9e-7 | 0.025 | +3.5e-7 | 1.7e-6 sigma | 8.1e-4 % |

- All stored samples (13,900 to 17,300 per fit); "with weight" counts weights above 1e-12 of the largest.
  Relative delta ln L at most 4.2e-9. Limits: 0.05 sigma, 5 %, ln Z error 0.20 to 0.24: passed by four
  orders of magnitude on the 3 galaxies in both arms, on the CPU. The A100 changes ln L by more than the CPU
  does: see "ln L on the A100, build against build" below, which is the check that counts.
- Outputs: scratch `rw/{base,f3}/c{0..5}/lnl.npz` (not kept); command `reweight.py RESULT.h5 BASE.npz CHANGED.npz`.

## A100 run 3 (`runs/03-notebook-cache/`, A100-SXM4-40GB, driver 610.57.04, 2 cores, one container, $1.29)

Each step is one full fit on an empty compile cache unless "seeded". Seconds.

| step | build | setting | cell | process | sampler | cell 3 | cell 4 | cache | ln Z | calls |
|---|---|---|---|---|---|---|---|---|---|---|
| 0 | f1 | | cn_free M1 | 151.0 | 69.2 | 27.5 | 100.6 | 191 MB | 91777.7723 | 5.432 M |
| 4 | f1 | | cn_free M1 | 143.1 | 68.0 | 25.7 | 98.3 | 191 MB | 91777.7723 | 5.432 M |
| 1 | n1 | | cn_free M1 | 138.0 | 68.2 | 19.8 | 99.1 | 250 MB | 91777.7723 | 5.432 M |
| 2 | n2 | | cn_free M1 | 135.8 | 69.7 | 19.5 | 97.7 | 250 MB | 91777.7723 | 5.432 M |
| 5 | n2 | | cn_free M1 | 135.7 | 69.0 | 19.7 | 97.1 | 250 MB | 91777.8151 | 5.388 M |
| 3 | n2 | constants hoisted | cn_free M1 | 120.8 | 69.5 | 12.1 | 89.4 | 3 MB | 91777.8117 | 5.418 M |
| 6 | n2 | constants hoisted | cn_free M1 | 120.4 | 69.8 | 11.7 | 89.7 | 3 MB | 91777.8117 | 5.418 M |
| 7 | n2 | compile cache off | cn_free M1 | 124.0 | 68.2 | 13.5 | 90.3 | 0 | 91777.8151 | 5.388 M |
| 8 | n2 | cache only compiles over 1 s | cn_free M1 | 138.2 | 69.6 | 19.7 | 97.6 | 245 MB | 91777.7723 | 5.432 M |
| 9 | n2 | | cn_free M9 | 127.6 | 60.5 | 20.1 | 88.8 | 247 MB | 96412.7622 | 4.656 M |
| 10 | n2 | seeded with the cache of step 9 | cn_free M1 | 126.2 | 69.1 | 14.1 | 94.3 | 495 MB | 91777.7723 | 5.432 M |
| 11 | n2 | constants hoisted | cn_free M9 | 113.7 | 63.1 | 12.1 | 83.0 | 3 MB | 96412.8180 | 4.611 M |
| 12 | n2 | constants hoisted, seeded with step 11 | cn_free M1 | 111.2 | 69.9 | 6.2 | 87.6 | 5 MB | 91777.8378 | 5.442 M |
| 13 | f1 | | plain M1 | 103.4 | 45.7 | 17.3 | 67.5 | 92 MB | 91772.1843 | 4.905 M |
| 14 | n2 | | plain M1 | 96.8 | 46.2 | 11.9 | 66.3 | 119 MB | 91772.1843 | 4.905 M |
| 15 | n2 | constants hoisted | plain M1 | 93.8 | 47.5 | 9.9 | 65.3 | 3 MB | 91772.1841 | 4.920 M |

- N1 (`predict_jit` in cell 3): cn_free process 147.1 (mean of steps 0, 4) -> 138.0 s; cell 3 26.6 -> 19.8 s. KEPT.
- N2 (warm-up thread after the kernel compile): 138.0 -> 135.8 s (steps 2, 5). Plain f1 -> n2: 103.4 -> 96.8 s. KEPT.
- Constants hoisted (`JAX_USE_SIMPLIFIED_JAXPR_CONSTANTS=True`: arrays closed over by a jitted function become
  arguments of the compiled program, not literals inside it): cn_free 135.8 -> 120.6 s (-11%), plain 96.8 -> 93.8 s
  (-3%). The cache directory falls from 250 MB to 3 MB; `save` of it 10.1 -> 3.0 s; `keep` 2.8 s both ways
  (steps 0, 6). The sampler rate is unchanged. Different compiled program: ln L changes at rounding level
  (another sampler realisation).
- Compile cache off: 135.8 -> 124.0 s. Writing 250 MB of programs costs 12 s; hoisting removes that cost and keeps the cache.
- Cache only compiles over 1 s: no gain (the large programs are the cost).
- Cache of another galaxy (steps 10, 12): 308 of 481 programs are the same for every galaxy; reading them saves
  9.5 s per fit (135.8 -> 126.2 s; hoisted 120.6 -> 111.2 s). Production gives each fit an empty cache.
- Same build, same seed, same container, empty cache: steps 2 and 5 differ (ln Z 91777.7723 and 91777.8151). XLA
  times its autotuning candidates at compile time, so two compiles can pick different kernels.

## A100 run 5 (`runs/05-validate/`, A100-SXM4-40GB, 2 cores, one container, $0.59): refits against production

`compare_fits.py`, production fit -> refit. "Other seed" is the unchanged build with seed 20260833: the scatter of
the sampler alone.

| fit | refit | max, rms median shift (sigma) | max width change | ln Z production -> refit | process, sampler (s) |
|---|---|---|---|---|---|
| cn_free M9 | F3, same seed | 0.202, 0.078 | 18.4 % | 96413.166 +/- 0.186 -> 96412.681 +/- 0.189 | 104.8, 41.3 |
| cn_free M10 | F3, same seed | 0.180, 0.095 | 32.3 % | 104125.068 +/- 0.177 -> 104124.955 +/- 0.178 | 94.8, 39.1 |
| plain M9 | F3, same seed | 0.142, 0.078 | 21.3 % | 96414.247 +/- 0.176 -> 96413.925 +/- 0.175 | 87.9, 33.5 |
| plain M10 | F3, same seed | 0.203, 0.079 | 20.7 % | 104123.750 +/- 0.173 -> 104124.566 +/- 0.171 | 79.8, 30.1 |
| cn_free M1 | base, other seed | 0.258, 0.098 | 41.7 % | 91777.893 +/- 0.236 -> 91778.524 +/- 0.243 | 170.0, 100.6 |
| plain M1 | base, other seed | 0.255, 0.098 | 57.9 % | 91772.524 +/- 0.201 -> 91772.315 +/- 0.237 | 108.7, 50.2 |
| cn_free M9 | base, other seed | 0.235, 0.095 | 22.7 % | 96413.166 +/- 0.186 -> 96413.301 +/- 0.235 | 158.0, 86.8 |
| plain M9 | base, other seed | 0.220, 0.083 | 20.0 % | 96414.247 +/- 0.176 -> 96413.426 +/- 0.229 | 105.6, 47.4 |

The F3 refits differ from production by no more than two seeds of the unchanged build differ. Two seeds of the
unchanged build differ in ln Z by up to 0.82, against a quoted error of 0.2.

## A100 run 4 (`runs/04-f2-f3/`, A100-SXM4-40GB, driver 610.57.04, 2 cores, one container, $0.81)

Full fits of M1 on an empty compile cache; seconds.

| step | build | cell | process | sampler | ln L per s | cell 3 | cell 4 | cache | ln Z | calls |
|---|---|---|---|---|---|---|---|---|---|---|
| 0 | n2 | cn_free | 142.8 | 70.5 | 77,077 | 20.7 | 99.7 | 250 MB | 91777.7723 | 5.432 M |
| 3 | n2 | cn_free | 137.2 | 69.2 | 77,835 | 19.3 | 97.8 | 250 MB | 91777.8151 | 5.388 M |
| 1 | f2 | cn_free | 115.3 | 58.7 | 92,896 | 15.5 | 81.1 | 229 MB | 91777.7383 | 5.450 M |
| 4 | f2 | cn_free | 117.0 | 58.2 | 92,741 | 15.6 | 81.7 | 229 MB | 91778.0232 | 5.399 M |
| 2 | f3 | cn_free | 108.1 | 50.0 | 109,085 | 15.7 | 72.5 | 225 MB | 91777.7383 | 5.450 M |
| 5 | f3 | cn_free | 107.8 | 49.8 | 109,461 | 15.7 | 73.4 | 225 MB | 91777.7383 | 5.450 M |
| 6 | n2 | plain | 98.2 | 46.9 | 104,279 | 11.9 | 67.5 | 119 MB | 91772.0046 | 4.889 M |
| 8 | n2 | plain | 97.3 | 46.8 | 104,771 | 11.6 | 67.2 | 119 MB | 91772.1843 | 4.905 M |
| 7 | f3 | plain | 89.0 | 37.3 | 131,540 | 11.8 | 57.8 | 115 MB | 91772.1843 | 4.905 M |
| 9 | f3 | plain | 89.3 | 37.0 | 132,473 | 12.0 | 58.5 | 115 MB | 91772.1843 | 4.905 M |

ln L parts on the A100, ms per batch of 100 (steps 10 to 12):

| part | f2 cn_free | f3 cn_free | f3 plain |
|---|---|---|---|
| loglike (the sampler's function) | 1.703 | 1.367 | 1.022 |
| predict | 0.798 | 0.786 | 0.499 |
| likelihood given prediction, all 6166 pixels | 0.969 | 0.982 | 0.876 |
| get_spectrum | 0.230 | 0.237 | 0.229 |
| C/N factor grid | 0.278 | 0.270 | |
| C/N factor spectrum | 0.231 | 0.260 | |

- F2 (float32 C/N tables): cn_free process 140.0 -> 116.2 s, sampler 69.9 -> 58.5 s. 17 s of cell 4: 11.4 s of
  sampler and 5.6 s of compile (the float64 copies of the tables were literals in each program).
- F3 (likelihood on the fitted pixel range): cn_free process 116.2 -> 108.0 s, sampler 58.5 -> 49.9 s; plain
  process 97.8 -> 89.2 s, sampler 46.9 -> 37.2 s.
- The F3 fits of plain M1 have the ln Z and call count of the n2 fit of step 8: the 1e-11 change did not move a
  single accept in that run.

### Reweighting, base against the final build (F4 with hoisted constants), CPU

| fit | samples with weight | delta ln L max / rms / mean | correlation with ln L | largest correlation with a parameter | delta ln Z | median shift max | width change max |
|---|---|---|---|---|---|---|---|
| plain M1 | 9210 | 3.7e-4 / 9.1e-5 / -2.6e-5 | 0.010 | 0.041 (`diffuse_tau_noll`) | -2.5e-5 | 3.5e-6 sigma | 2.1e-4 % |
| plain M9 | 8587 | 1.4e-4 / 3.0e-5 / -3.0e-6 | 0.011 | 0.029 | -2.5e-6 | 3.0e-6 sigma | 1.8e-4 % |
| plain M10 | 8733 | 1.3e-4 / 2.5e-5 / +4.3e-6 | 0.008 | 0.043 (`diffuse_tau_noll`) | +4.3e-6 | 4.7e-6 sigma | 1.3e-4 % |
| cn_free M1 | 10133 | 3.9e-4 / 9.6e-5 / -2.1e-5 | 0.006 | 0.018 | -2.0e-5 | 6.6e-6 sigma | 5.6e-4 % |
| cn_free M9 | 9061 | 1.6e-4 / 3.7e-5 / -3.8e-6 | 0.014 | 0.043 (`nfe`) | -3.8e-6 | 1.7e-6 sigma | 1.1e-3 % |
| cn_free M10 | 9269 | 1.3e-4 / 2.7e-5 / +5.7e-6 | 0.004 | 0.057 (`diffuse_tau_noll`) | +5.7e-6 | 1.9e-6 sigma | 9.7e-4 % |

- Relative delta ln L at most 4.3e-9. The mean offset (up to 2.6e-5) is a constant in ln L. The correlations
  are of a difference with rms below 1e-4: the reweighted medians move by at most 7e-6 sigma.
- Tests on the final build: ceridwen `tests/csp tests/likelihood tests/test_emission_line_columns.py
  tests/test_eline_marginalisation.py tests/test_baked_runtime.py` 145 passed, 93 skipped on 8ef5c8c
  (157 passed, 101 skipped on fa4a7b1, run 10 section); Astro
  `tests/test_cn_response_production.py`, `tests/test_cn_mock_data.py` 3 passed (run on a copy of
  `.stage/final` with the raw data of the main checkout); `tests/test_experiment.py` 39 passed.

## A100 run 6 (`runs/06-final/`, A100-SXM4-40GB, driver 610.57.04, 2 cores, one container, $0.84): base against the final build

Full fits on an empty compile cache; seconds. `final` is Astro 7ba8577d with ceridwen 8ef5c8c; `f3` here is
ceridwen d03f336 with the Astro changes N1, N2, H1 (the final build without F4).

| step | build | cell | process | sampler | ln L per s | cell 3 | cell 4 | compiled | cache | ln Z | calls |
|---|---|---|---|---|---|---|---|---|---|---|---|
| 0 | base | cn_free M1 | 172.4 | 98.1 | 56,301 | 26.0 | 122.6 | 795 | 176 MB | 91777.8563 | 5.521 M |
| 1 | final | cn_free M1 | 102.1 | 48.8 | 109,349 | 11.7 | 70.1 | 487 | 3 MB | 91778.2116 | 5.331 M |
| 3 | final | cn_free M1 | 98.2 | 48.1 | 110,722 | 11.2 | 68.1 | 487 | 3 MB | 91778.2116 | 5.331 M |
| 2 | f3 | cn_free M1 | 99.5 | 49.6 | 107,508 | 11.5 | 69.6 | 485 | 3 MB | 91778.2116 | 5.331 M |
| 4 | f3 | cn_free M1 | 99.8 | 49.9 | 107,596 | 11.8 | 69.4 | 485 | 3 MB | 91778.0968 | 5.365 M |
| 5 | base | plain M1 | 106.7 | 50.2 | 96,747 | 16.4 | 71.4 | 648 | 92 MB | 91772.4911 | 4.860 M |
| 6 | final | plain M1 | 86.7 | 39.4 | 124,945 | 9.9 | 57.7 | 472 | 3 MB | 91772.1841 | 4.920 M |
| 7 | final | plain M1 | 85.2 | 39.5 | 124,538 | 9.4 | 57.4 | 472 | 3 MB | 91772.1841 | 4.920 M |
| 8 | final | cn_free M9 | 90.4 | 40.7 | 113,577 | 11.8 | 60.0 | 489 | 3 MB | 96412.9838 | 4.627 M |
| 9 | final | cn_free M10 | 89.4 | 42.3 | 104,645 | 11.1 | 60.1 | 489 | 3 MB | 104125.0045 | 4.426 M |
| 10 | final | plain M9 | 80.0 | 33.0 | 131,151 | 9.9 | 50.8 | 473 | 3 MB | 96413.8621 | 4.334 M |
| 11 | final | plain M10 | 79.7 | 35.0 | 118,999 | 9.7 | 51.5 | 473 | 3 MB | 104124.5916 | 4.167 M |

ln L parts on the A100, cn_free M1, ms per batch of 100 (steps 12, 13):

| part | f3 | f4 |
|---|---|---|
| loglike (the sampler's function) | 1.361 | 1.306 |
| predict | 0.808 | 0.763 |
| likelihood given prediction | 0.926 | 0.957 |
| get_spectrum | 0.226 | 0.247 |
| C/N factor grid | 0.302 | 0.252 |
| C/N factor spectrum | 0.232 | 0.229 |

- Total, one first-time fit of M1 in one container (cost at $0.84 / 1298 s = $0.000647 per s):

| arm | base process | final process (mean of 2) | change | base cost | final cost | base sampler | final sampler |
|---|---|---|---|---|---|---|---|
| dr3_cn_free_w | 172.4 s | 100.2 s | -42 % (1.72x) | $0.112 | $0.065 | 98.1 s | 48.5 s |
| dr3_plain_w | 106.7 s | 86.0 s | -19 % (1.24x) | $0.069 | $0.056 | 50.2 s | 39.5 s |

- F4 (C/N table split into base and differential matrices): sampler 49.75 -> 48.45 s (-2.6 %), loglike part
  1.361 -> 1.306 ms (-4 %), process 99.65 -> 100.2 s (no gain inside the 2 to 4 s scatter of a pair). ln L on
  the GPU is identical to F3 at all 800 points; step 1 and step 2 have the same ln Z and call count. KEPT as a
  bit-identical change with a sampler gain; the process gain is not shown.
- The base fit of this container is slower than in run 2 (171 s) by no more than the scatter.

## A100 run 7 (`runs/07-gemm/`, A100-SXM4-40GB, driver 610.57.04, 2 cores, one container, $0.62): XLA GEMM settings

Final build, full fits of M1 on an empty compile cache; seconds. Flag names read from the strings of the
installed jaxlib 0.10.2.

| step | `XLA_FLAGS` | cell | process | sampler | ln L per s | cell 3 | cell 4 | tuned | ln Z | calls |
|---|---|---|---|---|---|---|---|---|---|---|
| 0 | none (default) | cn_free | 107.0 | 49.1 | 108,601 | 12.8 | 71.3 | 658 | 91778.2116 | 5.331 M |
| 2 | none (default) | cn_free | 105.1 | 50.2 | 106,202 | 12.2 | 72.4 | 658 | 91778.2116 | 5.331 M |
| 1 | `--xla_gpu_enable_triton_gemm=false` | cn_free | 100.2 | 51.5 | 104,538 | 10.6 | 68.9 | 644 | 91777.9194 | 5.389 M |
| 3 | `--xla_gpu_enable_triton_gemm=false` | cn_free | 96.8 | 50.7 | 106,247 | 10.4 | 67.5 | 644 | 91777.9194 | 5.389 M |
| 4 | Triton off and `--xla_gpu_enable_cublaslt=true` | cn_free | 96.5 | 50.6 | 106,391 | 10.3 | 67.5 | 644 | 91777.9194 | 5.389 M |
| 5 | `--xla_gpu_triton_gemm_any=true` | cn_free | 101.8 | 49.0 | 108,753 | 12.0 | 70.1 | 658 | 91778.2116 | 5.331 M |
| 6 | none (default) | plain | 88.2 | 39.6 | 124,208 | 9.5 | 58.5 | 602 | 91772.1841 | 4.920 M |
| 7 | `--xla_gpu_enable_triton_gemm=false` | plain | 85.2 | 39.4 | 124,156 | 9.1 | 55.6 | 585 | 91772.3853 | 4.894 M |
| 8 | Triton off and `--xla_gpu_enable_cublaslt=true` | plain | 81.4 | 39.2 | 124,751 | 8.5 | 54.3 | 585 | 91772.3853 | 4.894 M |

- `--xla_gpu_triton_gemm_any=true` and `--xla_gpu_enable_cublaslt=true` change nothing: same ln Z, call count
  and tuned-program count as the arm beside them.
- Triton GEMM off (matrix products go to cuBLAS): cn_free process 106.1 -> 98.5 s over the two pairs; the
  compile is shorter (cell 3 12.5 -> 10.5 s, cell 4 71.9 -> 68.2 s) and the sampler is 1 to 3 % slower
  (49.7 -> 51.1 s). Bench steps 9, 10: loglike 1.348 -> 1.251 ms, its compile 9.44 -> 6.90 s. Plain: one pair,
  88.2 -> 85.2 s. Run 8 repeats the pairs in both arms.

## A100 run 8 (`runs/08-triton-off/`, A100-SXM4-40GB, driver 620.70.06, 2 cores, one container, $0.87): all-sample check and Triton GEMM off

Final build (Astro 7ba8577d, ceridwen 8ef5c8c). Steps 0 to 11 evaluate ln L on the A100 at every stored
posterior sample (`lnl_check.py parts --step 1`); steps 12 to 19 are full fits of M1 on an empty compile cache.

### Full-fit check on 3 galaxies: final build against the production fit, every stored sample, on the A100

Base: the production ln L stored with the samples. Changed: the final build at the same points. The samples
get the weight w exp(delta ln L) (`reweight.py`); sigma is half the 16 to 84 % range of the production
posterior. Limits: 0.05 sigma, 5 %, the quoted ln Z error (0.17 to 0.24).

| arm | galaxy | samples with weight | delta ln L max | rms | mean | relative max | delta ln Z | max median shift | max width change | largest correlation with a parameter |
|---|---|---|---|---|---|---|---|---|---|---|
| plain | M1_210210 | 9,210 | 0.148 | 0.036 | +0.029 | 1.6e-6 | +0.029 | 0.008 sigma | 0.38 % | 0.28 (afe) |
| plain | M9_227630 | 8,587 | 0.217 | 0.027 | -0.014 | 2.3e-6 | -0.017 | 0.008 sigma | 0.75 % | 0.39 (logzsol) |
| plain | M10_201233 | 8,733 | 0.084 | 0.012 | +0.004 | 8.1e-7 | +0.003 | 0.006 sigma | 0.24 % | 0.25 (logsfr_ratios[11]) |
| cn_free | M1_210210 | 10,133 | 0.148 | 0.032 | +0.024 | 1.6e-6 | +0.024 | 0.009 sigma | 0.28 % | 0.24 (afe) |
| cn_free | M9_227630 | 9,061 | 0.150 | 0.026 | -0.003 | 1.6e-6 | -0.0004 | 0.028 sigma | 0.66 % | 0.40 (logzsol) |
| cn_free | M10_201233 | 9,269 | 0.091 | 0.011 | +0.0003 | 8.8e-7 | -0.0005 | 0.003 sigma | 0.12 % | 0.21 (logsfr_ratios[11]) |

- Medians, widths and ln Z pass the limits on the 3 galaxies in both arms.
- The delta ln L is float32-product size (relative 1e-6), not float64 size, and it correlates with a
  parameter at 0.2 to 0.4. See "ln L on the A100 against the CPU" for the cause.

### Triton GEMM off against the default, every stored sample

| arm | galaxy | delta ln L max | rms | mean | relative max | delta ln Z | max median shift | max width change |
|---|---|---|---|---|---|---|---|---|
| plain | M1_210210 | 2.1e-3 | 2.1e-4 | +1.4e-4 | 2.3e-8 | +1.3e-4 | 2.7e-5 sigma | 6.1e-4 % |
| plain | M9_227630 | 6.6e-4 | 1.4e-4 | +1.6e-6 | 6.8e-9 | +5.3e-6 | 6.2e-5 sigma | 1.8e-3 % |
| plain | M10_201233 | 9.0e-4 | 1.6e-4 | +9.3e-6 | 8.6e-9 | +1.4e-5 | 9.1e-5 sigma | 4.2e-3 % |
| cn_free | M1_210210 | 1.9e-3 | 2.2e-4 | +1.5e-4 | 2.0e-8 | +1.5e-4 | 1.6e-5 sigma | 3.0e-3 % |
| cn_free | M9_227630 | 7.7e-4 | 1.4e-4 | +1.1e-5 | 8.0e-9 | +1.3e-5 | 9.0e-6 sigma | 9.7e-4 % |
| cn_free | M10_201233 | 1.2e-3 | 1.6e-4 | +1.6e-5 | 1.2e-8 | +2.0e-5 | 2.8e-5 sigma | 2.5e-3 % |

### Triton GEMM off: full fits of M1 (seconds)

| step | `XLA_FLAGS` | cell | process | sampler | ln L per s | cell 3 | cell 4 | tuned | ln Z | calls |
|---|---|---|---|---|---|---|---|---|---|---|
| 12 | none (default) | cn_free | 103.9 | 49.2 | 108,314 | 13.1 | 70.6 | 658 | 91778.2116 | 5.331 M |
| 14 | none (default) | cn_free | 102.7 | 49.4 | 108,597 | 13.0 | 70.0 | 658 | 91778.0968 | 5.365 M |
| 13 | `--xla_gpu_enable_triton_gemm=false` | cn_free | 100.3 | 50.9 | 105,873 | 11.8 | 67.2 | 644 | 91777.9194 | 5.389 M |
| 15 | `--xla_gpu_enable_triton_gemm=false` | cn_free | 97.7 | 50.5 | 106,795 | 11.9 | 66.9 | 644 | 91777.9194 | 5.389 M |
| 16 | none (default) | plain | 90.2 | 39.4 | 124,929 | 11.1 | 59.3 | 602 | 91772.1841 | 4.920 M |
| 18 | none (default) | plain | 89.7 | 39.2 | 125,653 | 12.5 | 57.5 | 602 | 91772.1841 | 4.920 M |
| 17 | `--xla_gpu_enable_triton_gemm=false` | plain | 85.0 | 39.6 | 123,471 | 10.0 | 54.8 | 585 | 91772.3853 | 4.894 M |
| 19 | `--xla_gpu_enable_triton_gemm=false` | plain | 91.2 | 39.2 | 124,841 | 10.4 | 60.0 | 585 | 91772.3853 | 4.894 M |

- Runs 7 and 8 together, process time: cn_free default 107.0, 105.1, 103.9, 102.7 (mean 104.7 s) against
  off 100.2, 96.8, 100.3, 97.7 (mean 98.8 s): -5.9 s (-5.7 %), lower in each of the 4 pairs. Plain default
  88.2, 90.2, 89.7 (mean 89.4 s) against off 85.2, 85.0, 91.2 (mean 87.1 s): -2.2 s (-2.5 %), lower in 2 of 3.
- The gain is compile time (cell 4 70.9 -> 67.6 s in cn_free; 14 fewer programs tuned). The cn_free sampler
  is 1.4 s slower (49.5 -> 50.9 s); the plain sampler is equal.
- Step 14 gave another ln Z and call count than step 12 with the same build, flags and seed in one
  container: the default path is not repeatable from compile to compile. Triton off gave the same ln Z in
  all 4 cn_free fits and all 3 plain fits of runs 7 and 8.

## ln L on the A100, build against build (runs 2, 4, 6, 9, 11)

Points: every 20th dead point of M1 (cn_free 800, plain 700). "Top 30": ln L within 30 of the highest point
(cn_free 390, plain 348). "CPU": the final build on the local CPU, where float32 products are exact float32.

| comparison | arm | delta ln L max (top 30) | rms | mean | predicted spectrum, relative max / rms |
|---|---|---|---|---|---|
| CPU final against A100 base (production build) | cn_free | 0.071 | 0.023 | +0.008 | 1.2e-4 / 5.0e-5 |
| CPU final against A100 final, default precision | cn_free | 0.131 | 0.040 | +0.032 | 2.8e-4 / 9.5e-5 |
| CPU final against A100 final, `JAX_DEFAULT_MATMUL_PRECISION=highest` | cn_free | 2.1e-4 | 7.9e-5 | +1.3e-5 | 3.4e-7 / 4.5e-8 |
| A100 base against A100 final, default precision | cn_free | 0.083 | 0.031 | +0.024 | 3.1e-4 / 7.5e-5 |
| CPU final against A100 base | plain | 0.083 | 0.023 | +0.008 | 1.2e-4 / 4.7e-5 |
| CPU final against A100 final, highest | plain | 3.0e-4 | 8.3e-5 | +2.5e-5 | 2.6e-7 / 4.1e-8 |
| A100 base against A100 final, default precision (run 9) | plain | 0.100 | 0.037 | +0.030 | 2.8e-4 / 8.2e-5 |

- Per kept step on the A100 (cn_free, 710 points with ln L > 9e4): base -> F1 max 0.539, rms 0.063, mean
  +0.022; F1 -> F2 max 0.494, rms 0.021; F2 -> F3 5.3e-5; F3 -> F4 0; F4 -> F5 1.5e-11. Same build in two
  containers: 9.2e-3.
- Run 9 (`runs/09-mu/`, $0.21): base -> F1 changes each sample's predicted spectrum by one factor (per-sample
  mean relative change -2.1e-4 to +1.4e-4; spread of the per-pixel change across pixels 1.2e-5); photometry
  changes by the same factor (max 2.7e-4).
- Cause: on the A100, XLA runs float32 matrix products in TF32 by default (`xla/stream_executor/cuda/cuda_blas.cc`
  sets `CUBLAS_TF32_TENSOR_OP_MATH` when TF32 is allowed; JAX issue 19444: relative error 3.65e-4 at the
  default precision, 1.7e-7 at `highest`). With `highest` the A100 agrees with the CPU to float32 rounding.
- The production build already has this TF32 error (rms 0.023 in the top 30, spectrum 1.2e-4). F1 and F2 move
  the SFH basis and the C/N response into float32 products, and the error grows to rms 0.040 (spectrum 2.8e-4).
- The full-fit check on 3 galaxies with this error is in run 8: medians within 0.028 sigma, widths within
  0.75 %, ln Z within 0.029.

## A100 run 11 (`runs/11-matmul-precision/`, A100-SXM4-80GB, driver 610.57.04, 2 cores, one container, $0.79): float32 products at full precision

Final build; `JAX_DEFAULT_MATMUL_PRECISION=highest` in the step environment; full fits of M1 on an empty
compile cache, seconds.

| step | precision | cell | process | sampler | ln L per s | cell 4 | ln Z | calls |
|---|---|---|---|---|---|---|---|---|
| 5 | default | cn_free | 114.7 | 46.8 | 113,967 | 74.2 | 91778.2116 | 5.331 M |
| 8 | default | cn_free | 108.6 | 46.5 | 114,529 | 71.3 | 91778.2116 | 5.331 M |
| 6 | highest | cn_free | 128.9 | 57.0 | 94,600 | 89.5 | 91777.9545 | 5.391 M |
| 7 | highest | cn_free | 132.8 | 59.5 | 90,583 | 91.8 | 91777.9545 | 5.391 M |
| 9 | default | plain | 97.6 | 39.1 | 125,695 | 62.2 | 91772.1841 | 4.920 M |
| 12 | default | plain | 98.7 | 39.2 | 125,529 | 63.1 | 91772.1841 | 4.920 M |
| 10 | highest | plain | 105.8 | 43.8 | 112,954 | 70.2 | 91772.1301 | 4.950 M |
| 11 | highest | plain | 104.2 | 43.6 | 113,445 | 69.5 | 91772.1301 | 4.950 M |

- `highest` costs cn_free +19.2 s per fit (sampler +11.6 s, +25 %) and plain +6.9 s (sampler +4.6 s, +12 %).
  Bench: loglike 1.209 -> 1.607 ms per batch of 100.
- Not kept: it gives back most of F1 and F2. Listed under "Needs his decision".
- This container was an 80 GB card: the default fits took 108.6 to 114.7 s, against 102 to 105 s on the 40 GB
  cards of runs 6 to 10.

## A100 run 10 (`runs/10-f5/`, A100-SXM4-40GB, driver 620.70.06, 2 cores, one container, $0.63): F5

F5 (ceridwen 90bb0c7, fa4a7b1): the lowered ln L had 2 sequential search loops (`stablehlo.while`): the C/N
`searchsorted` on 4 metallicity knots and the line LSF `jnp.interp` on 6166 pixels (13 steps). With a fixed
redshift the line centres are constants, so the LSF is a numpy constant (as `_window` already does); the
4-knot search compares with each knot. After F5 the ln L has no loop in either arm.

| step | build | cell | process | sampler | ln L per s | cell 4 | ln Z | calls |
|---|---|---|---|---|---|---|---|---|
| 4 | final | cn_free | 104.1 | 49.2 | 108,247 | 70.4 | 91778.2116 | 5.331 M |
| 7 | final | cn_free | 105.0 | 48.4 | 110,042 | 70.7 | 91778.2116 | 5.331 M |
| 5 | f5 | cn_free | 96.7 | 43.2 | 123,311 | 63.6 | 91778.2116 | 5.331 M |
| 6 | f5 | cn_free | 98.7 | 43.7 | 122,076 | 64.7 | 91778.2116 | 5.331 M |
| 8 | final | plain | 91.1 | 39.6 | 125,512 | 59.6 | 91772.1529 | 4.973 M |
| 11 | final | plain | 88.3 | 39.2 | 125,600 | 57.9 | 91772.1841 | 4.920 M |
| 9 | f5 | plain | 85.7 | 34.8 | 141,532 | 54.5 | 91772.1841 | 4.920 M |
| 10 | f5 | plain | 84.7 | 34.4 | 142,991 | 53.5 | 91772.1841 | 4.920 M |

- cn_free: process -6.9 s (-6.6 %), sampler -5.4 s (-11 %). Plain: process -4.5 s (-5.0 %), sampler -4.8 s
  (-12 %). Same ln Z and call count where the default build repeats itself.
- Bench: loglike 1.319 -> 1.111 ms (cn_free), 0.999 -> 0.848 ms (plain); the likelihood given the
  prediction 0.946 -> 0.749 ms and 0.806 -> 0.663 ms.
- A100 ln L final -> f5: max 1.5e-11 on 800 and 700 points; predicted spectra identical. CPU: 0 of 800 differ.
- Tests: the second assertion of `tests/test_emission_line_columns.py::test_windowed_columns_equal_the_full_evaluation_bitwise`
  (all-constant columns against the traced evaluation) is now `assert_allclose(rtol=1e-14, atol=1e-300)`:
  XLA folds the all-constant program at compile time, with last-bit and subnormal differences. The windowed
  against full assertion stays bitwise. 157 passed, 101 skipped.

## Full-fit check by refit: final build (run 6) against production

`compare_fits.py`, production fit -> refit with the final build (Astro 7ba8577d, ceridwen 8ef5c8c), same seed.
Steps 1 and 3 (and 6 and 7) are two compiles of one build and give one result.

| fit | max, rms median shift (sigma) | max width change | delta ln Z (production error) |
|---|---|---|---|
| cn_free M1 | 0.261, 0.099 | 77.4 % (`logsfr_ratios[1]`) | +0.355 (0.236) |
| cn_free M9 | 0.147, 0.076 | 25.9 % | -0.152 (0.186) |
| cn_free M10 | 0.368, 0.096 | 30.7 % | -0.035 (0.177) |
| plain M1 | 0.223, 0.094 | 41.0 % | -0.307 (0.201) |
| plain M9 | 0.137, 0.075 | 22.4 % | -0.356 (0.176) |
| plain M10 | 0.164, 0.068 | 15.1 % | +0.869 (0.173) |
| noise floor (run 5): base build, other seed, M1 and M9 | 0.220 to 0.258, 0.083 to 0.098 | 20.0 to 57.9 % | -0.82 to +0.63 |

- A refit is an independent sampler realisation: the rms shift (0.068 to 0.099 sigma) is the rms of the
  unchanged build with another seed (0.083 to 0.098), and the ln Z differences match the seed-to-seed ln Z
  differences, which are up to 4 times the quoted ln Z error. The refit cannot resolve 0.05 sigma; the
  reweighting check of run 8 (no sampler noise) is the check against the limits.

## A100 run 12 (`runs/12-precision-products/`, A100-SXM4-40GB, driver 620.70.06, 2 cores, one container, $0.86): total, and full precision on single products

`t5`: Astro baa81fbd (Triton GEMM off) with ceridwen fa4a7b1 (F5): the kept build. `t6a`: t5 with the F1 product
(SFH basis) at `Precision.HIGHEST` (ceridwen 5f31bce, branch `speedups-overnight-2026-11-16-precision`). `t6b`: t6a
with the two C/N products also at `HIGHEST` (18ff96c). Full fits of M1 on an empty compile cache, seconds.

| step | build | cell | process | sampler | ln L per s | cell 4 | ln Z | calls |
|---|---|---|---|---|---|---|---|---|
| 5 | base | cn_free | 181.4 | 98.4 | 56,115 | 128.4 | 91777.8563 | 5.521 M |
| 6 | t5 | cn_free | 95.0 | 44.7 | 120,567 | 62.6 | 91777.9194 | 5.389 M |
| 11 | t5 | cn_free | 94.1 | 44.5 | 121,006 | 62.0 | 91777.9194 | 5.389 M |
| 7 | t6a | cn_free | 98.1 | 47.4 | 113,666 | 65.2 | 91778.1031 | 5.389 M |
| 10 | t6a | cn_free | 100.2 | 47.3 | 113,993 | 65.0 | 91778.1031 | 5.389 M |
| 8 | t6b | cn_free | 103.5 | 52.4 | 102,718 | 69.1 | 91778.2163 | 5.379 M |
| 9 | t6b | cn_free | 103.5 | 52.1 | 103,188 | 69.6 | 91778.2163 | 5.379 M |
| 12 | base | plain | 112.1 | 49.5 | 98,177 | 73.0 | 91772.4911 | 4.860 M |
| 13 | t5 | plain | 79.8 | 34.6 | 141,602 | 50.0 | 91772.3853 | 4.894 M |
| 14 | t6a | plain | 87.0 | 39.2 | 124,428 | 56.5 | 91772.2456 | 4.874 M |

- Total, base against the kept build, one container ($0.86 / 1330 s = $0.000647 per s):

| arm | base process | kept process | change | base cost | kept cost | base sampler | kept sampler |
|---|---|---|---|---|---|---|---|
| dr3_cn_free_w | 181.4 s | 94.6 s | -48 % (1.92x) | $0.117 | $0.061 | 98.4 s | 44.6 s |
| dr3_plain_w | 112.1 s | 79.8 s | -29 % (1.40x) | $0.073 | $0.052 | 49.5 s | 34.6 s |

- ln L against the CPU final build (`runprec.py`), top 30 of ln L / fit range:

| bench step | build | arm | max | rms | spectrum relative max / rms |
|---|---|---|---|---|---|
| 0 | t5 | cn_free | 0.132 / 1.01 | 0.040 / 0.121 | 2.8e-4 / 9.5e-5 |
| 1 | t6a | cn_free | 0.071 / 0.68 | 0.022 / 0.076 | 1.2e-4 / 5.0e-5 |
| 2 | t6b | cn_free | 0.071 / 0.69 | 0.023 / 0.073 | 1.2e-4 / 5.0e-5 |
| 3 | t5 | plain | 0.096 / 1.74 | 0.045 / 0.191 | 3.4e-4 / 9.7e-5 |
| 4 | t6a | plain | 0.083 / 0.86 | 0.023 / 0.092 | 1.2e-4 / 4.7e-5 |
| run 11 | base (production) | cn_free, plain | 0.071, 0.083 | 0.023, 0.023 | 1.2e-4 / 5.0e-5 |

- The F1 product at full precision (t6a) brings the A100 error back to the production level; the C/N products at
  full precision (t6b) add nothing. The rest of the TF32 error (1.2e-4) is in products the production build has.
- Cost of t6a: cn_free +4.6 s per fit (sampler +2.8 s, +6 %); plain +7.2 s (sampler +4.6 s, +13 %, one pair).
  Bench loglike: cn_free 1.032 -> 1.195 ms, plain 0.793 -> 0.947 ms. t6b: cn_free +9.0 s.

## A100 run 13 (`runs/13-bf16x6/`, A100-SXM4-40GB, driver 620.70.06, 2 cores, one container, $0.36): six bf16 passes on the F1 and C/N products

`t7`: t5 with the F1 product and the two C/N products at `jax.lax.DotAlgorithmPreset.BF16_BF16_F32_X6` (ceridwen
c41bfcf, detached; `TF32_TF32_F32_X3` raises "not supported by dot_general on CPU"). Full fits of M1, seconds.

| step | build | cell | process | sampler | ln L per s | cell 4 | ln Z | calls |
|---|---|---|---|---|---|---|---|---|
| 3 | t5 | cn_free | 96.2 | 44.8 | 120,350 | 63.1 | 91777.9194 | 5.389 M |
| 2 | t7 | cn_free | 121.9 | 69.3 | 76,601 | 87.8 | 91778.6207 | 5.312 M |
| 4 | t7 | cn_free | 120.3 | 69.0 | 76,948 | 86.9 | 91778.6207 | 5.312 M |
| 5 | t7 | plain | 95.2 | 45.5 | 106,624 | 62.2 | 91772.7235 | 4.849 M |

- ln L against the CPU final build, top 30: cn_free max 0.071, rms 0.023; plain max 0.083, rms 0.023; spectrum
  relative 1.2e-4 / 5.0e-5. The same as t6a.
- Cost: cn_free +24.9 s per fit (sampler +55 %); plain +15.4 s against t5 in run 12 (79.8 s). Bench loglike
  cn_free 1.032 -> 1.751 ms. Slower than `HIGHEST` (t6a): not a cheaper fix.

## State at 2026-11-17 18:20 GMT (final)

- Kept: ceridwen e7bb70e, d03884c, ba88af2, c7aba78, d03f336, 8ef5c8c, 90bb0c7, fa4a7b1 (branch
  `speedups-overnight-2026-11-16`, pushed to potatoist314/ceridwen); Astro 49de1f3f, 19e7a012, 7ba8577d, baa81fbd
  (branch `speedups-overnight-2026-11-16`, pushed to potatoist314/cosmic-chronometers-jwst). Pin not moved.
- Variants only: ceridwen 5f31bce (t6a), 18ff96c (t6b), c41bfcf (t7); branch `speedups-overnight-2026-11-16-precision`
  holds 18ff96c; not pushed.
- Spend: runs 1-13 $9.68 of about $10 (profile `liuhaoo3-14`). No containers left; `modal container list` empty.
