# Hill-climb report, 2026-10-14/15

- One benchmark fit on a Modal L40S now takes 234.6 s instead of 261.1 s (−10%), with identical results; cost per fit drops from $0.158 to $0.142 (fit process) and from $0.168 to $0.157 end to end.
- Five results-identical changes are kept on `hillclimb`: COSMOS catalogues read once, several cells in one notebook kernel, FilterSet built on the host, posterior-predictive programs compiled during the sampler, and the sampler's step-kernel compile started before the prior draw.
- Reliability: 154 of 154 GPU fits finished and passed the stored convergence check.
- Bigger sampler gains change results and need Liu Hao's call: `num_inner_steps` 33 halves the sampler time but moves ln Z by +0.54; `logZ_tol` −3 saves 8% of the sampler time with ln Z and posteriors unchanged within the seed scatter.
- The largest results-identical gain needs a modal-gpu backend change: an XLA autotune cache makes repeat fits bitwise identical and lets 4 fits share one L40S at 162 s each ($0.098 per fit); command buffers (−7 s), a compile cache (−16 s) and several cells per container (−29 s per extra fit) also need backend changes.

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

- Code: branch `hillclimb` at 62aba10 (ceridwen d61175d).
- Modal: L40S, 2 cores, 16 GiB, one fit per container, as scripts/modal_gpu.py does now. Do not request more cores: a container requested at 2 cores already runs at the 8-core time (261.0 vs ≈ 262 s, LEDGER entry 7), and Modal bills the larger of request and use.
- Cost per fit: $0.157 end to end ($0.142 for the fit process).
- If modal-gpu adopts the autotune cache on a Volume: 4 fits per container under MPS, $0.098 per fit for the benchmark galaxy.

## Proposals for the modal-gpu backend (results-identical, not kept: they change scripts/modal_gpu.py)

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
