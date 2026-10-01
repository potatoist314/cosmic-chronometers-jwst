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
| GPU image without NCCL and NVSHMEM | download 3.68 → 3.05 GB compressed | one boot: 17,900 dead-point lnL, log prior and stored values bitwise with the libraries present, hidden, present again; production fit on the new image (host 146008) vs the old (host 132677): all 17,800 dead-point lnL and logZ 236001.20006902877 bitwise, 5,624,104 lnL calls in both; container listings differ only by those 24 files (Actions run 36784540834) | `de74870`, `788492d` |
| GPU image without the eight cuDNN libraries XLA never loads | 3.05 → 2.32 GB (cuDNN layer 770 → 45 MB) | XLA needs `libcudnn.so.9` and `libcudnn_graph.so.9` only (`/proc/self/maps`); one boot: 17,900 lnL, 300 dead points of 3 sampler iterations, cell 14's 143 compiles bitwise with the other eight hidden; production fit on the new image (host 132677): all 54 result and 65 of 66 derived entries bitwise vs the previous image (the 66th is `wall_time_s`) | `88259d8`, `c9d0b3f` |
| … and without `libcusolverMg`, `libcufftw`, the nvrtc builtins and alt build | 2.32 → 2.15 GB | absent from `/proc/self/maps` in the same three jobs; production fit on it (host 383511, Ryzen 7 9800X3D) completed; dead-point positions bitwise vs the fit on the NCCL-trimmed image (host 146008, i5-12400F); 11,176 of 17,800 lnL differ by ≤ 9.5e-7 (2.5e-13 relative), all downstream of 9 of 28 filter effective wavelengths that sedpy_jax computes with NumPy `log`/`exp` on the host CPU (`observate.py:593–605`), ≤ 5.4e-15 relative | `c73a664`, `f3cf417` |
| Container that fails to start is replaced after 60 s | ≥ 4 min → 64 s per such host (host 415547 again, 2026-09-30 23:44) | no computation; runner tests | `5b3e186` |
| KL figure: one sort per KL value; prior reference sorted once | `marginal_kl_bits` 2.25 → 1.23 ms per call (min of 40), ~5,000 calls per figure rebuild | KL table and both noise floors of the production fit bitwise; tests against `np.histogram` at 17,800 / 65,536 / 65,537 / 100,000 samples | `27df4f7` |
| `--fits-per-gpu K`: K cells at once under CUDA MPS (swarm-throughput) | 4 targets, fit stage 839 → 641 s (K=2), 607 s (K=4), one boot | result and derived h5 of all 4 targets bitwise vs K=1 at K=2 and K=4 (only `wall_time_s`); K=1 default unchanged | `468ffe4` (`faf650c`) |
| KL figure: bootstrap and noise-floor KL values on threads | wall, this M1 Pro at load average 50–70: `kl_table` 10.9–20.5 → 4.7–6.1 s, SFH noise floor 4.1–7.8 → 3.4–3.8 s | results come back in input order; KL table and both noise floors of the production fit bitwise; test: threaded vs serial map on the stored eline_off fit | `987b0c7` |

## One production fit, before and after

M1_210210, `neb_eline_ca_nohe_zevo`, seed 20260927, RTX 5090, one run each.

| Stage | Before (`48f56a4`) | After (`48fdc7f`) | After (all, `04d4574`) | After (all, `f3cf417`, image 6ca819ac) |
|---|---|---|---|---|
| Offer search and refusals | 2.2 min | 26 s | 10 s (3 refusals) | 18 s (+2 refusals, 3 s) |
| Failed hosts | — | — | 3.5 min: host 415547 container start failed (Vast shim missing; destroyed by hand after 1 min, the stall rule acts after ≥ 4 min), host 564477 outbid | 8.8 min: host 18 vanished mid-fit (6 min), host 415547 container start failed again and was replaced after 64 s by the new rule (2.5 min) |
| Instance loading | ~5.9 min | 7.3 min | 2 min 25 s | 1 min 46 s (cold host) |
| Upload and bootstrap | ~11 min (SSH wait, upload, bootstrap) | 1 min 58 s | 1 min 11 s | 53 s |
| Fit (box) | 11.8 min | 4.5 min | ≤ 3.8 min | 3.5 min |
| Sampler wall | 628.2 s | 197.8 s | 187.6 s | 184.2 s |
| Sampler iteration 1 | | 17.0 s | 1.04 s | 1.02 s |
| Retrieval, teardown | 20 s | 12 s | 13 s | 23 s |
| Local figure rebuild | | 40.3 s | 47 s | 3 min 20 s (this Mac at load average ~150; 40–47 s unloaded) |
| Wall | 31.3 min | 14.6 min | 12.3 min (8.8 min without the failed hosts) | 19.5 min (10.7 min without the failed hosts) |
| Billed GPU time | 23.2 min | 9.5 min | 4.9 min | 8.7 min by invoice, for 4.8 min from running to destroyed (+4.4 min on the vanished host) |
| Cost | $0.162 | $0.067 | $0.036 | $0.071 (+$0.031 on the failed hosts) |
| ln Z | 236001.315 ± 0.185 | 236001.806 ± 0.205 | 236001.239 ± 0.245 | 236001.239 ± 0.189 |

