---
title: Per-galaxy fit diagnostics, gallery
date: 2026-09-05
section: Analyses
tags: [dr2-quiescent-sample, ceridwen, diagnostics]
job: t_8a78968d
---

187 galaxies. Method and checks: [Per-galaxy fit diagnostics](../per-galaxy-fit-diagnostics/).

## Model settings

Stellar grid
: C3K v2.3 high-res (c3k_hr, vt=10 km/s), MIST v2.5 (aMIST, alpha-variable) isochrones, Kroupa (2001) IMF. Axes [alpha/Fe] -0.2, 0, 0.2, 0.4, 0.6, log10 Z 13 nodes, log10(age/Gyr) 107 nodes.

Star-formation history
: Constant star-formation rate in each of 7 lookback bins. Edges 0, 0.03, 0.1, 0.3, 1, 3, 5 Gyr, then the universe age at the galaxy redshift. Metallicity constant in time.

Free parameters and priors
: 13 free values. Z Uniform(-4.233, -1.233). afe Uniform(-0.2, 0.6). diffuse_tau_kc Uniform(0, 2). log_f_calib Uniform(-4.605, -2.303). logmass Uniform(8, 13). logsfr_ratios Uniform(-3, 3), 7 values. spectrum_scaling ClippedNormal(mean=1, sigma=0.3, low=0.2, high=3).

Fixed
: Redshift at each galaxy's catalogue value, 0.603 to 0.987 across the sample. Dust index of the attenuation curve at -0.7. Stellar velocity dispersion at the catalogue value.

Dust, nebular emission and IGM
: kriek_conroy attenuation on the diffuse component. Birth-cloud dust false. Dust emission false. Nebular emission none. IGM absorption none.

Spectrum calibration
: No polynomial, order 0. A free fractional noise floor f_calib between 1 and 10 percent of the model flux. A free multiplicative scale spectrum_scaling.

Photometry anchor
: cosmos_ap3, the 12 COSMOS2015 3 arcsecond aperture fluxes with total IRAC and no offsets. The model photometry never carries the spectrum scale or a calibration polynomial.

## Galaxies

101089-M12_101089
: z 0.8510 · S/N 8.3

<figure>
<img loading="lazy" src="/wiki/f/results/rtx-5060-dr2-quiescent-full-spectrum/101089-M12_101089/diagnostics/photometric_chi2.png" alt="M12_101089: photometric pull and chi-squared contribution per band">
<figcaption>Pull of only the 12 fitted bands of galaxy M12_101089 against the model, 1.48 per band at a 5 percent flux error floor.</figcaption>
</figure>

<figure>
<img loading="lazy" src="/wiki/f/results/rtx-5060-dr2-quiescent-full-spectrum/101089-M12_101089/diagnostics/spectral_chi2.png" alt="M12_101089: spectral pull, binned mean pull squared, cumulative chi-squared">
<figcaption>Pull of only 3430 fitted spectrum pixels of galaxy M12_101089 against the model, 2.340 per pixel at a 9.99 percent error floor.</figcaption>
</figure>

<figure>
<img loading="lazy" src="/wiki/f/results/rtx-5060-dr2-quiescent-full-spectrum/101089-M12_101089/diagnostics/sf_timescales.png" alt="M12_101089: cumulative mass formed against lookback time with t10 to t90">
<figcaption>Mass formed in galaxy M12_101089 against lookback time: t10 6.25, t20 6.00, t50 5.24 Gyr, only a 16-84 percent range.</figcaption>
</figure>

101830-M12_101830
: z 0.9874 · S/N 11.3

<figure>
<img loading="lazy" src="/wiki/f/results/rtx-5060-dr2-quiescent-full-spectrum/101830-M12_101830/diagnostics/photometric_chi2.png" alt="M12_101830: photometric pull and chi-squared contribution per band">
<figcaption>Pull of only the 12 fitted bands of galaxy M12_101830 against the model, 6.95 per band at a 5 percent flux error floor.</figcaption>
</figure>

<figure>
<img loading="lazy" src="/wiki/f/results/rtx-5060-dr2-quiescent-full-spectrum/101830-M12_101830/diagnostics/spectral_chi2.png" alt="M12_101830: spectral pull, binned mean pull squared, cumulative chi-squared">
<figcaption>Pull of only 3814 fitted spectrum pixels of galaxy M12_101830 against the model, 1.537 per pixel at a 9.98 percent error floor.</figcaption>
</figure>

<figure>
<img loading="lazy" src="/wiki/f/results/rtx-5060-dr2-quiescent-full-spectrum/101830-M12_101830/diagnostics/sf_timescales.png" alt="M12_101830: cumulative mass formed against lookback time with t10 to t90">
<figcaption>Mass formed in galaxy M12_101830 against lookback time: t10 4.83, t20 4.44, t50 3.22 Gyr, only a 16-84 percent range.</figcaption>
</figure>

102456-M12_102456
: z 0.6779 · S/N 34.9

<figure>
<img loading="lazy" src="/wiki/f/results/rtx-5060-dr2-quiescent-full-spectrum/102456-M12_102456/diagnostics/photometric_chi2.png" alt="M12_102456: photometric pull and chi-squared contribution per band">
<figcaption>Pull of only the 12 fitted bands of galaxy M12_102456 against the model, 14.22 per band at a 5 percent flux error floor.</figcaption>
</figure>

<figure>
<img loading="lazy" src="/wiki/f/results/rtx-5060-dr2-quiescent-full-spectrum/102456-M12_102456/diagnostics/spectral_chi2.png" alt="M12_102456: spectral pull, binned mean pull squared, cumulative chi-squared">
<figcaption>Pull of only 3463 fitted spectrum pixels of galaxy M12_102456 against the model, 1.191 per pixel at a 5.90 percent error floor.</figcaption>
</figure>

<figure>
<img loading="lazy" src="/wiki/f/results/rtx-5060-dr2-quiescent-full-spectrum/102456-M12_102456/diagnostics/sf_timescales.png" alt="M12_102456: cumulative mass formed against lookback time with t10 to t90">
<figcaption>Mass formed in galaxy M12_102456 against lookback time: t10 6.00, t20 4.87, t50 3.61 Gyr, only a 16-84 percent range.</figcaption>
</figure>

102968-M14_102968
: z 0.9393 · S/N 9.5

<figure>
<img loading="lazy" src="/wiki/f/results/rtx-5060-dr2-quiescent-full-spectrum/102968-M14_102968/diagnostics/photometric_chi2.png" alt="M14_102968: photometric pull and chi-squared contribution per band">
<figcaption>Pull of only the 12 fitted bands of galaxy M14_102968 against the model, 12.50 per band at a 5 percent flux error floor.</figcaption>
</figure>

<figure>
<img loading="lazy" src="/wiki/f/results/rtx-5060-dr2-quiescent-full-spectrum/102968-M14_102968/diagnostics/spectral_chi2.png" alt="M14_102968: spectral pull, binned mean pull squared, cumulative chi-squared">
<figcaption>Pull of only 3813 fitted spectrum pixels of galaxy M14_102968 against the model, 1.099 per pixel at a 5.93 percent error floor.</figcaption>
</figure>

<figure>
<img loading="lazy" src="/wiki/f/results/rtx-5060-dr2-quiescent-full-spectrum/102968-M14_102968/diagnostics/sf_timescales.png" alt="M14_102968: cumulative mass formed against lookback time with t10 to t90">
<figcaption>Mass formed in galaxy M14_102968 against lookback time: t10 5.16, t20 4.69, t50 3.56 Gyr, only a 16-84 percent range.</figcaption>
</figure>

103366-M14_103366
: z 0.6742 · S/N 14.3

<figure>
<img loading="lazy" src="/wiki/f/results/rtx-5060-dr2-quiescent-full-spectrum/103366-M14_103366/diagnostics/photometric_chi2.png" alt="M14_103366: photometric pull and chi-squared contribution per band">
<figcaption>Pull of only the 12 fitted bands of galaxy M14_103366 against the model, 2.92 per band at a 5 percent flux error floor.</figcaption>
</figure>

<figure>
<img loading="lazy" src="/wiki/f/results/rtx-5060-dr2-quiescent-full-spectrum/103366-M14_103366/diagnostics/spectral_chi2.png" alt="M14_103366: spectral pull, binned mean pull squared, cumulative chi-squared">
<figcaption>Pull of only 3547 fitted spectrum pixels of galaxy M14_103366 against the model, 1.133 per pixel at a 5.25 percent error floor.</figcaption>
</figure>

<figure>
<img loading="lazy" src="/wiki/f/results/rtx-5060-dr2-quiescent-full-spectrum/103366-M14_103366/diagnostics/sf_timescales.png" alt="M14_103366: cumulative mass formed against lookback time with t10 to t90">
<figcaption>Mass formed in galaxy M14_103366 against lookback time: t10 6.32, t20 5.20, t50 3.43 Gyr, only a 16-84 percent range.</figcaption>
</figure>

104877-M14_104877
: z 0.9544 · S/N 3.6

<figure>
<img loading="lazy" src="/wiki/f/results/rtx-5060-dr2-quiescent-full-spectrum/104877-M14_104877/diagnostics/photometric_chi2.png" alt="M14_104877: photometric pull and chi-squared contribution per band">
<figcaption>Pull of only the 12 fitted bands of galaxy M14_104877 against the model, 7.39 per band at a 5 percent flux error floor.</figcaption>
</figure>

<figure>
<img loading="lazy" src="/wiki/f/results/rtx-5060-dr2-quiescent-full-spectrum/104877-M14_104877/diagnostics/spectral_chi2.png" alt="M14_104877: spectral pull, binned mean pull squared, cumulative chi-squared">
<figcaption>Pull of only 3800 fitted spectrum pixels of galaxy M14_104877 against the model, 1.776 per pixel at a 9.97 percent error floor.</figcaption>
</figure>

<figure>
<img loading="lazy" src="/wiki/f/results/rtx-5060-dr2-quiescent-full-spectrum/104877-M14_104877/diagnostics/sf_timescales.png" alt="M14_104877: cumulative mass formed against lookback time with t10 to t90">
<figcaption>Mass formed in galaxy M14_104877 against lookback time: t10 0.27, t20 0.10, t50 0.05 Gyr, only a 16-84 percent range.</figcaption>
</figure>

105474-M4_105474
: z 0.6732 · S/N 37.3

<figure>
<img loading="lazy" src="/wiki/f/results/rtx-5060-dr2-quiescent-full-spectrum/105474-M4_105474/diagnostics/photometric_chi2.png" alt="M4_105474: photometric pull and chi-squared contribution per band">
<figcaption>Pull of only the 12 fitted bands of galaxy M4_105474 against the model, 13.04 per band at a 5 percent flux error floor.</figcaption>
</figure>

<figure>
<img loading="lazy" src="/wiki/f/results/rtx-5060-dr2-quiescent-full-spectrum/105474-M4_105474/diagnostics/spectral_chi2.png" alt="M4_105474: spectral pull, binned mean pull squared, cumulative chi-squared">
<figcaption>Pull of only 3389 fitted spectrum pixels of galaxy M4_105474 against the model, 1.095 per pixel at a 5.85 percent error floor.</figcaption>
</figure>

<figure>
<img loading="lazy" src="/wiki/f/results/rtx-5060-dr2-quiescent-full-spectrum/105474-M4_105474/diagnostics/sf_timescales.png" alt="M4_105474: cumulative mass formed against lookback time with t10 to t90">
<figcaption>Mass formed in galaxy M4_105474 against lookback time: t10 2.46, t20 1.88, t50 0.80 Gyr, only a 16-84 percent range.</figcaption>
</figure>

107362-M3_107362
: z 0.6767 · S/N 23.7

<figure>
<img loading="lazy" src="/wiki/f/results/rtx-5060-dr2-quiescent-full-spectrum/107362-M3_107362/diagnostics/photometric_chi2.png" alt="M3_107362: photometric pull and chi-squared contribution per band">
<figcaption>Pull of only the 12 fitted bands of galaxy M3_107362 against the model, 13.98 per band at a 5 percent flux error floor.</figcaption>
</figure>

<figure>
<img loading="lazy" src="/wiki/f/results/rtx-5060-dr2-quiescent-full-spectrum/107362-M3_107362/diagnostics/spectral_chi2.png" alt="M3_107362: spectral pull, binned mean pull squared, cumulative chi-squared">
<figcaption>Pull of only 3484 fitted spectrum pixels of galaxy M3_107362 against the model, 1.155 per pixel at a 4.34 percent error floor.</figcaption>
</figure>

<figure>
<img loading="lazy" src="/wiki/f/results/rtx-5060-dr2-quiescent-full-spectrum/107362-M3_107362/diagnostics/sf_timescales.png" alt="M3_107362: cumulative mass formed against lookback time with t10 to t90">
<figcaption>Mass formed in galaxy M3_107362 against lookback time: t10 4.62, t20 4.22, t50 3.00 Gyr, only a 16-84 percent range.</figcaption>
</figure>

107370-M4_107370
: z 0.8436 · S/N 17.8

<figure>
<img loading="lazy" src="/wiki/f/results/rtx-5060-dr2-quiescent-full-spectrum/107370-M4_107370/diagnostics/photometric_chi2.png" alt="M4_107370: photometric pull and chi-squared contribution per band">
<figcaption>Pull of only the 12 fitted bands of galaxy M4_107370 against the model, 4.00 per band at a 5 percent flux error floor.</figcaption>
</figure>

<figure>
<img loading="lazy" src="/wiki/f/results/rtx-5060-dr2-quiescent-full-spectrum/107370-M4_107370/diagnostics/spectral_chi2.png" alt="M4_107370: spectral pull, binned mean pull squared, cumulative chi-squared">
<figcaption>Pull of only 3388 fitted spectrum pixels of galaxy M4_107370 against the model, 1.129 per pixel at a 6.02 percent error floor.</figcaption>
</figure>

<figure>
<img loading="lazy" src="/wiki/f/results/rtx-5060-dr2-quiescent-full-spectrum/107370-M4_107370/diagnostics/sf_timescales.png" alt="M4_107370: cumulative mass formed against lookback time with t10 to t90">
<figcaption>Mass formed in galaxy M4_107370 against lookback time: t10 4.60, t20 4.17, t50 2.91 Gyr, only a 16-84 percent range.</figcaption>
</figure>

107643-M4_107643
: z 0.7343 · S/N 21.0

<figure>
<img loading="lazy" src="/wiki/f/results/rtx-5060-dr2-quiescent-full-spectrum/107643-M4_107643/diagnostics/photometric_chi2.png" alt="M4_107643: photometric pull and chi-squared contribution per band">
<figcaption>Pull of only the 12 fitted bands of galaxy M4_107643 against the model, 1.40 per band at a 5 percent flux error floor.</figcaption>
</figure>

<figure>
<img loading="lazy" src="/wiki/f/results/rtx-5060-dr2-quiescent-full-spectrum/107643-M4_107643/diagnostics/spectral_chi2.png" alt="M4_107643: spectral pull, binned mean pull squared, cumulative chi-squared">
<figcaption>Pull of only 3496 fitted spectrum pixels of galaxy M4_107643 against the model, 1.098 per pixel at a 6.39 percent error floor.</figcaption>
</figure>

<figure>
<img loading="lazy" src="/wiki/f/results/rtx-5060-dr2-quiescent-full-spectrum/107643-M4_107643/diagnostics/sf_timescales.png" alt="M4_107643: cumulative mass formed against lookback time with t10 to t90">
<figcaption>Mass formed in galaxy M4_107643 against lookback time: t10 4.60, t20 4.18, t50 2.90 Gyr, only a 16-84 percent range.</figcaption>
</figure>

108989-M4_108989
: z 0.8278 · S/N 21.3

<figure>
<img loading="lazy" src="/wiki/f/results/rtx-5060-dr2-quiescent-full-spectrum/108989-M4_108989/diagnostics/photometric_chi2.png" alt="M4_108989: photometric pull and chi-squared contribution per band">
<figcaption>Pull of only the 12 fitted bands of galaxy M4_108989 against the model, 11.28 per band at a 5 percent flux error floor.</figcaption>
</figure>

<figure>
<img loading="lazy" src="/wiki/f/results/rtx-5060-dr2-quiescent-full-spectrum/108989-M4_108989/diagnostics/spectral_chi2.png" alt="M4_108989: spectral pull, binned mean pull squared, cumulative chi-squared">
<figcaption>Pull of only 3735 fitted spectrum pixels of galaxy M4_108989 against the model, 1.196 per pixel at a 4.64 percent error floor.</figcaption>
</figure>

<figure>
<img loading="lazy" src="/wiki/f/results/rtx-5060-dr2-quiescent-full-spectrum/108989-M4_108989/diagnostics/sf_timescales.png" alt="M4_108989: cumulative mass formed against lookback time with t10 to t90">
<figcaption>Mass formed in galaxy M4_108989 against lookback time: t10 6.24, t20 5.86, t50 4.72 Gyr, only a 16-84 percent range.</figcaption>
</figure>

109352-M3_109352
: z 0.7244 · S/N 23.9

<figure>
<img loading="lazy" src="/wiki/f/results/rtx-5060-dr2-quiescent-full-spectrum/109352-M3_109352/diagnostics/photometric_chi2.png" alt="M3_109352: photometric pull and chi-squared contribution per band">
<figcaption>Pull of only the 12 fitted bands of galaxy M3_109352 against the model, 11.39 per band at a 5 percent flux error floor.</figcaption>
</figure>

<figure>
<img loading="lazy" src="/wiki/f/results/rtx-5060-dr2-quiescent-full-spectrum/109352-M3_109352/diagnostics/spectral_chi2.png" alt="M3_109352: spectral pull, binned mean pull squared, cumulative chi-squared">
<figcaption>Pull of only 3530 fitted spectrum pixels of galaxy M3_109352 against the model, 1.140 per pixel at a 4.19 percent error floor.</figcaption>
</figure>

<figure>
<img loading="lazy" src="/wiki/f/results/rtx-5060-dr2-quiescent-full-spectrum/109352-M3_109352/diagnostics/sf_timescales.png" alt="M3_109352: cumulative mass formed against lookback time with t10 to t90">
<figcaption>Mass formed in galaxy M3_109352 against lookback time: t10 4.68, t20 4.27, t50 3.05 Gyr, only a 16-84 percent range.</figcaption>
</figure>

109713-M3_109713
: z 0.7275 · S/N 24.2

<figure>
<img loading="lazy" src="/wiki/f/results/rtx-5060-dr2-quiescent-full-spectrum/109713-M3_109713/diagnostics/photometric_chi2.png" alt="M3_109713: photometric pull and chi-squared contribution per band">
<figcaption>Pull of only the 12 fitted bands of galaxy M3_109713 against the model, 6.91 per band at a 5 percent flux error floor.</figcaption>
</figure>

<figure>
<img loading="lazy" src="/wiki/f/results/rtx-5060-dr2-quiescent-full-spectrum/109713-M3_109713/diagnostics/spectral_chi2.png" alt="M3_109713: spectral pull, binned mean pull squared, cumulative chi-squared">
<figcaption>Pull of only 3434 fitted spectrum pixels of galaxy M3_109713 against the model, 1.177 per pixel at a 4.36 percent error floor.</figcaption>
</figure>

<figure>
<img loading="lazy" src="/wiki/f/results/rtx-5060-dr2-quiescent-full-spectrum/109713-M3_109713/diagnostics/sf_timescales.png" alt="M3_109713: cumulative mass formed against lookback time with t10 to t90">
<figcaption>Mass formed in galaxy M3_109713 against lookback time: t10 4.63, t20 4.22, t50 2.99 Gyr, only a 16-84 percent range.</figcaption>
</figure>

109843-M3_109843
: z 0.7243 · S/N 12.9

<figure>
<img loading="lazy" src="/wiki/f/results/rtx-5060-dr2-quiescent-full-spectrum/109843-M3_109843/diagnostics/photometric_chi2.png" alt="M3_109843: photometric pull and chi-squared contribution per band">
<figcaption>Pull of only the 12 fitted bands of galaxy M3_109843 against the model, 3.72 per band at a 5 percent flux error floor.</figcaption>
</figure>

<figure>
<img loading="lazy" src="/wiki/f/results/rtx-5060-dr2-quiescent-full-spectrum/109843-M3_109843/diagnostics/spectral_chi2.png" alt="M3_109843: spectral pull, binned mean pull squared, cumulative chi-squared">
<figcaption>Pull of only 3418 fitted spectrum pixels of galaxy M3_109843 against the model, 1.188 per pixel at a 5.85 percent error floor.</figcaption>
</figure>

<figure>
<img loading="lazy" src="/wiki/f/results/rtx-5060-dr2-quiescent-full-spectrum/109843-M3_109843/diagnostics/sf_timescales.png" alt="M3_109843: cumulative mass formed against lookback time with t10 to t90">
<figcaption>Mass formed in galaxy M3_109843 against lookback time: t10 4.60, t20 4.16, t50 2.87 Gyr, only a 16-84 percent range.</figcaption>
</figure>

111390-M3_111390
: z 0.6673 · S/N 32.4

<figure>
<img loading="lazy" src="/wiki/f/results/rtx-5060-dr2-quiescent-full-spectrum/111390-M3_111390/diagnostics/photometric_chi2.png" alt="M3_111390: photometric pull and chi-squared contribution per band">
<figcaption>Pull of only the 12 fitted bands of galaxy M3_111390 against the model, 16.52 per band at a 5 percent flux error floor.</figcaption>
</figure>

<figure>
<img loading="lazy" src="/wiki/f/results/rtx-5060-dr2-quiescent-full-spectrum/111390-M3_111390/diagnostics/spectral_chi2.png" alt="M3_111390: spectral pull, binned mean pull squared, cumulative chi-squared">
<figcaption>Pull of only 3553 fitted spectrum pixels of galaxy M3_111390 against the model, 1.200 per pixel at a 3.39 percent error floor.</figcaption>
</figure>

<figure>
<img loading="lazy" src="/wiki/f/results/rtx-5060-dr2-quiescent-full-spectrum/111390-M3_111390/diagnostics/sf_timescales.png" alt="M3_111390: cumulative mass formed against lookback time with t10 to t90">
<figcaption>Mass formed in galaxy M3_111390 against lookback time: t10 4.60, t20 4.20, t50 2.98 Gyr, only a 16-84 percent range.</figcaption>
</figure>

112534-M4_112534
: z 0.9837 · S/N 6.4

<figure>
<img loading="lazy" src="/wiki/f/results/rtx-5060-dr2-quiescent-full-spectrum/112534-M4_112534/diagnostics/photometric_chi2.png" alt="M4_112534: photometric pull and chi-squared contribution per band">
<figcaption>Pull of only the 12 fitted bands of galaxy M4_112534 against the model, 5.52 per band at a 5 percent flux error floor.</figcaption>
</figure>

<figure>
<img loading="lazy" src="/wiki/f/results/rtx-5060-dr2-quiescent-full-spectrum/112534-M4_112534/diagnostics/spectral_chi2.png" alt="M4_112534: spectral pull, binned mean pull squared, cumulative chi-squared">
<figcaption>Pull of only 3828 fitted spectrum pixels of galaxy M4_112534 against the model, 1.110 per pixel at a 7.36 percent error floor.</figcaption>
</figure>

<figure>
<img loading="lazy" src="/wiki/f/results/rtx-5060-dr2-quiescent-full-spectrum/112534-M4_112534/diagnostics/sf_timescales.png" alt="M4_112534: cumulative mass formed against lookback time with t10 to t90">
<figcaption>Mass formed in galaxy M4_112534 against lookback time: t10 4.62, t20 4.22, t50 3.02 Gyr, only a 16-84 percent range.</figcaption>
</figure>

113852-M7_113852
: z 0.6752 · S/N 39.5

<figure>
<img loading="lazy" src="/wiki/f/results/rtx-5060-dr2-quiescent-full-spectrum/113852-M7_113852/diagnostics/photometric_chi2.png" alt="M7_113852: photometric pull and chi-squared contribution per band">
<figcaption>Pull of only the 12 fitted bands of galaxy M7_113852 against the model, 24.53 per band at a 5 percent flux error floor.</figcaption>
</figure>

<figure>
<img loading="lazy" src="/wiki/f/results/rtx-5060-dr2-quiescent-full-spectrum/113852-M7_113852/diagnostics/spectral_chi2.png" alt="M7_113852: spectral pull, binned mean pull squared, cumulative chi-squared">
<figcaption>Pull of only 3504 fitted spectrum pixels of galaxy M7_113852 against the model, 1.149 per pixel at a 4.23 percent error floor.</figcaption>
</figure>

<figure>
<img loading="lazy" src="/wiki/f/results/rtx-5060-dr2-quiescent-full-spectrum/113852-M7_113852/diagnostics/sf_timescales.png" alt="M7_113852: cumulative mass formed against lookback time with t10 to t90">
<figcaption>Mass formed in galaxy M7_113852 against lookback time: t10 4.62, t20 4.22, t50 3.01 Gyr, only a 16-84 percent range.</figcaption>
</figure>

117010-M3_117010
: z 0.6766 · S/N 18.3

<figure>
<img loading="lazy" src="/wiki/f/results/rtx-5060-dr2-quiescent-full-spectrum/117010-M3_117010/diagnostics/photometric_chi2.png" alt="M3_117010: photometric pull and chi-squared contribution per band">
<figcaption>Pull of only the 12 fitted bands of galaxy M3_117010 against the model, 3.66 per band at a 5 percent flux error floor.</figcaption>
</figure>

<figure>
<img loading="lazy" src="/wiki/f/results/rtx-5060-dr2-quiescent-full-spectrum/117010-M3_117010/diagnostics/spectral_chi2.png" alt="M3_117010: spectral pull, binned mean pull squared, cumulative chi-squared">
<figcaption>Pull of only 3414 fitted spectrum pixels of galaxy M3_117010 against the model, 1.149 per pixel at a 5.20 percent error floor.</figcaption>
</figure>

<figure>
<img loading="lazy" src="/wiki/f/results/rtx-5060-dr2-quiescent-full-spectrum/117010-M3_117010/diagnostics/sf_timescales.png" alt="M3_117010: cumulative mass formed against lookback time with t10 to t90">
<figcaption>Mass formed in galaxy M3_117010 against lookback time: t10 4.51, t20 3.99, t50 2.60 Gyr, only a 16-84 percent range.</figcaption>
</figure>

117400-M4_117400
: z 0.6687 · S/N 36.1

<figure>
<img loading="lazy" src="/wiki/f/results/rtx-5060-dr2-quiescent-full-spectrum/117400-M4_117400/diagnostics/photometric_chi2.png" alt="M4_117400: photometric pull and chi-squared contribution per band">
<figcaption>Pull of only the 12 fitted bands of galaxy M4_117400 against the model, 10.56 per band at a 5 percent flux error floor.</figcaption>
</figure>

<figure>
<img loading="lazy" src="/wiki/f/results/rtx-5060-dr2-quiescent-full-spectrum/117400-M4_117400/diagnostics/spectral_chi2.png" alt="M4_117400: spectral pull, binned mean pull squared, cumulative chi-squared">
<figcaption>Pull of only 3366 fitted spectrum pixels of galaxy M4_117400 against the model, 1.136 per pixel at a 5.10 percent error floor.</figcaption>
</figure>

<figure>
<img loading="lazy" src="/wiki/f/results/rtx-5060-dr2-quiescent-full-spectrum/117400-M4_117400/diagnostics/sf_timescales.png" alt="M4_117400: cumulative mass formed against lookback time with t10 to t90">
<figcaption>Mass formed in galaxy M4_117400 against lookback time: t10 4.63, t20 4.20, t50 2.95 Gyr, only a 16-84 percent range.</figcaption>
</figure>

117694-M3_117694
: z 0.6831 · S/N 24.2

<figure>
<img loading="lazy" src="/wiki/f/results/rtx-5060-dr2-quiescent-full-spectrum/117694-M3_117694/diagnostics/photometric_chi2.png" alt="M3_117694: photometric pull and chi-squared contribution per band">
<figcaption>Pull of only the 12 fitted bands of galaxy M3_117694 against the model, 2.73 per band at a 5 percent flux error floor.</figcaption>
</figure>

<figure>
<img loading="lazy" src="/wiki/f/results/rtx-5060-dr2-quiescent-full-spectrum/117694-M3_117694/diagnostics/spectral_chi2.png" alt="M3_117694: spectral pull, binned mean pull squared, cumulative chi-squared">
<figcaption>Pull of only 3508 fitted spectrum pixels of galaxy M3_117694 against the model, 1.177 per pixel at a 4.56 percent error floor.</figcaption>
</figure>

<figure>
<img loading="lazy" src="/wiki/f/results/rtx-5060-dr2-quiescent-full-spectrum/117694-M3_117694/diagnostics/sf_timescales.png" alt="M3_117694: cumulative mass formed against lookback time with t10 to t90">
<figcaption>Mass formed in galaxy M3_117694 against lookback time: t10 4.74, t20 4.33, t50 3.10 Gyr, only a 16-84 percent range.</figcaption>
</figure>

119474-M3_119474
: z 0.6809 · S/N 35.4

<figure>
<img loading="lazy" src="/wiki/f/results/rtx-5060-dr2-quiescent-full-spectrum/119474-M3_119474/diagnostics/photometric_chi2.png" alt="M3_119474: photometric pull and chi-squared contribution per band">
<figcaption>Pull of only the 12 fitted bands of galaxy M3_119474 against the model, 10.19 per band at a 5 percent flux error floor.</figcaption>
</figure>

<figure>
<img loading="lazy" src="/wiki/f/results/rtx-5060-dr2-quiescent-full-spectrum/119474-M3_119474/diagnostics/spectral_chi2.png" alt="M3_119474: spectral pull, binned mean pull squared, cumulative chi-squared">
<figcaption>Pull of only 3473 fitted spectrum pixels of galaxy M3_119474 against the model, 1.103 per pixel at a 3.82 percent error floor.</figcaption>
</figure>

<figure>
<img loading="lazy" src="/wiki/f/results/rtx-5060-dr2-quiescent-full-spectrum/119474-M3_119474/diagnostics/sf_timescales.png" alt="M3_119474: cumulative mass formed against lookback time with t10 to t90">
<figcaption>Mass formed in galaxy M3_119474 against lookback time: t10 7.09, t20 6.77, t50 5.82 Gyr, only a 16-84 percent range.</figcaption>
</figure>

119802-M3_119802
: z 0.6820 · S/N 25.4

<figure>
<img loading="lazy" src="/wiki/f/results/rtx-5060-dr2-quiescent-full-spectrum/119802-M3_119802/diagnostics/photometric_chi2.png" alt="M3_119802: photometric pull and chi-squared contribution per band">
<figcaption>Pull of only the 12 fitted bands of galaxy M3_119802 against the model, 16.15 per band at a 5 percent flux error floor.</figcaption>
</figure>

<figure>
<img loading="lazy" src="/wiki/f/results/rtx-5060-dr2-quiescent-full-spectrum/119802-M3_119802/diagnostics/spectral_chi2.png" alt="M3_119802: spectral pull, binned mean pull squared, cumulative chi-squared">
<figcaption>Pull of only 3461 fitted spectrum pixels of galaxy M3_119802 against the model, 1.215 per pixel at a 4.39 percent error floor.</figcaption>
</figure>

<figure>
<img loading="lazy" src="/wiki/f/results/rtx-5060-dr2-quiescent-full-spectrum/119802-M3_119802/diagnostics/sf_timescales.png" alt="M3_119802: cumulative mass formed against lookback time with t10 to t90">
<figcaption>Mass formed in galaxy M3_119802 against lookback time: t10 4.61, t20 4.21, t50 3.00 Gyr, only a 16-84 percent range.</figcaption>
</figure>

119809-M3_119809
: z 0.6801 · S/N 5.7

