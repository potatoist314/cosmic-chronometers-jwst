# Free speedups, overnight 2026-09-30

Branches: `speedups` in this repo and in `potatoist314/ceridwen` (ceridwen pinned at `a60f1f8`).
Neither is merged into `absorption-mask`.
"Free": bitwise-identical on CPU; on GPU, equal up to the float rounding that the
current kernel already shows between rentals (`results/speedup-lane-cause-2026-09-30`).
Reference fit: M1_210210, nebular grid, emission-line marginalisation, Ca mask, zevo, RTX 5090.

## Speedups on `speedups`

Likelihood figures: M1_210210 zevo model, RTX 5090, µs per call at batch 100 / 500, all in one boot.

| Speedup | Measured gain | Exactness evidence | Commit (ceridwen) |
|---|---|---|---|
| Lane slice kernel is the default | sampling 253.2 → 108.7 s | GPU differences are float32 rounding at `photometry.py:277` (`results/speedup-lane-cause-2026-09-30`); Liu Hao turned it on | `ae7392c` (`8161d3d`) |
| Sparse filter-grid interpolation in `Photometry.setup_for_model` | 6–15 s → 0.01–0.04 s per fit (Mac) | `_T` bitwise equal for 7 targets (`tests/test_photometry_projection.py`) | `25824a4` (`7c4db5e`) |
| Emission-line columns on 40σ windows | 38.1 → 32.6 µs (batch 100) | lnL of 17,300 dead points bitwise, CPU and GPU | `92d1483` (`f44eb32`) |
| Tied doublets as a column gather | 32.6 → 30.0 µs | same | `e663683` (`decead1`) |
| One-select placement of line windows | 30.0 → 27.7 µs; batch 500 27.1 → 22.2 µs | same | `48fdc7f` (`e47f619`) |
| (three likelihood changes together) | 38.1 → 27.7 / 32.5 → 22.2 µs; zevo sampling 254.5 → 185.5 s | 168 iterations and logZ 236002.7708042 in both; non-zevo dead-point positions bitwise (236.3 → 187.5 s) | |
| XLA GPU autotune level 0 | −7.6 s per fit (init 6.2 → 2.1 s, first iteration 7.8 → 4.3 s); posterior-predictive cell 12.3 → 6.4 s (compile 10.8 → 5.0 s, 143 programs) | level-0 processes bitwise equal to each other in one boot; across two rentals and both images, lnL of 17,300 dead points within 8.3e-7 (priors and stored values bitwise); default autotune differs between processes (165 of 17,300 lnL). Shift vs default ≤ 1.1e-2 (median 2.6e-3), inside the 1.5e-2 between-rental envelope | `ff005a2` |
| Step kernel compiled during sampler init | to first iteration done: CPU 32.6 → 31.5 s; GPU 9.86 / 9.84 → 7.66 / 7.62 s (iteration 1 4.92 → 0.98 s) | dead points bitwise on CPU (`test_step_compiled_during_init_compiles_once_and_matches_serial_run`); GPU: 300 dead points of iterations 1–3 bitwise across two old and two new processes, one boot | `07ff3dd` (`a60f1f8`) |
| COSMOS catalogues read once per process | −4.2 s per fit (box) | exact frame equality (`tests/test_cosmos_photometry.py`) | `35d8ac7` |
| KL table: one sort for both quantiles | 18.2 → 12.8 s (local figure rebuild) | kl_table and noise floors bitwise; test | `8b02c95` |
| Vast refusals parsed; next offer at once | refusals cost ~1 s each and no attempt (before: 2–5 per run, 1–2 min; tonight the old runner spent all 8 attempts on refusals in 44 s) | no computation | `07ddf22` |
| Upload: tests and dist left out | −68.5 MB | identical wheel RECORD files | `eaa86d3` |
| Upload: packed grid sent beside source | 612 → 473 MB, in parallel with source | grid sha256 check on the box | `9003842`, `61e824a` |
| Upload: packed grid as 4 parallel rsync parts | 8.6–11.3 vs 4.7–5.8 MB/s | same sha256 check | `66745cd` |
| Stage polling: one SSH call per poll | ~1.8 s per poll | no computation | `4aa058e` |
| Cell setup: one SSH call | −1.8 s per cell | config bytes unchanged | `7f04c7b` |
| Teardown: no second listing | −0.85 s | no computation | `4ea4cde` |
| Bootstrap starts while the grid uploads | upload + bootstrap 118 s (host 127708) → 61 s (host 370354), 71 s (host 132677); hosts differ | no computation; runner tests | `16ba69e` |
| Outbid or vanished instance is replaced | avoids an open-ended wait (12 min observed, session 3); final e2e: next rental 6 s after the outbid stop was seen | no computation; runner tests | `269633f` |
| GPU image holds the packages Vast's SSH launch installs | Vast's derived-image step 24–30 s → ~6 s (host 132677) | image = split image + one 79.4 MB layer (Actions run 36780287741); no computation | `8515f8f`, `04d4574` |
| GPU image with the 3.5 GB venv layer split into 11 | created → running 7.3 min (host 127708) / ~5.9 min (host 146008) → 2 min 7 s (host 370354) | 28,224 tar members identical (name, type, mode, owner, mtime, link, pax headers, sha256); container file listings and configuration identical (Actions run 36779780421) | `a481e48`, `7fb6f06`, `04d4574` |

