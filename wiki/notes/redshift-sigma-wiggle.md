---
title: Free redshift and velocity dispersion in the DR2 fit
date: 2026-09-06
section: Analyses
tags: [calibration, ceridwen, dr2-quiescent-sample]
job:
figures: [nuisance-posteriors.png, nuisance-degeneracies.png, parameters-fixed-vs-free.png, sfh-fixed-vs-free.png]
---

## Model settings

Run
: Four DR2 galaxies, one arm `zsig` against the production arm `poly3_total`, one RTX 5060 per attempt, `results/redshift-sigma-wiggle/`.

Arm
: `zsig` is `poly3_total` plus two nuisance parameters. Everything else is the production setting: Chebyshev order 3, cosmos_total photometry, 7 SFH bins, BlackJAX NSS.

Free redshift
: `zred` with prior Normal(z_cat, sigma_z), sigma_z = 100 km/s / c times (1 + z_cat). The Spectrum keeps the projection baked at z_cat and stretches the observed grid at each call. The stretch commutes with every smoothing kernel, so the only error is linear interpolation between 0.6 A pixels.

Free velocity dispersion
: `sigma_smooth` with prior Normal(sigma_cat, 0.2 sigma_cat), bounds 0.5 sigma_cat to 1.5 sigma_cat. sigma_cat is the DR2 stellar velocity dispersion.

Code
: `Spectrum(free_z=True)` and `predict(..., zred=z)` on the fork branch `free-z-spectrum` (354f5e9), not yet merged into the pinned ceridwen submodule. Switches `CERIDWEN_FREE_ZRED_KMS` (100) and `CERIDWEN_FREE_SIGMA_FRAC` (0.2) in `notebooks/ceridwen_integrated_photometry_spectra.ipynb`.

```
Delta v = c (z - z_cat) / (1 + z_cat)
sigma_pull = (sigma_smooth - sigma_cat) / sigma_cat_err
```

<figure>
<img src="figures/redshift-sigma-wiggle/nuisance-posteriors.png" alt="Posterior of Delta v and sigma_smooth for the four galaxies, with the DR2 value, the CPU redshift scan and the prior bounds">
<figcaption>Delta v and sigma_smooth posteriors against the DR2 sigma_cat (dashed), the CPU redshift scan (dotted) and the prior bounds (shaded), with M5_173928 railed at 1.5 sigma_cat</figcaption>
</figure>

<figure>
<img src="figures/redshift-sigma-wiggle/nuisance-degeneracies.png" alt="Corner of Delta v, sigma_smooth, log Z, afe and t_MW for the four galaxies">
<figcaption>sigma_smooth against Delta v, log Z, [alpha/Fe] and t_MW, with |r| at most 0.09 except log Z at +0.21 (M12_185653) and +0.32 (M5_172669)</figcaption>
</figure>

<figure>
<img src="figures/redshift-sigma-wiggle/parameters-fixed-vs-free.png" alt="log M, t50, age, tau_dust, log Z, afe for poly3_total and zsig, four galaxies">
<figcaption>Physical parameters with fixed against free nuisances, where only tau_dust on M5_173928 moves by more than one sigma</figcaption>
</figure>

<figure>
<img src="figures/redshift-sigma-wiggle/sfh-fixed-vs-free.png" alt="Star-formation history, poly3_total and zsig, four galaxies">
<figcaption>SFH bands with fixed against free nuisances</figcaption>
</figure>

<details>
<summary>Details</summary>

Every delta is `zsig` minus `poly3_total` of the same galaxy and seed. Raw chi2 is the spectral chi2 with the pixel errors alone, comparable across arms. Stored chi2 uses each fit's own f_calib.

| galaxy | S/N | Delta v [km/s] | CPU scan | sigma_smooth [km/s] | DR2 sigma_cat | pull | Delta raw chi2 | Delta stored chi2 | Delta phot chi2 | Delta ln Z |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| M5_173928 | 13 | +7.8 ± 9.4 | 0 | 267.8 ± 1.8 | 179.7 ± 13.3 | +6.6, at 1.5 sigma_cat | -535 | -3.1 | -11.8 | +73.3 |
| M12_185653 | 22 | +12.3 ± 6.0 | 0 | 144.2 ± 5.4 | 173.8 ± 10.2 | -2.9 | -66 | -19.6 | -0.4 | +7.4 |
| M1_206545 | 31 | -19.6 ± 4.4 | -21 | 241.3 ± 4.9 | 210.0 ± 8.0 | +3.9 | -71 | -32.8 | -10.5 | +32.7 |
| M5_172669 | 105 | +18.3 ± 3.2 | +52 | 231.5 ± 3.9 | 223.8 ± 6.1 | +1.3 | -66 | +39.4 | +1.1 | +4.4 |

| galaxy | Delta log M | Delta t50 [Gyr] | Delta age [Gyr] | Delta tau_dust | Delta f_calib | wall zsig [s] | wall poly3_total [s] |
| --- | --- | --- | --- | --- | --- | --- | --- |
| M5_173928 | -0.006 | -0.003 | +0.001 | -0.070 | -0.29 | 1411 | 354 |
| M12_185653 | +0.027 | +0.16 | +0.18 | +0.038 | -0.01 | 1144 | 306 |
| M1_206545 | -0.004 | -0.004 | -0.001 | -0.024 | -0.03 | 1349 | 371 |
| M5_172669 | +0.000 | -0.023 | -0.048 | -0.006 | -0.02 | 1511 | 404 |

Run: Vast.ai RTX 5060, instance 50009451 ($0.14, one cell, destroyed after a runner fault) then instance 50012613 ($0.15, three cells, destroyed). Records in `results/redshift-sigma-wiggle/vast_run_*.json`, tables `zsig-vs-poly3_total.csv` and `delta-vs-poly3_total.csv`, executed notebook `analysis.ipynb`.

```
CERIDWEN_ARMS_RESULTS=results/redshift-sigma-wiggle ceridwen/.venv/bin/python scripts/calibration_arms_vast.py run --arms zsig --targets M12_185653 M1_206545 M5_172669 M5_173928 --no-mocks --ceridwen-tree <ceridwen-freez> --spend-cap 1.50
JAX_PLATFORMS=cpu ceridwen/.venv/bin/python -m pytest <ceridwen-freez>/tests/test_spectrum_free_z.py -q
```

</details>