The two intermediate images each gave a complete production fit: dcfc83f7 (host 146008) $0.066, bitwise equal to `04d4574`'s fit; 4da04a83 (host 132677) $0.056, bitwise equal to dcfc83f7's. Fits on i5-12400F hosts (132677, 146008) are bitwise equal to each other; the Ryzen 7 9800X3D host differs at 2.5e-13 in lnL through the CPU-computed filter wavelengths.

## Spend

Vast invoices, 30 Sep – 1 Oct 2026 (read 1 Oct, 00:1x UTC).

| Run | Instances | Charge |
|---|---|---|
| session 1 (profile) | 53565581 | $0.145 |
| session 2 (likelihood, autotune) | 53572183, 53573864, 53575696 | $0.648 |
| e2e after (`48fdc7f`) | 53580917 | $0.067 |
| session 3 (image, compile overlap, cell 14) | 53588305 (outbid), 53590735 | $0.068 |
| e2e after (all, `04d4574`) | 53592074 (failed start), 53592331 (outbid), 53592414 | $0.036 |
| session 4 (NCCL/NVSHMEM A/B) | 53595253 | $0.067 |
| e2e on image dcfc83f7 | 53596914 (vanished while loading), 53597096 | $0.067 |
| session 5 (cuDNN/cuSPARSE/cuSOLVER A/B) | 53598740 | $0.151 |
| e2e on image 4da04a83 | 53601900 | $0.056 |
| e2e on image 6ca819ac (`c73a664`) | 53604961 (vanished mid-fit), 53605571 (failed start), 53605802 | $0.102 |
| Total | 18 instances, all destroyed | $1.407 |

Every run stayed under its $1 cap; the largest was session 2.

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
| Prefer hosts that pulled the image recently | created → running 42–77 s on hosts with the layers cached (146008, 132677) vs 106 s–7 min on cold hosts | free; conflicts with the AGENTS.md host ranking (Liu Hao's rule) |
| Grid fetched on the box instead of uploaded from this Mac | upload 473 MB at 8–11 MB/s is the setup critical path (53–144 s with bootstrap) | the nebular grid is not published: Zenodo record 21977508 has `amist_c3k_hr_krou_afe` only, whose `ssp_flux` differs; hosting it (Zenodo, a private registry layer) is a data-release decision |
| Lossless transform of the packed grid | integer delta along age: 0.775 → 0.732 of 612 MB (~26 MB, ~3 s upload); xz: 0.711 at 20× the pack time | free, but gain under the host-to-host spread; not built |
| GPU type (swarm-throughput) | RTX 5090 fastest and cheapest per fit up to ~$0.44/h; A100 SXM4 1.30×, 4090 1.62×, 5060 Ti 3.41×, 3090 3.75×, V100 3.91× slower solo | Liu Hao's choice; keep the 5090 (`results/speedups-swarm-throughput-2026-09-30/types`) |
| Rank offers by USD per fit (swarm-throughput) | host-record ranking paid $0.38–0.615/h for RTX 5090 while a valid $0.153/h bid existed (2.5–4× per fit) | Liu Hao's rental rule; 3 of 9 bid rentals tonight were stopped mid-job, and a K-fit stage loses all K cells' progress on a stop |
| vmapping several fits into one sampler (swarm-throughput) | MPS with 4 fits already reaches the batch-500 gain (1.26–1.34×) | changes row counts, so lnL bits change; not proposed |
| zstd image layers | cuBLAS layer 581 → 468 MB at `zstd -19` (−19.5%; `gzip -9` −0.1%), decompression 3.1 → 2.3 s; ~18 s per cold host at the 24 MB/s seen on host 383511 | results unchanged, but pulls need Docker Engine ≥ 23.0 (moby v23.0.0 release notes) and Vast does not report host Docker versions: an older host fails to start |

## Tried; not possible

- Removing cuDNN: XLA's GPU compiler requires DNN support (`RET_CHECK dnn_support != nullptr`, `gpu_compiler.cc:2798`).
- Removing cuSOLVER or cuSPARSE: the likelihood's `cholesky`/`inv` call `gpusolverDnCreate`, which fails with either library hidden.
- cuFFT, cuBLAS, nvrtc, cupti, cudart, nvJitLink: loaded in every job (`session5/run/out/libs-*.txt`).

## Blocked

- Merging `absorption-mask` into `speedups`: refused by the permission classifier; Liu Hao's call.
