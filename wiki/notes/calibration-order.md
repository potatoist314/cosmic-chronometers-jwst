---
title: Calibration polynomial order
date: 2026-09-15
section: Analyses
theme: Single-fit accuracy
tags: [calibration, ceridwen, dr2-quiescent-sample]
job:
figures: [parameters-by-order.png, sfh-histories.png, polynomial-vectors.png, coefficients.png, fit-M5_173928.png, chi2-M1_206545.png, corner-M1_206545.png]
---

## Setup

Arms
: Six reference galaxies, Chebyshev orders 3 (`new_default`), 5 (`poly5`) and 10 (`poly10`), coefficient prior \(\operatorname{Normal}(0, 0.1)\) at each order, cosmos_total photometry, StudentT SFH prior, free dust index, \(\tau_{\mathrm{dust}} \sim \operatorname{Uniform}(0, 0.2)\). Same seed per galaxy across orders. `scripts/calibration_arms_vast.py`.

Baseline
: The stored `results/fit-accuracy-knobs/new_default` fits used \(\tau_{\mathrm{dust}} \sim \operatorname{Uniform}(0, 2)\), so the order-3 arm was rerun with the current prior into `results/calibration-order/new_default/`. All 18 fits ran on one RTX 5060 (Vast instance 51132758); orders 5 and 10 on ceridwen 30cc016, order 3 on 56505a6 (same likelihood value, faster arithmetic).

Rule
: Meeting 2026-09-15: minimum calibration mode length 100 \(\text{\AA}\). Shortest mode = fitted span / order. Order 10: 242–247 \(\text{\AA}\) observed (125–154 \(\text{\AA}\) rest frame), maximum permitted order 24 in the observed frame.

## Evidence and parameters

| galaxy | S/N | \(\Delta \ln Z\) 5−3 | \(\Delta \ln Z\) 10−3 | \(t_{50}\) order 3 | \(t_{50}\) order 5 | \(t_{50}\) order 10 | phot \(\chi^2\) 3 / 5 / 10 | wall 3 / 5 / 10 [s] |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| M12_98104 | 7 | +4 | +20 | 4.05 ± 0.53 | 3.35 ± 0.31 | 4.07 ± 0.55 | 25 / 19 / 15 | 403 / 469 / 723 |
| M5_173928 | 13 | +224 | +555 | 5.02 ± 0.24 | 5.48 ± 0.23 | 5.51 ± 0.00 | 31 / 41 / 68 | 469 / 544 / 937 |
| M4_108989 | 21 | +263 | +284 | 4.84 ± 0.21 | 5.15 ± 0.17 | 5.15 ± 0.16 | 17 / 18 / 21 | 481 / 542 / 916 |
| M12_185653 | 22 | +23 | +29 | 4.79 ± 0.51 | 4.34 ± 0.40 | 4.67 ± 0.50 | 11 / 10 / 10 | 365 / 406 / 691 |
| M1_206545 | 31 | −2 | +305 | 5.10 ± 0.06 | 5.11 ± 0.07 | 6.07 ± 0.01 | 64 / 68 / 46 | 571 / 643 / 982 |
| M5_172669 | 105 | +82 | +427 | 2.00 ± 0.11 | 2.12 ± 0.16 | 2.29 ± 0.20 | 13 / 14 / 11 | 554 / 609 / 1033 |

\(t_{50}\): median ± half the 16–84 range, in Gyr. Wall time covers sampling only, same boot for all 18 fits.