## One production fit, before and after

M1_210210, `neb_eline_ca_nohe_zevo`, seed 20260927, RTX 5090, one run each.

| Stage | Before (`48f56a4`) | After (`48fdc7f`) | After (all, `04d4574`) |
|---|---|---|---|
| Offer search and refusals | 2.2 min | 26 s | 10 s (3 refusals) |
| Failed hosts | — | — | 3.5 min: host 415547 container start failed (Vast shim missing; destroyed by hand after 1 min, the stall rule acts after ≥ 4 min), host 564477 outbid |
| Instance loading | ~5.9 min | 7.3 min | 2 min 25 s |
| Upload and bootstrap | ~11 min (SSH wait, upload, bootstrap) | 1 min 58 s | 1 min 11 s |
| Fit (box) | 11.8 min | 4.5 min | ≤ 3.8 min |
| Sampler wall | 628.2 s | 197.8 s | 187.6 s |
| Sampler iteration 1 | | 17.0 s | 1.04 s |
| Retrieval, teardown | 20 s | 12 s | 13 s |
| Local figure rebuild | | 40.3 s | 47 s |
| Wall | 31.3 min | 14.6 min | 12.3 min (8.8 min without the failed hosts) |
| Billed GPU time | 23.2 min | 9.5 min | 4.9 min |
| Cost | $0.162 | $0.067 | $0.036 |
| ln Z | 236001.315 ± 0.185 | 236001.806 ± 0.205 | 236001.239 ± 0.245 |

## Spend

Vast invoices, 30 Sep 2026.

| Run | Instances | Charge |
|---|---|---|
| session 1 (profile) | 53565581 | $0.145 |
| session 2 (likelihood, autotune) | 53572183, 53573864, 53575696 | $0.648 |
| e2e after (`48fdc7f`) | 53580917 | $0.067 |
| session 3 (image, compile overlap, cell 14) | 53588305 (outbid), 53590735 | $0.068 |
| e2e after (all, `04d4574`) | 53592074 (failed start), 53592331 (outbid), 53592414 | $0.036 |
| Total | 10 instances, all destroyed | $0.964 |

## Not free: proposals, not built

| Proposal | Measured effect | Why not free |
|---|---|---|
| Tied doublet as elementwise sum instead of `profiles @ tie` | not measured on GPU | 1-ulp differences in 2 of 150,000 column elements on CPU (FMA) |
| `jax.jit` of the emission-line columns | | 1,049,770 elements differ on CPU, max 4.0e-28 |
| `jax.jit` of `posterior_draws_with_lines` | 3.89 → 1.64 s (CPU) | 3e-10 relative differences |
| Masked-row compaction / windowed Gram matrix | | reorders sums |
| Persistent XLA compile cache | warm cache −2.2 s | executables embed galaxy data; a new galaxy costs ~3 s more |
| Skip the catalogue YAML header parse | ~1.9 s per read | masked columns rely on it |
| Parallel offer-search API calls | ~2.5 s | pre-rental total is 5.6 s |
| Grid hosted for download on the box, or grid in the image | upload −1 to −3 min | new storage and image policy |
| float32 or power-of-two FFT | | changes rounding |
| FilterSet numpy rewrite (sedpy_jax) | 2.1 s | changes rounding |
| KL histogram sort shared between parameters | | reorders sums |
| `log_evidence_err` uses the numpy global RNG (`nested.py:958`) | | seed handling change, not a speedup |
| More than one fit per GPU | no gain measured | |
| Replace a host whose container fails to start at once, not after the 240 s stall rule | ~4 min per such host (one seen: 415547) | free; not built: one observation, Vast restart behaviour unknown |

## Blocked

- Merging `absorption-mask` into `speedups`: refused by the permission classifier; Liu Hao's call.
