# Speedups handoff (overnight 2026-09-30 + integration)

For an agent continuing this work. The full record is `REPORT.md` in this
directory; this file summarises what changed, how fast it got, and where the
proof lives. Branch `speedups` (astro + `potatoist314/ceridwen` submodule).

Reference fit everywhere below: M1_210210, `neb_eline_ca_nohe_zevo`, seed
20260927, nebular grid, RTX 5090, image `6ca819ac` unless stated.
"Free" = bitwise-identical on CPU; on GPU, equal within the float rounding
the kernel already shows between rentals.

## Bottom line (one production fit, same config)

| Stage | Before (`48f56a4`) | After (`f37e4c0`) |
|---|---|---|
| Sampler wall | 628.2 s | 106.6 s |
| Sampler iteration 1 | — | 0.43 s |
| Fit (box) | 11.8 min | ~2.4 min |
| Wall (no failed hosts/stalls) | 31.3 min | ~5.0 min |
| Cost | $0.162 | $0.059 |
| ln Z | 236001.315 ± 0.185 | 236001.239 ± 0.411 |

Later: `e2e-combined` (source `4fa1b1d`, ceridwen `2d5edc9`) reproduces the
`e2e-early` trajectory bitwise (173 iters, 5,624,104 calls, H5 evidence
236001.23886529845) in 99.55 s sampling. The ten-galaxy production-defaults
run (`results/quiescent-test-set-speedups-2026-10-01/`, commit `187b7ad`)
validates 10/10 (sampling 68–96 s each).

## Sampler (ceridwen/sampler)

- Lane slice kernel made default: sampling 253.2 → 108.7 s. GPU diffs are
  float32 rounding only. `ae7392c` (`8161d3d`).
- Lane rounds (no likelihood call below the prior slice; idle slots evaluate
  lookahead; bitwise-matched reuse): sampling 180.4 → 108.0 s,
  adapter.run 183.1 → 111.2 s (one boot). 168 iters, logZ and calls
  identical; 16,800 dead points + adapter samples bitwise.
  `cadac99` (`a935a99`, `e8b7643`). Tests: `test_nss_diagnostics.py`
  (bitwise vs `blackjax.nss`), `test_ns_checkpoint.py`.
- Edge-skip (stepping-out edges with no expansion left skip the batch):
  box sampling 132.0/133.2 → 129.2/130.2 s, adapter.run 140.7 → 137.0 s;
  production iters 20/140 take 150/238 rounds. Dead points + samples
  bitwise. `ea91453`. Proof: `integrate/gpu3/` + `cpu/cmp2.py` re-run.
- Step kernel compiles during sampler init: GPU to-iteration-1-done
  9.86/9.84 → 7.66/7.62 s (iter 1: 4.92 → 0.98 s). `07ff3dd` (`a60f1f8`).

## Likelihood (ceridwen/likelihood, csp)

Microbenchmarks: µs/call at batch 100 (one boot).

- Emission-line columns on 40σ windows: 38.1 → 32.6 µs. `92d1483`.
- Tied doublets as column gather: 32.6 → 30.0 µs. `e663683`.
- One-select line-window placement: 30.0 → 27.7 µs (batch 500: 27.1 → 22.2).
  `48fdc7f`. Together: zevo sampling 254.5 → 185.5 s. All: 17,300
  dead-point lnL bitwise, CPU and GPU.
- CSP model-support synthesis (compute only observed wavelengths):
  `model_predict` 8.14 → 7.35 µs. 17,800 lnL+lnP bitwise CPU and GPU;
  full box fits bitwise (logZ 236003.1618281287, 5,332,800 calls).
  `578b310` (`bae8f56`). Test: `tests/csp/test_wavelength_support.py`.
- Line-block triangular solve (posterior from the Cholesky line block only):
  no separate timing; bitwise with the CSP change. `2d5edc9` (`85d6288`).
- Sparse filter-grid interpolation: 6–15 s → 0.01–0.04 s per fit; `_T`
  bitwise for 7 targets. `25824a4`.

## Runner, setup, teardown (scripts/)

- XLA autotune level 0: −7.6 s/fit (init 6.2 → 2.1 s, iter1 7.8 → 4.3 s);
  level-0 runs are mutually bitwise in one boot; cross-rental lnL within
  8.3e-7. `ff005a2`.
- Catalogues read once per process: −4.2 s. `35d8ac7`.
- Refusals parsed, next offer at once (~1 s vs 1–2 min). `07ddf22`.
- Smaller/faster upload: drop tests+dist (−68.5 MB); packed grid beside
  source (612 → 473 MB, parallel); 4-way rsync parts (~2× MB/s).
  `eaa86d3`, `9003842`/`61e824a`, `66745cd`.
- Fewer SSH round trips: one call per poll (~1.8 s), one per cell setup,
  no second listing at teardown, box-side exit-file wait (0.1 s vs ~2.5 s).
  `4aa058e`, `7f04c7b`, `4ea4cde`, `267888d`.