| galaxy | \(\tau_{\mathrm{dust}}\) 3 / 5 / 10 | \(\delta_{\mathrm{dust}}\) 3 / 5 / 10 | \(\log_{10} M_\star\) 3 / 10 | \(P_{\max}/P_{\min}\) 3 / 5 / 10 | max \(|a_n|\) 3 / 5 / 10 |
| --- | --- | --- | --- | --- | --- |
| M12_98104 | 0.195 / 0.195 / 0.192 | −0.94 / −0.94 / −0.82 | 11.142 ± 0.039 / 11.158 ± 0.041 | 1.16 / 1.15 / 1.26 | 0.071 / 0.058 / 0.074 |
| M5_173928 | 0.199 / 0.199 / 0.199 | −0.99 / −0.99 / −0.99 | 11.633 ± 0.013 / 11.661 ± 0.008 | 1.21 / 1.26 / 1.68 | 0.083 / 0.072 / 0.089 |
| M4_108989 | 0.193 / 0.197 / 0.197 | −0.89 / −0.98 / −0.98 | 11.792 ± 0.015 / 11.809 ± 0.010 | 1.11 / 1.25 / 1.25 | 0.044 / 0.055 / 0.053 |
| M12_185653 | 0.187 / 0.180 / 0.187 | −0.10 / 0.05 / 0.06 | 11.074 ± 0.031 / 11.064 ± 0.028 | 1.10 / 1.20 / 1.14 | 0.025 / 0.040 / 0.033 |
| M1_206545 | 0.198 / 0.199 / 0.197 | −0.99 / −0.99 / −0.98 | 11.552 ± 0.008 / 11.614 ± 0.008 | 1.41 / 1.38 / 1.42 | 0.107 / 0.101 / 0.110 |
| M5_172669 | 0.199 / 0.199 / 0.197 | −0.99 / −0.99 / −0.98 | 11.305 ± 0.014 / 11.337 ± 0.022 | 1.17 / 1.19 / 1.27 | 0.076 / 0.075 / 0.081 |

<figure>
<img src="figures/calibration-order/parameters-by-order.png" alt="Posterior medians and 16-84 ranges of mass, t50, dust, dust index, mass-weighted age and calibration noise floor for six galaxies at orders 3, 5 and 10">
<figcaption>Posterior medians and 16–84 ranges by parameter, galaxy and order.</figcaption>
</figure>

<figure>
<img src="figures/calibration-order/sfh-histories.png" alt="Star-formation histories and cumulative mass fractions for six galaxies at orders 3, 5 and 10">
<figcaption>Star-formation histories and cumulative mass fractions by order.</figcaption>
</figure>

## Polynomial

<figure>
<img src="figures/calibration-order/polynomial-vectors.png" alt="Calibration polynomial P(lambda) for six galaxies at orders 3, 5 and 10, and the difference from the order-3 median">
<figcaption>\(P(\lambda)\) by order and difference from the order-3 median, dotted across masked pixels.</figcaption>
</figure>

<figure>
<img src="figures/calibration-order/coefficients.png" alt="Posterior magnitude of each Chebyshev coefficient against index for six galaxies at orders 3, 5 and 10">
<figcaption>\(|a_n|\) against \(n\), dashed line at prior width 0.1.</figcaption>
</figure>

## Fits

<figure>
<img src="figures/calibration-order/fit-M5_173928.png" alt="M5_173928 spectrum and photometry with the order 3, 5 and 10 posterior medians">
<figcaption>M5_173928: spectrum and photometry, posterior medians at orders 3, 5 and 10.</figcaption>
</figure>

<figure>
<img src="figures/calibration-order/chi2-M1_206545.png" alt="M1_206545 spectral pulls at the order-3 noise floor and cumulative raw chi-squared along the spectrum for orders 3, 5 and 10">
<figcaption>M1_206545: spectral pulls using order-3 \(f_{\mathrm{calib}}\) and cumulative raw \(\chi^2\).</figcaption>
</figure>

<figure>
<img src="figures/calibration-order/corner-M1_206545.png" alt="M1_206545 posterior corner plot at orders 3, 5 and 10">
<figcaption>M1_206545: posterior corner plot by order.</figcaption>
</figure>

<details>
<summary>Caveats</summary>

One seed per galaxy and order. \(\tau_{\mathrm{dust}}\) is at the 0.2 prior edge and \(\delta_{\mathrm{dust}}\) at the −1.0 bound at every order for five of six galaxies. At order 10, M5_173928 and M1_206545 have mass in the oldest SFH bin and \(t_{50}\) half-widths of 0.00–0.01 Gyr. Raw spectral \(\chi^2\) decreases with order for every galaxy, while photometric \(\chi^2\) increases for M5_173928 (31 to 68). Stored spectral \(\chi^2\) uses each fit's \(f_{\mathrm{calib}}\), with no comparison across arms.

</details>
