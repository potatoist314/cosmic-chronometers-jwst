---
title: M1_210210 emission-line marginalisation test
date: 2026-09-23
section: Analyses
theme: Single-fit accuracy
tags: [ceridwen, emission-lines, calibration, M1_210210]
job:
figures: [eline-off-spectrum.png, eline-off-photometry.png, eline-on-spectrum.png, eline-on-photometry.png]
---

## Fits

M1_210210; `eline_off` and `eline_on`, seed 20260832, COSMOS2025 photometry, order-10 calibration with constant prior 0.3, baked runtime. The on arm fixes \(z\) at the catalogue value; the off arm samples \(z\).

<figure>
<img src="figures/emission-line-marginalisation/eline-off-spectrum.png" alt="M1_210210 spectrum fit with emission-line marginalisation off">
<figcaption>Option off: observed spectrum and posterior-median fit; emission regions remain masked.</figcaption>
</figure>

<figure>
<img src="figures/emission-line-marginalisation/eline-off-photometry.png" alt="M1_210210 photometry fit with emission-line marginalisation off">
<figcaption>Option off: COSMOS2025 photometry and posterior fit.</figcaption>
</figure>

<figure>
<img src="figures/emission-line-marginalisation/eline-on-spectrum.png" alt="M1_210210 spectrum fit with emission-line marginalisation on">
<figcaption>Option on: observed spectrum and posterior-median fit, including the fitted lines.</figcaption>
</figure>

<figure>
<img src="figures/emission-line-marginalisation/eline-on-photometry.png" alt="M1_210210 photometry fit with emission-line marginalisation on">
<figcaption>Option on: COSMOS2025 photometry and posterior fit, including line flux.</figcaption>
</figure>

## Runtime

| Arm | Fit wall time [s] | Sampler wall time [s] | Likelihood calls |
| --- | ---: | ---: | ---: |
| Off | 1,898.3 | 891.5 | 8,424,501 |
| On | 4,321.6 | 3,275.7 | 6,145,311 |

## Line fluxes

Option on; posterior 16th, 50th and 84th percentiles. Units: \(10^{-18}\,\mathrm{erg\,s^{-1}\,cm^{-2}}\).

| FSPS line | Rest vacuum [Å] | 16th | Median | 84th |
| --- | ---: | ---: | ---: |
| Ba-8 3798 | 3799.0 | 4.58 | 5.56 | 6.63 |
| Ba-7 3835 | 3836.5 | 5.34 | 6.34 | 7.24 |
| [Ne III] 3869 | 3869.9 | 0.15 | 0.51 | 1.18 |
| He I 3888.63A | 3889.8 | 0.36 | 1.67 | 3.98 |
| Ba-6 3889 | 3890.2 | 4.16 | 6.50 | 8.21 |
| [Ne III] 3968 | 3968.7 | 0.05 | 0.15 | 0.36 |
| Ba-5 3970 | 3971.3 | 10.09 | 11.10 | 12.25 |
| [S II] 4070 | 4069.8 | 5.50 | 6.69 | 8.08 |
| [S II] 4078 | 4077.6 | 0.09 | 0.44 | 0.99 |
| Ba-delta 4101.76A | 4103.0 | 1.16 | 2.25 | 3.63 |
| Ba-gamma 4341 | 4341.7 | 4.64 | 6.09 | 8.00 |
| [O III] 4363 | 4364.3 | 6.54 | 8.11 | 9.85 |
| He I 4471.49A | 4472.8 | 0.11 | 0.41 | 1.17 |
| He II 4685.64A | 4687.0 | 0.10 | 0.40 | 1.08 |
| [Ar IV] 4711 | 4712.7 | 0.14 | 0.61 | 1.47 |
| [Ne IV] 4720 | 4721.4 | 1.49 | 3.30 | 5.18 |
| [Ar IV] 4740 | 4741.5 | 4.16 | 6.34 | 8.44 |
| Ba-beta 4861 | 4862.8 | 6.58 | 8.50 | 10.45 |
| [O III] 4931 | 4932.7 | 0.40 | 1.41 | 3.03 |
| [O III] 4959 | 4960.4 | 3.98 | 4.81 | 5.88 |
| [O III] 5007 | 5008.3 | 11.99 | 14.47 | 17.71 |
| [Ar III] 5192 | 5193.3 | 0.16 | 0.57 | 1.64 |
| [N I] 5200 | 5201.8 | 2.43 | 4.31 | 6.86 |

## Parameter shifts

| Parameter | Off | On | Shift |
| --- | ---: | ---: | ---: |
| Mass-weighted age [Gyr] | +5.075 | +4.667 | -0.408 |
| \([\mathrm{Fe}/\mathrm{H}]\) [dex] | -0.181 | -0.158 | +0.023 |
| \([\alpha/\mathrm{Fe}]\) [dex] | +0.050 | +0.048 | -0.003 |
| \(\log_{10}(M_\star/M_\odot)\) | +11.587 | +11.536 | -0.051 |
| \(\tau_{\mathrm{dust}}\) | +0.353 | +0.318 | -0.035 |
| Dust index | -0.994 | -0.989 | +0.005 |

## \(\mathrm{H}\beta\) residuals

| Half-width [km/s] | Pixels | Off mean | Off RMS | On mean | On RMS |
| ---: | ---: | ---: | ---: | ---: | ---: |
| ±300 | 26 | +0.334 | 0.568 | -0.050 | 0.484 |
| ±1,500 | 134 | +0.214 | 0.559 | +0.132 | 0.561 |

## Cost

| Vast charge | USD |
| --- | ---: |
| Failed setup host | $0.034 |
| Shared fit host | $0.415 |
| **Total** | **$0.449** |

<details>
<summary>Measurement notes and files</summary>

Posterior medians; shift is on minus off. Full intervals: [comparison.csv](/wiki/f/results/emission-line-marginalisation/comparison.csv).

Line flux source: [line-fluxes.csv](/wiki/f/results/emission-line-marginalisation/line-fluxes.csv). Twenty-three displayed lines share 21 free fluxes, including tied \([\mathrm{O\,III}]\) 4959/5007. The flat \(f\ge0\) prior allows positive medians without a detection.

Pull is (observed − posterior-median model) / effective uncertainty, on the same on-arm fitted pixels around catalogue \(z\). The off-arm model is evaluated in its masked line region. [Residual table](/wiki/f/results/emission-line-marginalisation/hbeta-residuals.csv).

Runtime source: [manifest](/wiki/f/results/emission-line-marginalisation/arms_manifest.json) and result HDF5 files. Both arms ran on Vast RTX 5060 Ti instance 52280855.

- [Off executed notebook](/wiki/f/results/emission-line-marginalisation/eline_off/210210-M1_210210/M1_210210_executed.ipynb) and [on executed notebook](/wiki/f/results/emission-line-marginalisation/eline_on/210210-M1_210210/M1_210210_executed.ipynb).
- [Executed comparison notebook](/wiki/f/results/emission-line-marginalisation/analysis.ipynb) and [research record](/wiki/r/e-emission-line-marginalisation/).
- Vast invoice charges: $0.034 for failed setup, $0.415 for the shared fit instance; total $0.449. Source: `results/emission-line-marginalisation/cost.json`.

</details>
