# Ceridwen GPU benchmark check

Use this check before another Vast.ai rental for the 2026-09-23 price benchmark.
Use `scripts/benchmark_ceridwen_vast.py` and `scripts/sweep_ceridwen_vast_gpus.py`.
Read `~/.claude/projects/-Users-liuhao-Downloads-Astro-project/memory/vast-benchmark-methodology.md`.
Do not use `scripts/bench_gpu_prices_vast.py` or its driver design.

## Checks before a rental

1. Check `results/gpu-benchmark-2026-09-23/matrix.json` and `results/gpu-benchmark-2026-09-23/sol/manifest.json` for tried hosts and offers. Do not retry them.
2. Require reliability above 99.5%. Apply the user's hourly rental ceilings and the $1.50 task cap in `~/.claude/scripts/workspace-overseers/caps/gpu-bench.json`.
3. Pin one project revision for all hosts. The current comparison uses `c869309c374bb7976b4bb9729a0650043fbfb4f7` and the M1_210210 defaults.
4. Upload only the source needed by the benchmark. A full Git clone transferred unrelated results and wasted rental time.
5. Confirm that `/workspace/cosmic-chronometers-jwst/data/raw` exists before `rsync` starts.
6. Confirm that the private `ceridwen` and `external/sedpy_jax` submodules exist on the host before bootstrap. Upload their pinned local revisions. A remote GitHub clone cannot authenticate.
7. If SSH drops, check the same instance. Check remote processes before another checkout or upload. A closed SSH channel can leave the remote command running.
8. Estimate the remaining cost on this host and the cost of a fresh host. Keep the cheaper path within the task cap. Do not use a fixed 8-minute or 15-minute teardown rule.
9. After a measurement, destroy only its task-owned instance with `vastai destroy instance <id> -y`. Confirm its absence with `vastai show instances`.

## Errors observed in this benchmark

| Host or offer | Instance | Observed error | Check before another rental |
| --- | ---: | --- | --- |
| RTX 5090 host 18 | None | Vast returned no instance JSON on repeated create attempts. | Mark the host and offer as tried after the first failure. |
| RTX 5080 host 54814 | None | Vast returned no instance JSON repeatedly. Later create replies reported HTTP 400 and 410 for offer 48484148. | Never retry a gone offer or its host. |
| RTX 5090 host 20317 | None | Vast returned HTTP 410 for offer 50259928. | Never retry the gone offer or its host. |
| RTX 5090 host 366851 | 52248243 | The instance became `offline` before it ran. | Check live status and compare the cost of waiting with replacement. |
| RTX 5060 Ti host 49107 | 52254606 | `_checkout_clean` raised `NameError` because the driver lacked `shlex`. The host was not at fault. | Compile and inspect the existing sweep before a rental. |
| RTX 5070 Ti host 166757 | 52256098 | The earlier driver destroyed the host after eight minutes without SSH. | Use the cost comparison; do not apply the old timeout. |
| RTX 5060 Ti host 605466 | 52256099 | The earlier driver destroyed the host after eight minutes without SSH. | Use the cost comparison; do not apply the old timeout. |
| RTX 5060 Ti host 62819 | None | Vast returned HTTP 400 for offer 44053742. | Never retry the gone offer or its host. |
| RTX 5060 Ti host 152538 | 52259479 | A remote clone of the private submodules requested GitHub credentials. | Upload the pinned local submodule trees. |
| RTX 5060 Ti host 516546 | 52260284 | A full-history root clone transferred about 1.1 GB before it was stopped. | Transfer only the required pinned source. |
| RTX 5090 host 90577 | 52265958 | SSH closed during checkout. The old cleanup destroyed the live instance. | Reconnect and inspect the same instance before any replacement. |
| RTX 5090 host 109053 | None | Vast returned no instance JSON for offer 39179900. | Mark the host and offer as tried. |
| RTX 5090 hosts 43794 and 362094 | None | Vast returned no instance JSON for offers 49539124 and 48425192. | Mark each host and offer as tried. |
| RTX 5080 host 580434 | 52276783 | SSH drops left overlapping Git clones. A later `rsync` failed because the new source upload lacked `data/raw`. Cleanup destroyed the instance before measurement. | Stop duplicate remote clones. Create `data/raw` before transfer. Retain a live instance when a short repair costs less. |
| RTX 5090 host 60576 | 52283516 | Vast remained in `created` without an SSH port after image load. The sweep destroyed it after an invalid cost comparison. Vast billed $0 GPU time and $0.005 disk for this instance. | Price `created` and `loading` waits at the disk rate. Check the bill. Treat a missing instance as gone. |
| RTX 5090 host 526342 | 52287384 | The image pull stayed at one status. One fresh offer appeared $0.0017 cheaper in the estimate, and the sweep destroyed this host. Vast billed $0 GPU time and $0.003 disk. | Require a clear savings margin and repeated cheaper estimates before replacing a loading host. |

The prior RTX 5060 result, 27,754 calls/s on host 166946, used an earlier code revision. Do not use it for ratios to the current 5060 Ti runs. Cross-host timings can vary with host load. Keep the per-host raw timing JSON and report both hosts.
