# Free speedups, overnight 2026-09-30

Branches: `speedups` in this repo and in `potatoist314/ceridwen` (ceridwen pinned at `2d5edc9`).

## Integration check, 1 October

`speedups` includes the four production commits through `absorption-mask` `759d7ba`. Host records and both wiki histories are retained. The root checkout's uncommitted work is unchanged.

Combined Ceridwen CPU checks: 70 targeted tests passed; 17,800 lnL and lnP values bitwise against `e8b7643`; production iterations 20 and 140 bitwise. Runner checks: 150 passed. Existing per-change GPU evidence is listed below and saved under `integrate/`; the complete combined tree has no new GPU timing.

The merged notebook suite has 3 passes and 5 failures: the historical posterior fixture lacks `diffuse_tau_noll`. The pre-merge test reproduces the same missing-parameter failure. Both current-default model tests pass. The fixture needs a separate repair; no reference values were changed.

Wiki: no length faults; all evidence references validate against the main checkout, and the merged pages build (50 notes) with that existing data. The isolated checkout lacks older evidence: the normal build and chrome audit fail, and 2 of 37 research tests fail, as before integration.
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
| `--fits-per-gpu K`: K cells at once under CUDA MPS (swarm-throughput) | 4 targets, fit stage 839 → 641 s (K=2), 607 s (K=4), one boot; 8 targets, 1098 s (K=4) → 957 s (K=8), one boot | result and derived h5 of all 4 targets bitwise vs K=1 at K=2 and K=4 (only `wall_time_s`); 8 targets K=8 vs K=4: 592 datasets, numeric bytes identical, strings equal; K=1 default unchanged | `468ffe4` (`faf650c`); records `39e271f` |
| KL figure: bootstrap and noise-floor KL values on threads | wall, this M1 Pro at load average 50–70: `kl_table` 10.9–20.5 → 4.7–6.1 s, SFH noise floor 4.1–7.8 → 3.4–3.8 s | results come back in input order; KL table and both noise floors of the production fit bitwise; test: threaded vs serial map on the stored eline_off fit | `987b0c7` |
| Local figure rebuild while later cells still run | a run of N one-at-a-time cells waits for 1 rebuild instead of N (40–47 s each on an idle M1 Pro, 3 min 20 s at load ~150); one-cell runs unchanged | same rebuild command and inputs; tests: rebuild during the run and only once, interrupted run kills the child and keeps the GPU derived bytes | `3dbc25f` |
| Lane kernel rounds: no likelihood call below the prior slice level; idle batch slots evaluate running lanes' next candidates, reused on a bitwise (step, t, position) match (swarm-sampler) | sampling 180.4 → 108.0 s, `BlackJAXNestedSamplerAdapter.run` 183.1 → 111.2 s (RTX 5090, one boot, host 662751); rounds at iterations 20 / 140: 376 / 427 → 156 / 245 | GPU, one boot: 168 iterations, logZ 236002.77080421132 and 5,478,067 calls in both, all 16,800 dead points and the adapter samples bitwise; CPU: `tests/test_nss_diagnostics.py` bitwise vs `blackjax.nss`, iterations 20 and 140 of the production model bitwise (worker), 2,000 dead points of 20 iterations bitwise (integrator) | `cadac99` (`a935a99`, `e8b7643`) |
| Stage polls wait on the box for the exit file | end of each billed stage (bootstrap, fit) seen within 0.1 s instead of ~2.5 s on average (half the 5 s poll interval) | no computation; runner tests, including a poll against a real exit file | `267888d` |
| First fit starts while the grid uploads; the notebook waits for the grid's sha256 check at the cell that loads it | host 132677, one run each: running → fit exit 3 min 42 s → 3 min 30 s; the fit started 6 s before the bootstrap ended instead of 7 s after it, and the grid was ready before its cell | result h5 of the production fit: all 35 datasets byte-identical to the `cadac99` fit on the same host; runner tests, including a wait that blocks on a real file | `f37e4c0` |
| Result download stopped after 30 s without new bytes, then resumed | a stalled first download (2 of 2 runs since 01:31 UTC, both host 132677) ends after ~31 s instead of 94–120 s; each retry took 12–15 s | no computation; tests, and openrsync over a transport that stops mid-file: stopped in 4 s with its ssh, partial file kept, the `--checksum` retry byte-identical | `0958e8d` |
| Stepping-out edges with no expansion left skip the batch (swarm-sampler) | box sampling 132.0/133.2 → 129.2/130.2 s, adapter.run 140.7 → 137.0 s (RTX 5090, instance 53616870) | GPU: spent payload is `ea91453` modulo docstring; spent/spent-b dead points and adapter-spent samples bitwise vs base (168 iterations, logZ 236002.77080421132, 5,478,067 calls; `integrate/gpu3/`, `results/speedups-swarm-sampler-2026-10-01/cpu/cmp2.py` re-run); CPU: `tests/test_nss_diagnostics.py` bitwise vs `blackjax.nss`, integrator replay of production iterations 20 and 140 bitwise vs `e8b7643` | `ea91453` |
| CSP: synthesise only the model wavelengths the observations read | GPU `model_predict` 8.14 → 7.35 µs per call at batch 100 (commit message) | 17,800 dead-point lnL and lnP bitwise on CPU (integrator replay vs `e8b7643`) and GPU (box dumps base vs cand same-boot 53604574 and vs cand2 cross-boot 53605629, autotune 0); full box fits on 53608103 (165 iterations, seed 20260927): logZ 236003.1618281287, 5,332,800 calls, all dead-point arrays bitwise; durables under `integrate/gpu-lik/` and `integrate/cpu/` | `578b310` (`bae8f56`) |
| Line-flux covariance from the line block of the Cholesky factor only | with the CSP change; no separate timing | with the CSP change (box dump-cand2 and fit-cand2 dead points bitwise vs base); `test_line_posterior_equals_the_full_triangular_solve_bitwise` | `2d5edc9` (`85d6288`) |
| Runner commands share one SSH connection per instance (ControlMaster auto, `%C` socket, ControlPersist 60); grid parts and result retrieval keep their own TCP streams | full-patch end-to-end timing unmeasured; session 7 new-connection commands cost ~3.5–3.9 s each | no computation; 150 runner tests; `ssh -G` accepts plain and shared options | `9d9bd93` |