<figure>
<img loading="lazy" src="/wiki/f/results/rtx-5060-dr2-quiescent-full-spectrum/119809-M3_119809/diagnostics/photometric_chi2.png" alt="M3_119809: photometric pull and chi-squared contribution per band">
<figcaption>Pull of only the 12 fitted bands of galaxy M3_119809 against the model, 9.86 per band at a 5 percent flux error floor.</figcaption>
</figure>

<figure>
<img loading="lazy" src="/wiki/f/results/rtx-5060-dr2-quiescent-full-spectrum/119809-M3_119809/diagnostics/spectral_chi2.png" alt="M3_119809: spectral pull, binned mean pull squared, cumulative chi-squared">
<figcaption>Pull of only 3557 fitted spectrum pixels of galaxy M3_119809 against the model, 1.199 per pixel at a 9.77 percent error floor.</figcaption>
</figure>

<figure>
<img loading="lazy" src="/wiki/f/results/rtx-5060-dr2-quiescent-full-spectrum/119809-M3_119809/diagnostics/sf_timescales.png" alt="M3_119809: cumulative mass formed against lookback time with t10 to t90">
<figcaption>Mass formed in galaxy M3_119809 against lookback time: t10 2.71, t20 1.93, t50 0.75 Gyr, only a 16-84 percent range.</figcaption>
</figure>

120308-M3_120308
: z 0.7279 · S/N 29.0

<figure>
<img loading="lazy" src="/wiki/f/results/rtx-5060-dr2-quiescent-full-spectrum/120308-M3_120308/diagnostics/photometric_chi2.png" alt="M3_120308: photometric pull and chi-squared contribution per band">
<figcaption>Pull of only the 12 fitted bands of galaxy M3_120308 against the model, 10.65 per band at a 5 percent flux error floor.</figcaption>
</figure>

<figure>
<img loading="lazy" src="/wiki/f/results/rtx-5060-dr2-quiescent-full-spectrum/120308-M3_120308/diagnostics/spectral_chi2.png" alt="M3_120308: spectral pull, binned mean pull squared, cumulative chi-squared">
<figcaption>Pull of only 3532 fitted spectrum pixels of galaxy M3_120308 against the model, 1.167 per pixel at a 4.07 percent error floor.</figcaption>
</figure>

<figure>
<img loading="lazy" src="/wiki/f/results/rtx-5060-dr2-quiescent-full-spectrum/120308-M3_120308/diagnostics/sf_timescales.png" alt="M3_120308: cumulative mass formed against lookback time with t10 to t90">
<figcaption>Mass formed in galaxy M3_120308 against lookback time: t10 4.60, t20 4.17, t50 2.89 Gyr, only a 16-84 percent range.</figcaption>
</figure>

120372-M7_120372
: z 0.9415 · S/N 19.1

<figure>
<img loading="lazy" src="/wiki/f/results/rtx-5060-dr2-quiescent-full-spectrum/120372-M7_120372/diagnostics/photometric_chi2.png" alt="M7_120372: photometric pull and chi-squared contribution per band">
<figcaption>Pull of only the 12 fitted bands of galaxy M7_120372 against the model, 14.20 per band at a 5 percent flux error floor.</figcaption>
</figure>

<figure>
<img loading="lazy" src="/wiki/f/results/rtx-5060-dr2-quiescent-full-spectrum/120372-M7_120372/diagnostics/spectral_chi2.png" alt="M7_120372: spectral pull, binned mean pull squared, cumulative chi-squared">
<figcaption>Pull of only 3787 fitted spectrum pixels of galaxy M7_120372 against the model, 1.142 per pixel at a 5.07 percent error floor.</figcaption>
</figure>

<figure>
<img loading="lazy" src="/wiki/f/results/rtx-5060-dr2-quiescent-full-spectrum/120372-M7_120372/diagnostics/sf_timescales.png" alt="M7_120372: cumulative mass formed against lookback time with t10 to t90">
<figcaption>Mass formed in galaxy M7_120372 against lookback time: t10 5.75, t20 5.40, t50 4.40 Gyr, only a 16-84 percent range.</figcaption>
</figure>

120488-M7_120488
: z 0.9335 · S/N 13.6

<figure>
<img loading="lazy" src="/wiki/f/results/rtx-5060-dr2-quiescent-full-spectrum/120488-M7_120488/diagnostics/photometric_chi2.png" alt="M7_120488: photometric pull and chi-squared contribution per band">
<figcaption>Pull of only the 12 fitted bands of galaxy M7_120488 against the model, 8.33 per band at a 5 percent flux error floor.</figcaption>
</figure>

<figure>
<img loading="lazy" src="/wiki/f/results/rtx-5060-dr2-quiescent-full-spectrum/120488-M7_120488/diagnostics/spectral_chi2.png" alt="M7_120488: spectral pull, binned mean pull squared, cumulative chi-squared">
<figcaption>Pull of only 3802 fitted spectrum pixels of galaxy M7_120488 against the model, 1.075 per pixel at a 5.59 percent error floor.</figcaption>
</figure>

<figure>
<img loading="lazy" src="/wiki/f/results/rtx-5060-dr2-quiescent-full-spectrum/120488-M7_120488/diagnostics/sf_timescales.png" alt="M7_120488: cumulative mass formed against lookback time with t10 to t90">
<figcaption>Mass formed in galaxy M7_120488 against lookback time: t10 4.84, t20 4.37, t50 2.94 Gyr, only a 16-84 percent range.</figcaption>
</figure>

120540-M3_120540
: z 0.9554 · S/N 15.1

<figure>
<img loading="lazy" src="/wiki/f/results/rtx-5060-dr2-quiescent-full-spectrum/120540-M3_120540/diagnostics/photometric_chi2.png" alt="M3_120540: photometric pull and chi-squared contribution per band">
<figcaption>Pull of only the 12 fitted bands of galaxy M3_120540 against the model, 15.13 per band at a 5 percent flux error floor.</figcaption>
</figure>

<figure>
<img loading="lazy" src="/wiki/f/results/rtx-5060-dr2-quiescent-full-spectrum/120540-M3_120540/diagnostics/spectral_chi2.png" alt="M3_120540: spectral pull, binned mean pull squared, cumulative chi-squared">
<figcaption>Pull of only 3813 fitted spectrum pixels of galaxy M3_120540 against the model, 1.071 per pixel at a 5.54 percent error floor.</figcaption>
</figure>

<figure>
<img loading="lazy" src="/wiki/f/results/rtx-5060-dr2-quiescent-full-spectrum/120540-M3_120540/diagnostics/sf_timescales.png" alt="M3_120540: cumulative mass formed against lookback time with t10 to t90">
<figcaption>Mass formed in galaxy M3_120540 against lookback time: t10 4.56, t20 4.09, t50 2.75 Gyr, only a 16-84 percent range.</figcaption>
</figure>

120758-M7_120758
: z 0.9365 · S/N 9.8

<figure>
<img loading="lazy" src="/wiki/f/results/rtx-5060-dr2-quiescent-full-spectrum/120758-M7_120758/diagnostics/photometric_chi2.png" alt="M7_120758: photometric pull and chi-squared contribution per band">
<figcaption>Pull of only the 12 fitted bands of galaxy M7_120758 against the model, 10.24 per band at a 5 percent flux error floor.</figcaption>
</figure>

<figure>
<img loading="lazy" src="/wiki/f/results/rtx-5060-dr2-quiescent-full-spectrum/120758-M7_120758/diagnostics/spectral_chi2.png" alt="M7_120758: spectral pull, binned mean pull squared, cumulative chi-squared">
<figcaption>Pull of only 3772 fitted spectrum pixels of galaxy M7_120758 against the model, 1.040 per pixel at a 6.16 percent error floor.</figcaption>
</figure>

<figure>
<img loading="lazy" src="/wiki/f/results/rtx-5060-dr2-quiescent-full-spectrum/120758-M7_120758/diagnostics/sf_timescales.png" alt="M7_120758: cumulative mass formed against lookback time with t10 to t90">
<figcaption>Mass formed in galaxy M7_120758 against lookback time: t10 5.28, t20 4.74, t50 3.57 Gyr, only a 16-84 percent range.</figcaption>
</figure>

121482-M7_121482
: z 0.9360 · S/N 7.3

<figure>
<img loading="lazy" src="/wiki/f/results/rtx-5060-dr2-quiescent-full-spectrum/121482-M7_121482/diagnostics/photometric_chi2.png" alt="M7_121482: photometric pull and chi-squared contribution per band">
<figcaption>Pull of only the 12 fitted bands of galaxy M7_121482 against the model, 6.40 per band at a 5 percent flux error floor.</figcaption>
</figure>

<figure>
<img loading="lazy" src="/wiki/f/results/rtx-5060-dr2-quiescent-full-spectrum/121482-M7_121482/diagnostics/spectral_chi2.png" alt="M7_121482: spectral pull, binned mean pull squared, cumulative chi-squared">
<figcaption>Pull of only 3818 fitted spectrum pixels of galaxy M7_121482 against the model, 1.146 per pixel at a 6.87 percent error floor.</figcaption>
</figure>

<figure>
<img loading="lazy" src="/wiki/f/results/rtx-5060-dr2-quiescent-full-spectrum/121482-M7_121482/diagnostics/sf_timescales.png" alt="M7_121482: cumulative mass formed against lookback time with t10 to t90">
<figcaption>Mass formed in galaxy M7_121482 against lookback time: t10 5.61, t20 5.09, t50 3.87 Gyr, only a 16-84 percent range.</figcaption>
</figure>

122025-M7_122025
: z 0.7477 · S/N 14.0

<figure>
<img loading="lazy" src="/wiki/f/results/rtx-5060-dr2-quiescent-full-spectrum/122025-M7_122025/diagnostics/photometric_chi2.png" alt="M7_122025: photometric pull and chi-squared contribution per band">
<figcaption>Pull of only the 12 fitted bands of galaxy M7_122025 against the model, 7.29 per band at a 5 percent flux error floor.</figcaption>
</figure>

<figure>
<img loading="lazy" src="/wiki/f/results/rtx-5060-dr2-quiescent-full-spectrum/122025-M7_122025/diagnostics/spectral_chi2.png" alt="M7_122025: spectral pull, binned mean pull squared, cumulative chi-squared">
<figcaption>Pull of only 3778 fitted spectrum pixels of galaxy M7_122025 against the model, 1.171 per pixel at a 5.94 percent error floor.</figcaption>
</figure>

<figure>
<img loading="lazy" src="/wiki/f/results/rtx-5060-dr2-quiescent-full-spectrum/122025-M7_122025/diagnostics/sf_timescales.png" alt="M7_122025: cumulative mass formed against lookback time with t10 to t90">
<figcaption>Mass formed in galaxy M7_122025 against lookback time: t10 4.62, t20 4.21, t50 3.01 Gyr, only a 16-84 percent range.</figcaption>
</figure>

122242-M7_122242
: z 0.6032 · S/N 26.0

<figure>
<img loading="lazy" src="/wiki/f/results/rtx-5060-dr2-quiescent-full-spectrum/122242-M7_122242/diagnostics/photometric_chi2.png" alt="M7_122242: photometric pull and chi-squared contribution per band">
<figcaption>Pull of only the 12 fitted bands of galaxy M7_122242 against the model, 6.48 per band at a 5 percent flux error floor.</figcaption>
</figure>

<figure>
<img loading="lazy" src="/wiki/f/results/rtx-5060-dr2-quiescent-full-spectrum/122242-M7_122242/diagnostics/spectral_chi2.png" alt="M7_122242: spectral pull, binned mean pull squared, cumulative chi-squared">
<figcaption>Pull of only 3516 fitted spectrum pixels of galaxy M7_122242 against the model, 1.132 per pixel at a 4.19 percent error floor.</figcaption>
</figure>

<figure>
<img loading="lazy" src="/wiki/f/results/rtx-5060-dr2-quiescent-full-spectrum/122242-M7_122242/diagnostics/sf_timescales.png" alt="M7_122242: cumulative mass formed against lookback time with t10 to t90">
<figcaption>Mass formed in galaxy M7_122242 against lookback time: t10 4.62, t20 4.22, t50 3.00 Gyr, only a 16-84 percent range.</figcaption>
</figure>

123161-M4_123161
: z 0.7995 · S/N 21.0

<figure>
<img loading="lazy" src="/wiki/f/results/rtx-5060-dr2-quiescent-full-spectrum/123161-M4_123161/diagnostics/photometric_chi2.png" alt="M4_123161: photometric pull and chi-squared contribution per band">
<figcaption>Pull of only the 12 fitted bands of galaxy M4_123161 against the model, 3.06 per band at a 5 percent flux error floor.</figcaption>
</figure>

<figure>
<img loading="lazy" src="/wiki/f/results/rtx-5060-dr2-quiescent-full-spectrum/123161-M4_123161/diagnostics/spectral_chi2.png" alt="M4_123161: spectral pull, binned mean pull squared, cumulative chi-squared">
<figcaption>Pull of only 3621 fitted spectrum pixels of galaxy M4_123161 against the model, 1.153 per pixel at a 5.62 percent error floor.</figcaption>
</figure>

<figure>
<img loading="lazy" src="/wiki/f/results/rtx-5060-dr2-quiescent-full-spectrum/123161-M4_123161/diagnostics/sf_timescales.png" alt="M4_123161: cumulative mass formed against lookback time with t10 to t90">
<figcaption>Mass formed in galaxy M4_123161 against lookback time: t10 6.39, t20 6.03, t50 4.69 Gyr, only a 16-84 percent range.</figcaption>
</figure>

124231-M4_124231
: z 0.6771 · S/N 34.5

<figure>
<img loading="lazy" src="/wiki/f/results/rtx-5060-dr2-quiescent-full-spectrum/124231-M4_124231/diagnostics/photometric_chi2.png" alt="M4_124231: photometric pull and chi-squared contribution per band">
<figcaption>Pull of only the 12 fitted bands of galaxy M4_124231 against the model, 8.63 per band at a 5 percent flux error floor.</figcaption>
</figure>

<figure>
<img loading="lazy" src="/wiki/f/results/rtx-5060-dr2-quiescent-full-spectrum/124231-M4_124231/diagnostics/spectral_chi2.png" alt="M4_124231: spectral pull, binned mean pull squared, cumulative chi-squared">
<figcaption>Pull of only 3566 fitted spectrum pixels of galaxy M4_124231 against the model, 1.223 per pixel at a 4.05 percent error floor.</figcaption>
</figure>

<figure>
<img loading="lazy" src="/wiki/f/results/rtx-5060-dr2-quiescent-full-spectrum/124231-M4_124231/diagnostics/sf_timescales.png" alt="M4_124231: cumulative mass formed against lookback time with t10 to t90">
<figcaption>Mass formed in galaxy M4_124231 against lookback time: t10 4.58, t20 4.15, t50 2.87 Gyr, only a 16-84 percent range.</figcaption>
</figure>

124875-M7_124875
: z 0.6026 · S/N 31.5

<figure>
<img loading="lazy" src="/wiki/f/results/rtx-5060-dr2-quiescent-full-spectrum/124875-M7_124875/diagnostics/photometric_chi2.png" alt="M7_124875: photometric pull and chi-squared contribution per band">
<figcaption>Pull of only the 12 fitted bands of galaxy M7_124875 against the model, 2.54 per band at a 5 percent flux error floor.</figcaption>
</figure>

<figure>
<img loading="lazy" src="/wiki/f/results/rtx-5060-dr2-quiescent-full-spectrum/124875-M7_124875/diagnostics/spectral_chi2.png" alt="M7_124875: spectral pull, binned mean pull squared, cumulative chi-squared">
<figcaption>Pull of only 3490 fitted spectrum pixels of galaxy M7_124875 against the model, 1.138 per pixel at a 3.89 percent error floor.</figcaption>
</figure>

<figure>
<img loading="lazy" src="/wiki/f/results/rtx-5060-dr2-quiescent-full-spectrum/124875-M7_124875/diagnostics/sf_timescales.png" alt="M7_124875: cumulative mass formed against lookback time with t10 to t90">
<figcaption>Mass formed in galaxy M7_124875 against lookback time: t10 4.58, t20 4.13, t50 2.81 Gyr, only a 16-84 percent range.</figcaption>
</figure>

125213-M4_125213
: z 0.6772 · S/N 27.9

<figure>
<img loading="lazy" src="/wiki/f/results/rtx-5060-dr2-quiescent-full-spectrum/125213-M4_125213/diagnostics/photometric_chi2.png" alt="M4_125213: photometric pull and chi-squared contribution per band">
<figcaption>Pull of only the 12 fitted bands of galaxy M4_125213 against the model, 10.74 per band at a 5 percent flux error floor.</figcaption>
</figure>

<figure>
<img loading="lazy" src="/wiki/f/results/rtx-5060-dr2-quiescent-full-spectrum/125213-M4_125213/diagnostics/spectral_chi2.png" alt="M4_125213: spectral pull, binned mean pull squared, cumulative chi-squared">
<figcaption>Pull of only 3458 fitted spectrum pixels of galaxy M4_125213 against the model, 1.191 per pixel at a 3.84 percent error floor.</figcaption>
</figure>

<figure>
<img loading="lazy" src="/wiki/f/results/rtx-5060-dr2-quiescent-full-spectrum/125213-M4_125213/diagnostics/sf_timescales.png" alt="M4_125213: cumulative mass formed against lookback time with t10 to t90">
<figcaption>Mass formed in galaxy M4_125213 against lookback time: t10 4.61, t20 4.21, t50 3.01 Gyr, only a 16-84 percent range.</figcaption>
</figure>

126153-M1_126153
: z 0.6823 · S/N 10.3

<figure>
<img loading="lazy" src="/wiki/f/results/rtx-5060-dr2-quiescent-full-spectrum/126153-M1_126153/diagnostics/photometric_chi2.png" alt="M1_126153: photometric pull and chi-squared contribution per band">
<figcaption>Pull of only the 12 fitted bands of galaxy M1_126153 against the model, 2.88 per band at a 5 percent flux error floor.</figcaption>
</figure>

<figure>
<img loading="lazy" src="/wiki/f/results/rtx-5060-dr2-quiescent-full-spectrum/126153-M1_126153/diagnostics/spectral_chi2.png" alt="M1_126153: spectral pull, binned mean pull squared, cumulative chi-squared">
<figcaption>Pull of only 3493 fitted spectrum pixels of galaxy M1_126153 against the model, 1.166 per pixel at a 6.63 percent error floor.</figcaption>
</figure>

<figure>
<img loading="lazy" src="/wiki/f/results/rtx-5060-dr2-quiescent-full-spectrum/126153-M1_126153/diagnostics/sf_timescales.png" alt="M1_126153: cumulative mass formed against lookback time with t10 to t90">
<figcaption>Mass formed in galaxy M1_126153 against lookback time: t10 6.98, t20 6.55, t50 5.28 Gyr, only a 16-84 percent range.</figcaption>
</figure>

126578-M1_126578
: z 0.7504 · S/N 15.1

<figure>
<img loading="lazy" src="/wiki/f/results/rtx-5060-dr2-quiescent-full-spectrum/126578-M1_126578/diagnostics/photometric_chi2.png" alt="M1_126578: photometric pull and chi-squared contribution per band">
<figcaption>Pull of only the 12 fitted bands of galaxy M1_126578 against the model, 11.95 per band at a 5 percent flux error floor.</figcaption>
</figure>

<figure>
<img loading="lazy" src="/wiki/f/results/rtx-5060-dr2-quiescent-full-spectrum/126578-M1_126578/diagnostics/spectral_chi2.png" alt="M1_126578: spectral pull, binned mean pull squared, cumulative chi-squared">
<figcaption>Pull of only 3545 fitted spectrum pixels of galaxy M1_126578 against the model, 1.166 per pixel at a 6.05 percent error floor.</figcaption>
</figure>

<figure>
<img loading="lazy" src="/wiki/f/results/rtx-5060-dr2-quiescent-full-spectrum/126578-M1_126578/diagnostics/sf_timescales.png" alt="M1_126578: cumulative mass formed against lookback time with t10 to t90">
<figcaption>Mass formed in galaxy M1_126578 against lookback time: t10 6.65, t20 6.29, t50 5.19 Gyr, only a 16-84 percent range.</figcaption>
</figure>

127946-M5_127946
: z 0.9387 · S/N 5.9

<figure>
<img loading="lazy" src="/wiki/f/results/rtx-5060-dr2-quiescent-full-spectrum/127946-M5_127946/diagnostics/photometric_chi2.png" alt="M5_127946: photometric pull and chi-squared contribution per band">
<figcaption>Pull of only the 12 fitted bands of galaxy M5_127946 against the model, 2.27 per band at a 5 percent flux error floor.</figcaption>
</figure>

<figure>
<img loading="lazy" src="/wiki/f/results/rtx-5060-dr2-quiescent-full-spectrum/127946-M5_127946/diagnostics/spectral_chi2.png" alt="M5_127946: spectral pull, binned mean pull squared, cumulative chi-squared">
<figcaption>Pull of only 3770 fitted spectrum pixels of galaxy M5_127946 against the model, 1.004 per pixel at a 8.79 percent error floor.</figcaption>
</figure>

<figure>
<img loading="lazy" src="/wiki/f/results/rtx-5060-dr2-quiescent-full-spectrum/127946-M5_127946/diagnostics/sf_timescales.png" alt="M5_127946: cumulative mass formed against lookback time with t10 to t90">
<figcaption>Mass formed in galaxy M5_127946 against lookback time: t10 5.94, t20 5.77, t50 5.25 Gyr, only a 16-84 percent range.</figcaption>
</figure>

128311-M5_128311
: z 0.7303 · S/N 26.0

<figure>
<img loading="lazy" src="/wiki/f/results/rtx-5060-dr2-quiescent-full-spectrum/128311-M5_128311/diagnostics/photometric_chi2.png" alt="M5_128311: photometric pull and chi-squared contribution per band">
<figcaption>Pull of only the 12 fitted bands of galaxy M5_128311 against the model, 9.85 per band at a 5 percent flux error floor.</figcaption>
</figure>

<figure>
<img loading="lazy" src="/wiki/f/results/rtx-5060-dr2-quiescent-full-spectrum/128311-M5_128311/diagnostics/spectral_chi2.png" alt="M5_128311: spectral pull, binned mean pull squared, cumulative chi-squared">
<figcaption>Pull of only 3681 fitted spectrum pixels of galaxy M5_128311 against the model, 1.121 per pixel at a 4.57 percent error floor.</figcaption>
</figure>

<figure>
<img loading="lazy" src="/wiki/f/results/rtx-5060-dr2-quiescent-full-spectrum/128311-M5_128311/diagnostics/sf_timescales.png" alt="M5_128311: cumulative mass formed against lookback time with t10 to t90">
<figcaption>Mass formed in galaxy M5_128311 against lookback time: t10 6.46, t20 5.78, t50 3.99 Gyr, only a 16-84 percent range.</figcaption>
</figure>

129596-M2_129596
: z 0.6956 · S/N 18.6

<figure>
<img loading="lazy" src="/wiki/f/results/rtx-5060-dr2-quiescent-full-spectrum/129596-M2_129596/diagnostics/photometric_chi2.png" alt="M2_129596: photometric pull and chi-squared contribution per band">
<figcaption>Pull of only the 12 fitted bands of galaxy M2_129596 against the model, 7.28 per band at a 5 percent flux error floor.</figcaption>
</figure>

<figure>
<img loading="lazy" src="/wiki/f/results/rtx-5060-dr2-quiescent-full-spectrum/129596-M2_129596/diagnostics/spectral_chi2.png" alt="M2_129596: spectral pull, binned mean pull squared, cumulative chi-squared">
<figcaption>Pull of only 3563 fitted spectrum pixels of galaxy M2_129596 against the model, 1.049 per pixel at a 3.64 percent error floor.</figcaption>
</figure>

<figure>
<img loading="lazy" src="/wiki/f/results/rtx-5060-dr2-quiescent-full-spectrum/129596-M2_129596/diagnostics/sf_timescales.png" alt="M2_129596: cumulative mass formed against lookback time with t10 to t90">
<figcaption>Mass formed in galaxy M2_129596 against lookback time: t10 5.89, t20 4.83, t50 3.51 Gyr, only a 16-84 percent range.</figcaption>
</figure>

130005-M2_130005
: z 0.8341 · S/N 18.2

<figure>
<img loading="lazy" src="/wiki/f/results/rtx-5060-dr2-quiescent-full-spectrum/130005-M2_130005/diagnostics/photometric_chi2.png" alt="M2_130005: photometric pull and chi-squared contribution per band">
<figcaption>Pull of only the 12 fitted bands of galaxy M2_130005 against the model, 7.86 per band at a 5 percent flux error floor.</figcaption>
</figure>

<figure>
<img loading="lazy" src="/wiki/f/results/rtx-5060-dr2-quiescent-full-spectrum/130005-M2_130005/diagnostics/spectral_chi2.png" alt="M2_130005: spectral pull, binned mean pull squared, cumulative chi-squared">
<figcaption>Pull of only 3369 fitted spectrum pixels of galaxy M2_130005 against the model, 1.112 per pixel at a 5.36 percent error floor.</figcaption>
</figure>

<figure>
<img loading="lazy" src="/wiki/f/results/rtx-5060-dr2-quiescent-full-spectrum/130005-M2_130005/diagnostics/sf_timescales.png" alt="M2_130005: cumulative mass formed against lookback time with t10 to t90">
<figcaption>Mass formed in galaxy M2_130005 against lookback time: t10 6.36, t20 6.13, t50 5.45 Gyr, only a 16-84 percent range.</figcaption>
</figure>

130052-M1_130052
: z 0.6041 · S/N 44.3

<figure>
<img loading="lazy" src="/wiki/f/results/rtx-5060-dr2-quiescent-full-spectrum/130052-M1_130052/diagnostics/photometric_chi2.png" alt="M1_130052: photometric pull and chi-squared contribution per band">
<figcaption>Pull of only the 12 fitted bands of galaxy M1_130052 against the model, 7.04 per band at a 5 percent flux error floor.</figcaption>
</figure>

<figure>
<img loading="lazy" src="/wiki/f/results/rtx-5060-dr2-quiescent-full-spectrum/130052-M1_130052/diagnostics/spectral_chi2.png" alt="M1_130052: spectral pull, binned mean pull squared, cumulative chi-squared">
<figcaption>Pull of only 3590 fitted spectrum pixels of galaxy M1_130052 against the model, 1.025 per pixel at a 2.65 percent error floor.</figcaption>
</figure>

<figure>
<img loading="lazy" src="/wiki/f/results/rtx-5060-dr2-quiescent-full-spectrum/130052-M1_130052/diagnostics/sf_timescales.png" alt="M1_130052: cumulative mass formed against lookback time with t10 to t90">
<figcaption>Mass formed in galaxy M1_130052 against lookback time: t10 7.58, t20 7.28, t50 6.38 Gyr, only a 16-84 percent range.</figcaption>
</figure>

133240-M1_133240
: z 0.7282 · S/N 11.4

<figure>
<img loading="lazy" src="/wiki/f/results/rtx-5060-dr2-quiescent-full-spectrum/133240-M1_133240/diagnostics/photometric_chi2.png" alt="M1_133240: photometric pull and chi-squared contribution per band">
<figcaption>Pull of only the 12 fitted bands of galaxy M1_133240 against the model, 2.57 per band at a 5 percent flux error floor.</figcaption>
</figure>

<figure>
<img loading="lazy" src="/wiki/f/results/rtx-5060-dr2-quiescent-full-spectrum/133240-M1_133240/diagnostics/spectral_chi2.png" alt="M1_133240: spectral pull, binned mean pull squared, cumulative chi-squared">
<figcaption>Pull of only 3560 fitted spectrum pixels of galaxy M1_133240 against the model, 1.077 per pixel at a 3.96 percent error floor.</figcaption>
</figure>

<figure>
<img loading="lazy" src="/wiki/f/results/rtx-5060-dr2-quiescent-full-spectrum/133240-M1_133240/diagnostics/sf_timescales.png" alt="M1_133240: cumulative mass formed against lookback time with t10 to t90">
<figcaption>Mass formed in galaxy M1_133240 against lookback time: t10 4.68, t20 4.27, t50 3.05 Gyr, only a 16-84 percent range.</figcaption>
</figure>

133501-M2_133501
: z 0.7292 · S/N 57.7

<figure>
<img loading="lazy" src="/wiki/f/results/rtx-5060-dr2-quiescent-full-spectrum/133501-M2_133501/diagnostics/photometric_chi2.png" alt="M2_133501: photometric pull and chi-squared contribution per band">
<figcaption>Pull of only the 12 fitted bands of galaxy M2_133501 against the model, 8.81 per band at a 5 percent flux error floor.</figcaption>
</figure>

<figure>
<img loading="lazy" src="/wiki/f/results/rtx-5060-dr2-quiescent-full-spectrum/133501-M2_133501/diagnostics/spectral_chi2.png" alt="M2_133501: spectral pull, binned mean pull squared, cumulative chi-squared">
<figcaption>Pull of only 3582 fitted spectrum pixels of galaxy M2_133501 against the model, 1.075 per pixel at a 4.72 percent error floor.</figcaption>
</figure>

<figure>
<img loading="lazy" src="/wiki/f/results/rtx-5060-dr2-quiescent-full-spectrum/133501-M2_133501/diagnostics/sf_timescales.png" alt="M2_133501: cumulative mass formed against lookback time with t10 to t90">
<figcaption>Mass formed in galaxy M2_133501 against lookback time: t10 4.48, t20 3.94, t50 2.55 Gyr, only a 16-84 percent range.</figcaption>
</figure>

134021-M2_134021
: z 0.7493 · S/N 25.8

<figure>
<img loading="lazy" src="/wiki/f/results/rtx-5060-dr2-quiescent-full-spectrum/134021-M2_134021/diagnostics/photometric_chi2.png" alt="M2_134021: photometric pull and chi-squared contribution per band">
<figcaption>Pull of only the 12 fitted bands of galaxy M2_134021 against the model, 8.55 per band at a 5 percent flux error floor.</figcaption>
</figure>

<figure>
<img loading="lazy" src="/wiki/f/results/rtx-5060-dr2-quiescent-full-spectrum/134021-M2_134021/diagnostics/spectral_chi2.png" alt="M2_134021: spectral pull, binned mean pull squared, cumulative chi-squared">
<figcaption>Pull of only 3558 fitted spectrum pixels of galaxy M2_134021 against the model, 1.054 per pixel at a 4.17 percent error floor.</figcaption>
</figure>

<figure>
<img loading="lazy" src="/wiki/f/results/rtx-5060-dr2-quiescent-full-spectrum/134021-M2_134021/diagnostics/sf_timescales.png" alt="M2_134021: cumulative mass formed against lookback time with t10 to t90">
<figcaption>Mass formed in galaxy M2_134021 against lookback time: t10 4.44, t20 3.84, t50 2.44 Gyr, only a 16-84 percent range.</figcaption>
</figure>

134391-M2_134391
: z 0.6835 · S/N 44.6

<figure>
<img loading="lazy" src="/wiki/f/results/rtx-5060-dr2-quiescent-full-spectrum/134391-M2_134391/diagnostics/photometric_chi2.png" alt="M2_134391: photometric pull and chi-squared contribution per band">
<figcaption>Pull of only the 12 fitted bands of galaxy M2_134391 against the model, 19.58 per band at a 5 percent flux error floor.</figcaption>
</figure>

<figure>
<img loading="lazy" src="/wiki/f/results/rtx-5060-dr2-quiescent-full-spectrum/134391-M2_134391/diagnostics/spectral_chi2.png" alt="M2_134391: spectral pull, binned mean pull squared, cumulative chi-squared">
<figcaption>Pull of only 3567 fitted spectrum pixels of galaxy M2_134391 against the model, 1.137 per pixel at a 2.90 percent error floor.</figcaption>
</figure>

