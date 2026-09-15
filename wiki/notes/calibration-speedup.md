---
title: Calibration polynomial speed-up
date: 2026-09-15
section: Analyses
theme: Compute
tags: [calibration, ceridwen, compute]
job:
figures: [timing-by-order.png, fit-M12_98104.png, sfh-M12_98104.png, corner-M12_98104.png]
---

## Change

Code
: `ceridwen/ceridwen/likelihood/calibration.py`, ceridwen commit 56505a6. `PolynomialCalibration._gram`, `normal_matrix`, `calibrate`.

Old arithmetic
: Gram matrix \(N = D^\mathsf{T} D + \Sigma_p^{-1}\) formed from an \((n_{\mathrm{pix}}, k, k)\) product summed over pixels per particle. An LU solve gives \(\hat a\); a separate slogdet uses the same matrix. Cost quadratic in order \(k\).

New arithmetic
: Chebyshev moments \(M_j = \sum_i w_i T_j(x_i)\), \(j = 0 \ldots 2k\), from one \((n_{\mathrm{pix}}) \cdot (n_{\mathrm{pix}}, 2k+1)\) matvec per particle. \(T_m T_n = \tfrac12 (T_{m+n} + T_{|m-n|})\) gives \(N_{mn} = \tfrac12 (M_{m+n} + M_{|m-n|}) + \Sigma_{p,mn}^{-1}\). One Cholesky factor gives \(\hat a\) and \(\ln|N| = 2 \sum \log \operatorname{diag} L\). Cost linear in \(k\). Tests compare the Gram matrix and its gradient with explicit \(D^\mathsf{T} D + \Sigma_p^{-1}\) at orders 1, 3, 7, 10 and 24 to \(10^{-10}\). `calibrate` agrees with an explicit solve and slogdet at orders 10 and 24 to \(10^{-9}\).

## Timing

Setup
: One RTX 5060, jax 0.10.2, joint M1_210210 likelihood (3523 spectral pixels). `jax.jit(jax.vmap(loglike))` over 100 or 500 particles; median of 20 timed calls after one compile. Old and new arithmetic share one process and boot. `scripts/benchmark_calibration_order.py`, `results/calibration-speedup/timing-gpu.json`.

| order | old, 100 | new, 100 | ratio | old, 500 | new, 500 | ratio |
| --- | --- | --- | --- | --- | --- | --- |
| 0 | | 12.5 | | | 5.9 | |
| 3 | 16.7 | 16.4 | 1.02 | 8.4 | 7.6 | 1.11 |
| 5 | 18.5 | 16.7 | 1.10 | 10.5 | 7.7 | 1.36 |
| 10 | 35.9 | 17.1 | 2.10 | 19.5 | 8.3 | 2.35 |
| 24 | 131.4 | 21.4 | 6.14 | 76.2 | 9.9 | 7.66 |

Microseconds per likelihood call. Summed log-likelihoods agree to every printed digit.

<figure>
<img src="figures/calibration-speedup/timing-by-order.png" alt="Microseconds per likelihood call against calibration order for the old and new arithmetic at 100 and 500 particles">
<figcaption>Cost per likelihood call against order, old and new arithmetic.</figcaption>
</figure>

## Refit

Run
: M12_98104, Chebyshev order 10, `new_default` settings, seed 20261007, BlackJAX NSS (num_live 500, num_inner_steps 65, num_delete 100). New fit: `results/calibration-speedup/poly10/98104-M12_98104/`. Old fit: `results/calibration-order/poly10/98104-M12_98104/`. Same box and boot (Vast instance 51132758).

| | old code | new code |
| --- | --- | --- |
| \(\ln Z\) | 249687.64 ± 0.27 | 249688.02 ± 0.28 |
| likelihood calls | 5 347 784 | 5 315 506 |
| sampler wall time [s] | 723 | 393 |
| \(\mu\mathrm{s}\) per call | 135 | 74 |
| \(\log_{10} M_\star\) | 11.158 ± 0.041 | 11.157 ± 0.034 |
| \(\tau_{\mathrm{dust}}\) | 0.192 ± 0.009 | 0.192 ± 0.009 |
| \(t_{50}\) [Gyr] | 4.07 ± 0.55 | 4.01 ± 0.46 |
| photometric \(\chi^2\) | 14.5 | 14.4 |

<figure>
<img src="figures/calibration-speedup/fit-M12_98104.png" alt="M12_98104 order-10 spectrum and photometry with the old-code and new-code posterior medians">
<figcaption>M12_98104, order 10: spectrum and photometry, old and new code medians.</figcaption>
</figure>

<figure>
<img src="figures/calibration-speedup/sfh-M12_98104.png" alt="M12_98104 order-10 star formation history and cumulative mass fraction, old and new code">
<figcaption>Star-formation history and cumulative mass fraction.</figcaption>
</figure>

<figure>
<img src="figures/calibration-speedup/corner-M12_98104.png" alt="M12_98104 order-10 posterior corner plot, old and new code">
<figcaption>Posterior corner plot, old and new code.</figcaption>
</figure>

<details>
<summary>Caveats</summary>

The benchmark's cost per call (17 \(\mu\mathrm{s}\) at order 10) is below the sampler's cost per logical call (74 \(\mu\mathrm{s}\)): the sampler adds proposals, bookkeeping and host transfers, so only the old/new ratio transfers. The refit is one target and one seed.

</details>
