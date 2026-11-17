# Speedups hill-climb 2026-11-17: ledger

Card t_cf15e524. Branch `speedups-hillclimb-2026-11-17` in both repos (Astro worktree
`tmp/worktrees/speedups-hillclimb-2` from absorption-mask 2d000184, ceridwen worktree inside it from pin 3b5177f).
Keep rule: results identical or different only by floating-point rounding, and a real same-runtime A100 gain;
the final build also passes the 3-galaxy reweighting check (medians within 0.05 sigma, widths within 5 %,
ln Z within its error). Arm order: `dr3_plain_w` first, then `dr3_cn_free_w`.

## Baseline (`runs/01-profile/`, Colab A100-SXM4-40GB, 12 cores, empty caches, M1_210210)

| step | cell | process s | sampler s | calls M | calls/s | ln Z | compiled / tuned |
|---|---|---|---|---|---|---|---|
| 0 | plain, profiled | 84.5 | 36.6 | 4.832 | 132,000 | 91772.2375 | 470 / 569 |
| 1 | plain | 79.5 | 36.5 | 4.832 | 132,500 | 91772.2375 | 470 / 569 |
| 2 | cn_free, profiled | 99.2 | 51.9 | 5.400 | 104,000 | 91777.8536 | 485 / 618 |

Notebook cells, plain step 1 (s): imports 4.6, data 7.2, model 7.8, sampler cell 52.6, output 1.3.

- Fixed start-up of a plain fit: 79.5 - 36.5 = 43 s.
- Sampler cell outside the sampler loop: 14.6 s before (ln L compile 10.4 s in the worker thread, 3.7 s main
  thread), 1.5 s after.
- Data cell (7.2 s): 1.9 s of 87 compiles; the rest is `cosmos_photometry.read_matches` (CPU profile, local:
  8.3 of 10.2 s), which reads 4 match catalogues with astropy `Table.read`. Their headers carry 776 to 7832
  lines of astropy column YAML; parsing it is 3.5 s of the 8.3 s locally.

## Attempts

| # | idea | change | before / after | max \|delta ln L\| | kept | why |
|---|---|---|---|---|---|---|
| 1 | One kernel for the fits of a container (`experiment.py remote` with several cells, b650b554) | 3 plain fits M1, M9, M10 in one kernel (`runs/02-kernel-cache` step 0) | alone 79.7 + 74.3 + 77.7 = 231.7 s; one kernel 181.8 s (2nd and 3rd fit 51.1 and 50.5 s of cells) | ln Z equal to 4 decimals (91772.2375, 96413.8065, 104123.9525) | yes | production called `remote` with one cell; `modal_gpu.batch` and `ColabRun.fit` now fit the uncached cells of a container or runtime in one kernel |
| 2 | One compile cache for all galaxies | `JAX_COMPILATION_CACHE_DIR=/tmp/xla/shared`, one process per fit, filled by the previous fits (steps 3-5) | M9 74.3 → 68.2 s, M10 77.7 → 69.2 s (168 and 26 programs compiled instead of 471) | ln Z equal to 4 decimals | no | entry 1 gives the same saving and more |
| 3 | CPU cores for the start-up | `taskset` to 2 and 4 of 12 cores, M1 (steps 6-7) | 12 cores 79.7 s; 4 cores 81.0 s; 2 cores 90.6 s | ln Z equal | no | Modal `cpu=2.0` is a request, not a limit: a container uses up to 16 cores above it when the host has them and pays for the higher of request and use (modal.com/docs/guide/resources, read 2026-11-17) |
| 4 | Entry 1 with both arms mixed in one kernel | plain and cn_free fits of M1, M9, M10 alternating in one kernel (`runs/03-kernel-batch` step 0), cn_free M9 and M10 alone (steps 1-2) | 6 fits 385.7 s; cn_free M9 alone 91.7 s (cells 85.2 s), in the kernel cells 67.5 s; M10 92.3 s (86.8 s) → 66.3 s | ln Z equal to 4 decimals for all 6 fits (cn_free 91777.8536, 96412.2203, 104125.0761) | yes, with entry 1 | host memory rose 7.1 → 8.9 GB over the 6 fits (about 0.3 GB per fit; `memory-0.txt`); GPU memory fixed at 31.5 GB. Modal `memory` is a request, not a limit: a container can exceed it and pays for its use (modal.com/docs/guide/resources, read 2026-11-17) |
| 5 | One ln L program for all galaxies of a kernel | none built: lowered the sampler's vmapped ln L for M1, M9, M10 on CPU (scratch probe) | per-galaxy shapes differ: SSP wavelength support 8618 / 8693, filters 28 / 30, resample length 3905 / 3904, fitted pixels 1630 / 1705, one more axis 6 / 7 | - | no | about 10 s of ln L compile per later fit; uniform shapes need padding through the ceridwen likelihood, SSP and photometry code (overlaps the upstream 2.0 merge) |
| 6 | Cache the catalogue read across fits of a kernel | none needed | data cell 7.0 s alone; 2.3 and 0.1 s for the 2nd and 3rd fit of a kernel (`runs/02-kernel-cache`, notebook cell times) | - | - | entry 1 already removes it |