<figure>
<img loading="lazy" src="/wiki/f/results/rtx-5060-dr2-quiescent-full-spectrum/134391-M2_134391/diagnostics/sf_timescales.png" alt="M2_134391: cumulative mass formed against lookback time with t10 to t90">
<figcaption>Mass formed in galaxy M2_134391 against lookback time: t10 4.61, t20 4.21, t50 3.00 Gyr, only a 16-84 percent range.</figcaption>
</figure>

139423-M1_139423
: z 0.7495 · S/N 28.1

<figure>
<img loading="lazy" src="/wiki/f/results/rtx-5060-dr2-quiescent-full-spectrum/139423-M1_139423/diagnostics/photometric_chi2.png" alt="M1_139423: photometric pull and chi-squared contribution per band">
<figcaption>Pull of only the 12 fitted bands of galaxy M1_139423 against the model, 3.92 per band at a 5 percent flux error floor.</figcaption>
</figure>

<figure>
<img loading="lazy" src="/wiki/f/results/rtx-5060-dr2-quiescent-full-spectrum/139423-M1_139423/diagnostics/spectral_chi2.png" alt="M1_139423: spectral pull, binned mean pull squared, cumulative chi-squared">
<figcaption>Pull of only 3456 fitted spectrum pixels of galaxy M1_139423 against the model, 1.149 per pixel at a 5.91 percent error floor.</figcaption>
</figure>

<figure>
<img loading="lazy" src="/wiki/f/results/rtx-5060-dr2-quiescent-full-spectrum/139423-M1_139423/diagnostics/sf_timescales.png" alt="M1_139423: cumulative mass formed against lookback time with t10 to t90">
<figcaption>Mass formed in galaxy M1_139423 against lookback time: t10 4.13, t20 3.16, t50 2.10 Gyr, only a 16-84 percent range.</figcaption>
</figure>

139662-M2_139662
: z 0.6706 · S/N 17.3

<figure>
<img loading="lazy" src="/wiki/f/results/rtx-5060-dr2-quiescent-full-spectrum/139662-M2_139662/diagnostics/photometric_chi2.png" alt="M2_139662: photometric pull and chi-squared contribution per band">
<figcaption>Pull of only the 12 fitted bands of galaxy M2_139662 against the model, 3.87 per band at a 5 percent flux error floor.</figcaption>
</figure>

<figure>
<img loading="lazy" src="/wiki/f/results/rtx-5060-dr2-quiescent-full-spectrum/139662-M2_139662/diagnostics/spectral_chi2.png" alt="M2_139662: spectral pull, binned mean pull squared, cumulative chi-squared">
<figcaption>Pull of only 3430 fitted spectrum pixels of galaxy M2_139662 against the model, 2.685 per pixel at a 10.00 percent error floor.</figcaption>
</figure>

<figure>
<img loading="lazy" src="/wiki/f/results/rtx-5060-dr2-quiescent-full-spectrum/139662-M2_139662/diagnostics/sf_timescales.png" alt="M2_139662: cumulative mass formed against lookback time with t10 to t90">
<figcaption>Mass formed in galaxy M2_139662 against lookback time: t10 7.15, t20 6.83, t50 5.86 Gyr, only a 16-84 percent range.</figcaption>
</figure>

143127-M7_143127
: z 0.6964 · S/N 12.2

<figure>
<img loading="lazy" src="/wiki/f/results/rtx-5060-dr2-quiescent-full-spectrum/143127-M7_143127/diagnostics/photometric_chi2.png" alt="M7_143127: photometric pull and chi-squared contribution per band">
<figcaption>Pull of only the 12 fitted bands of galaxy M7_143127 against the model, 3.32 per band at a 5 percent flux error floor.</figcaption>
</figure>

<figure>
<img loading="lazy" src="/wiki/f/results/rtx-5060-dr2-quiescent-full-spectrum/143127-M7_143127/diagnostics/spectral_chi2.png" alt="M7_143127: spectral pull, binned mean pull squared, cumulative chi-squared">
<figcaption>Pull of only 3537 fitted spectrum pixels of galaxy M7_143127 against the model, 1.204 per pixel at a 7.51 percent error floor.</figcaption>
</figure>

<figure>
<img loading="lazy" src="/wiki/f/results/rtx-5060-dr2-quiescent-full-spectrum/143127-M7_143127/diagnostics/sf_timescales.png" alt="M7_143127: cumulative mass formed against lookback time with t10 to t90">
<figcaption>Mass formed in galaxy M7_143127 against lookback time: t10 4.93, t20 4.51, t50 3.25 Gyr, only a 16-84 percent range.</figcaption>
</figure>

145276-M8_145276
: z 0.7506 · S/N 17.2

<figure>
<img loading="lazy" src="/wiki/f/results/rtx-5060-dr2-quiescent-full-spectrum/145276-M8_145276/diagnostics/photometric_chi2.png" alt="M8_145276: photometric pull and chi-squared contribution per band">
<figcaption>Pull of only the 12 fitted bands of galaxy M8_145276 against the model, 1.80 per band at a 5 percent flux error floor.</figcaption>
</figure>

<figure>
<img loading="lazy" src="/wiki/f/results/rtx-5060-dr2-quiescent-full-spectrum/145276-M8_145276/diagnostics/spectral_chi2.png" alt="M8_145276: spectral pull, binned mean pull squared, cumulative chi-squared">
<figcaption>Pull of only 3516 fitted spectrum pixels of galaxy M8_145276 against the model, 1.101 per pixel at a 4.08 percent error floor.</figcaption>
</figure>

<figure>
<img loading="lazy" src="/wiki/f/results/rtx-5060-dr2-quiescent-full-spectrum/145276-M8_145276/diagnostics/sf_timescales.png" alt="M8_145276: cumulative mass formed against lookback time with t10 to t90">
<figcaption>Mass formed in galaxy M8_145276 against lookback time: t10 4.60, t20 4.19, t50 2.94 Gyr, only a 16-84 percent range.</figcaption>
</figure>

146213-M7_146213
: z 0.6875 · S/N 19.2

<figure>
<img loading="lazy" src="/wiki/f/results/rtx-5060-dr2-quiescent-full-spectrum/146213-M7_146213/diagnostics/photometric_chi2.png" alt="M7_146213: photometric pull and chi-squared contribution per band">
<figcaption>Pull of only the 12 fitted bands of galaxy M7_146213 against the model, 3.26 per band at a 5 percent flux error floor.</figcaption>
</figure>

<figure>
<img loading="lazy" src="/wiki/f/results/rtx-5060-dr2-quiescent-full-spectrum/146213-M7_146213/diagnostics/spectral_chi2.png" alt="M7_146213: spectral pull, binned mean pull squared, cumulative chi-squared">
<figcaption>Pull of only 3557 fitted spectrum pixels of galaxy M7_146213 against the model, 1.116 per pixel at a 5.19 percent error floor.</figcaption>
</figure>

<figure>
<img loading="lazy" src="/wiki/f/results/rtx-5060-dr2-quiescent-full-spectrum/146213-M7_146213/diagnostics/sf_timescales.png" alt="M7_146213: cumulative mass formed against lookback time with t10 to t90">
<figcaption>Mass formed in galaxy M7_146213 against lookback time: t10 4.64, t20 4.24, t50 3.02 Gyr, only a 16-84 percent range.</figcaption>
</figure>

147270-M7_147270
: z 0.8473 · S/N 20.8

<figure>
<img loading="lazy" src="/wiki/f/results/rtx-5060-dr2-quiescent-full-spectrum/147270-M7_147270/diagnostics/photometric_chi2.png" alt="M7_147270: photometric pull and chi-squared contribution per band">
<figcaption>Pull of only the 12 fitted bands of galaxy M7_147270 against the model, 6.50 per band at a 5 percent flux error floor.</figcaption>
</figure>

<figure>
<img loading="lazy" src="/wiki/f/results/rtx-5060-dr2-quiescent-full-spectrum/147270-M7_147270/diagnostics/spectral_chi2.png" alt="M7_147270: spectral pull, binned mean pull squared, cumulative chi-squared">
<figcaption>Pull of only 3843 fitted spectrum pixels of galaxy M7_147270 against the model, 1.105 per pixel at a 4.47 percent error floor.</figcaption>
</figure>

<figure>
<img loading="lazy" src="/wiki/f/results/rtx-5060-dr2-quiescent-full-spectrum/147270-M7_147270/diagnostics/sf_timescales.png" alt="M7_147270: cumulative mass formed against lookback time with t10 to t90">
<figcaption>Mass formed in galaxy M7_147270 against lookback time: t10 6.12, t20 5.71, t50 4.54 Gyr, only a 16-84 percent range.</figcaption>
</figure>

147539-M8_147539
: z 0.6958 · S/N 30.5

<figure>
<img loading="lazy" src="/wiki/f/results/rtx-5060-dr2-quiescent-full-spectrum/147539-M8_147539/diagnostics/photometric_chi2.png" alt="M8_147539: photometric pull and chi-squared contribution per band">
<figcaption>Pull of only the 12 fitted bands of galaxy M8_147539 against the model, 7.06 per band at a 5 percent flux error floor.</figcaption>
</figure>

<figure>
<img loading="lazy" src="/wiki/f/results/rtx-5060-dr2-quiescent-full-spectrum/147539-M8_147539/diagnostics/spectral_chi2.png" alt="M8_147539: spectral pull, binned mean pull squared, cumulative chi-squared">
<figcaption>Pull of only 3558 fitted spectrum pixels of galaxy M8_147539 against the model, 1.192 per pixel at a 3.68 percent error floor.</figcaption>
</figure>

<figure>
<img loading="lazy" src="/wiki/f/results/rtx-5060-dr2-quiescent-full-spectrum/147539-M8_147539/diagnostics/sf_timescales.png" alt="M8_147539: cumulative mass formed against lookback time with t10 to t90">
<figcaption>Mass formed in galaxy M8_147539 against lookback time: t10 6.50, t20 5.67, t50 3.89 Gyr, only a 16-84 percent range.</figcaption>
</figure>

147849-M7_147849
: z 0.6773 · S/N 29.8

<figure>
<img loading="lazy" src="/wiki/f/results/rtx-5060-dr2-quiescent-full-spectrum/147849-M7_147849/diagnostics/photometric_chi2.png" alt="M7_147849: photometric pull and chi-squared contribution per band">
<figcaption>Pull of only the 12 fitted bands of galaxy M7_147849 against the model, 12.99 per band at a 5 percent flux error floor.</figcaption>
</figure>

<figure>
<img loading="lazy" src="/wiki/f/results/rtx-5060-dr2-quiescent-full-spectrum/147849-M7_147849/diagnostics/spectral_chi2.png" alt="M7_147849: spectral pull, binned mean pull squared, cumulative chi-squared">
<figcaption>Pull of only 3560 fitted spectrum pixels of galaxy M7_147849 against the model, 1.155 per pixel at a 4.21 percent error floor.</figcaption>
</figure>

<figure>
<img loading="lazy" src="/wiki/f/results/rtx-5060-dr2-quiescent-full-spectrum/147849-M7_147849/diagnostics/sf_timescales.png" alt="M7_147849: cumulative mass formed against lookback time with t10 to t90">
<figcaption>Mass formed in galaxy M7_147849 against lookback time: t10 4.61, t20 4.21, t50 3.00 Gyr, only a 16-84 percent range.</figcaption>
</figure>

148698-M8_148698
: z 0.6755 · S/N 33.0

<figure>
<img loading="lazy" src="/wiki/f/results/rtx-5060-dr2-quiescent-full-spectrum/148698-M8_148698/diagnostics/photometric_chi2.png" alt="M8_148698: photometric pull and chi-squared contribution per band">
<figcaption>Pull of only the 12 fitted bands of galaxy M8_148698 against the model, 1.72 per band at a 5 percent flux error floor.</figcaption>
</figure>

<figure>
<img loading="lazy" src="/wiki/f/results/rtx-5060-dr2-quiescent-full-spectrum/148698-M8_148698/diagnostics/spectral_chi2.png" alt="M8_148698: spectral pull, binned mean pull squared, cumulative chi-squared">
<figcaption>Pull of only 3587 fitted spectrum pixels of galaxy M8_148698 against the model, 1.072 per pixel at a 3.59 percent error floor.</figcaption>
</figure>

<figure>
<img loading="lazy" src="/wiki/f/results/rtx-5060-dr2-quiescent-full-spectrum/148698-M8_148698/diagnostics/sf_timescales.png" alt="M8_148698: cumulative mass formed against lookback time with t10 to t90">
<figcaption>Mass formed in galaxy M8_148698 against lookback time: t10 2.73, t20 2.46, t50 1.64 Gyr, only a 16-84 percent range.</figcaption>
</figure>

150848-M8_150848
: z 0.7011 · S/N 40.9

<figure>
<img loading="lazy" src="/wiki/f/results/rtx-5060-dr2-quiescent-full-spectrum/150848-M8_150848/diagnostics/photometric_chi2.png" alt="M8_150848: photometric pull and chi-squared contribution per band">
<figcaption>Pull of only the 12 fitted bands of galaxy M8_150848 against the model, 9.12 per band at a 5 percent flux error floor.</figcaption>
</figure>

<figure>
<img loading="lazy" src="/wiki/f/results/rtx-5060-dr2-quiescent-full-spectrum/150848-M8_150848/diagnostics/spectral_chi2.png" alt="M8_150848: spectral pull, binned mean pull squared, cumulative chi-squared">
<figcaption>Pull of only 3576 fitted spectrum pixels of galaxy M8_150848 against the model, 1.103 per pixel at a 3.05 percent error floor.</figcaption>
</figure>

<figure>
<img loading="lazy" src="/wiki/f/results/rtx-5060-dr2-quiescent-full-spectrum/150848-M8_150848/diagnostics/sf_timescales.png" alt="M8_150848: cumulative mass formed against lookback time with t10 to t90">
<figcaption>Mass formed in galaxy M8_150848 against lookback time: t10 4.61, t20 4.21, t50 3.01 Gyr, only a 16-84 percent range.</figcaption>
</figure>

152125-M7_152125
: z 0.7871 · S/N 16.0

<figure>
<img loading="lazy" src="/wiki/f/results/rtx-5060-dr2-quiescent-full-spectrum/152125-M7_152125/diagnostics/photometric_chi2.png" alt="M7_152125: photometric pull and chi-squared contribution per band">
<figcaption>Pull of only the 12 fitted bands of galaxy M7_152125 against the model, 10.82 per band at a 5 percent flux error floor.</figcaption>
</figure>

<figure>
<img loading="lazy" src="/wiki/f/results/rtx-5060-dr2-quiescent-full-spectrum/152125-M7_152125/diagnostics/spectral_chi2.png" alt="M7_152125: spectral pull, binned mean pull squared, cumulative chi-squared">
<figcaption>Pull of only 3608 fitted spectrum pixels of galaxy M7_152125 against the model, 1.099 per pixel at a 6.42 percent error floor.</figcaption>
</figure>

<figure>
<img loading="lazy" src="/wiki/f/results/rtx-5060-dr2-quiescent-full-spectrum/152125-M7_152125/diagnostics/sf_timescales.png" alt="M7_152125: cumulative mass formed against lookback time with t10 to t90">
<figcaption>Mass formed in galaxy M7_152125 against lookback time: t10 4.61, t20 4.21, t50 3.00 Gyr, only a 16-84 percent range.</figcaption>
</figure>

156118-M8_156118
: z 0.8295 · S/N 11.0

<figure>
<img loading="lazy" src="/wiki/f/results/rtx-5060-dr2-quiescent-full-spectrum/156118-M8_156118/diagnostics/photometric_chi2.png" alt="M8_156118: photometric pull and chi-squared contribution per band">
<figcaption>Pull of only the 12 fitted bands of galaxy M8_156118 against the model, 2.69 per band at a 5 percent flux error floor.</figcaption>
</figure>

<figure>
<img loading="lazy" src="/wiki/f/results/rtx-5060-dr2-quiescent-full-spectrum/156118-M8_156118/diagnostics/spectral_chi2.png" alt="M8_156118: spectral pull, binned mean pull squared, cumulative chi-squared">
<figcaption>Pull of only 3409 fitted spectrum pixels of galaxy M8_156118 against the model, 1.157 per pixel at a 5.44 percent error floor.</figcaption>
</figure>

<figure>
<img loading="lazy" src="/wiki/f/results/rtx-5060-dr2-quiescent-full-spectrum/156118-M8_156118/diagnostics/sf_timescales.png" alt="M8_156118: cumulative mass formed against lookback time with t10 to t90">
<figcaption>Mass formed in galaxy M8_156118 against lookback time: t10 4.59, t20 4.12, t50 2.78 Gyr, only a 16-84 percent range.</figcaption>
</figure>

160400-M8_160400
: z 0.6032 · S/N 44.3

<figure>
<img loading="lazy" src="/wiki/f/results/rtx-5060-dr2-quiescent-full-spectrum/160400-M8_160400/diagnostics/photometric_chi2.png" alt="M8_160400: photometric pull and chi-squared contribution per band">
<figcaption>Pull of only the 12 fitted bands of galaxy M8_160400 against the model, 6.07 per band at a 5 percent flux error floor.</figcaption>
</figure>

<figure>
<img loading="lazy" src="/wiki/f/results/rtx-5060-dr2-quiescent-full-spectrum/160400-M8_160400/diagnostics/spectral_chi2.png" alt="M8_160400: spectral pull, binned mean pull squared, cumulative chi-squared">
<figcaption>Pull of only 3558 fitted spectrum pixels of galaxy M8_160400 against the model, 1.082 per pixel at a 4.22 percent error floor.</figcaption>
</figure>

<figure>
<img loading="lazy" src="/wiki/f/results/rtx-5060-dr2-quiescent-full-spectrum/160400-M8_160400/diagnostics/sf_timescales.png" alt="M8_160400: cumulative mass formed against lookback time with t10 to t90">
<figcaption>Mass formed in galaxy M8_160400 against lookback time: t10 4.90, t20 4.47, t50 3.19 Gyr, only a 16-84 percent range.</figcaption>
</figure>

161113-M8_161113
: z 0.8911 · S/N 12.6

<figure>
<img loading="lazy" src="/wiki/f/results/rtx-5060-dr2-quiescent-full-spectrum/161113-M8_161113/diagnostics/photometric_chi2.png" alt="M8_161113: photometric pull and chi-squared contribution per band">
<figcaption>Pull of only the 12 fitted bands of galaxy M8_161113 against the model, 12.55 per band at a 5 percent flux error floor.</figcaption>
</figure>

<figure>
<img loading="lazy" src="/wiki/f/results/rtx-5060-dr2-quiescent-full-spectrum/161113-M8_161113/diagnostics/spectral_chi2.png" alt="M8_161113: spectral pull, binned mean pull squared, cumulative chi-squared">
<figcaption>Pull of only 3799 fitted spectrum pixels of galaxy M8_161113 against the model, 1.087 per pixel at a 5.28 percent error floor.</figcaption>
</figure>

<figure>
<img loading="lazy" src="/wiki/f/results/rtx-5060-dr2-quiescent-full-spectrum/161113-M8_161113/diagnostics/sf_timescales.png" alt="M8_161113: cumulative mass formed against lookback time with t10 to t90">
<figcaption>Mass formed in galaxy M8_161113 against lookback time: t10 5.98, t20 5.65, t50 4.63 Gyr, only a 16-84 percent range.</figcaption>
</figure>

161346-M8_161346
: z 0.6566 · S/N 40.5

<figure>
<img loading="lazy" src="/wiki/f/results/rtx-5060-dr2-quiescent-full-spectrum/161346-M8_161346/diagnostics/photometric_chi2.png" alt="M8_161346: photometric pull and chi-squared contribution per band">
<figcaption>Pull of only the 12 fitted bands of galaxy M8_161346 against the model, 3.91 per band at a 5 percent flux error floor.</figcaption>
</figure>

<figure>
<img loading="lazy" src="/wiki/f/results/rtx-5060-dr2-quiescent-full-spectrum/161346-M8_161346/diagnostics/spectral_chi2.png" alt="M8_161346: spectral pull, binned mean pull squared, cumulative chi-squared">
<figcaption>Pull of only 3447 fitted spectrum pixels of galaxy M8_161346 against the model, 1.126 per pixel at a 4.48 percent error floor.</figcaption>
</figure>

<figure>
<img loading="lazy" src="/wiki/f/results/rtx-5060-dr2-quiescent-full-spectrum/161346-M8_161346/diagnostics/sf_timescales.png" alt="M8_161346: cumulative mass formed against lookback time with t10 to t90">
<figcaption>Mass formed in galaxy M8_161346 against lookback time: t10 6.83, t20 6.11, t50 4.19 Gyr, only a 16-84 percent range.</figcaption>
</figure>

162149-M8_162149
: z 0.7034 · S/N 40.5

<figure>
<img loading="lazy" src="/wiki/f/results/rtx-5060-dr2-quiescent-full-spectrum/162149-M8_162149/diagnostics/photometric_chi2.png" alt="M8_162149: photometric pull and chi-squared contribution per band">
<figcaption>Pull of only the 12 fitted bands of galaxy M8_162149 against the model, 5.84 per band at a 5 percent flux error floor.</figcaption>
</figure>

<figure>
<img loading="lazy" src="/wiki/f/results/rtx-5060-dr2-quiescent-full-spectrum/162149-M8_162149/diagnostics/spectral_chi2.png" alt="M8_162149: spectral pull, binned mean pull squared, cumulative chi-squared">
<figcaption>Pull of only 3494 fitted spectrum pixels of galaxy M8_162149 against the model, 1.077 per pixel at a 3.89 percent error floor.</figcaption>
</figure>

<figure>
<img loading="lazy" src="/wiki/f/results/rtx-5060-dr2-quiescent-full-spectrum/162149-M8_162149/diagnostics/sf_timescales.png" alt="M8_162149: cumulative mass formed against lookback time with t10 to t90">
<figcaption>Mass formed in galaxy M8_162149 against lookback time: t10 6.40, t20 5.52, t50 3.62 Gyr, only a 16-84 percent range.</figcaption>
</figure>

162587-M7_162587
: z 0.7869 · S/N 12.6

<figure>
<img loading="lazy" src="/wiki/f/results/rtx-5060-dr2-quiescent-full-spectrum/162587-M7_162587/diagnostics/photometric_chi2.png" alt="M7_162587: photometric pull and chi-squared contribution per band">
<figcaption>Pull of only the 12 fitted bands of galaxy M7_162587 against the model, 6.68 per band at a 5 percent flux error floor.</figcaption>
</figure>

<figure>
<img loading="lazy" src="/wiki/f/results/rtx-5060-dr2-quiescent-full-spectrum/162587-M7_162587/diagnostics/spectral_chi2.png" alt="M7_162587: spectral pull, binned mean pull squared, cumulative chi-squared">
<figcaption>Pull of only 3544 fitted spectrum pixels of galaxy M7_162587 against the model, 1.263 per pixel at a 9.86 percent error floor.</figcaption>
</figure>

<figure>
<img loading="lazy" src="/wiki/f/results/rtx-5060-dr2-quiescent-full-spectrum/162587-M7_162587/diagnostics/sf_timescales.png" alt="M7_162587: cumulative mass formed against lookback time with t10 to t90">
<figcaption>Mass formed in galaxy M7_162587 against lookback time: t10 4.01, t20 2.99, t50 2.05 Gyr, only a 16-84 percent range.</figcaption>
</figure>

163989-M8_163989
: z 0.7583 · S/N 19.0

<figure>
<img loading="lazy" src="/wiki/f/results/rtx-5060-dr2-quiescent-full-spectrum/163989-M8_163989/diagnostics/photometric_chi2.png" alt="M8_163989: photometric pull and chi-squared contribution per band">
<figcaption>Pull of only the 12 fitted bands of galaxy M8_163989 against the model, 3.13 per band at a 5 percent flux error floor.</figcaption>
</figure>

<figure>
<img loading="lazy" src="/wiki/f/results/rtx-5060-dr2-quiescent-full-spectrum/163989-M8_163989/diagnostics/spectral_chi2.png" alt="M8_163989: spectral pull, binned mean pull squared, cumulative chi-squared">
<figcaption>Pull of only 3618 fitted spectrum pixels of galaxy M8_163989 against the model, 1.092 per pixel at a 5.28 percent error floor.</figcaption>
</figure>

<figure>
<img loading="lazy" src="/wiki/f/results/rtx-5060-dr2-quiescent-full-spectrum/163989-M8_163989/diagnostics/sf_timescales.png" alt="M8_163989: cumulative mass formed against lookback time with t10 to t90">
<figcaption>Mass formed in galaxy M8_163989 against lookback time: t10 4.61, t20 4.21, t50 3.00 Gyr, only a 16-84 percent range.</figcaption>
</figure>

165871-M5_165871
: z 0.7031 · S/N 25.0

<figure>
<img loading="lazy" src="/wiki/f/results/rtx-5060-dr2-quiescent-full-spectrum/165871-M5_165871/diagnostics/photometric_chi2.png" alt="M5_165871: photometric pull and chi-squared contribution per band">
<figcaption>Pull of only the 12 fitted bands of galaxy M5_165871 against the model, 4.76 per band at a 5 percent flux error floor.</figcaption>
</figure>

<figure>
<img loading="lazy" src="/wiki/f/results/rtx-5060-dr2-quiescent-full-spectrum/165871-M5_165871/diagnostics/spectral_chi2.png" alt="M5_165871: spectral pull, binned mean pull squared, cumulative chi-squared">
<figcaption>Pull of only 3460 fitted spectrum pixels of galaxy M5_165871 against the model, 1.099 per pixel at a 4.43 percent error floor.</figcaption>
</figure>

<figure>
<img loading="lazy" src="/wiki/f/results/rtx-5060-dr2-quiescent-full-spectrum/165871-M5_165871/diagnostics/sf_timescales.png" alt="M5_165871: cumulative mass formed against lookback time with t10 to t90">
<figcaption>Mass formed in galaxy M5_165871 against lookback time: t10 4.55, t20 4.08, t50 2.74 Gyr, only a 16-84 percent range.</figcaption>
</figure>

166634-M6_166634
: z 0.8527 · S/N 7.3

<figure>
<img loading="lazy" src="/wiki/f/results/rtx-5060-dr2-quiescent-full-spectrum/166634-M6_166634/diagnostics/photometric_chi2.png" alt="M6_166634: photometric pull and chi-squared contribution per band">
<figcaption>Pull of only the 12 fitted bands of galaxy M6_166634 against the model, 9.27 per band at a 5 percent flux error floor.</figcaption>
</figure>

<figure>
<img loading="lazy" src="/wiki/f/results/rtx-5060-dr2-quiescent-full-spectrum/166634-M6_166634/diagnostics/spectral_chi2.png" alt="M6_166634: spectral pull, binned mean pull squared, cumulative chi-squared">
<figcaption>Pull of only 3518 fitted spectrum pixels of galaxy M6_166634 against the model, 1.125 per pixel at a 9.35 percent error floor.</figcaption>
</figure>

<figure>
<img loading="lazy" src="/wiki/f/results/rtx-5060-dr2-quiescent-full-spectrum/166634-M6_166634/diagnostics/sf_timescales.png" alt="M6_166634: cumulative mass formed against lookback time with t10 to t90">
<figcaption>Mass formed in galaxy M6_166634 against lookback time: t10 6.35, t20 6.20, t50 5.74 Gyr, only a 16-84 percent range.</figcaption>
</figure>

167056-M5_167056
: z 0.8933 · S/N 8.1

<figure>
<img loading="lazy" src="/wiki/f/results/rtx-5060-dr2-quiescent-full-spectrum/167056-M5_167056/diagnostics/photometric_chi2.png" alt="M5_167056: photometric pull and chi-squared contribution per band">
<figcaption>Pull of only the 12 fitted bands of galaxy M5_167056 against the model, 4.04 per band at a 5 percent flux error floor.</figcaption>
</figure>

<figure>
<img loading="lazy" src="/wiki/f/results/rtx-5060-dr2-quiescent-full-spectrum/167056-M5_167056/diagnostics/spectral_chi2.png" alt="M5_167056: spectral pull, binned mean pull squared, cumulative chi-squared">
<figcaption>Pull of only 3796 fitted spectrum pixels of galaxy M5_167056 against the model, 1.071 per pixel at a 5.15 percent error floor.</figcaption>
</figure>

<figure>
<img loading="lazy" src="/wiki/f/results/rtx-5060-dr2-quiescent-full-spectrum/167056-M5_167056/diagnostics/sf_timescales.png" alt="M5_167056: cumulative mass formed against lookback time with t10 to t90">
<figcaption>Mass formed in galaxy M5_167056 against lookback time: t10 5.96, t20 5.61, t50 4.55 Gyr, only a 16-84 percent range.</figcaption>
</figure>

172669-M5_172669
: z 0.6037 · S/N 105.0

<figure>
<img loading="lazy" src="/wiki/f/results/rtx-5060-dr2-quiescent-full-spectrum/172669-M5_172669/diagnostics/photometric_chi2.png" alt="M5_172669: photometric pull and chi-squared contribution per band">
<figcaption>Pull of only the 12 fitted bands of galaxy M5_172669 against the model, 14.14 per band at a 5 percent flux error floor.</figcaption>
</figure>

<figure>
<img loading="lazy" src="/wiki/f/results/rtx-5060-dr2-quiescent-full-spectrum/172669-M5_172669/diagnostics/spectral_chi2.png" alt="M5_172669: spectral pull, binned mean pull squared, cumulative chi-squared">
<figcaption>Pull of only 3602 fitted spectrum pixels of galaxy M5_172669 against the model, 1.062 per pixel at a 2.90 percent error floor.</figcaption>
</figure>

<figure>
<img loading="lazy" src="/wiki/f/results/rtx-5060-dr2-quiescent-full-spectrum/172669-M5_172669/diagnostics/sf_timescales.png" alt="M5_172669: cumulative mass formed against lookback time with t10 to t90">
<figcaption>Mass formed in galaxy M5_172669 against lookback time: t10 2.74, t20 2.47, t50 1.66 Gyr, only a 16-84 percent range.</figcaption>
</figure>

173928-M5_173928
: z 0.9590 · S/N 13.3

<figure>
<img loading="lazy" src="/wiki/f/results/rtx-5060-dr2-quiescent-full-spectrum/173928-M5_173928/diagnostics/photometric_chi2.png" alt="M5_173928: photometric pull and chi-squared contribution per band">
<figcaption>Pull of only the 12 fitted bands of galaxy M5_173928 against the model, 12.07 per band at a 5 percent flux error floor.</figcaption>
</figure>

<figure>
<img loading="lazy" src="/wiki/f/results/rtx-5060-dr2-quiescent-full-spectrum/173928-M5_173928/diagnostics/spectral_chi2.png" alt="M5_173928: spectral pull, binned mean pull squared, cumulative chi-squared">
<figcaption>Pull of only 3836 fitted spectrum pixels of galaxy M5_173928 against the model, 0.946 per pixel at a 9.17 percent error floor.</figcaption>
</figure>

<figure>
<img loading="lazy" src="/wiki/f/results/rtx-5060-dr2-quiescent-full-spectrum/173928-M5_173928/diagnostics/sf_timescales.png" alt="M5_173928: cumulative mass formed against lookback time with t10 to t90">
<figcaption>Mass formed in galaxy M5_173928 against lookback time: t10 4.60, t20 4.18, t50 2.92 Gyr, only a 16-84 percent range.</figcaption>
</figure>

180774-M12_180774
: z 0.6782 · S/N 22.2

<figure>
<img loading="lazy" src="/wiki/f/results/rtx-5060-dr2-quiescent-full-spectrum/180774-M12_180774/diagnostics/photometric_chi2.png" alt="M12_180774: photometric pull and chi-squared contribution per band">
<figcaption>Pull of only the 12 fitted bands of galaxy M12_180774 against the model, 3.50 per band at a 5 percent flux error floor.</figcaption>
</figure>

