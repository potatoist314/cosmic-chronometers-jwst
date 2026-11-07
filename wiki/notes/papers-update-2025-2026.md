---
title: Papers: 2025–2026 update
date: 2026-11-07
section: Paper drafts
theme: Background reading
tags: [papers, literature, legac, jwst, sed-fitting, alpha-enhancement, cosmic-chronometers]
job: t_73af2ef9
---

Source: arXiv abstracts, read 2026-11-07. Earlier: `notes/papers-spectral-fitting.md`, `notes/external-comparison-samples.md`.

## Fitting codes and stellar models

<details>
<summary>Stoffers+2026 - CERIDWEN</summary>

- GPU-native JAX SED fitting with nested sampling that updates live points in parallel.
- Non-parametric SFHs use ~120 age bins and time-dependent chemical-enrichment histories.
- Samples stellar \([\alpha/\mathrm{Fe}]\) jointly with \([\mathrm{Fe}/\mathrm{H}]\), mass and SFH.
- Median sampling ~4 min, ~134× faster than equivalent CPU Prospector fits.
- [arXiv:2609.30145](https://arxiv.org/abs/2609.30145)

</details>

<details>
<summary>Zacharegkas+2025 - GPU Bayesian posteriors</summary>

- JAX accelerates galaxy photometry predictions and Bayesian SPS inference on GPUs.
- Approximate photometry calculations run faster by a factor of 50.
- SFH models include short-timescale burstiness with negligible additional computation.
- Parallel HMC produces approximately 1000 galaxy posteriors per minute on a single GPU.
- [arXiv:2506.19919](https://arxiv.org/abs/2506.19919) · Open J. Astrophys. 8 (2025)

</details>

<details>
<summary>Martín-Navarro+2026 - FASTAR</summary>

- FASTAR: differentiable SPS, benchmarked on globular clusters and early-type galaxy spectra.
- Models span ages between 20 Myr and 14 Gyr.
- Metallicity coverage spans \(-2.5<[\mathrm{M}/\mathrm{H}]<+0.3\).
- Detailed spectroscopic predictions cover \(3540\text{–}7400\ \text{\AA}\).
- [arXiv:2605.24093](https://arxiv.org/abs/2605.24093)

</details>

<details>
<summary>Dotter+2026 - MIST II, alpha-enhanced</summary>

- MIST models stellar evolution with self-consistent \([\alpha/\mathrm{Fe}]\) variations.
- Models include \([\alpha/\mathrm{Fe}]=-0.2, 0, +0.2, +0.4, +0.6\).
- Iron abundances span \(-3\leq[\mathrm{Fe}/\mathrm{H}]\leq+0.5\).
- Abundance variations extend from stellar interiors to synthetic spectra.
- [arXiv:2602.22012](https://arxiv.org/abs/2602.22012)

</details>

<details>
<summary>Annunziatella+2025 - SFH modelling choices</summary>

- BAGPIPES and Synthesizer spectro-photometric fits of massive galaxies at \(1<z<4.5\).
- Galaxies form 50% of their mass between \(3\leq z\leq9\).
- Non-parametric SFHs imply earlier, slower mass assembly than parametric forms.
- QGs have average mass-weighted ages \(t_M\sim1.1\ \mathrm{Gyr}\).
- [arXiv:2508.16951](https://arxiv.org/abs/2508.16951) · A&A 702, A224 (2025)

</details>

<details>
<summary>Lapasia+2026 - SFH prior and dust</summary>

- Prospector fits three optically dark galaxies with earlier redshift estimates consistent with \(z>5\).
- S1 has \(z_{\mathrm{spec}}=3.2439\pm0.0002\).
- Rising SFH priors yield lower stellar masses than constant SFH priors.
- Dust attenuation slope, attenuation amount, and stellar mass show significant degeneracy.
- [arXiv:2601.08693](https://arxiv.org/abs/2601.08693)

</details>

<details>
<summary>Mattolini+2025 - Local scaling relations</summary>

- Bayesian spectral-index and photometry fits of SDSS DR7 galaxies at \(0.005<z<0.22\).
- Light-weighted age measurements cover 354,977 galaxies (SNR>10).
- Metallicity measurements cover 89,852 galaxies (SNR>20).
- The mass-metallicity relation shifts upwards by 0.2 dex relative to previous works.
- [arXiv:2509.04570](https://arxiv.org/abs/2509.04570) · A&A 703, A5 (2025)

</details>

<details>
<summary>Hamadouche+2026 - Spectral feature atlas</summary>

- A lookup table compiles rest-frame optical-to-NIR spectral features of QGs.
- Feature origins include stellar photospheres and the interstellar medium.
- Diagnostics cover age, metallicity, surface gravity, \([\alpha/\mathrm{Fe}]\), electron temperature, and gas density.
- [arXiv:2603.13479](https://arxiv.org/abs/2603.13479)

</details>

## LEGA-C and z~0.7 quiescent galaxies

<details>
<summary>Nersesian+2025 - Quenching channels</summary>

- Prospector fits spectra and photometry of 2908 LEGA-C galaxies at \(0.6<z<1.0\).
- Main-population QGs quench over \(\tau_q=1.23\pm0.04\ \mathrm{Gyr}\).
- Compact post-starburst galaxies quench over \(\tau_q=0.13\pm0.03\ \mathrm{Gyr}\).
- At fixed stellar mass, smaller QGs quench faster than larger QGs.
- [arXiv:2512.10383](https://arxiv.org/abs/2512.10383) · A&A 705, A153 (2026)

</details>

<details>
<summary>Ditrani+2025 - COSMOS Wall environments</summary>

- Full-index and photometry fitting of 74 massive COSMOS Wall QGs at \(z\sim0.73\).
- Group galaxies are > 1 Gyr older than field galaxies.
- Stellar metallicities show no significant difference between X-ray and non-X-ray groups.
- Field galaxies have 0.15 dex higher metallicities.
- [arXiv:2503.19974](https://arxiv.org/abs/2503.19974)

</details>

<details>
<summary>Ditrani+2026 - Massive passive evolution</summary>

- Spectral-index fitting of massive BOSS and DESI LRGs at \(0.15<z<0.8\).
- Light-weighted ages follow passive evolution.
- \([\mathrm{Fe}/\mathrm{H}]\) remains flat towards lower redshift.
- \([\alpha/\mathrm{Fe}]\) remains flat towards lower redshift.
- [arXiv:2601.09789](https://arxiv.org/abs/2601.09789) · MNRAS (2026)

</details>

<details>
<summary>Cheng+2026 - Bottom-heavy IMFs</summary>

- Full-spectrum models fit nine massive QGs at \(z\approx0.7\) using JWST and LEGA-C spectra.
- The most massive galaxies show excess low-mass stars.
- The oldest galaxy has the most bottom-heavy IMF.
- The oldest galaxy has formation redshift \(z_{\mathrm{form}}>5\).
- [arXiv:2601.20864](https://arxiv.org/abs/2601.20864) · Nat. Astron. (2026)

</details>

<details>
<summary>Beverage+2026 - Empirical elemental yields</summary>

- Milky Way abundance trends model QGs at \(z\sim0\), \(z\sim0.7\), and \(z\sim2\).
- Empirical yields give a median offset of ~0.05 dex across 14 elements.
- Theoretical yields give a median offset of ~0.23 dex.
- Largest discrepancies involve N, Sr, Ba, and C at \(z\sim2\).
- [arXiv:2605.03000](https://arxiv.org/abs/2605.03000)

</details>

## JWST quiescent galaxies at z>1

<details>
<summary>Lu+2026 - TP-AGB spectral contributions</summary>

- Three SPS models fit 27 JWST/NIRSpec PRISM spectra of QGs at \(z>1\).
- Only M13 gives consistent ages across optical, NIR, and full-spectrum fits.
- M13 gives mass-weighted ages younger by <500 Myr than BC03 and C09.
- M13 gives stellar masses lower by <0.2 dex than BC03 and C09.
- [arXiv:2604.19942](https://arxiv.org/abs/2604.19942)

</details>

<details>
<summary>Beverage+2024 - Carbon and iron</summary>

- Ultradeep JWST-SUSPENSE spectra provide elemental abundances for 15 massive QGs at \(z=1\text{–}3\).
- \([\mathrm{C}/\mathrm{H}]\) is lower by \(0.26\pm0.04\) dex than in QGs at \(z\sim0\).
- \([\mathrm{Fe}/\mathrm{H}]\) is lower by \(0.16\pm0.03\) dex than in QGs at \(z\sim0\).
- \([\mathrm{Mg}/\mathrm{H}]\) is lower by \(0.07\pm0.04\) dex than in QGs at \(z\sim0\).
- [arXiv:2407.02556](https://arxiv.org/abs/2407.02556)

</details>

<details>
<summary>Cheng+2025 - Stellar population gradients</summary>

- Full-spectrum models fit eight massive JWST-SUSPENSE QGs at \(1.2\lesssim z\lesssim2.2\).
- Age gradients are negative.
- \([\mathrm{Fe}/\mathrm{H}]\) gradients are flat.
- \([\mathrm{Mg}/\mathrm{H}]\) and \([\mathrm{Mg}/\mathrm{Fe}]\) gradients show tentative positive trends.
- [arXiv:2509.12316](https://arxiv.org/abs/2509.12316) · A&A 710, A158 (2026)

</details>

<details>
<summary>Hamadouche+2026 - DeepDive quenching pathways</summary>

- Spectro-photometric fitting of ten massive DeepDive QGs at \(3<z<4\).
- Most galaxies form 50% of their stellar mass by \(z\sim5\).
- Most galaxies quench by \(z\sim4\).
- Mean \([\alpha/\mathrm{Fe}]\) is \(0.22^{+0.22}_{-0.17}\).
- [arXiv:2602.02485](https://arxiv.org/abs/2602.02485)

</details>

<details>
<summary>Leung+2026 - EXCELS ages and abundances</summary>

- Full-spectral fitting of 14 EXCELS QGs at \(3<z<5\) using JWST/NIRSpec spectroscopy.
- More massive galaxies assemble their stellar mass earlier.
- The age-mass relation has slope \(\simeq2\ \mathrm{Gyr}\) per dex in stellar mass.
- Chemical abundance estimates disagree across stellar models, wavelength ranges, SFH models, and fitting codes.
- [arXiv:2602.05934](https://arxiv.org/abs/2602.05934) · MNRAS (2026)

</details>

<details>
<summary>Edward+2026 - MAGAZ3NE resolved abundances</summary>

- JWST/NIRSpec IFU spectroscopy of three ultra-massive QGs at \(z\sim3.5\).
- Central regions have ages \(\approx0.6\text{–}0.7\ \mathrm{Gyr}\).
- Central regions have \([\alpha/\mathrm{Fe}]\approx0.2\text{–}0.5\).
- Two galaxies show positive age gradients.
- [arXiv:2605.27555](https://arxiv.org/abs/2605.27555)

</details>

<details>
<summary>O'Connor+2026 - Chemical formation timescales</summary>

- One-zone chemical evolution modelling of compiled abundances of massive QGs at \(z\sim2\).
- Formation timescales span \(\Delta t_{\mathrm{SF}}\sim0.1\text{–}0.4\ \mathrm{Gyr}\).
- Progenitors sustain \(\tau_\star\sim0.05\ \mathrm{Gyr}\) and retain most enriched ejecta (\(\eta\sim0\)).
- Models favour progenitor SFRs of \(200\text{–}400\ M_\odot\,\mathrm{yr^{-1}}\).
- [arXiv:2610.34883](https://arxiv.org/abs/2610.34883)

</details>

<details>
<summary>Zhang+2026 - Reconstructed number densities</summary>

- Prospector fits RUBIES QGs at \(2<z<5\) using JWST spectra and photometry.
- The sample has \(M_\star>10^{10.5}\,M_\odot\).
- Reconstructed and observed number densities agree up to \(z\sim7\).
- Observed and predicted number densities remain in tension at \(3<z<7\).
- [arXiv:2604.05024](https://arxiv.org/abs/2604.05024)

</details>

## Cosmic chronometers

<details>
<summary>Álvarez+2026 - DESI DR1 chronometers</summary>

- Stacked-spectrum Lick-index fits of DESI LRGs at \(0.3<z<1.2\) as cosmic chronometers.
- Cosmographic fitting constrains \(H(z)\) from age-redshift relations.
- Reddest envelope: \(H(z\approx0.61)=88.5^{+6.7}_{-12.6}\,(\mathrm{stat})\pm8.1\,(\mathrm{syst})\) km/s/Mpc.
- Data products include the \(H(z)\) covariance matrix.
- [arXiv:2608.13178](https://arxiv.org/abs/2608.13178)

</details>

<details>
<summary>Loubser+2025 - DESI expansion measurements</summary>

- \(D4000_n\) chronometry uses 360 000 passive DESI galaxies at \(0.3<z<1.0\).
- \(H(z=0.46)=88.48\pm0.57\,(\mathrm{stat})\pm12.32\,(\mathrm{syst})\ \mathrm{km\,s^{-1}\,Mpc^{-1}}\).
- \(H(z=0.67)=119.45\pm6.39\,(\mathrm{stat})\pm16.64\,(\mathrm{syst})\ \mathrm{km\,s^{-1}\,Mpc^{-1}}\).
- \(H(z=0.83)=108.28\pm10.07\,(\mathrm{stat})\pm15.08\,(\mathrm{syst})\ \mathrm{km\,s^{-1}\,Mpc^{-1}}\).
- [arXiv:2511.02730](https://arxiv.org/abs/2511.02730)

</details>

<details>
<summary>Lisiecki+2026 - Relic galaxy chronometers</summary>

- \(D_n4000\) and MILES models analyse 189 E-INSPIRE relic galaxies at \(0.07<z<0.22\).
- The measurement gives \(H(z=0.15)=85\pm53\ \mathrm{km\,s^{-1}\,Mpc^{-1}}\).
- Statistical limitations dominate the total uncertainty.
- Systematic uncertainty is 13%, or 8.7% without propagating alpha-enrichment.
- [arXiv:2608.10163](https://arxiv.org/abs/2608.10163)

</details>