- Overlap: bootstrap during grid upload (118 → 61–71 s); first fit starts
  during upload (running→fit-exit 3:42 → 3:30, byte-identical h5).
  `16ba69e`, `f37e4c0`.
- Recovery: outbid/vanished instance replaced (was open-ended, 12 min
  observed); failed container replaced after 60 s (≥4 min → 64 s);
  stalled download stops after 30 s idle and resumes (~31 s vs 94–120 s).
  `269633f`, `5b3e186`, `0958e8d`.
- Shared SSH per instance (ControlMaster auto, Persist 60; bulk grid parts
  and retrieval keep own TCP streams). End-to-end timing unmeasured.
  150 runner tests. `9d9bd93`.

## GPU image (6ca819ac; Actions-built, verified per layer)

- Holds Vast's SSH-launch packages: derived-image step 24–30 s → ~6 s.
- Split 3.5 GB venv layer in 11: created→running ~6–7 min → ~2 min.
- Drop NCCL/NVSHMEM: 3.68 → 3.05 GB compressed; production fit bitwise.
- Drop 8 unused cuDNN libs: 3.05 → 2.32 GB; fit bitwise except `wall_time_s`.
- Drop libcusolverMg/libcufftw/nvrtc-builtins: 2.32 → 2.15 GB.
  Commits `8515f8f` → `f3cf417` (see REPORT for run numbers).

## Throughput and local rebuild

- `--fits-per-gpu K` under CUDA MPS (default K=1 unchanged): 4 targets
  839 → 641 s (K=2) / 607 s (K=4); 8 targets 1098 → 957 s (K=8). All h5
  bitwise vs K=1. `468ffe4`. Records `39e271f`.
- 5090 kept: fastest and cheapest/fit to ~$0.44/h; next best (A100 SXM4)
  1.30× slower. `results/speedups-swarm-throughput-2026-09-30/types`.
- Local figure rebuild overlaps later cells (1 rebuild wait instead of N);
  KL sorts shared/threaded (kl_table ~2×, marginal KL 2.25 → 1.23 ms/call).
  All bitwise. `3dbc25f`, `8b02c95`, `27df4f7`, `987b0c7`.

## Rejected — do not retry without new evidence

REPORT "Not free" + "Tried" tables are the authority. Highlights: doublet
barrier-per-dot (92/1,780 CPU lnL differ); bins truncation (231/1,780,
max 0.035); windowed Gram (2,560/17,800 GPU lnL); XLA f1/f2 flag probes
(all 17,800 differ, cause unresolved); 2-batch lane rounds (slower and
not bitwise on GPU); K>1-by-default (RAM/stop risk); zstd layers (old
Docker fails); host-Docker-aware ranking (conflicts with rental rule).

## Exactness notes for the next agent

- `log_evidence_err` draws from numpy's global RNG: it legitimately varies
  run to run (0.14–0.41 observed at identical code). Compare values, not it.
- Cross-host: i5-12400F hosts are mutually bitwise; Ryzen differs at
  2.5e-13 in lnL via CPU-computed filter wavelengths; one host (383511)
  showed 17 derived sets + 1-ulp logZ wobble at identical code.
- Combined-tree derived draws differ from `e8b7643` at ≤6.3e-14 relative
  (10/39 sets); same-host control attributes this to the new GPU op
  sequences (inference, not proven op-level). Fit trajectory is bitwise.
- Local figure rebuild must run with `PYTHONPATH` pointing at the pinned
  worktree ceridwen/sedpy, or the kernel imports the stale main-checkout
  ceridwen (`ImportError: mass_mapped_beta`). GPU result/derived bytes are
  authoritative; verify sha256 after any rebuild.

## Where things are

- `REPORT.md` (this dir): per-change table, e2e stage table, spend ($2.311
  / 25 instances, every run under its $1 cap), session logs, GPU proofs.
- `integrate/`: durable GPU/CPU proof artifacts (gpu3, gpu-lik, cpu dumps,
  patches, comparison scripts).
- `e2e-combined/`: combined-tree validation fit + manifest + charges.
- `results/quiescent-test-set-speedups-2026-10-01/`: ten-galaxy
  production-defaults run (commit `187b7ad`), 10/10 validated.
- `results/speedups-swarm-{likelihood,sampler,throughput}-2026-*-*/`:
  worker records (`cpu/`, `sessionN/`, payload/dump comparisons).
- Baselines: `e2e-early` (f37e4c0/e8b7643, same image — code-parent
  baseline); `results/m1-210210-neb-eline-ca-nohe-zevo-2026-09-30/`
  (production code `dc1dbec`, same config).
- Runner: `python3 scripts/experiment.py run <config> --gpu "RTX 5090"`;
  `--dry-run` preflights; `--spend-cap 1`; policy in `AGENTS.md`
  (reliability >99.5%, bandwidth <$10/TB, host-record ranking).