<figure>
<img loading="lazy" src="/wiki/f/results/rtx-5060-dr2-quiescent-full-spectrum/180774-M12_180774/diagnostics/spectral_chi2.png" alt="M12_180774: spectral pull, binned mean pull squared, cumulative chi-squared">
<figcaption>Pull of only 3384 fitted spectrum pixels of galaxy M12_180774 against the model, 1.202 per pixel at a 7.39 percent error floor.</figcaption>
</figure>

<figure>
<img loading="lazy" src="/wiki/f/results/rtx-5060-dr2-quiescent-full-spectrum/180774-M12_180774/diagnostics/sf_timescales.png" alt="M12_180774: cumulative mass formed against lookback time with t10 to t90">
<figcaption>Mass formed in galaxy M12_180774 against lookback time: t10 6.77, t20 6.12, t50 4.05 Gyr, only a 16-84 percent range.</figcaption>
</figure>

181421-M12_181421
: z 0.9585 · S/N 11.3

<figure>
<img loading="lazy" src="/wiki/f/results/rtx-5060-dr2-quiescent-full-spectrum/181421-M12_181421/diagnostics/photometric_chi2.png" alt="M12_181421: photometric pull and chi-squared contribution per band">
<figcaption>Pull of only the 12 fitted bands of galaxy M12_181421 against the model, 4.03 per band at a 5 percent flux error floor.</figcaption>
</figure>

<figure>
<img loading="lazy" src="/wiki/f/results/rtx-5060-dr2-quiescent-full-spectrum/181421-M12_181421/diagnostics/spectral_chi2.png" alt="M12_181421: spectral pull, binned mean pull squared, cumulative chi-squared">
<figcaption>Pull of only 3800 fitted spectrum pixels of galaxy M12_181421 against the model, 1.158 per pixel at a 9.38 percent error floor.</figcaption>
</figure>

<figure>
<img loading="lazy" src="/wiki/f/results/rtx-5060-dr2-quiescent-full-spectrum/181421-M12_181421/diagnostics/sf_timescales.png" alt="M12_181421: cumulative mass formed against lookback time with t10 to t90">
<figcaption>Mass formed in galaxy M12_181421 against lookback time: t10 5.52, t20 5.02, t50 3.96 Gyr, only a 16-84 percent range.</figcaption>
</figure>

181945-M12_181945
: z 0.6795 · S/N 61.8

<figure>
<img loading="lazy" src="/wiki/f/results/rtx-5060-dr2-quiescent-full-spectrum/181945-M12_181945/diagnostics/photometric_chi2.png" alt="M12_181945: photometric pull and chi-squared contribution per band">
<figcaption>Pull of only the 12 fitted bands of galaxy M12_181945 against the model, 13.06 per band at a 5 percent flux error floor.</figcaption>
</figure>

<figure>
<img loading="lazy" src="/wiki/f/results/rtx-5060-dr2-quiescent-full-spectrum/181945-M12_181945/diagnostics/spectral_chi2.png" alt="M12_181945: spectral pull, binned mean pull squared, cumulative chi-squared">
<figcaption>Pull of only 3432 fitted spectrum pixels of galaxy M12_181945 against the model, 1.089 per pixel at a 4.24 percent error floor.</figcaption>
</figure>

<figure>
<img loading="lazy" src="/wiki/f/results/rtx-5060-dr2-quiescent-full-spectrum/181945-M12_181945/diagnostics/sf_timescales.png" alt="M12_181945: cumulative mass formed against lookback time with t10 to t90">
<figcaption>Mass formed in galaxy M12_181945 against lookback time: t10 4.53, t20 4.05, t50 2.69 Gyr, only a 16-84 percent range.</figcaption>
</figure>

182890-M12_182890
: z 0.7444 · S/N 16.8

<figure>
<img loading="lazy" src="/wiki/f/results/rtx-5060-dr2-quiescent-full-spectrum/182890-M12_182890/diagnostics/photometric_chi2.png" alt="M12_182890: photometric pull and chi-squared contribution per band">
<figcaption>Pull of only the 12 fitted bands of galaxy M12_182890 against the model, 9.89 per band at a 5 percent flux error floor.</figcaption>
</figure>

<figure>
<img loading="lazy" src="/wiki/f/results/rtx-5060-dr2-quiescent-full-spectrum/182890-M12_182890/diagnostics/spectral_chi2.png" alt="M12_182890: spectral pull, binned mean pull squared, cumulative chi-squared">
<figcaption>Pull of only 3569 fitted spectrum pixels of galaxy M12_182890 against the model, 1.188 per pixel at a 6.02 percent error floor.</figcaption>
</figure>

<figure>
<img loading="lazy" src="/wiki/f/results/rtx-5060-dr2-quiescent-full-spectrum/182890-M12_182890/diagnostics/sf_timescales.png" alt="M12_182890: cumulative mass formed against lookback time with t10 to t90">
<figcaption>Mass formed in galaxy M12_182890 against lookback time: t10 6.25, t20 5.44, t50 3.90 Gyr, only a 16-84 percent range.</figcaption>
</figure>

184916-M12_184916
: z 0.6794 · S/N 30.4

<figure>
<img loading="lazy" src="/wiki/f/results/rtx-5060-dr2-quiescent-full-spectrum/184916-M12_184916/diagnostics/photometric_chi2.png" alt="M12_184916: photometric pull and chi-squared contribution per band">
<figcaption>Pull of only the 12 fitted bands of galaxy M12_184916 against the model, 6.59 per band at a 5 percent flux error floor.</figcaption>
</figure>

<figure>
<img loading="lazy" src="/wiki/f/results/rtx-5060-dr2-quiescent-full-spectrum/184916-M12_184916/diagnostics/spectral_chi2.png" alt="M12_184916: spectral pull, binned mean pull squared, cumulative chi-squared">
<figcaption>Pull of only 3583 fitted spectrum pixels of galaxy M12_184916 against the model, 1.066 per pixel at a 9.59 percent error floor.</figcaption>
</figure>

<figure>
<img loading="lazy" src="/wiki/f/results/rtx-5060-dr2-quiescent-full-spectrum/184916-M12_184916/diagnostics/sf_timescales.png" alt="M12_184916: cumulative mass formed against lookback time with t10 to t90">
<figcaption>Mass formed in galaxy M12_184916 against lookback time: t10 7.16, t20 6.91, t50 6.15 Gyr, only a 16-84 percent range.</figcaption>
</figure>

185631-M12_185631
: z 0.9253 · S/N 4.9

<figure>
<img loading="lazy" src="/wiki/f/results/rtx-5060-dr2-quiescent-full-spectrum/185631-M12_185631/diagnostics/photometric_chi2.png" alt="M12_185631: photometric pull and chi-squared contribution per band">
<figcaption>Pull of only the 12 fitted bands of galaxy M12_185631 against the model, 1.99 per band at a 5 percent flux error floor.</figcaption>
</figure>

<figure>
<img loading="lazy" src="/wiki/f/results/rtx-5060-dr2-quiescent-full-spectrum/185631-M12_185631/diagnostics/spectral_chi2.png" alt="M12_185631: spectral pull, binned mean pull squared, cumulative chi-squared">
<figcaption>Pull of only 3840 fitted spectrum pixels of galaxy M12_185631 against the model, 1.804 per pixel at a 9.99 percent error floor.</figcaption>
</figure>

<figure>
<img loading="lazy" src="/wiki/f/results/rtx-5060-dr2-quiescent-full-spectrum/185631-M12_185631/diagnostics/sf_timescales.png" alt="M12_185631: cumulative mass formed against lookback time with t10 to t90">
<figcaption>Mass formed in galaxy M12_185631 against lookback time: t10 4.66, t20 4.16, t50 2.76 Gyr, only a 16-84 percent range.</figcaption>
</figure>

185653-M12_185653
: z 0.6776 · S/N 21.5

<figure>
<img loading="lazy" src="/wiki/f/results/rtx-5060-dr2-quiescent-full-spectrum/185653-M12_185653/diagnostics/photometric_chi2.png" alt="M12_185653: photometric pull and chi-squared contribution per band">
<figcaption>Pull of only the 12 fitted bands of galaxy M12_185653 against the model, 3.05 per band at a 5 percent flux error floor.</figcaption>
</figure>

<figure>
<img loading="lazy" src="/wiki/f/results/rtx-5060-dr2-quiescent-full-spectrum/185653-M12_185653/diagnostics/spectral_chi2.png" alt="M12_185653: spectral pull, binned mean pull squared, cumulative chi-squared">
<figcaption>Pull of only 3577 fitted spectrum pixels of galaxy M12_185653 against the model, 1.124 per pixel at a 6.44 percent error floor.</figcaption>
</figure>

<figure>
<img loading="lazy" src="/wiki/f/results/rtx-5060-dr2-quiescent-full-spectrum/185653-M12_185653/diagnostics/sf_timescales.png" alt="M12_185653: cumulative mass formed against lookback time with t10 to t90">
<figcaption>Mass formed in galaxy M12_185653 against lookback time: t10 4.63, t20 4.22, t50 3.01 Gyr, only a 16-84 percent range.</figcaption>
</figure>

189698-M10_189698
: z 0.9258 · S/N 7.2

<figure>
<img loading="lazy" src="/wiki/f/results/rtx-5060-dr2-quiescent-full-spectrum/189698-M10_189698/diagnostics/photometric_chi2.png" alt="M10_189698: photometric pull and chi-squared contribution per band">
<figcaption>Pull of only the 12 fitted bands of galaxy M10_189698 against the model, 4.75 per band at a 5 percent flux error floor.</figcaption>
</figure>

<figure>
<img loading="lazy" src="/wiki/f/results/rtx-5060-dr2-quiescent-full-spectrum/189698-M10_189698/diagnostics/spectral_chi2.png" alt="M10_189698: spectral pull, binned mean pull squared, cumulative chi-squared">
<figcaption>Pull of only 3675 fitted spectrum pixels of galaxy M10_189698 against the model, 1.040 per pixel at a 2.30 percent error floor.</figcaption>
</figure>

<figure>
<img loading="lazy" src="/wiki/f/results/rtx-5060-dr2-quiescent-full-spectrum/189698-M10_189698/diagnostics/sf_timescales.png" alt="M10_189698: cumulative mass formed against lookback time with t10 to t90">
<figcaption>Mass formed in galaxy M10_189698 against lookback time: t10 5.40, t20 4.82, t50 3.63 Gyr, only a 16-84 percent range.</figcaption>
</figure>

191718-M10_191718
: z 0.9840 · S/N 6.8

<figure>
<img loading="lazy" src="/wiki/f/results/rtx-5060-dr2-quiescent-full-spectrum/191718-M10_191718/diagnostics/photometric_chi2.png" alt="M10_191718: photometric pull and chi-squared contribution per band">
<figcaption>Pull of only the 12 fitted bands of galaxy M10_191718 against the model, 6.29 per band at a 5 percent flux error floor.</figcaption>
</figure>

<figure>
<img loading="lazy" src="/wiki/f/results/rtx-5060-dr2-quiescent-full-spectrum/191718-M10_191718/diagnostics/spectral_chi2.png" alt="M10_191718: spectral pull, binned mean pull squared, cumulative chi-squared">
<figcaption>Pull of only 3789 fitted spectrum pixels of galaxy M10_191718 against the model, 0.929 per pixel at a 6.39 percent error floor.</figcaption>
</figure>

<figure>
<img loading="lazy" src="/wiki/f/results/rtx-5060-dr2-quiescent-full-spectrum/191718-M10_191718/diagnostics/sf_timescales.png" alt="M10_191718: cumulative mass formed against lookback time with t10 to t90">
<figcaption>Mass formed in galaxy M10_191718 against lookback time: t10 4.64, t20 4.24, t50 3.03 Gyr, only a 16-84 percent range.</figcaption>
</figure>

197591-M10_197591
: z 0.7960 · S/N 23.9

<figure>
<img loading="lazy" src="/wiki/f/results/rtx-5060-dr2-quiescent-full-spectrum/197591-M10_197591/diagnostics/photometric_chi2.png" alt="M10_197591: photometric pull and chi-squared contribution per band">
<figcaption>Pull of only the 12 fitted bands of galaxy M10_197591 against the model, 9.19 per band at a 5 percent flux error floor.</figcaption>
</figure>

<figure>
<img loading="lazy" src="/wiki/f/results/rtx-5060-dr2-quiescent-full-spectrum/197591-M10_197591/diagnostics/spectral_chi2.png" alt="M10_197591: spectral pull, binned mean pull squared, cumulative chi-squared">
<figcaption>Pull of only 3789 fitted spectrum pixels of galaxy M10_197591 against the model, 1.055 per pixel at a 4.66 percent error floor.</figcaption>
</figure>

<figure>
<img loading="lazy" src="/wiki/f/results/rtx-5060-dr2-quiescent-full-spectrum/197591-M10_197591/diagnostics/sf_timescales.png" alt="M10_197591: cumulative mass formed against lookback time with t10 to t90">
<figcaption>Mass formed in galaxy M10_197591 against lookback time: t10 4.63, t20 4.23, t50 3.02 Gyr, only a 16-84 percent range.</figcaption>
</figure>

201233-M10_201233
: z 0.8177 · S/N 9.3

<figure>
<img loading="lazy" src="/wiki/f/results/rtx-5060-dr2-quiescent-full-spectrum/201233-M10_201233/diagnostics/photometric_chi2.png" alt="M10_201233: photometric pull and chi-squared contribution per band">
<figcaption>Pull of only the 12 fitted bands of galaxy M10_201233 against the model, 3.63 per band at a 5 percent flux error floor.</figcaption>
</figure>

<figure>
<img loading="lazy" src="/wiki/f/results/rtx-5060-dr2-quiescent-full-spectrum/201233-M10_201233/diagnostics/spectral_chi2.png" alt="M10_201233: spectral pull, binned mean pull squared, cumulative chi-squared">
<figcaption>Pull of only 3809 fitted spectrum pixels of galaxy M10_201233 against the model, 1.062 per pixel at a 4.16 percent error floor.</figcaption>
</figure>

<figure>
<img loading="lazy" src="/wiki/f/results/rtx-5060-dr2-quiescent-full-spectrum/201233-M10_201233/diagnostics/sf_timescales.png" alt="M10_201233: cumulative mass formed against lookback time with t10 to t90">
<figcaption>Mass formed in galaxy M10_201233 against lookback time: t10 4.63, t20 4.22, t50 3.02 Gyr, only a 16-84 percent range.</figcaption>
</figure>

205715-M5_205715
: z 0.7465 · S/N 33.2

<figure>
<img loading="lazy" src="/wiki/f/results/rtx-5060-dr2-quiescent-full-spectrum/205715-M5_205715/diagnostics/photometric_chi2.png" alt="M5_205715: photometric pull and chi-squared contribution per band">
<figcaption>Pull of only the 12 fitted bands of galaxy M5_205715 against the model, 5.29 per band at a 5 percent flux error floor.</figcaption>
</figure>

<figure>
<img loading="lazy" src="/wiki/f/results/rtx-5060-dr2-quiescent-full-spectrum/205715-M5_205715/diagnostics/spectral_chi2.png" alt="M5_205715: spectral pull, binned mean pull squared, cumulative chi-squared">
<figcaption>Pull of only 3411 fitted spectrum pixels of galaxy M5_205715 against the model, 1.147 per pixel at a 4.53 percent error floor.</figcaption>
</figure>

<figure>
<img loading="lazy" src="/wiki/f/results/rtx-5060-dr2-quiescent-full-spectrum/205715-M5_205715/diagnostics/sf_timescales.png" alt="M5_205715: cumulative mass formed against lookback time with t10 to t90">
<figcaption>Mass formed in galaxy M5_205715 against lookback time: t10 4.63, t20 4.23, t50 3.02 Gyr, only a 16-84 percent range.</figcaption>
</figure>

205742-M1_205742
: z 0.7273 · S/N 42.8

<figure>
<img loading="lazy" src="/wiki/f/results/rtx-5060-dr2-quiescent-full-spectrum/205742-M1_205742/diagnostics/photometric_chi2.png" alt="M1_205742: photometric pull and chi-squared contribution per band">
<figcaption>Pull of only the 12 fitted bands of galaxy M1_205742 against the model, 14.80 per band at a 5 percent flux error floor.</figcaption>
</figure>

<figure>
<img loading="lazy" src="/wiki/f/results/rtx-5060-dr2-quiescent-full-spectrum/205742-M1_205742/diagnostics/spectral_chi2.png" alt="M1_205742: spectral pull, binned mean pull squared, cumulative chi-squared">
<figcaption>Pull of only 3523 fitted spectrum pixels of galaxy M1_205742 against the model, 1.158 per pixel at a 3.87 percent error floor.</figcaption>
</figure>

<figure>
<img loading="lazy" src="/wiki/f/results/rtx-5060-dr2-quiescent-full-spectrum/205742-M1_205742/diagnostics/sf_timescales.png" alt="M1_205742: cumulative mass formed against lookback time with t10 to t90">
<figcaption>Mass formed in galaxy M1_205742 against lookback time: t10 6.52, t20 5.91, t50 4.37 Gyr, only a 16-84 percent range.</figcaption>
</figure>

205765-M5_205765
: z 0.7287 · S/N 14.3

<figure>
<img loading="lazy" src="/wiki/f/results/rtx-5060-dr2-quiescent-full-spectrum/205765-M5_205765/diagnostics/photometric_chi2.png" alt="M5_205765: photometric pull and chi-squared contribution per band">
<figcaption>Pull of only the 12 fitted bands of galaxy M5_205765 against the model, 25.62 per band at a 5 percent flux error floor.</figcaption>
</figure>

<figure>
<img loading="lazy" src="/wiki/f/results/rtx-5060-dr2-quiescent-full-spectrum/205765-M5_205765/diagnostics/spectral_chi2.png" alt="M5_205765: spectral pull, binned mean pull squared, cumulative chi-squared">
<figcaption>Pull of only 3504 fitted spectrum pixels of galaxy M5_205765 against the model, 1.040 per pixel at a 4.82 percent error floor.</figcaption>
</figure>

<figure>
<img loading="lazy" src="/wiki/f/results/rtx-5060-dr2-quiescent-full-spectrum/205765-M5_205765/diagnostics/sf_timescales.png" alt="M5_205765: cumulative mass formed against lookback time with t10 to t90">
<figcaption>Mass formed in galaxy M5_205765 against lookback time: t10 5.73, t20 4.80, t50 3.58 Gyr, only a 16-84 percent range.</figcaption>
</figure>

206501-M1_206501
: z 0.9262 · S/N 30.5

<figure>
<img loading="lazy" src="/wiki/f/results/rtx-5060-dr2-quiescent-full-spectrum/206501-M1_206501/diagnostics/photometric_chi2.png" alt="M1_206501: photometric pull and chi-squared contribution per band">
<figcaption>Pull of only the 12 fitted bands of galaxy M1_206501 against the model, 22.94 per band at a 5 percent flux error floor.</figcaption>
</figure>

<figure>
<img loading="lazy" src="/wiki/f/results/rtx-5060-dr2-quiescent-full-spectrum/206501-M1_206501/diagnostics/spectral_chi2.png" alt="M1_206501: spectral pull, binned mean pull squared, cumulative chi-squared">
<figcaption>Pull of only 3830 fitted spectrum pixels of galaxy M1_206501 against the model, 1.145 per pixel at a 5.43 percent error floor.</figcaption>
</figure>

<figure>
<img loading="lazy" src="/wiki/f/results/rtx-5060-dr2-quiescent-full-spectrum/206501-M1_206501/diagnostics/sf_timescales.png" alt="M1_206501: cumulative mass formed against lookback time with t10 to t90">
<figcaption>Mass formed in galaxy M1_206501 against lookback time: t10 5.85, t20 5.53, t50 4.57 Gyr, only a 16-84 percent range.</figcaption>
</figure>

206545-M1_206545
: z 0.7283 · S/N 31.4

<figure>
<img loading="lazy" src="/wiki/f/results/rtx-5060-dr2-quiescent-full-spectrum/206545-M1_206545/diagnostics/photometric_chi2.png" alt="M1_206545: photometric pull and chi-squared contribution per band">
<figcaption>Pull of only the 12 fitted bands of galaxy M1_206545 against the model, 11.09 per band at a 5 percent flux error floor.</figcaption>
</figure>

<figure>
<img loading="lazy" src="/wiki/f/results/rtx-5060-dr2-quiescent-full-spectrum/206545-M1_206545/diagnostics/spectral_chi2.png" alt="M1_206545: spectral pull, binned mean pull squared, cumulative chi-squared">
<figcaption>Pull of only 3422 fitted spectrum pixels of galaxy M1_206545 against the model, 1.286 per pixel at a 5.71 percent error floor.</figcaption>
</figure>

<figure>
<img loading="lazy" src="/wiki/f/results/rtx-5060-dr2-quiescent-full-spectrum/206545-M1_206545/diagnostics/sf_timescales.png" alt="M1_206545: cumulative mass formed against lookback time with t10 to t90">
<figcaption>Mass formed in galaxy M1_206545 against lookback time: t10 4.60, t20 4.18, t50 2.92 Gyr, only a 16-84 percent range.</figcaption>
</figure>

206669-M2_206669
: z 0.6716 · S/N 35.2

<figure>
<img loading="lazy" src="/wiki/f/results/rtx-5060-dr2-quiescent-full-spectrum/206669-M2_206669/diagnostics/photometric_chi2.png" alt="M2_206669: photometric pull and chi-squared contribution per band">
<figcaption>Pull of only the 12 fitted bands of galaxy M2_206669 against the model, 7.69 per band at a 5 percent flux error floor.</figcaption>
</figure>

<figure>
<img loading="lazy" src="/wiki/f/results/rtx-5060-dr2-quiescent-full-spectrum/206669-M2_206669/diagnostics/spectral_chi2.png" alt="M2_206669: spectral pull, binned mean pull squared, cumulative chi-squared">
<figcaption>Pull of only 3594 fitted spectrum pixels of galaxy M2_206669 against the model, 1.084 per pixel at a 3.57 percent error floor.</figcaption>
</figure>

<figure>
<img loading="lazy" src="/wiki/f/results/rtx-5060-dr2-quiescent-full-spectrum/206669-M2_206669/diagnostics/sf_timescales.png" alt="M2_206669: cumulative mass formed against lookback time with t10 to t90">
<figcaption>Mass formed in galaxy M2_206669 against lookback time: t10 6.32, t20 5.17, t50 3.74 Gyr, only a 16-84 percent range.</figcaption>
</figure>

206771-M5_206771
: z 0.6295 · S/N 12.3

<figure>
<img loading="lazy" src="/wiki/f/results/rtx-5060-dr2-quiescent-full-spectrum/206771-M5_206771/diagnostics/photometric_chi2.png" alt="M5_206771: photometric pull and chi-squared contribution per band">
<figcaption>Pull of only the 12 fitted bands of galaxy M5_206771 against the model, 2.90 per band at a 5 percent flux error floor.</figcaption>
</figure>

<figure>
<img loading="lazy" src="/wiki/f/results/rtx-5060-dr2-quiescent-full-spectrum/206771-M5_206771/diagnostics/spectral_chi2.png" alt="M5_206771: spectral pull, binned mean pull squared, cumulative chi-squared">
<figcaption>Pull of only 3571 fitted spectrum pixels of galaxy M5_206771 against the model, 1.150 per pixel at a 6.66 percent error floor.</figcaption>
</figure>

<figure>
<img loading="lazy" src="/wiki/f/results/rtx-5060-dr2-quiescent-full-spectrum/206771-M5_206771/diagnostics/sf_timescales.png" alt="M5_206771: cumulative mass formed against lookback time with t10 to t90">
<figcaption>Mass formed in galaxy M5_206771 against lookback time: t10 7.25, t20 6.77, t50 5.36 Gyr, only a 16-84 percent range.</figcaption>
</figure>

206858-M1_206858
: z 0.7248 · S/N 33.4

<figure>
<img loading="lazy" src="/wiki/f/results/rtx-5060-dr2-quiescent-full-spectrum/206858-M1_206858/diagnostics/photometric_chi2.png" alt="M1_206858: photometric pull and chi-squared contribution per band">
<figcaption>Pull of only the 12 fitted bands of galaxy M1_206858 against the model, 5.23 per band at a 5 percent flux error floor.</figcaption>
</figure>

<figure>
<img loading="lazy" src="/wiki/f/results/rtx-5060-dr2-quiescent-full-spectrum/206858-M1_206858/diagnostics/spectral_chi2.png" alt="M1_206858: spectral pull, binned mean pull squared, cumulative chi-squared">
<figcaption>Pull of only 3545 fitted spectrum pixels of galaxy M1_206858 against the model, 1.120 per pixel at a 4.35 percent error floor.</figcaption>
</figure>

<figure>
<img loading="lazy" src="/wiki/f/results/rtx-5060-dr2-quiescent-full-spectrum/206858-M1_206858/diagnostics/sf_timescales.png" alt="M1_206858: cumulative mass formed against lookback time with t10 to t90">
<figcaption>Mass formed in galaxy M1_206858 against lookback time: t10 2.74, t20 2.46, t50 1.65 Gyr, only a 16-84 percent range.</figcaption>
</figure>

208364-M2_208364
: z 0.6678 · S/N 25.1

<figure>
<img loading="lazy" src="/wiki/f/results/rtx-5060-dr2-quiescent-full-spectrum/208364-M2_208364/diagnostics/photometric_chi2.png" alt="M2_208364: photometric pull and chi-squared contribution per band">
<figcaption>Pull of only the 12 fitted bands of galaxy M2_208364 against the model, 5.45 per band at a 5 percent flux error floor.</figcaption>
</figure>

<figure>
<img loading="lazy" src="/wiki/f/results/rtx-5060-dr2-quiescent-full-spectrum/208364-M2_208364/diagnostics/spectral_chi2.png" alt="M2_208364: spectral pull, binned mean pull squared, cumulative chi-squared">
<figcaption>Pull of only 3581 fitted spectrum pixels of galaxy M2_208364 against the model, 1.050 per pixel at a 2.84 percent error floor.</figcaption>
</figure>

<figure>
<img loading="lazy" src="/wiki/f/results/rtx-5060-dr2-quiescent-full-spectrum/208364-M2_208364/diagnostics/sf_timescales.png" alt="M2_208364: cumulative mass formed against lookback time with t10 to t90">
<figcaption>Mass formed in galaxy M2_208364 against lookback time: t10 4.59, t20 4.15, t50 2.85 Gyr, only a 16-84 percent range.</figcaption>
</figure>

208622-M1_208622
: z 0.6479 · S/N 17.9

<figure>
<img loading="lazy" src="/wiki/f/results/rtx-5060-dr2-quiescent-full-spectrum/208622-M1_208622/diagnostics/photometric_chi2.png" alt="M1_208622: photometric pull and chi-squared contribution per band">
<figcaption>Pull of only the 12 fitted bands of galaxy M1_208622 against the model, 5.28 per band at a 5 percent flux error floor.</figcaption>
</figure>

<figure>
<img loading="lazy" src="/wiki/f/results/rtx-5060-dr2-quiescent-full-spectrum/208622-M1_208622/diagnostics/spectral_chi2.png" alt="M1_208622: spectral pull, binned mean pull squared, cumulative chi-squared">
<figcaption>Pull of only 3541 fitted spectrum pixels of galaxy M1_208622 against the model, 1.137 per pixel at a 4.07 percent error floor.</figcaption>
</figure>

<figure>
<img loading="lazy" src="/wiki/f/results/rtx-5060-dr2-quiescent-full-spectrum/208622-M1_208622/diagnostics/sf_timescales.png" alt="M1_208622: cumulative mass formed against lookback time with t10 to t90">
<figcaption>Mass formed in galaxy M1_208622 against lookback time: t10 4.63, t20 4.22, t50 3.01 Gyr, only a 16-84 percent range.</figcaption>
</figure>

210210-M1_210210
: z 0.6542 · S/N 62.2

<figure>
<img loading="lazy" src="/wiki/f/results/rtx-5060-dr2-quiescent-full-spectrum/210210-M1_210210/diagnostics/photometric_chi2.png" alt="M1_210210: photometric pull and chi-squared contribution per band">
<figcaption>Pull of only the 12 fitted bands of galaxy M1_210210 against the model, 9.68 per band at a 5 percent flux error floor.</figcaption>
</figure>

<figure>
<img loading="lazy" src="/wiki/f/results/rtx-5060-dr2-quiescent-full-spectrum/210210-M1_210210/diagnostics/spectral_chi2.png" alt="M1_210210: spectral pull, binned mean pull squared, cumulative chi-squared">
<figcaption>Pull of only 3523 fitted spectrum pixels of galaxy M1_210210 against the model, 1.112 per pixel at a 4.62 percent error floor.</figcaption>
</figure>

<figure>
<img loading="lazy" src="/wiki/f/results/rtx-5060-dr2-quiescent-full-spectrum/210210-M1_210210/diagnostics/sf_timescales.png" alt="M1_210210: cumulative mass formed against lookback time with t10 to t90">
<figcaption>Mass formed in galaxy M1_210210 against lookback time: t10 6.99, t20 6.42, t50 4.68 Gyr, only a 16-84 percent range.</figcaption>
</figure>

210940-M2_210940
: z 0.6949 · S/N 13.7

<figure>
<img loading="lazy" src="/wiki/f/results/rtx-5060-dr2-quiescent-full-spectrum/210940-M2_210940/diagnostics/photometric_chi2.png" alt="M2_210940: photometric pull and chi-squared contribution per band">
<figcaption>Pull of only the 12 fitted bands of galaxy M2_210940 against the model, 7.21 per band at a 5 percent flux error floor.</figcaption>
</figure>

<figure>
<img loading="lazy" src="/wiki/f/results/rtx-5060-dr2-quiescent-full-spectrum/210940-M2_210940/diagnostics/spectral_chi2.png" alt="M2_210940: spectral pull, binned mean pull squared, cumulative chi-squared">
<figcaption>Pull of only 3577 fitted spectrum pixels of galaxy M2_210940 against the model, 0.946 per pixel at a 4.07 percent error floor.</figcaption>
</figure>

<figure>
<img loading="lazy" src="/wiki/f/results/rtx-5060-dr2-quiescent-full-spectrum/210940-M2_210940/diagnostics/sf_timescales.png" alt="M2_210940: cumulative mass formed against lookback time with t10 to t90">
<figcaption>Mass formed in galaxy M2_210940 against lookback time: t10 4.77, t20 4.32, t50 2.98 Gyr, only a 16-84 percent range.</figcaption>
</figure>

211157-M1_211157
: z 0.6070 · S/N 35.1

<figure>
<img loading="lazy" src="/wiki/f/results/rtx-5060-dr2-quiescent-full-spectrum/211157-M1_211157/diagnostics/photometric_chi2.png" alt="M1_211157: photometric pull and chi-squared contribution per band">
<figcaption>Pull of only the 12 fitted bands of galaxy M1_211157 against the model, 7.30 per band at a 5 percent flux error floor.</figcaption>
</figure>

<figure>
<img loading="lazy" src="/wiki/f/results/rtx-5060-dr2-quiescent-full-spectrum/211157-M1_211157/diagnostics/spectral_chi2.png" alt="M1_211157: spectral pull, binned mean pull squared, cumulative chi-squared">
<figcaption>Pull of only 3567 fitted spectrum pixels of galaxy M1_211157 against the model, 1.214 per pixel at a 4.80 percent error floor.</figcaption>
</figure>

<figure>
<img loading="lazy" src="/wiki/f/results/rtx-5060-dr2-quiescent-full-spectrum/211157-M1_211157/diagnostics/sf_timescales.png" alt="M1_211157: cumulative mass formed against lookback time with t10 to t90">
<figcaption>Mass formed in galaxy M1_211157 against lookback time: t10 6.75, t20 5.64, t50 3.70 Gyr, only a 16-84 percent range.</figcaption>
</figure>

