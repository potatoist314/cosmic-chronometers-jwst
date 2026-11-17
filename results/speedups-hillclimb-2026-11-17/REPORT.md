# Speedups hill-climb, 17 Nov 2026

Window-194 arms `dr3_plain_w` and `dr3_cn_free_w`, A100-SXM4-40GB, seed 20260832, ceridwen 3b5177f. Base: Astro
2d000184. Kept build: Astro 377bf6ab (branch `speedups-hillclimb-2026-11-17`). Details and commands: `LEDGER.md`.

## Total

Modal cost at $0.000645 per container second (A100-40GB, 2 cores). Container start (image, inputs, kernel) 30.2 s.

| arm | fit alone | in one kernel: first / later fit | per fit, 13 fits per container | cost per fit, 13 per container |
|---|---|---|---|---|
| dr3_plain_w (Modal, 20 fits) | 84.0 s | 81.0 s / 51.9 s | 86.3 -> 56.5 s (-35 %) | $0.056 -> $0.036 |
| dr3_cn_free_w (Colab A/B, 2 fits) | 91.7, 92.3 s | 67.5, 66.3 s (later) | about 94 -> 71 s (-24 %) | about $0.061 -> $0.046 |

13 fits per container is the shape of the 16 Nov production run (130 fits, 10 containers). Real-path run: 20 plain
fits, 2 per container: container time 198.1 -> 163.1 s (-18 %), estimated $1.277 -> $1.052.

## Attempts

| # | attempt | gain | results | kept |
|---|---|---|---|---|
| 1 | Uncached fits of a container or Colab runtime in one kernel (`modal_gpu.batch`, `ColabRun.fit`) | plain later fits 74-80 -> 51 s; cn_free 92 -> 67 s | identical, 6 of 6 (Colab, same runtime) | yes |
| 2 | One compile cache for all galaxies of a run | M9 74.3 -> 68.2 s, M10 77.7 -> 69.2 s | ln Z equal | no: 1 gives more |
| 3 | Fewer CPU cores (4, 2 of 12) | 79.7 -> 81.0 s, 90.6 s | ln Z equal | no: slower |
| 4 | Both arms mixed in one kernel | as 1; host memory +0.3 GB per fit | identical, 6 of 6 | yes, with 1 |
| 5 | One ln L program for all galaxies | not built: 5 per-galaxy array shapes (SSP wavelengths 8618 / 8693, filters 28 / 30, fitted pixels 1630 / 1705, ...) | - | no |
| 6 | Catalogue read cached across fits | data cell 7.0 s alone, 0.1-2.3 s in a kernel already | - | not needed |

Full-fit check, final build, alone against one kernel, 3 galaxies per arm: median shift 0.000 sigma, width change
0.0 %, delta ln Z 0.000. Real path, base against new on Modal: 19 of 20 fits identical; M13_215951 differs by host
(its new fit is identical to the Colab fit).

## Needs his decision

- TF32 products: SFH basis as one float32 product (F1) and C/N tables with TF32 products (F2t), measured 16-17 Nov
  on this ceridwen: about -7 s plain and -9 s cn_free per fit; A100 delta ln L 0.54 and 0.49.
- SFH bin truncation (30 Sep patch, CPU ln L max 0.035): not measured on this build; it changes the SFH code that the
  upstream 2.0 merge is changing.

## Noticed, not done

- One ln L program for all galaxies would save about 10 s of compile per later fit; it needs padding through the
  ceridwen SSP, photometry and likelihood code, which the upstream 2.0 merge is changing.
- Compiling the next fit while the current fit samples would hide the same 10 s; XLA autotuning then shares the GPU
  with the sampler, which changed sampler paths under MPS in October.
- FilterSet eager compiles: 1.9 s in the first fit of a container; later fits 0.1-2.3 s.