## One production fit, before and after

M1_210210, `neb_eline_ca_nohe_zevo`, seed 20260927, RTX 5090, one run each.

| Stage | Before (`48f56a4`) | After (`48fdc7f`) | After (all, `04d4574`) | After (all, `f3cf417`, image 6ca819ac) | After (all, `cadac99`, image 6ca819ac) | After (all, `f37e4c0`, image 6ca819ac) |
|---|---|---|---|---|---|---|
| Offer search and refusals | 2.2 min | 26 s | 10 s (3 refusals) | 18 s (+2 refusals, 3 s) | 10 s (1 refusal) | 4 s |
| Failed hosts | — | — | 3.5 min: host 415547 container start failed (Vast shim missing; destroyed by hand after 1 min, the stall rule acts after ≥ 4 min), host 564477 outbid | 8.8 min: host 18 vanished mid-fit (6 min), host 415547 container start failed again and was replaced after 64 s by the new rule (2.5 min) | — | 2.1 min: host 127708 unavailable while loading, replaced by the runner |
| Instance loading | ~5.9 min | 7.3 min | 2 min 25 s | 1 min 46 s (cold host) | 1 min 10 s (host 132677, image layers cached) | 14 s (host 132677, image layers cached) |
| Upload and bootstrap | ~11 min (SSH wait, upload, bootstrap) | 1 min 58 s | 1 min 11 s | 53 s | 1 min 8 s | 1 min 3 s; the fit started 6 s before its end |
| Fit (box) | 11.8 min | 4.5 min | ≤ 3.8 min | 3.5 min | 2 min 34 s | 2 min 21 s after the bootstrap |
| Sampler wall | 628.2 s | 197.8 s | 187.6 s | 184.2 s | 106.6 s | 106.6 s |
| Sampler iteration 1 | | 17.0 s | 1.04 s | 1.02 s | 0.43 s | 0.43 s |
| Retrieval, teardown | 20 s | 12 s | 13 s | 23 s | 1 min 46 s: the first download stopped after 94 s with ssh exit 255; the retry took 12 s | 2 min 15 s: the first download stalled until the 120 s attempt timeout; the retry took ~15 s |
| Local figure rebuild | | 40.3 s | 47 s | 3 min 20 s (this Mac at load average ~150; 40–47 s unloaded) | 39 s (load average ~7; run again by hand: the worktree's venv imported another ceridwen checkout) | 40 s |
| Wall | 31.3 min | 14.6 min | 12.3 min (8.8 min without the failed hosts) | 19.5 min (10.7 min without the failed hosts) | 7.6 min (6.0 min without the stopped download) | 8.8 min (5.0 min without the failed host and the stall) |
| Billed GPU time | 23.2 min | 9.5 min | 4.9 min | 8.7 min by invoice, for 4.8 min from running to destroyed (+4.4 min on the vanished host) | 8.3 min by invoice, for 5.5 min from running to destroyed | 8.3 min by invoice, for 5.8 min from running to destroyed |
| Cost | $0.162 | $0.067 | $0.036 | $0.071 (+$0.031 on the failed hosts) | $0.059 | $0.059 ($0.000 on host 127708) |
| ln Z | 236001.315 ± 0.185 | 236001.806 ± 0.205 | 236001.239 ± 0.245 | 236001.239 ± 0.189 | 236001.239 ± 0.285 | 236001.239 ± 0.411 |

The `cadac99` fit (lane kernel rounds, host 132677) has the same 173 iterations and 5,624,104 likelihood calls as the earlier fits, and all 35 datasets of its `ceridwen_result.h5` are byte-identical to the fits on hosts 132677 (`c9d0b3f`, image 4da04a83) and 146008 (`de74870`), and so are those of the `f37e4c0` fit (host 132677); the ± differs between runs because `log_evidence_err` draws from numpy's global RNG.

The two intermediate images each gave a complete production fit: dcfc83f7 (host 146008) $0.066, bitwise equal to `04d4574`'s fit; 4da04a83 (host 132677) $0.056, bitwise equal to dcfc83f7's. Fits on i5-12400F hosts (132677, 146008) are bitwise equal to each other; the Ryzen 7 9800X3D host differs at 2.5e-13 in lnL through the CPU-computed filter wavelengths.

## Spend

Vast invoices, 30 Sep – 1 Oct 2026 (read 1 Oct, 00:1x, 01:0x and 02:2x UTC; session 7 from its run `charges.json`).

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
| session 6 (grid upload at 4, 8 and 12 streams) | 53613190 | $0.091 |
| e2e on `cadac99` (lane kernel rounds, stage polls) | 53619207 | $0.059 |
| e2e on `f37e4c0` (first fit during the upload) | 53622514 (unavailable while loading), 53622713 | $0.059 |
| session 7 (timed upload, transfer probes) | 53625717 | $0.061 |
| Total | 23 instances, all destroyed | $1.677 |

Every run stayed under its $1 cap; the largest was session 2.

## Session 7

Timed upload and transfer probes, 02:32–02:42 UTC, host 132677 (image layers cached), source `37399dd`, ceridwen `e8b7643`. Instance 53625717 destroyed 02:42:03 UTC; no instances left running.

Upload 57.38 s: new-connection SSH commands 3.5–3.9 s each, source archives 5.0/6.6/6.8 s, inputs rsync 14.49 s (`session7/run`, `gpu/session7.py`). Transfer probes: 3 of 10 showed stalls (78.9 s, 68.7 s, 163.1 s); without a stall 13 MB takes ~9 s on one stream or four. Post-fit pull 12.9 s, no stall. The box fit reached ln Z 236001.239 ± 0.281 with 5,624,104 calls in 106.6 s of sampling. Invoice: $0.057 GPU (0.140 h), $0.002 disk, $0.001 download, $0.001 upload (`session7/run/charges.json`).

## Not free: proposals, not built

| Proposal | Measured effect | Why not free |
|---|---|---|
| Tied doublet as elementwise sum instead of `profiles @ tie` | not measured on GPU | 1-ulp differences in 2 of 150,000 column elements on CPU (FMA) |
| Doublet `optimization_barrier` on each dot instead of the whole free matrix (uncommitted) | 92 of 1,780 CPU lnL differ, max 7.0e-10 (control: worker `trsm-s10` dump equals the clean subsample bitwise; dumps and patches under `integrate/cpu/`) | not bitwise; no GPU evidence; not integrated |
| SFH-basis table per-group bin truncation (`bins-truncation.patch`, unapplied) | 231 of 1,780 CPU lnL differ, max 0.035 (`integrate/cpu/dump-bins-s10.npz` vs clean baseline) | not bitwise; not integrated |
| `jax.jit` of the emission-line columns | | 1,049,770 elements differ on CPU, max 4.0e-28 |
| `jax.jit` of `posterior_draws_with_lines` | 3.89 → 1.64 s (CPU) | 3e-10 relative differences |
| Masked-row compaction / windowed Gram matrix | windowed Gram: 2,560 of 17,800 GPU lnL differ, max 1.7e-8 | reorders sums |
| XLA probes `f1` (Triton GEMM off), `f2` (also cuBLASLt on) | both dumps differ from the candidate baseline on all 17,800 GPU lnL; jobs and dumps under `integrate/gpu-lik/` | cause unresolved; not accepted or integrated |
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
| Default `--fits-per-gpu` K = pending cells up to 4, K=8 for 8+ cells (swarm-throughput) | 1.38× (K=4 vs K=1), 1.15× more at K=8 | results bitwise; K=4 peaks at 21.3 GB host RAM and K=8 at 37.2 GB, which the offer filter does not check; a bid rental stopped mid-stage loses all K cells; one-fit runs gain nothing |
| Two 100-row likelihood batches per round, the second for each lane's next candidate (swarm-sampler) | CPU rounds 156 / 245 → 141 / 175 | RTX 5090, one boot: sampling 108.0 → 155.0 s, 165 iterations, logZ 236003.45: not bitwise on GPU, and slower |
| Larger or compacted likelihood batch (swarm-sampler) | after `e8b7643` a round costs about one 100-row batch (~3.2 ms on RTX 5090) | the row count changes lnL bits on CPU |
| vmapping several fits into one sampler (swarm-throughput) | MPS with 4 fits already reaches the batch-500 gain (1.26–1.34×) | changes row counts, so lnL bits change; not proposed |
| zstd image layers | cuBLAS layer 581 → 468 MB at `zstd -19` (−19.5%; `gzip -9` −0.1%), decompression 3.1 → 2.3 s; ~18 s per cold host at the 24 MB/s seen on host 383511 | results unchanged, but pulls need Docker Engine ≥ 23.0 (moby v23.0.0 release notes) and Vast does not report host Docker versions: an older host fails to start |

## Tried; not possible

- Sampler, measured with no gain (swarm-sampler): hoisting the covariance Cholesky and inverse (XLA already hoists it); post-run finalise ~0.1 s; host loop between iterations ~1 ms; `free_moves` 4 / 8 / 12 within 2% on GPU (109.8 / 109.9 / 111.9 s).

- Removing cuDNN: XLA's GPU compiler requires DNN support (`RET_CHECK dnn_support != nullptr`, `gpu_compiler.cc:2798`).
- Removing cuSOLVER or cuSPARSE: the likelihood's `cholesky`/`inv` call `gpusolverDnCreate`, which fails with either library hidden.
- cuFFT, cuBLAS, nvrtc, cupti, cudart, nvJitLink: loaded in every job (`session5/run/out/libs-*.txt`).
- More grid upload streams: one boot (host 156806), the 473 MB packed grid, jobs 61–69 in `session6` (41–46 are void: `xargs -I@` also replaced the `@` in `user@host`). 4 streams 47.1–48.6 s, 8 streams 46.9–48.0 s (one 118.7 s trial timed out on a part). At 12 streams 2 of 3 trials lost parts to `kex_exchange_identification: read: Connection reset by peer`: sshd drops unauthenticated connections past `MaxStartups`, default 10:30:100 (sshd_config(5)). This Mac's upload capacity is 13.2 MB/s (`networkQuality`); 4 streams already reach 9.8 MB/s.

## Blocked

- Merging `absorption-mask` into `speedups`: refused by the permission classifier; Liu Hao's call.