211347-M5_211347
: z 0.6972 · S/N 29.2

<figure>
<img loading="lazy" src="/wiki/f/results/rtx-5060-dr2-quiescent-full-spectrum/211347-M5_211347/diagnostics/photometric_chi2.png" alt="M5_211347: photometric pull and chi-squared contribution per band">
<figcaption>Pull of only the 12 fitted bands of galaxy M5_211347 against the model, 9.29 per band at a 5 percent flux error floor.</figcaption>
</figure>

<figure>
<img loading="lazy" src="/wiki/f/results/rtx-5060-dr2-quiescent-full-spectrum/211347-M5_211347/diagnostics/spectral_chi2.png" alt="M5_211347: spectral pull, binned mean pull squared, cumulative chi-squared">
<figcaption>Pull of only 3413 fitted spectrum pixels of galaxy M5_211347 against the model, 1.143 per pixel at a 4.06 percent error floor.</figcaption>
</figure>

<figure>
<img loading="lazy" src="/wiki/f/results/rtx-5060-dr2-quiescent-full-spectrum/211347-M5_211347/diagnostics/sf_timescales.png" alt="M5_211347: cumulative mass formed against lookback time with t10 to t90">
<figcaption>Mass formed in galaxy M5_211347 against lookback time: t10 4.62, t20 4.20, t50 2.96 Gyr, only a 16-84 percent range.</figcaption>
</figure>

211767-M5_211767
: z 0.6674 · S/N 28.5

<figure>
<img loading="lazy" src="/wiki/f/results/rtx-5060-dr2-quiescent-full-spectrum/211767-M5_211767/diagnostics/photometric_chi2.png" alt="M5_211767: photometric pull and chi-squared contribution per band">
<figcaption>Pull of only the 12 fitted bands of galaxy M5_211767 against the model, 13.01 per band at a 5 percent flux error floor.</figcaption>
</figure>

<figure>
<img loading="lazy" src="/wiki/f/results/rtx-5060-dr2-quiescent-full-spectrum/211767-M5_211767/diagnostics/spectral_chi2.png" alt="M5_211767: spectral pull, binned mean pull squared, cumulative chi-squared">
<figcaption>Pull of only 3386 fitted spectrum pixels of galaxy M5_211767 against the model, 1.066 per pixel at a 4.19 percent error floor.</figcaption>
</figure>

<figure>
<img loading="lazy" src="/wiki/f/results/rtx-5060-dr2-quiescent-full-spectrum/211767-M5_211767/diagnostics/sf_timescales.png" alt="M5_211767: cumulative mass formed against lookback time with t10 to t90">
<figcaption>Mass formed in galaxy M5_211767 against lookback time: t10 4.63, t20 4.23, t50 3.02 Gyr, only a 16-84 percent range.</figcaption>
</figure>

212391-M9_212391
: z 0.7263 · S/N 19.6

<figure>
<img loading="lazy" src="/wiki/f/results/rtx-5060-dr2-quiescent-full-spectrum/212391-M9_212391/diagnostics/photometric_chi2.png" alt="M9_212391: photometric pull and chi-squared contribution per band">
<figcaption>Pull of only the 12 fitted bands of galaxy M9_212391 against the model, 2.45 per band at a 5 percent flux error floor.</figcaption>
</figure>

<figure>
<img loading="lazy" src="/wiki/f/results/rtx-5060-dr2-quiescent-full-spectrum/212391-M9_212391/diagnostics/spectral_chi2.png" alt="M9_212391: spectral pull, binned mean pull squared, cumulative chi-squared">
<figcaption>Pull of only 3557 fitted spectrum pixels of galaxy M9_212391 against the model, 1.109 per pixel at a 3.90 percent error floor.</figcaption>
</figure>

<figure>
<img loading="lazy" src="/wiki/f/results/rtx-5060-dr2-quiescent-full-spectrum/212391-M9_212391/diagnostics/sf_timescales.png" alt="M9_212391: cumulative mass formed against lookback time with t10 to t90">
<figcaption>Mass formed in galaxy M9_212391 against lookback time: t10 4.61, t20 4.20, t50 2.97 Gyr, only a 16-84 percent range.</figcaption>
</figure>

212718-M11_212718
: z 0.8898 · S/N 11.5

<figure>
<img loading="lazy" src="/wiki/f/results/rtx-5060-dr2-quiescent-full-spectrum/212718-M11_212718/diagnostics/photometric_chi2.png" alt="M11_212718: photometric pull and chi-squared contribution per band">
<figcaption>Pull of only the 12 fitted bands of galaxy M11_212718 against the model, 10.58 per band at a 5 percent flux error floor.</figcaption>
</figure>

<figure>
<img loading="lazy" src="/wiki/f/results/rtx-5060-dr2-quiescent-full-spectrum/212718-M11_212718/diagnostics/spectral_chi2.png" alt="M11_212718: spectral pull, binned mean pull squared, cumulative chi-squared">
<figcaption>Pull of only 3794 fitted spectrum pixels of galaxy M11_212718 against the model, 1.110 per pixel at a 5.40 percent error floor.</figcaption>
</figure>

<figure>
<img loading="lazy" src="/wiki/f/results/rtx-5060-dr2-quiescent-full-spectrum/212718-M11_212718/diagnostics/sf_timescales.png" alt="M11_212718: cumulative mass formed against lookback time with t10 to t90">
<figcaption>Mass formed in galaxy M11_212718 against lookback time: t10 5.99, t20 5.65, t50 4.63 Gyr, only a 16-84 percent range.</figcaption>
</figure>

213004-M11_213004
: z 0.7465 · S/N 39.4

<figure>
<img loading="lazy" src="/wiki/f/results/rtx-5060-dr2-quiescent-full-spectrum/213004-M11_213004/diagnostics/photometric_chi2.png" alt="M11_213004: photometric pull and chi-squared contribution per band">
<figcaption>Pull of only the 12 fitted bands of galaxy M11_213004 against the model, 18.37 per band at a 5 percent flux error floor.</figcaption>
</figure>

<figure>
<img loading="lazy" src="/wiki/f/results/rtx-5060-dr2-quiescent-full-spectrum/213004-M11_213004/diagnostics/spectral_chi2.png" alt="M11_213004: spectral pull, binned mean pull squared, cumulative chi-squared">
<figcaption>Pull of only 3439 fitted spectrum pixels of galaxy M11_213004 against the model, 1.125 per pixel at a 4.57 percent error floor.</figcaption>
</figure>

<figure>
<img loading="lazy" src="/wiki/f/results/rtx-5060-dr2-quiescent-full-spectrum/213004-M11_213004/diagnostics/sf_timescales.png" alt="M11_213004: cumulative mass formed against lookback time with t10 to t90">
<figcaption>Mass formed in galaxy M11_213004 against lookback time: t10 4.63, t20 4.22, t50 3.02 Gyr, only a 16-84 percent range.</figcaption>
</figure>

213587-M9_213587
: z 0.8900 · S/N 27.1

<figure>
<img loading="lazy" src="/wiki/f/results/rtx-5060-dr2-quiescent-full-spectrum/213587-M9_213587/diagnostics/photometric_chi2.png" alt="M9_213587: photometric pull and chi-squared contribution per band">
<figcaption>Pull of only the 12 fitted bands of galaxy M9_213587 against the model, 10.11 per band at a 5 percent flux error floor.</figcaption>
</figure>

<figure>
<img loading="lazy" src="/wiki/f/results/rtx-5060-dr2-quiescent-full-spectrum/213587-M9_213587/diagnostics/spectral_chi2.png" alt="M9_213587: spectral pull, binned mean pull squared, cumulative chi-squared">
<figcaption>Pull of only 3738 fitted spectrum pixels of galaxy M9_213587 against the model, 1.101 per pixel at a 4.06 percent error floor.</figcaption>
</figure>

<figure>
<img loading="lazy" src="/wiki/f/results/rtx-5060-dr2-quiescent-full-spectrum/213587-M9_213587/diagnostics/sf_timescales.png" alt="M9_213587: cumulative mass formed against lookback time with t10 to t90">
<figcaption>Mass formed in galaxy M9_213587 against lookback time: t10 4.61, t20 4.21, t50 3.01 Gyr, only a 16-84 percent range.</figcaption>
</figure>

213772-M10_213772
: z 0.7004 · S/N 40.9

<figure>
<img loading="lazy" src="/wiki/f/results/rtx-5060-dr2-quiescent-full-spectrum/213772-M10_213772/diagnostics/photometric_chi2.png" alt="M10_213772: photometric pull and chi-squared contribution per band">
<figcaption>Pull of only the 12 fitted bands of galaxy M10_213772 against the model, 7.96 per band at a 5 percent flux error floor.</figcaption>
</figure>

<figure>
<img loading="lazy" src="/wiki/f/results/rtx-5060-dr2-quiescent-full-spectrum/213772-M10_213772/diagnostics/spectral_chi2.png" alt="M10_213772: spectral pull, binned mean pull squared, cumulative chi-squared">
<figcaption>Pull of only 3565 fitted spectrum pixels of galaxy M10_213772 against the model, 1.028 per pixel at a 4.86 percent error floor.</figcaption>
</figure>

<figure>
<img loading="lazy" src="/wiki/f/results/rtx-5060-dr2-quiescent-full-spectrum/213772-M10_213772/diagnostics/sf_timescales.png" alt="M10_213772: cumulative mass formed against lookback time with t10 to t90">
<figcaption>Mass formed in galaxy M10_213772 against lookback time: t10 7.03, t20 6.76, t50 5.96 Gyr, only a 16-84 percent range.</figcaption>
</figure>

214296-M11_214296
: z 0.6797 · S/N 19.1

<figure>
<img loading="lazy" src="/wiki/f/results/rtx-5060-dr2-quiescent-full-spectrum/214296-M11_214296/diagnostics/photometric_chi2.png" alt="M11_214296: photometric pull and chi-squared contribution per band">
<figcaption>Pull of only the 12 fitted bands of galaxy M11_214296 against the model, 13.10 per band at a 5 percent flux error floor.</figcaption>
</figure>

<figure>
<img loading="lazy" src="/wiki/f/results/rtx-5060-dr2-quiescent-full-spectrum/214296-M11_214296/diagnostics/spectral_chi2.png" alt="M11_214296: spectral pull, binned mean pull squared, cumulative chi-squared">
<figcaption>Pull of only 3427 fitted spectrum pixels of galaxy M11_214296 against the model, 1.122 per pixel at a 4.69 percent error floor.</figcaption>
</figure>

<figure>
<img loading="lazy" src="/wiki/f/results/rtx-5060-dr2-quiescent-full-spectrum/214296-M11_214296/diagnostics/sf_timescales.png" alt="M11_214296: cumulative mass formed against lookback time with t10 to t90">
<figcaption>Mass formed in galaxy M11_214296 against lookback time: t10 4.34, t20 3.60, t50 2.27 Gyr, only a 16-84 percent range.</figcaption>
</figure>

214430-M11_214430
: z 0.8911 · S/N 15.2

<figure>
<img loading="lazy" src="/wiki/f/results/rtx-5060-dr2-quiescent-full-spectrum/214430-M11_214430/diagnostics/photometric_chi2.png" alt="M11_214430: photometric pull and chi-squared contribution per band">
<figcaption>Pull of only the 12 fitted bands of galaxy M11_214430 against the model, 17.47 per band at a 5 percent flux error floor.</figcaption>
</figure>

<figure>
<img loading="lazy" src="/wiki/f/results/rtx-5060-dr2-quiescent-full-spectrum/214430-M11_214430/diagnostics/spectral_chi2.png" alt="M11_214430: spectral pull, binned mean pull squared, cumulative chi-squared">
<figcaption>Pull of only 3810 fitted spectrum pixels of galaxy M11_214430 against the model, 1.162 per pixel at a 5.23 percent error floor.</figcaption>
</figure>

<figure>
<img loading="lazy" src="/wiki/f/results/rtx-5060-dr2-quiescent-full-spectrum/214430-M11_214430/diagnostics/sf_timescales.png" alt="M11_214430: cumulative mass formed against lookback time with t10 to t90">
<figcaption>Mass formed in galaxy M11_214430 against lookback time: t10 5.79, t20 5.26, t50 4.09 Gyr, only a 16-84 percent range.</figcaption>
</figure>

214899-M9_214899
: z 0.6751 · S/N 18.8

<figure>
<img loading="lazy" src="/wiki/f/results/rtx-5060-dr2-quiescent-full-spectrum/214899-M9_214899/diagnostics/photometric_chi2.png" alt="M9_214899: photometric pull and chi-squared contribution per band">
<figcaption>Pull of only the 12 fitted bands of galaxy M9_214899 against the model, 2.03 per band at a 5 percent flux error floor.</figcaption>
</figure>

<figure>
<img loading="lazy" src="/wiki/f/results/rtx-5060-dr2-quiescent-full-spectrum/214899-M9_214899/diagnostics/spectral_chi2.png" alt="M9_214899: spectral pull, binned mean pull squared, cumulative chi-squared">
<figcaption>Pull of only 3493 fitted spectrum pixels of galaxy M9_214899 against the model, 1.084 per pixel at a 3.92 percent error floor.</figcaption>
</figure>

<figure>
<img loading="lazy" src="/wiki/f/results/rtx-5060-dr2-quiescent-full-spectrum/214899-M9_214899/diagnostics/sf_timescales.png" alt="M9_214899: cumulative mass formed against lookback time with t10 to t90">
<figcaption>Mass formed in galaxy M9_214899 against lookback time: t10 4.61, t20 4.19, t50 2.92 Gyr, only a 16-84 percent range.</figcaption>
</figure>

215519-M10_215519
: z 0.6146 · S/N 17.7

<figure>
<img loading="lazy" src="/wiki/f/results/rtx-5060-dr2-quiescent-full-spectrum/215519-M10_215519/diagnostics/photometric_chi2.png" alt="M10_215519: photometric pull and chi-squared contribution per band">
<figcaption>Pull of only the 12 fitted bands of galaxy M10_215519 against the model, 1.97 per band at a 5 percent flux error floor.</figcaption>
</figure>

<figure>
<img loading="lazy" src="/wiki/f/results/rtx-5060-dr2-quiescent-full-spectrum/215519-M10_215519/diagnostics/spectral_chi2.png" alt="M10_215519: spectral pull, binned mean pull squared, cumulative chi-squared">
<figcaption>Pull of only 3575 fitted spectrum pixels of galaxy M10_215519 against the model, 1.023 per pixel at a 4.44 percent error floor.</figcaption>
</figure>

<figure>
<img loading="lazy" src="/wiki/f/results/rtx-5060-dr2-quiescent-full-spectrum/215519-M10_215519/diagnostics/sf_timescales.png" alt="M10_215519: cumulative mass formed against lookback time with t10 to t90">
<figcaption>Mass formed in galaxy M10_215519 against lookback time: t10 7.52, t20 7.22, t50 6.34 Gyr, only a 16-84 percent range.</figcaption>
</figure>

215585-M11_215585
: z 0.7487 · S/N 35.6

<figure>
<img loading="lazy" src="/wiki/f/results/rtx-5060-dr2-quiescent-full-spectrum/215585-M11_215585/diagnostics/photometric_chi2.png" alt="M11_215585: photometric pull and chi-squared contribution per band">
<figcaption>Pull of only the 12 fitted bands of galaxy M11_215585 against the model, 17.50 per band at a 5 percent flux error floor.</figcaption>
</figure>

<figure>
<img loading="lazy" src="/wiki/f/results/rtx-5060-dr2-quiescent-full-spectrum/215585-M11_215585/diagnostics/spectral_chi2.png" alt="M11_215585: spectral pull, binned mean pull squared, cumulative chi-squared">
<figcaption>Pull of only 3757 fitted spectrum pixels of galaxy M11_215585 against the model, 1.145 per pixel at a 4.65 percent error floor.</figcaption>
</figure>

<figure>
<img loading="lazy" src="/wiki/f/results/rtx-5060-dr2-quiescent-full-spectrum/215585-M11_215585/diagnostics/sf_timescales.png" alt="M11_215585: cumulative mass formed against lookback time with t10 to t90">
<figcaption>Mass formed in galaxy M11_215585 against lookback time: t10 6.56, t20 6.09, t50 4.73 Gyr, only a 16-84 percent range.</figcaption>
</figure>

216730-M10_216730
: z 0.8937 · S/N 36.7

<figure>
<img loading="lazy" src="/wiki/f/results/rtx-5060-dr2-quiescent-full-spectrum/216730-M10_216730/diagnostics/photometric_chi2.png" alt="M10_216730: photometric pull and chi-squared contribution per band">
<figcaption>Pull of only the 12 fitted bands of galaxy M10_216730 against the model, 3.34 per band at a 5 percent flux error floor.</figcaption>
</figure>

<figure>
<img loading="lazy" src="/wiki/f/results/rtx-5060-dr2-quiescent-full-spectrum/216730-M10_216730/diagnostics/spectral_chi2.png" alt="M10_216730: spectral pull, binned mean pull squared, cumulative chi-squared">
<figcaption>Pull of only 3418 fitted spectrum pixels of galaxy M10_216730 against the model, 1.039 per pixel at a 6.22 percent error floor.</figcaption>
</figure>

<figure>
<img loading="lazy" src="/wiki/f/results/rtx-5060-dr2-quiescent-full-spectrum/216730-M10_216730/diagnostics/sf_timescales.png" alt="M10_216730: cumulative mass formed against lookback time with t10 to t90">
<figcaption>Mass formed in galaxy M10_216730 against lookback time: t10 2.73, t20 2.46, t50 1.65 Gyr, only a 16-84 percent range.</figcaption>
</figure>

216899-M11_216899
: z 0.6978 · S/N 21.1

<figure>
<img loading="lazy" src="/wiki/f/results/rtx-5060-dr2-quiescent-full-spectrum/216899-M11_216899/diagnostics/photometric_chi2.png" alt="M11_216899: photometric pull and chi-squared contribution per band">
<figcaption>Pull of only the 12 fitted bands of galaxy M11_216899 against the model, 3.75 per band at a 5 percent flux error floor.</figcaption>
</figure>

<figure>
<img loading="lazy" src="/wiki/f/results/rtx-5060-dr2-quiescent-full-spectrum/216899-M11_216899/diagnostics/spectral_chi2.png" alt="M11_216899: spectral pull, binned mean pull squared, cumulative chi-squared">
<figcaption>Pull of only 3430 fitted spectrum pixels of galaxy M11_216899 against the model, 1.713 per pixel at a 9.99 percent error floor.</figcaption>
</figure>

<figure>
<img loading="lazy" src="/wiki/f/results/rtx-5060-dr2-quiescent-full-spectrum/216899-M11_216899/diagnostics/sf_timescales.png" alt="M11_216899: cumulative mass formed against lookback time with t10 to t90">
<figcaption>Mass formed in galaxy M11_216899 against lookback time: t10 6.74, t20 6.16, t50 4.58 Gyr, only a 16-84 percent range.</figcaption>
</figure>

217020-M10_217020
: z 0.8934 · S/N 12.8

<figure>
<img loading="lazy" src="/wiki/f/results/rtx-5060-dr2-quiescent-full-spectrum/217020-M10_217020/diagnostics/photometric_chi2.png" alt="M10_217020: photometric pull and chi-squared contribution per band">
<figcaption>Pull of only the 12 fitted bands of galaxy M10_217020 against the model, 8.48 per band at a 5 percent flux error floor.</figcaption>
</figure>

<figure>
<img loading="lazy" src="/wiki/f/results/rtx-5060-dr2-quiescent-full-spectrum/217020-M10_217020/diagnostics/spectral_chi2.png" alt="M10_217020: spectral pull, binned mean pull squared, cumulative chi-squared">
<figcaption>Pull of only 3443 fitted spectrum pixels of galaxy M10_217020 against the model, 1.025 per pixel at a 6.80 percent error floor.</figcaption>
</figure>

<figure>
<img loading="lazy" src="/wiki/f/results/rtx-5060-dr2-quiescent-full-spectrum/217020-M10_217020/diagnostics/sf_timescales.png" alt="M10_217020: cumulative mass formed against lookback time with t10 to t90">
<figcaption>Mass formed in galaxy M10_217020 against lookback time: t10 4.55, t20 4.06, t50 2.69 Gyr, only a 16-84 percent range.</figcaption>
</figure>

217564-M11_217564
: z 0.8899 · S/N 3.7

<figure>
<img loading="lazy" src="/wiki/f/results/rtx-5060-dr2-quiescent-full-spectrum/217564-M11_217564/diagnostics/photometric_chi2.png" alt="M11_217564: photometric pull and chi-squared contribution per band">
<figcaption>Pull of only the 12 fitted bands of galaxy M11_217564 against the model, 11.80 per band at a 5 percent flux error floor.</figcaption>
</figure>

<figure>
<img loading="lazy" src="/wiki/f/results/rtx-5060-dr2-quiescent-full-spectrum/217564-M11_217564/diagnostics/spectral_chi2.png" alt="M11_217564: spectral pull, binned mean pull squared, cumulative chi-squared">
<figcaption>Pull of only 3827 fitted spectrum pixels of galaxy M11_217564 against the model, 1.132 per pixel at a 9.13 percent error floor.</figcaption>
</figure>

<figure>
<img loading="lazy" src="/wiki/f/results/rtx-5060-dr2-quiescent-full-spectrum/217564-M11_217564/diagnostics/sf_timescales.png" alt="M11_217564: cumulative mass formed against lookback time with t10 to t90">
<figcaption>Mass formed in galaxy M11_217564 against lookback time: t10 4.66, t20 4.22, t50 2.94 Gyr, only a 16-84 percent range.</figcaption>
</figure>

218207-M11_218207
: z 0.6818 · S/N 36.8

<figure>
<img loading="lazy" src="/wiki/f/results/rtx-5060-dr2-quiescent-full-spectrum/218207-M11_218207/diagnostics/photometric_chi2.png" alt="M11_218207: photometric pull and chi-squared contribution per band">
<figcaption>Pull of only the 12 fitted bands of galaxy M11_218207 against the model, 16.41 per band at a 5 percent flux error floor.</figcaption>
</figure>

<figure>
<img loading="lazy" src="/wiki/f/results/rtx-5060-dr2-quiescent-full-spectrum/218207-M11_218207/diagnostics/spectral_chi2.png" alt="M11_218207: spectral pull, binned mean pull squared, cumulative chi-squared">
<figcaption>Pull of only 3424 fitted spectrum pixels of galaxy M11_218207 against the model, 1.081 per pixel at a 5.64 percent error floor.</figcaption>
</figure>

<figure>
<img loading="lazy" src="/wiki/f/results/rtx-5060-dr2-quiescent-full-spectrum/218207-M11_218207/diagnostics/sf_timescales.png" alt="M11_218207: cumulative mass formed against lookback time with t10 to t90">
<figcaption>Mass formed in galaxy M11_218207 against lookback time: t10 4.62, t20 4.21, t50 3.01 Gyr, only a 16-84 percent range.</figcaption>
</figure>

218701-M9_218701
: z 0.6953 · S/N 30.7

<figure>
<img loading="lazy" src="/wiki/f/results/rtx-5060-dr2-quiescent-full-spectrum/218701-M9_218701/diagnostics/photometric_chi2.png" alt="M9_218701: photometric pull and chi-squared contribution per band">
<figcaption>Pull of only the 12 fitted bands of galaxy M9_218701 against the model, 3.01 per band at a 5 percent flux error floor.</figcaption>
</figure>

<figure>
<img loading="lazy" src="/wiki/f/results/rtx-5060-dr2-quiescent-full-spectrum/218701-M9_218701/diagnostics/spectral_chi2.png" alt="M9_218701: spectral pull, binned mean pull squared, cumulative chi-squared">
<figcaption>Pull of only 3580 fitted spectrum pixels of galaxy M9_218701 against the model, 1.120 per pixel at a 3.43 percent error floor.</figcaption>
</figure>

<figure>
<img loading="lazy" src="/wiki/f/results/rtx-5060-dr2-quiescent-full-spectrum/218701-M9_218701/diagnostics/sf_timescales.png" alt="M9_218701: cumulative mass formed against lookback time with t10 to t90">
<figcaption>Mass formed in galaxy M9_218701 against lookback time: t10 4.52, t20 4.00, t50 2.60 Gyr, only a 16-84 percent range.</figcaption>
</figure>

221163-M11_221163
: z 0.6975 · S/N 34.2

<figure>
<img loading="lazy" src="/wiki/f/results/rtx-5060-dr2-quiescent-full-spectrum/221163-M11_221163/diagnostics/photometric_chi2.png" alt="M11_221163: photometric pull and chi-squared contribution per band">
<figcaption>Pull of only the 12 fitted bands of galaxy M11_221163 against the model, 22.98 per band at a 5 percent flux error floor.</figcaption>
</figure>

<figure>
<img loading="lazy" src="/wiki/f/results/rtx-5060-dr2-quiescent-full-spectrum/221163-M11_221163/diagnostics/spectral_chi2.png" alt="M11_221163: spectral pull, binned mean pull squared, cumulative chi-squared">
<figcaption>Pull of only 3615 fitted spectrum pixels of galaxy M11_221163 against the model, 1.106 per pixel at a 4.84 percent error floor.</figcaption>
</figure>

<figure>
<img loading="lazy" src="/wiki/f/results/rtx-5060-dr2-quiescent-full-spectrum/221163-M11_221163/diagnostics/sf_timescales.png" alt="M11_221163: cumulative mass formed against lookback time with t10 to t90">
<figcaption>Mass formed in galaxy M11_221163 against lookback time: t10 6.41, t20 5.52, t50 3.90 Gyr, only a 16-84 percent range.</figcaption>
</figure>

225431-M9_225431
: z 0.7014 · S/N 19.9

<figure>
<img loading="lazy" src="/wiki/f/results/rtx-5060-dr2-quiescent-full-spectrum/225431-M9_225431/diagnostics/photometric_chi2.png" alt="M9_225431: photometric pull and chi-squared contribution per band">
<figcaption>Pull of only the 12 fitted bands of galaxy M9_225431 against the model, 4.37 per band at a 5 percent flux error floor.</figcaption>
</figure>

<figure>
<img loading="lazy" src="/wiki/f/results/rtx-5060-dr2-quiescent-full-spectrum/225431-M9_225431/diagnostics/spectral_chi2.png" alt="M9_225431: spectral pull, binned mean pull squared, cumulative chi-squared">
<figcaption>Pull of only 3439 fitted spectrum pixels of galaxy M9_225431 against the model, 1.081 per pixel at a 4.54 percent error floor.</figcaption>
</figure>

<figure>
<img loading="lazy" src="/wiki/f/results/rtx-5060-dr2-quiescent-full-spectrum/225431-M9_225431/diagnostics/sf_timescales.png" alt="M9_225431: cumulative mass formed against lookback time with t10 to t90">
<figcaption>Mass formed in galaxy M9_225431 against lookback time: t10 4.81, t20 4.39, t50 3.09 Gyr, only a 16-84 percent range.</figcaption>
</figure>

225441-M10_225441
: z 0.6823 · S/N 28.9

<figure>
<img loading="lazy" src="/wiki/f/results/rtx-5060-dr2-quiescent-full-spectrum/225441-M10_225441/diagnostics/photometric_chi2.png" alt="M10_225441: photometric pull and chi-squared contribution per band">
<figcaption>Pull of only the 12 fitted bands of galaxy M10_225441 against the model, 1.59 per band at a 5 percent flux error floor.</figcaption>
</figure>

<figure>
<img loading="lazy" src="/wiki/f/results/rtx-5060-dr2-quiescent-full-spectrum/225441-M10_225441/diagnostics/spectral_chi2.png" alt="M10_225441: spectral pull, binned mean pull squared, cumulative chi-squared">
<figcaption>Pull of only 3535 fitted spectrum pixels of galaxy M10_225441 against the model, 1.069 per pixel at a 4.38 percent error floor.</figcaption>
</figure>

<figure>
<img loading="lazy" src="/wiki/f/results/rtx-5060-dr2-quiescent-full-spectrum/225441-M10_225441/diagnostics/sf_timescales.png" alt="M10_225441: cumulative mass formed against lookback time with t10 to t90">
<figcaption>Mass formed in galaxy M10_225441 against lookback time: t10 2.74, t20 2.47, t50 1.65 Gyr, only a 16-84 percent range.</figcaption>
</figure>

225678-M9_225678
: z 0.7326 · S/N 12.3

<figure>
<img loading="lazy" src="/wiki/f/results/rtx-5060-dr2-quiescent-full-spectrum/225678-M9_225678/diagnostics/photometric_chi2.png" alt="M9_225678: photometric pull and chi-squared contribution per band">
<figcaption>Pull of only the 12 fitted bands of galaxy M9_225678 against the model, 6.49 per band at a 5 percent flux error floor.</figcaption>
</figure>

<figure>
<img loading="lazy" src="/wiki/f/results/rtx-5060-dr2-quiescent-full-spectrum/225678-M9_225678/diagnostics/spectral_chi2.png" alt="M9_225678: spectral pull, binned mean pull squared, cumulative chi-squared">
<figcaption>Pull of only 3441 fitted spectrum pixels of galaxy M9_225678 against the model, 1.170 per pixel at a 4.55 percent error floor.</figcaption>
</figure>

<figure>
<img loading="lazy" src="/wiki/f/results/rtx-5060-dr2-quiescent-full-spectrum/225678-M9_225678/diagnostics/sf_timescales.png" alt="M9_225678: cumulative mass formed against lookback time with t10 to t90">
<figcaption>Mass formed in galaxy M9_225678 against lookback time: t10 6.70, t20 6.29, t50 5.06 Gyr, only a 16-84 percent range.</figcaption>
</figure>

226316-M9_226316
: z 0.6088 · S/N 51.5

<figure>
<img loading="lazy" src="/wiki/f/results/rtx-5060-dr2-quiescent-full-spectrum/226316-M9_226316/diagnostics/photometric_chi2.png" alt="M9_226316: photometric pull and chi-squared contribution per band">
<figcaption>Pull of only the 12 fitted bands of galaxy M9_226316 against the model, 8.81 per band at a 5 percent flux error floor.</figcaption>
</figure>

<figure>
<img loading="lazy" src="/wiki/f/results/rtx-5060-dr2-quiescent-full-spectrum/226316-M9_226316/diagnostics/spectral_chi2.png" alt="M9_226316: spectral pull, binned mean pull squared, cumulative chi-squared">
<figcaption>Pull of only 3585 fitted spectrum pixels of galaxy M9_226316 against the model, 1.033 per pixel at a 3.35 percent error floor.</figcaption>
</figure>

<figure>
<img loading="lazy" src="/wiki/f/results/rtx-5060-dr2-quiescent-full-spectrum/226316-M9_226316/diagnostics/sf_timescales.png" alt="M9_226316: cumulative mass formed against lookback time with t10 to t90">
<figcaption>Mass formed in galaxy M9_226316 against lookback time: t10 7.55, t20 7.26, t50 6.38 Gyr, only a 16-84 percent range.</figcaption>
</figure>

226721-M11_226721
: z 0.7373 · S/N 29.0

<figure>
<img loading="lazy" src="/wiki/f/results/rtx-5060-dr2-quiescent-full-spectrum/226721-M11_226721/diagnostics/photometric_chi2.png" alt="M11_226721: photometric pull and chi-squared contribution per band">
<figcaption>Pull of only the 12 fitted bands of galaxy M11_226721 against the model, 3.37 per band at a 5 percent flux error floor.</figcaption>
</figure>

<figure>
<img loading="lazy" src="/wiki/f/results/rtx-5060-dr2-quiescent-full-spectrum/226721-M11_226721/diagnostics/spectral_chi2.png" alt="M11_226721: spectral pull, binned mean pull squared, cumulative chi-squared">
<figcaption>Pull of only 3405 fitted spectrum pixels of galaxy M11_226721 against the model, 1.132 per pixel at a 4.88 percent error floor.</figcaption>
</figure>