## Full-fit check (final build 377bf6ab, Colab A100, `compare_fits.py`, alone against one kernel)

| arm | galaxy | max median shift (sigma) | max width change | ln Z alone → kernel |
|---|---|---|---|---|
| plain | M1, M9, M10 | 0.000 | 0.0 % | 91772.270, 96413.836, 104123.981, delta 0.000 |
| cn_free | M1, M9, M10 | 0.000 | 0.0 % | 91777.890, 96412.252, 104125.105, delta 0.000 |

Effective sample counts equal.

## Tests

- Astro full selection: base 2d000184 and branch both 13 failed, 15 errors, 350 passed; same failing tests
  (emission-line marginalisation, checkpoint-evolution plot, regenerate-fit-notebooks, dust bump, results board).
- Fast-path assertion (`tests/test_ceridwen_dr2_production.py -k constant_calibration`): passed.
- `tests/test_modal_gpu.py`, `tests/test_experiment.py`: 74 passed. Ceridwen unchanged (pin 3b5177f).

## Real path (`experiment.py run`, A100-40GB, seed 20260832, `dr3_plain_w`)

Modal, profile liuhaoo3-14, the first 20 targets of `results/dr3-more-galaxies-2026-11-16/plain-modal`
(`real/plain-modal/`), 10 containers of 2 fits. Base: 2d000184, one process per fit. New: 377bf6ab, one kernel.

| build | container s, mean (min-max) | estimated | billed | first / second fit in a container |
|---|---|---|---|---|
| base 2d000184 | 198.1 (173.1-210.7) | $1.277 | $1.118 | one process each |
| new 377bf6ab | 163.1 (153.7-172.1), -18 % | $1.052 | $1.070 | 77-87 s / 46-59 s |

- Results, base against new: 19 of 20 identical (median shift 0.000 sigma, delta ln Z 0.000). M13_215951 differs
  (0.310 sigma, delta ln Z +0.224, error 0.17); its new fit (2nd in its kernel) is identical to the Colab fit (1st in
  its kernel), so the difference is the base host, not kernel position.
- Colab (`real/plain-colab/`), 6 of the same targets in one kernel, 1.80 units: fits 82, 56, 56, 45, 45, 65 s.
  Against the new Modal fits: 4 identical; M13_216897 and M13_219726 differ (0.275 and 0.240 sigma, delta ln Z
  -0.224 and -0.607). Positions Colab / Modal: 2nd / 1st and 3rd / 1st; M14_103557 at 4th / 1st is identical.
- Against the production fits of 16 Nov (ceridwen 13791e0, before the 16-17 Nov speedups): max shift 0.41 sigma,
  |delta ln Z| up to 2.9 errors; ln L rounding changed with those speedups.
