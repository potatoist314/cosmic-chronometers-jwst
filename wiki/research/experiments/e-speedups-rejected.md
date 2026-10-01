---
kind: experiment
id: e-speedups-rejected
title: Rejected overnight speedup options
date: 2026-10-01
origin: existing
status: recorded
question: q-compute
source_notes: speedups-follow-ups
---

## Context

Overnight campaign of 30 Sep 2026 measuring candidate Ceridwen speedups on the M1_210210 zevo model; options that changed results, showed no gain, were never tried, or need Liu Hao's decision.

## Runs

```json
[]
```

## Figures

```json
[]
```

## Measurements

| Option | Differing \(\ln L\) | Max difference | Source |
| --- | --- | --- | --- |
| Barrier per dot, CPU | 92 / 1,780 | \(7.0\times10^{-10}\) | [dump-bar-s10.npz](https://github.com/potatoist314/cosmic-chronometers-jwst/blob/4fa1b1df0249548a7da8959edd6c8009395082f8/results/speedups-overnight-2026-09-30/integrate/cpu/dump-bar-s10.npz) |
| Bin truncation, CPU | 231 / 1,780 | 0.035 | [dump-bins-s10.npz](https://github.com/potatoist314/cosmic-chronometers-jwst/blob/4fa1b1df0249548a7da8959edd6c8009395082f8/results/speedups-overnight-2026-09-30/integrate/cpu/dump-bins-s10.npz) |
| XLA f1/f2, GPU | 17,800 / 17,800 |  | [dump-f1.npz](https://github.com/potatoist314/cosmic-chronometers-jwst/blob/4fa1b1df0249548a7da8959edd6c8009395082f8/results/speedups-overnight-2026-09-30/integrate/gpu-lik/dumps/dump-f1.npz) |
| Windowed Gram, GPU | 2,560 / 17,800 | \(1.7\times10^{-8}\) | REPORT, Not free table |

## Results

Barrier relocation: 92 of 1,780 CPU \(\ln L\) differ, max \(7.0\times10^{-10}\). SFH bin truncation: 231 of 1,780 differ, max 0.035. XLA f1/f2 probes: all 17,800 GPU \(\ln L\) differ; cause unresolved. Windowed Gram: 2,560 of 17,800 differ, max \(1.7\times10^{-8}\). Full option tables are in the source note.

## Caveats

Run evidence lives on the `speedups` branch at the pinned commit, not in this checkout.

## References

- [Overnight REPORT](https://github.com/potatoist314/cosmic-chronometers-jwst/blob/4fa1b1df0249548a7da8959edd6c8009395082f8/results/speedups-overnight-2026-09-30/REPORT.md) · [Preserved evidence tree](https://github.com/potatoist314/cosmic-chronometers-jwst/tree/4fa1b1df0249548a7da8959edd6c8009395082f8/results/speedups-overnight-2026-09-30/integrate)
- [speedups-follow-ups · source note](wiki/notes/speedups-follow-ups.md)