<figure>
<img loading="lazy" src="/wiki/f/results/rtx-5060-dr2-quiescent-full-spectrum/226721-M11_226721/diagnostics/sf_timescales.png" alt="M11_226721: cumulative mass formed against lookback time with t10 to t90">
<figcaption>Mass formed in galaxy M11_226721 against lookback time: t10 5.83, t20 4.84, t50 3.40 Gyr, only a 16-84 percent range.</figcaption>
</figure>

227516-M10_227516
: z 0.7792 · S/N 29.2

<figure>
<img loading="lazy" src="/wiki/f/results/rtx-5060-dr2-quiescent-full-spectrum/227516-M10_227516/diagnostics/photometric_chi2.png" alt="M10_227516: photometric pull and chi-squared contribution per band">
<figcaption>Pull of only the 12 fitted bands of galaxy M10_227516 against the model, 10.54 per band at a 5 percent flux error floor.</figcaption>
</figure>

<figure>
<img loading="lazy" src="/wiki/f/results/rtx-5060-dr2-quiescent-full-spectrum/227516-M10_227516/diagnostics/spectral_chi2.png" alt="M10_227516: spectral pull, binned mean pull squared, cumulative chi-squared">
<figcaption>Pull of only 3686 fitted spectrum pixels of galaxy M10_227516 against the model, 1.077 per pixel at a 4.77 percent error floor.</figcaption>
</figure>

<figure>
<img loading="lazy" src="/wiki/f/results/rtx-5060-dr2-quiescent-full-spectrum/227516-M10_227516/diagnostics/sf_timescales.png" alt="M10_227516: cumulative mass formed against lookback time with t10 to t90">
<figcaption>Mass formed in galaxy M10_227516 against lookback time: t10 6.41, t20 5.96, t50 4.65 Gyr, only a 16-84 percent range.</figcaption>
</figure>

227630-M9_227630
: z 0.7296 · S/N 19.1

<figure>
<img loading="lazy" src="/wiki/f/results/rtx-5060-dr2-quiescent-full-spectrum/227630-M9_227630/diagnostics/photometric_chi2.png" alt="M9_227630: photometric pull and chi-squared contribution per band">
<figcaption>Pull of only the 12 fitted bands of galaxy M9_227630 against the model, 4.00 per band at a 5 percent flux error floor.</figcaption>
</figure>

<figure>
<img loading="lazy" src="/wiki/f/results/rtx-5060-dr2-quiescent-full-spectrum/227630-M9_227630/diagnostics/spectral_chi2.png" alt="M9_227630: spectral pull, binned mean pull squared, cumulative chi-squared">
<figcaption>Pull of only 3490 fitted spectrum pixels of galaxy M9_227630 against the model, 1.119 per pixel at a 3.93 percent error floor.</figcaption>
</figure>

<figure>
<img loading="lazy" src="/wiki/f/results/rtx-5060-dr2-quiescent-full-spectrum/227630-M9_227630/diagnostics/sf_timescales.png" alt="M9_227630: cumulative mass formed against lookback time with t10 to t90">
<figcaption>Mass formed in galaxy M9_227630 against lookback time: t10 4.65, t20 4.23, t50 3.00 Gyr, only a 16-84 percent range.</figcaption>
</figure>

227672-M10_227672
: z 0.6093 · S/N 19.3

<figure>
<img loading="lazy" src="/wiki/f/results/rtx-5060-dr2-quiescent-full-spectrum/227672-M10_227672/diagnostics/photometric_chi2.png" alt="M10_227672: photometric pull and chi-squared contribution per band">
<figcaption>Pull of only the 12 fitted bands of galaxy M10_227672 against the model, 8.49 per band at a 5 percent flux error floor.</figcaption>
</figure>

<figure>
<img loading="lazy" src="/wiki/f/results/rtx-5060-dr2-quiescent-full-spectrum/227672-M10_227672/diagnostics/spectral_chi2.png" alt="M10_227672: spectral pull, binned mean pull squared, cumulative chi-squared">
<figcaption>Pull of only 3555 fitted spectrum pixels of galaxy M10_227672 against the model, 1.048 per pixel at a 2.97 percent error floor.</figcaption>
</figure>

<figure>
<img loading="lazy" src="/wiki/f/results/rtx-5060-dr2-quiescent-full-spectrum/227672-M10_227672/diagnostics/sf_timescales.png" alt="M10_227672: cumulative mass formed against lookback time with t10 to t90">
<figcaption>Mass formed in galaxy M10_227672 against lookback time: t10 4.62, t20 4.22, t50 3.01 Gyr, only a 16-84 percent range.</figcaption>
</figure>

228215-M10_228215
: z 0.6109 · S/N 36.8

<figure>
<img loading="lazy" src="/wiki/f/results/rtx-5060-dr2-quiescent-full-spectrum/228215-M10_228215/diagnostics/photometric_chi2.png" alt="M10_228215: photometric pull and chi-squared contribution per band">
<figcaption>Pull of only the 12 fitted bands of galaxy M10_228215 against the model, 9.45 per band at a 5 percent flux error floor.</figcaption>
</figure>

<figure>
<img loading="lazy" src="/wiki/f/results/rtx-5060-dr2-quiescent-full-spectrum/228215-M10_228215/diagnostics/spectral_chi2.png" alt="M10_228215: spectral pull, binned mean pull squared, cumulative chi-squared">
<figcaption>Pull of only 3559 fitted spectrum pixels of galaxy M10_228215 against the model, 1.125 per pixel at a 2.90 percent error floor.</figcaption>
</figure>

<figure>
<img loading="lazy" src="/wiki/f/results/rtx-5060-dr2-quiescent-full-spectrum/228215-M10_228215/diagnostics/sf_timescales.png" alt="M10_228215: cumulative mass formed against lookback time with t10 to t90">
<figcaption>Mass formed in galaxy M10_228215 against lookback time: t10 4.97, t20 4.54, t50 3.27 Gyr, only a 16-84 percent range.</figcaption>
</figure>

228380-M10_228380
: z 0.6114 · S/N 36.1

<figure>
<img loading="lazy" src="/wiki/f/results/rtx-5060-dr2-quiescent-full-spectrum/228380-M10_228380/diagnostics/photometric_chi2.png" alt="M10_228380: photometric pull and chi-squared contribution per band">
<figcaption>Pull of only the 12 fitted bands of galaxy M10_228380 against the model, 28.77 per band at a 5 percent flux error floor.</figcaption>
</figure>

<figure>
<img loading="lazy" src="/wiki/f/results/rtx-5060-dr2-quiescent-full-spectrum/228380-M10_228380/diagnostics/spectral_chi2.png" alt="M10_228380: spectral pull, binned mean pull squared, cumulative chi-squared">
<figcaption>Pull of only 3568 fitted spectrum pixels of galaxy M10_228380 against the model, 1.133 per pixel at a 3.25 percent error floor.</figcaption>
</figure>

<figure>
<img loading="lazy" src="/wiki/f/results/rtx-5060-dr2-quiescent-full-spectrum/228380-M10_228380/diagnostics/sf_timescales.png" alt="M10_228380: cumulative mass formed against lookback time with t10 to t90">
<figcaption>Mass formed in galaxy M10_228380 against lookback time: t10 4.62, t20 4.22, t50 3.01 Gyr, only a 16-84 percent range.</figcaption>
</figure>

228717-M10_228717
: z 0.9399 · S/N 14.3

<figure>
<img loading="lazy" src="/wiki/f/results/rtx-5060-dr2-quiescent-full-spectrum/228717-M10_228717/diagnostics/photometric_chi2.png" alt="M10_228717: photometric pull and chi-squared contribution per band">
<figcaption>Pull of only the 12 fitted bands of galaxy M10_228717 against the model, 16.42 per band at a 5 percent flux error floor.</figcaption>
</figure>

<figure>
<img loading="lazy" src="/wiki/f/results/rtx-5060-dr2-quiescent-full-spectrum/228717-M10_228717/diagnostics/spectral_chi2.png" alt="M10_228717: spectral pull, binned mean pull squared, cumulative chi-squared">
<figcaption>Pull of only 3835 fitted spectrum pixels of galaxy M10_228717 against the model, 0.976 per pixel at a 6.45 percent error floor.</figcaption>
</figure>

<figure>
<img loading="lazy" src="/wiki/f/results/rtx-5060-dr2-quiescent-full-spectrum/228717-M10_228717/diagnostics/sf_timescales.png" alt="M10_228717: cumulative mass formed against lookback time with t10 to t90">
<figcaption>Mass formed in galaxy M10_228717 against lookback time: t10 5.82, t20 5.54, t50 4.59 Gyr, only a 16-84 percent range.</figcaption>
</figure>

229551-M11_229551
: z 0.6958 · S/N 32.8

<figure>
<img loading="lazy" src="/wiki/f/results/rtx-5060-dr2-quiescent-full-spectrum/229551-M11_229551/diagnostics/photometric_chi2.png" alt="M11_229551: photometric pull and chi-squared contribution per band">
<figcaption>Pull of only the 12 fitted bands of galaxy M11_229551 against the model, 8.28 per band at a 5 percent flux error floor.</figcaption>
</figure>

<figure>
<img loading="lazy" src="/wiki/f/results/rtx-5060-dr2-quiescent-full-spectrum/229551-M11_229551/diagnostics/spectral_chi2.png" alt="M11_229551: spectral pull, binned mean pull squared, cumulative chi-squared">
<figcaption>Pull of only 3463 fitted spectrum pixels of galaxy M11_229551 against the model, 1.109 per pixel at a 4.70 percent error floor.</figcaption>
</figure>

<figure>
<img loading="lazy" src="/wiki/f/results/rtx-5060-dr2-quiescent-full-spectrum/229551-M11_229551/diagnostics/sf_timescales.png" alt="M11_229551: cumulative mass formed against lookback time with t10 to t90">
<figcaption>Mass formed in galaxy M11_229551 against lookback time: t10 4.59, t20 4.16, t50 2.87 Gyr, only a 16-84 percent range.</figcaption>
</figure>

229883-M9_229883
: z 0.7280 · S/N 22.6

<figure>
<img loading="lazy" src="/wiki/f/results/rtx-5060-dr2-quiescent-full-spectrum/229883-M9_229883/diagnostics/photometric_chi2.png" alt="M9_229883: photometric pull and chi-squared contribution per band">
<figcaption>Pull of only the 12 fitted bands of galaxy M9_229883 against the model, 8.40 per band at a 5 percent flux error floor.</figcaption>
</figure>

<figure>
<img loading="lazy" src="/wiki/f/results/rtx-5060-dr2-quiescent-full-spectrum/229883-M9_229883/diagnostics/spectral_chi2.png" alt="M9_229883: spectral pull, binned mean pull squared, cumulative chi-squared">
<figcaption>Pull of only 3544 fitted spectrum pixels of galaxy M9_229883 against the model, 1.167 per pixel at a 4.25 percent error floor.</figcaption>
</figure>

<figure>
<img loading="lazy" src="/wiki/f/results/rtx-5060-dr2-quiescent-full-spectrum/229883-M9_229883/diagnostics/sf_timescales.png" alt="M9_229883: cumulative mass formed against lookback time with t10 to t90">
<figcaption>Mass formed in galaxy M9_229883 against lookback time: t10 6.20, t20 5.26, t50 3.61 Gyr, only a 16-84 percent range.</figcaption>
</figure>

230747-M13_230747
: z 0.6985 · S/N 22.6

<figure>
<img loading="lazy" src="/wiki/f/results/rtx-5060-dr2-quiescent-full-spectrum/230747-M13_230747/diagnostics/photometric_chi2.png" alt="M13_230747: photometric pull and chi-squared contribution per band">
<figcaption>Pull of only the 12 fitted bands of galaxy M13_230747 against the model, 1.97 per band at a 5 percent flux error floor.</figcaption>
</figure>

<figure>
<img loading="lazy" src="/wiki/f/results/rtx-5060-dr2-quiescent-full-spectrum/230747-M13_230747/diagnostics/spectral_chi2.png" alt="M13_230747: spectral pull, binned mean pull squared, cumulative chi-squared">
<figcaption>Pull of only 3562 fitted spectrum pixels of galaxy M13_230747 against the model, 1.116 per pixel at a 5.54 percent error floor.</figcaption>
</figure>

<figure>
<img loading="lazy" src="/wiki/f/results/rtx-5060-dr2-quiescent-full-spectrum/230747-M13_230747/diagnostics/sf_timescales.png" alt="M13_230747: cumulative mass formed against lookback time with t10 to t90">
<figcaption>Mass formed in galaxy M13_230747 against lookback time: t10 4.60, t20 4.17, t50 2.90 Gyr, only a 16-84 percent range.</figcaption>
</figure>

230983-M10_230983
: z 0.6961 · S/N 21.7

<figure>
<img loading="lazy" src="/wiki/f/results/rtx-5060-dr2-quiescent-full-spectrum/230983-M10_230983/diagnostics/photometric_chi2.png" alt="M10_230983: photometric pull and chi-squared contribution per band">
<figcaption>Pull of only the 12 fitted bands of galaxy M10_230983 against the model, 4.69 per band at a 5 percent flux error floor.</figcaption>
</figure>

<figure>
<img loading="lazy" src="/wiki/f/results/rtx-5060-dr2-quiescent-full-spectrum/230983-M10_230983/diagnostics/spectral_chi2.png" alt="M10_230983: spectral pull, binned mean pull squared, cumulative chi-squared">
<figcaption>Pull of only 3586 fitted spectrum pixels of galaxy M10_230983 against the model, 1.034 per pixel at a 4.26 percent error floor.</figcaption>
</figure>

<figure>
<img loading="lazy" src="/wiki/f/results/rtx-5060-dr2-quiescent-full-spectrum/230983-M10_230983/diagnostics/sf_timescales.png" alt="M10_230983: cumulative mass formed against lookback time with t10 to t90">
<figcaption>Mass formed in galaxy M10_230983 against lookback time: t10 6.96, t20 6.60, t50 5.51 Gyr, only a 16-84 percent range.</figcaption>
</figure>

231276-M9_231276
: z 0.6541 · S/N 40.1

<figure>
<img loading="lazy" src="/wiki/f/results/rtx-5060-dr2-quiescent-full-spectrum/231276-M9_231276/diagnostics/photometric_chi2.png" alt="M9_231276: photometric pull and chi-squared contribution per band">
<figcaption>Pull of only the 12 fitted bands of galaxy M9_231276 against the model, 8.63 per band at a 5 percent flux error floor.</figcaption>
</figure>

<figure>
<img loading="lazy" src="/wiki/f/results/rtx-5060-dr2-quiescent-full-spectrum/231276-M9_231276/diagnostics/spectral_chi2.png" alt="M9_231276: spectral pull, binned mean pull squared, cumulative chi-squared">
<figcaption>Pull of only 3522 fitted spectrum pixels of galaxy M9_231276 against the model, 1.112 per pixel at a 5.99 percent error floor.</figcaption>
</figure>

<figure>
<img loading="lazy" src="/wiki/f/results/rtx-5060-dr2-quiescent-full-spectrum/231276-M9_231276/diagnostics/sf_timescales.png" alt="M9_231276: cumulative mass formed against lookback time with t10 to t90">
<figcaption>Mass formed in galaxy M9_231276 against lookback time: t10 6.98, t20 6.40, t50 4.48 Gyr, only a 16-84 percent range.</figcaption>
</figure>

231544-M10_231544
: z 0.6548 · S/N 26.1

<figure>
<img loading="lazy" src="/wiki/f/results/rtx-5060-dr2-quiescent-full-spectrum/231544-M10_231544/diagnostics/photometric_chi2.png" alt="M10_231544: photometric pull and chi-squared contribution per band">
<figcaption>Pull of only the 12 fitted bands of galaxy M10_231544 against the model, 2.85 per band at a 5 percent flux error floor.</figcaption>
</figure>

<figure>
<img loading="lazy" src="/wiki/f/results/rtx-5060-dr2-quiescent-full-spectrum/231544-M10_231544/diagnostics/spectral_chi2.png" alt="M10_231544: spectral pull, binned mean pull squared, cumulative chi-squared">
<figcaption>Pull of only 3492 fitted spectrum pixels of galaxy M10_231544 against the model, 1.065 per pixel at a 2.75 percent error floor.</figcaption>
</figure>

<figure>
<img loading="lazy" src="/wiki/f/results/rtx-5060-dr2-quiescent-full-spectrum/231544-M10_231544/diagnostics/sf_timescales.png" alt="M10_231544: cumulative mass formed against lookback time with t10 to t90">
<figcaption>Mass formed in galaxy M10_231544 against lookback time: t10 4.61, t20 4.20, t50 2.95 Gyr, only a 16-84 percent range.</figcaption>
</figure>

231554-M13_231554
: z 0.6973 · S/N 10.9

<figure>
<img loading="lazy" src="/wiki/f/results/rtx-5060-dr2-quiescent-full-spectrum/231554-M13_231554/diagnostics/photometric_chi2.png" alt="M13_231554: photometric pull and chi-squared contribution per band">
<figcaption>Pull of only the 12 fitted bands of galaxy M13_231554 against the model, 2.81 per band at a 5 percent flux error floor.</figcaption>
</figure>

<figure>
<img loading="lazy" src="/wiki/f/results/rtx-5060-dr2-quiescent-full-spectrum/231554-M13_231554/diagnostics/spectral_chi2.png" alt="M13_231554: spectral pull, binned mean pull squared, cumulative chi-squared">
<figcaption>Pull of only 3586 fitted spectrum pixels of galaxy M13_231554 against the model, 1.213 per pixel at a 9.96 percent error floor.</figcaption>
</figure>

<figure>
<img loading="lazy" src="/wiki/f/results/rtx-5060-dr2-quiescent-full-spectrum/231554-M13_231554/diagnostics/sf_timescales.png" alt="M13_231554: cumulative mass formed against lookback time with t10 to t90">
<figcaption>Mass formed in galaxy M13_231554 against lookback time: t10 6.91, t20 6.51, t50 5.32 Gyr, only a 16-84 percent range.</figcaption>
</figure>

232005-M9_232005
: z 0.6111 · S/N 29.0

<figure>
<img loading="lazy" src="/wiki/f/results/rtx-5060-dr2-quiescent-full-spectrum/232005-M9_232005/diagnostics/photometric_chi2.png" alt="M9_232005: photometric pull and chi-squared contribution per band">
<figcaption>Pull of only the 12 fitted bands of galaxy M9_232005 against the model, 7.22 per band at a 5 percent flux error floor.</figcaption>
</figure>

<figure>
<img loading="lazy" src="/wiki/f/results/rtx-5060-dr2-quiescent-full-spectrum/232005-M9_232005/diagnostics/spectral_chi2.png" alt="M9_232005: spectral pull, binned mean pull squared, cumulative chi-squared">
<figcaption>Pull of only 3494 fitted spectrum pixels of galaxy M9_232005 against the model, 1.109 per pixel at a 2.86 percent error floor.</figcaption>
</figure>

<figure>
<img loading="lazy" src="/wiki/f/results/rtx-5060-dr2-quiescent-full-spectrum/232005-M9_232005/diagnostics/sf_timescales.png" alt="M9_232005: cumulative mass formed against lookback time with t10 to t90">
<figcaption>Mass formed in galaxy M9_232005 against lookback time: t10 4.75, t20 4.33, t50 3.05 Gyr, only a 16-84 percent range.</figcaption>
</figure>

232627-M13_232627
: z 0.6211 · S/N 36.4

<figure>
<img loading="lazy" src="/wiki/f/results/rtx-5060-dr2-quiescent-full-spectrum/232627-M13_232627/diagnostics/photometric_chi2.png" alt="M13_232627: photometric pull and chi-squared contribution per band">
<figcaption>Pull of only the 12 fitted bands of galaxy M13_232627 against the model, 7.74 per band at a 5 percent flux error floor.</figcaption>
</figure>

<figure>
<img loading="lazy" src="/wiki/f/results/rtx-5060-dr2-quiescent-full-spectrum/232627-M13_232627/diagnostics/spectral_chi2.png" alt="M13_232627: spectral pull, binned mean pull squared, cumulative chi-squared">
<figcaption>Pull of only 3526 fitted spectrum pixels of galaxy M13_232627 against the model, 1.042 per pixel at a 4.34 percent error floor.</figcaption>
</figure>

<figure>
<img loading="lazy" src="/wiki/f/results/rtx-5060-dr2-quiescent-full-spectrum/232627-M13_232627/diagnostics/sf_timescales.png" alt="M13_232627: cumulative mass formed against lookback time with t10 to t90">
<figcaption>Mass formed in galaxy M13_232627 against lookback time: t10 7.38, t20 6.98, t50 5.80 Gyr, only a 16-84 percent range.</figcaption>
</figure>

232890-M9_232890
: z 0.7657 · S/N 12.6

<figure>
<img loading="lazy" src="/wiki/f/results/rtx-5060-dr2-quiescent-full-spectrum/232890-M9_232890/diagnostics/photometric_chi2.png" alt="M9_232890: photometric pull and chi-squared contribution per band">
<figcaption>Pull of only the 12 fitted bands of galaxy M9_232890 against the model, 2.65 per band at a 5 percent flux error floor.</figcaption>
</figure>

<figure>
<img loading="lazy" src="/wiki/f/results/rtx-5060-dr2-quiescent-full-spectrum/232890-M9_232890/diagnostics/spectral_chi2.png" alt="M9_232890: spectral pull, binned mean pull squared, cumulative chi-squared">
<figcaption>Pull of only 3545 fitted spectrum pixels of galaxy M9_232890 against the model, 1.111 per pixel at a 3.99 percent error floor.</figcaption>
</figure>

<figure>
<img loading="lazy" src="/wiki/f/results/rtx-5060-dr2-quiescent-full-spectrum/232890-M9_232890/diagnostics/sf_timescales.png" alt="M9_232890: cumulative mass formed against lookback time with t10 to t90">
<figcaption>Mass formed in galaxy M9_232890 against lookback time: t10 4.62, t20 4.22, t50 3.00 Gyr, only a 16-84 percent range.</figcaption>
</figure>

232962-M11_232962
: z 0.6977 · S/N 30.8

<figure>
<img loading="lazy" src="/wiki/f/results/rtx-5060-dr2-quiescent-full-spectrum/232962-M11_232962/diagnostics/photometric_chi2.png" alt="M11_232962: photometric pull and chi-squared contribution per band">
<figcaption>Pull of only the 12 fitted bands of galaxy M11_232962 against the model, 10.14 per band at a 5 percent flux error floor.</figcaption>
</figure>

<figure>
<img loading="lazy" src="/wiki/f/results/rtx-5060-dr2-quiescent-full-spectrum/232962-M11_232962/diagnostics/spectral_chi2.png" alt="M11_232962: spectral pull, binned mean pull squared, cumulative chi-squared">
<figcaption>Pull of only 3398 fitted spectrum pixels of galaxy M11_232962 against the model, 1.167 per pixel at a 6.43 percent error floor.</figcaption>
</figure>

<figure>
<img loading="lazy" src="/wiki/f/results/rtx-5060-dr2-quiescent-full-spectrum/232962-M11_232962/diagnostics/sf_timescales.png" alt="M11_232962: cumulative mass formed against lookback time with t10 to t90">
<figcaption>Mass formed in galaxy M11_232962 against lookback time: t10 4.77, t20 4.22, t50 2.71 Gyr, only a 16-84 percent range.</figcaption>
</figure>

233129-M10_233129
: z 0.6186 · S/N 75.5

<figure>
<img loading="lazy" src="/wiki/f/results/rtx-5060-dr2-quiescent-full-spectrum/233129-M10_233129/diagnostics/photometric_chi2.png" alt="M10_233129: photometric pull and chi-squared contribution per band">
<figcaption>Pull of only the 12 fitted bands of galaxy M10_233129 against the model, 14.53 per band at a 5 percent flux error floor.</figcaption>
</figure>

<figure>
<img loading="lazy" src="/wiki/f/results/rtx-5060-dr2-quiescent-full-spectrum/233129-M10_233129/diagnostics/spectral_chi2.png" alt="M10_233129: spectral pull, binned mean pull squared, cumulative chi-squared">
<figcaption>Pull of only 3456 fitted spectrum pixels of galaxy M10_233129 against the model, 1.057 per pixel at a 2.60 percent error floor.</figcaption>
</figure>

<figure>
<img loading="lazy" src="/wiki/f/results/rtx-5060-dr2-quiescent-full-spectrum/233129-M10_233129/diagnostics/sf_timescales.png" alt="M10_233129: cumulative mass formed against lookback time with t10 to t90">
<figcaption>Mass formed in galaxy M10_233129 against lookback time: t10 4.51, t20 4.00, t50 2.62 Gyr, only a 16-84 percent range.</figcaption>
</figure>

233169-M9_233169
: z 0.6104 · S/N 51.4

<figure>
<img loading="lazy" src="/wiki/f/results/rtx-5060-dr2-quiescent-full-spectrum/233169-M9_233169/diagnostics/photometric_chi2.png" alt="M9_233169: photometric pull and chi-squared contribution per band">
<figcaption>Pull of only the 12 fitted bands of galaxy M9_233169 against the model, 8.01 per band at a 5 percent flux error floor.</figcaption>
</figure>

<figure>
<img loading="lazy" src="/wiki/f/results/rtx-5060-dr2-quiescent-full-spectrum/233169-M9_233169/diagnostics/spectral_chi2.png" alt="M9_233169: spectral pull, binned mean pull squared, cumulative chi-squared">
<figcaption>Pull of only 3500 fitted spectrum pixels of galaxy M9_233169 against the model, 1.046 per pixel at a 3.10 percent error floor.</figcaption>
</figure>

<figure>
<img loading="lazy" src="/wiki/f/results/rtx-5060-dr2-quiescent-full-spectrum/233169-M9_233169/diagnostics/sf_timescales.png" alt="M9_233169: cumulative mass formed against lookback time with t10 to t90">
<figcaption>Mass formed in galaxy M9_233169 against lookback time: t10 7.35, t20 6.87, t50 5.41 Gyr, only a 16-84 percent range.</figcaption>
</figure>

233902-M6_233902
: z 0.7293 · S/N 19.1

<figure>
<img loading="lazy" src="/wiki/f/results/rtx-5060-dr2-quiescent-full-spectrum/233902-M6_233902/diagnostics/photometric_chi2.png" alt="M6_233902: photometric pull and chi-squared contribution per band">
<figcaption>Pull of only the 12 fitted bands of galaxy M6_233902 against the model, 3.20 per band at a 5 percent flux error floor.</figcaption>
</figure>

<figure>
<img loading="lazy" src="/wiki/f/results/rtx-5060-dr2-quiescent-full-spectrum/233902-M6_233902/diagnostics/spectral_chi2.png" alt="M6_233902: spectral pull, binned mean pull squared, cumulative chi-squared">
<figcaption>Pull of only 3382 fitted spectrum pixels of galaxy M6_233902 against the model, 1.098 per pixel at a 5.84 percent error floor.</figcaption>
</figure>

<figure>
<img loading="lazy" src="/wiki/f/results/rtx-5060-dr2-quiescent-full-spectrum/233902-M6_233902/diagnostics/sf_timescales.png" alt="M6_233902: cumulative mass formed against lookback time with t10 to t90">
<figcaption>Mass formed in galaxy M6_233902 against lookback time: t10 6.61, t20 6.08, t50 4.44 Gyr, only a 16-84 percent range.</figcaption>
</figure>

236682-M5_236682
: z 0.7342 · S/N 31.6

<figure>
<img loading="lazy" src="/wiki/f/results/rtx-5060-dr2-quiescent-full-spectrum/236682-M5_236682/diagnostics/photometric_chi2.png" alt="M5_236682: photometric pull and chi-squared contribution per band">
<figcaption>Pull of only the 12 fitted bands of galaxy M5_236682 against the model, 8.51 per band at a 5 percent flux error floor.</figcaption>
</figure>

<figure>
<img loading="lazy" src="/wiki/f/results/rtx-5060-dr2-quiescent-full-spectrum/236682-M5_236682/diagnostics/spectral_chi2.png" alt="M5_236682: spectral pull, binned mean pull squared, cumulative chi-squared">
<figcaption>Pull of only 3387 fitted spectrum pixels of galaxy M5_236682 against the model, 1.145 per pixel at a 4.38 percent error floor.</figcaption>
</figure>

<figure>
<img loading="lazy" src="/wiki/f/results/rtx-5060-dr2-quiescent-full-spectrum/236682-M5_236682/diagnostics/sf_timescales.png" alt="M5_236682: cumulative mass formed against lookback time with t10 to t90">
<figcaption>Mass formed in galaxy M5_236682 against lookback time: t10 4.91, t20 4.49, t50 3.22 Gyr, only a 16-84 percent range.</figcaption>
</figure>

236994-M5_236994
: z 0.7297 · S/N 31.8

<figure>
<img loading="lazy" src="/wiki/f/results/rtx-5060-dr2-quiescent-full-spectrum/236994-M5_236994/diagnostics/photometric_chi2.png" alt="M5_236994: photometric pull and chi-squared contribution per band">
<figcaption>Pull of only the 12 fitted bands of galaxy M5_236994 against the model, 16.09 per band at a 5 percent flux error floor.</figcaption>
</figure>

<figure>
<img loading="lazy" src="/wiki/f/results/rtx-5060-dr2-quiescent-full-spectrum/236994-M5_236994/diagnostics/spectral_chi2.png" alt="M5_236994: spectral pull, binned mean pull squared, cumulative chi-squared">
<figcaption>Pull of only 3423 fitted spectrum pixels of galaxy M5_236994 against the model, 1.151 per pixel at a 4.36 percent error floor.</figcaption>
</figure>

<figure>
<img loading="lazy" src="/wiki/f/results/rtx-5060-dr2-quiescent-full-spectrum/236994-M5_236994/diagnostics/sf_timescales.png" alt="M5_236994: cumulative mass formed against lookback time with t10 to t90">
<figcaption>Mass formed in galaxy M5_236994 against lookback time: t10 4.59, t20 4.16, t50 2.87 Gyr, only a 16-84 percent range.</figcaption>
</figure>

237437-M6_237437
: z 0.7337 · S/N 25.0

<figure>
<img loading="lazy" src="/wiki/f/results/rtx-5060-dr2-quiescent-full-spectrum/237437-M6_237437/diagnostics/photometric_chi2.png" alt="M6_237437: photometric pull and chi-squared contribution per band">
<figcaption>Pull of only the 12 fitted bands of galaxy M6_237437 against the model, 6.08 per band at a 5 percent flux error floor.</figcaption>
</figure>

<figure>
<img loading="lazy" src="/wiki/f/results/rtx-5060-dr2-quiescent-full-spectrum/237437-M6_237437/diagnostics/spectral_chi2.png" alt="M6_237437: spectral pull, binned mean pull squared, cumulative chi-squared">
<figcaption>Pull of only 3463 fitted spectrum pixels of galaxy M6_237437 against the model, 1.214 per pixel at a 4.45 percent error floor.</figcaption>
</figure>

<figure>
<img loading="lazy" src="/wiki/f/results/rtx-5060-dr2-quiescent-full-spectrum/237437-M6_237437/diagnostics/sf_timescales.png" alt="M6_237437: cumulative mass formed against lookback time with t10 to t90">
<figcaption>Mass formed in galaxy M6_237437 against lookback time: t10 4.69, t20 4.28, t50 3.06 Gyr, only a 16-84 percent range.</figcaption>
</figure>

237641-M6_237641
: z 0.8579 · S/N 19.3

