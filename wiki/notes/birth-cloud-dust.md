---
title: M1_210210 with birth-cloud dust and with the dust index down to -3
date: 2026-09-24
section: Analyses
theme: Single-fit accuracy
tags: [ceridwen, dust, birth-cloud, reference-galaxy]
job:
figures: [spectrum-dust1_off-M1_210210.png, photometry-dust1_off-M1_210210.png, spectrum-dust1_on-M1_210210.png, photometry-dust1_on-M1_210210.png, spectrum-dust_index_m3-M1_210210.png, photometry-dust_index_m3-M1_210210.png, corner-M1_210210.png, sfh-M1_210210.png]
---

<figure>
<img src="figures/birth-cloud-dust/spectrum-dust1_off-M1_210210.png" alt="LEGA-C spectrum and pull for M1_210210, dust1_off">
<figcaption><code>spectrum-dust1_off-M1_210210.png</code> · Birth-cloud dust off (current defaults): LEGA-C M1_210210 spectrum over fitted pixels; joint Ceridwen posterior median and \(16\text{–}84\%\) band; lower-panel pull at fitted noise floor; shaded fitted-filter wavelength ranges.</figcaption>
</figure>

<figure>
<img src="figures/birth-cloud-dust/photometry-dust1_off-M1_210210.png" alt="COSMOS2025 photometry and per-band pulls for M1_210210, dust1_off">
<figcaption><code>photometry-dust1_off-M1_210210.png</code> · Birth-cloud dust off (current defaults): M1_210210 observed COSMOS2025 total band fluxes \(\pm\) fitted uncertainties; joint Ceridwen per-band posterior medians (\(16\text{–}84\%\)); median model continuum; LEGA-C spectral range; band-name rail; lower-panel per-band pulls.</figcaption>
</figure>

<figure>
<img src="figures/birth-cloud-dust/spectrum-dust1_on-M1_210210.png" alt="LEGA-C spectrum and pull for M1_210210, dust1_on">
<figcaption><code>spectrum-dust1_on-M1_210210.png</code> · Birth-cloud dust on: LEGA-C M1_210210 spectrum over fitted pixels; joint Ceridwen posterior median and \(16\text{–}84\%\) band; lower-panel pull at fitted noise floor; shaded fitted-filter wavelength ranges.</figcaption>
</figure>

<figure>
<img src="figures/birth-cloud-dust/photometry-dust1_on-M1_210210.png" alt="COSMOS2025 photometry and per-band pulls for M1_210210, dust1_on">
<figcaption><code>photometry-dust1_on-M1_210210.png</code> · Birth-cloud dust on: M1_210210 observed COSMOS2025 total band fluxes \(\pm\) fitted uncertainties; joint Ceridwen per-band posterior medians (\(16\text{–}84\%\)); median model continuum; LEGA-C spectral range; band-name rail; lower-panel per-band pulls.</figcaption>
</figure>

<figure>
<img src="figures/birth-cloud-dust/spectrum-dust_index_m3-M1_210210.png" alt="LEGA-C spectrum and pull for M1_210210, dust_index_m3">
<figcaption><code>spectrum-dust_index_m3-M1_210210.png</code> · Dust-index prior \(\mathrm{Uniform}(-3, 0.4)\): LEGA-C M1_210210 spectrum over fitted pixels; joint Ceridwen posterior median and \(16\text{–}84\%\) band; lower-panel pull at fitted noise floor; shaded fitted-filter wavelength ranges.</figcaption>
</figure>

<figure>
<img src="figures/birth-cloud-dust/photometry-dust_index_m3-M1_210210.png" alt="COSMOS2025 photometry and per-band pulls for M1_210210, dust_index_m3">
<figcaption><code>photometry-dust_index_m3-M1_210210.png</code> · Dust-index prior \(\mathrm{Uniform}(-3, 0.4)\): M1_210210 observed COSMOS2025 total band fluxes \(\pm\) fitted uncertainties; joint Ceridwen per-band posterior medians (\(16\text{–}84\%\)); median model continuum; LEGA-C spectral range; band-name rail; lower-panel per-band pulls.</figcaption>
</figure>

<figure>
<img src="figures/birth-cloud-dust/corner-M1_210210.png" alt="Physical-parameter posteriors for the three fits of M1_210210">
<figcaption><code>corner-M1_210210.png</code> · Physical-parameter posteriors for the birth-cloud dust off, birth-cloud dust on and extended dust-index prior fits of M1_210210.</figcaption>
</figure>

<figure>
<img src="figures/birth-cloud-dust/sfh-M1_210210.png" alt="Star-formation history and cumulative mass fraction for the three fits of M1_210210">
<figcaption><code>sfh-M1_210210.png</code> · Star-formation history with \(16\text{–}84\%\) band and cumulative mass fraction for the three fits of M1_210210.</figcaption>
</figure>

<details>
<summary>Fits</summary>

Target
: M1_210210, \(z=0.6542\), seed 20260832

