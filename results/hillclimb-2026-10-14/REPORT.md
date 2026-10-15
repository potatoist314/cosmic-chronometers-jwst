# Hill-climb report, 2026-10-14/15

- One benchmark fit on a Modal L40S now takes 234.6 s instead of 261.1 s (−10%), with identical results; cost per fit drops from $0.158 to $0.142 (fit process) and from $0.168 to $0.157 end to end.
- Five results-identical changes are kept on `hillclimb`: COSMOS catalogues read once, several cells in one notebook kernel, FilterSet built on the host, posterior-predictive programs compiled during the sampler, and the sampler's step-kernel compile started before the prior draw.
- Reliability: 154 of 154 GPU fits finished and passed the stored convergence check (phase 2: 99 of 99).
- Bigger sampler gains change results and need Liu Hao's call: `num_inner_steps` 33 halves the sampler time but moves ln Z by +0.54; `logZ_tol` −3 saves 8% of the sampler time with ln Z and posteriors unchanged within the seed scatter.
- Phase 2 (`hillclimb-2`) builds the backend changes: a sample run of more than 10 galaxies now costs $0.149 per fit instead of $0.160; a rerun of a cached galaxy costs $0.147, or $0.104 when 4 share a GPU, bitwise identical to the first fit. XLA autotune level 0 would let every sample fit share a GPU (≈ $0.105) but moves ln Z by −0.05 to −0.54 (Liu Hao's call).

## Benchmark and method

- Galaxy: M5_238580 (manifest index 80, seed 20260832), October defaults (benchmark-cells.json). Of the 135 DR2 refit fits it is nearest the sample medians in z, S/N, sampler wall, likelihood calls, Kish ESS and χ²/ndof (LEDGER.md header).
- GPU: Modal L40S, workspace initialincrease, 2 cores and 16 GiB per container (as scripts/modal_gpu.py). GPU types are compared by gpu-bench-modal, not here.
- Same-container A/B: arms alternate in one container (modal_ab.py), each fit as the production `scripts/experiment.py remote` call; 3 repeats per arm; mean ± sd.
- End to end: `scripts/experiment.py run results/hillclimb-2026-10-14/experiment.json --gpu L40S --revision REV` (modal-gpu backend), 3 runs per build.
- Cost: $0.000604 per container second (L40S $0.000542 + 2 × $0.0000131 per core + 16 × $0.00000222 per GiB; modal.com/pricing, as cited in scripts/modal_gpu.py).
- Results-identical: CPU fits compared byte for byte (every dataset and attribute except time stamps, `log_evidence_err` and git provenance). GPU: lnL on dead points with identical parameters. Repeats of one build differ by up to 5.5e-5 in one container and 7.9e-3 across containers, and land on two sampler paths (ln Z 236690.2596 and 236690.2461).
- Per-change record with noise: LEDGER.md. Run records: runs/<run>/ (timings.json: plan and per-step output of modal_ab.py; summary.json: summarise.py; manifest.json: end-to-end runs).

## Kept changes (branch `hillclimb`, all pushed)

| Change | Commit | Measured gain (L40S, same container, n = 3 per arm) | Results-identical check |
|---|---|---|---|
| COSMOS catalogues read once per process (cherry-pick of speedups 35d8ac7) | 01932b8 | observations cell 16.0 → 12.8 s | tests/test_cosmos_photometry.py exact frames; GPU on standard paths |
| Several cells in one notebook kernel (`experiment.py remote`) | b650b55 | second fit in a kernel: notebook 255.0 → 226.2 s | CPU byte-identical; GPU on standard paths. Gains only when a container fits several cells |
| FilterSet padded and differenced on the host (ceridwen 41f7472) | e015bad | observations 13.1 → 7.2 s; process 265.5 → 256.5 s | new ceridwen test (bit for bit); CPU fit byte-identical |
| Posterior-predictive programs compiled in a thread during the sampler (fit notebook) | d9ae647 | predictive cell 15.8 → 1.5 s; process 245.5 → 231.6 s | CPU fit byte-identical; GPU lnL within the same-container envelope |
| Step-kernel compile submitted before the prior draw (ceridwen d61175d) | 62aba10 | sampler-cell setup 22.0 → 19.8 s | CPU fit byte-identical; existing compile-once / serial-equality test |

## Before and after

Before: a0d6c48 (branch start). After: 62aba10 (branch head). Same container, alternating, n = 3 each.

### Wall time and stage split (s)

| Stage | Before | After |
|---|---|---|
| Fit process (kernel start to exit) | 261.1 ± 1.9 | 234.6 ± 0.6 |
| Kernel start | 1.2 ± 0.2 | 1.1 ± 0.1 |
| Imports | 5.2 ± 1.3 | 4.5 ± 0.1 |
| Observations | 15.7 ± 0.1 | 6.8 ± 0.1 |
| Model | 15.9 ± 0.4 | 15.5 ± 0.1 |
| Sampler setup (cell minus sampler wall) | 21.3 ± 0.4 | 20.2 ± 0.4 |
| Sampler wall | 177.9 ± 0.2 | 178.9 ± 0.5 |
| Posterior predictive | 17.2 ± 0.2 | 1.5 ± 0.0 |
| Corner / SFH | 1.3 ± 0.1 | 1.2 ± 0.0 |
| After the kernel (outputs) | 5.2 ± 0.5 | 4.5 ± 0.2 |

### End to end on Modal (experiment.py run, n = 3 each)

| | Before (4ac2224) | After (62aba10) |
|---|---|---|
| Container seconds | 278.8 ± 21.1 | 260.3 ± 14.7 |
| Container start → fit start (image, bootstrap) | 24.5 ± 1.5 | 24.1 ± 2.4 |
| Estimated cost per fit | $0.168 ± 0.013 | $0.157 ± 0.009 |
| Driver time without a queue | — | 300.1 ± 25.1 |

The 4ac2224 and dfd47b9 runs waited 9–48 min in the queue: the workspace's 10-GPU limit (Starter plan, modal.com/pricing) was shared with gpu-bench-modal. Modal billed cost: at 02:05 BST the hourly billing report covered only up to 23:00 UTC and had not posted these apps, so costs here are estimates; `modal billing summary` then showed $9.69 metered for the workspace, all covered by credits (billed $0).

### Cost per fit

| | Before | After |
|---|---|---|
| Fit process × $0.000604/s | $0.158 | $0.142 |
| End-to-end container × $0.000604/s | $0.168 | $0.157 |

### Throughput (one L40S)

| | Before | After |
|---|---|---|
| Fits per GPU-hour, end to end (one fit per container) | 12.9 | 13.8 |
| Fits per GPU-hour, fit process only | 13.8 | 15.3 |

### ESS per second

The kept changes do not change the sampling: both builds land on the same two sampler paths, so ESS per fit is unchanged and ESS per process second rises with the shorter process. Per-parameter ESS: posterior variance over the variance of the posterior mean across 200 simulated nested-sampling weight draws (anesthetic, seed 0), combined with the Kish term (summarise.py).

| | Path 3d78 (ln Z 236690.2461) | Path 9ac5 (ln Z 236690.2596) |
|---|---|---|
| Kish ESS | 4442 | 4345 |
| ESS logzsol / afe / logmass / t50 | 2619 / 2829 / 2179 / 1805 | 2951 / 2926 / 2604 / 2152 |

| ESS per second (mean of the two paths) | Before | After |
|---|---|---|
| Kish, per sampler second | 24.7 | 24.6 |
| Kish, per process second | 16.8 | 18.7 |
| logzsol / afe / logmass / t50, per process second | 10.7 / 11.0 / 9.2 / 7.6 | 11.9 / 12.3 / 10.2 / 8.4 |

### Reliability

| | Count |
|---|---|
| GPU fits tonight (A/B harness + end to end) | 154 |
| Exit 0 | 154 |
| Stored check passed (`diagnostics/passed`: finite ln Z and error, weight ESS ≥ 200) | 154 |
| Start failures | 6 end-to-end attempts at 22:07 UTC, my setup: catalogue symlinks in this worktree pointed outside the repository and the container's tar extraction refused them (`AbsoluteLinkError`); copies fixed it. The client showed only "Could not deserialize remote exception" |

## Recommended production setting

- Code: branch `hillclimb-2` (backend 49ac029; ceridwen d61175d).
- Modal: L40S, 2 cores, 16 GiB, scripts/modal_gpu.py defaults: up to 10 cells get one container each; more cells share 10 containers (Starter plan GPU limit); reruns of a cached setup share a GPU 4 at a time. Do not request more cores (entry 7).
- Cost per fit for M5_238580, billed: $0.159 with one container per cell (≤ 10 cells), $0.149 above 10 cells, $0.147 for a cached rerun, $0.104 for 4 cached reruns on one GPU.
- If Liu Hao accepts XLA autotune level 0 (phase-2 proposal): 4 fits per GPU for every cell, ≈ $0.105 per fit.

## Proposals for the modal-gpu backend (phase 1; built in phase 2, below)

| Proposal | Measured gain | Evidence | Ledger |
|---|---|---|---|
| XLA command buffers on (`XLA_FLAGS=''`) | sampler 179.3 → 172.0 s; process 262.8 → 256.8 s | 3 of 3 fits finished; on the standard path, lnL shift 5.5e-5. They were turned off on 5 Sep (5eb6483) for kernel deaths on RTX 5060; 3 fits are thin reliability evidence | 1 |
| Persistent compile cache on a Modal Volume | new galaxy 258.6 → 242.3 s; same galaxy rerun 219.8 s | CPU byte-identical; GPU fits on the standard paths | 3 |
| Several cells per container in one kernel (b650b55 already runs a config's cells in one kernel) | second fit 255.0 → 226.2 s, plus ≈ 24 s container start and ≈ 15 s bootstrap per extra cell | CPU byte-identical | 6 |
| XLA per-fusion autotune cache (`--xla_gpu_per_fusion_autotune_cache_dir` on a Modal Volume) plus 4 fits per container under MPS (`nvidia-cuda-mps-control -d`, `XLA_CLIENT_MEM_FRACTION` 0.21) | solo: sampler setup 20.6 → 15.4 s, process 239.5 → 231.6 s. K4+MPS: 162.3 s per fit for M5_238580 (solo 234.6 s), 103.5 s for M4_107643 (solo ≈ 157 s); $0.098 per M5 fit at the requested 2 cores and 16 GiB (Modal bills the larger of request and use) | The cache writer, its readers and the 4 concurrent fits share one hash, for M5 and for M4; without the cache, repeats differ and concurrent fits leave the solo sampler paths (entry 14). A galaxy's first fit autotunes its missing fusions (M4 added 256 to M5's 721 entries, 488 kB in all); if that first fit shares the GPU, those choices are made on a shared GPU | 15, 18 |

## Proposals that change results (measured, not kept)

M5_238580, L40S, 3 seeds per arm (20260832, 20261014, 20261015) unless noted. Seed scatter of the base: ln Z ± 0.07–0.11; medians ± 0.001–0.002 (logzsol, afe, logmass), ± 0.03–0.05 Gyr (t50).

| Change | Sampler s / process s | ln Z | Posterior medians (variant vs base) | ESS | Ledger |
|---|---|---|---|---|---|
| `num_inner_steps` 65 → 33 | 92.7 vs 178.7 / 159.5 vs 248.1 | +0.54 (236690.684 ± 0.031 vs .147 ± 0.108) | logzsol −0.2167 vs −0.2146; afe −0.0377 vs −0.0371; logmass 11.594 vs 11.593; t50 4.65 vs 4.60 Gyr | Kish 4350 vs 4366 | 8 |
| `num_delete` 100 → 250 | 122.5 vs 179.3 / 192.5 vs 251.6 | +0.02, but seed scatter 0.52 vs 0.11 | logzsol −0.2182 vs −0.2150; afe −0.0367 vs −0.0372; logmass 11.5933 vs 11.5930; t50 4.63 vs 4.60 Gyr | Kish −19%; ESS/s +15 to +27% | 11 |
| `logZ_tol` −5 → −3 | 167.2 vs 182.4 / 258.8 vs 279.0 | +0.009 (scatter 0.067) | logzsol −0.2148 vs −0.2137; afe −0.0366 vs −0.0367; logmass 11.5937 vs 11.5925; t50 4.60 vs 4.58 Gyr | Kish −1%; ESS/s +3 to +6% | 10 |
| XLA autotune level 0 (one seed, 3 repeats) | 181.0 vs 180.3 / 257.5 vs 267.5 | 236689.705 vs 236690.246/.260 | logzsol −0.216 vs −0.213/−0.216; afe −0.036 vs −0.038/−0.037; logmass 11.593 vs 11.593/11.597; t50 4.63 vs 4.61/4.66 Gyr | repeats bitwise identical | 4 |
| K fits per GPU under MPS (one seed) | per fit: K4 178.5 ± 6.2, K8 152.9 (e015bad; solo 245.5–256.5 on that build) | without an autotune cache: 17 of 40 fits on new paths, ln Z 236689.705–236690.375 (with the cache: bitwise, see the backend table) | logzsol −0.2164 to −0.2121; afe −0.0375 to −0.0359; logmass 11.5918–11.5967; t50 4.57–4.66 Gyr | Kish 4321–4442 | 14 |

## Rejected

- Requesting 8 cores (no gain over the 2-core request; entry 7).
- Jitted initial-mass `predict` (float32 photometry differs by up to 1.3e-7 on CPU; `theta_init` is stored; entry 9).

## Reused

- COSMOS read-once: cherry-pick of 35d8ac7 from the speedups branch.
- modal-gpu backend (scripts/modal_gpu.py, `experiment.py run`) for every end-to-end run; not edited.
- `experiment.py remote` and `run_ceridwen_vast_multi_gpu.py` for every A/B fit; `--fits-per-gpu` memory fraction (0.85/K) for the K runs.
- `scripts/build_dr2_quiescent_summary.formation_times` for t50; anesthetic for the ESS weight draws.
- ceridwen's step-kernel-in-a-thread design (ceridwen a60f1f8, project 07ff3dd) and its compile-once test; the 30 Sep XLA-flag, compile-cache and fits-per-GPU records as starting points.

## Notes

- The wiki was not edited (brief). Wiki code excerpts of fit-notebook cells 10 and 14 and of `nested.py` `run()` may now be out of date.
- tests: tests/test_experiment.py, test_modal_gpu.py, test_cosmos_photometry.py 68 passed; ceridwen suite 581 passed, 1 failed (test_ssp_provenance needs python-fsps, also at d7c0536). tests/test_emission_line_marginalisation.py and test_ceridwen_dr2_production.py: the same 8 failures with and without the branch's notebook change (stale logzsol/afe range, `CERIDWEN_PLOTS` env list, `mass_mapped_beta`).

## Phase 2: Modal backend (branch `hillclimb-2`, 2026-10-15)

- Kept in 49ac029 (scripts/modal_gpu.py, scripts/experiment.py): XLA command buffers on; a JAX compile cache, with XLA's autotune cache inside it, saved per galaxy setup on the Modal Volume `ceridwen-xla-cache`; 4 cached fits per GPU under MPS; several cells per container once an experiment has more than 10 cells.
- Same container (L40S, n = 3): command buffers −11.2 s per fit; a cached fit 197.8 s instead of 233.5 s (−15%); 4 cached fits on one GPU 151.6 s per fit (−35%). Cached and shared fits are bitwise identical to the fit that wrote the cache.
- End to end at 49ac029, billed by Modal: $0.160 per fit before; after, $0.159 for a setup's first fit, $0.147 for a rerun of a cached setup, $0.104 per fit when 4 reruns share a GPU.
- A sample run fits each galaxy once, and every galaxy is a new setup: the cache and MPS sharing then do nothing. Such a run gets command buffers (−11 s) less the cache save (+6 s), and several new setups per container (above 10 cells) halve the overhead outside the fit (15.3 vs 31.0 s): $0.149 per fit instead of $0.160 (−7%).
- Reliability: 99 of 99 phase-2 GPU fits finished and passed the stored convergence check, 93 of them with command buffers on.

### What the backend does now (49ac029)

| Part | Behaviour |
|---|---|
| Command buffers | On (XLA default); the `--xla_gpu_enable_command_buffer=` workaround for RTX 5060 kernel deaths (5eb6483) is dropped |
| Cache key | sha256 of image, GPU type, pinned source (commit and submodules) and the cell without its name and arm (target, seed, settings and priors stay) |
| Cache file | `<key>.tar` on the Volume: JAX compile cache (`JAX_COMPILATION_CACHE_DIR`, minimum compile time 0) with XLA's per-fusion autotune cache inside it; 1383 files, 97 MB for M5_238580. Unpacked to `/tmp/xla/<key>`, the same path wherever it is written or read |
| First fit of a setup | Alone on the GPU, on an empty cache; saves the tar (temporary name, then rename) |
| Cached fits | Read the tar. 2 or more in one container share the GPU under MPS, 4 at a time, `XLA_CLIENT_MEM_FRACTION` 0.21 |
| Guards | A shared fit that autotunes anything makes every shared fit of its setup refit alone. Programs a cached fit compiles anew without autotuning (another host fingerprint) are added to the tar |
| Containers | One per cell up to 10 (Starter plan: "10 GPU concurrency", modal.com/pricing); beyond 10, cells sorted by cache key share 10 containers. Cost is split equally across a container's cells |
| Records | Per cell in the manifest: `mode` (alone, cached, shared), `tuned` (autotune entries written), `compiled` (programs compiled), `retuned`, `container_cells` |

### Same container (modal_ab.py, L40S, d3ae726, n = 3)

| s | Base (buffers off, no cache) | Buffers on | Cache writer | Cache reader | 4 readers under MPS |
|---|---|---|---|---|---|
| Fit process | 233.5 ± 5.1 | 222.3 ± 5.2 | 223.6 ± 5.8 | 197.8 ± 2.6 | 151.6 ± 0.8 per fit (606 ± 3 per 4) |
| Model cell | 14.5 ± 1.3 | 13.5 ± 1.6 | 13.2 ± 1.7 | 4.8 ± 0.2 | 3.9 ± 0.2 |
| Sampler cell | 198.0 ± 2.4 | 190.6 ± 2.0 | 193.0 ± 2.5 | 177.7 ± 0.9 | 585 (concurrent) |
| Sampler wall | 179.5 ± 0.7 | 172.4 ± 0.3 | 172.2 ± 0.2 | 171.9 ± 0.4 | 578.8 ± 0.8 (concurrent) |
| Paired difference vs base | — | −11.2 ± 0.8 | −9.8 ± 0.8 | −35.7 ± 2.5 | — |

All 24 fits on the two standard sampler paths (3d78, 9ac5). In each container the writer, the reader and the 4 shared fits share one hash (20d8, 5c88, c870); in container 2, buffers off and on also share one (1362).

### End to end (`experiment.py run`, L40S, billed per app by `modal billing report`)

Validation at 49ac029 (runs/v2-*, runs/m4-*). Each round starts with the setup's tar deleted. "4 shared" reads a cache written in another container.

| | First fit of a setup | Cached rerun | 4 shared reruns, one container | Writer + 4 shared, one container | 4 new setups, one container |
|---|---|---|---|---|---|
| Container s per fit | 256.6 ± 4.7 (n 2) | 237.7 ± 6.4 (n 3) | 162.6 ± 4.7 (n 3 × 4) | 168.7 (n 1 × 5) | 242.9 ± 4.8 (n 3 × 4) |
| Billed $ per fit | 0.159 ± 0.003 | 0.147 ± 0.003 | 0.104 ± 0.003 | 0.106 | 0.149 ± 0.003 |
| Fits per GPU-hour | 14.0 | 15.1 | 22.1 | 21.3 | 14.8 |
| Fit / overhead s | 225.6 ± 1.1 / 31.0 ± 3.7 | 205.8 ± 6.7 / 28.6 ± 4.1 (n 7, both series) | — | — | 227.7 ± 6.8 / 15.3 ± 1.1 |

Old backend (d3ae726, series 1, runs/e2e2-old*): 257.1 ± 8.4 s, $0.160 ± 0.005 per fit, 14.0 fits per GPU-hour; fit 232.0 ± 6.4 s, overhead 25.1 ± 2.0 s. Series 1 ran the new backend before entry 23's fixes (runs/e2e2-*): first fit 263.7 ± 10.0 s, $0.166 ± 0.004; cached with a compile-cache hit 225.0 ± 0.8 s, $0.137 ± 0.001 (n 2), with a miss 238.9 ± 4.4 s, $0.150 ± 0.003 (n 2); 4 shared 164.3 ± 3.3 s, $0.105 ± 0.003 per fit (n 3 × 4).

"Overhead" is container time outside the fit notebook (bootstrap, the cache save, packing results). A first fit's save adds ≈ 6 s (31.0 vs 25.1 s). Billed cost runs 1–7% above the estimate (requested 2 cores and 16 GiB × container seconds). The manifest's `billed_usd`, read as the run ends, was 5–27% below the settled `modal billing report` value in these runs.

### Cache behaviour

- Saving a 97 MB cache takes 4.7 s (tar onto the Volume 2.1 s, commit 2.7 s); loading takes 1.8 s (probe container, 1383 files).
- jax 0.10.2 (the image) keys each compiled program by the autotune directory's path (`xla_gpu_per_fusion_autotune_cache_dir` is not cleared in jax/_src/cache_key.py; jax 0.11.1 clears it). A per-cell-index directory made shared cells at index 1–3 recompile all 663 programs; 49ac029 uses one path per setup key.
- JAX hashes the GPU topology fingerprint into every program key (jax/_src/cache_key.py `_hash_accelerator_config`), and L40S hosts differ: 4 fingerprints in 18 probe containers, with the same platform version, compile options and XLA flags (runs/keyprobe):

| Host | Driver | ECC, memory | Containers | GPU topology fingerprint |
|---|---|---|---|---|
| AMD | 610.57.04 | on, 46068 MiB | 3 | 11274905002941961806 |
| Intel | 610.57.04 | on, 46068 MiB | 6 | 7537698629312052454 |
| Intel | 610.57.04 | off, 49140 MiB | 6 | 886291908185532482 |
| Intel | 580.95.05 | on, 46068 MiB | 3 | 2913705999010927856 |

- So a cached fit reuses compiled programs only on a host with the writer's fingerprint (3 of 7 cached reruns here); every autotune entry hits on every host (0 autotuned in all cross-container reads), so the sampler path is always the writer's. A miss costs ≈ 13 s (227.2 vs 239.8 s container time; programs compile again) and adds that host's 663 programs (≈ 100 MB) to the tar; a setup's tar holds at most one program set per fingerprint.
- A new seed compiled 7 programs and autotuned 3 fusions on another seed's cache, so the seed is part of the key.
- Volumes are free up to 1 TiB per month (modal.com/pricing). Cache files are written once per setup and host fingerprint, so Volume v1 (no Beta data-loss caveat) is used.

### Cost per fit, throughput and ESS per second

ESS per fit is unchanged (the two standard sampler paths, as in phase 1); per-second values use the fit process time from the same-container A/B, mean of the two paths.

| | Base | Buffers on | Cached | 4 shared |
|---|---|---|---|---|
| Fit process s | 233.5 | 222.3 | 197.8 | 151.6 |
| Fits per GPU-hour (process) | 15.4 | 16.2 | 18.2 | 23.7 |
| Kish ESS per s | 18.8 | 19.8 | 22.2 | 29.0 |
| logzsol / afe / logmass / t50 ESS per s | 11.9 / 12.3 / 10.2 / 8.5 | 12.5 / 12.9 / 10.8 / 8.9 | 14.1 / 14.5 / 12.1 / 10.0 | 18.4 / 19.0 / 15.8 / 13.1 |

### Results identical (how checked)

- Same container: bitwise (result hash over every `samples/` dataset) for writer, reader and 4 shared fits in each container.
- End to end at 49ac029: all 22 fits on path 9ac5 (ln Z 236690.2596); every reader bitwise equal to its writer except the 5 that compiled on another host fingerprint (relative lnL ≤ 6.9e-12); two first fits in different containers differ by 8.7e-6 (entry 24). The 12 fits of entry 25 fit alone on an empty cache, as a single first fit does.
- Series 1: readers bitwise equal to their writer on compile-cache hits, else relative lnL max 1.9e-9; old-backend repeats 4.7e-10.

### Reliability (phase 2)

| Series | GPU fits | Finished and passed the stored check |
|---|---|---|
| Same-container A/B (runs/ab-modes*) | 24 | 24 |
| End to end, series 1 (runs/e2e2-*, 3 on the old backend) | 23 | 23 |
| Validation at 49ac029 (runs/v2-*) | 22 | 22 |
| 4 new setups per container (runs/m4-*) | 12 | 12 |
| Autotune level 0 A/B (runs/ab-at0mps*) | 18 | 18 |
| All | 99 | 99 |

Container start failures: 1 from a bootstrap environment bug of mine, fixed before 49ac029; 3 old-backend starts from a baseline worktree with symlinked inputs (Modal `AbsoluteLinkError`). No kernel deaths in 93 L40S fits with command buffers on; the RTX 5060 deaths behind 5eb6483 were not retested (GPU types are gpu-bench-modal's).

### Proposal that changes results: XLA autotune level 0 with 4 fits per GPU

`--xla_gpu_autotune_level=0` turns XLA's autotuning off. With nothing to autotune, a shared GPU cannot change a fit's kernels: in each container (runs/ab-at0mps*, one seed per container, n = 3) the 4 fits under MPS, without any cache, are bitwise identical to the solo fit, and seed 20260832 gives the same hash as phase 1's level-0 fits (entry 4). Every fit of a sample run would then get the shared-GPU gain, which the cache gives only to reruns.

| | Default solo | Level 0 solo | Level 0, 4 under MPS |
|---|---|---|---|
| Process s per fit | 233.3 ± 0.6 | 225.9 ± 1.0 (paired −7.3 ± 0.7) | 155.4 ± 1.1 |
| ln Z, seeds 20260832 / 20261014 / 20261015 | 236690.2461 / .1514 / .1782 | 236689.7049 / .9791 / 236690.1318 | bitwise as solo |
| Stored ln Z error | 0.26 / 0.31 / 0.32 | 0.17 / 0.20 / 0.23 | bitwise as solo |
| Medians logzsol / afe / logmass / t50, mean of 3 seeds | −0.2149 / −0.0366 / 11.5937 / 4.596 Gyr | −0.2165 / −0.0374 / 11.5940 / 4.643 Gyr | bitwise as solo |
| Kish ESS | 4442 / 4464 / 4438 | 4442 / 4441 / 4364 | bitwise as solo |

- ln Z moves by −0.54, −0.17 and −0.05 (mean −0.25); its seed scatter is 0.05 for the default here and 0.22 for level 0. Medians move by at most the phase-1 seed scatter (t50 +0.05 Gyr against ± 0.03–0.05 Gyr).
- Expected cost for a sample run with 4 fits per GPU: ≈ $0.105 per fit (4 shared reruns at 49ac029 measured 162.6 s and $0.104), against $0.149 with the kept backend. Not built: it changes results (rule 6).

### Not adopted

- `num_inner_steps` 33 and `logZ_tol` −3 (phase-1 proposals table): Liu Hao's call.
- Splitting each setup's tar per host fingerprint, so a fit loads only its own host's programs: ≈ 5 s per cached fit once a tar holds all 4 program sets (load 1.8 s per 97 MB); not built.
- Skipping the save for a setup's first fit: ≈ 6 s less overhead per fit in a sample run (31.0 vs 25.1 s), but reruns would then find no cache; kept as built.

### Reused (phase 2)

- modal-gpu backend structure (`fit`, `stage`, `main`, `ModalRun.execute`, the guard and stop fixes from modal-fix) extended, not replaced; `modal_gpu.cost_usd` for estimates.
- modal_ab.py and summarise.py from phase 1 for every A/B and summary; phase-1 benchmark galaxy, seeds and ESS method.
- XLA's own per-fusion autotune cache inside JAX's persistent compile cache (no hand-written cache); `nvidia-cuda-mps-control` for MPS.