<figure>
<img loading="lazy" src="/wiki/f/results/rtx-5060-dr2-quiescent-full-spectrum/237641-M6_237641/diagnostics/photometric_chi2.png" alt="M6_237641: photometric pull and chi-squared contribution per band">
<figcaption>Pull of only the 12 fitted bands of galaxy M6_237641 against the model, 3.11 per band at a 5 percent flux error floor.</figcaption>
</figure>

<figure>
<img loading="lazy" src="/wiki/f/results/rtx-5060-dr2-quiescent-full-spectrum/237641-M6_237641/diagnostics/spectral_chi2.png" alt="M6_237641: spectral pull, binned mean pull squared, cumulative chi-squared">
<figcaption>Pull of only 3432 fitted spectrum pixels of galaxy M6_237641 against the model, 1.139 per pixel at a 6.25 percent error floor.</figcaption>
</figure>

<figure>
<img loading="lazy" src="/wiki/f/results/rtx-5060-dr2-quiescent-full-spectrum/237641-M6_237641/diagnostics/sf_timescales.png" alt="M6_237641: cumulative mass formed against lookback time with t10 to t90">
<figcaption>Mass formed in galaxy M6_237641 against lookback time: t10 4.57, t20 4.13, t50 2.81 Gyr, only a 16-84 percent range.</figcaption>
</figure>

238314-M5_238314
: z 0.7320 · S/N 34.6

<figure>
<img loading="lazy" src="/wiki/f/results/rtx-5060-dr2-quiescent-full-spectrum/238314-M5_238314/diagnostics/photometric_chi2.png" alt="M5_238314: photometric pull and chi-squared contribution per band">
<figcaption>Pull of only the 12 fitted bands of galaxy M5_238314 against the model, 7.36 per band at a 5 percent flux error floor.</figcaption>
</figure>

<figure>
<img loading="lazy" src="/wiki/f/results/rtx-5060-dr2-quiescent-full-spectrum/238314-M5_238314/diagnostics/spectral_chi2.png" alt="M5_238314: spectral pull, binned mean pull squared, cumulative chi-squared">
<figcaption>Pull of only 3417 fitted spectrum pixels of galaxy M5_238314 against the model, 1.179 per pixel at a 4.53 percent error floor.</figcaption>
</figure>

<figure>
<img loading="lazy" src="/wiki/f/results/rtx-5060-dr2-quiescent-full-spectrum/238314-M5_238314/diagnostics/sf_timescales.png" alt="M5_238314: cumulative mass formed against lookback time with t10 to t90">
<figcaption>Mass formed in galaxy M5_238314 against lookback time: t10 4.66, t20 4.26, t50 3.04 Gyr, only a 16-84 percent range.</figcaption>
</figure>

238580-M5_238580
: z 0.7304 · S/N 24.3

<figure>
<img loading="lazy" src="/wiki/f/results/rtx-5060-dr2-quiescent-full-spectrum/238580-M5_238580/diagnostics/photometric_chi2.png" alt="M5_238580: photometric pull and chi-squared contribution per band">
<figcaption>Pull of only the 12 fitted bands of galaxy M5_238580 against the model, 7.11 per band at a 5 percent flux error floor.</figcaption>
</figure>

<figure>
<img loading="lazy" src="/wiki/f/results/rtx-5060-dr2-quiescent-full-spectrum/238580-M5_238580/diagnostics/spectral_chi2.png" alt="M5_238580: spectral pull, binned mean pull squared, cumulative chi-squared">
<figcaption>Pull of only 3557 fitted spectrum pixels of galaxy M5_238580 against the model, 1.151 per pixel at a 6.16 percent error floor.</figcaption>
</figure>

<figure>
<img loading="lazy" src="/wiki/f/results/rtx-5060-dr2-quiescent-full-spectrum/238580-M5_238580/diagnostics/sf_timescales.png" alt="M5_238580: cumulative mass formed against lookback time with t10 to t90">
<figcaption>Mass formed in galaxy M5_238580 against lookback time: t10 6.88, t20 6.64, t50 5.91 Gyr, only a 16-84 percent range.</figcaption>
</figure>

240899-M6_240899
: z 0.7395 · S/N 15.6

<figure>
<img loading="lazy" src="/wiki/f/results/rtx-5060-dr2-quiescent-full-spectrum/240899-M6_240899/diagnostics/photometric_chi2.png" alt="M6_240899: photometric pull and chi-squared contribution per band">
<figcaption>Pull of only the 12 fitted bands of galaxy M6_240899 against the model, 4.99 per band at a 5 percent flux error floor.</figcaption>
</figure>

<figure>
<img loading="lazy" src="/wiki/f/results/rtx-5060-dr2-quiescent-full-spectrum/240899-M6_240899/diagnostics/spectral_chi2.png" alt="M6_240899: spectral pull, binned mean pull squared, cumulative chi-squared">
<figcaption>Pull of only 3479 fitted spectrum pixels of galaxy M6_240899 against the model, 1.148 per pixel at a 5.56 percent error floor.</figcaption>
</figure>

<figure>
<img loading="lazy" src="/wiki/f/results/rtx-5060-dr2-quiescent-full-spectrum/240899-M6_240899/diagnostics/sf_timescales.png" alt="M6_240899: cumulative mass formed against lookback time with t10 to t90">
<figcaption>Mass formed in galaxy M6_240899 against lookback time: t10 6.54, t20 6.01, t50 2.91 Gyr, only a 16-84 percent range.</figcaption>
</figure>

241189-M5_241189
: z 0.7287 · S/N 29.0

<figure>
<img loading="lazy" src="/wiki/f/results/rtx-5060-dr2-quiescent-full-spectrum/241189-M5_241189/diagnostics/photometric_chi2.png" alt="M5_241189: photometric pull and chi-squared contribution per band">
<figcaption>Pull of only the 12 fitted bands of galaxy M5_241189 against the model, 6.24 per band at a 5 percent flux error floor.</figcaption>
</figure>

<figure>
<img loading="lazy" src="/wiki/f/results/rtx-5060-dr2-quiescent-full-spectrum/241189-M5_241189/diagnostics/spectral_chi2.png" alt="M5_241189: spectral pull, binned mean pull squared, cumulative chi-squared">
<figcaption>Pull of only 3459 fitted spectrum pixels of galaxy M5_241189 against the model, 1.113 per pixel at a 3.96 percent error floor.</figcaption>
</figure>

<figure>
<img loading="lazy" src="/wiki/f/results/rtx-5060-dr2-quiescent-full-spectrum/241189-M5_241189/diagnostics/sf_timescales.png" alt="M5_241189: cumulative mass formed against lookback time with t10 to t90">
<figcaption>Mass formed in galaxy M5_241189 against lookback time: t10 4.95, t20 4.52, t50 3.23 Gyr, only a 16-84 percent range.</figcaption>
</figure>

243871-M13_243871
: z 0.7334 · S/N 22.3

<figure>
<img loading="lazy" src="/wiki/f/results/rtx-5060-dr2-quiescent-full-spectrum/243871-M13_243871/diagnostics/photometric_chi2.png" alt="M13_243871: photometric pull and chi-squared contribution per band">
<figcaption>Pull of only the 12 fitted bands of galaxy M13_243871 against the model, 1.87 per band at a 5 percent flux error floor.</figcaption>
</figure>

<figure>
<img loading="lazy" src="/wiki/f/results/rtx-5060-dr2-quiescent-full-spectrum/243871-M13_243871/diagnostics/spectral_chi2.png" alt="M13_243871: spectral pull, binned mean pull squared, cumulative chi-squared">
<figcaption>Pull of only 3539 fitted spectrum pixels of galaxy M13_243871 against the model, 1.084 per pixel at a 6.40 percent error floor.</figcaption>
</figure>

<figure>
<img loading="lazy" src="/wiki/f/results/rtx-5060-dr2-quiescent-full-spectrum/243871-M13_243871/diagnostics/sf_timescales.png" alt="M13_243871: cumulative mass formed against lookback time with t10 to t90">
<figcaption>Mass formed in galaxy M13_243871 against lookback time: t10 4.73, t20 4.26, t50 2.92 Gyr, only a 16-84 percent range.</figcaption>
</figure>

244239-M13_244239
: z 0.7378 · S/N 24.5

<figure>
<img loading="lazy" src="/wiki/f/results/rtx-5060-dr2-quiescent-full-spectrum/244239-M13_244239/diagnostics/photometric_chi2.png" alt="M13_244239: photometric pull and chi-squared contribution per band">
<figcaption>Pull of only the 12 fitted bands of galaxy M13_244239 against the model, 3.83 per band at a 5 percent flux error floor.</figcaption>
</figure>

<figure>
<img loading="lazy" src="/wiki/f/results/rtx-5060-dr2-quiescent-full-spectrum/244239-M13_244239/diagnostics/spectral_chi2.png" alt="M13_244239: spectral pull, binned mean pull squared, cumulative chi-squared">
<figcaption>Pull of only 3568 fitted spectrum pixels of galaxy M13_244239 against the model, 1.113 per pixel at a 5.26 percent error floor.</figcaption>
</figure>

<figure>
<img loading="lazy" src="/wiki/f/results/rtx-5060-dr2-quiescent-full-spectrum/244239-M13_244239/diagnostics/sf_timescales.png" alt="M13_244239: cumulative mass formed against lookback time with t10 to t90">
<figcaption>Mass formed in galaxy M13_244239 against lookback time: t10 4.65, t20 4.25, t50 3.04 Gyr, only a 16-84 percent range.</figcaption>
</figure>

244680-M13_244680
: z 0.9576 · S/N 4.4

<figure>
<img loading="lazy" src="/wiki/f/results/rtx-5060-dr2-quiescent-full-spectrum/244680-M13_244680/diagnostics/photometric_chi2.png" alt="M13_244680: photometric pull and chi-squared contribution per band">
<figcaption>Pull of only the 12 fitted bands of galaxy M13_244680 against the model, 3.66 per band at a 5 percent flux error floor.</figcaption>
</figure>

<figure>
<img loading="lazy" src="/wiki/f/results/rtx-5060-dr2-quiescent-full-spectrum/244680-M13_244680/diagnostics/spectral_chi2.png" alt="M13_244680: spectral pull, binned mean pull squared, cumulative chi-squared">
<figcaption>Pull of only 3849 fitted spectrum pixels of galaxy M13_244680 against the model, 1.549 per pixel at a 9.98 percent error floor.</figcaption>
</figure>

<figure>
<img loading="lazy" src="/wiki/f/results/rtx-5060-dr2-quiescent-full-spectrum/244680-M13_244680/diagnostics/sf_timescales.png" alt="M13_244680: cumulative mass formed against lookback time with t10 to t90">
<figcaption>Mass formed in galaxy M13_244680 against lookback time: t10 4.64, t20 4.22, t50 2.99 Gyr, only a 16-84 percent range.</figcaption>
</figure>

244738-M11_244738
: z 0.6971 · S/N 29.0

<figure>
<img loading="lazy" src="/wiki/f/results/rtx-5060-dr2-quiescent-full-spectrum/244738-M11_244738/diagnostics/photometric_chi2.png" alt="M11_244738: photometric pull and chi-squared contribution per band">
<figcaption>Pull of only the 12 fitted bands of galaxy M11_244738 against the model, 16.64 per band at a 5 percent flux error floor.</figcaption>
</figure>

<figure>
<img loading="lazy" src="/wiki/f/results/rtx-5060-dr2-quiescent-full-spectrum/244738-M11_244738/diagnostics/spectral_chi2.png" alt="M11_244738: spectral pull, binned mean pull squared, cumulative chi-squared">
<figcaption>Pull of only 3442 fitted spectrum pixels of galaxy M11_244738 against the model, 1.114 per pixel at a 4.25 percent error floor.</figcaption>
</figure>

<figure>
<img loading="lazy" src="/wiki/f/results/rtx-5060-dr2-quiescent-full-spectrum/244738-M11_244738/diagnostics/sf_timescales.png" alt="M11_244738: cumulative mass formed against lookback time with t10 to t90">
<figcaption>Mass formed in galaxy M11_244738 against lookback time: t10 4.62, t20 4.21, t50 3.01 Gyr, only a 16-84 percent range.</figcaption>
</figure>

245252-M11_245252
: z 0.6944 · S/N 44.2

<figure>
<img loading="lazy" src="/wiki/f/results/rtx-5060-dr2-quiescent-full-spectrum/245252-M11_245252/diagnostics/photometric_chi2.png" alt="M11_245252: photometric pull and chi-squared contribution per band">
<figcaption>Pull of only the 12 fitted bands of galaxy M11_245252 against the model, 22.75 per band at a 5 percent flux error floor.</figcaption>
</figure>

<figure>
<img loading="lazy" src="/wiki/f/results/rtx-5060-dr2-quiescent-full-spectrum/245252-M11_245252/diagnostics/spectral_chi2.png" alt="M11_245252: spectral pull, binned mean pull squared, cumulative chi-squared">
<figcaption>Pull of only 3516 fitted spectrum pixels of galaxy M11_245252 against the model, 1.102 per pixel at a 4.23 percent error floor.</figcaption>
</figure>

<figure>
<img loading="lazy" src="/wiki/f/results/rtx-5060-dr2-quiescent-full-spectrum/245252-M11_245252/diagnostics/sf_timescales.png" alt="M11_245252: cumulative mass formed against lookback time with t10 to t90">
<figcaption>Mass formed in galaxy M11_245252 against lookback time: t10 4.63, t20 4.22, t50 3.02 Gyr, only a 16-84 percent range.</figcaption>
</figure>

245621-M11_245621
: z 0.7350 · S/N 17.0

<figure>
<img loading="lazy" src="/wiki/f/results/rtx-5060-dr2-quiescent-full-spectrum/245621-M11_245621/diagnostics/photometric_chi2.png" alt="M11_245621: photometric pull and chi-squared contribution per band">
<figcaption>Pull of only the 12 fitted bands of galaxy M11_245621 against the model, 3.38 per band at a 5 percent flux error floor.</figcaption>
</figure>

<figure>
<img loading="lazy" src="/wiki/f/results/rtx-5060-dr2-quiescent-full-spectrum/245621-M11_245621/diagnostics/spectral_chi2.png" alt="M11_245621: spectral pull, binned mean pull squared, cumulative chi-squared">
<figcaption>Pull of only 3542 fitted spectrum pixels of galaxy M11_245621 against the model, 1.096 per pixel at a 5.82 percent error floor.</figcaption>
</figure>

<figure>
<img loading="lazy" src="/wiki/f/results/rtx-5060-dr2-quiescent-full-spectrum/245621-M11_245621/diagnostics/sf_timescales.png" alt="M11_245621: cumulative mass formed against lookback time with t10 to t90">
<figcaption>Mass formed in galaxy M11_245621 against lookback time: t10 4.62, t20 4.22, t50 3.02 Gyr, only a 16-84 percent range.</figcaption>
</figure>

245763-M13_245763
: z 0.7542 · S/N 9.4

<figure>
<img loading="lazy" src="/wiki/f/results/rtx-5060-dr2-quiescent-full-spectrum/245763-M13_245763/diagnostics/photometric_chi2.png" alt="M13_245763: photometric pull and chi-squared contribution per band">
<figcaption>Pull of only the 12 fitted bands of galaxy M13_245763 against the model, 4.87 per band at a 5 percent flux error floor.</figcaption>
</figure>

<figure>
<img loading="lazy" src="/wiki/f/results/rtx-5060-dr2-quiescent-full-spectrum/245763-M13_245763/diagnostics/spectral_chi2.png" alt="M13_245763: spectral pull, binned mean pull squared, cumulative chi-squared">
<figcaption>Pull of only 3820 fitted spectrum pixels of galaxy M13_245763 against the model, 1.138 per pixel at a 9.22 percent error floor.</figcaption>
</figure>

<figure>
<img loading="lazy" src="/wiki/f/results/rtx-5060-dr2-quiescent-full-spectrum/245763-M13_245763/diagnostics/sf_timescales.png" alt="M13_245763: cumulative mass formed against lookback time with t10 to t90">
<figcaption>Mass formed in galaxy M13_245763 against lookback time: t10 6.74, t20 6.48, t50 5.71 Gyr, only a 16-84 percent range.</figcaption>
</figure>

245864-M11_245864
: z 0.6981 · S/N 13.3

<figure>
<img loading="lazy" src="/wiki/f/results/rtx-5060-dr2-quiescent-full-spectrum/245864-M11_245864/diagnostics/photometric_chi2.png" alt="M11_245864: photometric pull and chi-squared contribution per band">
<figcaption>Pull of only the 12 fitted bands of galaxy M11_245864 against the model, 3.39 per band at a 5 percent flux error floor.</figcaption>
</figure>

<figure>
<img loading="lazy" src="/wiki/f/results/rtx-5060-dr2-quiescent-full-spectrum/245864-M11_245864/diagnostics/spectral_chi2.png" alt="M11_245864: spectral pull, binned mean pull squared, cumulative chi-squared">
<figcaption>Pull of only 3522 fitted spectrum pixels of galaxy M11_245864 against the model, 1.115 per pixel at a 4.80 percent error floor.</figcaption>
</figure>

<figure>
<img loading="lazy" src="/wiki/f/results/rtx-5060-dr2-quiescent-full-spectrum/245864-M11_245864/diagnostics/sf_timescales.png" alt="M11_245864: cumulative mass formed against lookback time with t10 to t90">
<figcaption>Mass formed in galaxy M11_245864 against lookback time: t10 4.61, t20 4.18, t50 2.90 Gyr, only a 16-84 percent range.</figcaption>
</figure>

246149-M13_246149
: z 0.7345 · S/N 26.6

<figure>
<img loading="lazy" src="/wiki/f/results/rtx-5060-dr2-quiescent-full-spectrum/246149-M13_246149/diagnostics/photometric_chi2.png" alt="M13_246149: photometric pull and chi-squared contribution per band">
<figcaption>Pull of only the 12 fitted bands of galaxy M13_246149 against the model, 7.52 per band at a 5 percent flux error floor.</figcaption>
</figure>

<figure>
<img loading="lazy" src="/wiki/f/results/rtx-5060-dr2-quiescent-full-spectrum/246149-M13_246149/diagnostics/spectral_chi2.png" alt="M13_246149: spectral pull, binned mean pull squared, cumulative chi-squared">
<figcaption>Pull of only 3689 fitted spectrum pixels of galaxy M13_246149 against the model, 1.082 per pixel at a 6.13 percent error floor.</figcaption>
</figure>

<figure>
<img loading="lazy" src="/wiki/f/results/rtx-5060-dr2-quiescent-full-spectrum/246149-M13_246149/diagnostics/sf_timescales.png" alt="M13_246149: cumulative mass formed against lookback time with t10 to t90">
<figcaption>Mass formed in galaxy M13_246149 against lookback time: t10 5.84, t20 4.85, t50 3.58 Gyr, only a 16-84 percent range.</figcaption>
</figure>

248217-M13_248217
: z 0.6109 · S/N 30.6

<figure>
<img loading="lazy" src="/wiki/f/results/rtx-5060-dr2-quiescent-full-spectrum/248217-M13_248217/diagnostics/photometric_chi2.png" alt="M13_248217: photometric pull and chi-squared contribution per band">
<figcaption>Pull of only the 12 fitted bands of galaxy M13_248217 against the model, 8.88 per band at a 5 percent flux error floor.</figcaption>
</figure>

<figure>
<img loading="lazy" src="/wiki/f/results/rtx-5060-dr2-quiescent-full-spectrum/248217-M13_248217/diagnostics/spectral_chi2.png" alt="M13_248217: spectral pull, binned mean pull squared, cumulative chi-squared">
<figcaption>Pull of only 3587 fitted spectrum pixels of galaxy M13_248217 against the model, 1.114 per pixel at a 4.30 percent error floor.</figcaption>
</figure>

<figure>
<img loading="lazy" src="/wiki/f/results/rtx-5060-dr2-quiescent-full-spectrum/248217-M13_248217/diagnostics/sf_timescales.png" alt="M13_248217: cumulative mass formed against lookback time with t10 to t90">
<figcaption>Mass formed in galaxy M13_248217 against lookback time: t10 4.70, t20 4.29, t50 3.07 Gyr, only a 16-84 percent range.</figcaption>
</figure>

248829-M11_248829
: z 0.7635 · S/N 19.7

<figure>
<img loading="lazy" src="/wiki/f/results/rtx-5060-dr2-quiescent-full-spectrum/248829-M11_248829/diagnostics/photometric_chi2.png" alt="M11_248829: photometric pull and chi-squared contribution per band">
<figcaption>Pull of only the 12 fitted bands of galaxy M11_248829 against the model, 4.75 per band at a 5 percent flux error floor.</figcaption>
</figure>

<figure>
<img loading="lazy" src="/wiki/f/results/rtx-5060-dr2-quiescent-full-spectrum/248829-M11_248829/diagnostics/spectral_chi2.png" alt="M11_248829: spectral pull, binned mean pull squared, cumulative chi-squared">
<figcaption>Pull of only 3443 fitted spectrum pixels of galaxy M11_248829 against the model, 1.184 per pixel at a 4.90 percent error floor.</figcaption>
</figure>

<figure>
<img loading="lazy" src="/wiki/f/results/rtx-5060-dr2-quiescent-full-spectrum/248829-M11_248829/diagnostics/sf_timescales.png" alt="M11_248829: cumulative mass formed against lookback time with t10 to t90">
<figcaption>Mass formed in galaxy M11_248829 against lookback time: t10 4.59, t20 4.15, t50 2.86 Gyr, only a 16-84 percent range.</figcaption>
</figure>

250391-M11_250391
: z 0.8893 · S/N 35.8

<figure>
<img loading="lazy" src="/wiki/f/results/rtx-5060-dr2-quiescent-full-spectrum/250391-M11_250391/diagnostics/photometric_chi2.png" alt="M11_250391: photometric pull and chi-squared contribution per band">
<figcaption>Pull of only the 12 fitted bands of galaxy M11_250391 against the model, 18.54 per band at a 5 percent flux error floor.</figcaption>
</figure>

<figure>
<img loading="lazy" src="/wiki/f/results/rtx-5060-dr2-quiescent-full-spectrum/250391-M11_250391/diagnostics/spectral_chi2.png" alt="M11_250391: spectral pull, binned mean pull squared, cumulative chi-squared">
<figcaption>Pull of only 3849 fitted spectrum pixels of galaxy M11_250391 against the model, 1.083 per pixel at a 4.68 percent error floor.</figcaption>
</figure>

<figure>
<img loading="lazy" src="/wiki/f/results/rtx-5060-dr2-quiescent-full-spectrum/250391-M11_250391/diagnostics/sf_timescales.png" alt="M11_250391: cumulative mass formed against lookback time with t10 to t90">
<figcaption>Mass formed in galaxy M11_250391 against lookback time: t10 2.17, t20 1.28, t50 0.69 Gyr, only a 16-84 percent range.</figcaption>
</figure>

253688-M13_253688
: z 0.8370 · S/N 4.8

<figure>
<img loading="lazy" src="/wiki/f/results/rtx-5060-dr2-quiescent-full-spectrum/253688-M13_253688/diagnostics/photometric_chi2.png" alt="M13_253688: photometric pull and chi-squared contribution per band">
<figcaption>Pull of only the 12 fitted bands of galaxy M13_253688 against the model, 1.89 per band at a 5 percent flux error floor.</figcaption>
</figure>

<figure>
<img loading="lazy" src="/wiki/f/results/rtx-5060-dr2-quiescent-full-spectrum/253688-M13_253688/diagnostics/spectral_chi2.png" alt="M13_253688: spectral pull, binned mean pull squared, cumulative chi-squared">
<figcaption>Pull of only 3320 fitted spectrum pixels of galaxy M13_253688 against the model, 2.554 per pixel at a 9.99 percent error floor.</figcaption>
</figure>

<figure>
<img loading="lazy" src="/wiki/f/results/rtx-5060-dr2-quiescent-full-spectrum/253688-M13_253688/diagnostics/sf_timescales.png" alt="M13_253688: cumulative mass formed against lookback time with t10 to t90">
<figcaption>Mass formed in galaxy M13_253688 against lookback time: t10 5.34, t20 3.53, t50 2.05 Gyr, only a 16-84 percent range.</figcaption>
</figure>

254350-M13_254350
: z 0.6692 · S/N 13.5

<figure>
<img loading="lazy" src="/wiki/f/results/rtx-5060-dr2-quiescent-full-spectrum/254350-M13_254350/diagnostics/photometric_chi2.png" alt="M13_254350: photometric pull and chi-squared contribution per band">
<figcaption>Pull of only the 12 fitted bands of galaxy M13_254350 against the model, 5.68 per band at a 5 percent flux error floor.</figcaption>
</figure>

<figure>
<img loading="lazy" src="/wiki/f/results/rtx-5060-dr2-quiescent-full-spectrum/254350-M13_254350/diagnostics/spectral_chi2.png" alt="M13_254350: spectral pull, binned mean pull squared, cumulative chi-squared">
<figcaption>Pull of only 3576 fitted spectrum pixels of galaxy M13_254350 against the model, 1.122 per pixel at a 9.26 percent error floor.</figcaption>
</figure>

<figure>
<img loading="lazy" src="/wiki/f/results/rtx-5060-dr2-quiescent-full-spectrum/254350-M13_254350/diagnostics/sf_timescales.png" alt="M13_254350: cumulative mass formed against lookback time with t10 to t90">
<figcaption>Mass formed in galaxy M13_254350 against lookback time: t10 4.93, t20 4.46, t50 3.07 Gyr, only a 16-84 percent range.</figcaption>
</figure>

255047-M13_255047
: z 0.8643 · S/N 9.4

<figure>
<img loading="lazy" src="/wiki/f/results/rtx-5060-dr2-quiescent-full-spectrum/255047-M13_255047/diagnostics/photometric_chi2.png" alt="M13_255047: photometric pull and chi-squared contribution per band">
<figcaption>Pull of only the 12 fitted bands of galaxy M13_255047 against the model, 2.97 per band at a 5 percent flux error floor.</figcaption>
</figure>

<figure>
<img loading="lazy" src="/wiki/f/results/rtx-5060-dr2-quiescent-full-spectrum/255047-M13_255047/diagnostics/spectral_chi2.png" alt="M13_255047: spectral pull, binned mean pull squared, cumulative chi-squared">
<figcaption>Pull of only 3802 fitted spectrum pixels of galaxy M13_255047 against the model, 1.294 per pixel at a 9.97 percent error floor.</figcaption>
</figure>

<figure>
<img loading="lazy" src="/wiki/f/results/rtx-5060-dr2-quiescent-full-spectrum/255047-M13_255047/diagnostics/sf_timescales.png" alt="M13_255047: cumulative mass formed against lookback time with t10 to t90">
<figcaption>Mass formed in galaxy M13_255047 against lookback time: t10 4.55, t20 4.08, t50 2.73 Gyr, only a 16-84 percent range.</figcaption>
</figure>

257455-M11_257455
: z 0.6657 · S/N 36.0

<figure>
<img loading="lazy" src="/wiki/f/results/rtx-5060-dr2-quiescent-full-spectrum/257455-M11_257455/diagnostics/photometric_chi2.png" alt="M11_257455: photometric pull and chi-squared contribution per band">
<figcaption>Pull of only the 12 fitted bands of galaxy M11_257455 against the model, 7.60 per band at a 5 percent flux error floor.</figcaption>
</figure>

<figure>
<img loading="lazy" src="/wiki/f/results/rtx-5060-dr2-quiescent-full-spectrum/257455-M11_257455/diagnostics/spectral_chi2.png" alt="M11_257455: spectral pull, binned mean pull squared, cumulative chi-squared">
<figcaption>Pull of only 3537 fitted spectrum pixels of galaxy M11_257455 against the model, 1.127 per pixel at a 5.41 percent error floor.</figcaption>
</figure>

<figure>
<img loading="lazy" src="/wiki/f/results/rtx-5060-dr2-quiescent-full-spectrum/257455-M11_257455/diagnostics/sf_timescales.png" alt="M11_257455: cumulative mass formed against lookback time with t10 to t90">
<figcaption>Mass formed in galaxy M11_257455 against lookback time: t10 4.58, t20 4.14, t50 2.84 Gyr, only a 16-84 percent range.</figcaption>
</figure>

258753-M13_258753
: z 0.9096 · S/N 8.1

<figure>
<img loading="lazy" src="/wiki/f/results/rtx-5060-dr2-quiescent-full-spectrum/258753-M13_258753/diagnostics/photometric_chi2.png" alt="M13_258753: photometric pull and chi-squared contribution per band">
<figcaption>Pull of only the 12 fitted bands of galaxy M13_258753 against the model, 2.61 per band at a 5 percent flux error floor.</figcaption>
</figure>

<figure>
<img loading="lazy" src="/wiki/f/results/rtx-5060-dr2-quiescent-full-spectrum/258753-M13_258753/diagnostics/spectral_chi2.png" alt="M13_258753: spectral pull, binned mean pull squared, cumulative chi-squared">
<figcaption>Pull of only 3818 fitted spectrum pixels of galaxy M13_258753 against the model, 1.398 per pixel at a 9.98 percent error floor.</figcaption>
</figure>

<figure>
<img loading="lazy" src="/wiki/f/results/rtx-5060-dr2-quiescent-full-spectrum/258753-M13_258753/diagnostics/sf_timescales.png" alt="M13_258753: cumulative mass formed against lookback time with t10 to t90">
<figcaption>Mass formed in galaxy M13_258753 against lookback time: t10 6.09, t20 5.94, t50 5.50 Gyr, only a 16-84 percent range.</figcaption>
</figure>

259737-M13_259737
: z 0.7028 · S/N 14.7

<figure>
<img loading="lazy" src="/wiki/f/results/rtx-5060-dr2-quiescent-full-spectrum/259737-M13_259737/diagnostics/photometric_chi2.png" alt="M13_259737: photometric pull and chi-squared contribution per band">
<figcaption>Pull of only the 12 fitted bands of galaxy M13_259737 against the model, 8.56 per band at a 5 percent flux error floor.</figcaption>
</figure>

<figure>
<img loading="lazy" src="/wiki/f/results/rtx-5060-dr2-quiescent-full-spectrum/259737-M13_259737/diagnostics/spectral_chi2.png" alt="M13_259737: spectral pull, binned mean pull squared, cumulative chi-squared">
<figcaption>Pull of only 3592 fitted spectrum pixels of galaxy M13_259737 against the model, 1.527 per pixel at a 9.99 percent error floor.</figcaption>
</figure>

<figure>
<img loading="lazy" src="/wiki/f/results/rtx-5060-dr2-quiescent-full-spectrum/259737-M13_259737/diagnostics/sf_timescales.png" alt="M13_259737: cumulative mass formed against lookback time with t10 to t90">
<figcaption>Mass formed in galaxy M13_259737 against lookback time: t10 4.67, t20 4.26, t50 3.02 Gyr, only a 16-84 percent range.</figcaption>
</figure>

27068-M14_27068
: z 0.6783 · S/N 21.2

<figure>
<img loading="lazy" src="/wiki/f/results/rtx-5060-dr2-quiescent-full-spectrum/27068-M14_27068/diagnostics/photometric_chi2.png" alt="M14_27068: photometric pull and chi-squared contribution per band">
<figcaption>Pull of only the 12 fitted bands of galaxy M14_27068 against the model, 14.01 per band at a 5 percent flux error floor.</figcaption>
</figure>

<figure>
<img loading="lazy" src="/wiki/f/results/rtx-5060-dr2-quiescent-full-spectrum/27068-M14_27068/diagnostics/spectral_chi2.png" alt="M14_27068: spectral pull, binned mean pull squared, cumulative chi-squared">
<figcaption>Pull of only 3452 fitted spectrum pixels of galaxy M14_27068 against the model, 1.131 per pixel at a 4.74 percent error floor.</figcaption>
</figure>