Arms
: `dust1_off`: birth-cloud dust off (current defaults) · `results/birth-cloud-dust/dust1_off/210210-M1_210210`
: `dust1_on`: birth-cloud dust on, power law with \(\tau_{\mathrm{bc}}=r_{\mathrm{dust}}\tau_{\mathrm{dust}}\), index \(-1\), ages \(\leq 10\,\mathrm{Myr}\) · `results/birth-cloud-dust/dust1_on/210210-M1_210210`
: `dust_index_m3`: dust-index prior \(\mathrm{Uniform}(-3, 0.4)\) · `results/birth-cloud-dust/dust_index_m3/210210-M1_210210`

Common
: BlackJAX NSS: `num_live=500`, `num_inner_steps=65`, `num_delete=100`. Order-10 calibration with fitted constant. 3523 spectral pixels and 28 COSMOS2025 bands. `dust1_off` ran on one RTX 5060 Ti; `dust1_on` and `dust_index_m3` ran on one on-demand RTX 5090.

Evaluation
: `results/birth-cloud-dust/analysis.ipynb`

Record
: experiment `e-birth-cloud-dust`

</details>

<details open>
<summary>Parameters</summary>

| Quantity | off | on | m3 |
| --- | --- | --- | --- |
| Birth-cloud dust | off | on | off |
| Dust-index prior | \(\mathrm{Uniform}(-1, 0.4)\) | \(\mathrm{Uniform}(-1, 0.4)\) | \(\mathrm{Uniform}(-3, 0.4)\) |
| \(\ln Z\) | \(231432.39 \pm 0.22\) | \(231446.95 \pm 0.24\) | \(231501.86 \pm 0.40\) |
| Photometric \(\chi^2\) | \(146.8\) | \(118.2\) | \(48.0\) |
| Spectral \(\chi^2\), catalogue uncertainties | \(10855.5\) | \(10840.9\) | \(10725.3\) |
| Spectral \(\chi^2\) at the off fit’s floor | \(3357.2\) | \(3353.0\) | \(3321.8\) |
| \(u^*\) pull | \(-7.38\) | \(-6.31\) | \(+0.06\) |
| \(\log_{10}(M_\star/M_\odot)\) | \(11.587 \pm 0.011\) | \(11.585 \pm 0.010\) | \(11.538 \pm 0.012\) |
| \([\mathrm{Fe}/\mathrm{H}]\) | \(-0.181 \pm 0.021\) | \(-0.184 \pm 0.020\) | \(-0.117 \pm 0.023\) |
| \([\alpha/\mathrm{Fe}]\) | \(+0.050 \pm 0.010\) | \(+0.054 \pm 0.011\) | \(+0.069 \pm 0.009\) |
| \(\tau_{\mathrm{dust}}\) | \(0.353 \pm 0.011\) | \(0.332 \pm 0.011\) | \(0.141 \pm 0.016\) |
| \(\delta_{\mathrm{dust}}\) | \(-0.994 \pm 0.007\) | \(-0.992 \pm 0.009\) | \(-2.361 \pm 0.151\) |
| \(r_{\mathrm{dust}}\) | — | \(1.375 \pm 0.221\) | — |
| \(t_{\mathrm{MW}}\) [Gyr] | \(5.07 \pm 0.12\) | \(5.14 \pm 0.12\) | \(5.14 \pm 0.13\) |
| \(t_{20}\) [Gyr] | \(3.64 \pm 0.11\) | \(3.72 \pm 0.12\) | \(3.72 \pm 0.13\) |
| \(t_{50}\) [Gyr] | \(5.17 \pm 0.21\) | \(5.25 \pm 0.20\) | \(5.27 \pm 0.21\) |
| \(t_{80}\) [Gyr] | \(6.61 \pm 0.08\) | \(6.64 \pm 0.08\) | \(6.65 \pm 0.08\) |
| \(f_{\mathrm{calib}}\) [%] | \(2.73 \pm 0.06\) | \(2.69 \pm 0.06\) | \(2.46 \pm 0.06\) |
| \(z\) | \(0.654218 \pm 0.000016\) | \(0.654219 \pm 0.000015\) | \(0.654223 \pm 0.000015\) |
| \(\sigma_\star\) [km/s] | \(267.3 \pm 3.1\) | \(266.5 \pm 3.0\) | \(262.5 \pm 2.9\) |
| ESS | \(4560\) | \(4930\) | \(4267\) |
| Likelihood calls | \(8424501\) | \(8709803\) | \(8257747\) |
| Sampler wall time [s] | \(914.9\) | \(3373.4\) | \(274.6\) |
| Vast instance, spend | 52299165, $0.3244 shared run | 52400715, $0.9962 shared run | 52400715, $0.9962 shared run |

</details>

<details>
<summary>Caveats</summary>

- All three arms fit identical data arrays under identical likelihood conventions, so \(\ln Z\) differences are Bayes factors between the model-plus-prior choices; prior volumes differ (extra \(r_{\mathrm{dust}}\); wider index prior in m3).
- In off and on, the \(\delta_{\mathrm{dust}}\) posterior median sits at the prior edge \(-1\). In m3 it is \(-2.36\), inside the \(\mathrm{Uniform}(-3, 0.4)\) prior.
- `dust1_on` failed remotely on the stale 6-group validator count, then recovered locally. See experiment `e-birth-cloud-dust`.
- The box used branch defaults: 28 COSMOS2025 bands.
- One galaxy.

</details>