<figure>
<img loading="lazy" src="/wiki/f/results/rtx-5060-dr2-quiescent-full-spectrum/27068-M14_27068/diagnostics/sf_timescales.png" alt="M14_27068: cumulative mass formed against lookback time with t10 to t90">
<figcaption>Mass formed in galaxy M14_27068 against lookback time: t10 4.50, t20 3.97, t50 2.57 Gyr, only a 16-84 percent range.</figcaption>
</figure>

31835-M14_31835
: z 0.6774 · S/N 27.4

<figure>
<img loading="lazy" src="/wiki/f/results/rtx-5060-dr2-quiescent-full-spectrum/31835-M14_31835/diagnostics/photometric_chi2.png" alt="M14_31835: photometric pull and chi-squared contribution per band">
<figcaption>Pull of only the 12 fitted bands of galaxy M14_31835 against the model, 4.45 per band at a 5 percent flux error floor.</figcaption>
</figure>

<figure>
<img loading="lazy" src="/wiki/f/results/rtx-5060-dr2-quiescent-full-spectrum/31835-M14_31835/diagnostics/spectral_chi2.png" alt="M14_31835: spectral pull, binned mean pull squared, cumulative chi-squared">
<figcaption>Pull of only 3558 fitted spectrum pixels of galaxy M14_31835 against the model, 1.081 per pixel at a 4.13 percent error floor.</figcaption>
</figure>

<figure>
<img loading="lazy" src="/wiki/f/results/rtx-5060-dr2-quiescent-full-spectrum/31835-M14_31835/diagnostics/sf_timescales.png" alt="M14_31835: cumulative mass formed against lookback time with t10 to t90">
<figcaption>Mass formed in galaxy M14_31835 against lookback time: t10 4.62, t20 4.21, t50 3.00 Gyr, only a 16-84 percent range.</figcaption>
</figure>

36550-M14_36550
: z 0.7386 · S/N 8.0

<figure>
<img loading="lazy" src="/wiki/f/results/rtx-5060-dr2-quiescent-full-spectrum/36550-M14_36550/diagnostics/photometric_chi2.png" alt="M14_36550: photometric pull and chi-squared contribution per band">
<figcaption>Pull of only the 12 fitted bands of galaxy M14_36550 against the model, 2.13 per band at a 5 percent flux error floor.</figcaption>
</figure>

<figure>
<img loading="lazy" src="/wiki/f/results/rtx-5060-dr2-quiescent-full-spectrum/36550-M14_36550/diagnostics/spectral_chi2.png" alt="M14_36550: spectral pull, binned mean pull squared, cumulative chi-squared">
<figcaption>Pull of only 3361 fitted spectrum pixels of galaxy M14_36550 against the model, 1.228 per pixel at a 9.92 percent error floor.</figcaption>
</figure>

<figure>
<img loading="lazy" src="/wiki/f/results/rtx-5060-dr2-quiescent-full-spectrum/36550-M14_36550/diagnostics/sf_timescales.png" alt="M14_36550: cumulative mass formed against lookback time with t10 to t90">
<figcaption>Mass formed in galaxy M14_36550 against lookback time: t10 4.62, t20 4.19, t50 2.92 Gyr, only a 16-84 percent range.</figcaption>
</figure>

37023-M14_37023
: z 0.7355 · S/N 21.0

<figure>
<img loading="lazy" src="/wiki/f/results/rtx-5060-dr2-quiescent-full-spectrum/37023-M14_37023/diagnostics/photometric_chi2.png" alt="M14_37023: photometric pull and chi-squared contribution per band">
<figcaption>Pull of only the 12 fitted bands of galaxy M14_37023 against the model, 5.04 per band at a 5 percent flux error floor.</figcaption>
</figure>

<figure>
<img loading="lazy" src="/wiki/f/results/rtx-5060-dr2-quiescent-full-spectrum/37023-M14_37023/diagnostics/spectral_chi2.png" alt="M14_37023: spectral pull, binned mean pull squared, cumulative chi-squared">
<figcaption>Pull of only 3393 fitted spectrum pixels of galaxy M14_37023 against the model, 1.139 per pixel at a 3.75 percent error floor.</figcaption>
</figure>

<figure>
<img loading="lazy" src="/wiki/f/results/rtx-5060-dr2-quiescent-full-spectrum/37023-M14_37023/diagnostics/sf_timescales.png" alt="M14_37023: cumulative mass formed against lookback time with t10 to t90">
<figcaption>Mass formed in galaxy M14_37023 against lookback time: t10 4.56, t20 4.11, t50 2.79 Gyr, only a 16-84 percent range.</figcaption>
</figure>

37219-M14_37219
: z 0.7347 · S/N 15.0

<figure>
<img loading="lazy" src="/wiki/f/results/rtx-5060-dr2-quiescent-full-spectrum/37219-M14_37219/diagnostics/photometric_chi2.png" alt="M14_37219: photometric pull and chi-squared contribution per band">
<figcaption>Pull of only the 12 fitted bands of galaxy M14_37219 against the model, 2.82 per band at a 5 percent flux error floor.</figcaption>
</figure>

<figure>
<img loading="lazy" src="/wiki/f/results/rtx-5060-dr2-quiescent-full-spectrum/37219-M14_37219/diagnostics/spectral_chi2.png" alt="M14_37219: spectral pull, binned mean pull squared, cumulative chi-squared">
<figcaption>Pull of only 3540 fitted spectrum pixels of galaxy M14_37219 against the model, 1.096 per pixel at a 4.17 percent error floor.</figcaption>
</figure>

<figure>
<img loading="lazy" src="/wiki/f/results/rtx-5060-dr2-quiescent-full-spectrum/37219-M14_37219/diagnostics/sf_timescales.png" alt="M14_37219: cumulative mass formed against lookback time with t10 to t90">
<figcaption>Mass formed in galaxy M14_37219 against lookback time: t10 4.60, t20 4.18, t50 2.92 Gyr, only a 16-84 percent range.</figcaption>
</figure>

37723-M14_37723
: z 0.7360 · S/N 22.9

<figure>
<img loading="lazy" src="/wiki/f/results/rtx-5060-dr2-quiescent-full-spectrum/37723-M14_37723/diagnostics/photometric_chi2.png" alt="M14_37723: photometric pull and chi-squared contribution per band">
<figcaption>Pull of only the 12 fitted bands of galaxy M14_37723 against the model, 2.84 per band at a 5 percent flux error floor.</figcaption>
</figure>

<figure>
<img loading="lazy" src="/wiki/f/results/rtx-5060-dr2-quiescent-full-spectrum/37723-M14_37723/diagnostics/spectral_chi2.png" alt="M14_37723: spectral pull, binned mean pull squared, cumulative chi-squared">
<figcaption>Pull of only 3408 fitted spectrum pixels of galaxy M14_37723 against the model, 1.098 per pixel at a 4.08 percent error floor.</figcaption>
</figure>

<figure>
<img loading="lazy" src="/wiki/f/results/rtx-5060-dr2-quiescent-full-spectrum/37723-M14_37723/diagnostics/sf_timescales.png" alt="M14_37723: cumulative mass formed against lookback time with t10 to t90">
<figcaption>Mass formed in galaxy M14_37723 against lookback time: t10 4.60, t20 4.18, t50 2.92 Gyr, only a 16-84 percent range.</figcaption>
</figure>

37843-M14_37843
: z 0.9694 · S/N 6.5

<figure>
<img loading="lazy" src="/wiki/f/results/rtx-5060-dr2-quiescent-full-spectrum/37843-M14_37843/diagnostics/photometric_chi2.png" alt="M14_37843: photometric pull and chi-squared contribution per band">
<figcaption>Pull of only the 12 fitted bands of galaxy M14_37843 against the model, 8.70 per band at a 5 percent flux error floor.</figcaption>
</figure>

<figure>
<img loading="lazy" src="/wiki/f/results/rtx-5060-dr2-quiescent-full-spectrum/37843-M14_37843/diagnostics/spectral_chi2.png" alt="M14_37843: spectral pull, binned mean pull squared, cumulative chi-squared">
<figcaption>Pull of only 3817 fitted spectrum pixels of galaxy M14_37843 against the model, 1.064 per pixel at a 6.57 percent error floor.</figcaption>
</figure>

<figure>
<img loading="lazy" src="/wiki/f/results/rtx-5060-dr2-quiescent-full-spectrum/37843-M14_37843/diagnostics/sf_timescales.png" alt="M14_37843: cumulative mass formed against lookback time with t10 to t90">
<figcaption>Mass formed in galaxy M14_37843 against lookback time: t10 4.63, t20 4.22, t50 3.02 Gyr, only a 16-84 percent range.</figcaption>
</figure>

38646-M14_38646
: z 0.9689 · S/N 9.7

<figure>
<img loading="lazy" src="/wiki/f/results/rtx-5060-dr2-quiescent-full-spectrum/38646-M14_38646/diagnostics/photometric_chi2.png" alt="M14_38646: photometric pull and chi-squared contribution per band">
<figcaption>Pull of only the 12 fitted bands of galaxy M14_38646 against the model, 15.44 per band at a 5 percent flux error floor.</figcaption>
</figure>

<figure>
<img loading="lazy" src="/wiki/f/results/rtx-5060-dr2-quiescent-full-spectrum/38646-M14_38646/diagnostics/spectral_chi2.png" alt="M14_38646: spectral pull, binned mean pull squared, cumulative chi-squared">
<figcaption>Pull of only 3817 fitted spectrum pixels of galaxy M14_38646 against the model, 1.132 per pixel at a 5.72 percent error floor.</figcaption>
</figure>

<figure>
<img loading="lazy" src="/wiki/f/results/rtx-5060-dr2-quiescent-full-spectrum/38646-M14_38646/diagnostics/sf_timescales.png" alt="M14_38646: cumulative mass formed against lookback time with t10 to t90">
<figcaption>Mass formed in galaxy M14_38646 against lookback time: t10 4.81, t20 4.43, t50 3.24 Gyr, only a 16-84 percent range.</figcaption>
</figure>

38648-M14_38648
: z 0.6743 · S/N 52.7

<figure>
<img loading="lazy" src="/wiki/f/results/rtx-5060-dr2-quiescent-full-spectrum/38648-M14_38648/diagnostics/photometric_chi2.png" alt="M14_38648: photometric pull and chi-squared contribution per band">
<figcaption>Pull of only the 12 fitted bands of galaxy M14_38648 against the model, 16.59 per band at a 5 percent flux error floor.</figcaption>
</figure>

<figure>
<img loading="lazy" src="/wiki/f/results/rtx-5060-dr2-quiescent-full-spectrum/38648-M14_38648/diagnostics/spectral_chi2.png" alt="M14_38648: spectral pull, binned mean pull squared, cumulative chi-squared">
<figcaption>Pull of only 3566 fitted spectrum pixels of galaxy M14_38648 against the model, 1.081 per pixel at a 5.01 percent error floor.</figcaption>
</figure>

<figure>
<img loading="lazy" src="/wiki/f/results/rtx-5060-dr2-quiescent-full-spectrum/38648-M14_38648/diagnostics/sf_timescales.png" alt="M14_38648: cumulative mass formed against lookback time with t10 to t90">
<figcaption>Mass formed in galaxy M14_38648 against lookback time: t10 2.74, t20 2.47, t50 1.65 Gyr, only a 16-84 percent range.</figcaption>
</figure>

38771-M14_38771
: z 0.6758 · S/N 12.3

<figure>
<img loading="lazy" src="/wiki/f/results/rtx-5060-dr2-quiescent-full-spectrum/38771-M14_38771/diagnostics/photometric_chi2.png" alt="M14_38771: photometric pull and chi-squared contribution per band">
<figcaption>Pull of only the 12 fitted bands of galaxy M14_38771 against the model, 3.92 per band at a 5 percent flux error floor.</figcaption>
</figure>

<figure>
<img loading="lazy" src="/wiki/f/results/rtx-5060-dr2-quiescent-full-spectrum/38771-M14_38771/diagnostics/spectral_chi2.png" alt="M14_38771: spectral pull, binned mean pull squared, cumulative chi-squared">
<figcaption>Pull of only 3550 fitted spectrum pixels of galaxy M14_38771 against the model, 1.108 per pixel at a 7.60 percent error floor.</figcaption>
</figure>

<figure>
<img loading="lazy" src="/wiki/f/results/rtx-5060-dr2-quiescent-full-spectrum/38771-M14_38771/diagnostics/sf_timescales.png" alt="M14_38771: cumulative mass formed against lookback time with t10 to t90">
<figcaption>Mass formed in galaxy M14_38771 against lookback time: t10 7.01, t20 6.58, t50 5.29 Gyr, only a 16-84 percent range.</figcaption>
</figure>

39865-M14_39865
: z 0.8291 · S/N 6.8

<figure>
<img loading="lazy" src="/wiki/f/results/rtx-5060-dr2-quiescent-full-spectrum/39865-M14_39865/diagnostics/photometric_chi2.png" alt="M14_39865: photometric pull and chi-squared contribution per band">
<figcaption>Pull of only the 12 fitted bands of galaxy M14_39865 against the model, 2.66 per band at a 5 percent flux error floor.</figcaption>
</figure>

<figure>
<img loading="lazy" src="/wiki/f/results/rtx-5060-dr2-quiescent-full-spectrum/39865-M14_39865/diagnostics/spectral_chi2.png" alt="M14_39865: spectral pull, binned mean pull squared, cumulative chi-squared">
<figcaption>Pull of only 3438 fitted spectrum pixels of galaxy M14_39865 against the model, 1.106 per pixel at a 7.63 percent error floor.</figcaption>
</figure>

<figure>
<img loading="lazy" src="/wiki/f/results/rtx-5060-dr2-quiescent-full-spectrum/39865-M14_39865/diagnostics/sf_timescales.png" alt="M14_39865: cumulative mass formed against lookback time with t10 to t90">
<figcaption>Mass formed in galaxy M14_39865 against lookback time: t10 6.05, t20 5.48, t50 3.72 Gyr, only a 16-84 percent range.</figcaption>
</figure>

77632-M15_77632
: z 0.8253 · S/N 34.5

<figure>
<img loading="lazy" src="/wiki/f/results/rtx-5060-dr2-quiescent-full-spectrum/77632-M15_77632/diagnostics/photometric_chi2.png" alt="M15_77632: photometric pull and chi-squared contribution per band">
<figcaption>Pull of only the 12 fitted bands of galaxy M15_77632 against the model, 11.32 per band at a 5 percent flux error floor.</figcaption>
</figure>

<figure>
<img loading="lazy" src="/wiki/f/results/rtx-5060-dr2-quiescent-full-spectrum/77632-M15_77632/diagnostics/spectral_chi2.png" alt="M15_77632: spectral pull, binned mean pull squared, cumulative chi-squared">
<figcaption>Pull of only 3431 fitted spectrum pixels of galaxy M15_77632 against the model, 1.173 per pixel at a 4.18 percent error floor.</figcaption>
</figure>

<figure>
<img loading="lazy" src="/wiki/f/results/rtx-5060-dr2-quiescent-full-spectrum/77632-M15_77632/diagnostics/sf_timescales.png" alt="M15_77632: cumulative mass formed against lookback time with t10 to t90">
<figcaption>Mass formed in galaxy M15_77632 against lookback time: t10 4.63, t20 4.23, t50 3.03 Gyr, only a 16-84 percent range.</figcaption>
</figure>

77745-M15_77745
: z 0.8256 · S/N 30.7

<figure>
<img loading="lazy" src="/wiki/f/results/rtx-5060-dr2-quiescent-full-spectrum/77745-M15_77745/diagnostics/photometric_chi2.png" alt="M15_77745: photometric pull and chi-squared contribution per band">
<figcaption>Pull of only the 12 fitted bands of galaxy M15_77745 against the model, 5.56 per band at a 5 percent flux error floor.</figcaption>
</figure>

<figure>
<img loading="lazy" src="/wiki/f/results/rtx-5060-dr2-quiescent-full-spectrum/77745-M15_77745/diagnostics/spectral_chi2.png" alt="M15_77745: spectral pull, binned mean pull squared, cumulative chi-squared">
<figcaption>Pull of only 3450 fitted spectrum pixels of galaxy M15_77745 against the model, 1.146 per pixel at a 4.68 percent error floor.</figcaption>
</figure>

<figure>
<img loading="lazy" src="/wiki/f/results/rtx-5060-dr2-quiescent-full-spectrum/77745-M15_77745/diagnostics/sf_timescales.png" alt="M15_77745: cumulative mass formed against lookback time with t10 to t90">
<figcaption>Mass formed in galaxy M15_77745 against lookback time: t10 6.27, t20 5.91, t50 4.58 Gyr, only a 16-84 percent range.</figcaption>
</figure>

84337-M4_84337
: z 0.8388 · S/N 14.9

<figure>
<img loading="lazy" src="/wiki/f/results/rtx-5060-dr2-quiescent-full-spectrum/84337-M4_84337/diagnostics/photometric_chi2.png" alt="M4_84337: photometric pull and chi-squared contribution per band">
<figcaption>Pull of only the 12 fitted bands of galaxy M4_84337 against the model, 7.35 per band at a 5 percent flux error floor.</figcaption>
</figure>

<figure>
<img loading="lazy" src="/wiki/f/results/rtx-5060-dr2-quiescent-full-spectrum/84337-M4_84337/diagnostics/spectral_chi2.png" alt="M4_84337: spectral pull, binned mean pull squared, cumulative chi-squared">
<figcaption>Pull of only 3695 fitted spectrum pixels of galaxy M4_84337 against the model, 1.071 per pixel at a 5.76 percent error floor.</figcaption>
</figure>

<figure>
<img loading="lazy" src="/wiki/f/results/rtx-5060-dr2-quiescent-full-spectrum/84337-M4_84337/diagnostics/sf_timescales.png" alt="M4_84337: cumulative mass formed against lookback time with t10 to t90">
<figcaption>Mass formed in galaxy M4_84337 against lookback time: t10 6.15, t20 5.73, t50 4.23 Gyr, only a 16-84 percent range.</figcaption>
</figure>

87207-M15_87207
: z 0.8325 · S/N 7.5

<figure>
<img loading="lazy" src="/wiki/f/results/rtx-5060-dr2-quiescent-full-spectrum/87207-M15_87207/diagnostics/photometric_chi2.png" alt="M15_87207: photometric pull and chi-squared contribution per band">
<figcaption>Pull of only the 12 fitted bands of galaxy M15_87207 against the model, 3.28 per band at a 5 percent flux error floor.</figcaption>
</figure>

<figure>
<img loading="lazy" src="/wiki/f/results/rtx-5060-dr2-quiescent-full-spectrum/87207-M15_87207/diagnostics/spectral_chi2.png" alt="M15_87207: spectral pull, binned mean pull squared, cumulative chi-squared">
<figcaption>Pull of only 3813 fitted spectrum pixels of galaxy M15_87207 against the model, 1.207 per pixel at a 9.82 percent error floor.</figcaption>
</figure>

<figure>
<img loading="lazy" src="/wiki/f/results/rtx-5060-dr2-quiescent-full-spectrum/87207-M15_87207/diagnostics/sf_timescales.png" alt="M15_87207: cumulative mass formed against lookback time with t10 to t90">
<figcaption>Mass formed in galaxy M15_87207 against lookback time: t10 6.19, t20 5.78, t50 4.60 Gyr, only a 16-84 percent range.</figcaption>
</figure>

88032-M15_88032
: z 0.8392 · S/N 22.6

<figure>
<img loading="lazy" src="/wiki/f/results/rtx-5060-dr2-quiescent-full-spectrum/88032-M15_88032/diagnostics/photometric_chi2.png" alt="M15_88032: photometric pull and chi-squared contribution per band">
<figcaption>Pull of only the 12 fitted bands of galaxy M15_88032 against the model, 4.70 per band at a 5 percent flux error floor.</figcaption>
</figure>

<figure>
<img loading="lazy" src="/wiki/f/results/rtx-5060-dr2-quiescent-full-spectrum/88032-M15_88032/diagnostics/spectral_chi2.png" alt="M15_88032: spectral pull, binned mean pull squared, cumulative chi-squared">
<figcaption>Pull of only 3649 fitted spectrum pixels of galaxy M15_88032 against the model, 1.114 per pixel at a 5.39 percent error floor.</figcaption>
</figure>

<figure>
<img loading="lazy" src="/wiki/f/results/rtx-5060-dr2-quiescent-full-spectrum/88032-M15_88032/diagnostics/sf_timescales.png" alt="M15_88032: cumulative mass formed against lookback time with t10 to t90">
<figcaption>Mass formed in galaxy M15_88032 against lookback time: t10 4.58, t20 4.13, t50 2.81 Gyr, only a 16-84 percent range.</figcaption>
</figure>

89072-M15_89072
: z 0.8370 · S/N 7.1

<figure>
<img loading="lazy" src="/wiki/f/results/rtx-5060-dr2-quiescent-full-spectrum/89072-M15_89072/diagnostics/photometric_chi2.png" alt="M15_89072: photometric pull and chi-squared contribution per band">
<figcaption>Pull of only the 12 fitted bands of galaxy M15_89072 against the model, 2.31 per band at a 5 percent flux error floor.</figcaption>
</figure>

<figure>
<img loading="lazy" src="/wiki/f/results/rtx-5060-dr2-quiescent-full-spectrum/89072-M15_89072/diagnostics/spectral_chi2.png" alt="M15_89072: spectral pull, binned mean pull squared, cumulative chi-squared">
<figcaption>Pull of only 3661 fitted spectrum pixels of galaxy M15_89072 against the model, 1.154 per pixel at a 9.88 percent error floor.</figcaption>
</figure>

<figure>
<img loading="lazy" src="/wiki/f/results/rtx-5060-dr2-quiescent-full-spectrum/89072-M15_89072/diagnostics/sf_timescales.png" alt="M15_89072: cumulative mass formed against lookback time with t10 to t90">
<figcaption>Mass formed in galaxy M15_89072 against lookback time: t10 4.63, t20 4.20, t50 2.93 Gyr, only a 16-84 percent range.</figcaption>
</figure>

89153-M15_89153
: z 0.8351 · S/N 9.8

<figure>
<img loading="lazy" src="/wiki/f/results/rtx-5060-dr2-quiescent-full-spectrum/89153-M15_89153/diagnostics/photometric_chi2.png" alt="M15_89153: photometric pull and chi-squared contribution per band">
<figcaption>Pull of only the 12 fitted bands of galaxy M15_89153 against the model, 3.58 per band at a 5 percent flux error floor.</figcaption>
</figure>

<figure>
<img loading="lazy" src="/wiki/f/results/rtx-5060-dr2-quiescent-full-spectrum/89153-M15_89153/diagnostics/spectral_chi2.png" alt="M15_89153: spectral pull, binned mean pull squared, cumulative chi-squared">
<figcaption>Pull of only 3414 fitted spectrum pixels of galaxy M15_89153 against the model, 1.127 per pixel at a 9.36 percent error floor.</figcaption>
</figure>

<figure>
<img loading="lazy" src="/wiki/f/results/rtx-5060-dr2-quiescent-full-spectrum/89153-M15_89153/diagnostics/sf_timescales.png" alt="M15_89153: cumulative mass formed against lookback time with t10 to t90">
<figcaption>Mass formed in galaxy M15_89153 against lookback time: t10 2.76, t20 2.48, t50 1.64 Gyr, only a 16-84 percent range.</figcaption>
</figure>

91529-M12_91529
: z 0.8406 · S/N 34.8

<figure>
<img loading="lazy" src="/wiki/f/results/rtx-5060-dr2-quiescent-full-spectrum/91529-M12_91529/diagnostics/photometric_chi2.png" alt="M12_91529: photometric pull and chi-squared contribution per band">
<figcaption>Pull of only the 12 fitted bands of galaxy M12_91529 against the model, 5.12 per band at a 5 percent flux error floor.</figcaption>
</figure>

<figure>
<img loading="lazy" src="/wiki/f/results/rtx-5060-dr2-quiescent-full-spectrum/91529-M12_91529/diagnostics/spectral_chi2.png" alt="M12_91529: spectral pull, binned mean pull squared, cumulative chi-squared">
<figcaption>Pull of only 3821 fitted spectrum pixels of galaxy M12_91529 against the model, 1.106 per pixel at a 4.60 percent error floor.</figcaption>
</figure>

<figure>
<img loading="lazy" src="/wiki/f/results/rtx-5060-dr2-quiescent-full-spectrum/91529-M12_91529/diagnostics/sf_timescales.png" alt="M12_91529: cumulative mass formed against lookback time with t10 to t90">
<figcaption>Mass formed in galaxy M12_91529 against lookback time: t10 4.29, t20 3.56, t50 2.26 Gyr, only a 16-84 percent range.</figcaption>
</figure>

92132-M12_92132
: z 0.7475 · S/N 16.1

<figure>
<img loading="lazy" src="/wiki/f/results/rtx-5060-dr2-quiescent-full-spectrum/92132-M12_92132/diagnostics/photometric_chi2.png" alt="M12_92132: photometric pull and chi-squared contribution per band">
<figcaption>Pull of only the 12 fitted bands of galaxy M12_92132 against the model, 7.16 per band at a 5 percent flux error floor.</figcaption>
</figure>

<figure>
<img loading="lazy" src="/wiki/f/results/rtx-5060-dr2-quiescent-full-spectrum/92132-M12_92132/diagnostics/spectral_chi2.png" alt="M12_92132: spectral pull, binned mean pull squared, cumulative chi-squared">
<figcaption>Pull of only 3817 fitted spectrum pixels of galaxy M12_92132 against the model, 1.126 per pixel at a 6.63 percent error floor.</figcaption>
</figure>

<figure>
<img loading="lazy" src="/wiki/f/results/rtx-5060-dr2-quiescent-full-spectrum/92132-M12_92132/diagnostics/sf_timescales.png" alt="M12_92132: cumulative mass formed against lookback time with t10 to t90">
<figcaption>Mass formed in galaxy M12_92132 against lookback time: t10 4.54, t20 4.05, t50 2.69 Gyr, only a 16-84 percent range.</figcaption>
</figure>

93943-M2_93943
: z 0.8800 · S/N 13.1

<figure>
<img loading="lazy" src="/wiki/f/results/rtx-5060-dr2-quiescent-full-spectrum/93943-M2_93943/diagnostics/photometric_chi2.png" alt="M2_93943: photometric pull and chi-squared contribution per band">
<figcaption>Pull of only the 12 fitted bands of galaxy M2_93943 against the model, 9.15 per band at a 5 percent flux error floor.</figcaption>
</figure>

<figure>
<img loading="lazy" src="/wiki/f/results/rtx-5060-dr2-quiescent-full-spectrum/93943-M2_93943/diagnostics/spectral_chi2.png" alt="M2_93943: spectral pull, binned mean pull squared, cumulative chi-squared">
<figcaption>Pull of only 3836 fitted spectrum pixels of galaxy M2_93943 against the model, 1.011 per pixel at a 3.72 percent error floor.</figcaption>
</figure>

<figure>
<img loading="lazy" src="/wiki/f/results/rtx-5060-dr2-quiescent-full-spectrum/93943-M2_93943/diagnostics/sf_timescales.png" alt="M2_93943: cumulative mass formed against lookback time with t10 to t90">
<figcaption>Mass formed in galaxy M2_93943 against lookback time: t10 2.74, t20 2.46, t50 1.65 Gyr, only a 16-84 percent range.</figcaption>
</figure>

94494-M2_94494
: z 0.7401 · S/N 30.6

<figure>
<img loading="lazy" src="/wiki/f/results/rtx-5060-dr2-quiescent-full-spectrum/94494-M2_94494/diagnostics/photometric_chi2.png" alt="M2_94494: photometric pull and chi-squared contribution per band">
<figcaption>Pull of only the 12 fitted bands of galaxy M2_94494 against the model, 6.15 per band at a 5 percent flux error floor.</figcaption>
</figure>

<figure>
<img loading="lazy" src="/wiki/f/results/rtx-5060-dr2-quiescent-full-spectrum/94494-M2_94494/diagnostics/spectral_chi2.png" alt="M2_94494: spectral pull, binned mean pull squared, cumulative chi-squared">
<figcaption>Pull of only 3530 fitted spectrum pixels of galaxy M2_94494 against the model, 1.044 per pixel at a 4.04 percent error floor.</figcaption>
</figure>

<figure>
<img loading="lazy" src="/wiki/f/results/rtx-5060-dr2-quiescent-full-spectrum/94494-M2_94494/diagnostics/sf_timescales.png" alt="M2_94494: cumulative mass formed against lookback time with t10 to t90">
<figcaption>Mass formed in galaxy M2_94494 against lookback time: t10 4.59, t20 4.16, t50 2.90 Gyr, only a 16-84 percent range.</figcaption>
</figure>

97310-M2_97310
: z 0.9428 · S/N 6.9

<figure>
<img loading="lazy" src="/wiki/f/results/rtx-5060-dr2-quiescent-full-spectrum/97310-M2_97310/diagnostics/photometric_chi2.png" alt="M2_97310: photometric pull and chi-squared contribution per band">
<figcaption>Pull of only the 12 fitted bands of galaxy M2_97310 against the model, 3.45 per band at a 5 percent flux error floor.</figcaption>
</figure>

<figure>
<img loading="lazy" src="/wiki/f/results/rtx-5060-dr2-quiescent-full-spectrum/97310-M2_97310/diagnostics/spectral_chi2.png" alt="M2_97310: spectral pull, binned mean pull squared, cumulative chi-squared">
<figcaption>Pull of only 3806 fitted spectrum pixels of galaxy M2_97310 against the model, 0.972 per pixel at a 5.18 percent error floor.</figcaption>
</figure>

<figure>
<img loading="lazy" src="/wiki/f/results/rtx-5060-dr2-quiescent-full-spectrum/97310-M2_97310/diagnostics/sf_timescales.png" alt="M2_97310: cumulative mass formed against lookback time with t10 to t90">
<figcaption>Mass formed in galaxy M2_97310 against lookback time: t10 2.88, t20 2.60, t50 1.75 Gyr, only a 16-84 percent range.</figcaption>
</figure>

98104-M12_98104
: z 0.9814 · S/N 6.6

<figure>
<img loading="lazy" src="/wiki/f/results/rtx-5060-dr2-quiescent-full-spectrum/98104-M12_98104/diagnostics/photometric_chi2.png" alt="M12_98104: photometric pull and chi-squared contribution per band">
<figcaption>Pull of only the 12 fitted bands of galaxy M12_98104 against the model, 4.06 per band at a 5 percent flux error floor.</figcaption>
</figure>

<figure>
<img loading="lazy" src="/wiki/f/results/rtx-5060-dr2-quiescent-full-spectrum/98104-M12_98104/diagnostics/spectral_chi2.png" alt="M12_98104: spectral pull, binned mean pull squared, cumulative chi-squared">
<figcaption>Pull of only 3804 fitted spectrum pixels of galaxy M12_98104 against the model, 1.554 per pixel at a 9.98 percent error floor.</figcaption>
</figure>

<figure>
<img loading="lazy" src="/wiki/f/results/rtx-5060-dr2-quiescent-full-spectrum/98104-M12_98104/diagnostics/sf_timescales.png" alt="M12_98104: cumulative mass formed against lookback time with t10 to t90">
<figcaption>Mass formed in galaxy M12_98104 against lookback time: t10 4.61, t20 4.21, t50 3.00 Gyr, only a 16-84 percent range.</figcaption>
</figure>

<details>
<summary>Details</summary>

Per-galaxy numbers, 75 columns, one row per galaxy: `results/per-galaxy-diagnostics.csv`.

Each galaxy's own settings, redshift and seed: `results/rtx-5060-dr2-quiescent-full-spectrum/<target>/diagnostics/model_parameters.txt`.

```
ceridwen/.venv/bin/python scripts/per_galaxy_diagnostics.py run
ceridwen/.venv/bin/python scripts/per_galaxy_diagnostics.py gallery
```

</details>
