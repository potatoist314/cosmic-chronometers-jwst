---
title: Per-galaxy fit diagnostics, gallery
date: 2026-09-05
section: Analyses
tags: [dr2-quiescent-sample, ceridwen, diagnostics]
job: t_8a78968d
---

187 galaxies. Method, checks and flags: [Per-galaxy fit diagnostics](../per-galaxy-fit-diagnostics/).

### 101089-M12_101089

| z | S/N | photometry χ²/N | spectrum χ²/N | f_calib | t50 [Gyr] | model |
| --- | --- | --- | --- | --- | --- | --- |
| 0.8510 | 8.3 | 1.48 | 2.340 | 9.99% | 5.24 | [parameters](/wiki/f/results/rtx-5060-dr2-quiescent-full-spectrum/101089-M12_101089/diagnostics/model_parameters.txt) |

Flags:

- spectrum chi2/N 2.34 > 1.5
- calibration floor at prior bound (10.0% of 10%)
- 57 pixels with |pull| > 4

<figure>
<img loading="lazy" src="/wiki/f/results/rtx-5060-dr2-quiescent-full-spectrum/101089-M12_101089/diagnostics/photometric_chi2.png" alt="M12_101089: photometric pull and chi-squared contribution per band">
<figcaption><code>photometric_chi2.png</code> Pull and chi-squared contribution for the 12 COSMOS2015 bands of galaxy M12_101089. Pull equals observed minus model over sigma. Uncertainty: sigma includes the 5 percent flux floor. Comparison: filled points use the posterior-median model. Open squares use the best sample with the fit's own sigma. Total chi-squared 17.8 over 12 bands gives 1.48 per band. Caveat: the spectrum dominates the joint fit, so the fit does not constrain the bands on their own.</figcaption>
</figure>

<figure>
<img loading="lazy" src="/wiki/f/results/rtx-5060-dr2-quiescent-full-spectrum/101089-M12_101089/diagnostics/spectral_chi2.png" alt="M12_101089: spectral pull, binned mean pull squared, cumulative chi-squared">
<figcaption><code>spectral_chi2.png</code> Pull per fitted pixel of the LEGA-C spectrum of galaxy M12_101089. Below it: mean pull squared in 25 Å bins and the cumulative chi-squared fraction against wavelength. Uncertainty: sigma includes the fitted calibration floor of 9.99 percent of the model flux. Comparison: the stored pull versus the pull at the best sample. Shaded bands mark masked pixels. Red points mark pixels with pull beyond 4 sigma. Total chi-squared 8026.7 over 3430 pixels, 57 outlier pixels. Caveat: the fitted floor absorbs model mismatch, so chi-squared near 1 does not prove a good model.</figcaption>
</figure>

<figure>
<img loading="lazy" src="/wiki/f/results/rtx-5060-dr2-quiescent-full-spectrum/101089-M12_101089/diagnostics/sf_timescales.png" alt="M12_101089: cumulative mass formed against lookback time with t10 to t90">
<figcaption><code>sf_timescales.png</code> Fraction of the final stellar mass of galaxy M12_101089 formed earlier than each lookback time. The line is the posterior median. The band is the 16-84 percent range over 400 draws. Comparison: points mark t10 to t90 with 16-84 percent (thick) and 2.5-97.5 percent (thin) intervals versus the universe age. t50 is 5.24 Gyr with a 16-84 percent range of 3.85 to 5.40 Gyr. Caveat: the 7-bin star-formation history model quantises these times to the bin edges.</figcaption>
</figure>

### 101830-M12_101830

| z | S/N | photometry χ²/N | spectrum χ²/N | f_calib | t50 [Gyr] | model |
| --- | --- | --- | --- | --- | --- | --- |
| 0.9874 | 11.3 | 6.95 | 1.537 | 9.98% | 3.22 | [parameters](/wiki/f/results/rtx-5060-dr2-quiescent-full-spectrum/101830-M12_101830/diagnostics/model_parameters.txt) |

Flags:

- photometry chi2/N 6.9 > 3
- spectrum chi2/N 1.54 > 1.5
- calibration floor at prior bound (10.0% of 10%)
- 24 pixels with |pull| > 4

<figure>
<img loading="lazy" src="/wiki/f/results/rtx-5060-dr2-quiescent-full-spectrum/101830-M12_101830/diagnostics/photometric_chi2.png" alt="M12_101830: photometric pull and chi-squared contribution per band">
<figcaption><code>photometric_chi2.png</code> Pull and chi-squared contribution for the 12 COSMOS2015 bands of galaxy M12_101830. Pull equals observed minus model over sigma. Uncertainty: sigma includes the 5 percent flux floor. Comparison: filled points use the posterior-median model. Open squares use the best sample with the fit's own sigma. Total chi-squared 83.4 over 12 bands gives 6.95 per band. Caveat: the spectrum dominates the joint fit, so the fit does not constrain the bands on their own.</figcaption>
</figure>

<figure>
<img loading="lazy" src="/wiki/f/results/rtx-5060-dr2-quiescent-full-spectrum/101830-M12_101830/diagnostics/spectral_chi2.png" alt="M12_101830: spectral pull, binned mean pull squared, cumulative chi-squared">
<figcaption><code>spectral_chi2.png</code> Pull per fitted pixel of the LEGA-C spectrum of galaxy M12_101830. Below it: mean pull squared in 25 Å bins and the cumulative chi-squared fraction against wavelength. Uncertainty: sigma includes the fitted calibration floor of 9.98 percent of the model flux. Comparison: the stored pull versus the pull at the best sample. Shaded bands mark masked pixels. Red points mark pixels with pull beyond 4 sigma. Total chi-squared 5861.2 over 3814 pixels, 24 outlier pixels. Caveat: the fitted floor absorbs model mismatch, so chi-squared near 1 does not prove a good model.</figcaption>
</figure>

<figure>
<img loading="lazy" src="/wiki/f/results/rtx-5060-dr2-quiescent-full-spectrum/101830-M12_101830/diagnostics/sf_timescales.png" alt="M12_101830: cumulative mass formed against lookback time with t10 to t90">
<figcaption><code>sf_timescales.png</code> Fraction of the final stellar mass of galaxy M12_101830 formed earlier than each lookback time. The line is the posterior median. The band is the 16-84 percent range over 400 draws. Comparison: points mark t10 to t90 with 16-84 percent (thick) and 2.5-97.5 percent (thin) intervals versus the universe age. t50 is 3.22 Gyr with a 16-84 percent range of 3.01 to 3.68 Gyr. Caveat: the 7-bin star-formation history model quantises these times to the bin edges.</figcaption>
</figure>

### 102456-M12_102456

| z | S/N | photometry χ²/N | spectrum χ²/N | f_calib | t50 [Gyr] | model |
| --- | --- | --- | --- | --- | --- | --- |
| 0.6779 | 34.9 | 14.22 | 1.191 | 5.90% | 3.61 | [parameters](/wiki/f/results/rtx-5060-dr2-quiescent-full-spectrum/102456-M12_102456/diagnostics/model_parameters.txt) |

Flags:

- photometry chi2/N 14.2 > 3
- 10 pixels with |pull| > 4

<figure>
<img loading="lazy" src="/wiki/f/results/rtx-5060-dr2-quiescent-full-spectrum/102456-M12_102456/diagnostics/photometric_chi2.png" alt="M12_102456: photometric pull and chi-squared contribution per band">
<figcaption><code>photometric_chi2.png</code> Pull and chi-squared contribution for the 12 COSMOS2015 bands of galaxy M12_102456. Pull equals observed minus model over sigma. Uncertainty: sigma includes the 5 percent flux floor. Comparison: filled points use the posterior-median model. Open squares use the best sample with the fit's own sigma. Total chi-squared 170.6 over 12 bands gives 14.22 per band. Caveat: the spectrum dominates the joint fit, so the fit does not constrain the bands on their own.</figcaption>
</figure>

<figure>
<img loading="lazy" src="/wiki/f/results/rtx-5060-dr2-quiescent-full-spectrum/102456-M12_102456/diagnostics/spectral_chi2.png" alt="M12_102456: spectral pull, binned mean pull squared, cumulative chi-squared">
<figcaption><code>spectral_chi2.png</code> Pull per fitted pixel of the LEGA-C spectrum of galaxy M12_102456. Below it: mean pull squared in 25 Å bins and the cumulative chi-squared fraction against wavelength. Uncertainty: sigma includes the fitted calibration floor of 5.90 percent of the model flux. Comparison: the stored pull versus the pull at the best sample. Shaded bands mark masked pixels. Red points mark pixels with pull beyond 4 sigma. Total chi-squared 4124.0 over 3463 pixels, 10 outlier pixels. Caveat: the fitted floor absorbs model mismatch, so chi-squared near 1 does not prove a good model.</figcaption>
</figure>

<figure>
<img loading="lazy" src="/wiki/f/results/rtx-5060-dr2-quiescent-full-spectrum/102456-M12_102456/diagnostics/sf_timescales.png" alt="M12_102456: cumulative mass formed against lookback time with t10 to t90">
<figcaption><code>sf_timescales.png</code> Fraction of the final stellar mass of galaxy M12_102456 formed earlier than each lookback time. The line is the posterior median. The band is the 16-84 percent range over 400 draws. Comparison: points mark t10 to t90 with 16-84 percent (thick) and 2.5-97.5 percent (thin) intervals versus the universe age. t50 is 3.61 Gyr with a 16-84 percent range of 3.37 to 3.78 Gyr. Caveat: the 7-bin star-formation history model quantises these times to the bin edges.</figcaption>
</figure>

### 102968-M14_102968

| z | S/N | photometry χ²/N | spectrum χ²/N | f_calib | t50 [Gyr] | model |
| --- | --- | --- | --- | --- | --- | --- |
| 0.9393 | 9.5 | 12.50 | 1.099 | 5.93% | 3.56 | [parameters](/wiki/f/results/rtx-5060-dr2-quiescent-full-spectrum/102968-M14_102968/diagnostics/model_parameters.txt) |

Flags:

- photometry chi2/N 12.5 > 3
- 1 pixels with |pull| > 4

<figure>
<img loading="lazy" src="/wiki/f/results/rtx-5060-dr2-quiescent-full-spectrum/102968-M14_102968/diagnostics/photometric_chi2.png" alt="M14_102968: photometric pull and chi-squared contribution per band">
<figcaption><code>photometric_chi2.png</code> Pull and chi-squared contribution for the 12 COSMOS2015 bands of galaxy M14_102968. Pull equals observed minus model over sigma. Uncertainty: sigma includes the 5 percent flux floor. Comparison: filled points use the posterior-median model. Open squares use the best sample with the fit's own sigma. Total chi-squared 150.0 over 12 bands gives 12.50 per band. Caveat: the spectrum dominates the joint fit, so the fit does not constrain the bands on their own.</figcaption>
</figure>

<figure>
<img loading="lazy" src="/wiki/f/results/rtx-5060-dr2-quiescent-full-spectrum/102968-M14_102968/diagnostics/spectral_chi2.png" alt="M14_102968: spectral pull, binned mean pull squared, cumulative chi-squared">
<figcaption><code>spectral_chi2.png</code> Pull per fitted pixel of the LEGA-C spectrum of galaxy M14_102968. Below it: mean pull squared in 25 Å bins and the cumulative chi-squared fraction against wavelength. Uncertainty: sigma includes the fitted calibration floor of 5.93 percent of the model flux. Comparison: the stored pull versus the pull at the best sample. Shaded bands mark masked pixels. Red points mark pixels with pull beyond 4 sigma. Total chi-squared 4189.0 over 3813 pixels, 1 outlier pixels. Caveat: the fitted floor absorbs model mismatch, so chi-squared near 1 does not prove a good model.</figcaption>
</figure>

<figure>
<img loading="lazy" src="/wiki/f/results/rtx-5060-dr2-quiescent-full-spectrum/102968-M14_102968/diagnostics/sf_timescales.png" alt="M14_102968: cumulative mass formed against lookback time with t10 to t90">
<figcaption><code>sf_timescales.png</code> Fraction of the final stellar mass of galaxy M14_102968 formed earlier than each lookback time. The line is the posterior median. The band is the 16-84 percent range over 400 draws. Comparison: points mark t10 to t90 with 16-84 percent (thick) and 2.5-97.5 percent (thin) intervals versus the universe age. t50 is 3.56 Gyr with a 16-84 percent range of 3.10 to 3.90 Gyr. Caveat: the 7-bin star-formation history model quantises these times to the bin edges.</figcaption>
</figure>

### 103366-M14_103366

| z | S/N | photometry χ²/N | spectrum χ²/N | f_calib | t50 [Gyr] | model |
| --- | --- | --- | --- | --- | --- | --- |
| 0.6742 | 14.3 | 2.92 | 1.133 | 5.25% | 3.43 | [parameters](/wiki/f/results/rtx-5060-dr2-quiescent-full-spectrum/103366-M14_103366/diagnostics/model_parameters.txt) |

Flags:

- 3 pixels with |pull| > 4

<figure>
<img loading="lazy" src="/wiki/f/results/rtx-5060-dr2-quiescent-full-spectrum/103366-M14_103366/diagnostics/photometric_chi2.png" alt="M14_103366: photometric pull and chi-squared contribution per band">
<figcaption><code>photometric_chi2.png</code> Pull and chi-squared contribution for the 12 COSMOS2015 bands of galaxy M14_103366. Pull equals observed minus model over sigma. Uncertainty: sigma includes the 5 percent flux floor. Comparison: filled points use the posterior-median model. Open squares use the best sample with the fit's own sigma. Total chi-squared 35.0 over 12 bands gives 2.92 per band. Caveat: the spectrum dominates the joint fit, so the fit does not constrain the bands on their own.</figcaption>
</figure>

<figure>
<img loading="lazy" src="/wiki/f/results/rtx-5060-dr2-quiescent-full-spectrum/103366-M14_103366/diagnostics/spectral_chi2.png" alt="M14_103366: spectral pull, binned mean pull squared, cumulative chi-squared">
<figcaption><code>spectral_chi2.png</code> Pull per fitted pixel of the LEGA-C spectrum of galaxy M14_103366. Below it: mean pull squared in 25 Å bins and the cumulative chi-squared fraction against wavelength. Uncertainty: sigma includes the fitted calibration floor of 5.25 percent of the model flux. Comparison: the stored pull versus the pull at the best sample. Shaded bands mark masked pixels. Red points mark pixels with pull beyond 4 sigma. Total chi-squared 4019.3 over 3547 pixels, 3 outlier pixels. Caveat: the fitted floor absorbs model mismatch, so chi-squared near 1 does not prove a good model.</figcaption>
</figure>

<figure>
<img loading="lazy" src="/wiki/f/results/rtx-5060-dr2-quiescent-full-spectrum/103366-M14_103366/diagnostics/sf_timescales.png" alt="M14_103366: cumulative mass formed against lookback time with t10 to t90">
<figcaption><code>sf_timescales.png</code> Fraction of the final stellar mass of galaxy M14_103366 formed earlier than each lookback time. The line is the posterior median. The band is the 16-84 percent range over 400 draws. Comparison: points mark t10 to t90 with 16-84 percent (thick) and 2.5-97.5 percent (thin) intervals versus the universe age. t50 is 3.43 Gyr with a 16-84 percent range of 2.64 to 4.85 Gyr. Caveat: the 7-bin star-formation history model quantises these times to the bin edges.</figcaption>
</figure>

### 104877-M14_104877

| z | S/N | photometry χ²/N | spectrum χ²/N | f_calib | t50 [Gyr] | model |
| --- | --- | --- | --- | --- | --- | --- |
| 0.9544 | 3.6 | 7.39 | 1.776 | 9.97% | 0.05 | [parameters](/wiki/f/results/rtx-5060-dr2-quiescent-full-spectrum/104877-M14_104877/diagnostics/model_parameters.txt) |

Flags:

- photometry chi2/N 7.4 > 3
- spectrum chi2/N 1.78 > 1.5
- calibration floor at prior bound (10.0% of 10%)
- 19 pixels with |pull| > 4

<figure>
<img loading="lazy" src="/wiki/f/results/rtx-5060-dr2-quiescent-full-spectrum/104877-M14_104877/diagnostics/photometric_chi2.png" alt="M14_104877: photometric pull and chi-squared contribution per band">
<figcaption><code>photometric_chi2.png</code> Pull and chi-squared contribution for the 12 COSMOS2015 bands of galaxy M14_104877. Pull equals observed minus model over sigma. Uncertainty: sigma includes the 5 percent flux floor. Comparison: filled points use the posterior-median model. Open squares use the best sample with the fit's own sigma. Total chi-squared 88.6 over 12 bands gives 7.39 per band. Caveat: the spectrum dominates the joint fit, so the fit does not constrain the bands on their own.</figcaption>
</figure>

<figure>
<img loading="lazy" src="/wiki/f/results/rtx-5060-dr2-quiescent-full-spectrum/104877-M14_104877/diagnostics/spectral_chi2.png" alt="M14_104877: spectral pull, binned mean pull squared, cumulative chi-squared">
<figcaption><code>spectral_chi2.png</code> Pull per fitted pixel of the LEGA-C spectrum of galaxy M14_104877. Below it: mean pull squared in 25 Å bins and the cumulative chi-squared fraction against wavelength. Uncertainty: sigma includes the fitted calibration floor of 9.97 percent of the model flux. Comparison: the stored pull versus the pull at the best sample. Shaded bands mark masked pixels. Red points mark pixels with pull beyond 4 sigma. Total chi-squared 6748.6 over 3800 pixels, 19 outlier pixels. Caveat: the fitted floor absorbs model mismatch, so chi-squared near 1 does not prove a good model.</figcaption>
</figure>

<figure>
<img loading="lazy" src="/wiki/f/results/rtx-5060-dr2-quiescent-full-spectrum/104877-M14_104877/diagnostics/sf_timescales.png" alt="M14_104877: cumulative mass formed against lookback time with t10 to t90">
<figcaption><code>sf_timescales.png</code> Fraction of the final stellar mass of galaxy M14_104877 formed earlier than each lookback time. The line is the posterior median. The band is the 16-84 percent range over 400 draws. Comparison: points mark t10 to t90 with 16-84 percent (thick) and 2.5-97.5 percent (thin) intervals versus the universe age. t50 is 0.05 Gyr with a 16-84 percent range of 0.04 to 0.13 Gyr. Caveat: the 7-bin star-formation history model quantises these times to the bin edges.</figcaption>
</figure>

### 105474-M4_105474

| z | S/N | photometry χ²/N | spectrum χ²/N | f_calib | t50 [Gyr] | model |
| --- | --- | --- | --- | --- | --- | --- |
| 0.6732 | 37.3 | 13.04 | 1.095 | 5.85% | 0.80 | [parameters](/wiki/f/results/rtx-5060-dr2-quiescent-full-spectrum/105474-M4_105474/diagnostics/model_parameters.txt) |

Flags:

- photometry chi2/N 13.0 > 3
- 3 pixels with |pull| > 4

<figure>
<img loading="lazy" src="/wiki/f/results/rtx-5060-dr2-quiescent-full-spectrum/105474-M4_105474/diagnostics/photometric_chi2.png" alt="M4_105474: photometric pull and chi-squared contribution per band">
<figcaption><code>photometric_chi2.png</code> Pull and chi-squared contribution for the 12 COSMOS2015 bands of galaxy M4_105474. Pull equals observed minus model over sigma. Uncertainty: sigma includes the 5 percent flux floor. Comparison: filled points use the posterior-median model. Open squares use the best sample with the fit's own sigma. Total chi-squared 156.4 over 12 bands gives 13.04 per band. Caveat: the spectrum dominates the joint fit, so the fit does not constrain the bands on their own.</figcaption>
</figure>

<figure>
<img loading="lazy" src="/wiki/f/results/rtx-5060-dr2-quiescent-full-spectrum/105474-M4_105474/diagnostics/spectral_chi2.png" alt="M4_105474: spectral pull, binned mean pull squared, cumulative chi-squared">
<figcaption><code>spectral_chi2.png</code> Pull per fitted pixel of the LEGA-C spectrum of galaxy M4_105474. Below it: mean pull squared in 25 Å bins and the cumulative chi-squared fraction against wavelength. Uncertainty: sigma includes the fitted calibration floor of 5.85 percent of the model flux. Comparison: the stored pull versus the pull at the best sample. Shaded bands mark masked pixels. Red points mark pixels with pull beyond 4 sigma. Total chi-squared 3712.2 over 3389 pixels, 3 outlier pixels. Caveat: the fitted floor absorbs model mismatch, so chi-squared near 1 does not prove a good model.</figcaption>
</figure>

<figure>
<img loading="lazy" src="/wiki/f/results/rtx-5060-dr2-quiescent-full-spectrum/105474-M4_105474/diagnostics/sf_timescales.png" alt="M4_105474: cumulative mass formed against lookback time with t10 to t90">
<figcaption><code>sf_timescales.png</code> Fraction of the final stellar mass of galaxy M4_105474 formed earlier than each lookback time. The line is the posterior median. The band is the 16-84 percent range over 400 draws. Comparison: points mark t10 to t90 with 16-84 percent (thick) and 2.5-97.5 percent (thin) intervals versus the universe age. t50 is 0.80 Gyr with a 16-84 percent range of 0.77 to 0.83 Gyr. Caveat: the 7-bin star-formation history model quantises these times to the bin edges.</figcaption>
</figure>

### 107362-M3_107362

| z | S/N | photometry χ²/N | spectrum χ²/N | f_calib | t50 [Gyr] | model |
| --- | --- | --- | --- | --- | --- | --- |
| 0.6767 | 23.7 | 13.98 | 1.155 | 4.34% | 3.00 | [parameters](/wiki/f/results/rtx-5060-dr2-quiescent-full-spectrum/107362-M3_107362/diagnostics/model_parameters.txt) |

Flags:

- photometry chi2/N 14.0 > 3
- 3 pixels with |pull| > 4

<figure>
<img loading="lazy" src="/wiki/f/results/rtx-5060-dr2-quiescent-full-spectrum/107362-M3_107362/diagnostics/photometric_chi2.png" alt="M3_107362: photometric pull and chi-squared contribution per band">
<figcaption><code>photometric_chi2.png</code> Pull and chi-squared contribution for the 12 COSMOS2015 bands of galaxy M3_107362. Pull equals observed minus model over sigma. Uncertainty: sigma includes the 5 percent flux floor. Comparison: filled points use the posterior-median model. Open squares use the best sample with the fit's own sigma. Total chi-squared 167.8 over 12 bands gives 13.98 per band. Caveat: the spectrum dominates the joint fit, so the fit does not constrain the bands on their own.</figcaption>
</figure>

<figure>
<img loading="lazy" src="/wiki/f/results/rtx-5060-dr2-quiescent-full-spectrum/107362-M3_107362/diagnostics/spectral_chi2.png" alt="M3_107362: spectral pull, binned mean pull squared, cumulative chi-squared">
<figcaption><code>spectral_chi2.png</code> Pull per fitted pixel of the LEGA-C spectrum of galaxy M3_107362. Below it: mean pull squared in 25 Å bins and the cumulative chi-squared fraction against wavelength. Uncertainty: sigma includes the fitted calibration floor of 4.34 percent of the model flux. Comparison: the stored pull versus the pull at the best sample. Shaded bands mark masked pixels. Red points mark pixels with pull beyond 4 sigma. Total chi-squared 4025.4 over 3484 pixels, 3 outlier pixels. Caveat: the fitted floor absorbs model mismatch, so chi-squared near 1 does not prove a good model.</figcaption>
</figure>

<figure>
<img loading="lazy" src="/wiki/f/results/rtx-5060-dr2-quiescent-full-spectrum/107362-M3_107362/diagnostics/sf_timescales.png" alt="M3_107362: cumulative mass formed against lookback time with t10 to t90">
<figcaption><code>sf_timescales.png</code> Fraction of the final stellar mass of galaxy M3_107362 formed earlier than each lookback time. The line is the posterior median. The band is the 16-84 percent range over 400 draws. Comparison: points mark t10 to t90 with 16-84 percent (thick) and 2.5-97.5 percent (thin) intervals versus the universe age. t50 is 3.00 Gyr with a 16-84 percent range of 2.98 to 3.06 Gyr. Caveat: the 7-bin star-formation history model quantises these times to the bin edges.</figcaption>
</figure>

### 107370-M4_107370

| z | S/N | photometry χ²/N | spectrum χ²/N | f_calib | t50 [Gyr] | model |
| --- | --- | --- | --- | --- | --- | --- |
| 0.8436 | 17.8 | 4.00 | 1.129 | 6.02% | 2.91 | [parameters](/wiki/f/results/rtx-5060-dr2-quiescent-full-spectrum/107370-M4_107370/diagnostics/model_parameters.txt) |

Flags:

- photometry chi2/N 4.0 > 3
- 8 pixels with |pull| > 4

<figure>
<img loading="lazy" src="/wiki/f/results/rtx-5060-dr2-quiescent-full-spectrum/107370-M4_107370/diagnostics/photometric_chi2.png" alt="M4_107370: photometric pull and chi-squared contribution per band">
<figcaption><code>photometric_chi2.png</code> Pull and chi-squared contribution for the 12 COSMOS2015 bands of galaxy M4_107370. Pull equals observed minus model over sigma. Uncertainty: sigma includes the 5 percent flux floor. Comparison: filled points use the posterior-median model. Open squares use the best sample with the fit's own sigma. Total chi-squared 48.0 over 12 bands gives 4.00 per band. Caveat: the spectrum dominates the joint fit, so the fit does not constrain the bands on their own.</figcaption>
</figure>

<figure>
<img loading="lazy" src="/wiki/f/results/rtx-5060-dr2-quiescent-full-spectrum/107370-M4_107370/diagnostics/spectral_chi2.png" alt="M4_107370: spectral pull, binned mean pull squared, cumulative chi-squared">
<figcaption><code>spectral_chi2.png</code> Pull per fitted pixel of the LEGA-C spectrum of galaxy M4_107370. Below it: mean pull squared in 25 Å bins and the cumulative chi-squared fraction against wavelength. Uncertainty: sigma includes the fitted calibration floor of 6.02 percent of the model flux. Comparison: the stored pull versus the pull at the best sample. Shaded bands mark masked pixels. Red points mark pixels with pull beyond 4 sigma. Total chi-squared 3825.5 over 3388 pixels, 8 outlier pixels. Caveat: the fitted floor absorbs model mismatch, so chi-squared near 1 does not prove a good model.</figcaption>
</figure>

<figure>
<img loading="lazy" src="/wiki/f/results/rtx-5060-dr2-quiescent-full-spectrum/107370-M4_107370/diagnostics/sf_timescales.png" alt="M4_107370: cumulative mass formed against lookback time with t10 to t90">
<figcaption><code>sf_timescales.png</code> Fraction of the final stellar mass of galaxy M4_107370 formed earlier than each lookback time. The line is the posterior median. The band is the 16-84 percent range over 400 draws. Comparison: points mark t10 to t90 with 16-84 percent (thick) and 2.5-97.5 percent (thin) intervals versus the universe age. t50 is 2.91 Gyr with a 16-84 percent range of 2.84 to 2.98 Gyr. Caveat: the 7-bin star-formation history model quantises these times to the bin edges.</figcaption>
</figure>

### 107643-M4_107643

| z | S/N | photometry χ²/N | spectrum χ²/N | f_calib | t50 [Gyr] | model |
| --- | --- | --- | --- | --- | --- | --- |
| 0.7343 | 21.0 | 1.40 | 1.098 | 6.39% | 2.90 | [parameters](/wiki/f/results/rtx-5060-dr2-quiescent-full-spectrum/107643-M4_107643/diagnostics/model_parameters.txt) |

Flags:

- 8 pixels with |pull| > 4

<figure>
<img loading="lazy" src="/wiki/f/results/rtx-5060-dr2-quiescent-full-spectrum/107643-M4_107643/diagnostics/photometric_chi2.png" alt="M4_107643: photometric pull and chi-squared contribution per band">
<figcaption><code>photometric_chi2.png</code> Pull and chi-squared contribution for the 12 COSMOS2015 bands of galaxy M4_107643. Pull equals observed minus model over sigma. Uncertainty: sigma includes the 5 percent flux floor. Comparison: filled points use the posterior-median model. Open squares use the best sample with the fit's own sigma. Total chi-squared 16.8 over 12 bands gives 1.40 per band. Caveat: the spectrum dominates the joint fit, so the fit does not constrain the bands on their own.</figcaption>
</figure>

<figure>
<img loading="lazy" src="/wiki/f/results/rtx-5060-dr2-quiescent-full-spectrum/107643-M4_107643/diagnostics/spectral_chi2.png" alt="M4_107643: spectral pull, binned mean pull squared, cumulative chi-squared">
<figcaption><code>spectral_chi2.png</code> Pull per fitted pixel of the LEGA-C spectrum of galaxy M4_107643. Below it: mean pull squared in 25 Å bins and the cumulative chi-squared fraction against wavelength. Uncertainty: sigma includes the fitted calibration floor of 6.39 percent of the model flux. Comparison: the stored pull versus the pull at the best sample. Shaded bands mark masked pixels. Red points mark pixels with pull beyond 4 sigma. Total chi-squared 3837.2 over 3496 pixels, 8 outlier pixels. Caveat: the fitted floor absorbs model mismatch, so chi-squared near 1 does not prove a good model.</figcaption>
</figure>

<figure>
<img loading="lazy" src="/wiki/f/results/rtx-5060-dr2-quiescent-full-spectrum/107643-M4_107643/diagnostics/sf_timescales.png" alt="M4_107643: cumulative mass formed against lookback time with t10 to t90">
<figcaption><code>sf_timescales.png</code> Fraction of the final stellar mass of galaxy M4_107643 formed earlier than each lookback time. The line is the posterior median. The band is the 16-84 percent range over 400 draws. Comparison: points mark t10 to t90 with 16-84 percent (thick) and 2.5-97.5 percent (thin) intervals versus the universe age. t50 is 2.90 Gyr with a 16-84 percent range of 2.81 to 2.98 Gyr. Caveat: the 7-bin star-formation history model quantises these times to the bin edges.</figcaption>
</figure>

### 108989-M4_108989

| z | S/N | photometry χ²/N | spectrum χ²/N | f_calib | t50 [Gyr] | model |
| --- | --- | --- | --- | --- | --- | --- |
| 0.8278 | 21.3 | 11.28 | 1.196 | 4.64% | 4.72 | [parameters](/wiki/f/results/rtx-5060-dr2-quiescent-full-spectrum/108989-M4_108989/diagnostics/model_parameters.txt) |

Flags:

- photometry chi2/N 11.3 > 3
- 3 pixels with |pull| > 4

<figure>
<img loading="lazy" src="/wiki/f/results/rtx-5060-dr2-quiescent-full-spectrum/108989-M4_108989/diagnostics/photometric_chi2.png" alt="M4_108989: photometric pull and chi-squared contribution per band">
<figcaption><code>photometric_chi2.png</code> Pull and chi-squared contribution for the 12 COSMOS2015 bands of galaxy M4_108989. Pull equals observed minus model over sigma. Uncertainty: sigma includes the 5 percent flux floor. Comparison: filled points use the posterior-median model. Open squares use the best sample with the fit's own sigma. Total chi-squared 135.3 over 12 bands gives 11.28 per band. Caveat: the spectrum dominates the joint fit, so the fit does not constrain the bands on their own.</figcaption>
</figure>

<figure>
<img loading="lazy" src="/wiki/f/results/rtx-5060-dr2-quiescent-full-spectrum/108989-M4_108989/diagnostics/spectral_chi2.png" alt="M4_108989: spectral pull, binned mean pull squared, cumulative chi-squared">
<figcaption><code>spectral_chi2.png</code> Pull per fitted pixel of the LEGA-C spectrum of galaxy M4_108989. Below it: mean pull squared in 25 Å bins and the cumulative chi-squared fraction against wavelength. Uncertainty: sigma includes the fitted calibration floor of 4.64 percent of the model flux. Comparison: the stored pull versus the pull at the best sample. Shaded bands mark masked pixels. Red points mark pixels with pull beyond 4 sigma. Total chi-squared 4467.5 over 3735 pixels, 3 outlier pixels. Caveat: the fitted floor absorbs model mismatch, so chi-squared near 1 does not prove a good model.</figcaption>
</figure>

<figure>
<img loading="lazy" src="/wiki/f/results/rtx-5060-dr2-quiescent-full-spectrum/108989-M4_108989/diagnostics/sf_timescales.png" alt="M4_108989: cumulative mass formed against lookback time with t10 to t90">
<figcaption><code>sf_timescales.png</code> Fraction of the final stellar mass of galaxy M4_108989 formed earlier than each lookback time. The line is the posterior median. The band is the 16-84 percent range over 400 draws. Comparison: points mark t10 to t90 with 16-84 percent (thick) and 2.5-97.5 percent (thin) intervals versus the universe age. t50 is 4.72 Gyr with a 16-84 percent range of 4.64 to 4.82 Gyr. Caveat: the 7-bin star-formation history model quantises these times to the bin edges.</figcaption>
</figure>

### 109352-M3_109352

| z | S/N | photometry χ²/N | spectrum χ²/N | f_calib | t50 [Gyr] | model |
| --- | --- | --- | --- | --- | --- | --- |
| 0.7244 | 23.9 | 11.39 | 1.140 | 4.19% | 3.05 | [parameters](/wiki/f/results/rtx-5060-dr2-quiescent-full-spectrum/109352-M3_109352/diagnostics/model_parameters.txt) |

Flags:

- photometry chi2/N 11.4 > 3
- 10 pixels with |pull| > 4

<figure>
<img loading="lazy" src="/wiki/f/results/rtx-5060-dr2-quiescent-full-spectrum/109352-M3_109352/diagnostics/photometric_chi2.png" alt="M3_109352: photometric pull and chi-squared contribution per band">
<figcaption><code>photometric_chi2.png</code> Pull and chi-squared contribution for the 12 COSMOS2015 bands of galaxy M3_109352. Pull equals observed minus model over sigma. Uncertainty: sigma includes the 5 percent flux floor. Comparison: filled points use the posterior-median model. Open squares use the best sample with the fit's own sigma. Total chi-squared 136.7 over 12 bands gives 11.39 per band. Caveat: the spectrum dominates the joint fit, so the fit does not constrain the bands on their own.</figcaption>
</figure>

<figure>
<img loading="lazy" src="/wiki/f/results/rtx-5060-dr2-quiescent-full-spectrum/109352-M3_109352/diagnostics/spectral_chi2.png" alt="M3_109352: spectral pull, binned mean pull squared, cumulative chi-squared">
<figcaption><code>spectral_chi2.png</code> Pull per fitted pixel of the LEGA-C spectrum of galaxy M3_109352. Below it: mean pull squared in 25 Å bins and the cumulative chi-squared fraction against wavelength. Uncertainty: sigma includes the fitted calibration floor of 4.19 percent of the model flux. Comparison: the stored pull versus the pull at the best sample. Shaded bands mark masked pixels. Red points mark pixels with pull beyond 4 sigma. Total chi-squared 4025.0 over 3530 pixels, 10 outlier pixels. Caveat: the fitted floor absorbs model mismatch, so chi-squared near 1 does not prove a good model.</figcaption>
</figure>

<figure>
<img loading="lazy" src="/wiki/f/results/rtx-5060-dr2-quiescent-full-spectrum/109352-M3_109352/diagnostics/sf_timescales.png" alt="M3_109352: cumulative mass formed against lookback time with t10 to t90">
<figcaption><code>sf_timescales.png</code> Fraction of the final stellar mass of galaxy M3_109352 formed earlier than each lookback time. The line is the posterior median. The band is the 16-84 percent range over 400 draws. Comparison: points mark t10 to t90 with 16-84 percent (thick) and 2.5-97.5 percent (thin) intervals versus the universe age. t50 is 3.05 Gyr with a 16-84 percent range of 2.99 to 3.37 Gyr. Caveat: the 7-bin star-formation history model quantises these times to the bin edges.</figcaption>
</figure>

### 109713-M3_109713

| z | S/N | photometry χ²/N | spectrum χ²/N | f_calib | t50 [Gyr] | model |
| --- | --- | --- | --- | --- | --- | --- |
| 0.7275 | 24.2 | 6.91 | 1.177 | 4.36% | 2.99 | [parameters](/wiki/f/results/rtx-5060-dr2-quiescent-full-spectrum/109713-M3_109713/diagnostics/model_parameters.txt) |

Flags:

- photometry chi2/N 6.9 > 3
- 5 pixels with |pull| > 4

<figure>
<img loading="lazy" src="/wiki/f/results/rtx-5060-dr2-quiescent-full-spectrum/109713-M3_109713/diagnostics/photometric_chi2.png" alt="M3_109713: photometric pull and chi-squared contribution per band">
<figcaption><code>photometric_chi2.png</code> Pull and chi-squared contribution for the 12 COSMOS2015 bands of galaxy M3_109713. Pull equals observed minus model over sigma. Uncertainty: sigma includes the 5 percent flux floor. Comparison: filled points use the posterior-median model. Open squares use the best sample with the fit's own sigma. Total chi-squared 83.0 over 12 bands gives 6.91 per band. Caveat: the spectrum dominates the joint fit, so the fit does not constrain the bands on their own.</figcaption>
</figure>

<figure>
<img loading="lazy" src="/wiki/f/results/rtx-5060-dr2-quiescent-full-spectrum/109713-M3_109713/diagnostics/spectral_chi2.png" alt="M3_109713: spectral pull, binned mean pull squared, cumulative chi-squared">
<figcaption><code>spectral_chi2.png</code> Pull per fitted pixel of the LEGA-C spectrum of galaxy M3_109713. Below it: mean pull squared in 25 Å bins and the cumulative chi-squared fraction against wavelength. Uncertainty: sigma includes the fitted calibration floor of 4.36 percent of the model flux. Comparison: the stored pull versus the pull at the best sample. Shaded bands mark masked pixels. Red points mark pixels with pull beyond 4 sigma. Total chi-squared 4041.0 over 3434 pixels, 5 outlier pixels. Caveat: the fitted floor absorbs model mismatch, so chi-squared near 1 does not prove a good model.</figcaption>
</figure>

<figure>
<img loading="lazy" src="/wiki/f/results/rtx-5060-dr2-quiescent-full-spectrum/109713-M3_109713/diagnostics/sf_timescales.png" alt="M3_109713: cumulative mass formed against lookback time with t10 to t90">
<figcaption><code>sf_timescales.png</code> Fraction of the final stellar mass of galaxy M3_109713 formed earlier than each lookback time. The line is the posterior median. The band is the 16-84 percent range over 400 draws. Comparison: points mark t10 to t90 with 16-84 percent (thick) and 2.5-97.5 percent (thin) intervals versus the universe age. t50 is 2.99 Gyr with a 16-84 percent range of 2.94 to 3.10 Gyr. Caveat: the 7-bin star-formation history model quantises these times to the bin edges.</figcaption>
</figure>

### 109843-M3_109843

| z | S/N | photometry χ²/N | spectrum χ²/N | f_calib | t50 [Gyr] | model |
| --- | --- | --- | --- | --- | --- | --- |
| 0.7243 | 12.9 | 3.72 | 1.188 | 5.85% | 2.87 | [parameters](/wiki/f/results/rtx-5060-dr2-quiescent-full-spectrum/109843-M3_109843/diagnostics/model_parameters.txt) |

Flags:

- photometry chi2/N 3.7 > 3
- 2 pixels with |pull| > 4

<figure>
<img loading="lazy" src="/wiki/f/results/rtx-5060-dr2-quiescent-full-spectrum/109843-M3_109843/diagnostics/photometric_chi2.png" alt="M3_109843: photometric pull and chi-squared contribution per band">
<figcaption><code>photometric_chi2.png</code> Pull and chi-squared contribution for the 12 COSMOS2015 bands of galaxy M3_109843. Pull equals observed minus model over sigma. Uncertainty: sigma includes the 5 percent flux floor. Comparison: filled points use the posterior-median model. Open squares use the best sample with the fit's own sigma. Total chi-squared 44.7 over 12 bands gives 3.72 per band. Caveat: the spectrum dominates the joint fit, so the fit does not constrain the bands on their own.</figcaption>
</figure>

<figure>
<img loading="lazy" src="/wiki/f/results/rtx-5060-dr2-quiescent-full-spectrum/109843-M3_109843/diagnostics/spectral_chi2.png" alt="M3_109843: spectral pull, binned mean pull squared, cumulative chi-squared">
<figcaption><code>spectral_chi2.png</code> Pull per fitted pixel of the LEGA-C spectrum of galaxy M3_109843. Below it: mean pull squared in 25 Å bins and the cumulative chi-squared fraction against wavelength. Uncertainty: sigma includes the fitted calibration floor of 5.85 percent of the model flux. Comparison: the stored pull versus the pull at the best sample. Shaded bands mark masked pixels. Red points mark pixels with pull beyond 4 sigma. Total chi-squared 4059.3 over 3418 pixels, 2 outlier pixels. Caveat: the fitted floor absorbs model mismatch, so chi-squared near 1 does not prove a good model.</figcaption>
</figure>

<figure>
<img loading="lazy" src="/wiki/f/results/rtx-5060-dr2-quiescent-full-spectrum/109843-M3_109843/diagnostics/sf_timescales.png" alt="M3_109843: cumulative mass formed against lookback time with t10 to t90">
<figcaption><code>sf_timescales.png</code> Fraction of the final stellar mass of galaxy M3_109843 formed earlier than each lookback time. The line is the posterior median. The band is the 16-84 percent range over 400 draws. Comparison: points mark t10 to t90 with 16-84 percent (thick) and 2.5-97.5 percent (thin) intervals versus the universe age. t50 is 2.87 Gyr with a 16-84 percent range of 2.80 to 2.98 Gyr. Caveat: the 7-bin star-formation history model quantises these times to the bin edges.</figcaption>
</figure>

### 111390-M3_111390

| z | S/N | photometry χ²/N | spectrum χ²/N | f_calib | t50 [Gyr] | model |
| --- | --- | --- | --- | --- | --- | --- |
| 0.6673 | 32.4 | 16.52 | 1.200 | 3.39% | 2.98 | [parameters](/wiki/f/results/rtx-5060-dr2-quiescent-full-spectrum/111390-M3_111390/diagnostics/model_parameters.txt) |

Flags:

- photometry chi2/N 16.5 > 3
- 16 pixels with |pull| > 4

<figure>
<img loading="lazy" src="/wiki/f/results/rtx-5060-dr2-quiescent-full-spectrum/111390-M3_111390/diagnostics/photometric_chi2.png" alt="M3_111390: photometric pull and chi-squared contribution per band">
<figcaption><code>photometric_chi2.png</code> Pull and chi-squared contribution for the 12 COSMOS2015 bands of galaxy M3_111390. Pull equals observed minus model over sigma. Uncertainty: sigma includes the 5 percent flux floor. Comparison: filled points use the posterior-median model. Open squares use the best sample with the fit's own sigma. Total chi-squared 198.3 over 12 bands gives 16.52 per band. Caveat: the spectrum dominates the joint fit, so the fit does not constrain the bands on their own.</figcaption>
</figure>

<figure>
<img loading="lazy" src="/wiki/f/results/rtx-5060-dr2-quiescent-full-spectrum/111390-M3_111390/diagnostics/spectral_chi2.png" alt="M3_111390: spectral pull, binned mean pull squared, cumulative chi-squared">
<figcaption><code>spectral_chi2.png</code> Pull per fitted pixel of the LEGA-C spectrum of galaxy M3_111390. Below it: mean pull squared in 25 Å bins and the cumulative chi-squared fraction against wavelength. Uncertainty: sigma includes the fitted calibration floor of 3.39 percent of the model flux. Comparison: the stored pull versus the pull at the best sample. Shaded bands mark masked pixels. Red points mark pixels with pull beyond 4 sigma. Total chi-squared 4265.2 over 3553 pixels, 16 outlier pixels. Caveat: the fitted floor absorbs model mismatch, so chi-squared near 1 does not prove a good model.</figcaption>
</figure>

<figure>
<img loading="lazy" src="/wiki/f/results/rtx-5060-dr2-quiescent-full-spectrum/111390-M3_111390/diagnostics/sf_timescales.png" alt="M3_111390: cumulative mass formed against lookback time with t10 to t90">
<figcaption><code>sf_timescales.png</code> Fraction of the final stellar mass of galaxy M3_111390 formed earlier than each lookback time. The line is the posterior median. The band is the 16-84 percent range over 400 draws. Comparison: points mark t10 to t90 with 16-84 percent (thick) and 2.5-97.5 percent (thin) intervals versus the universe age. t50 is 2.98 Gyr with a 16-84 percent range of 2.90 to 3.01 Gyr. Caveat: the 7-bin star-formation history model quantises these times to the bin edges.</figcaption>
</figure>

### 112534-M4_112534

| z | S/N | photometry χ²/N | spectrum χ²/N | f_calib | t50 [Gyr] | model |
| --- | --- | --- | --- | --- | --- | --- |
| 0.9837 | 6.4 | 5.52 | 1.110 | 7.36% | 3.02 | [parameters](/wiki/f/results/rtx-5060-dr2-quiescent-full-spectrum/112534-M4_112534/diagnostics/model_parameters.txt) |

Flags:

- photometry chi2/N 5.5 > 3
- 10 pixels with |pull| > 4

<figure>
<img loading="lazy" src="/wiki/f/results/rtx-5060-dr2-quiescent-full-spectrum/112534-M4_112534/diagnostics/photometric_chi2.png" alt="M4_112534: photometric pull and chi-squared contribution per band">
<figcaption><code>photometric_chi2.png</code> Pull and chi-squared contribution for the 12 COSMOS2015 bands of galaxy M4_112534. Pull equals observed minus model over sigma. Uncertainty: sigma includes the 5 percent flux floor. Comparison: filled points use the posterior-median model. Open squares use the best sample with the fit's own sigma. Total chi-squared 66.3 over 12 bands gives 5.52 per band. Caveat: the spectrum dominates the joint fit, so the fit does not constrain the bands on their own.</figcaption>
</figure>

<figure>
<img loading="lazy" src="/wiki/f/results/rtx-5060-dr2-quiescent-full-spectrum/112534-M4_112534/diagnostics/spectral_chi2.png" alt="M4_112534: spectral pull, binned mean pull squared, cumulative chi-squared">
<figcaption><code>spectral_chi2.png</code> Pull per fitted pixel of the LEGA-C spectrum of galaxy M4_112534. Below it: mean pull squared in 25 Å bins and the cumulative chi-squared fraction against wavelength. Uncertainty: sigma includes the fitted calibration floor of 7.36 percent of the model flux. Comparison: the stored pull versus the pull at the best sample. Shaded bands mark masked pixels. Red points mark pixels with pull beyond 4 sigma. Total chi-squared 4247.7 over 3828 pixels, 10 outlier pixels. Caveat: the fitted floor absorbs model mismatch, so chi-squared near 1 does not prove a good model.</figcaption>
</figure>

<figure>
<img loading="lazy" src="/wiki/f/results/rtx-5060-dr2-quiescent-full-spectrum/112534-M4_112534/diagnostics/sf_timescales.png" alt="M4_112534: cumulative mass formed against lookback time with t10 to t90">
<figcaption><code>sf_timescales.png</code> Fraction of the final stellar mass of galaxy M4_112534 formed earlier than each lookback time. The line is the posterior median. The band is the 16-84 percent range over 400 draws. Comparison: points mark t10 to t90 with 16-84 percent (thick) and 2.5-97.5 percent (thin) intervals versus the universe age. t50 is 3.02 Gyr with a 16-84 percent range of 3.00 to 3.12 Gyr. Caveat: the 7-bin star-formation history model quantises these times to the bin edges.</figcaption>
</figure>

### 113852-M7_113852

| z | S/N | photometry χ²/N | spectrum χ²/N | f_calib | t50 [Gyr] | model |
| --- | --- | --- | --- | --- | --- | --- |
| 0.6752 | 39.5 | 24.53 | 1.149 | 4.23% | 3.01 | [parameters](/wiki/f/results/rtx-5060-dr2-quiescent-full-spectrum/113852-M7_113852/diagnostics/model_parameters.txt) |

Flags:

- photometry chi2/N 24.5 > 3
- 7 pixels with |pull| > 4

<figure>
<img loading="lazy" src="/wiki/f/results/rtx-5060-dr2-quiescent-full-spectrum/113852-M7_113852/diagnostics/photometric_chi2.png" alt="M7_113852: photometric pull and chi-squared contribution per band">
<figcaption><code>photometric_chi2.png</code> Pull and chi-squared contribution for the 12 COSMOS2015 bands of galaxy M7_113852. Pull equals observed minus model over sigma. Uncertainty: sigma includes the 5 percent flux floor. Comparison: filled points use the posterior-median model. Open squares use the best sample with the fit's own sigma. Total chi-squared 294.4 over 12 bands gives 24.53 per band. Caveat: the spectrum dominates the joint fit, so the fit does not constrain the bands on their own.</figcaption>
</figure>

<figure>
<img loading="lazy" src="/wiki/f/results/rtx-5060-dr2-quiescent-full-spectrum/113852-M7_113852/diagnostics/spectral_chi2.png" alt="M7_113852: spectral pull, binned mean pull squared, cumulative chi-squared">
<figcaption><code>spectral_chi2.png</code> Pull per fitted pixel of the LEGA-C spectrum of galaxy M7_113852. Below it: mean pull squared in 25 Å bins and the cumulative chi-squared fraction against wavelength. Uncertainty: sigma includes the fitted calibration floor of 4.23 percent of the model flux. Comparison: the stored pull versus the pull at the best sample. Shaded bands mark masked pixels. Red points mark pixels with pull beyond 4 sigma. Total chi-squared 4025.0 over 3504 pixels, 7 outlier pixels. Caveat: the fitted floor absorbs model mismatch, so chi-squared near 1 does not prove a good model.</figcaption>
</figure>

<figure>
<img loading="lazy" src="/wiki/f/results/rtx-5060-dr2-quiescent-full-spectrum/113852-M7_113852/diagnostics/sf_timescales.png" alt="M7_113852: cumulative mass formed against lookback time with t10 to t90">
<figcaption><code>sf_timescales.png</code> Fraction of the final stellar mass of galaxy M7_113852 formed earlier than each lookback time. The line is the posterior median. The band is the 16-84 percent range over 400 draws. Comparison: points mark t10 to t90 with 16-84 percent (thick) and 2.5-97.5 percent (thin) intervals versus the universe age. t50 is 3.01 Gyr with a 16-84 percent range of 3.00 to 3.04 Gyr. Caveat: the 7-bin star-formation history model quantises these times to the bin edges.</figcaption>
</figure>

### 117010-M3_117010

| z | S/N | photometry χ²/N | spectrum χ²/N | f_calib | t50 [Gyr] | model |
| --- | --- | --- | --- | --- | --- | --- |
| 0.6766 | 18.3 | 3.66 | 1.149 | 5.20% | 2.60 | [parameters](/wiki/f/results/rtx-5060-dr2-quiescent-full-spectrum/117010-M3_117010/diagnostics/model_parameters.txt) |

Flags:

- photometry chi2/N 3.7 > 3
- 2 pixels with |pull| > 4

<figure>
<img loading="lazy" src="/wiki/f/results/rtx-5060-dr2-quiescent-full-spectrum/117010-M3_117010/diagnostics/photometric_chi2.png" alt="M3_117010: photometric pull and chi-squared contribution per band">
<figcaption><code>photometric_chi2.png</code> Pull and chi-squared contribution for the 12 COSMOS2015 bands of galaxy M3_117010. Pull equals observed minus model over sigma. Uncertainty: sigma includes the 5 percent flux floor. Comparison: filled points use the posterior-median model. Open squares use the best sample with the fit's own sigma. Total chi-squared 43.9 over 12 bands gives 3.66 per band. Caveat: the spectrum dominates the joint fit, so the fit does not constrain the bands on their own.</figcaption>
</figure>

<figure>
<img loading="lazy" src="/wiki/f/results/rtx-5060-dr2-quiescent-full-spectrum/117010-M3_117010/diagnostics/spectral_chi2.png" alt="M3_117010: spectral pull, binned mean pull squared, cumulative chi-squared">
<figcaption><code>spectral_chi2.png</code> Pull per fitted pixel of the LEGA-C spectrum of galaxy M3_117010. Below it: mean pull squared in 25 Å bins and the cumulative chi-squared fraction against wavelength. Uncertainty: sigma includes the fitted calibration floor of 5.20 percent of the model flux. Comparison: the stored pull versus the pull at the best sample. Shaded bands mark masked pixels. Red points mark pixels with pull beyond 4 sigma. Total chi-squared 3922.6 over 3414 pixels, 2 outlier pixels. Caveat: the fitted floor absorbs model mismatch, so chi-squared near 1 does not prove a good model.</figcaption>
</figure>

<figure>
<img loading="lazy" src="/wiki/f/results/rtx-5060-dr2-quiescent-full-spectrum/117010-M3_117010/diagnostics/sf_timescales.png" alt="M3_117010: cumulative mass formed against lookback time with t10 to t90">
<figcaption><code>sf_timescales.png</code> Fraction of the final stellar mass of galaxy M3_117010 formed earlier than each lookback time. The line is the posterior median. The band is the 16-84 percent range over 400 draws. Comparison: points mark t10 to t90 with 16-84 percent (thick) and 2.5-97.5 percent (thin) intervals versus the universe age. t50 is 2.60 Gyr with a 16-84 percent range of 2.54 to 2.71 Gyr. Caveat: the 7-bin star-formation history model quantises these times to the bin edges.</figcaption>
</figure>

### 117400-M4_117400

| z | S/N | photometry χ²/N | spectrum χ²/N | f_calib | t50 [Gyr] | model |
| --- | --- | --- | --- | --- | --- | --- |
| 0.6687 | 36.1 | 10.56 | 1.136 | 5.10% | 2.95 | [parameters](/wiki/f/results/rtx-5060-dr2-quiescent-full-spectrum/117400-M4_117400/diagnostics/model_parameters.txt) |

Flags:

- photometry chi2/N 10.6 > 3
- 1 pixels with |pull| > 4

<figure>
<img loading="lazy" src="/wiki/f/results/rtx-5060-dr2-quiescent-full-spectrum/117400-M4_117400/diagnostics/photometric_chi2.png" alt="M4_117400: photometric pull and chi-squared contribution per band">
<figcaption><code>photometric_chi2.png</code> Pull and chi-squared contribution for the 12 COSMOS2015 bands of galaxy M4_117400. Pull equals observed minus model over sigma. Uncertainty: sigma includes the 5 percent flux floor. Comparison: filled points use the posterior-median model. Open squares use the best sample with the fit's own sigma. Total chi-squared 126.8 over 12 bands gives 10.56 per band. Caveat: the spectrum dominates the joint fit, so the fit does not constrain the bands on their own.</figcaption>
</figure>

<figure>
<img loading="lazy" src="/wiki/f/results/rtx-5060-dr2-quiescent-full-spectrum/117400-M4_117400/diagnostics/spectral_chi2.png" alt="M4_117400: spectral pull, binned mean pull squared, cumulative chi-squared">
<figcaption><code>spectral_chi2.png</code> Pull per fitted pixel of the LEGA-C spectrum of galaxy M4_117400. Below it: mean pull squared in 25 Å bins and the cumulative chi-squared fraction against wavelength. Uncertainty: sigma includes the fitted calibration floor of 5.10 percent of the model flux. Comparison: the stored pull versus the pull at the best sample. Shaded bands mark masked pixels. Red points mark pixels with pull beyond 4 sigma. Total chi-squared 3824.4 over 3366 pixels, 1 outlier pixels. Caveat: the fitted floor absorbs model mismatch, so chi-squared near 1 does not prove a good model.</figcaption>
</figure>

<figure>
<img loading="lazy" src="/wiki/f/results/rtx-5060-dr2-quiescent-full-spectrum/117400-M4_117400/diagnostics/sf_timescales.png" alt="M4_117400: cumulative mass formed against lookback time with t10 to t90">
<figcaption><code>sf_timescales.png</code> Fraction of the final stellar mass of galaxy M4_117400 formed earlier than each lookback time. The line is the posterior median. The band is the 16-84 percent range over 400 draws. Comparison: points mark t10 to t90 with 16-84 percent (thick) and 2.5-97.5 percent (thin) intervals versus the universe age. t50 is 2.95 Gyr with a 16-84 percent range of 2.91 to 3.05 Gyr. Caveat: the 7-bin star-formation history model quantises these times to the bin edges.</figcaption>
</figure>

### 117694-M3_117694

| z | S/N | photometry χ²/N | spectrum χ²/N | f_calib | t50 [Gyr] | model |
| --- | --- | --- | --- | --- | --- | --- |
| 0.6831 | 24.2 | 2.73 | 1.177 | 4.56% | 3.10 | [parameters](/wiki/f/results/rtx-5060-dr2-quiescent-full-spectrum/117694-M3_117694/diagnostics/model_parameters.txt) |

Flags:

- 18 pixels with |pull| > 4

<figure>
<img loading="lazy" src="/wiki/f/results/rtx-5060-dr2-quiescent-full-spectrum/117694-M3_117694/diagnostics/photometric_chi2.png" alt="M3_117694: photometric pull and chi-squared contribution per band">
<figcaption><code>photometric_chi2.png</code> Pull and chi-squared contribution for the 12 COSMOS2015 bands of galaxy M3_117694. Pull equals observed minus model over sigma. Uncertainty: sigma includes the 5 percent flux floor. Comparison: filled points use the posterior-median model. Open squares use the best sample with the fit's own sigma. Total chi-squared 32.8 over 12 bands gives 2.73 per band. Caveat: the spectrum dominates the joint fit, so the fit does not constrain the bands on their own.</figcaption>
</figure>

<figure>
<img loading="lazy" src="/wiki/f/results/rtx-5060-dr2-quiescent-full-spectrum/117694-M3_117694/diagnostics/spectral_chi2.png" alt="M3_117694: spectral pull, binned mean pull squared, cumulative chi-squared">
<figcaption><code>spectral_chi2.png</code> Pull per fitted pixel of the LEGA-C spectrum of galaxy M3_117694. Below it: mean pull squared in 25 Å bins and the cumulative chi-squared fraction against wavelength. Uncertainty: sigma includes the fitted calibration floor of 4.56 percent of the model flux. Comparison: the stored pull versus the pull at the best sample. Shaded bands mark masked pixels. Red points mark pixels with pull beyond 4 sigma. Total chi-squared 4130.1 over 3508 pixels, 18 outlier pixels. Caveat: the fitted floor absorbs model mismatch, so chi-squared near 1 does not prove a good model.</figcaption>
</figure>

<figure>
<img loading="lazy" src="/wiki/f/results/rtx-5060-dr2-quiescent-full-spectrum/117694-M3_117694/diagnostics/sf_timescales.png" alt="M3_117694: cumulative mass formed against lookback time with t10 to t90">
<figcaption><code>sf_timescales.png</code> Fraction of the final stellar mass of galaxy M3_117694 formed earlier than each lookback time. The line is the posterior median. The band is the 16-84 percent range over 400 draws. Comparison: points mark t10 to t90 with 16-84 percent (thick) and 2.5-97.5 percent (thin) intervals versus the universe age. t50 is 3.10 Gyr with a 16-84 percent range of 3.01 to 3.41 Gyr. Caveat: the 7-bin star-formation history model quantises these times to the bin edges.</figcaption>
</figure>

### 119474-M3_119474

| z | S/N | photometry χ²/N | spectrum χ²/N | f_calib | t50 [Gyr] | model |
| --- | --- | --- | --- | --- | --- | --- |
| 0.6809 | 35.4 | 10.19 | 1.103 | 3.82% | 5.82 | [parameters](/wiki/f/results/rtx-5060-dr2-quiescent-full-spectrum/119474-M3_119474/diagnostics/model_parameters.txt) |

Flags:

- photometry chi2/N 10.2 > 3
- 6 pixels with |pull| > 4

<figure>
<img loading="lazy" src="/wiki/f/results/rtx-5060-dr2-quiescent-full-spectrum/119474-M3_119474/diagnostics/photometric_chi2.png" alt="M3_119474: photometric pull and chi-squared contribution per band">
<figcaption><code>photometric_chi2.png</code> Pull and chi-squared contribution for the 12 COSMOS2015 bands of galaxy M3_119474. Pull equals observed minus model over sigma. Uncertainty: sigma includes the 5 percent flux floor. Comparison: filled points use the posterior-median model. Open squares use the best sample with the fit's own sigma. Total chi-squared 122.3 over 12 bands gives 10.19 per band. Caveat: the spectrum dominates the joint fit, so the fit does not constrain the bands on their own.</figcaption>
</figure>

<figure>
<img loading="lazy" src="/wiki/f/results/rtx-5060-dr2-quiescent-full-spectrum/119474-M3_119474/diagnostics/spectral_chi2.png" alt="M3_119474: spectral pull, binned mean pull squared, cumulative chi-squared">
<figcaption><code>spectral_chi2.png</code> Pull per fitted pixel of the LEGA-C spectrum of galaxy M3_119474. Below it: mean pull squared in 25 Å bins and the cumulative chi-squared fraction against wavelength. Uncertainty: sigma includes the fitted calibration floor of 3.82 percent of the model flux. Comparison: the stored pull versus the pull at the best sample. Shaded bands mark masked pixels. Red points mark pixels with pull beyond 4 sigma. Total chi-squared 3829.5 over 3473 pixels, 6 outlier pixels. Caveat: the fitted floor absorbs model mismatch, so chi-squared near 1 does not prove a good model.</figcaption>
</figure>

<figure>
<img loading="lazy" src="/wiki/f/results/rtx-5060-dr2-quiescent-full-spectrum/119474-M3_119474/diagnostics/sf_timescales.png" alt="M3_119474: cumulative mass formed against lookback time with t10 to t90">
<figcaption><code>sf_timescales.png</code> Fraction of the final stellar mass of galaxy M3_119474 formed earlier than each lookback time. The line is the posterior median. The band is the 16-84 percent range over 400 draws. Comparison: points mark t10 to t90 with 16-84 percent (thick) and 2.5-97.5 percent (thin) intervals versus the universe age. t50 is 5.82 Gyr with a 16-84 percent range of 5.63 to 5.90 Gyr. Caveat: the 7-bin star-formation history model quantises these times to the bin edges.</figcaption>
</figure>

### 119802-M3_119802

| z | S/N | photometry χ²/N | spectrum χ²/N | f_calib | t50 [Gyr] | model |
| --- | --- | --- | --- | --- | --- | --- |
| 0.6820 | 25.4 | 16.15 | 1.215 | 4.39% | 3.00 | [parameters](/wiki/f/results/rtx-5060-dr2-quiescent-full-spectrum/119802-M3_119802/diagnostics/model_parameters.txt) |

Flags:

- photometry chi2/N 16.2 > 3
- 16 pixels with |pull| > 4

<figure>
<img loading="lazy" src="/wiki/f/results/rtx-5060-dr2-quiescent-full-spectrum/119802-M3_119802/diagnostics/photometric_chi2.png" alt="M3_119802: photometric pull and chi-squared contribution per band">
<figcaption><code>photometric_chi2.png</code> Pull and chi-squared contribution for the 12 COSMOS2015 bands of galaxy M3_119802. Pull equals observed minus model over sigma. Uncertainty: sigma includes the 5 percent flux floor. Comparison: filled points use the posterior-median model. Open squares use the best sample with the fit's own sigma. Total chi-squared 193.8 over 12 bands gives 16.15 per band. Caveat: the spectrum dominates the joint fit, so the fit does not constrain the bands on their own.</figcaption>
</figure>

<figure>
<img loading="lazy" src="/wiki/f/results/rtx-5060-dr2-quiescent-full-spectrum/119802-M3_119802/diagnostics/spectral_chi2.png" alt="M3_119802: spectral pull, binned mean pull squared, cumulative chi-squared">
<figcaption><code>spectral_chi2.png</code> Pull per fitted pixel of the LEGA-C spectrum of galaxy M3_119802. Below it: mean pull squared in 25 Å bins and the cumulative chi-squared fraction against wavelength. Uncertainty: sigma includes the fitted calibration floor of 4.39 percent of the model flux. Comparison: the stored pull versus the pull at the best sample. Shaded bands mark masked pixels. Red points mark pixels with pull beyond 4 sigma. Total chi-squared 4206.6 over 3461 pixels, 16 outlier pixels. Caveat: the fitted floor absorbs model mismatch, so chi-squared near 1 does not prove a good model.</figcaption>
</figure>

<figure>
<img loading="lazy" src="/wiki/f/results/rtx-5060-dr2-quiescent-full-spectrum/119802-M3_119802/diagnostics/sf_timescales.png" alt="M3_119802: cumulative mass formed against lookback time with t10 to t90">
<figcaption><code>sf_timescales.png</code> Fraction of the final stellar mass of galaxy M3_119802 formed earlier than each lookback time. The line is the posterior median. The band is the 16-84 percent range over 400 draws. Comparison: points mark t10 to t90 with 16-84 percent (thick) and 2.5-97.5 percent (thin) intervals versus the universe age. t50 is 3.00 Gyr with a 16-84 percent range of 2.99 to 3.05 Gyr. Caveat: the 7-bin star-formation history model quantises these times to the bin edges.</figcaption>
</figure>

### 119809-M3_119809

| z | S/N | photometry χ²/N | spectrum χ²/N | f_calib | t50 [Gyr] | model |
| --- | --- | --- | --- | --- | --- | --- |
| 0.6801 | 5.7 | 9.86 | 1.199 | 9.77% | 0.75 | [parameters](/wiki/f/results/rtx-5060-dr2-quiescent-full-spectrum/119809-M3_119809/diagnostics/model_parameters.txt) |

Flags:

- photometry chi2/N 9.9 > 3
- 8 pixels with |pull| > 4

<figure>
<img loading="lazy" src="/wiki/f/results/rtx-5060-dr2-quiescent-full-spectrum/119809-M3_119809/diagnostics/photometric_chi2.png" alt="M3_119809: photometric pull and chi-squared contribution per band">
<figcaption><code>photometric_chi2.png</code> Pull and chi-squared contribution for the 12 COSMOS2015 bands of galaxy M3_119809. Pull equals observed minus model over sigma. Uncertainty: sigma includes the 5 percent flux floor. Comparison: filled points use the posterior-median model. Open squares use the best sample with the fit's own sigma. Total chi-squared 118.4 over 12 bands gives 9.86 per band. Caveat: the spectrum dominates the joint fit, so the fit does not constrain the bands on their own.</figcaption>
</figure>

<figure>
<img loading="lazy" src="/wiki/f/results/rtx-5060-dr2-quiescent-full-spectrum/119809-M3_119809/diagnostics/spectral_chi2.png" alt="M3_119809: spectral pull, binned mean pull squared, cumulative chi-squared">
<figcaption><code>spectral_chi2.png</code> Pull per fitted pixel of the LEGA-C spectrum of galaxy M3_119809. Below it: mean pull squared in 25 Å bins and the cumulative chi-squared fraction against wavelength. Uncertainty: sigma includes the fitted calibration floor of 9.77 percent of the model flux. Comparison: the stored pull versus the pull at the best sample. Shaded bands mark masked pixels. Red points mark pixels with pull beyond 4 sigma. Total chi-squared 4264.0 over 3557 pixels, 8 outlier pixels. Caveat: the fitted floor absorbs model mismatch, so chi-squared near 1 does not prove a good model.</figcaption>
</figure>

<figure>
<img loading="lazy" src="/wiki/f/results/rtx-5060-dr2-quiescent-full-spectrum/119809-M3_119809/diagnostics/sf_timescales.png" alt="M3_119809: cumulative mass formed against lookback time with t10 to t90">
<figcaption><code>sf_timescales.png</code> Fraction of the final stellar mass of galaxy M3_119809 formed earlier than each lookback time. The line is the posterior median. The band is the 16-84 percent range over 400 draws. Comparison: points mark t10 to t90 with 16-84 percent (thick) and 2.5-97.5 percent (thin) intervals versus the universe age. t50 is 0.75 Gyr with a 16-84 percent range of 0.57 to 1.01 Gyr. Caveat: the 7-bin star-formation history model quantises these times to the bin edges.</figcaption>
</figure>

### 120308-M3_120308

| z | S/N | photometry χ²/N | spectrum χ²/N | f_calib | t50 [Gyr] | model |
| --- | --- | --- | --- | --- | --- | --- |
| 0.7279 | 29.0 | 10.65 | 1.167 | 4.07% | 2.89 | [parameters](/wiki/f/results/rtx-5060-dr2-quiescent-full-spectrum/120308-M3_120308/diagnostics/model_parameters.txt) |

Flags:

- photometry chi2/N 10.6 > 3
- 10 pixels with |pull| > 4

<figure>
<img loading="lazy" src="/wiki/f/results/rtx-5060-dr2-quiescent-full-spectrum/120308-M3_120308/diagnostics/photometric_chi2.png" alt="M3_120308: photometric pull and chi-squared contribution per band">
<figcaption><code>photometric_chi2.png</code> Pull and chi-squared contribution for the 12 COSMOS2015 bands of galaxy M3_120308. Pull equals observed minus model over sigma. Uncertainty: sigma includes the 5 percent flux floor. Comparison: filled points use the posterior-median model. Open squares use the best sample with the fit's own sigma. Total chi-squared 127.8 over 12 bands gives 10.65 per band. Caveat: the spectrum dominates the joint fit, so the fit does not constrain the bands on their own.</figcaption>
</figure>

<figure>
<img loading="lazy" src="/wiki/f/results/rtx-5060-dr2-quiescent-full-spectrum/120308-M3_120308/diagnostics/spectral_chi2.png" alt="M3_120308: spectral pull, binned mean pull squared, cumulative chi-squared">
<figcaption><code>spectral_chi2.png</code> Pull per fitted pixel of the LEGA-C spectrum of galaxy M3_120308. Below it: mean pull squared in 25 Å bins and the cumulative chi-squared fraction against wavelength. Uncertainty: sigma includes the fitted calibration floor of 4.07 percent of the model flux. Comparison: the stored pull versus the pull at the best sample. Shaded bands mark masked pixels. Red points mark pixels with pull beyond 4 sigma. Total chi-squared 4123.3 over 3532 pixels, 10 outlier pixels. Caveat: the fitted floor absorbs model mismatch, so chi-squared near 1 does not prove a good model.</figcaption>
</figure>

<figure>
<img loading="lazy" src="/wiki/f/results/rtx-5060-dr2-quiescent-full-spectrum/120308-M3_120308/diagnostics/sf_timescales.png" alt="M3_120308: cumulative mass formed against lookback time with t10 to t90">
<figcaption><code>sf_timescales.png</code> Fraction of the final stellar mass of galaxy M3_120308 formed earlier than each lookback time. The line is the posterior median. The band is the 16-84 percent range over 400 draws. Comparison: points mark t10 to t90 with 16-84 percent (thick) and 2.5-97.5 percent (thin) intervals versus the universe age. t50 is 2.89 Gyr with a 16-84 percent range of 2.85 to 2.97 Gyr. Caveat: the 7-bin star-formation history model quantises these times to the bin edges.</figcaption>
</figure>

### 120372-M7_120372

| z | S/N | photometry χ²/N | spectrum χ²/N | f_calib | t50 [Gyr] | model |
| --- | --- | --- | --- | --- | --- | --- |
| 0.9415 | 19.1 | 14.20 | 1.142 | 5.07% | 4.40 | [parameters](/wiki/f/results/rtx-5060-dr2-quiescent-full-spectrum/120372-M7_120372/diagnostics/model_parameters.txt) |

Flags:

- photometry chi2/N 14.2 > 3
- 10 pixels with |pull| > 4

<figure>
<img loading="lazy" src="/wiki/f/results/rtx-5060-dr2-quiescent-full-spectrum/120372-M7_120372/diagnostics/photometric_chi2.png" alt="M7_120372: photometric pull and chi-squared contribution per band">
<figcaption><code>photometric_chi2.png</code> Pull and chi-squared contribution for the 12 COSMOS2015 bands of galaxy M7_120372. Pull equals observed minus model over sigma. Uncertainty: sigma includes the 5 percent flux floor. Comparison: filled points use the posterior-median model. Open squares use the best sample with the fit's own sigma. Total chi-squared 170.4 over 12 bands gives 14.20 per band. Caveat: the spectrum dominates the joint fit, so the fit does not constrain the bands on their own.</figcaption>
</figure>

<figure>
<img loading="lazy" src="/wiki/f/results/rtx-5060-dr2-quiescent-full-spectrum/120372-M7_120372/diagnostics/spectral_chi2.png" alt="M7_120372: spectral pull, binned mean pull squared, cumulative chi-squared">
<figcaption><code>spectral_chi2.png</code> Pull per fitted pixel of the LEGA-C spectrum of galaxy M7_120372. Below it: mean pull squared in 25 Å bins and the cumulative chi-squared fraction against wavelength. Uncertainty: sigma includes the fitted calibration floor of 5.07 percent of the model flux. Comparison: the stored pull versus the pull at the best sample. Shaded bands mark masked pixels. Red points mark pixels with pull beyond 4 sigma. Total chi-squared 4322.9 over 3787 pixels, 10 outlier pixels. Caveat: the fitted floor absorbs model mismatch, so chi-squared near 1 does not prove a good model.</figcaption>
</figure>

<figure>
<img loading="lazy" src="/wiki/f/results/rtx-5060-dr2-quiescent-full-spectrum/120372-M7_120372/diagnostics/sf_timescales.png" alt="M7_120372: cumulative mass formed against lookback time with t10 to t90">
<figcaption><code>sf_timescales.png</code> Fraction of the final stellar mass of galaxy M7_120372 formed earlier than each lookback time. The line is the posterior median. The band is the 16-84 percent range over 400 draws. Comparison: points mark t10 to t90 with 16-84 percent (thick) and 2.5-97.5 percent (thin) intervals versus the universe age. t50 is 4.40 Gyr with a 16-84 percent range of 4.32 to 4.49 Gyr. Caveat: the 7-bin star-formation history model quantises these times to the bin edges.</figcaption>
</figure>

### 120488-M7_120488

| z | S/N | photometry χ²/N | spectrum χ²/N | f_calib | t50 [Gyr] | model |
| --- | --- | --- | --- | --- | --- | --- |
| 0.9335 | 13.6 | 8.33 | 1.075 | 5.59% | 2.94 | [parameters](/wiki/f/results/rtx-5060-dr2-quiescent-full-spectrum/120488-M7_120488/diagnostics/model_parameters.txt) |

Flags:

- photometry chi2/N 8.3 > 3
- 2 pixels with |pull| > 4

<figure>
<img loading="lazy" src="/wiki/f/results/rtx-5060-dr2-quiescent-full-spectrum/120488-M7_120488/diagnostics/photometric_chi2.png" alt="M7_120488: photometric pull and chi-squared contribution per band">
<figcaption><code>photometric_chi2.png</code> Pull and chi-squared contribution for the 12 COSMOS2015 bands of galaxy M7_120488. Pull equals observed minus model over sigma. Uncertainty: sigma includes the 5 percent flux floor. Comparison: filled points use the posterior-median model. Open squares use the best sample with the fit's own sigma. Total chi-squared 99.9 over 12 bands gives 8.33 per band. Caveat: the spectrum dominates the joint fit, so the fit does not constrain the bands on their own.</figcaption>
</figure>

<figure>
<img loading="lazy" src="/wiki/f/results/rtx-5060-dr2-quiescent-full-spectrum/120488-M7_120488/diagnostics/spectral_chi2.png" alt="M7_120488: spectral pull, binned mean pull squared, cumulative chi-squared">
<figcaption><code>spectral_chi2.png</code> Pull per fitted pixel of the LEGA-C spectrum of galaxy M7_120488. Below it: mean pull squared in 25 Å bins and the cumulative chi-squared fraction against wavelength. Uncertainty: sigma includes the fitted calibration floor of 5.59 percent of the model flux. Comparison: the stored pull versus the pull at the best sample. Shaded bands mark masked pixels. Red points mark pixels with pull beyond 4 sigma. Total chi-squared 4086.7 over 3802 pixels, 2 outlier pixels. Caveat: the fitted floor absorbs model mismatch, so chi-squared near 1 does not prove a good model.</figcaption>
</figure>

<figure>
<img loading="lazy" src="/wiki/f/results/rtx-5060-dr2-quiescent-full-spectrum/120488-M7_120488/diagnostics/sf_timescales.png" alt="M7_120488: cumulative mass formed against lookback time with t10 to t90">
<figcaption><code>sf_timescales.png</code> Fraction of the final stellar mass of galaxy M7_120488 formed earlier than each lookback time. The line is the posterior median. The band is the 16-84 percent range over 400 draws. Comparison: points mark t10 to t90 with 16-84 percent (thick) and 2.5-97.5 percent (thin) intervals versus the universe age. t50 is 2.94 Gyr with a 16-84 percent range of 2.80 to 3.60 Gyr. Caveat: the 7-bin star-formation history model quantises these times to the bin edges.</figcaption>
</figure>

### 120540-M3_120540

| z | S/N | photometry χ²/N | spectrum χ²/N | f_calib | t50 [Gyr] | model |
| --- | --- | --- | --- | --- | --- | --- |
| 0.9554 | 15.1 | 15.13 | 1.071 | 5.54% | 2.75 | [parameters](/wiki/f/results/rtx-5060-dr2-quiescent-full-spectrum/120540-M3_120540/diagnostics/model_parameters.txt) |

Flags:

- photometry chi2/N 15.1 > 3

<figure>
<img loading="lazy" src="/wiki/f/results/rtx-5060-dr2-quiescent-full-spectrum/120540-M3_120540/diagnostics/photometric_chi2.png" alt="M3_120540: photometric pull and chi-squared contribution per band">
<figcaption><code>photometric_chi2.png</code> Pull and chi-squared contribution for the 12 COSMOS2015 bands of galaxy M3_120540. Pull equals observed minus model over sigma. Uncertainty: sigma includes the 5 percent flux floor. Comparison: filled points use the posterior-median model. Open squares use the best sample with the fit's own sigma. Total chi-squared 181.5 over 12 bands gives 15.13 per band. Caveat: the spectrum dominates the joint fit, so the fit does not constrain the bands on their own.</figcaption>
</figure>

<figure>
<img loading="lazy" src="/wiki/f/results/rtx-5060-dr2-quiescent-full-spectrum/120540-M3_120540/diagnostics/spectral_chi2.png" alt="M3_120540: spectral pull, binned mean pull squared, cumulative chi-squared">
<figcaption><code>spectral_chi2.png</code> Pull per fitted pixel of the LEGA-C spectrum of galaxy M3_120540. Below it: mean pull squared in 25 Å bins and the cumulative chi-squared fraction against wavelength. Uncertainty: sigma includes the fitted calibration floor of 5.54 percent of the model flux. Comparison: the stored pull versus the pull at the best sample. Shaded bands mark masked pixels. Red points mark pixels with pull beyond 4 sigma. Total chi-squared 4084.4 over 3813 pixels, 0 outlier pixels. Caveat: the fitted floor absorbs model mismatch, so chi-squared near 1 does not prove a good model.</figcaption>
</figure>

<figure>
<img loading="lazy" src="/wiki/f/results/rtx-5060-dr2-quiescent-full-spectrum/120540-M3_120540/diagnostics/sf_timescales.png" alt="M3_120540: cumulative mass formed against lookback time with t10 to t90">
<figcaption><code>sf_timescales.png</code> Fraction of the final stellar mass of galaxy M3_120540 formed earlier than each lookback time. The line is the posterior median. The band is the 16-84 percent range over 400 draws. Comparison: points mark t10 to t90 with 16-84 percent (thick) and 2.5-97.5 percent (thin) intervals versus the universe age. t50 is 2.75 Gyr with a 16-84 percent range of 2.69 to 2.82 Gyr. Caveat: the 7-bin star-formation history model quantises these times to the bin edges.</figcaption>
</figure>

### 120758-M7_120758

| z | S/N | photometry χ²/N | spectrum χ²/N | f_calib | t50 [Gyr] | model |
| --- | --- | --- | --- | --- | --- | --- |
| 0.9365 | 9.8 | 10.24 | 1.040 | 6.16% | 3.57 | [parameters](/wiki/f/results/rtx-5060-dr2-quiescent-full-spectrum/120758-M7_120758/diagnostics/model_parameters.txt) |

Flags:

- photometry chi2/N 10.2 > 3
- 1 pixels with |pull| > 4

<figure>
<img loading="lazy" src="/wiki/f/results/rtx-5060-dr2-quiescent-full-spectrum/120758-M7_120758/diagnostics/photometric_chi2.png" alt="M7_120758: photometric pull and chi-squared contribution per band">
<figcaption><code>photometric_chi2.png</code> Pull and chi-squared contribution for the 12 COSMOS2015 bands of galaxy M7_120758. Pull equals observed minus model over sigma. Uncertainty: sigma includes the 5 percent flux floor. Comparison: filled points use the posterior-median model. Open squares use the best sample with the fit's own sigma. Total chi-squared 122.9 over 12 bands gives 10.24 per band. Caveat: the spectrum dominates the joint fit, so the fit does not constrain the bands on their own.</figcaption>
</figure>

<figure>
<img loading="lazy" src="/wiki/f/results/rtx-5060-dr2-quiescent-full-spectrum/120758-M7_120758/diagnostics/spectral_chi2.png" alt="M7_120758: spectral pull, binned mean pull squared, cumulative chi-squared">
<figcaption><code>spectral_chi2.png</code> Pull per fitted pixel of the LEGA-C spectrum of galaxy M7_120758. Below it: mean pull squared in 25 Å bins and the cumulative chi-squared fraction against wavelength. Uncertainty: sigma includes the fitted calibration floor of 6.16 percent of the model flux. Comparison: the stored pull versus the pull at the best sample. Shaded bands mark masked pixels. Red points mark pixels with pull beyond 4 sigma. Total chi-squared 3921.9 over 3772 pixels, 1 outlier pixels. Caveat: the fitted floor absorbs model mismatch, so chi-squared near 1 does not prove a good model.</figcaption>
</figure>

<figure>
<img loading="lazy" src="/wiki/f/results/rtx-5060-dr2-quiescent-full-spectrum/120758-M7_120758/diagnostics/sf_timescales.png" alt="M7_120758: cumulative mass formed against lookback time with t10 to t90">
<figcaption><code>sf_timescales.png</code> Fraction of the final stellar mass of galaxy M7_120758 formed earlier than each lookback time. The line is the posterior median. The band is the 16-84 percent range over 400 draws. Comparison: points mark t10 to t90 with 16-84 percent (thick) and 2.5-97.5 percent (thin) intervals versus the universe age. t50 is 3.57 Gyr with a 16-84 percent range of 3.19 to 3.79 Gyr. Caveat: the 7-bin star-formation history model quantises these times to the bin edges.</figcaption>
</figure>

### 121482-M7_121482

| z | S/N | photometry χ²/N | spectrum χ²/N | f_calib | t50 [Gyr] | model |
| --- | --- | --- | --- | --- | --- | --- |
| 0.9360 | 7.3 | 6.40 | 1.146 | 6.87% | 3.87 | [parameters](/wiki/f/results/rtx-5060-dr2-quiescent-full-spectrum/121482-M7_121482/diagnostics/model_parameters.txt) |

Flags:

- photometry chi2/N 6.4 > 3
- 3 pixels with |pull| > 4

<figure>
<img loading="lazy" src="/wiki/f/results/rtx-5060-dr2-quiescent-full-spectrum/121482-M7_121482/diagnostics/photometric_chi2.png" alt="M7_121482: photometric pull and chi-squared contribution per band">
<figcaption><code>photometric_chi2.png</code> Pull and chi-squared contribution for the 12 COSMOS2015 bands of galaxy M7_121482. Pull equals observed minus model over sigma. Uncertainty: sigma includes the 5 percent flux floor. Comparison: filled points use the posterior-median model. Open squares use the best sample with the fit's own sigma. Total chi-squared 76.8 over 12 bands gives 6.40 per band. Caveat: the spectrum dominates the joint fit, so the fit does not constrain the bands on their own.</figcaption>
</figure>

<figure>
<img loading="lazy" src="/wiki/f/results/rtx-5060-dr2-quiescent-full-spectrum/121482-M7_121482/diagnostics/spectral_chi2.png" alt="M7_121482: spectral pull, binned mean pull squared, cumulative chi-squared">
<figcaption><code>spectral_chi2.png</code> Pull per fitted pixel of the LEGA-C spectrum of galaxy M7_121482. Below it: mean pull squared in 25 Å bins and the cumulative chi-squared fraction against wavelength. Uncertainty: sigma includes the fitted calibration floor of 6.87 percent of the model flux. Comparison: the stored pull versus the pull at the best sample. Shaded bands mark masked pixels. Red points mark pixels with pull beyond 4 sigma. Total chi-squared 4374.5 over 3818 pixels, 3 outlier pixels. Caveat: the fitted floor absorbs model mismatch, so chi-squared near 1 does not prove a good model.</figcaption>
</figure>

<figure>
<img loading="lazy" src="/wiki/f/results/rtx-5060-dr2-quiescent-full-spectrum/121482-M7_121482/diagnostics/sf_timescales.png" alt="M7_121482: cumulative mass formed against lookback time with t10 to t90">
<figcaption><code>sf_timescales.png</code> Fraction of the final stellar mass of galaxy M7_121482 formed earlier than each lookback time. The line is the posterior median. The band is the 16-84 percent range over 400 draws. Comparison: points mark t10 to t90 with 16-84 percent (thick) and 2.5-97.5 percent (thin) intervals versus the universe age. t50 is 3.87 Gyr with a 16-84 percent range of 3.15 to 4.41 Gyr. Caveat: the 7-bin star-formation history model quantises these times to the bin edges.</figcaption>
</figure>

### 122025-M7_122025

| z | S/N | photometry χ²/N | spectrum χ²/N | f_calib | t50 [Gyr] | model |
| --- | --- | --- | --- | --- | --- | --- |
| 0.7477 | 14.0 | 7.29 | 1.171 | 5.94% | 3.01 | [parameters](/wiki/f/results/rtx-5060-dr2-quiescent-full-spectrum/122025-M7_122025/diagnostics/model_parameters.txt) |

Flags:

- photometry chi2/N 7.3 > 3
- 5 pixels with |pull| > 4

<figure>
<img loading="lazy" src="/wiki/f/results/rtx-5060-dr2-quiescent-full-spectrum/122025-M7_122025/diagnostics/photometric_chi2.png" alt="M7_122025: photometric pull and chi-squared contribution per band">
<figcaption><code>photometric_chi2.png</code> Pull and chi-squared contribution for the 12 COSMOS2015 bands of galaxy M7_122025. Pull equals observed minus model over sigma. Uncertainty: sigma includes the 5 percent flux floor. Comparison: filled points use the posterior-median model. Open squares use the best sample with the fit's own sigma. Total chi-squared 87.5 over 12 bands gives 7.29 per band. Caveat: the spectrum dominates the joint fit, so the fit does not constrain the bands on their own.</figcaption>
</figure>

<figure>
<img loading="lazy" src="/wiki/f/results/rtx-5060-dr2-quiescent-full-spectrum/122025-M7_122025/diagnostics/spectral_chi2.png" alt="M7_122025: spectral pull, binned mean pull squared, cumulative chi-squared">
<figcaption><code>spectral_chi2.png</code> Pull per fitted pixel of the LEGA-C spectrum of galaxy M7_122025. Below it: mean pull squared in 25 Å bins and the cumulative chi-squared fraction against wavelength. Uncertainty: sigma includes the fitted calibration floor of 5.94 percent of the model flux. Comparison: the stored pull versus the pull at the best sample. Shaded bands mark masked pixels. Red points mark pixels with pull beyond 4 sigma. Total chi-squared 4425.5 over 3778 pixels, 5 outlier pixels. Caveat: the fitted floor absorbs model mismatch, so chi-squared near 1 does not prove a good model.</figcaption>
</figure>

<figure>
<img loading="lazy" src="/wiki/f/results/rtx-5060-dr2-quiescent-full-spectrum/122025-M7_122025/diagnostics/sf_timescales.png" alt="M7_122025: cumulative mass formed against lookback time with t10 to t90">
<figcaption><code>sf_timescales.png</code> Fraction of the final stellar mass of galaxy M7_122025 formed earlier than each lookback time. The line is the posterior median. The band is the 16-84 percent range over 400 draws. Comparison: points mark t10 to t90 with 16-84 percent (thick) and 2.5-97.5 percent (thin) intervals versus the universe age. t50 is 3.01 Gyr with a 16-84 percent range of 3.00 to 3.05 Gyr. Caveat: the 7-bin star-formation history model quantises these times to the bin edges.</figcaption>
</figure>

### 122242-M7_122242

| z | S/N | photometry χ²/N | spectrum χ²/N | f_calib | t50 [Gyr] | model |
| --- | --- | --- | --- | --- | --- | --- |
| 0.6032 | 26.0 | 6.48 | 1.132 | 4.19% | 3.00 | [parameters](/wiki/f/results/rtx-5060-dr2-quiescent-full-spectrum/122242-M7_122242/diagnostics/model_parameters.txt) |

Flags:

- photometry chi2/N 6.5 > 3
- 2 pixels with |pull| > 4

<figure>
<img loading="lazy" src="/wiki/f/results/rtx-5060-dr2-quiescent-full-spectrum/122242-M7_122242/diagnostics/photometric_chi2.png" alt="M7_122242: photometric pull and chi-squared contribution per band">
<figcaption><code>photometric_chi2.png</code> Pull and chi-squared contribution for the 12 COSMOS2015 bands of galaxy M7_122242. Pull equals observed minus model over sigma. Uncertainty: sigma includes the 5 percent flux floor. Comparison: filled points use the posterior-median model. Open squares use the best sample with the fit's own sigma. Total chi-squared 77.7 over 12 bands gives 6.48 per band. Caveat: the spectrum dominates the joint fit, so the fit does not constrain the bands on their own.</figcaption>
</figure>

<figure>
<img loading="lazy" src="/wiki/f/results/rtx-5060-dr2-quiescent-full-spectrum/122242-M7_122242/diagnostics/spectral_chi2.png" alt="M7_122242: spectral pull, binned mean pull squared, cumulative chi-squared">
<figcaption><code>spectral_chi2.png</code> Pull per fitted pixel of the LEGA-C spectrum of galaxy M7_122242. Below it: mean pull squared in 25 Å bins and the cumulative chi-squared fraction against wavelength. Uncertainty: sigma includes the fitted calibration floor of 4.19 percent of the model flux. Comparison: the stored pull versus the pull at the best sample. Shaded bands mark masked pixels. Red points mark pixels with pull beyond 4 sigma. Total chi-squared 3980.2 over 3516 pixels, 2 outlier pixels. Caveat: the fitted floor absorbs model mismatch, so chi-squared near 1 does not prove a good model.</figcaption>
</figure>

<figure>
<img loading="lazy" src="/wiki/f/results/rtx-5060-dr2-quiescent-full-spectrum/122242-M7_122242/diagnostics/sf_timescales.png" alt="M7_122242: cumulative mass formed against lookback time with t10 to t90">
<figcaption><code>sf_timescales.png</code> Fraction of the final stellar mass of galaxy M7_122242 formed earlier than each lookback time. The line is the posterior median. The band is the 16-84 percent range over 400 draws. Comparison: points mark t10 to t90 with 16-84 percent (thick) and 2.5-97.5 percent (thin) intervals versus the universe age. t50 is 3.00 Gyr with a 16-84 percent range of 2.96 to 3.07 Gyr. Caveat: the 7-bin star-formation history model quantises these times to the bin edges.</figcaption>
</figure>

### 123161-M4_123161

| z | S/N | photometry χ²/N | spectrum χ²/N | f_calib | t50 [Gyr] | model |
| --- | --- | --- | --- | --- | --- | --- |
| 0.7995 | 21.0 | 3.06 | 1.153 | 5.62% | 4.69 | [parameters](/wiki/f/results/rtx-5060-dr2-quiescent-full-spectrum/123161-M4_123161/diagnostics/model_parameters.txt) |

Flags:

- photometry chi2/N 3.1 > 3

<figure>
<img loading="lazy" src="/wiki/f/results/rtx-5060-dr2-quiescent-full-spectrum/123161-M4_123161/diagnostics/photometric_chi2.png" alt="M4_123161: photometric pull and chi-squared contribution per band">
<figcaption><code>photometric_chi2.png</code> Pull and chi-squared contribution for the 12 COSMOS2015 bands of galaxy M4_123161. Pull equals observed minus model over sigma. Uncertainty: sigma includes the 5 percent flux floor. Comparison: filled points use the posterior-median model. Open squares use the best sample with the fit's own sigma. Total chi-squared 36.7 over 12 bands gives 3.06 per band. Caveat: the spectrum dominates the joint fit, so the fit does not constrain the bands on their own.</figcaption>
</figure>

<figure>
<img loading="lazy" src="/wiki/f/results/rtx-5060-dr2-quiescent-full-spectrum/123161-M4_123161/diagnostics/spectral_chi2.png" alt="M4_123161: spectral pull, binned mean pull squared, cumulative chi-squared">
<figcaption><code>spectral_chi2.png</code> Pull per fitted pixel of the LEGA-C spectrum of galaxy M4_123161. Below it: mean pull squared in 25 Å bins and the cumulative chi-squared fraction against wavelength. Uncertainty: sigma includes the fitted calibration floor of 5.62 percent of the model flux. Comparison: the stored pull versus the pull at the best sample. Shaded bands mark masked pixels. Red points mark pixels with pull beyond 4 sigma. Total chi-squared 4176.5 over 3621 pixels, 0 outlier pixels. Caveat: the fitted floor absorbs model mismatch, so chi-squared near 1 does not prove a good model.</figcaption>
</figure>

<figure>
<img loading="lazy" src="/wiki/f/results/rtx-5060-dr2-quiescent-full-spectrum/123161-M4_123161/diagnostics/sf_timescales.png" alt="M4_123161: cumulative mass formed against lookback time with t10 to t90">
<figcaption><code>sf_timescales.png</code> Fraction of the final stellar mass of galaxy M4_123161 formed earlier than each lookback time. The line is the posterior median. The band is the 16-84 percent range over 400 draws. Comparison: points mark t10 to t90 with 16-84 percent (thick) and 2.5-97.5 percent (thin) intervals versus the universe age. t50 is 4.69 Gyr with a 16-84 percent range of 3.74 to 5.22 Gyr. Caveat: the 7-bin star-formation history model quantises these times to the bin edges.</figcaption>
</figure>

### 124231-M4_124231

| z | S/N | photometry χ²/N | spectrum χ²/N | f_calib | t50 [Gyr] | model |
| --- | --- | --- | --- | --- | --- | --- |
| 0.6771 | 34.5 | 8.63 | 1.223 | 4.05% | 2.87 | [parameters](/wiki/f/results/rtx-5060-dr2-quiescent-full-spectrum/124231-M4_124231/diagnostics/model_parameters.txt) |

Flags:

- photometry chi2/N 8.6 > 3
- 26 pixels with |pull| > 4

<figure>
<img loading="lazy" src="/wiki/f/results/rtx-5060-dr2-quiescent-full-spectrum/124231-M4_124231/diagnostics/photometric_chi2.png" alt="M4_124231: photometric pull and chi-squared contribution per band">
<figcaption><code>photometric_chi2.png</code> Pull and chi-squared contribution for the 12 COSMOS2015 bands of galaxy M4_124231. Pull equals observed minus model over sigma. Uncertainty: sigma includes the 5 percent flux floor. Comparison: filled points use the posterior-median model. Open squares use the best sample with the fit's own sigma. Total chi-squared 103.6 over 12 bands gives 8.63 per band. Caveat: the spectrum dominates the joint fit, so the fit does not constrain the bands on their own.</figcaption>
</figure>

<figure>
<img loading="lazy" src="/wiki/f/results/rtx-5060-dr2-quiescent-full-spectrum/124231-M4_124231/diagnostics/spectral_chi2.png" alt="M4_124231: spectral pull, binned mean pull squared, cumulative chi-squared">
<figcaption><code>spectral_chi2.png</code> Pull per fitted pixel of the LEGA-C spectrum of galaxy M4_124231. Below it: mean pull squared in 25 Å bins and the cumulative chi-squared fraction against wavelength. Uncertainty: sigma includes the fitted calibration floor of 4.05 percent of the model flux. Comparison: the stored pull versus the pull at the best sample. Shaded bands mark masked pixels. Red points mark pixels with pull beyond 4 sigma. Total chi-squared 4359.7 over 3566 pixels, 26 outlier pixels. Caveat: the fitted floor absorbs model mismatch, so chi-squared near 1 does not prove a good model.</figcaption>
</figure>

<figure>
<img loading="lazy" src="/wiki/f/results/rtx-5060-dr2-quiescent-full-spectrum/124231-M4_124231/diagnostics/sf_timescales.png" alt="M4_124231: cumulative mass formed against lookback time with t10 to t90">
<figcaption><code>sf_timescales.png</code> Fraction of the final stellar mass of galaxy M4_124231 formed earlier than each lookback time. The line is the posterior median. The band is the 16-84 percent range over 400 draws. Comparison: points mark t10 to t90 with 16-84 percent (thick) and 2.5-97.5 percent (thin) intervals versus the universe age. t50 is 2.87 Gyr with a 16-84 percent range of 2.83 to 2.91 Gyr. Caveat: the 7-bin star-formation history model quantises these times to the bin edges.</figcaption>
</figure>

### 124875-M7_124875

| z | S/N | photometry χ²/N | spectrum χ²/N | f_calib | t50 [Gyr] | model |
| --- | --- | --- | --- | --- | --- | --- |
| 0.6026 | 31.5 | 2.54 | 1.138 | 3.89% | 2.81 | [parameters](/wiki/f/results/rtx-5060-dr2-quiescent-full-spectrum/124875-M7_124875/diagnostics/model_parameters.txt) |

Flags:

- 7 pixels with |pull| > 4

<figure>
<img loading="lazy" src="/wiki/f/results/rtx-5060-dr2-quiescent-full-spectrum/124875-M7_124875/diagnostics/photometric_chi2.png" alt="M7_124875: photometric pull and chi-squared contribution per band">
<figcaption><code>photometric_chi2.png</code> Pull and chi-squared contribution for the 12 COSMOS2015 bands of galaxy M7_124875. Pull equals observed minus model over sigma. Uncertainty: sigma includes the 5 percent flux floor. Comparison: filled points use the posterior-median model. Open squares use the best sample with the fit's own sigma. Total chi-squared 30.5 over 12 bands gives 2.54 per band. Caveat: the spectrum dominates the joint fit, so the fit does not constrain the bands on their own.</figcaption>
</figure>

<figure>
<img loading="lazy" src="/wiki/f/results/rtx-5060-dr2-quiescent-full-spectrum/124875-M7_124875/diagnostics/spectral_chi2.png" alt="M7_124875: spectral pull, binned mean pull squared, cumulative chi-squared">
<figcaption><code>spectral_chi2.png</code> Pull per fitted pixel of the LEGA-C spectrum of galaxy M7_124875. Below it: mean pull squared in 25 Å bins and the cumulative chi-squared fraction against wavelength. Uncertainty: sigma includes the fitted calibration floor of 3.89 percent of the model flux. Comparison: the stored pull versus the pull at the best sample. Shaded bands mark masked pixels. Red points mark pixels with pull beyond 4 sigma. Total chi-squared 3972.3 over 3490 pixels, 7 outlier pixels. Caveat: the fitted floor absorbs model mismatch, so chi-squared near 1 does not prove a good model.</figcaption>
</figure>

<figure>
<img loading="lazy" src="/wiki/f/results/rtx-5060-dr2-quiescent-full-spectrum/124875-M7_124875/diagnostics/sf_timescales.png" alt="M7_124875: cumulative mass formed against lookback time with t10 to t90">
<figcaption><code>sf_timescales.png</code> Fraction of the final stellar mass of galaxy M7_124875 formed earlier than each lookback time. The line is the posterior median. The band is the 16-84 percent range over 400 draws. Comparison: points mark t10 to t90 with 16-84 percent (thick) and 2.5-97.5 percent (thin) intervals versus the universe age. t50 is 2.81 Gyr with a 16-84 percent range of 2.77 to 2.89 Gyr. Caveat: the 7-bin star-formation history model quantises these times to the bin edges.</figcaption>
</figure>

### 125213-M4_125213

| z | S/N | photometry χ²/N | spectrum χ²/N | f_calib | t50 [Gyr] | model |
| --- | --- | --- | --- | --- | --- | --- |
| 0.6772 | 27.9 | 10.74 | 1.191 | 3.84% | 3.01 | [parameters](/wiki/f/results/rtx-5060-dr2-quiescent-full-spectrum/125213-M4_125213/diagnostics/model_parameters.txt) |

Flags:

- photometry chi2/N 10.7 > 3
- 6 pixels with |pull| > 4

<figure>
<img loading="lazy" src="/wiki/f/results/rtx-5060-dr2-quiescent-full-spectrum/125213-M4_125213/diagnostics/photometric_chi2.png" alt="M4_125213: photometric pull and chi-squared contribution per band">
<figcaption><code>photometric_chi2.png</code> Pull and chi-squared contribution for the 12 COSMOS2015 bands of galaxy M4_125213. Pull equals observed minus model over sigma. Uncertainty: sigma includes the 5 percent flux floor. Comparison: filled points use the posterior-median model. Open squares use the best sample with the fit's own sigma. Total chi-squared 128.9 over 12 bands gives 10.74 per band. Caveat: the spectrum dominates the joint fit, so the fit does not constrain the bands on their own.</figcaption>
</figure>

<figure>
<img loading="lazy" src="/wiki/f/results/rtx-5060-dr2-quiescent-full-spectrum/125213-M4_125213/diagnostics/spectral_chi2.png" alt="M4_125213: spectral pull, binned mean pull squared, cumulative chi-squared">
<figcaption><code>spectral_chi2.png</code> Pull per fitted pixel of the LEGA-C spectrum of galaxy M4_125213. Below it: mean pull squared in 25 Å bins and the cumulative chi-squared fraction against wavelength. Uncertainty: sigma includes the fitted calibration floor of 3.84 percent of the model flux. Comparison: the stored pull versus the pull at the best sample. Shaded bands mark masked pixels. Red points mark pixels with pull beyond 4 sigma. Total chi-squared 4119.5 over 3458 pixels, 6 outlier pixels. Caveat: the fitted floor absorbs model mismatch, so chi-squared near 1 does not prove a good model.</figcaption>
</figure>

<figure>
<img loading="lazy" src="/wiki/f/results/rtx-5060-dr2-quiescent-full-spectrum/125213-M4_125213/diagnostics/sf_timescales.png" alt="M4_125213: cumulative mass formed against lookback time with t10 to t90">
<figcaption><code>sf_timescales.png</code> Fraction of the final stellar mass of galaxy M4_125213 formed earlier than each lookback time. The line is the posterior median. The band is the 16-84 percent range over 400 draws. Comparison: points mark t10 to t90 with 16-84 percent (thick) and 2.5-97.5 percent (thin) intervals versus the universe age. t50 is 3.01 Gyr with a 16-84 percent range of 2.99 to 3.03 Gyr. Caveat: the 7-bin star-formation history model quantises these times to the bin edges.</figcaption>
</figure>

### 126153-M1_126153

| z | S/N | photometry χ²/N | spectrum χ²/N | f_calib | t50 [Gyr] | model |
| --- | --- | --- | --- | --- | --- | --- |
| 0.6823 | 10.3 | 2.88 | 1.166 | 6.63% | 5.28 | [parameters](/wiki/f/results/rtx-5060-dr2-quiescent-full-spectrum/126153-M1_126153/diagnostics/model_parameters.txt) |

Flags:

- 7 pixels with |pull| > 4

<figure>
<img loading="lazy" src="/wiki/f/results/rtx-5060-dr2-quiescent-full-spectrum/126153-M1_126153/diagnostics/photometric_chi2.png" alt="M1_126153: photometric pull and chi-squared contribution per band">
<figcaption><code>photometric_chi2.png</code> Pull and chi-squared contribution for the 12 COSMOS2015 bands of galaxy M1_126153. Pull equals observed minus model over sigma. Uncertainty: sigma includes the 5 percent flux floor. Comparison: filled points use the posterior-median model. Open squares use the best sample with the fit's own sigma. Total chi-squared 34.5 over 12 bands gives 2.88 per band. Caveat: the spectrum dominates the joint fit, so the fit does not constrain the bands on their own.</figcaption>
</figure>

<figure>
<img loading="lazy" src="/wiki/f/results/rtx-5060-dr2-quiescent-full-spectrum/126153-M1_126153/diagnostics/spectral_chi2.png" alt="M1_126153: spectral pull, binned mean pull squared, cumulative chi-squared">
<figcaption><code>spectral_chi2.png</code> Pull per fitted pixel of the LEGA-C spectrum of galaxy M1_126153. Below it: mean pull squared in 25 Å bins and the cumulative chi-squared fraction against wavelength. Uncertainty: sigma includes the fitted calibration floor of 6.63 percent of the model flux. Comparison: the stored pull versus the pull at the best sample. Shaded bands mark masked pixels. Red points mark pixels with pull beyond 4 sigma. Total chi-squared 4071.8 over 3493 pixels, 7 outlier pixels. Caveat: the fitted floor absorbs model mismatch, so chi-squared near 1 does not prove a good model.</figcaption>
</figure>

<figure>
<img loading="lazy" src="/wiki/f/results/rtx-5060-dr2-quiescent-full-spectrum/126153-M1_126153/diagnostics/sf_timescales.png" alt="M1_126153: cumulative mass formed against lookback time with t10 to t90">
<figcaption><code>sf_timescales.png</code> Fraction of the final stellar mass of galaxy M1_126153 formed earlier than each lookback time. The line is the posterior median. The band is the 16-84 percent range over 400 draws. Comparison: points mark t10 to t90 with 16-84 percent (thick) and 2.5-97.5 percent (thin) intervals versus the universe age. t50 is 5.28 Gyr with a 16-84 percent range of 2.76 to 5.68 Gyr. Caveat: the 7-bin star-formation history model quantises these times to the bin edges.</figcaption>
</figure>

### 126578-M1_126578

| z | S/N | photometry χ²/N | spectrum χ²/N | f_calib | t50 [Gyr] | model |
| --- | --- | --- | --- | --- | --- | --- |
| 0.7504 | 15.1 | 11.95 | 1.166 | 6.05% | 5.19 | [parameters](/wiki/f/results/rtx-5060-dr2-quiescent-full-spectrum/126578-M1_126578/diagnostics/model_parameters.txt) |

Flags:

- photometry chi2/N 11.9 > 3
- 9 pixels with |pull| > 4

<figure>
<img loading="lazy" src="/wiki/f/results/rtx-5060-dr2-quiescent-full-spectrum/126578-M1_126578/diagnostics/photometric_chi2.png" alt="M1_126578: photometric pull and chi-squared contribution per band">
<figcaption><code>photometric_chi2.png</code> Pull and chi-squared contribution for the 12 COSMOS2015 bands of galaxy M1_126578. Pull equals observed minus model over sigma. Uncertainty: sigma includes the 5 percent flux floor. Comparison: filled points use the posterior-median model. Open squares use the best sample with the fit's own sigma. Total chi-squared 143.4 over 12 bands gives 11.95 per band. Caveat: the spectrum dominates the joint fit, so the fit does not constrain the bands on their own.</figcaption>
</figure>

<figure>
<img loading="lazy" src="/wiki/f/results/rtx-5060-dr2-quiescent-full-spectrum/126578-M1_126578/diagnostics/spectral_chi2.png" alt="M1_126578: spectral pull, binned mean pull squared, cumulative chi-squared">
<figcaption><code>spectral_chi2.png</code> Pull per fitted pixel of the LEGA-C spectrum of galaxy M1_126578. Below it: mean pull squared in 25 Å bins and the cumulative chi-squared fraction against wavelength. Uncertainty: sigma includes the fitted calibration floor of 6.05 percent of the model flux. Comparison: the stored pull versus the pull at the best sample. Shaded bands mark masked pixels. Red points mark pixels with pull beyond 4 sigma. Total chi-squared 4133.5 over 3545 pixels, 9 outlier pixels. Caveat: the fitted floor absorbs model mismatch, so chi-squared near 1 does not prove a good model.</figcaption>
</figure>

<figure>
<img loading="lazy" src="/wiki/f/results/rtx-5060-dr2-quiescent-full-spectrum/126578-M1_126578/diagnostics/sf_timescales.png" alt="M1_126578: cumulative mass formed against lookback time with t10 to t90">
<figcaption><code>sf_timescales.png</code> Fraction of the final stellar mass of galaxy M1_126578 formed earlier than each lookback time. The line is the posterior median. The band is the 16-84 percent range over 400 draws. Comparison: points mark t10 to t90 with 16-84 percent (thick) and 2.5-97.5 percent (thin) intervals versus the universe age. t50 is 5.19 Gyr with a 16-84 percent range of 4.37 to 5.80 Gyr. Caveat: the 7-bin star-formation history model quantises these times to the bin edges.</figcaption>
</figure>

### 127946-M5_127946

| z | S/N | photometry χ²/N | spectrum χ²/N | f_calib | t50 [Gyr] | model |
| --- | --- | --- | --- | --- | --- | --- |
| 0.9387 | 5.9 | 2.27 | 1.004 | 8.79% | 5.25 | [parameters](/wiki/f/results/rtx-5060-dr2-quiescent-full-spectrum/127946-M5_127946/diagnostics/model_parameters.txt) |

Flags:

- 2 pixels with |pull| > 4

<figure>
<img loading="lazy" src="/wiki/f/results/rtx-5060-dr2-quiescent-full-spectrum/127946-M5_127946/diagnostics/photometric_chi2.png" alt="M5_127946: photometric pull and chi-squared contribution per band">
<figcaption><code>photometric_chi2.png</code> Pull and chi-squared contribution for the 12 COSMOS2015 bands of galaxy M5_127946. Pull equals observed minus model over sigma. Uncertainty: sigma includes the 5 percent flux floor. Comparison: filled points use the posterior-median model. Open squares use the best sample with the fit's own sigma. Total chi-squared 27.3 over 12 bands gives 2.27 per band. Caveat: the spectrum dominates the joint fit, so the fit does not constrain the bands on their own.</figcaption>
</figure>

<figure>
<img loading="lazy" src="/wiki/f/results/rtx-5060-dr2-quiescent-full-spectrum/127946-M5_127946/diagnostics/spectral_chi2.png" alt="M5_127946: spectral pull, binned mean pull squared, cumulative chi-squared">
<figcaption><code>spectral_chi2.png</code> Pull per fitted pixel of the LEGA-C spectrum of galaxy M5_127946. Below it: mean pull squared in 25 Å bins and the cumulative chi-squared fraction against wavelength. Uncertainty: sigma includes the fitted calibration floor of 8.79 percent of the model flux. Comparison: the stored pull versus the pull at the best sample. Shaded bands mark masked pixels. Red points mark pixels with pull beyond 4 sigma. Total chi-squared 3785.8 over 3770 pixels, 2 outlier pixels. Caveat: the fitted floor absorbs model mismatch, so chi-squared near 1 does not prove a good model.</figcaption>
</figure>

<figure>
<img loading="lazy" src="/wiki/f/results/rtx-5060-dr2-quiescent-full-spectrum/127946-M5_127946/diagnostics/sf_timescales.png" alt="M5_127946: cumulative mass formed against lookback time with t10 to t90">
<figcaption><code>sf_timescales.png</code> Fraction of the final stellar mass of galaxy M5_127946 formed earlier than each lookback time. The line is the posterior median. The band is the 16-84 percent range over 400 draws. Comparison: points mark t10 to t90 with 16-84 percent (thick) and 2.5-97.5 percent (thin) intervals versus the universe age. t50 is 5.25 Gyr with a 16-84 percent range of 5.12 to 5.35 Gyr. Caveat: the 7-bin star-formation history model quantises these times to the bin edges.</figcaption>
</figure>

### 128311-M5_128311

| z | S/N | photometry χ²/N | spectrum χ²/N | f_calib | t50 [Gyr] | model |
| --- | --- | --- | --- | --- | --- | --- |
| 0.7303 | 26.0 | 9.85 | 1.121 | 4.57% | 3.99 | [parameters](/wiki/f/results/rtx-5060-dr2-quiescent-full-spectrum/128311-M5_128311/diagnostics/model_parameters.txt) |

Flags:

- photometry chi2/N 9.9 > 3
- 2 pixels with |pull| > 4

<figure>
<img loading="lazy" src="/wiki/f/results/rtx-5060-dr2-quiescent-full-spectrum/128311-M5_128311/diagnostics/photometric_chi2.png" alt="M5_128311: photometric pull and chi-squared contribution per band">
<figcaption><code>photometric_chi2.png</code> Pull and chi-squared contribution for the 12 COSMOS2015 bands of galaxy M5_128311. Pull equals observed minus model over sigma. Uncertainty: sigma includes the 5 percent flux floor. Comparison: filled points use the posterior-median model. Open squares use the best sample with the fit's own sigma. Total chi-squared 118.2 over 12 bands gives 9.85 per band. Caveat: the spectrum dominates the joint fit, so the fit does not constrain the bands on their own.</figcaption>
</figure>

<figure>
<img loading="lazy" src="/wiki/f/results/rtx-5060-dr2-quiescent-full-spectrum/128311-M5_128311/diagnostics/spectral_chi2.png" alt="M5_128311: spectral pull, binned mean pull squared, cumulative chi-squared">
<figcaption><code>spectral_chi2.png</code> Pull per fitted pixel of the LEGA-C spectrum of galaxy M5_128311. Below it: mean pull squared in 25 Å bins and the cumulative chi-squared fraction against wavelength. Uncertainty: sigma includes the fitted calibration floor of 4.57 percent of the model flux. Comparison: the stored pull versus the pull at the best sample. Shaded bands mark masked pixels. Red points mark pixels with pull beyond 4 sigma. Total chi-squared 4127.2 over 3681 pixels, 2 outlier pixels. Caveat: the fitted floor absorbs model mismatch, so chi-squared near 1 does not prove a good model.</figcaption>
</figure>

<figure>
<img loading="lazy" src="/wiki/f/results/rtx-5060-dr2-quiescent-full-spectrum/128311-M5_128311/diagnostics/sf_timescales.png" alt="M5_128311: cumulative mass formed against lookback time with t10 to t90">
<figcaption><code>sf_timescales.png</code> Fraction of the final stellar mass of galaxy M5_128311 formed earlier than each lookback time. The line is the posterior median. The band is the 16-84 percent range over 400 draws. Comparison: points mark t10 to t90 with 16-84 percent (thick) and 2.5-97.5 percent (thin) intervals versus the universe age. t50 is 3.99 Gyr with a 16-84 percent range of 3.71 to 4.36 Gyr. Caveat: the 7-bin star-formation history model quantises these times to the bin edges.</figcaption>
</figure>

### 129596-M2_129596

| z | S/N | photometry χ²/N | spectrum χ²/N | f_calib | t50 [Gyr] | model |
| --- | --- | --- | --- | --- | --- | --- |
| 0.6956 | 18.6 | 7.28 | 1.049 | 3.64% | 3.51 | [parameters](/wiki/f/results/rtx-5060-dr2-quiescent-full-spectrum/129596-M2_129596/diagnostics/model_parameters.txt) |

Flags:

- photometry chi2/N 7.3 > 3

<figure>
<img loading="lazy" src="/wiki/f/results/rtx-5060-dr2-quiescent-full-spectrum/129596-M2_129596/diagnostics/photometric_chi2.png" alt="M2_129596: photometric pull and chi-squared contribution per band">
<figcaption><code>photometric_chi2.png</code> Pull and chi-squared contribution for the 12 COSMOS2015 bands of galaxy M2_129596. Pull equals observed minus model over sigma. Uncertainty: sigma includes the 5 percent flux floor. Comparison: filled points use the posterior-median model. Open squares use the best sample with the fit's own sigma. Total chi-squared 87.3 over 12 bands gives 7.28 per band. Caveat: the spectrum dominates the joint fit, so the fit does not constrain the bands on their own.</figcaption>
</figure>

<figure>
<img loading="lazy" src="/wiki/f/results/rtx-5060-dr2-quiescent-full-spectrum/129596-M2_129596/diagnostics/spectral_chi2.png" alt="M2_129596: spectral pull, binned mean pull squared, cumulative chi-squared">
<figcaption><code>spectral_chi2.png</code> Pull per fitted pixel of the LEGA-C spectrum of galaxy M2_129596. Below it: mean pull squared in 25 Å bins and the cumulative chi-squared fraction against wavelength. Uncertainty: sigma includes the fitted calibration floor of 3.64 percent of the model flux. Comparison: the stored pull versus the pull at the best sample. Shaded bands mark masked pixels. Red points mark pixels with pull beyond 4 sigma. Total chi-squared 3738.0 over 3563 pixels, 0 outlier pixels. Caveat: the fitted floor absorbs model mismatch, so chi-squared near 1 does not prove a good model.</figcaption>
</figure>

<figure>
<img loading="lazy" src="/wiki/f/results/rtx-5060-dr2-quiescent-full-spectrum/129596-M2_129596/diagnostics/sf_timescales.png" alt="M2_129596: cumulative mass formed against lookback time with t10 to t90">
<figcaption><code>sf_timescales.png</code> Fraction of the final stellar mass of galaxy M2_129596 formed earlier than each lookback time. The line is the posterior median. The band is the 16-84 percent range over 400 draws. Comparison: points mark t10 to t90 with 16-84 percent (thick) and 2.5-97.5 percent (thin) intervals versus the universe age. t50 is 3.51 Gyr with a 16-84 percent range of 3.01 to 3.95 Gyr. Caveat: the 7-bin star-formation history model quantises these times to the bin edges.</figcaption>
</figure>

### 130005-M2_130005

| z | S/N | photometry χ²/N | spectrum χ²/N | f_calib | t50 [Gyr] | model |
| --- | --- | --- | --- | --- | --- | --- |
| 0.8341 | 18.2 | 7.86 | 1.112 | 5.36% | 5.45 | [parameters](/wiki/f/results/rtx-5060-dr2-quiescent-full-spectrum/130005-M2_130005/diagnostics/model_parameters.txt) |

Flags:

- photometry chi2/N 7.9 > 3
- 6 pixels with |pull| > 4

<figure>
<img loading="lazy" src="/wiki/f/results/rtx-5060-dr2-quiescent-full-spectrum/130005-M2_130005/diagnostics/photometric_chi2.png" alt="M2_130005: photometric pull and chi-squared contribution per band">
<figcaption><code>photometric_chi2.png</code> Pull and chi-squared contribution for the 12 COSMOS2015 bands of galaxy M2_130005. Pull equals observed minus model over sigma. Uncertainty: sigma includes the 5 percent flux floor. Comparison: filled points use the posterior-median model. Open squares use the best sample with the fit's own sigma. Total chi-squared 94.3 over 12 bands gives 7.86 per band. Caveat: the spectrum dominates the joint fit, so the fit does not constrain the bands on their own.</figcaption>
</figure>

<figure>
<img loading="lazy" src="/wiki/f/results/rtx-5060-dr2-quiescent-full-spectrum/130005-M2_130005/diagnostics/spectral_chi2.png" alt="M2_130005: spectral pull, binned mean pull squared, cumulative chi-squared">
<figcaption><code>spectral_chi2.png</code> Pull per fitted pixel of the LEGA-C spectrum of galaxy M2_130005. Below it: mean pull squared in 25 Å bins and the cumulative chi-squared fraction against wavelength. Uncertainty: sigma includes the fitted calibration floor of 5.36 percent of the model flux. Comparison: the stored pull versus the pull at the best sample. Shaded bands mark masked pixels. Red points mark pixels with pull beyond 4 sigma. Total chi-squared 3747.1 over 3369 pixels, 6 outlier pixels. Caveat: the fitted floor absorbs model mismatch, so chi-squared near 1 does not prove a good model.</figcaption>
</figure>

<figure>
<img loading="lazy" src="/wiki/f/results/rtx-5060-dr2-quiescent-full-spectrum/130005-M2_130005/diagnostics/sf_timescales.png" alt="M2_130005: cumulative mass formed against lookback time with t10 to t90">
<figcaption><code>sf_timescales.png</code> Fraction of the final stellar mass of galaxy M2_130005 formed earlier than each lookback time. The line is the posterior median. The band is the 16-84 percent range over 400 draws. Comparison: points mark t10 to t90 with 16-84 percent (thick) and 2.5-97.5 percent (thin) intervals versus the universe age. t50 is 5.45 Gyr with a 16-84 percent range of 4.93 to 5.57 Gyr. Caveat: the 7-bin star-formation history model quantises these times to the bin edges.</figcaption>
</figure>

### 130052-M1_130052

| z | S/N | photometry χ²/N | spectrum χ²/N | f_calib | t50 [Gyr] | model |
| --- | --- | --- | --- | --- | --- | --- |
| 0.6041 | 44.3 | 7.04 | 1.025 | 2.65% | 6.38 | [parameters](/wiki/f/results/rtx-5060-dr2-quiescent-full-spectrum/130052-M1_130052/diagnostics/model_parameters.txt) |

Flags:

- photometry chi2/N 7.0 > 3

<figure>
<img loading="lazy" src="/wiki/f/results/rtx-5060-dr2-quiescent-full-spectrum/130052-M1_130052/diagnostics/photometric_chi2.png" alt="M1_130052: photometric pull and chi-squared contribution per band">
<figcaption><code>photometric_chi2.png</code> Pull and chi-squared contribution for the 12 COSMOS2015 bands of galaxy M1_130052. Pull equals observed minus model over sigma. Uncertainty: sigma includes the 5 percent flux floor. Comparison: filled points use the posterior-median model. Open squares use the best sample with the fit's own sigma. Total chi-squared 84.4 over 12 bands gives 7.04 per band. Caveat: the spectrum dominates the joint fit, so the fit does not constrain the bands on their own.</figcaption>
</figure>

<figure>
<img loading="lazy" src="/wiki/f/results/rtx-5060-dr2-quiescent-full-spectrum/130052-M1_130052/diagnostics/spectral_chi2.png" alt="M1_130052: spectral pull, binned mean pull squared, cumulative chi-squared">
<figcaption><code>spectral_chi2.png</code> Pull per fitted pixel of the LEGA-C spectrum of galaxy M1_130052. Below it: mean pull squared in 25 Å bins and the cumulative chi-squared fraction against wavelength. Uncertainty: sigma includes the fitted calibration floor of 2.65 percent of the model flux. Comparison: the stored pull versus the pull at the best sample. Shaded bands mark masked pixels. Red points mark pixels with pull beyond 4 sigma. Total chi-squared 3678.2 over 3590 pixels, 0 outlier pixels. Caveat: the fitted floor absorbs model mismatch, so chi-squared near 1 does not prove a good model.</figcaption>
</figure>

<figure>
<img loading="lazy" src="/wiki/f/results/rtx-5060-dr2-quiescent-full-spectrum/130052-M1_130052/diagnostics/sf_timescales.png" alt="M1_130052: cumulative mass formed against lookback time with t10 to t90">
<figcaption><code>sf_timescales.png</code> Fraction of the final stellar mass of galaxy M1_130052 formed earlier than each lookback time. The line is the posterior median. The band is the 16-84 percent range over 400 draws. Comparison: points mark t10 to t90 with 16-84 percent (thick) and 2.5-97.5 percent (thin) intervals versus the universe age. t50 is 6.38 Gyr with a 16-84 percent range of 6.32 to 6.41 Gyr. Caveat: the 7-bin star-formation history model quantises these times to the bin edges.</figcaption>
</figure>

### 133240-M1_133240

| z | S/N | photometry χ²/N | spectrum χ²/N | f_calib | t50 [Gyr] | model |
| --- | --- | --- | --- | --- | --- | --- |
| 0.7282 | 11.4 | 2.57 | 1.077 | 3.96% | 3.05 | [parameters](/wiki/f/results/rtx-5060-dr2-quiescent-full-spectrum/133240-M1_133240/diagnostics/model_parameters.txt) |

Flags: none.

<figure>
<img loading="lazy" src="/wiki/f/results/rtx-5060-dr2-quiescent-full-spectrum/133240-M1_133240/diagnostics/photometric_chi2.png" alt="M1_133240: photometric pull and chi-squared contribution per band">
<figcaption><code>photometric_chi2.png</code> Pull and chi-squared contribution for the 12 COSMOS2015 bands of galaxy M1_133240. Pull equals observed minus model over sigma. Uncertainty: sigma includes the 5 percent flux floor. Comparison: filled points use the posterior-median model. Open squares use the best sample with the fit's own sigma. Total chi-squared 30.9 over 12 bands gives 2.57 per band. Caveat: the spectrum dominates the joint fit, so the fit does not constrain the bands on their own.</figcaption>
</figure>

<figure>
<img loading="lazy" src="/wiki/f/results/rtx-5060-dr2-quiescent-full-spectrum/133240-M1_133240/diagnostics/spectral_chi2.png" alt="M1_133240: spectral pull, binned mean pull squared, cumulative chi-squared">
<figcaption><code>spectral_chi2.png</code> Pull per fitted pixel of the LEGA-C spectrum of galaxy M1_133240. Below it: mean pull squared in 25 Å bins and the cumulative chi-squared fraction against wavelength. Uncertainty: sigma includes the fitted calibration floor of 3.96 percent of the model flux. Comparison: the stored pull versus the pull at the best sample. Shaded bands mark masked pixels. Red points mark pixels with pull beyond 4 sigma. Total chi-squared 3833.1 over 3560 pixels, 0 outlier pixels. Caveat: the fitted floor absorbs model mismatch, so chi-squared near 1 does not prove a good model.</figcaption>
</figure>

<figure>
<img loading="lazy" src="/wiki/f/results/rtx-5060-dr2-quiescent-full-spectrum/133240-M1_133240/diagnostics/sf_timescales.png" alt="M1_133240: cumulative mass formed against lookback time with t10 to t90">
<figcaption><code>sf_timescales.png</code> Fraction of the final stellar mass of galaxy M1_133240 formed earlier than each lookback time. The line is the posterior median. The band is the 16-84 percent range over 400 draws. Comparison: points mark t10 to t90 with 16-84 percent (thick) and 2.5-97.5 percent (thin) intervals versus the universe age. t50 is 3.05 Gyr with a 16-84 percent range of 3.00 to 3.32 Gyr. Caveat: the 7-bin star-formation history model quantises these times to the bin edges.</figcaption>
</figure>

### 133501-M2_133501

| z | S/N | photometry χ²/N | spectrum χ²/N | f_calib | t50 [Gyr] | model |
| --- | --- | --- | --- | --- | --- | --- |
| 0.7292 | 57.7 | 8.81 | 1.075 | 4.72% | 2.55 | [parameters](/wiki/f/results/rtx-5060-dr2-quiescent-full-spectrum/133501-M2_133501/diagnostics/model_parameters.txt) |

Flags:

- photometry chi2/N 8.8 > 3
- 12 pixels with |pull| > 4

<figure>
<img loading="lazy" src="/wiki/f/results/rtx-5060-dr2-quiescent-full-spectrum/133501-M2_133501/diagnostics/photometric_chi2.png" alt="M2_133501: photometric pull and chi-squared contribution per band">
<figcaption><code>photometric_chi2.png</code> Pull and chi-squared contribution for the 12 COSMOS2015 bands of galaxy M2_133501. Pull equals observed minus model over sigma. Uncertainty: sigma includes the 5 percent flux floor. Comparison: filled points use the posterior-median model. Open squares use the best sample with the fit's own sigma. Total chi-squared 105.8 over 12 bands gives 8.81 per band. Caveat: the spectrum dominates the joint fit, so the fit does not constrain the bands on their own.</figcaption>
</figure>

<figure>
<img loading="lazy" src="/wiki/f/results/rtx-5060-dr2-quiescent-full-spectrum/133501-M2_133501/diagnostics/spectral_chi2.png" alt="M2_133501: spectral pull, binned mean pull squared, cumulative chi-squared">
<figcaption><code>spectral_chi2.png</code> Pull per fitted pixel of the LEGA-C spectrum of galaxy M2_133501. Below it: mean pull squared in 25 Å bins and the cumulative chi-squared fraction against wavelength. Uncertainty: sigma includes the fitted calibration floor of 4.72 percent of the model flux. Comparison: the stored pull versus the pull at the best sample. Shaded bands mark masked pixels. Red points mark pixels with pull beyond 4 sigma. Total chi-squared 3850.3 over 3582 pixels, 12 outlier pixels. Caveat: the fitted floor absorbs model mismatch, so chi-squared near 1 does not prove a good model.</figcaption>
</figure>

<figure>
<img loading="lazy" src="/wiki/f/results/rtx-5060-dr2-quiescent-full-spectrum/133501-M2_133501/diagnostics/sf_timescales.png" alt="M2_133501: cumulative mass formed against lookback time with t10 to t90">
<figcaption><code>sf_timescales.png</code> Fraction of the final stellar mass of galaxy M2_133501 formed earlier than each lookback time. The line is the posterior median. The band is the 16-84 percent range over 400 draws. Comparison: points mark t10 to t90 with 16-84 percent (thick) and 2.5-97.5 percent (thin) intervals versus the universe age. t50 is 2.55 Gyr with a 16-84 percent range of 2.52 to 2.58 Gyr. Caveat: the 7-bin star-formation history model quantises these times to the bin edges.</figcaption>
</figure>

### 134021-M2_134021

| z | S/N | photometry χ²/N | spectrum χ²/N | f_calib | t50 [Gyr] | model |
| --- | --- | --- | --- | --- | --- | --- |
| 0.7493 | 25.8 | 8.55 | 1.054 | 4.17% | 2.44 | [parameters](/wiki/f/results/rtx-5060-dr2-quiescent-full-spectrum/134021-M2_134021/diagnostics/model_parameters.txt) |

Flags:

- photometry chi2/N 8.6 > 3
- 1 pixels with |pull| > 4

<figure>
<img loading="lazy" src="/wiki/f/results/rtx-5060-dr2-quiescent-full-spectrum/134021-M2_134021/diagnostics/photometric_chi2.png" alt="M2_134021: photometric pull and chi-squared contribution per band">
<figcaption><code>photometric_chi2.png</code> Pull and chi-squared contribution for the 12 COSMOS2015 bands of galaxy M2_134021. Pull equals observed minus model over sigma. Uncertainty: sigma includes the 5 percent flux floor. Comparison: filled points use the posterior-median model. Open squares use the best sample with the fit's own sigma. Total chi-squared 102.6 over 12 bands gives 8.55 per band. Caveat: the spectrum dominates the joint fit, so the fit does not constrain the bands on their own.</figcaption>
</figure>

<figure>
<img loading="lazy" src="/wiki/f/results/rtx-5060-dr2-quiescent-full-spectrum/134021-M2_134021/diagnostics/spectral_chi2.png" alt="M2_134021: spectral pull, binned mean pull squared, cumulative chi-squared">
<figcaption><code>spectral_chi2.png</code> Pull per fitted pixel of the LEGA-C spectrum of galaxy M2_134021. Below it: mean pull squared in 25 Å bins and the cumulative chi-squared fraction against wavelength. Uncertainty: sigma includes the fitted calibration floor of 4.17 percent of the model flux. Comparison: the stored pull versus the pull at the best sample. Shaded bands mark masked pixels. Red points mark pixels with pull beyond 4 sigma. Total chi-squared 3748.4 over 3558 pixels, 1 outlier pixels. Caveat: the fitted floor absorbs model mismatch, so chi-squared near 1 does not prove a good model.</figcaption>
</figure>

<figure>
<img loading="lazy" src="/wiki/f/results/rtx-5060-dr2-quiescent-full-spectrum/134021-M2_134021/diagnostics/sf_timescales.png" alt="M2_134021: cumulative mass formed against lookback time with t10 to t90">
<figcaption><code>sf_timescales.png</code> Fraction of the final stellar mass of galaxy M2_134021 formed earlier than each lookback time. The line is the posterior median. The band is the 16-84 percent range over 400 draws. Comparison: points mark t10 to t90 with 16-84 percent (thick) and 2.5-97.5 percent (thin) intervals versus the universe age. t50 is 2.44 Gyr with a 16-84 percent range of 2.39 to 2.51 Gyr. Caveat: the 7-bin star-formation history model quantises these times to the bin edges.</figcaption>
</figure>

### 134391-M2_134391

| z | S/N | photometry χ²/N | spectrum χ²/N | f_calib | t50 [Gyr] | model |
| --- | --- | --- | --- | --- | --- | --- |
| 0.6835 | 44.6 | 19.58 | 1.137 | 2.90% | 3.00 | [parameters](/wiki/f/results/rtx-5060-dr2-quiescent-full-spectrum/134391-M2_134391/diagnostics/model_parameters.txt) |

Flags:

- photometry chi2/N 19.6 > 3
- 5 pixels with |pull| > 4

<figure>
<img loading="lazy" src="/wiki/f/results/rtx-5060-dr2-quiescent-full-spectrum/134391-M2_134391/diagnostics/photometric_chi2.png" alt="M2_134391: photometric pull and chi-squared contribution per band">
<figcaption><code>photometric_chi2.png</code> Pull and chi-squared contribution for the 12 COSMOS2015 bands of galaxy M2_134391. Pull equals observed minus model over sigma. Uncertainty: sigma includes the 5 percent flux floor. Comparison: filled points use the posterior-median model. Open squares use the best sample with the fit's own sigma. Total chi-squared 235.0 over 12 bands gives 19.58 per band. Caveat: the spectrum dominates the joint fit, so the fit does not constrain the bands on their own.</figcaption>
</figure>

<figure>
<img loading="lazy" src="/wiki/f/results/rtx-5060-dr2-quiescent-full-spectrum/134391-M2_134391/diagnostics/spectral_chi2.png" alt="M2_134391: spectral pull, binned mean pull squared, cumulative chi-squared">
<figcaption><code>spectral_chi2.png</code> Pull per fitted pixel of the LEGA-C spectrum of galaxy M2_134391. Below it: mean pull squared in 25 Å bins and the cumulative chi-squared fraction against wavelength. Uncertainty: sigma includes the fitted calibration floor of 2.90 percent of the model flux. Comparison: the stored pull versus the pull at the best sample. Shaded bands mark masked pixels. Red points mark pixels with pull beyond 4 sigma. Total chi-squared 4054.5 over 3567 pixels, 5 outlier pixels. Caveat: the fitted floor absorbs model mismatch, so chi-squared near 1 does not prove a good model.</figcaption>
</figure>

<figure>
<img loading="lazy" src="/wiki/f/results/rtx-5060-dr2-quiescent-full-spectrum/134391-M2_134391/diagnostics/sf_timescales.png" alt="M2_134391: cumulative mass formed against lookback time with t10 to t90">
<figcaption><code>sf_timescales.png</code> Fraction of the final stellar mass of galaxy M2_134391 formed earlier than each lookback time. The line is the posterior median. The band is the 16-84 percent range over 400 draws. Comparison: points mark t10 to t90 with 16-84 percent (thick) and 2.5-97.5 percent (thin) intervals versus the universe age. t50 is 3.00 Gyr with a 16-84 percent range of 2.99 to 3.02 Gyr. Caveat: the 7-bin star-formation history model quantises these times to the bin edges.</figcaption>
</figure>

### 139423-M1_139423

| z | S/N | photometry χ²/N | spectrum χ²/N | f_calib | t50 [Gyr] | model |
| --- | --- | --- | --- | --- | --- | --- |
| 0.7495 | 28.1 | 3.92 | 1.149 | 5.91% | 2.10 | [parameters](/wiki/f/results/rtx-5060-dr2-quiescent-full-spectrum/139423-M1_139423/diagnostics/model_parameters.txt) |

Flags:

- photometry chi2/N 3.9 > 3
- 16 pixels with |pull| > 4

<figure>
<img loading="lazy" src="/wiki/f/results/rtx-5060-dr2-quiescent-full-spectrum/139423-M1_139423/diagnostics/photometric_chi2.png" alt="M1_139423: photometric pull and chi-squared contribution per band">
<figcaption><code>photometric_chi2.png</code> Pull and chi-squared contribution for the 12 COSMOS2015 bands of galaxy M1_139423. Pull equals observed minus model over sigma. Uncertainty: sigma includes the 5 percent flux floor. Comparison: filled points use the posterior-median model. Open squares use the best sample with the fit's own sigma. Total chi-squared 47.0 over 12 bands gives 3.92 per band. Caveat: the spectrum dominates the joint fit, so the fit does not constrain the bands on their own.</figcaption>
</figure>

<figure>
<img loading="lazy" src="/wiki/f/results/rtx-5060-dr2-quiescent-full-spectrum/139423-M1_139423/diagnostics/spectral_chi2.png" alt="M1_139423: spectral pull, binned mean pull squared, cumulative chi-squared">
<figcaption><code>spectral_chi2.png</code> Pull per fitted pixel of the LEGA-C spectrum of galaxy M1_139423. Below it: mean pull squared in 25 Å bins and the cumulative chi-squared fraction against wavelength. Uncertainty: sigma includes the fitted calibration floor of 5.91 percent of the model flux. Comparison: the stored pull versus the pull at the best sample. Shaded bands mark masked pixels. Red points mark pixels with pull beyond 4 sigma. Total chi-squared 3971.6 over 3456 pixels, 16 outlier pixels. Caveat: the fitted floor absorbs model mismatch, so chi-squared near 1 does not prove a good model.</figcaption>
</figure>

<figure>
<img loading="lazy" src="/wiki/f/results/rtx-5060-dr2-quiescent-full-spectrum/139423-M1_139423/diagnostics/sf_timescales.png" alt="M1_139423: cumulative mass formed against lookback time with t10 to t90">
<figcaption><code>sf_timescales.png</code> Fraction of the final stellar mass of galaxy M1_139423 formed earlier than each lookback time. The line is the posterior median. The band is the 16-84 percent range over 400 draws. Comparison: points mark t10 to t90 with 16-84 percent (thick) and 2.5-97.5 percent (thin) intervals versus the universe age. t50 is 2.10 Gyr with a 16-84 percent range of 2.02 to 2.17 Gyr. Caveat: the 7-bin star-formation history model quantises these times to the bin edges.</figcaption>
</figure>

### 139662-M2_139662

| z | S/N | photometry χ²/N | spectrum χ²/N | f_calib | t50 [Gyr] | model |
| --- | --- | --- | --- | --- | --- | --- |
| 0.6706 | 17.3 | 3.87 | 2.685 | 10.00% | 5.86 | [parameters](/wiki/f/results/rtx-5060-dr2-quiescent-full-spectrum/139662-M2_139662/diagnostics/model_parameters.txt) |

Flags:

- photometry chi2/N 3.9 > 3
- spectrum chi2/N 2.68 > 1.5
- calibration floor at prior bound (10.0% of 10%)
- 82 pixels with |pull| > 4

<figure>
<img loading="lazy" src="/wiki/f/results/rtx-5060-dr2-quiescent-full-spectrum/139662-M2_139662/diagnostics/photometric_chi2.png" alt="M2_139662: photometric pull and chi-squared contribution per band">
<figcaption><code>photometric_chi2.png</code> Pull and chi-squared contribution for the 12 COSMOS2015 bands of galaxy M2_139662. Pull equals observed minus model over sigma. Uncertainty: sigma includes the 5 percent flux floor. Comparison: filled points use the posterior-median model. Open squares use the best sample with the fit's own sigma. Total chi-squared 46.5 over 12 bands gives 3.87 per band. Caveat: the spectrum dominates the joint fit, so the fit does not constrain the bands on their own.</figcaption>
</figure>

<figure>
<img loading="lazy" src="/wiki/f/results/rtx-5060-dr2-quiescent-full-spectrum/139662-M2_139662/diagnostics/spectral_chi2.png" alt="M2_139662: spectral pull, binned mean pull squared, cumulative chi-squared">
<figcaption><code>spectral_chi2.png</code> Pull per fitted pixel of the LEGA-C spectrum of galaxy M2_139662. Below it: mean pull squared in 25 Å bins and the cumulative chi-squared fraction against wavelength. Uncertainty: sigma includes the fitted calibration floor of 10.00 percent of the model flux. Comparison: the stored pull versus the pull at the best sample. Shaded bands mark masked pixels. Red points mark pixels with pull beyond 4 sigma. Total chi-squared 9209.2 over 3430 pixels, 82 outlier pixels. Caveat: the fitted floor absorbs model mismatch, so chi-squared near 1 does not prove a good model.</figcaption>
</figure>

<figure>
<img loading="lazy" src="/wiki/f/results/rtx-5060-dr2-quiescent-full-spectrum/139662-M2_139662/diagnostics/sf_timescales.png" alt="M2_139662: cumulative mass formed against lookback time with t10 to t90">
<figcaption><code>sf_timescales.png</code> Fraction of the final stellar mass of galaxy M2_139662 formed earlier than each lookback time. The line is the posterior median. The band is the 16-84 percent range over 400 draws. Comparison: points mark t10 to t90 with 16-84 percent (thick) and 2.5-97.5 percent (thin) intervals versus the universe age. t50 is 5.86 Gyr with a 16-84 percent range of 5.69 to 5.94 Gyr. Caveat: the 7-bin star-formation history model quantises these times to the bin edges.</figcaption>
</figure>

### 143127-M7_143127

| z | S/N | photometry χ²/N | spectrum χ²/N | f_calib | t50 [Gyr] | model |
| --- | --- | --- | --- | --- | --- | --- |
| 0.6964 | 12.2 | 3.32 | 1.204 | 7.51% | 3.25 | [parameters](/wiki/f/results/rtx-5060-dr2-quiescent-full-spectrum/143127-M7_143127/diagnostics/model_parameters.txt) |

Flags:

- photometry chi2/N 3.3 > 3
- 12 pixels with |pull| > 4

<figure>
<img loading="lazy" src="/wiki/f/results/rtx-5060-dr2-quiescent-full-spectrum/143127-M7_143127/diagnostics/photometric_chi2.png" alt="M7_143127: photometric pull and chi-squared contribution per band">
<figcaption><code>photometric_chi2.png</code> Pull and chi-squared contribution for the 12 COSMOS2015 bands of galaxy M7_143127. Pull equals observed minus model over sigma. Uncertainty: sigma includes the 5 percent flux floor. Comparison: filled points use the posterior-median model. Open squares use the best sample with the fit's own sigma. Total chi-squared 39.9 over 12 bands gives 3.32 per band. Caveat: the spectrum dominates the joint fit, so the fit does not constrain the bands on their own.</figcaption>
</figure>

<figure>
<img loading="lazy" src="/wiki/f/results/rtx-5060-dr2-quiescent-full-spectrum/143127-M7_143127/diagnostics/spectral_chi2.png" alt="M7_143127: spectral pull, binned mean pull squared, cumulative chi-squared">
<figcaption><code>spectral_chi2.png</code> Pull per fitted pixel of the LEGA-C spectrum of galaxy M7_143127. Below it: mean pull squared in 25 Å bins and the cumulative chi-squared fraction against wavelength. Uncertainty: sigma includes the fitted calibration floor of 7.51 percent of the model flux. Comparison: the stored pull versus the pull at the best sample. Shaded bands mark masked pixels. Red points mark pixels with pull beyond 4 sigma. Total chi-squared 4257.9 over 3537 pixels, 12 outlier pixels. Caveat: the fitted floor absorbs model mismatch, so chi-squared near 1 does not prove a good model.</figcaption>
</figure>

<figure>
<img loading="lazy" src="/wiki/f/results/rtx-5060-dr2-quiescent-full-spectrum/143127-M7_143127/diagnostics/sf_timescales.png" alt="M7_143127: cumulative mass formed against lookback time with t10 to t90">
<figcaption><code>sf_timescales.png</code> Fraction of the final stellar mass of galaxy M7_143127 formed earlier than each lookback time. The line is the posterior median. The band is the 16-84 percent range over 400 draws. Comparison: points mark t10 to t90 with 16-84 percent (thick) and 2.5-97.5 percent (thin) intervals versus the universe age. t50 is 3.25 Gyr with a 16-84 percent range of 3.01 to 3.90 Gyr. Caveat: the 7-bin star-formation history model quantises these times to the bin edges.</figcaption>
</figure>

### 145276-M8_145276

| z | S/N | photometry χ²/N | spectrum χ²/N | f_calib | t50 [Gyr] | model |
| --- | --- | --- | --- | --- | --- | --- |
| 0.7506 | 17.2 | 1.80 | 1.101 | 4.08% | 2.94 | [parameters](/wiki/f/results/rtx-5060-dr2-quiescent-full-spectrum/145276-M8_145276/diagnostics/model_parameters.txt) |

Flags:

- 7 pixels with |pull| > 4

<figure>
<img loading="lazy" src="/wiki/f/results/rtx-5060-dr2-quiescent-full-spectrum/145276-M8_145276/diagnostics/photometric_chi2.png" alt="M8_145276: photometric pull and chi-squared contribution per band">
<figcaption><code>photometric_chi2.png</code> Pull and chi-squared contribution for the 12 COSMOS2015 bands of galaxy M8_145276. Pull equals observed minus model over sigma. Uncertainty: sigma includes the 5 percent flux floor. Comparison: filled points use the posterior-median model. Open squares use the best sample with the fit's own sigma. Total chi-squared 21.5 over 12 bands gives 1.80 per band. Caveat: the spectrum dominates the joint fit, so the fit does not constrain the bands on their own.</figcaption>
</figure>

<figure>
<img loading="lazy" src="/wiki/f/results/rtx-5060-dr2-quiescent-full-spectrum/145276-M8_145276/diagnostics/spectral_chi2.png" alt="M8_145276: spectral pull, binned mean pull squared, cumulative chi-squared">
<figcaption><code>spectral_chi2.png</code> Pull per fitted pixel of the LEGA-C spectrum of galaxy M8_145276. Below it: mean pull squared in 25 Å bins and the cumulative chi-squared fraction against wavelength. Uncertainty: sigma includes the fitted calibration floor of 4.08 percent of the model flux. Comparison: the stored pull versus the pull at the best sample. Shaded bands mark masked pixels. Red points mark pixels with pull beyond 4 sigma. Total chi-squared 3870.6 over 3516 pixels, 7 outlier pixels. Caveat: the fitted floor absorbs model mismatch, so chi-squared near 1 does not prove a good model.</figcaption>
</figure>

<figure>
<img loading="lazy" src="/wiki/f/results/rtx-5060-dr2-quiescent-full-spectrum/145276-M8_145276/diagnostics/sf_timescales.png" alt="M8_145276: cumulative mass formed against lookback time with t10 to t90">
<figcaption><code>sf_timescales.png</code> Fraction of the final stellar mass of galaxy M8_145276 formed earlier than each lookback time. The line is the posterior median. The band is the 16-84 percent range over 400 draws. Comparison: points mark t10 to t90 with 16-84 percent (thick) and 2.5-97.5 percent (thin) intervals versus the universe age. t50 is 2.94 Gyr with a 16-84 percent range of 2.86 to 3.00 Gyr. Caveat: the 7-bin star-formation history model quantises these times to the bin edges.</figcaption>
</figure>

### 146213-M7_146213

| z | S/N | photometry χ²/N | spectrum χ²/N | f_calib | t50 [Gyr] | model |
| --- | --- | --- | --- | --- | --- | --- |
| 0.6875 | 19.2 | 3.26 | 1.116 | 5.19% | 3.02 | [parameters](/wiki/f/results/rtx-5060-dr2-quiescent-full-spectrum/146213-M7_146213/diagnostics/model_parameters.txt) |

Flags:

- photometry chi2/N 3.3 > 3
- 3 pixels with |pull| > 4

<figure>
<img loading="lazy" src="/wiki/f/results/rtx-5060-dr2-quiescent-full-spectrum/146213-M7_146213/diagnostics/photometric_chi2.png" alt="M7_146213: photometric pull and chi-squared contribution per band">
<figcaption><code>photometric_chi2.png</code> Pull and chi-squared contribution for the 12 COSMOS2015 bands of galaxy M7_146213. Pull equals observed minus model over sigma. Uncertainty: sigma includes the 5 percent flux floor. Comparison: filled points use the posterior-median model. Open squares use the best sample with the fit's own sigma. Total chi-squared 39.1 over 12 bands gives 3.26 per band. Caveat: the spectrum dominates the joint fit, so the fit does not constrain the bands on their own.</figcaption>
</figure>

<figure>
<img loading="lazy" src="/wiki/f/results/rtx-5060-dr2-quiescent-full-spectrum/146213-M7_146213/diagnostics/spectral_chi2.png" alt="M7_146213: spectral pull, binned mean pull squared, cumulative chi-squared">
<figcaption><code>spectral_chi2.png</code> Pull per fitted pixel of the LEGA-C spectrum of galaxy M7_146213. Below it: mean pull squared in 25 Å bins and the cumulative chi-squared fraction against wavelength. Uncertainty: sigma includes the fitted calibration floor of 5.19 percent of the model flux. Comparison: the stored pull versus the pull at the best sample. Shaded bands mark masked pixels. Red points mark pixels with pull beyond 4 sigma. Total chi-squared 3970.3 over 3557 pixels, 3 outlier pixels. Caveat: the fitted floor absorbs model mismatch, so chi-squared near 1 does not prove a good model.</figcaption>
</figure>

<figure>
<img loading="lazy" src="/wiki/f/results/rtx-5060-dr2-quiescent-full-spectrum/146213-M7_146213/diagnostics/sf_timescales.png" alt="M7_146213: cumulative mass formed against lookback time with t10 to t90">
<figcaption><code>sf_timescales.png</code> Fraction of the final stellar mass of galaxy M7_146213 formed earlier than each lookback time. The line is the posterior median. The band is the 16-84 percent range over 400 draws. Comparison: points mark t10 to t90 with 16-84 percent (thick) and 2.5-97.5 percent (thin) intervals versus the universe age. t50 is 3.02 Gyr with a 16-84 percent range of 2.99 to 3.18 Gyr. Caveat: the 7-bin star-formation history model quantises these times to the bin edges.</figcaption>
</figure>

### 147270-M7_147270

| z | S/N | photometry χ²/N | spectrum χ²/N | f_calib | t50 [Gyr] | model |
| --- | --- | --- | --- | --- | --- | --- |
| 0.8473 | 20.8 | 6.50 | 1.105 | 4.47% | 4.54 | [parameters](/wiki/f/results/rtx-5060-dr2-quiescent-full-spectrum/147270-M7_147270/diagnostics/model_parameters.txt) |

Flags:

- photometry chi2/N 6.5 > 3
- 1 pixels with |pull| > 4

<figure>
<img loading="lazy" src="/wiki/f/results/rtx-5060-dr2-quiescent-full-spectrum/147270-M7_147270/diagnostics/photometric_chi2.png" alt="M7_147270: photometric pull and chi-squared contribution per band">
<figcaption><code>photometric_chi2.png</code> Pull and chi-squared contribution for the 12 COSMOS2015 bands of galaxy M7_147270. Pull equals observed minus model over sigma. Uncertainty: sigma includes the 5 percent flux floor. Comparison: filled points use the posterior-median model. Open squares use the best sample with the fit's own sigma. Total chi-squared 78.0 over 12 bands gives 6.50 per band. Caveat: the spectrum dominates the joint fit, so the fit does not constrain the bands on their own.</figcaption>
</figure>

<figure>
<img loading="lazy" src="/wiki/f/results/rtx-5060-dr2-quiescent-full-spectrum/147270-M7_147270/diagnostics/spectral_chi2.png" alt="M7_147270: spectral pull, binned mean pull squared, cumulative chi-squared">
<figcaption><code>spectral_chi2.png</code> Pull per fitted pixel of the LEGA-C spectrum of galaxy M7_147270. Below it: mean pull squared in 25 Å bins and the cumulative chi-squared fraction against wavelength. Uncertainty: sigma includes the fitted calibration floor of 4.47 percent of the model flux. Comparison: the stored pull versus the pull at the best sample. Shaded bands mark masked pixels. Red points mark pixels with pull beyond 4 sigma. Total chi-squared 4246.0 over 3843 pixels, 1 outlier pixels. Caveat: the fitted floor absorbs model mismatch, so chi-squared near 1 does not prove a good model.</figcaption>
</figure>

<figure>
<img loading="lazy" src="/wiki/f/results/rtx-5060-dr2-quiescent-full-spectrum/147270-M7_147270/diagnostics/sf_timescales.png" alt="M7_147270: cumulative mass formed against lookback time with t10 to t90">
<figcaption><code>sf_timescales.png</code> Fraction of the final stellar mass of galaxy M7_147270 formed earlier than each lookback time. The line is the posterior median. The band is the 16-84 percent range over 400 draws. Comparison: points mark t10 to t90 with 16-84 percent (thick) and 2.5-97.5 percent (thin) intervals versus the universe age. t50 is 4.54 Gyr with a 16-84 percent range of 4.48 to 4.64 Gyr. Caveat: the 7-bin star-formation history model quantises these times to the bin edges.</figcaption>
</figure>

### 147539-M8_147539

| z | S/N | photometry χ²/N | spectrum χ²/N | f_calib | t50 [Gyr] | model |
| --- | --- | --- | --- | --- | --- | --- |
| 0.6958 | 30.5 | 7.06 | 1.192 | 3.68% | 3.89 | [parameters](/wiki/f/results/rtx-5060-dr2-quiescent-full-spectrum/147539-M8_147539/diagnostics/model_parameters.txt) |

Flags:

- photometry chi2/N 7.1 > 3
- 8 pixels with |pull| > 4

<figure>
<img loading="lazy" src="/wiki/f/results/rtx-5060-dr2-quiescent-full-spectrum/147539-M8_147539/diagnostics/photometric_chi2.png" alt="M8_147539: photometric pull and chi-squared contribution per band">
<figcaption><code>photometric_chi2.png</code> Pull and chi-squared contribution for the 12 COSMOS2015 bands of galaxy M8_147539. Pull equals observed minus model over sigma. Uncertainty: sigma includes the 5 percent flux floor. Comparison: filled points use the posterior-median model. Open squares use the best sample with the fit's own sigma. Total chi-squared 84.7 over 12 bands gives 7.06 per band. Caveat: the spectrum dominates the joint fit, so the fit does not constrain the bands on their own.</figcaption>
</figure>

<figure>
<img loading="lazy" src="/wiki/f/results/rtx-5060-dr2-quiescent-full-spectrum/147539-M8_147539/diagnostics/spectral_chi2.png" alt="M8_147539: spectral pull, binned mean pull squared, cumulative chi-squared">
<figcaption><code>spectral_chi2.png</code> Pull per fitted pixel of the LEGA-C spectrum of galaxy M8_147539. Below it: mean pull squared in 25 Å bins and the cumulative chi-squared fraction against wavelength. Uncertainty: sigma includes the fitted calibration floor of 3.68 percent of the model flux. Comparison: the stored pull versus the pull at the best sample. Shaded bands mark masked pixels. Red points mark pixels with pull beyond 4 sigma. Total chi-squared 4241.1 over 3558 pixels, 8 outlier pixels. Caveat: the fitted floor absorbs model mismatch, so chi-squared near 1 does not prove a good model.</figcaption>
</figure>

<figure>
<img loading="lazy" src="/wiki/f/results/rtx-5060-dr2-quiescent-full-spectrum/147539-M8_147539/diagnostics/sf_timescales.png" alt="M8_147539: cumulative mass formed against lookback time with t10 to t90">
<figcaption><code>sf_timescales.png</code> Fraction of the final stellar mass of galaxy M8_147539 formed earlier than each lookback time. The line is the posterior median. The band is the 16-84 percent range over 400 draws. Comparison: points mark t10 to t90 with 16-84 percent (thick) and 2.5-97.5 percent (thin) intervals versus the universe age. t50 is 3.89 Gyr with a 16-84 percent range of 3.65 to 4.15 Gyr. Caveat: the 7-bin star-formation history model quantises these times to the bin edges.</figcaption>
</figure>

### 147849-M7_147849

| z | S/N | photometry χ²/N | spectrum χ²/N | f_calib | t50 [Gyr] | model |
| --- | --- | --- | --- | --- | --- | --- |
| 0.6773 | 29.8 | 12.99 | 1.155 | 4.21% | 3.00 | [parameters](/wiki/f/results/rtx-5060-dr2-quiescent-full-spectrum/147849-M7_147849/diagnostics/model_parameters.txt) |

Flags:

- photometry chi2/N 13.0 > 3
- 7 pixels with |pull| > 4

<figure>
<img loading="lazy" src="/wiki/f/results/rtx-5060-dr2-quiescent-full-spectrum/147849-M7_147849/diagnostics/photometric_chi2.png" alt="M7_147849: photometric pull and chi-squared contribution per band">
<figcaption><code>photometric_chi2.png</code> Pull and chi-squared contribution for the 12 COSMOS2015 bands of galaxy M7_147849. Pull equals observed minus model over sigma. Uncertainty: sigma includes the 5 percent flux floor. Comparison: filled points use the posterior-median model. Open squares use the best sample with the fit's own sigma. Total chi-squared 155.9 over 12 bands gives 12.99 per band. Caveat: the spectrum dominates the joint fit, so the fit does not constrain the bands on their own.</figcaption>
</figure>

<figure>
<img loading="lazy" src="/wiki/f/results/rtx-5060-dr2-quiescent-full-spectrum/147849-M7_147849/diagnostics/spectral_chi2.png" alt="M7_147849: spectral pull, binned mean pull squared, cumulative chi-squared">
<figcaption><code>spectral_chi2.png</code> Pull per fitted pixel of the LEGA-C spectrum of galaxy M7_147849. Below it: mean pull squared in 25 Å bins and the cumulative chi-squared fraction against wavelength. Uncertainty: sigma includes the fitted calibration floor of 4.21 percent of the model flux. Comparison: the stored pull versus the pull at the best sample. Shaded bands mark masked pixels. Red points mark pixels with pull beyond 4 sigma. Total chi-squared 4110.8 over 3560 pixels, 7 outlier pixels. Caveat: the fitted floor absorbs model mismatch, so chi-squared near 1 does not prove a good model.</figcaption>
</figure>

<figure>
<img loading="lazy" src="/wiki/f/results/rtx-5060-dr2-quiescent-full-spectrum/147849-M7_147849/diagnostics/sf_timescales.png" alt="M7_147849: cumulative mass formed against lookback time with t10 to t90">
<figcaption><code>sf_timescales.png</code> Fraction of the final stellar mass of galaxy M7_147849 formed earlier than each lookback time. The line is the posterior median. The band is the 16-84 percent range over 400 draws. Comparison: points mark t10 to t90 with 16-84 percent (thick) and 2.5-97.5 percent (thin) intervals versus the universe age. t50 is 3.00 Gyr with a 16-84 percent range of 2.99 to 3.04 Gyr. Caveat: the 7-bin star-formation history model quantises these times to the bin edges.</figcaption>
</figure>

### 148698-M8_148698

| z | S/N | photometry χ²/N | spectrum χ²/N | f_calib | t50 [Gyr] | model |
| --- | --- | --- | --- | --- | --- | --- |
| 0.6755 | 33.0 | 1.72 | 1.072 | 3.59% | 1.64 | [parameters](/wiki/f/results/rtx-5060-dr2-quiescent-full-spectrum/148698-M8_148698/diagnostics/model_parameters.txt) |

Flags:

- 1 pixels with |pull| > 4

<figure>
<img loading="lazy" src="/wiki/f/results/rtx-5060-dr2-quiescent-full-spectrum/148698-M8_148698/diagnostics/photometric_chi2.png" alt="M8_148698: photometric pull and chi-squared contribution per band">
<figcaption><code>photometric_chi2.png</code> Pull and chi-squared contribution for the 12 COSMOS2015 bands of galaxy M8_148698. Pull equals observed minus model over sigma. Uncertainty: sigma includes the 5 percent flux floor. Comparison: filled points use the posterior-median model. Open squares use the best sample with the fit's own sigma. Total chi-squared 20.6 over 12 bands gives 1.72 per band. Caveat: the spectrum dominates the joint fit, so the fit does not constrain the bands on their own.</figcaption>
</figure>

<figure>
<img loading="lazy" src="/wiki/f/results/rtx-5060-dr2-quiescent-full-spectrum/148698-M8_148698/diagnostics/spectral_chi2.png" alt="M8_148698: spectral pull, binned mean pull squared, cumulative chi-squared">
<figcaption><code>spectral_chi2.png</code> Pull per fitted pixel of the LEGA-C spectrum of galaxy M8_148698. Below it: mean pull squared in 25 Å bins and the cumulative chi-squared fraction against wavelength. Uncertainty: sigma includes the fitted calibration floor of 3.59 percent of the model flux. Comparison: the stored pull versus the pull at the best sample. Shaded bands mark masked pixels. Red points mark pixels with pull beyond 4 sigma. Total chi-squared 3844.3 over 3587 pixels, 1 outlier pixels. Caveat: the fitted floor absorbs model mismatch, so chi-squared near 1 does not prove a good model.</figcaption>
</figure>

<figure>
<img loading="lazy" src="/wiki/f/results/rtx-5060-dr2-quiescent-full-spectrum/148698-M8_148698/diagnostics/sf_timescales.png" alt="M8_148698: cumulative mass formed against lookback time with t10 to t90">
<figcaption><code>sf_timescales.png</code> Fraction of the final stellar mass of galaxy M8_148698 formed earlier than each lookback time. The line is the posterior median. The band is the 16-84 percent range over 400 draws. Comparison: points mark t10 to t90 with 16-84 percent (thick) and 2.5-97.5 percent (thin) intervals versus the universe age. t50 is 1.64 Gyr with a 16-84 percent range of 1.62 to 1.65 Gyr. Caveat: the 7-bin star-formation history model quantises these times to the bin edges.</figcaption>
</figure>

### 150848-M8_150848

| z | S/N | photometry χ²/N | spectrum χ²/N | f_calib | t50 [Gyr] | model |
| --- | --- | --- | --- | --- | --- | --- |
| 0.7011 | 40.9 | 9.12 | 1.103 | 3.05% | 3.01 | [parameters](/wiki/f/results/rtx-5060-dr2-quiescent-full-spectrum/150848-M8_150848/diagnostics/model_parameters.txt) |

Flags:

- photometry chi2/N 9.1 > 3
- 3 pixels with |pull| > 4

<figure>
<img loading="lazy" src="/wiki/f/results/rtx-5060-dr2-quiescent-full-spectrum/150848-M8_150848/diagnostics/photometric_chi2.png" alt="M8_150848: photometric pull and chi-squared contribution per band">
<figcaption><code>photometric_chi2.png</code> Pull and chi-squared contribution for the 12 COSMOS2015 bands of galaxy M8_150848. Pull equals observed minus model over sigma. Uncertainty: sigma includes the 5 percent flux floor. Comparison: filled points use the posterior-median model. Open squares use the best sample with the fit's own sigma. Total chi-squared 109.5 over 12 bands gives 9.12 per band. Caveat: the spectrum dominates the joint fit, so the fit does not constrain the bands on their own.</figcaption>
</figure>

<figure>
<img loading="lazy" src="/wiki/f/results/rtx-5060-dr2-quiescent-full-spectrum/150848-M8_150848/diagnostics/spectral_chi2.png" alt="M8_150848: spectral pull, binned mean pull squared, cumulative chi-squared">
<figcaption><code>spectral_chi2.png</code> Pull per fitted pixel of the LEGA-C spectrum of galaxy M8_150848. Below it: mean pull squared in 25 Å bins and the cumulative chi-squared fraction against wavelength. Uncertainty: sigma includes the fitted calibration floor of 3.05 percent of the model flux. Comparison: the stored pull versus the pull at the best sample. Shaded bands mark masked pixels. Red points mark pixels with pull beyond 4 sigma. Total chi-squared 3945.2 over 3576 pixels, 3 outlier pixels. Caveat: the fitted floor absorbs model mismatch, so chi-squared near 1 does not prove a good model.</figcaption>
</figure>

<figure>
<img loading="lazy" src="/wiki/f/results/rtx-5060-dr2-quiescent-full-spectrum/150848-M8_150848/diagnostics/sf_timescales.png" alt="M8_150848: cumulative mass formed against lookback time with t10 to t90">
<figcaption><code>sf_timescales.png</code> Fraction of the final stellar mass of galaxy M8_150848 formed earlier than each lookback time. The line is the posterior median. The band is the 16-84 percent range over 400 draws. Comparison: points mark t10 to t90 with 16-84 percent (thick) and 2.5-97.5 percent (thin) intervals versus the universe age. t50 is 3.01 Gyr with a 16-84 percent range of 3.00 to 3.04 Gyr. Caveat: the 7-bin star-formation history model quantises these times to the bin edges.</figcaption>
</figure>

### 152125-M7_152125

| z | S/N | photometry χ²/N | spectrum χ²/N | f_calib | t50 [Gyr] | model |
| --- | --- | --- | --- | --- | --- | --- |
| 0.7871 | 16.0 | 10.82 | 1.099 | 6.42% | 3.00 | [parameters](/wiki/f/results/rtx-5060-dr2-quiescent-full-spectrum/152125-M7_152125/diagnostics/model_parameters.txt) |

Flags:

- photometry chi2/N 10.8 > 3
- 8 pixels with |pull| > 4

<figure>
<img loading="lazy" src="/wiki/f/results/rtx-5060-dr2-quiescent-full-spectrum/152125-M7_152125/diagnostics/photometric_chi2.png" alt="M7_152125: photometric pull and chi-squared contribution per band">
<figcaption><code>photometric_chi2.png</code> Pull and chi-squared contribution for the 12 COSMOS2015 bands of galaxy M7_152125. Pull equals observed minus model over sigma. Uncertainty: sigma includes the 5 percent flux floor. Comparison: filled points use the posterior-median model. Open squares use the best sample with the fit's own sigma. Total chi-squared 129.9 over 12 bands gives 10.82 per band. Caveat: the spectrum dominates the joint fit, so the fit does not constrain the bands on their own.</figcaption>
</figure>

<figure>
<img loading="lazy" src="/wiki/f/results/rtx-5060-dr2-quiescent-full-spectrum/152125-M7_152125/diagnostics/spectral_chi2.png" alt="M7_152125: spectral pull, binned mean pull squared, cumulative chi-squared">
<figcaption><code>spectral_chi2.png</code> Pull per fitted pixel of the LEGA-C spectrum of galaxy M7_152125. Below it: mean pull squared in 25 Å bins and the cumulative chi-squared fraction against wavelength. Uncertainty: sigma includes the fitted calibration floor of 6.42 percent of the model flux. Comparison: the stored pull versus the pull at the best sample. Shaded bands mark masked pixels. Red points mark pixels with pull beyond 4 sigma. Total chi-squared 3966.1 over 3608 pixels, 8 outlier pixels. Caveat: the fitted floor absorbs model mismatch, so chi-squared near 1 does not prove a good model.</figcaption>
</figure>

<figure>
<img loading="lazy" src="/wiki/f/results/rtx-5060-dr2-quiescent-full-spectrum/152125-M7_152125/diagnostics/sf_timescales.png" alt="M7_152125: cumulative mass formed against lookback time with t10 to t90">
<figcaption><code>sf_timescales.png</code> Fraction of the final stellar mass of galaxy M7_152125 formed earlier than each lookback time. The line is the posterior median. The band is the 16-84 percent range over 400 draws. Comparison: points mark t10 to t90 with 16-84 percent (thick) and 2.5-97.5 percent (thin) intervals versus the universe age. t50 is 3.00 Gyr with a 16-84 percent range of 2.95 to 3.05 Gyr. Caveat: the 7-bin star-formation history model quantises these times to the bin edges.</figcaption>
</figure>

### 156118-M8_156118

| z | S/N | photometry χ²/N | spectrum χ²/N | f_calib | t50 [Gyr] | model |
| --- | --- | --- | --- | --- | --- | --- |
| 0.8295 | 11.0 | 2.69 | 1.157 | 5.44% | 2.78 | [parameters](/wiki/f/results/rtx-5060-dr2-quiescent-full-spectrum/156118-M8_156118/diagnostics/model_parameters.txt) |

Flags:

- 4 pixels with |pull| > 4

<figure>
<img loading="lazy" src="/wiki/f/results/rtx-5060-dr2-quiescent-full-spectrum/156118-M8_156118/diagnostics/photometric_chi2.png" alt="M8_156118: photometric pull and chi-squared contribution per band">
<figcaption><code>photometric_chi2.png</code> Pull and chi-squared contribution for the 12 COSMOS2015 bands of galaxy M8_156118. Pull equals observed minus model over sigma. Uncertainty: sigma includes the 5 percent flux floor. Comparison: filled points use the posterior-median model. Open squares use the best sample with the fit's own sigma. Total chi-squared 32.3 over 12 bands gives 2.69 per band. Caveat: the spectrum dominates the joint fit, so the fit does not constrain the bands on their own.</figcaption>
</figure>

<figure>
<img loading="lazy" src="/wiki/f/results/rtx-5060-dr2-quiescent-full-spectrum/156118-M8_156118/diagnostics/spectral_chi2.png" alt="M8_156118: spectral pull, binned mean pull squared, cumulative chi-squared">
<figcaption><code>spectral_chi2.png</code> Pull per fitted pixel of the LEGA-C spectrum of galaxy M8_156118. Below it: mean pull squared in 25 Å bins and the cumulative chi-squared fraction against wavelength. Uncertainty: sigma includes the fitted calibration floor of 5.44 percent of the model flux. Comparison: the stored pull versus the pull at the best sample. Shaded bands mark masked pixels. Red points mark pixels with pull beyond 4 sigma. Total chi-squared 3944.6 over 3409 pixels, 4 outlier pixels. Caveat: the fitted floor absorbs model mismatch, so chi-squared near 1 does not prove a good model.</figcaption>
</figure>

<figure>
<img loading="lazy" src="/wiki/f/results/rtx-5060-dr2-quiescent-full-spectrum/156118-M8_156118/diagnostics/sf_timescales.png" alt="M8_156118: cumulative mass formed against lookback time with t10 to t90">
<figcaption><code>sf_timescales.png</code> Fraction of the final stellar mass of galaxy M8_156118 formed earlier than each lookback time. The line is the posterior median. The band is the 16-84 percent range over 400 draws. Comparison: points mark t10 to t90 with 16-84 percent (thick) and 2.5-97.5 percent (thin) intervals versus the universe age. t50 is 2.78 Gyr with a 16-84 percent range of 2.70 to 2.98 Gyr. Caveat: the 7-bin star-formation history model quantises these times to the bin edges.</figcaption>
</figure>

### 160400-M8_160400

| z | S/N | photometry χ²/N | spectrum χ²/N | f_calib | t50 [Gyr] | model |
| --- | --- | --- | --- | --- | --- | --- |
| 0.6032 | 44.3 | 6.07 | 1.082 | 4.22% | 3.19 | [parameters](/wiki/f/results/rtx-5060-dr2-quiescent-full-spectrum/160400-M8_160400/diagnostics/model_parameters.txt) |

Flags:

- photometry chi2/N 6.1 > 3
- 5 pixels with |pull| > 4

<figure>
<img loading="lazy" src="/wiki/f/results/rtx-5060-dr2-quiescent-full-spectrum/160400-M8_160400/diagnostics/photometric_chi2.png" alt="M8_160400: photometric pull and chi-squared contribution per band">
<figcaption><code>photometric_chi2.png</code> Pull and chi-squared contribution for the 12 COSMOS2015 bands of galaxy M8_160400. Pull equals observed minus model over sigma. Uncertainty: sigma includes the 5 percent flux floor. Comparison: filled points use the posterior-median model. Open squares use the best sample with the fit's own sigma. Total chi-squared 72.8 over 12 bands gives 6.07 per band. Caveat: the spectrum dominates the joint fit, so the fit does not constrain the bands on their own.</figcaption>
</figure>

<figure>
<img loading="lazy" src="/wiki/f/results/rtx-5060-dr2-quiescent-full-spectrum/160400-M8_160400/diagnostics/spectral_chi2.png" alt="M8_160400: spectral pull, binned mean pull squared, cumulative chi-squared">
<figcaption><code>spectral_chi2.png</code> Pull per fitted pixel of the LEGA-C spectrum of galaxy M8_160400. Below it: mean pull squared in 25 Å bins and the cumulative chi-squared fraction against wavelength. Uncertainty: sigma includes the fitted calibration floor of 4.22 percent of the model flux. Comparison: the stored pull versus the pull at the best sample. Shaded bands mark masked pixels. Red points mark pixels with pull beyond 4 sigma. Total chi-squared 3850.4 over 3558 pixels, 5 outlier pixels. Caveat: the fitted floor absorbs model mismatch, so chi-squared near 1 does not prove a good model.</figcaption>
</figure>

<figure>
<img loading="lazy" src="/wiki/f/results/rtx-5060-dr2-quiescent-full-spectrum/160400-M8_160400/diagnostics/sf_timescales.png" alt="M8_160400: cumulative mass formed against lookback time with t10 to t90">
<figcaption><code>sf_timescales.png</code> Fraction of the final stellar mass of galaxy M8_160400 formed earlier than each lookback time. The line is the posterior median. The band is the 16-84 percent range over 400 draws. Comparison: points mark t10 to t90 with 16-84 percent (thick) and 2.5-97.5 percent (thin) intervals versus the universe age. t50 is 3.19 Gyr with a 16-84 percent range of 3.02 to 3.48 Gyr. Caveat: the 7-bin star-formation history model quantises these times to the bin edges.</figcaption>
</figure>

### 161113-M8_161113

| z | S/N | photometry χ²/N | spectrum χ²/N | f_calib | t50 [Gyr] | model |
| --- | --- | --- | --- | --- | --- | --- |
| 0.8911 | 12.6 | 12.55 | 1.087 | 5.28% | 4.63 | [parameters](/wiki/f/results/rtx-5060-dr2-quiescent-full-spectrum/161113-M8_161113/diagnostics/model_parameters.txt) |

Flags:

- photometry chi2/N 12.5 > 3
- 3 pixels with |pull| > 4

<figure>
<img loading="lazy" src="/wiki/f/results/rtx-5060-dr2-quiescent-full-spectrum/161113-M8_161113/diagnostics/photometric_chi2.png" alt="M8_161113: photometric pull and chi-squared contribution per band">
<figcaption><code>photometric_chi2.png</code> Pull and chi-squared contribution for the 12 COSMOS2015 bands of galaxy M8_161113. Pull equals observed minus model over sigma. Uncertainty: sigma includes the 5 percent flux floor. Comparison: filled points use the posterior-median model. Open squares use the best sample with the fit's own sigma. Total chi-squared 150.5 over 12 bands gives 12.55 per band. Caveat: the spectrum dominates the joint fit, so the fit does not constrain the bands on their own.</figcaption>
</figure>

<figure>
<img loading="lazy" src="/wiki/f/results/rtx-5060-dr2-quiescent-full-spectrum/161113-M8_161113/diagnostics/spectral_chi2.png" alt="M8_161113: spectral pull, binned mean pull squared, cumulative chi-squared">
<figcaption><code>spectral_chi2.png</code> Pull per fitted pixel of the LEGA-C spectrum of galaxy M8_161113. Below it: mean pull squared in 25 Å bins and the cumulative chi-squared fraction against wavelength. Uncertainty: sigma includes the fitted calibration floor of 5.28 percent of the model flux. Comparison: the stored pull versus the pull at the best sample. Shaded bands mark masked pixels. Red points mark pixels with pull beyond 4 sigma. Total chi-squared 4128.6 over 3799 pixels, 3 outlier pixels. Caveat: the fitted floor absorbs model mismatch, so chi-squared near 1 does not prove a good model.</figcaption>
</figure>

<figure>
<img loading="lazy" src="/wiki/f/results/rtx-5060-dr2-quiescent-full-spectrum/161113-M8_161113/diagnostics/sf_timescales.png" alt="M8_161113: cumulative mass formed against lookback time with t10 to t90">
<figcaption><code>sf_timescales.png</code> Fraction of the final stellar mass of galaxy M8_161113 formed earlier than each lookback time. The line is the posterior median. The band is the 16-84 percent range over 400 draws. Comparison: points mark t10 to t90 with 16-84 percent (thick) and 2.5-97.5 percent (thin) intervals versus the universe age. t50 is 4.63 Gyr with a 16-84 percent range of 4.48 to 4.68 Gyr. Caveat: the 7-bin star-formation history model quantises these times to the bin edges.</figcaption>
</figure>

### 161346-M8_161346

| z | S/N | photometry χ²/N | spectrum χ²/N | f_calib | t50 [Gyr] | model |
| --- | --- | --- | --- | --- | --- | --- |
| 0.6566 | 40.5 | 3.91 | 1.126 | 4.48% | 4.19 | [parameters](/wiki/f/results/rtx-5060-dr2-quiescent-full-spectrum/161346-M8_161346/diagnostics/model_parameters.txt) |

Flags:

- photometry chi2/N 3.9 > 3
- 6 pixels with |pull| > 4

<figure>
<img loading="lazy" src="/wiki/f/results/rtx-5060-dr2-quiescent-full-spectrum/161346-M8_161346/diagnostics/photometric_chi2.png" alt="M8_161346: photometric pull and chi-squared contribution per band">
<figcaption><code>photometric_chi2.png</code> Pull and chi-squared contribution for the 12 COSMOS2015 bands of galaxy M8_161346. Pull equals observed minus model over sigma. Uncertainty: sigma includes the 5 percent flux floor. Comparison: filled points use the posterior-median model. Open squares use the best sample with the fit's own sigma. Total chi-squared 46.9 over 12 bands gives 3.91 per band. Caveat: the spectrum dominates the joint fit, so the fit does not constrain the bands on their own.</figcaption>
</figure>

<figure>
<img loading="lazy" src="/wiki/f/results/rtx-5060-dr2-quiescent-full-spectrum/161346-M8_161346/diagnostics/spectral_chi2.png" alt="M8_161346: spectral pull, binned mean pull squared, cumulative chi-squared">
<figcaption><code>spectral_chi2.png</code> Pull per fitted pixel of the LEGA-C spectrum of galaxy M8_161346. Below it: mean pull squared in 25 Å bins and the cumulative chi-squared fraction against wavelength. Uncertainty: sigma includes the fitted calibration floor of 4.48 percent of the model flux. Comparison: the stored pull versus the pull at the best sample. Shaded bands mark masked pixels. Red points mark pixels with pull beyond 4 sigma. Total chi-squared 3880.2 over 3447 pixels, 6 outlier pixels. Caveat: the fitted floor absorbs model mismatch, so chi-squared near 1 does not prove a good model.</figcaption>
</figure>

<figure>
<img loading="lazy" src="/wiki/f/results/rtx-5060-dr2-quiescent-full-spectrum/161346-M8_161346/diagnostics/sf_timescales.png" alt="M8_161346: cumulative mass formed against lookback time with t10 to t90">
<figcaption><code>sf_timescales.png</code> Fraction of the final stellar mass of galaxy M8_161346 formed earlier than each lookback time. The line is the posterior median. The band is the 16-84 percent range over 400 draws. Comparison: points mark t10 to t90 with 16-84 percent (thick) and 2.5-97.5 percent (thin) intervals versus the universe age. t50 is 4.19 Gyr with a 16-84 percent range of 3.89 to 4.44 Gyr. Caveat: the 7-bin star-formation history model quantises these times to the bin edges.</figcaption>
</figure>

### 162149-M8_162149

| z | S/N | photometry χ²/N | spectrum χ²/N | f_calib | t50 [Gyr] | model |
| --- | --- | --- | --- | --- | --- | --- |
| 0.7034 | 40.5 | 5.84 | 1.077 | 3.89% | 3.62 | [parameters](/wiki/f/results/rtx-5060-dr2-quiescent-full-spectrum/162149-M8_162149/diagnostics/model_parameters.txt) |

Flags:

- photometry chi2/N 5.8 > 3
- 3 pixels with |pull| > 4

<figure>
<img loading="lazy" src="/wiki/f/results/rtx-5060-dr2-quiescent-full-spectrum/162149-M8_162149/diagnostics/photometric_chi2.png" alt="M8_162149: photometric pull and chi-squared contribution per band">
<figcaption><code>photometric_chi2.png</code> Pull and chi-squared contribution for the 12 COSMOS2015 bands of galaxy M8_162149. Pull equals observed minus model over sigma. Uncertainty: sigma includes the 5 percent flux floor. Comparison: filled points use the posterior-median model. Open squares use the best sample with the fit's own sigma. Total chi-squared 70.0 over 12 bands gives 5.84 per band. Caveat: the spectrum dominates the joint fit, so the fit does not constrain the bands on their own.</figcaption>
</figure>

<figure>
<img loading="lazy" src="/wiki/f/results/rtx-5060-dr2-quiescent-full-spectrum/162149-M8_162149/diagnostics/spectral_chi2.png" alt="M8_162149: spectral pull, binned mean pull squared, cumulative chi-squared">
<figcaption><code>spectral_chi2.png</code> Pull per fitted pixel of the LEGA-C spectrum of galaxy M8_162149. Below it: mean pull squared in 25 Å bins and the cumulative chi-squared fraction against wavelength. Uncertainty: sigma includes the fitted calibration floor of 3.89 percent of the model flux. Comparison: the stored pull versus the pull at the best sample. Shaded bands mark masked pixels. Red points mark pixels with pull beyond 4 sigma. Total chi-squared 3763.5 over 3494 pixels, 3 outlier pixels. Caveat: the fitted floor absorbs model mismatch, so chi-squared near 1 does not prove a good model.</figcaption>
</figure>

<figure>
<img loading="lazy" src="/wiki/f/results/rtx-5060-dr2-quiescent-full-spectrum/162149-M8_162149/diagnostics/sf_timescales.png" alt="M8_162149: cumulative mass formed against lookback time with t10 to t90">
<figcaption><code>sf_timescales.png</code> Fraction of the final stellar mass of galaxy M8_162149 formed earlier than each lookback time. The line is the posterior median. The band is the 16-84 percent range over 400 draws. Comparison: points mark t10 to t90 with 16-84 percent (thick) and 2.5-97.5 percent (thin) intervals versus the universe age. t50 is 3.62 Gyr with a 16-84 percent range of 3.33 to 3.89 Gyr. Caveat: the 7-bin star-formation history model quantises these times to the bin edges.</figcaption>
</figure>

### 162587-M7_162587

| z | S/N | photometry χ²/N | spectrum χ²/N | f_calib | t50 [Gyr] | model |
| --- | --- | --- | --- | --- | --- | --- |
| 0.7869 | 12.6 | 6.68 | 1.263 | 9.86% | 2.05 | [parameters](/wiki/f/results/rtx-5060-dr2-quiescent-full-spectrum/162587-M7_162587/diagnostics/model_parameters.txt) |

Flags:

- photometry chi2/N 6.7 > 3
- calibration floor at prior bound (9.9% of 10%)
- 15 pixels with |pull| > 4

<figure>
<img loading="lazy" src="/wiki/f/results/rtx-5060-dr2-quiescent-full-spectrum/162587-M7_162587/diagnostics/photometric_chi2.png" alt="M7_162587: photometric pull and chi-squared contribution per band">
<figcaption><code>photometric_chi2.png</code> Pull and chi-squared contribution for the 12 COSMOS2015 bands of galaxy M7_162587. Pull equals observed minus model over sigma. Uncertainty: sigma includes the 5 percent flux floor. Comparison: filled points use the posterior-median model. Open squares use the best sample with the fit's own sigma. Total chi-squared 80.1 over 12 bands gives 6.68 per band. Caveat: the spectrum dominates the joint fit, so the fit does not constrain the bands on their own.</figcaption>
</figure>

<figure>
<img loading="lazy" src="/wiki/f/results/rtx-5060-dr2-quiescent-full-spectrum/162587-M7_162587/diagnostics/spectral_chi2.png" alt="M7_162587: spectral pull, binned mean pull squared, cumulative chi-squared">
<figcaption><code>spectral_chi2.png</code> Pull per fitted pixel of the LEGA-C spectrum of galaxy M7_162587. Below it: mean pull squared in 25 Å bins and the cumulative chi-squared fraction against wavelength. Uncertainty: sigma includes the fitted calibration floor of 9.86 percent of the model flux. Comparison: the stored pull versus the pull at the best sample. Shaded bands mark masked pixels. Red points mark pixels with pull beyond 4 sigma. Total chi-squared 4477.6 over 3544 pixels, 15 outlier pixels. Caveat: the fitted floor absorbs model mismatch, so chi-squared near 1 does not prove a good model.</figcaption>
</figure>

<figure>
<img loading="lazy" src="/wiki/f/results/rtx-5060-dr2-quiescent-full-spectrum/162587-M7_162587/diagnostics/sf_timescales.png" alt="M7_162587: cumulative mass formed against lookback time with t10 to t90">
<figcaption><code>sf_timescales.png</code> Fraction of the final stellar mass of galaxy M7_162587 formed earlier than each lookback time. The line is the posterior median. The band is the 16-84 percent range over 400 draws. Comparison: points mark t10 to t90 with 16-84 percent (thick) and 2.5-97.5 percent (thin) intervals versus the universe age. t50 is 2.05 Gyr with a 16-84 percent range of 1.70 to 2.24 Gyr. Caveat: the 7-bin star-formation history model quantises these times to the bin edges.</figcaption>
</figure>

### 163989-M8_163989

| z | S/N | photometry χ²/N | spectrum χ²/N | f_calib | t50 [Gyr] | model |
| --- | --- | --- | --- | --- | --- | --- |
| 0.7583 | 19.0 | 3.13 | 1.092 | 5.28% | 3.00 | [parameters](/wiki/f/results/rtx-5060-dr2-quiescent-full-spectrum/163989-M8_163989/diagnostics/model_parameters.txt) |

Flags:

- photometry chi2/N 3.1 > 3
- 3 pixels with |pull| > 4

<figure>
<img loading="lazy" src="/wiki/f/results/rtx-5060-dr2-quiescent-full-spectrum/163989-M8_163989/diagnostics/photometric_chi2.png" alt="M8_163989: photometric pull and chi-squared contribution per band">
<figcaption><code>photometric_chi2.png</code> Pull and chi-squared contribution for the 12 COSMOS2015 bands of galaxy M8_163989. Pull equals observed minus model over sigma. Uncertainty: sigma includes the 5 percent flux floor. Comparison: filled points use the posterior-median model. Open squares use the best sample with the fit's own sigma. Total chi-squared 37.6 over 12 bands gives 3.13 per band. Caveat: the spectrum dominates the joint fit, so the fit does not constrain the bands on their own.</figcaption>
</figure>

<figure>
<img loading="lazy" src="/wiki/f/results/rtx-5060-dr2-quiescent-full-spectrum/163989-M8_163989/diagnostics/spectral_chi2.png" alt="M8_163989: spectral pull, binned mean pull squared, cumulative chi-squared">
<figcaption><code>spectral_chi2.png</code> Pull per fitted pixel of the LEGA-C spectrum of galaxy M8_163989. Below it: mean pull squared in 25 Å bins and the cumulative chi-squared fraction against wavelength. Uncertainty: sigma includes the fitted calibration floor of 5.28 percent of the model flux. Comparison: the stored pull versus the pull at the best sample. Shaded bands mark masked pixels. Red points mark pixels with pull beyond 4 sigma. Total chi-squared 3951.8 over 3618 pixels, 3 outlier pixels. Caveat: the fitted floor absorbs model mismatch, so chi-squared near 1 does not prove a good model.</figcaption>
</figure>

<figure>
<img loading="lazy" src="/wiki/f/results/rtx-5060-dr2-quiescent-full-spectrum/163989-M8_163989/diagnostics/sf_timescales.png" alt="M8_163989: cumulative mass formed against lookback time with t10 to t90">
<figcaption><code>sf_timescales.png</code> Fraction of the final stellar mass of galaxy M8_163989 formed earlier than each lookback time. The line is the posterior median. The band is the 16-84 percent range over 400 draws. Comparison: points mark t10 to t90 with 16-84 percent (thick) and 2.5-97.5 percent (thin) intervals versus the universe age. t50 is 3.00 Gyr with a 16-84 percent range of 2.99 to 3.04 Gyr. Caveat: the 7-bin star-formation history model quantises these times to the bin edges.</figcaption>
</figure>

### 165871-M5_165871

| z | S/N | photometry χ²/N | spectrum χ²/N | f_calib | t50 [Gyr] | model |
| --- | --- | --- | --- | --- | --- | --- |
| 0.7031 | 25.0 | 4.76 | 1.099 | 4.43% | 2.74 | [parameters](/wiki/f/results/rtx-5060-dr2-quiescent-full-spectrum/165871-M5_165871/diagnostics/model_parameters.txt) |

Flags:

- photometry chi2/N 4.8 > 3
- 8 pixels with |pull| > 4

<figure>
<img loading="lazy" src="/wiki/f/results/rtx-5060-dr2-quiescent-full-spectrum/165871-M5_165871/diagnostics/photometric_chi2.png" alt="M5_165871: photometric pull and chi-squared contribution per band">
<figcaption><code>photometric_chi2.png</code> Pull and chi-squared contribution for the 12 COSMOS2015 bands of galaxy M5_165871. Pull equals observed minus model over sigma. Uncertainty: sigma includes the 5 percent flux floor. Comparison: filled points use the posterior-median model. Open squares use the best sample with the fit's own sigma. Total chi-squared 57.1 over 12 bands gives 4.76 per band. Caveat: the spectrum dominates the joint fit, so the fit does not constrain the bands on their own.</figcaption>
</figure>

<figure>
<img loading="lazy" src="/wiki/f/results/rtx-5060-dr2-quiescent-full-spectrum/165871-M5_165871/diagnostics/spectral_chi2.png" alt="M5_165871: spectral pull, binned mean pull squared, cumulative chi-squared">
<figcaption><code>spectral_chi2.png</code> Pull per fitted pixel of the LEGA-C spectrum of galaxy M5_165871. Below it: mean pull squared in 25 Å bins and the cumulative chi-squared fraction against wavelength. Uncertainty: sigma includes the fitted calibration floor of 4.43 percent of the model flux. Comparison: the stored pull versus the pull at the best sample. Shaded bands mark masked pixels. Red points mark pixels with pull beyond 4 sigma. Total chi-squared 3802.3 over 3460 pixels, 8 outlier pixels. Caveat: the fitted floor absorbs model mismatch, so chi-squared near 1 does not prove a good model.</figcaption>
</figure>

<figure>
<img loading="lazy" src="/wiki/f/results/rtx-5060-dr2-quiescent-full-spectrum/165871-M5_165871/diagnostics/sf_timescales.png" alt="M5_165871: cumulative mass formed against lookback time with t10 to t90">
<figcaption><code>sf_timescales.png</code> Fraction of the final stellar mass of galaxy M5_165871 formed earlier than each lookback time. The line is the posterior median. The band is the 16-84 percent range over 400 draws. Comparison: points mark t10 to t90 with 16-84 percent (thick) and 2.5-97.5 percent (thin) intervals versus the universe age. t50 is 2.74 Gyr with a 16-84 percent range of 2.70 to 2.79 Gyr. Caveat: the 7-bin star-formation history model quantises these times to the bin edges.</figcaption>
</figure>

### 166634-M6_166634

| z | S/N | photometry χ²/N | spectrum χ²/N | f_calib | t50 [Gyr] | model |
| --- | --- | --- | --- | --- | --- | --- |
| 0.8527 | 7.3 | 9.27 | 1.125 | 9.35% | 5.74 | [parameters](/wiki/f/results/rtx-5060-dr2-quiescent-full-spectrum/166634-M6_166634/diagnostics/model_parameters.txt) |

Flags:

- photometry chi2/N 9.3 > 3
- 3 pixels with |pull| > 4

<figure>
<img loading="lazy" src="/wiki/f/results/rtx-5060-dr2-quiescent-full-spectrum/166634-M6_166634/diagnostics/photometric_chi2.png" alt="M6_166634: photometric pull and chi-squared contribution per band">
<figcaption><code>photometric_chi2.png</code> Pull and chi-squared contribution for the 12 COSMOS2015 bands of galaxy M6_166634. Pull equals observed minus model over sigma. Uncertainty: sigma includes the 5 percent flux floor. Comparison: filled points use the posterior-median model. Open squares use the best sample with the fit's own sigma. Total chi-squared 111.2 over 12 bands gives 9.27 per band. Caveat: the spectrum dominates the joint fit, so the fit does not constrain the bands on their own.</figcaption>
</figure>

<figure>
<img loading="lazy" src="/wiki/f/results/rtx-5060-dr2-quiescent-full-spectrum/166634-M6_166634/diagnostics/spectral_chi2.png" alt="M6_166634: spectral pull, binned mean pull squared, cumulative chi-squared">
<figcaption><code>spectral_chi2.png</code> Pull per fitted pixel of the LEGA-C spectrum of galaxy M6_166634. Below it: mean pull squared in 25 Å bins and the cumulative chi-squared fraction against wavelength. Uncertainty: sigma includes the fitted calibration floor of 9.35 percent of the model flux. Comparison: the stored pull versus the pull at the best sample. Shaded bands mark masked pixels. Red points mark pixels with pull beyond 4 sigma. Total chi-squared 3956.8 over 3518 pixels, 3 outlier pixels. Caveat: the fitted floor absorbs model mismatch, so chi-squared near 1 does not prove a good model.</figcaption>
</figure>

<figure>
<img loading="lazy" src="/wiki/f/results/rtx-5060-dr2-quiescent-full-spectrum/166634-M6_166634/diagnostics/sf_timescales.png" alt="M6_166634: cumulative mass formed against lookback time with t10 to t90">
<figcaption><code>sf_timescales.png</code> Fraction of the final stellar mass of galaxy M6_166634 formed earlier than each lookback time. The line is the posterior median. The band is the 16-84 percent range over 400 draws. Comparison: points mark t10 to t90 with 16-84 percent (thick) and 2.5-97.5 percent (thin) intervals versus the universe age. t50 is 5.74 Gyr with a 16-84 percent range of 5.73 to 5.75 Gyr. Caveat: the 7-bin star-formation history model quantises these times to the bin edges.</figcaption>
</figure>

### 167056-M5_167056

| z | S/N | photometry χ²/N | spectrum χ²/N | f_calib | t50 [Gyr] | model |
| --- | --- | --- | --- | --- | --- | --- |
| 0.8933 | 8.1 | 4.04 | 1.071 | 5.15% | 4.55 | [parameters](/wiki/f/results/rtx-5060-dr2-quiescent-full-spectrum/167056-M5_167056/diagnostics/model_parameters.txt) |

Flags:

- photometry chi2/N 4.0 > 3
- 1 pixels with |pull| > 4

<figure>
<img loading="lazy" src="/wiki/f/results/rtx-5060-dr2-quiescent-full-spectrum/167056-M5_167056/diagnostics/photometric_chi2.png" alt="M5_167056: photometric pull and chi-squared contribution per band">
<figcaption><code>photometric_chi2.png</code> Pull and chi-squared contribution for the 12 COSMOS2015 bands of galaxy M5_167056. Pull equals observed minus model over sigma. Uncertainty: sigma includes the 5 percent flux floor. Comparison: filled points use the posterior-median model. Open squares use the best sample with the fit's own sigma. Total chi-squared 48.5 over 12 bands gives 4.04 per band. Caveat: the spectrum dominates the joint fit, so the fit does not constrain the bands on their own.</figcaption>
</figure>

<figure>
<img loading="lazy" src="/wiki/f/results/rtx-5060-dr2-quiescent-full-spectrum/167056-M5_167056/diagnostics/spectral_chi2.png" alt="M5_167056: spectral pull, binned mean pull squared, cumulative chi-squared">
<figcaption><code>spectral_chi2.png</code> Pull per fitted pixel of the LEGA-C spectrum of galaxy M5_167056. Below it: mean pull squared in 25 Å bins and the cumulative chi-squared fraction against wavelength. Uncertainty: sigma includes the fitted calibration floor of 5.15 percent of the model flux. Comparison: the stored pull versus the pull at the best sample. Shaded bands mark masked pixels. Red points mark pixels with pull beyond 4 sigma. Total chi-squared 4063.7 over 3796 pixels, 1 outlier pixels. Caveat: the fitted floor absorbs model mismatch, so chi-squared near 1 does not prove a good model.</figcaption>
</figure>

<figure>
<img loading="lazy" src="/wiki/f/results/rtx-5060-dr2-quiescent-full-spectrum/167056-M5_167056/diagnostics/sf_timescales.png" alt="M5_167056: cumulative mass formed against lookback time with t10 to t90">
<figcaption><code>sf_timescales.png</code> Fraction of the final stellar mass of galaxy M5_167056 formed earlier than each lookback time. The line is the posterior median. The band is the 16-84 percent range over 400 draws. Comparison: points mark t10 to t90 with 16-84 percent (thick) and 2.5-97.5 percent (thin) intervals versus the universe age. t50 is 4.55 Gyr with a 16-84 percent range of 4.29 to 4.65 Gyr. Caveat: the 7-bin star-formation history model quantises these times to the bin edges.</figcaption>
</figure>

### 172669-M5_172669

| z | S/N | photometry χ²/N | spectrum χ²/N | f_calib | t50 [Gyr] | model |
| --- | --- | --- | --- | --- | --- | --- |
| 0.6037 | 105.0 | 14.14 | 1.062 | 2.90% | 1.66 | [parameters](/wiki/f/results/rtx-5060-dr2-quiescent-full-spectrum/172669-M5_172669/diagnostics/model_parameters.txt) |

Flags:

- photometry chi2/N 14.1 > 3
- 29 pixels with |pull| > 4

<figure>
<img loading="lazy" src="/wiki/f/results/rtx-5060-dr2-quiescent-full-spectrum/172669-M5_172669/diagnostics/photometric_chi2.png" alt="M5_172669: photometric pull and chi-squared contribution per band">
<figcaption><code>photometric_chi2.png</code> Pull and chi-squared contribution for the 12 COSMOS2015 bands of galaxy M5_172669. Pull equals observed minus model over sigma. Uncertainty: sigma includes the 5 percent flux floor. Comparison: filled points use the posterior-median model. Open squares use the best sample with the fit's own sigma. Total chi-squared 169.6 over 12 bands gives 14.14 per band. Caveat: the spectrum dominates the joint fit, so the fit does not constrain the bands on their own.</figcaption>
</figure>

<figure>
<img loading="lazy" src="/wiki/f/results/rtx-5060-dr2-quiescent-full-spectrum/172669-M5_172669/diagnostics/spectral_chi2.png" alt="M5_172669: spectral pull, binned mean pull squared, cumulative chi-squared">
<figcaption><code>spectral_chi2.png</code> Pull per fitted pixel of the LEGA-C spectrum of galaxy M5_172669. Below it: mean pull squared in 25 Å bins and the cumulative chi-squared fraction against wavelength. Uncertainty: sigma includes the fitted calibration floor of 2.90 percent of the model flux. Comparison: the stored pull versus the pull at the best sample. Shaded bands mark masked pixels. Red points mark pixels with pull beyond 4 sigma. Total chi-squared 3825.9 over 3602 pixels, 29 outlier pixels. Caveat: the fitted floor absorbs model mismatch, so chi-squared near 1 does not prove a good model.</figcaption>
</figure>

<figure>
<img loading="lazy" src="/wiki/f/results/rtx-5060-dr2-quiescent-full-spectrum/172669-M5_172669/diagnostics/sf_timescales.png" alt="M5_172669: cumulative mass formed against lookback time with t10 to t90">
<figcaption><code>sf_timescales.png</code> Fraction of the final stellar mass of galaxy M5_172669 formed earlier than each lookback time. The line is the posterior median. The band is the 16-84 percent range over 400 draws. Comparison: points mark t10 to t90 with 16-84 percent (thick) and 2.5-97.5 percent (thin) intervals versus the universe age. t50 is 1.66 Gyr with a 16-84 percent range of 1.65 to 1.67 Gyr. Caveat: the 7-bin star-formation history model quantises these times to the bin edges.</figcaption>
</figure>

### 173928-M5_173928

| z | S/N | photometry χ²/N | spectrum χ²/N | f_calib | t50 [Gyr] | model |
| --- | --- | --- | --- | --- | --- | --- |
| 0.9590 | 13.3 | 12.07 | 0.946 | 9.17% | 2.92 | [parameters](/wiki/f/results/rtx-5060-dr2-quiescent-full-spectrum/173928-M5_173928/diagnostics/model_parameters.txt) |

Flags:

- photometry chi2/N 12.1 > 3
- 23 pixels with |pull| > 4

<figure>
<img loading="lazy" src="/wiki/f/results/rtx-5060-dr2-quiescent-full-spectrum/173928-M5_173928/diagnostics/photometric_chi2.png" alt="M5_173928: photometric pull and chi-squared contribution per band">
<figcaption><code>photometric_chi2.png</code> Pull and chi-squared contribution for the 12 COSMOS2015 bands of galaxy M5_173928. Pull equals observed minus model over sigma. Uncertainty: sigma includes the 5 percent flux floor. Comparison: filled points use the posterior-median model. Open squares use the best sample with the fit's own sigma. Total chi-squared 144.8 over 12 bands gives 12.07 per band. Caveat: the spectrum dominates the joint fit, so the fit does not constrain the bands on their own.</figcaption>
</figure>

<figure>
<img loading="lazy" src="/wiki/f/results/rtx-5060-dr2-quiescent-full-spectrum/173928-M5_173928/diagnostics/spectral_chi2.png" alt="M5_173928: spectral pull, binned mean pull squared, cumulative chi-squared">
<figcaption><code>spectral_chi2.png</code> Pull per fitted pixel of the LEGA-C spectrum of galaxy M5_173928. Below it: mean pull squared in 25 Å bins and the cumulative chi-squared fraction against wavelength. Uncertainty: sigma includes the fitted calibration floor of 9.17 percent of the model flux. Comparison: the stored pull versus the pull at the best sample. Shaded bands mark masked pixels. Red points mark pixels with pull beyond 4 sigma. Total chi-squared 3629.2 over 3836 pixels, 23 outlier pixels. Caveat: the fitted floor absorbs model mismatch, so chi-squared near 1 does not prove a good model.</figcaption>
</figure>

<figure>
<img loading="lazy" src="/wiki/f/results/rtx-5060-dr2-quiescent-full-spectrum/173928-M5_173928/diagnostics/sf_timescales.png" alt="M5_173928: cumulative mass formed against lookback time with t10 to t90">
<figcaption><code>sf_timescales.png</code> Fraction of the final stellar mass of galaxy M5_173928 formed earlier than each lookback time. The line is the posterior median. The band is the 16-84 percent range over 400 draws. Comparison: points mark t10 to t90 with 16-84 percent (thick) and 2.5-97.5 percent (thin) intervals versus the universe age. t50 is 2.92 Gyr with a 16-84 percent range of 2.87 to 2.99 Gyr. Caveat: the 7-bin star-formation history model quantises these times to the bin edges.</figcaption>
</figure>

### 180774-M12_180774

| z | S/N | photometry χ²/N | spectrum χ²/N | f_calib | t50 [Gyr] | model |
| --- | --- | --- | --- | --- | --- | --- |
| 0.6782 | 22.2 | 3.50 | 1.202 | 7.39% | 4.05 | [parameters](/wiki/f/results/rtx-5060-dr2-quiescent-full-spectrum/180774-M12_180774/diagnostics/model_parameters.txt) |

Flags:

- photometry chi2/N 3.5 > 3
- 9 pixels with |pull| > 4

<figure>
<img loading="lazy" src="/wiki/f/results/rtx-5060-dr2-quiescent-full-spectrum/180774-M12_180774/diagnostics/photometric_chi2.png" alt="M12_180774: photometric pull and chi-squared contribution per band">
<figcaption><code>photometric_chi2.png</code> Pull and chi-squared contribution for the 12 COSMOS2015 bands of galaxy M12_180774. Pull equals observed minus model over sigma. Uncertainty: sigma includes the 5 percent flux floor. Comparison: filled points use the posterior-median model. Open squares use the best sample with the fit's own sigma. Total chi-squared 42.0 over 12 bands gives 3.50 per band. Caveat: the spectrum dominates the joint fit, so the fit does not constrain the bands on their own.</figcaption>
</figure>

<figure>
<img loading="lazy" src="/wiki/f/results/rtx-5060-dr2-quiescent-full-spectrum/180774-M12_180774/diagnostics/spectral_chi2.png" alt="M12_180774: spectral pull, binned mean pull squared, cumulative chi-squared">
<figcaption><code>spectral_chi2.png</code> Pull per fitted pixel of the LEGA-C spectrum of galaxy M12_180774. Below it: mean pull squared in 25 Å bins and the cumulative chi-squared fraction against wavelength. Uncertainty: sigma includes the fitted calibration floor of 7.39 percent of the model flux. Comparison: the stored pull versus the pull at the best sample. Shaded bands mark masked pixels. Red points mark pixels with pull beyond 4 sigma. Total chi-squared 4068.8 over 3384 pixels, 9 outlier pixels. Caveat: the fitted floor absorbs model mismatch, so chi-squared near 1 does not prove a good model.</figcaption>
</figure>

<figure>
<img loading="lazy" src="/wiki/f/results/rtx-5060-dr2-quiescent-full-spectrum/180774-M12_180774/diagnostics/sf_timescales.png" alt="M12_180774: cumulative mass formed against lookback time with t10 to t90">
<figcaption><code>sf_timescales.png</code> Fraction of the final stellar mass of galaxy M12_180774 formed earlier than each lookback time. The line is the posterior median. The band is the 16-84 percent range over 400 draws. Comparison: points mark t10 to t90 with 16-84 percent (thick) and 2.5-97.5 percent (thin) intervals versus the universe age. t50 is 4.05 Gyr with a 16-84 percent range of 3.07 to 4.75 Gyr. Caveat: the 7-bin star-formation history model quantises these times to the bin edges.</figcaption>
</figure>

### 181421-M12_181421

| z | S/N | photometry χ²/N | spectrum χ²/N | f_calib | t50 [Gyr] | model |
| --- | --- | --- | --- | --- | --- | --- |
| 0.9585 | 11.3 | 4.03 | 1.158 | 9.38% | 3.96 | [parameters](/wiki/f/results/rtx-5060-dr2-quiescent-full-spectrum/181421-M12_181421/diagnostics/model_parameters.txt) |

Flags:

- photometry chi2/N 4.0 > 3
- 4 pixels with |pull| > 4

<figure>
<img loading="lazy" src="/wiki/f/results/rtx-5060-dr2-quiescent-full-spectrum/181421-M12_181421/diagnostics/photometric_chi2.png" alt="M12_181421: photometric pull and chi-squared contribution per band">
<figcaption><code>photometric_chi2.png</code> Pull and chi-squared contribution for the 12 COSMOS2015 bands of galaxy M12_181421. Pull equals observed minus model over sigma. Uncertainty: sigma includes the 5 percent flux floor. Comparison: filled points use the posterior-median model. Open squares use the best sample with the fit's own sigma. Total chi-squared 48.4 over 12 bands gives 4.03 per band. Caveat: the spectrum dominates the joint fit, so the fit does not constrain the bands on their own.</figcaption>
</figure>

<figure>
<img loading="lazy" src="/wiki/f/results/rtx-5060-dr2-quiescent-full-spectrum/181421-M12_181421/diagnostics/spectral_chi2.png" alt="M12_181421: spectral pull, binned mean pull squared, cumulative chi-squared">
<figcaption><code>spectral_chi2.png</code> Pull per fitted pixel of the LEGA-C spectrum of galaxy M12_181421. Below it: mean pull squared in 25 Å bins and the cumulative chi-squared fraction against wavelength. Uncertainty: sigma includes the fitted calibration floor of 9.38 percent of the model flux. Comparison: the stored pull versus the pull at the best sample. Shaded bands mark masked pixels. Red points mark pixels with pull beyond 4 sigma. Total chi-squared 4400.8 over 3800 pixels, 4 outlier pixels. Caveat: the fitted floor absorbs model mismatch, so chi-squared near 1 does not prove a good model.</figcaption>
</figure>

<figure>
<img loading="lazy" src="/wiki/f/results/rtx-5060-dr2-quiescent-full-spectrum/181421-M12_181421/diagnostics/sf_timescales.png" alt="M12_181421: cumulative mass formed against lookback time with t10 to t90">
<figcaption><code>sf_timescales.png</code> Fraction of the final stellar mass of galaxy M12_181421 formed earlier than each lookback time. The line is the posterior median. The band is the 16-84 percent range over 400 draws. Comparison: points mark t10 to t90 with 16-84 percent (thick) and 2.5-97.5 percent (thin) intervals versus the universe age. t50 is 3.96 Gyr with a 16-84 percent range of 3.37 to 4.24 Gyr. Caveat: the 7-bin star-formation history model quantises these times to the bin edges.</figcaption>
</figure>

### 181945-M12_181945

| z | S/N | photometry χ²/N | spectrum χ²/N | f_calib | t50 [Gyr] | model |
| --- | --- | --- | --- | --- | --- | --- |
| 0.6795 | 61.8 | 13.06 | 1.089 | 4.24% | 2.69 | [parameters](/wiki/f/results/rtx-5060-dr2-quiescent-full-spectrum/181945-M12_181945/diagnostics/model_parameters.txt) |

Flags:

- photometry chi2/N 13.1 > 3
- 9 pixels with |pull| > 4

<figure>
<img loading="lazy" src="/wiki/f/results/rtx-5060-dr2-quiescent-full-spectrum/181945-M12_181945/diagnostics/photometric_chi2.png" alt="M12_181945: photometric pull and chi-squared contribution per band">
<figcaption><code>photometric_chi2.png</code> Pull and chi-squared contribution for the 12 COSMOS2015 bands of galaxy M12_181945. Pull equals observed minus model over sigma. Uncertainty: sigma includes the 5 percent flux floor. Comparison: filled points use the posterior-median model. Open squares use the best sample with the fit's own sigma. Total chi-squared 156.7 over 12 bands gives 13.06 per band. Caveat: the spectrum dominates the joint fit, so the fit does not constrain the bands on their own.</figcaption>
</figure>

<figure>
<img loading="lazy" src="/wiki/f/results/rtx-5060-dr2-quiescent-full-spectrum/181945-M12_181945/diagnostics/spectral_chi2.png" alt="M12_181945: spectral pull, binned mean pull squared, cumulative chi-squared">
<figcaption><code>spectral_chi2.png</code> Pull per fitted pixel of the LEGA-C spectrum of galaxy M12_181945. Below it: mean pull squared in 25 Å bins and the cumulative chi-squared fraction against wavelength. Uncertainty: sigma includes the fitted calibration floor of 4.24 percent of the model flux. Comparison: the stored pull versus the pull at the best sample. Shaded bands mark masked pixels. Red points mark pixels with pull beyond 4 sigma. Total chi-squared 3735.8 over 3432 pixels, 9 outlier pixels. Caveat: the fitted floor absorbs model mismatch, so chi-squared near 1 does not prove a good model.</figcaption>
</figure>

<figure>
<img loading="lazy" src="/wiki/f/results/rtx-5060-dr2-quiescent-full-spectrum/181945-M12_181945/diagnostics/sf_timescales.png" alt="M12_181945: cumulative mass formed against lookback time with t10 to t90">
<figcaption><code>sf_timescales.png</code> Fraction of the final stellar mass of galaxy M12_181945 formed earlier than each lookback time. The line is the posterior median. The band is the 16-84 percent range over 400 draws. Comparison: points mark t10 to t90 with 16-84 percent (thick) and 2.5-97.5 percent (thin) intervals versus the universe age. t50 is 2.69 Gyr with a 16-84 percent range of 2.66 to 2.71 Gyr. Caveat: the 7-bin star-formation history model quantises these times to the bin edges.</figcaption>
</figure>

### 182890-M12_182890

| z | S/N | photometry χ²/N | spectrum χ²/N | f_calib | t50 [Gyr] | model |
| --- | --- | --- | --- | --- | --- | --- |
| 0.7444 | 16.8 | 9.89 | 1.188 | 6.02% | 3.90 | [parameters](/wiki/f/results/rtx-5060-dr2-quiescent-full-spectrum/182890-M12_182890/diagnostics/model_parameters.txt) |

Flags:

- photometry chi2/N 9.9 > 3
- 4 pixels with |pull| > 4

<figure>
<img loading="lazy" src="/wiki/f/results/rtx-5060-dr2-quiescent-full-spectrum/182890-M12_182890/diagnostics/photometric_chi2.png" alt="M12_182890: photometric pull and chi-squared contribution per band">
<figcaption><code>photometric_chi2.png</code> Pull and chi-squared contribution for the 12 COSMOS2015 bands of galaxy M12_182890. Pull equals observed minus model over sigma. Uncertainty: sigma includes the 5 percent flux floor. Comparison: filled points use the posterior-median model. Open squares use the best sample with the fit's own sigma. Total chi-squared 118.7 over 12 bands gives 9.89 per band. Caveat: the spectrum dominates the joint fit, so the fit does not constrain the bands on their own.</figcaption>
</figure>

<figure>
<img loading="lazy" src="/wiki/f/results/rtx-5060-dr2-quiescent-full-spectrum/182890-M12_182890/diagnostics/spectral_chi2.png" alt="M12_182890: spectral pull, binned mean pull squared, cumulative chi-squared">
<figcaption><code>spectral_chi2.png</code> Pull per fitted pixel of the LEGA-C spectrum of galaxy M12_182890. Below it: mean pull squared in 25 Å bins and the cumulative chi-squared fraction against wavelength. Uncertainty: sigma includes the fitted calibration floor of 6.02 percent of the model flux. Comparison: the stored pull versus the pull at the best sample. Shaded bands mark masked pixels. Red points mark pixels with pull beyond 4 sigma. Total chi-squared 4239.8 over 3569 pixels, 4 outlier pixels. Caveat: the fitted floor absorbs model mismatch, so chi-squared near 1 does not prove a good model.</figcaption>
</figure>

<figure>
<img loading="lazy" src="/wiki/f/results/rtx-5060-dr2-quiescent-full-spectrum/182890-M12_182890/diagnostics/sf_timescales.png" alt="M12_182890: cumulative mass formed against lookback time with t10 to t90">
<figcaption><code>sf_timescales.png</code> Fraction of the final stellar mass of galaxy M12_182890 formed earlier than each lookback time. The line is the posterior median. The band is the 16-84 percent range over 400 draws. Comparison: points mark t10 to t90 with 16-84 percent (thick) and 2.5-97.5 percent (thin) intervals versus the universe age. t50 is 3.90 Gyr with a 16-84 percent range of 3.50 to 4.44 Gyr. Caveat: the 7-bin star-formation history model quantises these times to the bin edges.</figcaption>
</figure>

### 184916-M12_184916

| z | S/N | photometry χ²/N | spectrum χ²/N | f_calib | t50 [Gyr] | model |
| --- | --- | --- | --- | --- | --- | --- |
| 0.6794 | 30.4 | 6.59 | 1.066 | 9.59% | 6.15 | [parameters](/wiki/f/results/rtx-5060-dr2-quiescent-full-spectrum/184916-M12_184916/diagnostics/model_parameters.txt) |

Flags:

- photometry chi2/N 6.6 > 3
- 41 pixels with |pull| > 4

<figure>
<img loading="lazy" src="/wiki/f/results/rtx-5060-dr2-quiescent-full-spectrum/184916-M12_184916/diagnostics/photometric_chi2.png" alt="M12_184916: photometric pull and chi-squared contribution per band">
<figcaption><code>photometric_chi2.png</code> Pull and chi-squared contribution for the 12 COSMOS2015 bands of galaxy M12_184916. Pull equals observed minus model over sigma. Uncertainty: sigma includes the 5 percent flux floor. Comparison: filled points use the posterior-median model. Open squares use the best sample with the fit's own sigma. Total chi-squared 79.0 over 12 bands gives 6.59 per band. Caveat: the spectrum dominates the joint fit, so the fit does not constrain the bands on their own.</figcaption>
</figure>

<figure>
<img loading="lazy" src="/wiki/f/results/rtx-5060-dr2-quiescent-full-spectrum/184916-M12_184916/diagnostics/spectral_chi2.png" alt="M12_184916: spectral pull, binned mean pull squared, cumulative chi-squared">
<figcaption><code>spectral_chi2.png</code> Pull per fitted pixel of the LEGA-C spectrum of galaxy M12_184916. Below it: mean pull squared in 25 Å bins and the cumulative chi-squared fraction against wavelength. Uncertainty: sigma includes the fitted calibration floor of 9.59 percent of the model flux. Comparison: the stored pull versus the pull at the best sample. Shaded bands mark masked pixels. Red points mark pixels with pull beyond 4 sigma. Total chi-squared 3820.7 over 3583 pixels, 41 outlier pixels. Caveat: the fitted floor absorbs model mismatch, so chi-squared near 1 does not prove a good model.</figcaption>
</figure>

<figure>
<img loading="lazy" src="/wiki/f/results/rtx-5060-dr2-quiescent-full-spectrum/184916-M12_184916/diagnostics/sf_timescales.png" alt="M12_184916: cumulative mass formed against lookback time with t10 to t90">
<figcaption><code>sf_timescales.png</code> Fraction of the final stellar mass of galaxy M12_184916 formed earlier than each lookback time. The line is the posterior median. The band is the 16-84 percent range over 400 draws. Comparison: points mark t10 to t90 with 16-84 percent (thick) and 2.5-97.5 percent (thin) intervals versus the universe age. t50 is 6.15 Gyr with a 16-84 percent range of 6.04 to 6.18 Gyr. Caveat: the 7-bin star-formation history model quantises these times to the bin edges.</figcaption>
</figure>

### 185631-M12_185631

| z | S/N | photometry χ²/N | spectrum χ²/N | f_calib | t50 [Gyr] | model |
| --- | --- | --- | --- | --- | --- | --- |
| 0.9253 | 4.9 | 1.99 | 1.804 | 9.99% | 2.76 | [parameters](/wiki/f/results/rtx-5060-dr2-quiescent-full-spectrum/185631-M12_185631/diagnostics/model_parameters.txt) |

Flags:

- spectrum chi2/N 1.80 > 1.5
- calibration floor at prior bound (10.0% of 10%)
- 13 pixels with |pull| > 4

<figure>
<img loading="lazy" src="/wiki/f/results/rtx-5060-dr2-quiescent-full-spectrum/185631-M12_185631/diagnostics/photometric_chi2.png" alt="M12_185631: photometric pull and chi-squared contribution per band">
<figcaption><code>photometric_chi2.png</code> Pull and chi-squared contribution for the 12 COSMOS2015 bands of galaxy M12_185631. Pull equals observed minus model over sigma. Uncertainty: sigma includes the 5 percent flux floor. Comparison: filled points use the posterior-median model. Open squares use the best sample with the fit's own sigma. Total chi-squared 23.9 over 12 bands gives 1.99 per band. Caveat: the spectrum dominates the joint fit, so the fit does not constrain the bands on their own.</figcaption>
</figure>

<figure>
<img loading="lazy" src="/wiki/f/results/rtx-5060-dr2-quiescent-full-spectrum/185631-M12_185631/diagnostics/spectral_chi2.png" alt="M12_185631: spectral pull, binned mean pull squared, cumulative chi-squared">
<figcaption><code>spectral_chi2.png</code> Pull per fitted pixel of the LEGA-C spectrum of galaxy M12_185631. Below it: mean pull squared in 25 Å bins and the cumulative chi-squared fraction against wavelength. Uncertainty: sigma includes the fitted calibration floor of 9.99 percent of the model flux. Comparison: the stored pull versus the pull at the best sample. Shaded bands mark masked pixels. Red points mark pixels with pull beyond 4 sigma. Total chi-squared 6927.5 over 3840 pixels, 13 outlier pixels. Caveat: the fitted floor absorbs model mismatch, so chi-squared near 1 does not prove a good model.</figcaption>
</figure>

<figure>
<img loading="lazy" src="/wiki/f/results/rtx-5060-dr2-quiescent-full-spectrum/185631-M12_185631/diagnostics/sf_timescales.png" alt="M12_185631: cumulative mass formed against lookback time with t10 to t90">
<figcaption><code>sf_timescales.png</code> Fraction of the final stellar mass of galaxy M12_185631 formed earlier than each lookback time. The line is the posterior median. The band is the 16-84 percent range over 400 draws. Comparison: points mark t10 to t90 with 16-84 percent (thick) and 2.5-97.5 percent (thin) intervals versus the universe age. t50 is 2.76 Gyr with a 16-84 percent range of 2.61 to 3.80 Gyr. Caveat: the 7-bin star-formation history model quantises these times to the bin edges.</figcaption>
</figure>

### 185653-M12_185653

| z | S/N | photometry χ²/N | spectrum χ²/N | f_calib | t50 [Gyr] | model |
| --- | --- | --- | --- | --- | --- | --- |
| 0.6776 | 21.5 | 3.05 | 1.124 | 6.44% | 3.01 | [parameters](/wiki/f/results/rtx-5060-dr2-quiescent-full-spectrum/185653-M12_185653/diagnostics/model_parameters.txt) |

Flags:

- photometry chi2/N 3.0 > 3
- 10 pixels with |pull| > 4

<figure>
<img loading="lazy" src="/wiki/f/results/rtx-5060-dr2-quiescent-full-spectrum/185653-M12_185653/diagnostics/photometric_chi2.png" alt="M12_185653: photometric pull and chi-squared contribution per band">
<figcaption><code>photometric_chi2.png</code> Pull and chi-squared contribution for the 12 COSMOS2015 bands of galaxy M12_185653. Pull equals observed minus model over sigma. Uncertainty: sigma includes the 5 percent flux floor. Comparison: filled points use the posterior-median model. Open squares use the best sample with the fit's own sigma. Total chi-squared 36.6 over 12 bands gives 3.05 per band. Caveat: the spectrum dominates the joint fit, so the fit does not constrain the bands on their own.</figcaption>
</figure>

<figure>
<img loading="lazy" src="/wiki/f/results/rtx-5060-dr2-quiescent-full-spectrum/185653-M12_185653/diagnostics/spectral_chi2.png" alt="M12_185653: spectral pull, binned mean pull squared, cumulative chi-squared">
<figcaption><code>spectral_chi2.png</code> Pull per fitted pixel of the LEGA-C spectrum of galaxy M12_185653. Below it: mean pull squared in 25 Å bins and the cumulative chi-squared fraction against wavelength. Uncertainty: sigma includes the fitted calibration floor of 6.44 percent of the model flux. Comparison: the stored pull versus the pull at the best sample. Shaded bands mark masked pixels. Red points mark pixels with pull beyond 4 sigma. Total chi-squared 4021.1 over 3577 pixels, 10 outlier pixels. Caveat: the fitted floor absorbs model mismatch, so chi-squared near 1 does not prove a good model.</figcaption>
</figure>

<figure>
<img loading="lazy" src="/wiki/f/results/rtx-5060-dr2-quiescent-full-spectrum/185653-M12_185653/diagnostics/sf_timescales.png" alt="M12_185653: cumulative mass formed against lookback time with t10 to t90">
<figcaption><code>sf_timescales.png</code> Fraction of the final stellar mass of galaxy M12_185653 formed earlier than each lookback time. The line is the posterior median. The band is the 16-84 percent range over 400 draws. Comparison: points mark t10 to t90 with 16-84 percent (thick) and 2.5-97.5 percent (thin) intervals versus the universe age. t50 is 3.01 Gyr with a 16-84 percent range of 2.99 to 3.11 Gyr. Caveat: the 7-bin star-formation history model quantises these times to the bin edges.</figcaption>
</figure>

### 189698-M10_189698

| z | S/N | photometry χ²/N | spectrum χ²/N | f_calib | t50 [Gyr] | model |
| --- | --- | --- | --- | --- | --- | --- |
| 0.9258 | 7.2 | 4.75 | 1.040 | 2.30% | 3.63 | [parameters](/wiki/f/results/rtx-5060-dr2-quiescent-full-spectrum/189698-M10_189698/diagnostics/model_parameters.txt) |

Flags:

- photometry chi2/N 4.8 > 3

<figure>
<img loading="lazy" src="/wiki/f/results/rtx-5060-dr2-quiescent-full-spectrum/189698-M10_189698/diagnostics/photometric_chi2.png" alt="M10_189698: photometric pull and chi-squared contribution per band">
<figcaption><code>photometric_chi2.png</code> Pull and chi-squared contribution for the 12 COSMOS2015 bands of galaxy M10_189698. Pull equals observed minus model over sigma. Uncertainty: sigma includes the 5 percent flux floor. Comparison: filled points use the posterior-median model. Open squares use the best sample with the fit's own sigma. Total chi-squared 57.0 over 12 bands gives 4.75 per band. Caveat: the spectrum dominates the joint fit, so the fit does not constrain the bands on their own.</figcaption>
</figure>

<figure>
<img loading="lazy" src="/wiki/f/results/rtx-5060-dr2-quiescent-full-spectrum/189698-M10_189698/diagnostics/spectral_chi2.png" alt="M10_189698: spectral pull, binned mean pull squared, cumulative chi-squared">
<figcaption><code>spectral_chi2.png</code> Pull per fitted pixel of the LEGA-C spectrum of galaxy M10_189698. Below it: mean pull squared in 25 Å bins and the cumulative chi-squared fraction against wavelength. Uncertainty: sigma includes the fitted calibration floor of 2.30 percent of the model flux. Comparison: the stored pull versus the pull at the best sample. Shaded bands mark masked pixels. Red points mark pixels with pull beyond 4 sigma. Total chi-squared 3821.6 over 3675 pixels, 0 outlier pixels. Caveat: the fitted floor absorbs model mismatch, so chi-squared near 1 does not prove a good model.</figcaption>
</figure>

<figure>
<img loading="lazy" src="/wiki/f/results/rtx-5060-dr2-quiescent-full-spectrum/189698-M10_189698/diagnostics/sf_timescales.png" alt="M10_189698: cumulative mass formed against lookback time with t10 to t90">
<figcaption><code>sf_timescales.png</code> Fraction of the final stellar mass of galaxy M10_189698 formed earlier than each lookback time. The line is the posterior median. The band is the 16-84 percent range over 400 draws. Comparison: points mark t10 to t90 with 16-84 percent (thick) and 2.5-97.5 percent (thin) intervals versus the universe age. t50 is 3.63 Gyr with a 16-84 percent range of 3.12 to 4.00 Gyr. Caveat: the 7-bin star-formation history model quantises these times to the bin edges.</figcaption>
</figure>

### 191718-M10_191718

| z | S/N | photometry χ²/N | spectrum χ²/N | f_calib | t50 [Gyr] | model |
| --- | --- | --- | --- | --- | --- | --- |
| 0.9840 | 6.8 | 6.29 | 0.929 | 6.39% | 3.03 | [parameters](/wiki/f/results/rtx-5060-dr2-quiescent-full-spectrum/191718-M10_191718/diagnostics/model_parameters.txt) |

Flags:

- photometry chi2/N 6.3 > 3
- 2 pixels with |pull| > 4

<figure>
<img loading="lazy" src="/wiki/f/results/rtx-5060-dr2-quiescent-full-spectrum/191718-M10_191718/diagnostics/photometric_chi2.png" alt="M10_191718: photometric pull and chi-squared contribution per band">
<figcaption><code>photometric_chi2.png</code> Pull and chi-squared contribution for the 12 COSMOS2015 bands of galaxy M10_191718. Pull equals observed minus model over sigma. Uncertainty: sigma includes the 5 percent flux floor. Comparison: filled points use the posterior-median model. Open squares use the best sample with the fit's own sigma. Total chi-squared 75.5 over 12 bands gives 6.29 per band. Caveat: the spectrum dominates the joint fit, so the fit does not constrain the bands on their own.</figcaption>
</figure>

<figure>
<img loading="lazy" src="/wiki/f/results/rtx-5060-dr2-quiescent-full-spectrum/191718-M10_191718/diagnostics/spectral_chi2.png" alt="M10_191718: spectral pull, binned mean pull squared, cumulative chi-squared">
<figcaption><code>spectral_chi2.png</code> Pull per fitted pixel of the LEGA-C spectrum of galaxy M10_191718. Below it: mean pull squared in 25 Å bins and the cumulative chi-squared fraction against wavelength. Uncertainty: sigma includes the fitted calibration floor of 6.39 percent of the model flux. Comparison: the stored pull versus the pull at the best sample. Shaded bands mark masked pixels. Red points mark pixels with pull beyond 4 sigma. Total chi-squared 3520.0 over 3789 pixels, 2 outlier pixels. Caveat: the fitted floor absorbs model mismatch, so chi-squared near 1 does not prove a good model.</figcaption>
</figure>

<figure>
<img loading="lazy" src="/wiki/f/results/rtx-5060-dr2-quiescent-full-spectrum/191718-M10_191718/diagnostics/sf_timescales.png" alt="M10_191718: cumulative mass formed against lookback time with t10 to t90">
<figcaption><code>sf_timescales.png</code> Fraction of the final stellar mass of galaxy M10_191718 formed earlier than each lookback time. The line is the posterior median. The band is the 16-84 percent range over 400 draws. Comparison: points mark t10 to t90 with 16-84 percent (thick) and 2.5-97.5 percent (thin) intervals versus the universe age. t50 is 3.03 Gyr with a 16-84 percent range of 3.00 to 3.17 Gyr. Caveat: the 7-bin star-formation history model quantises these times to the bin edges.</figcaption>
</figure>

### 197591-M10_197591

| z | S/N | photometry χ²/N | spectrum χ²/N | f_calib | t50 [Gyr] | model |
| --- | --- | --- | --- | --- | --- | --- |
| 0.7960 | 23.9 | 9.19 | 1.055 | 4.66% | 3.02 | [parameters](/wiki/f/results/rtx-5060-dr2-quiescent-full-spectrum/197591-M10_197591/diagnostics/model_parameters.txt) |

Flags:

- photometry chi2/N 9.2 > 3
- 2 pixels with |pull| > 4

<figure>
<img loading="lazy" src="/wiki/f/results/rtx-5060-dr2-quiescent-full-spectrum/197591-M10_197591/diagnostics/photometric_chi2.png" alt="M10_197591: photometric pull and chi-squared contribution per band">
<figcaption><code>photometric_chi2.png</code> Pull and chi-squared contribution for the 12 COSMOS2015 bands of galaxy M10_197591. Pull equals observed minus model over sigma. Uncertainty: sigma includes the 5 percent flux floor. Comparison: filled points use the posterior-median model. Open squares use the best sample with the fit's own sigma. Total chi-squared 110.2 over 12 bands gives 9.19 per band. Caveat: the spectrum dominates the joint fit, so the fit does not constrain the bands on their own.</figcaption>
</figure>

<figure>
<img loading="lazy" src="/wiki/f/results/rtx-5060-dr2-quiescent-full-spectrum/197591-M10_197591/diagnostics/spectral_chi2.png" alt="M10_197591: spectral pull, binned mean pull squared, cumulative chi-squared">
<figcaption><code>spectral_chi2.png</code> Pull per fitted pixel of the LEGA-C spectrum of galaxy M10_197591. Below it: mean pull squared in 25 Å bins and the cumulative chi-squared fraction against wavelength. Uncertainty: sigma includes the fitted calibration floor of 4.66 percent of the model flux. Comparison: the stored pull versus the pull at the best sample. Shaded bands mark masked pixels. Red points mark pixels with pull beyond 4 sigma. Total chi-squared 3997.7 over 3789 pixels, 2 outlier pixels. Caveat: the fitted floor absorbs model mismatch, so chi-squared near 1 does not prove a good model.</figcaption>
</figure>

<figure>
<img loading="lazy" src="/wiki/f/results/rtx-5060-dr2-quiescent-full-spectrum/197591-M10_197591/diagnostics/sf_timescales.png" alt="M10_197591: cumulative mass formed against lookback time with t10 to t90">
<figcaption><code>sf_timescales.png</code> Fraction of the final stellar mass of galaxy M10_197591 formed earlier than each lookback time. The line is the posterior median. The band is the 16-84 percent range over 400 draws. Comparison: points mark t10 to t90 with 16-84 percent (thick) and 2.5-97.5 percent (thin) intervals versus the universe age. t50 is 3.02 Gyr with a 16-84 percent range of 3.00 to 3.15 Gyr. Caveat: the 7-bin star-formation history model quantises these times to the bin edges.</figcaption>
</figure>

### 201233-M10_201233

| z | S/N | photometry χ²/N | spectrum χ²/N | f_calib | t50 [Gyr] | model |
| --- | --- | --- | --- | --- | --- | --- |
| 0.8177 | 9.3 | 3.63 | 1.062 | 4.16% | 3.02 | [parameters](/wiki/f/results/rtx-5060-dr2-quiescent-full-spectrum/201233-M10_201233/diagnostics/model_parameters.txt) |

Flags:

- photometry chi2/N 3.6 > 3

<figure>
<img loading="lazy" src="/wiki/f/results/rtx-5060-dr2-quiescent-full-spectrum/201233-M10_201233/diagnostics/photometric_chi2.png" alt="M10_201233: photometric pull and chi-squared contribution per band">
<figcaption><code>photometric_chi2.png</code> Pull and chi-squared contribution for the 12 COSMOS2015 bands of galaxy M10_201233. Pull equals observed minus model over sigma. Uncertainty: sigma includes the 5 percent flux floor. Comparison: filled points use the posterior-median model. Open squares use the best sample with the fit's own sigma. Total chi-squared 43.5 over 12 bands gives 3.63 per band. Caveat: the spectrum dominates the joint fit, so the fit does not constrain the bands on their own.</figcaption>
</figure>

<figure>
<img loading="lazy" src="/wiki/f/results/rtx-5060-dr2-quiescent-full-spectrum/201233-M10_201233/diagnostics/spectral_chi2.png" alt="M10_201233: spectral pull, binned mean pull squared, cumulative chi-squared">
<figcaption><code>spectral_chi2.png</code> Pull per fitted pixel of the LEGA-C spectrum of galaxy M10_201233. Below it: mean pull squared in 25 Å bins and the cumulative chi-squared fraction against wavelength. Uncertainty: sigma includes the fitted calibration floor of 4.16 percent of the model flux. Comparison: the stored pull versus the pull at the best sample. Shaded bands mark masked pixels. Red points mark pixels with pull beyond 4 sigma. Total chi-squared 4045.4 over 3809 pixels, 0 outlier pixels. Caveat: the fitted floor absorbs model mismatch, so chi-squared near 1 does not prove a good model.</figcaption>
</figure>

<figure>
<img loading="lazy" src="/wiki/f/results/rtx-5060-dr2-quiescent-full-spectrum/201233-M10_201233/diagnostics/sf_timescales.png" alt="M10_201233: cumulative mass formed against lookback time with t10 to t90">
<figcaption><code>sf_timescales.png</code> Fraction of the final stellar mass of galaxy M10_201233 formed earlier than each lookback time. The line is the posterior median. The band is the 16-84 percent range over 400 draws. Comparison: points mark t10 to t90 with 16-84 percent (thick) and 2.5-97.5 percent (thin) intervals versus the universe age. t50 is 3.02 Gyr with a 16-84 percent range of 3.00 to 3.13 Gyr. Caveat: the 7-bin star-formation history model quantises these times to the bin edges.</figcaption>
</figure>

### 205715-M5_205715

| z | S/N | photometry χ²/N | spectrum χ²/N | f_calib | t50 [Gyr] | model |
| --- | --- | --- | --- | --- | --- | --- |
| 0.7465 | 33.2 | 5.29 | 1.147 | 4.53% | 3.02 | [parameters](/wiki/f/results/rtx-5060-dr2-quiescent-full-spectrum/205715-M5_205715/diagnostics/model_parameters.txt) |

Flags:

- photometry chi2/N 5.3 > 3
- 4 pixels with |pull| > 4

<figure>
<img loading="lazy" src="/wiki/f/results/rtx-5060-dr2-quiescent-full-spectrum/205715-M5_205715/diagnostics/photometric_chi2.png" alt="M5_205715: photometric pull and chi-squared contribution per band">
<figcaption><code>photometric_chi2.png</code> Pull and chi-squared contribution for the 12 COSMOS2015 bands of galaxy M5_205715. Pull equals observed minus model over sigma. Uncertainty: sigma includes the 5 percent flux floor. Comparison: filled points use the posterior-median model. Open squares use the best sample with the fit's own sigma. Total chi-squared 63.5 over 12 bands gives 5.29 per band. Caveat: the spectrum dominates the joint fit, so the fit does not constrain the bands on their own.</figcaption>
</figure>

<figure>
<img loading="lazy" src="/wiki/f/results/rtx-5060-dr2-quiescent-full-spectrum/205715-M5_205715/diagnostics/spectral_chi2.png" alt="M5_205715: spectral pull, binned mean pull squared, cumulative chi-squared">
<figcaption><code>spectral_chi2.png</code> Pull per fitted pixel of the LEGA-C spectrum of galaxy M5_205715. Below it: mean pull squared in 25 Å bins and the cumulative chi-squared fraction against wavelength. Uncertainty: sigma includes the fitted calibration floor of 4.53 percent of the model flux. Comparison: the stored pull versus the pull at the best sample. Shaded bands mark masked pixels. Red points mark pixels with pull beyond 4 sigma. Total chi-squared 3913.4 over 3411 pixels, 4 outlier pixels. Caveat: the fitted floor absorbs model mismatch, so chi-squared near 1 does not prove a good model.</figcaption>
</figure>

<figure>
<img loading="lazy" src="/wiki/f/results/rtx-5060-dr2-quiescent-full-spectrum/205715-M5_205715/diagnostics/sf_timescales.png" alt="M5_205715: cumulative mass formed against lookback time with t10 to t90">
<figcaption><code>sf_timescales.png</code> Fraction of the final stellar mass of galaxy M5_205715 formed earlier than each lookback time. The line is the posterior median. The band is the 16-84 percent range over 400 draws. Comparison: points mark t10 to t90 with 16-84 percent (thick) and 2.5-97.5 percent (thin) intervals versus the universe age. t50 is 3.02 Gyr with a 16-84 percent range of 2.99 to 3.11 Gyr. Caveat: the 7-bin star-formation history model quantises these times to the bin edges.</figcaption>
</figure>

### 205742-M1_205742

| z | S/N | photometry χ²/N | spectrum χ²/N | f_calib | t50 [Gyr] | model |
| --- | --- | --- | --- | --- | --- | --- |
| 0.7273 | 42.8 | 14.80 | 1.158 | 3.87% | 4.37 | [parameters](/wiki/f/results/rtx-5060-dr2-quiescent-full-spectrum/205742-M1_205742/diagnostics/model_parameters.txt) |

Flags:

- photometry chi2/N 14.8 > 3
- 13 pixels with |pull| > 4

<figure>
<img loading="lazy" src="/wiki/f/results/rtx-5060-dr2-quiescent-full-spectrum/205742-M1_205742/diagnostics/photometric_chi2.png" alt="M1_205742: photometric pull and chi-squared contribution per band">
<figcaption><code>photometric_chi2.png</code> Pull and chi-squared contribution for the 12 COSMOS2015 bands of galaxy M1_205742. Pull equals observed minus model over sigma. Uncertainty: sigma includes the 5 percent flux floor. Comparison: filled points use the posterior-median model. Open squares use the best sample with the fit's own sigma. Total chi-squared 177.6 over 12 bands gives 14.80 per band. Caveat: the spectrum dominates the joint fit, so the fit does not constrain the bands on their own.</figcaption>
</figure>

<figure>
<img loading="lazy" src="/wiki/f/results/rtx-5060-dr2-quiescent-full-spectrum/205742-M1_205742/diagnostics/spectral_chi2.png" alt="M1_205742: spectral pull, binned mean pull squared, cumulative chi-squared">
<figcaption><code>spectral_chi2.png</code> Pull per fitted pixel of the LEGA-C spectrum of galaxy M1_205742. Below it: mean pull squared in 25 Å bins and the cumulative chi-squared fraction against wavelength. Uncertainty: sigma includes the fitted calibration floor of 3.87 percent of the model flux. Comparison: the stored pull versus the pull at the best sample. Shaded bands mark masked pixels. Red points mark pixels with pull beyond 4 sigma. Total chi-squared 4079.6 over 3523 pixels, 13 outlier pixels. Caveat: the fitted floor absorbs model mismatch, so chi-squared near 1 does not prove a good model.</figcaption>
</figure>

<figure>
<img loading="lazy" src="/wiki/f/results/rtx-5060-dr2-quiescent-full-spectrum/205742-M1_205742/diagnostics/sf_timescales.png" alt="M1_205742: cumulative mass formed against lookback time with t10 to t90">
<figcaption><code>sf_timescales.png</code> Fraction of the final stellar mass of galaxy M1_205742 formed earlier than each lookback time. The line is the posterior median. The band is the 16-84 percent range over 400 draws. Comparison: points mark t10 to t90 with 16-84 percent (thick) and 2.5-97.5 percent (thin) intervals versus the universe age. t50 is 4.37 Gyr with a 16-84 percent range of 3.01 to 5.03 Gyr. Caveat: the 7-bin star-formation history model quantises these times to the bin edges.</figcaption>
</figure>

### 205765-M5_205765

| z | S/N | photometry χ²/N | spectrum χ²/N | f_calib | t50 [Gyr] | model |
| --- | --- | --- | --- | --- | --- | --- |
| 0.7287 | 14.3 | 25.62 | 1.040 | 4.82% | 3.58 | [parameters](/wiki/f/results/rtx-5060-dr2-quiescent-full-spectrum/205765-M5_205765/diagnostics/model_parameters.txt) |

Flags:

- photometry chi2/N 25.6 > 3
- 5 pixels with |pull| > 4

<figure>
<img loading="lazy" src="/wiki/f/results/rtx-5060-dr2-quiescent-full-spectrum/205765-M5_205765/diagnostics/photometric_chi2.png" alt="M5_205765: photometric pull and chi-squared contribution per band">
<figcaption><code>photometric_chi2.png</code> Pull and chi-squared contribution for the 12 COSMOS2015 bands of galaxy M5_205765. Pull equals observed minus model over sigma. Uncertainty: sigma includes the 5 percent flux floor. Comparison: filled points use the posterior-median model. Open squares use the best sample with the fit's own sigma. Total chi-squared 307.4 over 12 bands gives 25.62 per band. Caveat: the spectrum dominates the joint fit, so the fit does not constrain the bands on their own.</figcaption>
</figure>

<figure>
<img loading="lazy" src="/wiki/f/results/rtx-5060-dr2-quiescent-full-spectrum/205765-M5_205765/diagnostics/spectral_chi2.png" alt="M5_205765: spectral pull, binned mean pull squared, cumulative chi-squared">
<figcaption><code>spectral_chi2.png</code> Pull per fitted pixel of the LEGA-C spectrum of galaxy M5_205765. Below it: mean pull squared in 25 Å bins and the cumulative chi-squared fraction against wavelength. Uncertainty: sigma includes the fitted calibration floor of 4.82 percent of the model flux. Comparison: the stored pull versus the pull at the best sample. Shaded bands mark masked pixels. Red points mark pixels with pull beyond 4 sigma. Total chi-squared 3644.7 over 3504 pixels, 5 outlier pixels. Caveat: the fitted floor absorbs model mismatch, so chi-squared near 1 does not prove a good model.</figcaption>
</figure>

<figure>
<img loading="lazy" src="/wiki/f/results/rtx-5060-dr2-quiescent-full-spectrum/205765-M5_205765/diagnostics/sf_timescales.png" alt="M5_205765: cumulative mass formed against lookback time with t10 to t90">
<figcaption><code>sf_timescales.png</code> Fraction of the final stellar mass of galaxy M5_205765 formed earlier than each lookback time. The line is the posterior median. The band is the 16-84 percent range over 400 draws. Comparison: points mark t10 to t90 with 16-84 percent (thick) and 2.5-97.5 percent (thin) intervals versus the universe age. t50 is 3.58 Gyr with a 16-84 percent range of 3.25 to 4.02 Gyr. Caveat: the 7-bin star-formation history model quantises these times to the bin edges.</figcaption>
</figure>

### 206501-M1_206501

| z | S/N | photometry χ²/N | spectrum χ²/N | f_calib | t50 [Gyr] | model |
| --- | --- | --- | --- | --- | --- | --- |
| 0.9262 | 30.5 | 22.94 | 1.145 | 5.43% | 4.57 | [parameters](/wiki/f/results/rtx-5060-dr2-quiescent-full-spectrum/206501-M1_206501/diagnostics/model_parameters.txt) |

Flags:

- photometry chi2/N 22.9 > 3
- 17 pixels with |pull| > 4

<figure>
<img loading="lazy" src="/wiki/f/results/rtx-5060-dr2-quiescent-full-spectrum/206501-M1_206501/diagnostics/photometric_chi2.png" alt="M1_206501: photometric pull and chi-squared contribution per band">
<figcaption><code>photometric_chi2.png</code> Pull and chi-squared contribution for the 12 COSMOS2015 bands of galaxy M1_206501. Pull equals observed minus model over sigma. Uncertainty: sigma includes the 5 percent flux floor. Comparison: filled points use the posterior-median model. Open squares use the best sample with the fit's own sigma. Total chi-squared 275.3 over 12 bands gives 22.94 per band. Caveat: the spectrum dominates the joint fit, so the fit does not constrain the bands on their own.</figcaption>
</figure>

<figure>
<img loading="lazy" src="/wiki/f/results/rtx-5060-dr2-quiescent-full-spectrum/206501-M1_206501/diagnostics/spectral_chi2.png" alt="M1_206501: spectral pull, binned mean pull squared, cumulative chi-squared">
<figcaption><code>spectral_chi2.png</code> Pull per fitted pixel of the LEGA-C spectrum of galaxy M1_206501. Below it: mean pull squared in 25 Å bins and the cumulative chi-squared fraction against wavelength. Uncertainty: sigma includes the fitted calibration floor of 5.43 percent of the model flux. Comparison: the stored pull versus the pull at the best sample. Shaded bands mark masked pixels. Red points mark pixels with pull beyond 4 sigma. Total chi-squared 4386.9 over 3830 pixels, 17 outlier pixels. Caveat: the fitted floor absorbs model mismatch, so chi-squared near 1 does not prove a good model.</figcaption>
</figure>

<figure>
<img loading="lazy" src="/wiki/f/results/rtx-5060-dr2-quiescent-full-spectrum/206501-M1_206501/diagnostics/sf_timescales.png" alt="M1_206501: cumulative mass formed against lookback time with t10 to t90">
<figcaption><code>sf_timescales.png</code> Fraction of the final stellar mass of galaxy M1_206501 formed earlier than each lookback time. The line is the posterior median. The band is the 16-84 percent range over 400 draws. Comparison: points mark t10 to t90 with 16-84 percent (thick) and 2.5-97.5 percent (thin) intervals versus the universe age. t50 is 4.57 Gyr with a 16-84 percent range of 4.55 to 4.65 Gyr. Caveat: the 7-bin star-formation history model quantises these times to the bin edges.</figcaption>
</figure>

### 206545-M1_206545

| z | S/N | photometry χ²/N | spectrum χ²/N | f_calib | t50 [Gyr] | model |
| --- | --- | --- | --- | --- | --- | --- |
| 0.7283 | 31.4 | 11.09 | 1.286 | 5.71% | 2.92 | [parameters](/wiki/f/results/rtx-5060-dr2-quiescent-full-spectrum/206545-M1_206545/diagnostics/model_parameters.txt) |

Flags:

- photometry chi2/N 11.1 > 3
- 22 pixels with |pull| > 4

<figure>
<img loading="lazy" src="/wiki/f/results/rtx-5060-dr2-quiescent-full-spectrum/206545-M1_206545/diagnostics/photometric_chi2.png" alt="M1_206545: photometric pull and chi-squared contribution per band">
<figcaption><code>photometric_chi2.png</code> Pull and chi-squared contribution for the 12 COSMOS2015 bands of galaxy M1_206545. Pull equals observed minus model over sigma. Uncertainty: sigma includes the 5 percent flux floor. Comparison: filled points use the posterior-median model. Open squares use the best sample with the fit's own sigma. Total chi-squared 133.1 over 12 bands gives 11.09 per band. Caveat: the spectrum dominates the joint fit, so the fit does not constrain the bands on their own.</figcaption>
</figure>

<figure>
<img loading="lazy" src="/wiki/f/results/rtx-5060-dr2-quiescent-full-spectrum/206545-M1_206545/diagnostics/spectral_chi2.png" alt="M1_206545: spectral pull, binned mean pull squared, cumulative chi-squared">
<figcaption><code>spectral_chi2.png</code> Pull per fitted pixel of the LEGA-C spectrum of galaxy M1_206545. Below it: mean pull squared in 25 Å bins and the cumulative chi-squared fraction against wavelength. Uncertainty: sigma includes the fitted calibration floor of 5.71 percent of the model flux. Comparison: the stored pull versus the pull at the best sample. Shaded bands mark masked pixels. Red points mark pixels with pull beyond 4 sigma. Total chi-squared 4401.0 over 3422 pixels, 22 outlier pixels. Caveat: the fitted floor absorbs model mismatch, so chi-squared near 1 does not prove a good model.</figcaption>
</figure>

<figure>
<img loading="lazy" src="/wiki/f/results/rtx-5060-dr2-quiescent-full-spectrum/206545-M1_206545/diagnostics/sf_timescales.png" alt="M1_206545: cumulative mass formed against lookback time with t10 to t90">
<figcaption><code>sf_timescales.png</code> Fraction of the final stellar mass of galaxy M1_206545 formed earlier than each lookback time. The line is the posterior median. The band is the 16-84 percent range over 400 draws. Comparison: points mark t10 to t90 with 16-84 percent (thick) and 2.5-97.5 percent (thin) intervals versus the universe age. t50 is 2.92 Gyr with a 16-84 percent range of 2.89 to 2.97 Gyr. Caveat: the 7-bin star-formation history model quantises these times to the bin edges.</figcaption>
</figure>

### 206669-M2_206669

| z | S/N | photometry χ²/N | spectrum χ²/N | f_calib | t50 [Gyr] | model |
| --- | --- | --- | --- | --- | --- | --- |
| 0.6716 | 35.2 | 7.69 | 1.084 | 3.57% | 3.74 | [parameters](/wiki/f/results/rtx-5060-dr2-quiescent-full-spectrum/206669-M2_206669/diagnostics/model_parameters.txt) |

Flags:

- photometry chi2/N 7.7 > 3
- 3 pixels with |pull| > 4

<figure>
<img loading="lazy" src="/wiki/f/results/rtx-5060-dr2-quiescent-full-spectrum/206669-M2_206669/diagnostics/photometric_chi2.png" alt="M2_206669: photometric pull and chi-squared contribution per band">
<figcaption><code>photometric_chi2.png</code> Pull and chi-squared contribution for the 12 COSMOS2015 bands of galaxy M2_206669. Pull equals observed minus model over sigma. Uncertainty: sigma includes the 5 percent flux floor. Comparison: filled points use the posterior-median model. Open squares use the best sample with the fit's own sigma. Total chi-squared 92.3 over 12 bands gives 7.69 per band. Caveat: the spectrum dominates the joint fit, so the fit does not constrain the bands on their own.</figcaption>
</figure>

<figure>
<img loading="lazy" src="/wiki/f/results/rtx-5060-dr2-quiescent-full-spectrum/206669-M2_206669/diagnostics/spectral_chi2.png" alt="M2_206669: spectral pull, binned mean pull squared, cumulative chi-squared">
<figcaption><code>spectral_chi2.png</code> Pull per fitted pixel of the LEGA-C spectrum of galaxy M2_206669. Below it: mean pull squared in 25 Å bins and the cumulative chi-squared fraction against wavelength. Uncertainty: sigma includes the fitted calibration floor of 3.57 percent of the model flux. Comparison: the stored pull versus the pull at the best sample. Shaded bands mark masked pixels. Red points mark pixels with pull beyond 4 sigma. Total chi-squared 3896.3 over 3594 pixels, 3 outlier pixels. Caveat: the fitted floor absorbs model mismatch, so chi-squared near 1 does not prove a good model.</figcaption>
</figure>

<figure>
<img loading="lazy" src="/wiki/f/results/rtx-5060-dr2-quiescent-full-spectrum/206669-M2_206669/diagnostics/sf_timescales.png" alt="M2_206669: cumulative mass formed against lookback time with t10 to t90">
<figcaption><code>sf_timescales.png</code> Fraction of the final stellar mass of galaxy M2_206669 formed earlier than each lookback time. The line is the posterior median. The band is the 16-84 percent range over 400 draws. Comparison: points mark t10 to t90 with 16-84 percent (thick) and 2.5-97.5 percent (thin) intervals versus the universe age. t50 is 3.74 Gyr with a 16-84 percent range of 3.47 to 4.10 Gyr. Caveat: the 7-bin star-formation history model quantises these times to the bin edges.</figcaption>
</figure>

### 206771-M5_206771

| z | S/N | photometry χ²/N | spectrum χ²/N | f_calib | t50 [Gyr] | model |
| --- | --- | --- | --- | --- | --- | --- |
| 0.6295 | 12.3 | 2.90 | 1.150 | 6.66% | 5.36 | [parameters](/wiki/f/results/rtx-5060-dr2-quiescent-full-spectrum/206771-M5_206771/diagnostics/model_parameters.txt) |

Flags:

- 3 pixels with |pull| > 4

<figure>
<img loading="lazy" src="/wiki/f/results/rtx-5060-dr2-quiescent-full-spectrum/206771-M5_206771/diagnostics/photometric_chi2.png" alt="M5_206771: photometric pull and chi-squared contribution per band">
<figcaption><code>photometric_chi2.png</code> Pull and chi-squared contribution for the 12 COSMOS2015 bands of galaxy M5_206771. Pull equals observed minus model over sigma. Uncertainty: sigma includes the 5 percent flux floor. Comparison: filled points use the posterior-median model. Open squares use the best sample with the fit's own sigma. Total chi-squared 34.8 over 12 bands gives 2.90 per band. Caveat: the spectrum dominates the joint fit, so the fit does not constrain the bands on their own.</figcaption>
</figure>

<figure>
<img loading="lazy" src="/wiki/f/results/rtx-5060-dr2-quiescent-full-spectrum/206771-M5_206771/diagnostics/spectral_chi2.png" alt="M5_206771: spectral pull, binned mean pull squared, cumulative chi-squared">
<figcaption><code>spectral_chi2.png</code> Pull per fitted pixel of the LEGA-C spectrum of galaxy M5_206771. Below it: mean pull squared in 25 Å bins and the cumulative chi-squared fraction against wavelength. Uncertainty: sigma includes the fitted calibration floor of 6.66 percent of the model flux. Comparison: the stored pull versus the pull at the best sample. Shaded bands mark masked pixels. Red points mark pixels with pull beyond 4 sigma. Total chi-squared 4106.4 over 3571 pixels, 3 outlier pixels. Caveat: the fitted floor absorbs model mismatch, so chi-squared near 1 does not prove a good model.</figcaption>
</figure>

<figure>
<img loading="lazy" src="/wiki/f/results/rtx-5060-dr2-quiescent-full-spectrum/206771-M5_206771/diagnostics/sf_timescales.png" alt="M5_206771: cumulative mass formed against lookback time with t10 to t90">
<figcaption><code>sf_timescales.png</code> Fraction of the final stellar mass of galaxy M5_206771 formed earlier than each lookback time. The line is the posterior median. The band is the 16-84 percent range over 400 draws. Comparison: points mark t10 to t90 with 16-84 percent (thick) and 2.5-97.5 percent (thin) intervals versus the universe age. t50 is 5.36 Gyr with a 16-84 percent range of 5.12 to 5.53 Gyr. Caveat: the 7-bin star-formation history model quantises these times to the bin edges.</figcaption>
</figure>

### 206858-M1_206858

| z | S/N | photometry χ²/N | spectrum χ²/N | f_calib | t50 [Gyr] | model |
| --- | --- | --- | --- | --- | --- | --- |
| 0.7248 | 33.4 | 5.23 | 1.120 | 4.35% | 1.65 | [parameters](/wiki/f/results/rtx-5060-dr2-quiescent-full-spectrum/206858-M1_206858/diagnostics/model_parameters.txt) |

Flags:

- photometry chi2/N 5.2 > 3
- 13 pixels with |pull| > 4

<figure>
<img loading="lazy" src="/wiki/f/results/rtx-5060-dr2-quiescent-full-spectrum/206858-M1_206858/diagnostics/photometric_chi2.png" alt="M1_206858: photometric pull and chi-squared contribution per band">
<figcaption><code>photometric_chi2.png</code> Pull and chi-squared contribution for the 12 COSMOS2015 bands of galaxy M1_206858. Pull equals observed minus model over sigma. Uncertainty: sigma includes the 5 percent flux floor. Comparison: filled points use the posterior-median model. Open squares use the best sample with the fit's own sigma. Total chi-squared 62.8 over 12 bands gives 5.23 per band. Caveat: the spectrum dominates the joint fit, so the fit does not constrain the bands on their own.</figcaption>
</figure>

<figure>
<img loading="lazy" src="/wiki/f/results/rtx-5060-dr2-quiescent-full-spectrum/206858-M1_206858/diagnostics/spectral_chi2.png" alt="M1_206858: spectral pull, binned mean pull squared, cumulative chi-squared">
<figcaption><code>spectral_chi2.png</code> Pull per fitted pixel of the LEGA-C spectrum of galaxy M1_206858. Below it: mean pull squared in 25 Å bins and the cumulative chi-squared fraction against wavelength. Uncertainty: sigma includes the fitted calibration floor of 4.35 percent of the model flux. Comparison: the stored pull versus the pull at the best sample. Shaded bands mark masked pixels. Red points mark pixels with pull beyond 4 sigma. Total chi-squared 3968.9 over 3545 pixels, 13 outlier pixels. Caveat: the fitted floor absorbs model mismatch, so chi-squared near 1 does not prove a good model.</figcaption>
</figure>

<figure>
<img loading="lazy" src="/wiki/f/results/rtx-5060-dr2-quiescent-full-spectrum/206858-M1_206858/diagnostics/sf_timescales.png" alt="M1_206858: cumulative mass formed against lookback time with t10 to t90">
<figcaption><code>sf_timescales.png</code> Fraction of the final stellar mass of galaxy M1_206858 formed earlier than each lookback time. The line is the posterior median. The band is the 16-84 percent range over 400 draws. Comparison: points mark t10 to t90 with 16-84 percent (thick) and 2.5-97.5 percent (thin) intervals versus the universe age. t50 is 1.65 Gyr with a 16-84 percent range of 1.64 to 1.66 Gyr. Caveat: the 7-bin star-formation history model quantises these times to the bin edges.</figcaption>
</figure>

### 208364-M2_208364

| z | S/N | photometry χ²/N | spectrum χ²/N | f_calib | t50 [Gyr] | model |
| --- | --- | --- | --- | --- | --- | --- |
| 0.6678 | 25.1 | 5.45 | 1.050 | 2.84% | 2.85 | [parameters](/wiki/f/results/rtx-5060-dr2-quiescent-full-spectrum/208364-M2_208364/diagnostics/model_parameters.txt) |

Flags:

- photometry chi2/N 5.4 > 3

<figure>
<img loading="lazy" src="/wiki/f/results/rtx-5060-dr2-quiescent-full-spectrum/208364-M2_208364/diagnostics/photometric_chi2.png" alt="M2_208364: photometric pull and chi-squared contribution per band">
<figcaption><code>photometric_chi2.png</code> Pull and chi-squared contribution for the 12 COSMOS2015 bands of galaxy M2_208364. Pull equals observed minus model over sigma. Uncertainty: sigma includes the 5 percent flux floor. Comparison: filled points use the posterior-median model. Open squares use the best sample with the fit's own sigma. Total chi-squared 65.3 over 12 bands gives 5.45 per band. Caveat: the spectrum dominates the joint fit, so the fit does not constrain the bands on their own.</figcaption>
</figure>

<figure>
<img loading="lazy" src="/wiki/f/results/rtx-5060-dr2-quiescent-full-spectrum/208364-M2_208364/diagnostics/spectral_chi2.png" alt="M2_208364: spectral pull, binned mean pull squared, cumulative chi-squared">
<figcaption><code>spectral_chi2.png</code> Pull per fitted pixel of the LEGA-C spectrum of galaxy M2_208364. Below it: mean pull squared in 25 Å bins and the cumulative chi-squared fraction against wavelength. Uncertainty: sigma includes the fitted calibration floor of 2.84 percent of the model flux. Comparison: the stored pull versus the pull at the best sample. Shaded bands mark masked pixels. Red points mark pixels with pull beyond 4 sigma. Total chi-squared 3760.3 over 3581 pixels, 0 outlier pixels. Caveat: the fitted floor absorbs model mismatch, so chi-squared near 1 does not prove a good model.</figcaption>
</figure>

<figure>
<img loading="lazy" src="/wiki/f/results/rtx-5060-dr2-quiescent-full-spectrum/208364-M2_208364/diagnostics/sf_timescales.png" alt="M2_208364: cumulative mass formed against lookback time with t10 to t90">
<figcaption><code>sf_timescales.png</code> Fraction of the final stellar mass of galaxy M2_208364 formed earlier than each lookback time. The line is the posterior median. The band is the 16-84 percent range over 400 draws. Comparison: points mark t10 to t90 with 16-84 percent (thick) and 2.5-97.5 percent (thin) intervals versus the universe age. t50 is 2.85 Gyr with a 16-84 percent range of 2.80 to 2.94 Gyr. Caveat: the 7-bin star-formation history model quantises these times to the bin edges.</figcaption>
</figure>

### 208622-M1_208622

| z | S/N | photometry χ²/N | spectrum χ²/N | f_calib | t50 [Gyr] | model |
| --- | --- | --- | --- | --- | --- | --- |
| 0.6479 | 17.9 | 5.28 | 1.137 | 4.07% | 3.01 | [parameters](/wiki/f/results/rtx-5060-dr2-quiescent-full-spectrum/208622-M1_208622/diagnostics/model_parameters.txt) |

Flags:

- photometry chi2/N 5.3 > 3
- 5 pixels with |pull| > 4

<figure>
<img loading="lazy" src="/wiki/f/results/rtx-5060-dr2-quiescent-full-spectrum/208622-M1_208622/diagnostics/photometric_chi2.png" alt="M1_208622: photometric pull and chi-squared contribution per band">
<figcaption><code>photometric_chi2.png</code> Pull and chi-squared contribution for the 12 COSMOS2015 bands of galaxy M1_208622. Pull equals observed minus model over sigma. Uncertainty: sigma includes the 5 percent flux floor. Comparison: filled points use the posterior-median model. Open squares use the best sample with the fit's own sigma. Total chi-squared 63.4 over 12 bands gives 5.28 per band. Caveat: the spectrum dominates the joint fit, so the fit does not constrain the bands on their own.</figcaption>
</figure>

<figure>
<img loading="lazy" src="/wiki/f/results/rtx-5060-dr2-quiescent-full-spectrum/208622-M1_208622/diagnostics/spectral_chi2.png" alt="M1_208622: spectral pull, binned mean pull squared, cumulative chi-squared">
<figcaption><code>spectral_chi2.png</code> Pull per fitted pixel of the LEGA-C spectrum of galaxy M1_208622. Below it: mean pull squared in 25 Å bins and the cumulative chi-squared fraction against wavelength. Uncertainty: sigma includes the fitted calibration floor of 4.07 percent of the model flux. Comparison: the stored pull versus the pull at the best sample. Shaded bands mark masked pixels. Red points mark pixels with pull beyond 4 sigma. Total chi-squared 4026.0 over 3541 pixels, 5 outlier pixels. Caveat: the fitted floor absorbs model mismatch, so chi-squared near 1 does not prove a good model.</figcaption>
</figure>

<figure>
<img loading="lazy" src="/wiki/f/results/rtx-5060-dr2-quiescent-full-spectrum/208622-M1_208622/diagnostics/sf_timescales.png" alt="M1_208622: cumulative mass formed against lookback time with t10 to t90">
<figcaption><code>sf_timescales.png</code> Fraction of the final stellar mass of galaxy M1_208622 formed earlier than each lookback time. The line is the posterior median. The band is the 16-84 percent range over 400 draws. Comparison: points mark t10 to t90 with 16-84 percent (thick) and 2.5-97.5 percent (thin) intervals versus the universe age. t50 is 3.01 Gyr with a 16-84 percent range of 2.99 to 3.08 Gyr. Caveat: the 7-bin star-formation history model quantises these times to the bin edges.</figcaption>
</figure>

### 210210-M1_210210

| z | S/N | photometry χ²/N | spectrum χ²/N | f_calib | t50 [Gyr] | model |
| --- | --- | --- | --- | --- | --- | --- |
| 0.6542 | 62.2 | 9.68 | 1.112 | 4.62% | 4.68 | [parameters](/wiki/f/results/rtx-5060-dr2-quiescent-full-spectrum/210210-M1_210210/diagnostics/model_parameters.txt) |

Flags:

- photometry chi2/N 9.7 > 3
- 10 pixels with |pull| > 4

<figure>
<img loading="lazy" src="/wiki/f/results/rtx-5060-dr2-quiescent-full-spectrum/210210-M1_210210/diagnostics/photometric_chi2.png" alt="M1_210210: photometric pull and chi-squared contribution per band">
<figcaption><code>photometric_chi2.png</code> Pull and chi-squared contribution for the 12 COSMOS2015 bands of galaxy M1_210210. Pull equals observed minus model over sigma. Uncertainty: sigma includes the 5 percent flux floor. Comparison: filled points use the posterior-median model. Open squares use the best sample with the fit's own sigma. Total chi-squared 116.2 over 12 bands gives 9.68 per band. Caveat: the spectrum dominates the joint fit, so the fit does not constrain the bands on their own.</figcaption>
</figure>

<figure>
<img loading="lazy" src="/wiki/f/results/rtx-5060-dr2-quiescent-full-spectrum/210210-M1_210210/diagnostics/spectral_chi2.png" alt="M1_210210: spectral pull, binned mean pull squared, cumulative chi-squared">
<figcaption><code>spectral_chi2.png</code> Pull per fitted pixel of the LEGA-C spectrum of galaxy M1_210210. Below it: mean pull squared in 25 Å bins and the cumulative chi-squared fraction against wavelength. Uncertainty: sigma includes the fitted calibration floor of 4.62 percent of the model flux. Comparison: the stored pull versus the pull at the best sample. Shaded bands mark masked pixels. Red points mark pixels with pull beyond 4 sigma. Total chi-squared 3919.2 over 3523 pixels, 10 outlier pixels. Caveat: the fitted floor absorbs model mismatch, so chi-squared near 1 does not prove a good model.</figcaption>
</figure>

<figure>
<img loading="lazy" src="/wiki/f/results/rtx-5060-dr2-quiescent-full-spectrum/210210-M1_210210/diagnostics/sf_timescales.png" alt="M1_210210: cumulative mass formed against lookback time with t10 to t90">
<figcaption><code>sf_timescales.png</code> Fraction of the final stellar mass of galaxy M1_210210 formed earlier than each lookback time. The line is the posterior median. The band is the 16-84 percent range over 400 draws. Comparison: points mark t10 to t90 with 16-84 percent (thick) and 2.5-97.5 percent (thin) intervals versus the universe age. t50 is 4.68 Gyr with a 16-84 percent range of 4.60 to 4.84 Gyr. Caveat: the 7-bin star-formation history model quantises these times to the bin edges.</figcaption>
</figure>

### 210940-M2_210940

| z | S/N | photometry χ²/N | spectrum χ²/N | f_calib | t50 [Gyr] | model |
| --- | --- | --- | --- | --- | --- | --- |
| 0.6949 | 13.7 | 7.21 | 0.946 | 4.07% | 2.98 | [parameters](/wiki/f/results/rtx-5060-dr2-quiescent-full-spectrum/210940-M2_210940/diagnostics/model_parameters.txt) |

Flags:

- photometry chi2/N 7.2 > 3
- 1 pixels with |pull| > 4

<figure>
<img loading="lazy" src="/wiki/f/results/rtx-5060-dr2-quiescent-full-spectrum/210940-M2_210940/diagnostics/photometric_chi2.png" alt="M2_210940: photometric pull and chi-squared contribution per band">
<figcaption><code>photometric_chi2.png</code> Pull and chi-squared contribution for the 12 COSMOS2015 bands of galaxy M2_210940. Pull equals observed minus model over sigma. Uncertainty: sigma includes the 5 percent flux floor. Comparison: filled points use the posterior-median model. Open squares use the best sample with the fit's own sigma. Total chi-squared 86.6 over 12 bands gives 7.21 per band. Caveat: the spectrum dominates the joint fit, so the fit does not constrain the bands on their own.</figcaption>
</figure>

<figure>
<img loading="lazy" src="/wiki/f/results/rtx-5060-dr2-quiescent-full-spectrum/210940-M2_210940/diagnostics/spectral_chi2.png" alt="M2_210940: spectral pull, binned mean pull squared, cumulative chi-squared">
<figcaption><code>spectral_chi2.png</code> Pull per fitted pixel of the LEGA-C spectrum of galaxy M2_210940. Below it: mean pull squared in 25 Å bins and the cumulative chi-squared fraction against wavelength. Uncertainty: sigma includes the fitted calibration floor of 4.07 percent of the model flux. Comparison: the stored pull versus the pull at the best sample. Shaded bands mark masked pixels. Red points mark pixels with pull beyond 4 sigma. Total chi-squared 3382.3 over 3577 pixels, 1 outlier pixels. Caveat: the fitted floor absorbs model mismatch, so chi-squared near 1 does not prove a good model.</figcaption>
</figure>

<figure>
<img loading="lazy" src="/wiki/f/results/rtx-5060-dr2-quiescent-full-spectrum/210940-M2_210940/diagnostics/sf_timescales.png" alt="M2_210940: cumulative mass formed against lookback time with t10 to t90">
<figcaption><code>sf_timescales.png</code> Fraction of the final stellar mass of galaxy M2_210940 formed earlier than each lookback time. The line is the posterior median. The band is the 16-84 percent range over 400 draws. Comparison: points mark t10 to t90 with 16-84 percent (thick) and 2.5-97.5 percent (thin) intervals versus the universe age. t50 is 2.98 Gyr with a 16-84 percent range of 2.83 to 3.89 Gyr. Caveat: the 7-bin star-formation history model quantises these times to the bin edges.</figcaption>
</figure>

### 211157-M1_211157

| z | S/N | photometry χ²/N | spectrum χ²/N | f_calib | t50 [Gyr] | model |
| --- | --- | --- | --- | --- | --- | --- |
| 0.6070 | 35.1 | 7.30 | 1.214 | 4.80% | 3.70 | [parameters](/wiki/f/results/rtx-5060-dr2-quiescent-full-spectrum/211157-M1_211157/diagnostics/model_parameters.txt) |

Flags:

- photometry chi2/N 7.3 > 3
- 14 pixels with |pull| > 4

<figure>
<img loading="lazy" src="/wiki/f/results/rtx-5060-dr2-quiescent-full-spectrum/211157-M1_211157/diagnostics/photometric_chi2.png" alt="M1_211157: photometric pull and chi-squared contribution per band">
<figcaption><code>photometric_chi2.png</code> Pull and chi-squared contribution for the 12 COSMOS2015 bands of galaxy M1_211157. Pull equals observed minus model over sigma. Uncertainty: sigma includes the 5 percent flux floor. Comparison: filled points use the posterior-median model. Open squares use the best sample with the fit's own sigma. Total chi-squared 87.7 over 12 bands gives 7.30 per band. Caveat: the spectrum dominates the joint fit, so the fit does not constrain the bands on their own.</figcaption>
</figure>

<figure>
<img loading="lazy" src="/wiki/f/results/rtx-5060-dr2-quiescent-full-spectrum/211157-M1_211157/diagnostics/spectral_chi2.png" alt="M1_211157: spectral pull, binned mean pull squared, cumulative chi-squared">
<figcaption><code>spectral_chi2.png</code> Pull per fitted pixel of the LEGA-C spectrum of galaxy M1_211157. Below it: mean pull squared in 25 Å bins and the cumulative chi-squared fraction against wavelength. Uncertainty: sigma includes the fitted calibration floor of 4.80 percent of the model flux. Comparison: the stored pull versus the pull at the best sample. Shaded bands mark masked pixels. Red points mark pixels with pull beyond 4 sigma. Total chi-squared 4330.8 over 3567 pixels, 14 outlier pixels. Caveat: the fitted floor absorbs model mismatch, so chi-squared near 1 does not prove a good model.</figcaption>
</figure>

<figure>
<img loading="lazy" src="/wiki/f/results/rtx-5060-dr2-quiescent-full-spectrum/211157-M1_211157/diagnostics/sf_timescales.png" alt="M1_211157: cumulative mass formed against lookback time with t10 to t90">
<figcaption><code>sf_timescales.png</code> Fraction of the final stellar mass of galaxy M1_211157 formed earlier than each lookback time. The line is the posterior median. The band is the 16-84 percent range over 400 draws. Comparison: points mark t10 to t90 with 16-84 percent (thick) and 2.5-97.5 percent (thin) intervals versus the universe age. t50 is 3.70 Gyr with a 16-84 percent range of 3.24 to 4.11 Gyr. Caveat: the 7-bin star-formation history model quantises these times to the bin edges.</figcaption>
</figure>

### 211347-M5_211347

| z | S/N | photometry χ²/N | spectrum χ²/N | f_calib | t50 [Gyr] | model |
| --- | --- | --- | --- | --- | --- | --- |
| 0.6972 | 29.2 | 9.29 | 1.143 | 4.06% | 2.96 | [parameters](/wiki/f/results/rtx-5060-dr2-quiescent-full-spectrum/211347-M5_211347/diagnostics/model_parameters.txt) |

Flags:

- photometry chi2/N 9.3 > 3
- 6 pixels with |pull| > 4

<figure>
<img loading="lazy" src="/wiki/f/results/rtx-5060-dr2-quiescent-full-spectrum/211347-M5_211347/diagnostics/photometric_chi2.png" alt="M5_211347: photometric pull and chi-squared contribution per band">
<figcaption><code>photometric_chi2.png</code> Pull and chi-squared contribution for the 12 COSMOS2015 bands of galaxy M5_211347. Pull equals observed minus model over sigma. Uncertainty: sigma includes the 5 percent flux floor. Comparison: filled points use the posterior-median model. Open squares use the best sample with the fit's own sigma. Total chi-squared 111.5 over 12 bands gives 9.29 per band. Caveat: the spectrum dominates the joint fit, so the fit does not constrain the bands on their own.</figcaption>
</figure>

<figure>
<img loading="lazy" src="/wiki/f/results/rtx-5060-dr2-quiescent-full-spectrum/211347-M5_211347/diagnostics/spectral_chi2.png" alt="M5_211347: spectral pull, binned mean pull squared, cumulative chi-squared">
<figcaption><code>spectral_chi2.png</code> Pull per fitted pixel of the LEGA-C spectrum of galaxy M5_211347. Below it: mean pull squared in 25 Å bins and the cumulative chi-squared fraction against wavelength. Uncertainty: sigma includes the fitted calibration floor of 4.06 percent of the model flux. Comparison: the stored pull versus the pull at the best sample. Shaded bands mark masked pixels. Red points mark pixels with pull beyond 4 sigma. Total chi-squared 3902.2 over 3413 pixels, 6 outlier pixels. Caveat: the fitted floor absorbs model mismatch, so chi-squared near 1 does not prove a good model.</figcaption>
</figure>

<figure>
<img loading="lazy" src="/wiki/f/results/rtx-5060-dr2-quiescent-full-spectrum/211347-M5_211347/diagnostics/sf_timescales.png" alt="M5_211347: cumulative mass formed against lookback time with t10 to t90">
<figcaption><code>sf_timescales.png</code> Fraction of the final stellar mass of galaxy M5_211347 formed earlier than each lookback time. The line is the posterior median. The band is the 16-84 percent range over 400 draws. Comparison: points mark t10 to t90 with 16-84 percent (thick) and 2.5-97.5 percent (thin) intervals versus the universe age. t50 is 2.96 Gyr with a 16-84 percent range of 2.93 to 3.05 Gyr. Caveat: the 7-bin star-formation history model quantises these times to the bin edges.</figcaption>
</figure>

### 211767-M5_211767

| z | S/N | photometry χ²/N | spectrum χ²/N | f_calib | t50 [Gyr] | model |
| --- | --- | --- | --- | --- | --- | --- |
| 0.6674 | 28.5 | 13.01 | 1.066 | 4.19% | 3.02 | [parameters](/wiki/f/results/rtx-5060-dr2-quiescent-full-spectrum/211767-M5_211767/diagnostics/model_parameters.txt) |

Flags:

- photometry chi2/N 13.0 > 3

<figure>
<img loading="lazy" src="/wiki/f/results/rtx-5060-dr2-quiescent-full-spectrum/211767-M5_211767/diagnostics/photometric_chi2.png" alt="M5_211767: photometric pull and chi-squared contribution per band">
<figcaption><code>photometric_chi2.png</code> Pull and chi-squared contribution for the 12 COSMOS2015 bands of galaxy M5_211767. Pull equals observed minus model over sigma. Uncertainty: sigma includes the 5 percent flux floor. Comparison: filled points use the posterior-median model. Open squares use the best sample with the fit's own sigma. Total chi-squared 156.1 over 12 bands gives 13.01 per band. Caveat: the spectrum dominates the joint fit, so the fit does not constrain the bands on their own.</figcaption>
</figure>

<figure>
<img loading="lazy" src="/wiki/f/results/rtx-5060-dr2-quiescent-full-spectrum/211767-M5_211767/diagnostics/spectral_chi2.png" alt="M5_211767: spectral pull, binned mean pull squared, cumulative chi-squared">
<figcaption><code>spectral_chi2.png</code> Pull per fitted pixel of the LEGA-C spectrum of galaxy M5_211767. Below it: mean pull squared in 25 Å bins and the cumulative chi-squared fraction against wavelength. Uncertainty: sigma includes the fitted calibration floor of 4.19 percent of the model flux. Comparison: the stored pull versus the pull at the best sample. Shaded bands mark masked pixels. Red points mark pixels with pull beyond 4 sigma. Total chi-squared 3610.7 over 3386 pixels, 0 outlier pixels. Caveat: the fitted floor absorbs model mismatch, so chi-squared near 1 does not prove a good model.</figcaption>
</figure>

<figure>
<img loading="lazy" src="/wiki/f/results/rtx-5060-dr2-quiescent-full-spectrum/211767-M5_211767/diagnostics/sf_timescales.png" alt="M5_211767: cumulative mass formed against lookback time with t10 to t90">
<figcaption><code>sf_timescales.png</code> Fraction of the final stellar mass of galaxy M5_211767 formed earlier than each lookback time. The line is the posterior median. The band is the 16-84 percent range over 400 draws. Comparison: points mark t10 to t90 with 16-84 percent (thick) and 2.5-97.5 percent (thin) intervals versus the universe age. t50 is 3.02 Gyr with a 16-84 percent range of 3.00 to 3.09 Gyr. Caveat: the 7-bin star-formation history model quantises these times to the bin edges.</figcaption>
</figure>

### 212391-M9_212391

| z | S/N | photometry χ²/N | spectrum χ²/N | f_calib | t50 [Gyr] | model |
| --- | --- | --- | --- | --- | --- | --- |
| 0.7263 | 19.6 | 2.45 | 1.109 | 3.90% | 2.97 | [parameters](/wiki/f/results/rtx-5060-dr2-quiescent-full-spectrum/212391-M9_212391/diagnostics/model_parameters.txt) |

Flags:

- 4 pixels with |pull| > 4

<figure>
<img loading="lazy" src="/wiki/f/results/rtx-5060-dr2-quiescent-full-spectrum/212391-M9_212391/diagnostics/photometric_chi2.png" alt="M9_212391: photometric pull and chi-squared contribution per band">
<figcaption><code>photometric_chi2.png</code> Pull and chi-squared contribution for the 12 COSMOS2015 bands of galaxy M9_212391. Pull equals observed minus model over sigma. Uncertainty: sigma includes the 5 percent flux floor. Comparison: filled points use the posterior-median model. Open squares use the best sample with the fit's own sigma. Total chi-squared 29.4 over 12 bands gives 2.45 per band. Caveat: the spectrum dominates the joint fit, so the fit does not constrain the bands on their own.</figcaption>
</figure>

<figure>
<img loading="lazy" src="/wiki/f/results/rtx-5060-dr2-quiescent-full-spectrum/212391-M9_212391/diagnostics/spectral_chi2.png" alt="M9_212391: spectral pull, binned mean pull squared, cumulative chi-squared">
<figcaption><code>spectral_chi2.png</code> Pull per fitted pixel of the LEGA-C spectrum of galaxy M9_212391. Below it: mean pull squared in 25 Å bins and the cumulative chi-squared fraction against wavelength. Uncertainty: sigma includes the fitted calibration floor of 3.90 percent of the model flux. Comparison: the stored pull versus the pull at the best sample. Shaded bands mark masked pixels. Red points mark pixels with pull beyond 4 sigma. Total chi-squared 3944.8 over 3557 pixels, 4 outlier pixels. Caveat: the fitted floor absorbs model mismatch, so chi-squared near 1 does not prove a good model.</figcaption>
</figure>

<figure>
<img loading="lazy" src="/wiki/f/results/rtx-5060-dr2-quiescent-full-spectrum/212391-M9_212391/diagnostics/sf_timescales.png" alt="M9_212391: cumulative mass formed against lookback time with t10 to t90">
<figcaption><code>sf_timescales.png</code> Fraction of the final stellar mass of galaxy M9_212391 formed earlier than each lookback time. The line is the posterior median. The band is the 16-84 percent range over 400 draws. Comparison: points mark t10 to t90 with 16-84 percent (thick) and 2.5-97.5 percent (thin) intervals versus the universe age. t50 is 2.97 Gyr with a 16-84 percent range of 2.90 to 3.01 Gyr. Caveat: the 7-bin star-formation history model quantises these times to the bin edges.</figcaption>
</figure>

### 212718-M11_212718

| z | S/N | photometry χ²/N | spectrum χ²/N | f_calib | t50 [Gyr] | model |
| --- | --- | --- | --- | --- | --- | --- |
| 0.8898 | 11.5 | 10.58 | 1.110 | 5.40% | 4.63 | [parameters](/wiki/f/results/rtx-5060-dr2-quiescent-full-spectrum/212718-M11_212718/diagnostics/model_parameters.txt) |

Flags:

- photometry chi2/N 10.6 > 3

<figure>
<img loading="lazy" src="/wiki/f/results/rtx-5060-dr2-quiescent-full-spectrum/212718-M11_212718/diagnostics/photometric_chi2.png" alt="M11_212718: photometric pull and chi-squared contribution per band">
<figcaption><code>photometric_chi2.png</code> Pull and chi-squared contribution for the 12 COSMOS2015 bands of galaxy M11_212718. Pull equals observed minus model over sigma. Uncertainty: sigma includes the 5 percent flux floor. Comparison: filled points use the posterior-median model. Open squares use the best sample with the fit's own sigma. Total chi-squared 126.9 over 12 bands gives 10.58 per band. Caveat: the spectrum dominates the joint fit, so the fit does not constrain the bands on their own.</figcaption>
</figure>

<figure>
<img loading="lazy" src="/wiki/f/results/rtx-5060-dr2-quiescent-full-spectrum/212718-M11_212718/diagnostics/spectral_chi2.png" alt="M11_212718: spectral pull, binned mean pull squared, cumulative chi-squared">
<figcaption><code>spectral_chi2.png</code> Pull per fitted pixel of the LEGA-C spectrum of galaxy M11_212718. Below it: mean pull squared in 25 Å bins and the cumulative chi-squared fraction against wavelength. Uncertainty: sigma includes the fitted calibration floor of 5.40 percent of the model flux. Comparison: the stored pull versus the pull at the best sample. Shaded bands mark masked pixels. Red points mark pixels with pull beyond 4 sigma. Total chi-squared 4212.2 over 3794 pixels, 0 outlier pixels. Caveat: the fitted floor absorbs model mismatch, so chi-squared near 1 does not prove a good model.</figcaption>
</figure>

<figure>
<img loading="lazy" src="/wiki/f/results/rtx-5060-dr2-quiescent-full-spectrum/212718-M11_212718/diagnostics/sf_timescales.png" alt="M11_212718: cumulative mass formed against lookback time with t10 to t90">
<figcaption><code>sf_timescales.png</code> Fraction of the final stellar mass of galaxy M11_212718 formed earlier than each lookback time. The line is the posterior median. The band is the 16-84 percent range over 400 draws. Comparison: points mark t10 to t90 with 16-84 percent (thick) and 2.5-97.5 percent (thin) intervals versus the universe age. t50 is 4.63 Gyr with a 16-84 percent range of 4.47 to 5.06 Gyr. Caveat: the 7-bin star-formation history model quantises these times to the bin edges.</figcaption>
</figure>

### 213004-M11_213004

| z | S/N | photometry χ²/N | spectrum χ²/N | f_calib | t50 [Gyr] | model |
| --- | --- | --- | --- | --- | --- | --- |
| 0.7465 | 39.4 | 18.37 | 1.125 | 4.57% | 3.02 | [parameters](/wiki/f/results/rtx-5060-dr2-quiescent-full-spectrum/213004-M11_213004/diagnostics/model_parameters.txt) |

Flags:

- photometry chi2/N 18.4 > 3
- 10 pixels with |pull| > 4

<figure>
<img loading="lazy" src="/wiki/f/results/rtx-5060-dr2-quiescent-full-spectrum/213004-M11_213004/diagnostics/photometric_chi2.png" alt="M11_213004: photometric pull and chi-squared contribution per band">
<figcaption><code>photometric_chi2.png</code> Pull and chi-squared contribution for the 12 COSMOS2015 bands of galaxy M11_213004. Pull equals observed minus model over sigma. Uncertainty: sigma includes the 5 percent flux floor. Comparison: filled points use the posterior-median model. Open squares use the best sample with the fit's own sigma. Total chi-squared 220.5 over 12 bands gives 18.37 per band. Caveat: the spectrum dominates the joint fit, so the fit does not constrain the bands on their own.</figcaption>
</figure>

<figure>
<img loading="lazy" src="/wiki/f/results/rtx-5060-dr2-quiescent-full-spectrum/213004-M11_213004/diagnostics/spectral_chi2.png" alt="M11_213004: spectral pull, binned mean pull squared, cumulative chi-squared">
<figcaption><code>spectral_chi2.png</code> Pull per fitted pixel of the LEGA-C spectrum of galaxy M11_213004. Below it: mean pull squared in 25 Å bins and the cumulative chi-squared fraction against wavelength. Uncertainty: sigma includes the fitted calibration floor of 4.57 percent of the model flux. Comparison: the stored pull versus the pull at the best sample. Shaded bands mark masked pixels. Red points mark pixels with pull beyond 4 sigma. Total chi-squared 3869.6 over 3439 pixels, 10 outlier pixels. Caveat: the fitted floor absorbs model mismatch, so chi-squared near 1 does not prove a good model.</figcaption>
</figure>

<figure>
<img loading="lazy" src="/wiki/f/results/rtx-5060-dr2-quiescent-full-spectrum/213004-M11_213004/diagnostics/sf_timescales.png" alt="M11_213004: cumulative mass formed against lookback time with t10 to t90">
<figcaption><code>sf_timescales.png</code> Fraction of the final stellar mass of galaxy M11_213004 formed earlier than each lookback time. The line is the posterior median. The band is the 16-84 percent range over 400 draws. Comparison: points mark t10 to t90 with 16-84 percent (thick) and 2.5-97.5 percent (thin) intervals versus the universe age. t50 is 3.02 Gyr with a 16-84 percent range of 3.00 to 3.10 Gyr. Caveat: the 7-bin star-formation history model quantises these times to the bin edges.</figcaption>
</figure>

### 213587-M9_213587

| z | S/N | photometry χ²/N | spectrum χ²/N | f_calib | t50 [Gyr] | model |
| --- | --- | --- | --- | --- | --- | --- |
| 0.8900 | 27.1 | 10.11 | 1.101 | 4.06% | 3.01 | [parameters](/wiki/f/results/rtx-5060-dr2-quiescent-full-spectrum/213587-M9_213587/diagnostics/model_parameters.txt) |

Flags:

- photometry chi2/N 10.1 > 3
- 6 pixels with |pull| > 4

<figure>
<img loading="lazy" src="/wiki/f/results/rtx-5060-dr2-quiescent-full-spectrum/213587-M9_213587/diagnostics/photometric_chi2.png" alt="M9_213587: photometric pull and chi-squared contribution per band">
<figcaption><code>photometric_chi2.png</code> Pull and chi-squared contribution for the 12 COSMOS2015 bands of galaxy M9_213587. Pull equals observed minus model over sigma. Uncertainty: sigma includes the 5 percent flux floor. Comparison: filled points use the posterior-median model. Open squares use the best sample with the fit's own sigma. Total chi-squared 121.3 over 12 bands gives 10.11 per band. Caveat: the spectrum dominates the joint fit, so the fit does not constrain the bands on their own.</figcaption>
</figure>

<figure>
<img loading="lazy" src="/wiki/f/results/rtx-5060-dr2-quiescent-full-spectrum/213587-M9_213587/diagnostics/spectral_chi2.png" alt="M9_213587: spectral pull, binned mean pull squared, cumulative chi-squared">
<figcaption><code>spectral_chi2.png</code> Pull per fitted pixel of the LEGA-C spectrum of galaxy M9_213587. Below it: mean pull squared in 25 Å bins and the cumulative chi-squared fraction against wavelength. Uncertainty: sigma includes the fitted calibration floor of 4.06 percent of the model flux. Comparison: the stored pull versus the pull at the best sample. Shaded bands mark masked pixels. Red points mark pixels with pull beyond 4 sigma. Total chi-squared 4115.5 over 3738 pixels, 6 outlier pixels. Caveat: the fitted floor absorbs model mismatch, so chi-squared near 1 does not prove a good model.</figcaption>
</figure>

<figure>
<img loading="lazy" src="/wiki/f/results/rtx-5060-dr2-quiescent-full-spectrum/213587-M9_213587/diagnostics/sf_timescales.png" alt="M9_213587: cumulative mass formed against lookback time with t10 to t90">
<figcaption><code>sf_timescales.png</code> Fraction of the final stellar mass of galaxy M9_213587 formed earlier than each lookback time. The line is the posterior median. The band is the 16-84 percent range over 400 draws. Comparison: points mark t10 to t90 with 16-84 percent (thick) and 2.5-97.5 percent (thin) intervals versus the universe age. t50 is 3.01 Gyr with a 16-84 percent range of 3.00 to 3.05 Gyr. Caveat: the 7-bin star-formation history model quantises these times to the bin edges.</figcaption>
</figure>

### 213772-M10_213772

| z | S/N | photometry χ²/N | spectrum χ²/N | f_calib | t50 [Gyr] | model |
| --- | --- | --- | --- | --- | --- | --- |
| 0.7004 | 40.9 | 7.96 | 1.028 | 4.86% | 5.96 | [parameters](/wiki/f/results/rtx-5060-dr2-quiescent-full-spectrum/213772-M10_213772/diagnostics/model_parameters.txt) |

Flags:

- photometry chi2/N 8.0 > 3
- 12 pixels with |pull| > 4

<figure>
<img loading="lazy" src="/wiki/f/results/rtx-5060-dr2-quiescent-full-spectrum/213772-M10_213772/diagnostics/photometric_chi2.png" alt="M10_213772: photometric pull and chi-squared contribution per band">
<figcaption><code>photometric_chi2.png</code> Pull and chi-squared contribution for the 12 COSMOS2015 bands of galaxy M10_213772. Pull equals observed minus model over sigma. Uncertainty: sigma includes the 5 percent flux floor. Comparison: filled points use the posterior-median model. Open squares use the best sample with the fit's own sigma. Total chi-squared 95.5 over 12 bands gives 7.96 per band. Caveat: the spectrum dominates the joint fit, so the fit does not constrain the bands on their own.</figcaption>
</figure>

<figure>
<img loading="lazy" src="/wiki/f/results/rtx-5060-dr2-quiescent-full-spectrum/213772-M10_213772/diagnostics/spectral_chi2.png" alt="M10_213772: spectral pull, binned mean pull squared, cumulative chi-squared">
<figcaption><code>spectral_chi2.png</code> Pull per fitted pixel of the LEGA-C spectrum of galaxy M10_213772. Below it: mean pull squared in 25 Å bins and the cumulative chi-squared fraction against wavelength. Uncertainty: sigma includes the fitted calibration floor of 4.86 percent of the model flux. Comparison: the stored pull versus the pull at the best sample. Shaded bands mark masked pixels. Red points mark pixels with pull beyond 4 sigma. Total chi-squared 3664.8 over 3565 pixels, 12 outlier pixels. Caveat: the fitted floor absorbs model mismatch, so chi-squared near 1 does not prove a good model.</figcaption>
</figure>

<figure>
<img loading="lazy" src="/wiki/f/results/rtx-5060-dr2-quiescent-full-spectrum/213772-M10_213772/diagnostics/sf_timescales.png" alt="M10_213772: cumulative mass formed against lookback time with t10 to t90">
<figcaption><code>sf_timescales.png</code> Fraction of the final stellar mass of galaxy M10_213772 formed earlier than each lookback time. The line is the posterior median. The band is the 16-84 percent range over 400 draws. Comparison: points mark t10 to t90 with 16-84 percent (thick) and 2.5-97.5 percent (thin) intervals versus the universe age. t50 is 5.96 Gyr with a 16-84 percent range of 5.76 to 6.02 Gyr. Caveat: the 7-bin star-formation history model quantises these times to the bin edges.</figcaption>
</figure>

### 214296-M11_214296

| z | S/N | photometry χ²/N | spectrum χ²/N | f_calib | t50 [Gyr] | model |
| --- | --- | --- | --- | --- | --- | --- |
| 0.6797 | 19.1 | 13.10 | 1.122 | 4.69% | 2.27 | [parameters](/wiki/f/results/rtx-5060-dr2-quiescent-full-spectrum/214296-M11_214296/diagnostics/model_parameters.txt) |

Flags:

- photometry chi2/N 13.1 > 3
- 5 pixels with |pull| > 4

<figure>
<img loading="lazy" src="/wiki/f/results/rtx-5060-dr2-quiescent-full-spectrum/214296-M11_214296/diagnostics/photometric_chi2.png" alt="M11_214296: photometric pull and chi-squared contribution per band">
<figcaption><code>photometric_chi2.png</code> Pull and chi-squared contribution for the 12 COSMOS2015 bands of galaxy M11_214296. Pull equals observed minus model over sigma. Uncertainty: sigma includes the 5 percent flux floor. Comparison: filled points use the posterior-median model. Open squares use the best sample with the fit's own sigma. Total chi-squared 157.2 over 12 bands gives 13.10 per band. Caveat: the spectrum dominates the joint fit, so the fit does not constrain the bands on their own.</figcaption>
</figure>

<figure>
<img loading="lazy" src="/wiki/f/results/rtx-5060-dr2-quiescent-full-spectrum/214296-M11_214296/diagnostics/spectral_chi2.png" alt="M11_214296: spectral pull, binned mean pull squared, cumulative chi-squared">
<figcaption><code>spectral_chi2.png</code> Pull per fitted pixel of the LEGA-C spectrum of galaxy M11_214296. Below it: mean pull squared in 25 Å bins and the cumulative chi-squared fraction against wavelength. Uncertainty: sigma includes the fitted calibration floor of 4.69 percent of the model flux. Comparison: the stored pull versus the pull at the best sample. Shaded bands mark masked pixels. Red points mark pixels with pull beyond 4 sigma. Total chi-squared 3844.3 over 3427 pixels, 5 outlier pixels. Caveat: the fitted floor absorbs model mismatch, so chi-squared near 1 does not prove a good model.</figcaption>
</figure>

<figure>
<img loading="lazy" src="/wiki/f/results/rtx-5060-dr2-quiescent-full-spectrum/214296-M11_214296/diagnostics/sf_timescales.png" alt="M11_214296: cumulative mass formed against lookback time with t10 to t90">
<figcaption><code>sf_timescales.png</code> Fraction of the final stellar mass of galaxy M11_214296 formed earlier than each lookback time. The line is the posterior median. The band is the 16-84 percent range over 400 draws. Comparison: points mark t10 to t90 with 16-84 percent (thick) and 2.5-97.5 percent (thin) intervals versus the universe age. t50 is 2.27 Gyr with a 16-84 percent range of 2.19 to 2.37 Gyr. Caveat: the 7-bin star-formation history model quantises these times to the bin edges.</figcaption>
</figure>

### 214430-M11_214430

| z | S/N | photometry χ²/N | spectrum χ²/N | f_calib | t50 [Gyr] | model |
| --- | --- | --- | --- | --- | --- | --- |
| 0.8911 | 15.2 | 17.47 | 1.162 | 5.23% | 4.09 | [parameters](/wiki/f/results/rtx-5060-dr2-quiescent-full-spectrum/214430-M11_214430/diagnostics/model_parameters.txt) |

Flags:

- photometry chi2/N 17.5 > 3
- 4 pixels with |pull| > 4

<figure>
<img loading="lazy" src="/wiki/f/results/rtx-5060-dr2-quiescent-full-spectrum/214430-M11_214430/diagnostics/photometric_chi2.png" alt="M11_214430: photometric pull and chi-squared contribution per band">
<figcaption><code>photometric_chi2.png</code> Pull and chi-squared contribution for the 12 COSMOS2015 bands of galaxy M11_214430. Pull equals observed minus model over sigma. Uncertainty: sigma includes the 5 percent flux floor. Comparison: filled points use the posterior-median model. Open squares use the best sample with the fit's own sigma. Total chi-squared 209.7 over 12 bands gives 17.47 per band. Caveat: the spectrum dominates the joint fit, so the fit does not constrain the bands on their own.</figcaption>
</figure>

<figure>
<img loading="lazy" src="/wiki/f/results/rtx-5060-dr2-quiescent-full-spectrum/214430-M11_214430/diagnostics/spectral_chi2.png" alt="M11_214430: spectral pull, binned mean pull squared, cumulative chi-squared">
<figcaption><code>spectral_chi2.png</code> Pull per fitted pixel of the LEGA-C spectrum of galaxy M11_214430. Below it: mean pull squared in 25 Å bins and the cumulative chi-squared fraction against wavelength. Uncertainty: sigma includes the fitted calibration floor of 5.23 percent of the model flux. Comparison: the stored pull versus the pull at the best sample. Shaded bands mark masked pixels. Red points mark pixels with pull beyond 4 sigma. Total chi-squared 4425.8 over 3810 pixels, 4 outlier pixels. Caveat: the fitted floor absorbs model mismatch, so chi-squared near 1 does not prove a good model.</figcaption>
</figure>

<figure>
<img loading="lazy" src="/wiki/f/results/rtx-5060-dr2-quiescent-full-spectrum/214430-M11_214430/diagnostics/sf_timescales.png" alt="M11_214430: cumulative mass formed against lookback time with t10 to t90">
<figcaption><code>sf_timescales.png</code> Fraction of the final stellar mass of galaxy M11_214430 formed earlier than each lookback time. The line is the posterior median. The band is the 16-84 percent range over 400 draws. Comparison: points mark t10 to t90 with 16-84 percent (thick) and 2.5-97.5 percent (thin) intervals versus the universe age. t50 is 4.09 Gyr with a 16-84 percent range of 3.92 to 4.25 Gyr. Caveat: the 7-bin star-formation history model quantises these times to the bin edges.</figcaption>
</figure>

### 214899-M9_214899

| z | S/N | photometry χ²/N | spectrum χ²/N | f_calib | t50 [Gyr] | model |
| --- | --- | --- | --- | --- | --- | --- |
| 0.6751 | 18.8 | 2.03 | 1.084 | 3.92% | 2.92 | [parameters](/wiki/f/results/rtx-5060-dr2-quiescent-full-spectrum/214899-M9_214899/diagnostics/model_parameters.txt) |

Flags:

- 3 pixels with |pull| > 4

<figure>
<img loading="lazy" src="/wiki/f/results/rtx-5060-dr2-quiescent-full-spectrum/214899-M9_214899/diagnostics/photometric_chi2.png" alt="M9_214899: photometric pull and chi-squared contribution per band">
<figcaption><code>photometric_chi2.png</code> Pull and chi-squared contribution for the 12 COSMOS2015 bands of galaxy M9_214899. Pull equals observed minus model over sigma. Uncertainty: sigma includes the 5 percent flux floor. Comparison: filled points use the posterior-median model. Open squares use the best sample with the fit's own sigma. Total chi-squared 24.3 over 12 bands gives 2.03 per band. Caveat: the spectrum dominates the joint fit, so the fit does not constrain the bands on their own.</figcaption>
</figure>

<figure>
<img loading="lazy" src="/wiki/f/results/rtx-5060-dr2-quiescent-full-spectrum/214899-M9_214899/diagnostics/spectral_chi2.png" alt="M9_214899: spectral pull, binned mean pull squared, cumulative chi-squared">
<figcaption><code>spectral_chi2.png</code> Pull per fitted pixel of the LEGA-C spectrum of galaxy M9_214899. Below it: mean pull squared in 25 Å bins and the cumulative chi-squared fraction against wavelength. Uncertainty: sigma includes the fitted calibration floor of 3.92 percent of the model flux. Comparison: the stored pull versus the pull at the best sample. Shaded bands mark masked pixels. Red points mark pixels with pull beyond 4 sigma. Total chi-squared 3784.9 over 3493 pixels, 3 outlier pixels. Caveat: the fitted floor absorbs model mismatch, so chi-squared near 1 does not prove a good model.</figcaption>
</figure>

<figure>
<img loading="lazy" src="/wiki/f/results/rtx-5060-dr2-quiescent-full-spectrum/214899-M9_214899/diagnostics/sf_timescales.png" alt="M9_214899: cumulative mass formed against lookback time with t10 to t90">
<figcaption><code>sf_timescales.png</code> Fraction of the final stellar mass of galaxy M9_214899 formed earlier than each lookback time. The line is the posterior median. The band is the 16-84 percent range over 400 draws. Comparison: points mark t10 to t90 with 16-84 percent (thick) and 2.5-97.5 percent (thin) intervals versus the universe age. t50 is 2.92 Gyr with a 16-84 percent range of 2.85 to 3.02 Gyr. Caveat: the 7-bin star-formation history model quantises these times to the bin edges.</figcaption>
</figure>

### 215519-M10_215519

| z | S/N | photometry χ²/N | spectrum χ²/N | f_calib | t50 [Gyr] | model |
| --- | --- | --- | --- | --- | --- | --- |
| 0.6146 | 17.7 | 1.97 | 1.023 | 4.44% | 6.34 | [parameters](/wiki/f/results/rtx-5060-dr2-quiescent-full-spectrum/215519-M10_215519/diagnostics/model_parameters.txt) |

Flags:

- 6 pixels with |pull| > 4

<figure>
<img loading="lazy" src="/wiki/f/results/rtx-5060-dr2-quiescent-full-spectrum/215519-M10_215519/diagnostics/photometric_chi2.png" alt="M10_215519: photometric pull and chi-squared contribution per band">
<figcaption><code>photometric_chi2.png</code> Pull and chi-squared contribution for the 12 COSMOS2015 bands of galaxy M10_215519. Pull equals observed minus model over sigma. Uncertainty: sigma includes the 5 percent flux floor. Comparison: filled points use the posterior-median model. Open squares use the best sample with the fit's own sigma. Total chi-squared 23.6 over 12 bands gives 1.97 per band. Caveat: the spectrum dominates the joint fit, so the fit does not constrain the bands on their own.</figcaption>
</figure>

<figure>
<img loading="lazy" src="/wiki/f/results/rtx-5060-dr2-quiescent-full-spectrum/215519-M10_215519/diagnostics/spectral_chi2.png" alt="M10_215519: spectral pull, binned mean pull squared, cumulative chi-squared">
<figcaption><code>spectral_chi2.png</code> Pull per fitted pixel of the LEGA-C spectrum of galaxy M10_215519. Below it: mean pull squared in 25 Å bins and the cumulative chi-squared fraction against wavelength. Uncertainty: sigma includes the fitted calibration floor of 4.44 percent of the model flux. Comparison: the stored pull versus the pull at the best sample. Shaded bands mark masked pixels. Red points mark pixels with pull beyond 4 sigma. Total chi-squared 3658.0 over 3575 pixels, 6 outlier pixels. Caveat: the fitted floor absorbs model mismatch, so chi-squared near 1 does not prove a good model.</figcaption>
</figure>

<figure>
<img loading="lazy" src="/wiki/f/results/rtx-5060-dr2-quiescent-full-spectrum/215519-M10_215519/diagnostics/sf_timescales.png" alt="M10_215519: cumulative mass formed against lookback time with t10 to t90">
<figcaption><code>sf_timescales.png</code> Fraction of the final stellar mass of galaxy M10_215519 formed earlier than each lookback time. The line is the posterior median. The band is the 16-84 percent range over 400 draws. Comparison: points mark t10 to t90 with 16-84 percent (thick) and 2.5-97.5 percent (thin) intervals versus the universe age. t50 is 6.34 Gyr with a 16-84 percent range of 6.22 to 6.37 Gyr. Caveat: the 7-bin star-formation history model quantises these times to the bin edges.</figcaption>
</figure>

### 215585-M11_215585

| z | S/N | photometry χ²/N | spectrum χ²/N | f_calib | t50 [Gyr] | model |
| --- | --- | --- | --- | --- | --- | --- |
| 0.7487 | 35.6 | 17.50 | 1.145 | 4.65% | 4.73 | [parameters](/wiki/f/results/rtx-5060-dr2-quiescent-full-spectrum/215585-M11_215585/diagnostics/model_parameters.txt) |

Flags:

- photometry chi2/N 17.5 > 3
- 5 pixels with |pull| > 4

<figure>
<img loading="lazy" src="/wiki/f/results/rtx-5060-dr2-quiescent-full-spectrum/215585-M11_215585/diagnostics/photometric_chi2.png" alt="M11_215585: photometric pull and chi-squared contribution per band">
<figcaption><code>photometric_chi2.png</code> Pull and chi-squared contribution for the 12 COSMOS2015 bands of galaxy M11_215585. Pull equals observed minus model over sigma. Uncertainty: sigma includes the 5 percent flux floor. Comparison: filled points use the posterior-median model. Open squares use the best sample with the fit's own sigma. Total chi-squared 210.0 over 12 bands gives 17.50 per band. Caveat: the spectrum dominates the joint fit, so the fit does not constrain the bands on their own.</figcaption>
</figure>

<figure>
<img loading="lazy" src="/wiki/f/results/rtx-5060-dr2-quiescent-full-spectrum/215585-M11_215585/diagnostics/spectral_chi2.png" alt="M11_215585: spectral pull, binned mean pull squared, cumulative chi-squared">
<figcaption><code>spectral_chi2.png</code> Pull per fitted pixel of the LEGA-C spectrum of galaxy M11_215585. Below it: mean pull squared in 25 Å bins and the cumulative chi-squared fraction against wavelength. Uncertainty: sigma includes the fitted calibration floor of 4.65 percent of the model flux. Comparison: the stored pull versus the pull at the best sample. Shaded bands mark masked pixels. Red points mark pixels with pull beyond 4 sigma. Total chi-squared 4303.0 over 3757 pixels, 5 outlier pixels. Caveat: the fitted floor absorbs model mismatch, so chi-squared near 1 does not prove a good model.</figcaption>
</figure>

<figure>
<img loading="lazy" src="/wiki/f/results/rtx-5060-dr2-quiescent-full-spectrum/215585-M11_215585/diagnostics/sf_timescales.png" alt="M11_215585: cumulative mass formed against lookback time with t10 to t90">
<figcaption><code>sf_timescales.png</code> Fraction of the final stellar mass of galaxy M11_215585 formed earlier than each lookback time. The line is the posterior median. The band is the 16-84 percent range over 400 draws. Comparison: points mark t10 to t90 with 16-84 percent (thick) and 2.5-97.5 percent (thin) intervals versus the universe age. t50 is 4.73 Gyr with a 16-84 percent range of 4.62 to 4.84 Gyr. Caveat: the 7-bin star-formation history model quantises these times to the bin edges.</figcaption>
</figure>

### 216730-M10_216730

| z | S/N | photometry χ²/N | spectrum χ²/N | f_calib | t50 [Gyr] | model |
| --- | --- | --- | --- | --- | --- | --- |
| 0.8937 | 36.7 | 3.34 | 1.039 | 6.22% | 1.65 | [parameters](/wiki/f/results/rtx-5060-dr2-quiescent-full-spectrum/216730-M10_216730/diagnostics/model_parameters.txt) |

Flags:

- photometry chi2/N 3.3 > 3
- 14 pixels with |pull| > 4

<figure>
<img loading="lazy" src="/wiki/f/results/rtx-5060-dr2-quiescent-full-spectrum/216730-M10_216730/diagnostics/photometric_chi2.png" alt="M10_216730: photometric pull and chi-squared contribution per band">
<figcaption><code>photometric_chi2.png</code> Pull and chi-squared contribution for the 12 COSMOS2015 bands of galaxy M10_216730. Pull equals observed minus model over sigma. Uncertainty: sigma includes the 5 percent flux floor. Comparison: filled points use the posterior-median model. Open squares use the best sample with the fit's own sigma. Total chi-squared 40.1 over 12 bands gives 3.34 per band. Caveat: the spectrum dominates the joint fit, so the fit does not constrain the bands on their own.</figcaption>
</figure>

<figure>
<img loading="lazy" src="/wiki/f/results/rtx-5060-dr2-quiescent-full-spectrum/216730-M10_216730/diagnostics/spectral_chi2.png" alt="M10_216730: spectral pull, binned mean pull squared, cumulative chi-squared">
<figcaption><code>spectral_chi2.png</code> Pull per fitted pixel of the LEGA-C spectrum of galaxy M10_216730. Below it: mean pull squared in 25 Å bins and the cumulative chi-squared fraction against wavelength. Uncertainty: sigma includes the fitted calibration floor of 6.22 percent of the model flux. Comparison: the stored pull versus the pull at the best sample. Shaded bands mark masked pixels. Red points mark pixels with pull beyond 4 sigma. Total chi-squared 3550.6 over 3418 pixels, 14 outlier pixels. Caveat: the fitted floor absorbs model mismatch, so chi-squared near 1 does not prove a good model.</figcaption>
</figure>

<figure>
<img loading="lazy" src="/wiki/f/results/rtx-5060-dr2-quiescent-full-spectrum/216730-M10_216730/diagnostics/sf_timescales.png" alt="M10_216730: cumulative mass formed against lookback time with t10 to t90">
<figcaption><code>sf_timescales.png</code> Fraction of the final stellar mass of galaxy M10_216730 formed earlier than each lookback time. The line is the posterior median. The band is the 16-84 percent range over 400 draws. Comparison: points mark t10 to t90 with 16-84 percent (thick) and 2.5-97.5 percent (thin) intervals versus the universe age. t50 is 1.65 Gyr with a 16-84 percent range of 1.63 to 1.65 Gyr. Caveat: the 7-bin star-formation history model quantises these times to the bin edges.</figcaption>
</figure>

### 216899-M11_216899

| z | S/N | photometry χ²/N | spectrum χ²/N | f_calib | t50 [Gyr] | model |
| --- | --- | --- | --- | --- | --- | --- |
| 0.6978 | 21.1 | 3.75 | 1.713 | 9.99% | 4.58 | [parameters](/wiki/f/results/rtx-5060-dr2-quiescent-full-spectrum/216899-M11_216899/diagnostics/model_parameters.txt) |

Flags:

- photometry chi2/N 3.7 > 3
- spectrum chi2/N 1.71 > 1.5
- calibration floor at prior bound (10.0% of 10%)
- 12 pixels with |pull| > 4

<figure>
<img loading="lazy" src="/wiki/f/results/rtx-5060-dr2-quiescent-full-spectrum/216899-M11_216899/diagnostics/photometric_chi2.png" alt="M11_216899: photometric pull and chi-squared contribution per band">
<figcaption><code>photometric_chi2.png</code> Pull and chi-squared contribution for the 12 COSMOS2015 bands of galaxy M11_216899. Pull equals observed minus model over sigma. Uncertainty: sigma includes the 5 percent flux floor. Comparison: filled points use the posterior-median model. Open squares use the best sample with the fit's own sigma. Total chi-squared 45.0 over 12 bands gives 3.75 per band. Caveat: the spectrum dominates the joint fit, so the fit does not constrain the bands on their own.</figcaption>
</figure>

<figure>
<img loading="lazy" src="/wiki/f/results/rtx-5060-dr2-quiescent-full-spectrum/216899-M11_216899/diagnostics/spectral_chi2.png" alt="M11_216899: spectral pull, binned mean pull squared, cumulative chi-squared">
<figcaption><code>spectral_chi2.png</code> Pull per fitted pixel of the LEGA-C spectrum of galaxy M11_216899. Below it: mean pull squared in 25 Å bins and the cumulative chi-squared fraction against wavelength. Uncertainty: sigma includes the fitted calibration floor of 9.99 percent of the model flux. Comparison: the stored pull versus the pull at the best sample. Shaded bands mark masked pixels. Red points mark pixels with pull beyond 4 sigma. Total chi-squared 5874.2 over 3430 pixels, 12 outlier pixels. Caveat: the fitted floor absorbs model mismatch, so chi-squared near 1 does not prove a good model.</figcaption>
</figure>

<figure>
<img loading="lazy" src="/wiki/f/results/rtx-5060-dr2-quiescent-full-spectrum/216899-M11_216899/diagnostics/sf_timescales.png" alt="M11_216899: cumulative mass formed against lookback time with t10 to t90">
<figcaption><code>sf_timescales.png</code> Fraction of the final stellar mass of galaxy M11_216899 formed earlier than each lookback time. The line is the posterior median. The band is the 16-84 percent range over 400 draws. Comparison: points mark t10 to t90 with 16-84 percent (thick) and 2.5-97.5 percent (thin) intervals versus the universe age. t50 is 4.58 Gyr with a 16-84 percent range of 4.21 to 5.08 Gyr. Caveat: the 7-bin star-formation history model quantises these times to the bin edges.</figcaption>
</figure>

### 217020-M10_217020

| z | S/N | photometry χ²/N | spectrum χ²/N | f_calib | t50 [Gyr] | model |
| --- | --- | --- | --- | --- | --- | --- |
| 0.8934 | 12.8 | 8.48 | 1.025 | 6.80% | 2.69 | [parameters](/wiki/f/results/rtx-5060-dr2-quiescent-full-spectrum/217020-M10_217020/diagnostics/model_parameters.txt) |

Flags:

- photometry chi2/N 8.5 > 3
- 6 pixels with |pull| > 4

<figure>
<img loading="lazy" src="/wiki/f/results/rtx-5060-dr2-quiescent-full-spectrum/217020-M10_217020/diagnostics/photometric_chi2.png" alt="M10_217020: photometric pull and chi-squared contribution per band">
<figcaption><code>photometric_chi2.png</code> Pull and chi-squared contribution for the 12 COSMOS2015 bands of galaxy M10_217020. Pull equals observed minus model over sigma. Uncertainty: sigma includes the 5 percent flux floor. Comparison: filled points use the posterior-median model. Open squares use the best sample with the fit's own sigma. Total chi-squared 101.8 over 12 bands gives 8.48 per band. Caveat: the spectrum dominates the joint fit, so the fit does not constrain the bands on their own.</figcaption>
</figure>

<figure>
<img loading="lazy" src="/wiki/f/results/rtx-5060-dr2-quiescent-full-spectrum/217020-M10_217020/diagnostics/spectral_chi2.png" alt="M10_217020: spectral pull, binned mean pull squared, cumulative chi-squared">
<figcaption><code>spectral_chi2.png</code> Pull per fitted pixel of the LEGA-C spectrum of galaxy M10_217020. Below it: mean pull squared in 25 Å bins and the cumulative chi-squared fraction against wavelength. Uncertainty: sigma includes the fitted calibration floor of 6.80 percent of the model flux. Comparison: the stored pull versus the pull at the best sample. Shaded bands mark masked pixels. Red points mark pixels with pull beyond 4 sigma. Total chi-squared 3528.2 over 3443 pixels, 6 outlier pixels. Caveat: the fitted floor absorbs model mismatch, so chi-squared near 1 does not prove a good model.</figcaption>
</figure>

<figure>
<img loading="lazy" src="/wiki/f/results/rtx-5060-dr2-quiescent-full-spectrum/217020-M10_217020/diagnostics/sf_timescales.png" alt="M10_217020: cumulative mass formed against lookback time with t10 to t90">
<figcaption><code>sf_timescales.png</code> Fraction of the final stellar mass of galaxy M10_217020 formed earlier than each lookback time. The line is the posterior median. The band is the 16-84 percent range over 400 draws. Comparison: points mark t10 to t90 with 16-84 percent (thick) and 2.5-97.5 percent (thin) intervals versus the universe age. t50 is 2.69 Gyr with a 16-84 percent range of 2.63 to 2.80 Gyr. Caveat: the 7-bin star-formation history model quantises these times to the bin edges.</figcaption>
</figure>

### 217564-M11_217564

| z | S/N | photometry χ²/N | spectrum χ²/N | f_calib | t50 [Gyr] | model |
| --- | --- | --- | --- | --- | --- | --- |
| 0.8899 | 3.7 | 11.80 | 1.132 | 9.13% | 2.94 | [parameters](/wiki/f/results/rtx-5060-dr2-quiescent-full-spectrum/217564-M11_217564/diagnostics/model_parameters.txt) |

Flags:

- photometry chi2/N 11.8 > 3
- 2 pixels with |pull| > 4

<figure>
<img loading="lazy" src="/wiki/f/results/rtx-5060-dr2-quiescent-full-spectrum/217564-M11_217564/diagnostics/photometric_chi2.png" alt="M11_217564: photometric pull and chi-squared contribution per band">
<figcaption><code>photometric_chi2.png</code> Pull and chi-squared contribution for the 12 COSMOS2015 bands of galaxy M11_217564. Pull equals observed minus model over sigma. Uncertainty: sigma includes the 5 percent flux floor. Comparison: filled points use the posterior-median model. Open squares use the best sample with the fit's own sigma. Total chi-squared 141.6 over 12 bands gives 11.80 per band. Caveat: the spectrum dominates the joint fit, so the fit does not constrain the bands on their own.</figcaption>
</figure>

<figure>
<img loading="lazy" src="/wiki/f/results/rtx-5060-dr2-quiescent-full-spectrum/217564-M11_217564/diagnostics/spectral_chi2.png" alt="M11_217564: spectral pull, binned mean pull squared, cumulative chi-squared">
<figcaption><code>spectral_chi2.png</code> Pull per fitted pixel of the LEGA-C spectrum of galaxy M11_217564. Below it: mean pull squared in 25 Å bins and the cumulative chi-squared fraction against wavelength. Uncertainty: sigma includes the fitted calibration floor of 9.13 percent of the model flux. Comparison: the stored pull versus the pull at the best sample. Shaded bands mark masked pixels. Red points mark pixels with pull beyond 4 sigma. Total chi-squared 4330.4 over 3827 pixels, 2 outlier pixels. Caveat: the fitted floor absorbs model mismatch, so chi-squared near 1 does not prove a good model.</figcaption>
</figure>

<figure>
<img loading="lazy" src="/wiki/f/results/rtx-5060-dr2-quiescent-full-spectrum/217564-M11_217564/diagnostics/sf_timescales.png" alt="M11_217564: cumulative mass formed against lookback time with t10 to t90">
<figcaption><code>sf_timescales.png</code> Fraction of the final stellar mass of galaxy M11_217564 formed earlier than each lookback time. The line is the posterior median. The band is the 16-84 percent range over 400 draws. Comparison: points mark t10 to t90 with 16-84 percent (thick) and 2.5-97.5 percent (thin) intervals versus the universe age. t50 is 2.94 Gyr with a 16-84 percent range of 2.68 to 3.25 Gyr. Caveat: the 7-bin star-formation history model quantises these times to the bin edges.</figcaption>
</figure>

### 218207-M11_218207

| z | S/N | photometry χ²/N | spectrum χ²/N | f_calib | t50 [Gyr] | model |
| --- | --- | --- | --- | --- | --- | --- |
| 0.6818 | 36.8 | 16.41 | 1.081 | 5.64% | 3.01 | [parameters](/wiki/f/results/rtx-5060-dr2-quiescent-full-spectrum/218207-M11_218207/diagnostics/model_parameters.txt) |

Flags:

- photometry chi2/N 16.4 > 3
- 9 pixels with |pull| > 4

<figure>
<img loading="lazy" src="/wiki/f/results/rtx-5060-dr2-quiescent-full-spectrum/218207-M11_218207/diagnostics/photometric_chi2.png" alt="M11_218207: photometric pull and chi-squared contribution per band">
<figcaption><code>photometric_chi2.png</code> Pull and chi-squared contribution for the 12 COSMOS2015 bands of galaxy M11_218207. Pull equals observed minus model over sigma. Uncertainty: sigma includes the 5 percent flux floor. Comparison: filled points use the posterior-median model. Open squares use the best sample with the fit's own sigma. Total chi-squared 196.9 over 12 bands gives 16.41 per band. Caveat: the spectrum dominates the joint fit, so the fit does not constrain the bands on their own.</figcaption>
</figure>

<figure>
<img loading="lazy" src="/wiki/f/results/rtx-5060-dr2-quiescent-full-spectrum/218207-M11_218207/diagnostics/spectral_chi2.png" alt="M11_218207: spectral pull, binned mean pull squared, cumulative chi-squared">
<figcaption><code>spectral_chi2.png</code> Pull per fitted pixel of the LEGA-C spectrum of galaxy M11_218207. Below it: mean pull squared in 25 Å bins and the cumulative chi-squared fraction against wavelength. Uncertainty: sigma includes the fitted calibration floor of 5.64 percent of the model flux. Comparison: the stored pull versus the pull at the best sample. Shaded bands mark masked pixels. Red points mark pixels with pull beyond 4 sigma. Total chi-squared 3700.9 over 3424 pixels, 9 outlier pixels. Caveat: the fitted floor absorbs model mismatch, so chi-squared near 1 does not prove a good model.</figcaption>
</figure>

<figure>
<img loading="lazy" src="/wiki/f/results/rtx-5060-dr2-quiescent-full-spectrum/218207-M11_218207/diagnostics/sf_timescales.png" alt="M11_218207: cumulative mass formed against lookback time with t10 to t90">
<figcaption><code>sf_timescales.png</code> Fraction of the final stellar mass of galaxy M11_218207 formed earlier than each lookback time. The line is the posterior median. The band is the 16-84 percent range over 400 draws. Comparison: points mark t10 to t90 with 16-84 percent (thick) and 2.5-97.5 percent (thin) intervals versus the universe age. t50 is 3.01 Gyr with a 16-84 percent range of 3.00 to 3.05 Gyr. Caveat: the 7-bin star-formation history model quantises these times to the bin edges.</figcaption>
</figure>

### 218701-M9_218701

| z | S/N | photometry χ²/N | spectrum χ²/N | f_calib | t50 [Gyr] | model |
| --- | --- | --- | --- | --- | --- | --- |
| 0.6953 | 30.7 | 3.01 | 1.120 | 3.43% | 2.60 | [parameters](/wiki/f/results/rtx-5060-dr2-quiescent-full-spectrum/218701-M9_218701/diagnostics/model_parameters.txt) |

Flags:

- photometry chi2/N 3.0 > 3
- 4 pixels with |pull| > 4

<figure>
<img loading="lazy" src="/wiki/f/results/rtx-5060-dr2-quiescent-full-spectrum/218701-M9_218701/diagnostics/photometric_chi2.png" alt="M9_218701: photometric pull and chi-squared contribution per band">
<figcaption><code>photometric_chi2.png</code> Pull and chi-squared contribution for the 12 COSMOS2015 bands of galaxy M9_218701. Pull equals observed minus model over sigma. Uncertainty: sigma includes the 5 percent flux floor. Comparison: filled points use the posterior-median model. Open squares use the best sample with the fit's own sigma. Total chi-squared 36.1 over 12 bands gives 3.01 per band. Caveat: the spectrum dominates the joint fit, so the fit does not constrain the bands on their own.</figcaption>
</figure>

<figure>
<img loading="lazy" src="/wiki/f/results/rtx-5060-dr2-quiescent-full-spectrum/218701-M9_218701/diagnostics/spectral_chi2.png" alt="M9_218701: spectral pull, binned mean pull squared, cumulative chi-squared">
<figcaption><code>spectral_chi2.png</code> Pull per fitted pixel of the LEGA-C spectrum of galaxy M9_218701. Below it: mean pull squared in 25 Å bins and the cumulative chi-squared fraction against wavelength. Uncertainty: sigma includes the fitted calibration floor of 3.43 percent of the model flux. Comparison: the stored pull versus the pull at the best sample. Shaded bands mark masked pixels. Red points mark pixels with pull beyond 4 sigma. Total chi-squared 4008.5 over 3580 pixels, 4 outlier pixels. Caveat: the fitted floor absorbs model mismatch, so chi-squared near 1 does not prove a good model.</figcaption>
</figure>

<figure>
<img loading="lazy" src="/wiki/f/results/rtx-5060-dr2-quiescent-full-spectrum/218701-M9_218701/diagnostics/sf_timescales.png" alt="M9_218701: cumulative mass formed against lookback time with t10 to t90">
<figcaption><code>sf_timescales.png</code> Fraction of the final stellar mass of galaxy M9_218701 formed earlier than each lookback time. The line is the posterior median. The band is the 16-84 percent range over 400 draws. Comparison: points mark t10 to t90 with 16-84 percent (thick) and 2.5-97.5 percent (thin) intervals versus the universe age. t50 is 2.60 Gyr with a 16-84 percent range of 2.55 to 2.67 Gyr. Caveat: the 7-bin star-formation history model quantises these times to the bin edges.</figcaption>
</figure>

### 221163-M11_221163

| z | S/N | photometry χ²/N | spectrum χ²/N | f_calib | t50 [Gyr] | model |
| --- | --- | --- | --- | --- | --- | --- |
| 0.6975 | 34.2 | 22.98 | 1.106 | 4.84% | 3.90 | [parameters](/wiki/f/results/rtx-5060-dr2-quiescent-full-spectrum/221163-M11_221163/diagnostics/model_parameters.txt) |

Flags:

- photometry chi2/N 23.0 > 3
- 4 pixels with |pull| > 4

<figure>
<img loading="lazy" src="/wiki/f/results/rtx-5060-dr2-quiescent-full-spectrum/221163-M11_221163/diagnostics/photometric_chi2.png" alt="M11_221163: photometric pull and chi-squared contribution per band">
<figcaption><code>photometric_chi2.png</code> Pull and chi-squared contribution for the 12 COSMOS2015 bands of galaxy M11_221163. Pull equals observed minus model over sigma. Uncertainty: sigma includes the 5 percent flux floor. Comparison: filled points use the posterior-median model. Open squares use the best sample with the fit's own sigma. Total chi-squared 275.7 over 12 bands gives 22.98 per band. Caveat: the spectrum dominates the joint fit, so the fit does not constrain the bands on their own.</figcaption>
</figure>

<figure>
<img loading="lazy" src="/wiki/f/results/rtx-5060-dr2-quiescent-full-spectrum/221163-M11_221163/diagnostics/spectral_chi2.png" alt="M11_221163: spectral pull, binned mean pull squared, cumulative chi-squared">
<figcaption><code>spectral_chi2.png</code> Pull per fitted pixel of the LEGA-C spectrum of galaxy M11_221163. Below it: mean pull squared in 25 Å bins and the cumulative chi-squared fraction against wavelength. Uncertainty: sigma includes the fitted calibration floor of 4.84 percent of the model flux. Comparison: the stored pull versus the pull at the best sample. Shaded bands mark masked pixels. Red points mark pixels with pull beyond 4 sigma. Total chi-squared 3999.0 over 3615 pixels, 4 outlier pixels. Caveat: the fitted floor absorbs model mismatch, so chi-squared near 1 does not prove a good model.</figcaption>
</figure>

<figure>
<img loading="lazy" src="/wiki/f/results/rtx-5060-dr2-quiescent-full-spectrum/221163-M11_221163/diagnostics/sf_timescales.png" alt="M11_221163: cumulative mass formed against lookback time with t10 to t90">
<figcaption><code>sf_timescales.png</code> Fraction of the final stellar mass of galaxy M11_221163 formed earlier than each lookback time. The line is the posterior median. The band is the 16-84 percent range over 400 draws. Comparison: points mark t10 to t90 with 16-84 percent (thick) and 2.5-97.5 percent (thin) intervals versus the universe age. t50 is 3.90 Gyr with a 16-84 percent range of 3.68 to 4.13 Gyr. Caveat: the 7-bin star-formation history model quantises these times to the bin edges.</figcaption>
</figure>

### 225431-M9_225431

| z | S/N | photometry χ²/N | spectrum χ²/N | f_calib | t50 [Gyr] | model |
| --- | --- | --- | --- | --- | --- | --- |
| 0.7014 | 19.9 | 4.37 | 1.081 | 4.54% | 3.09 | [parameters](/wiki/f/results/rtx-5060-dr2-quiescent-full-spectrum/225431-M9_225431/diagnostics/model_parameters.txt) |

Flags:

- photometry chi2/N 4.4 > 3
- 6 pixels with |pull| > 4

<figure>
<img loading="lazy" src="/wiki/f/results/rtx-5060-dr2-quiescent-full-spectrum/225431-M9_225431/diagnostics/photometric_chi2.png" alt="M9_225431: photometric pull and chi-squared contribution per band">
<figcaption><code>photometric_chi2.png</code> Pull and chi-squared contribution for the 12 COSMOS2015 bands of galaxy M9_225431. Pull equals observed minus model over sigma. Uncertainty: sigma includes the 5 percent flux floor. Comparison: filled points use the posterior-median model. Open squares use the best sample with the fit's own sigma. Total chi-squared 52.4 over 12 bands gives 4.37 per band. Caveat: the spectrum dominates the joint fit, so the fit does not constrain the bands on their own.</figcaption>
</figure>

<figure>
<img loading="lazy" src="/wiki/f/results/rtx-5060-dr2-quiescent-full-spectrum/225431-M9_225431/diagnostics/spectral_chi2.png" alt="M9_225431: spectral pull, binned mean pull squared, cumulative chi-squared">
<figcaption><code>spectral_chi2.png</code> Pull per fitted pixel of the LEGA-C spectrum of galaxy M9_225431. Below it: mean pull squared in 25 Å bins and the cumulative chi-squared fraction against wavelength. Uncertainty: sigma includes the fitted calibration floor of 4.54 percent of the model flux. Comparison: the stored pull versus the pull at the best sample. Shaded bands mark masked pixels. Red points mark pixels with pull beyond 4 sigma. Total chi-squared 3716.7 over 3439 pixels, 6 outlier pixels. Caveat: the fitted floor absorbs model mismatch, so chi-squared near 1 does not prove a good model.</figcaption>
</figure>

<figure>
<img loading="lazy" src="/wiki/f/results/rtx-5060-dr2-quiescent-full-spectrum/225431-M9_225431/diagnostics/sf_timescales.png" alt="M9_225431: cumulative mass formed against lookback time with t10 to t90">
<figcaption><code>sf_timescales.png</code> Fraction of the final stellar mass of galaxy M9_225431 formed earlier than each lookback time. The line is the posterior median. The band is the 16-84 percent range over 400 draws. Comparison: points mark t10 to t90 with 16-84 percent (thick) and 2.5-97.5 percent (thin) intervals versus the universe age. t50 is 3.09 Gyr with a 16-84 percent range of 2.95 to 3.52 Gyr. Caveat: the 7-bin star-formation history model quantises these times to the bin edges.</figcaption>
</figure>

### 225441-M10_225441

| z | S/N | photometry χ²/N | spectrum χ²/N | f_calib | t50 [Gyr] | model |
| --- | --- | --- | --- | --- | --- | --- |
| 0.6823 | 28.9 | 1.59 | 1.069 | 4.38% | 1.65 | [parameters](/wiki/f/results/rtx-5060-dr2-quiescent-full-spectrum/225441-M10_225441/diagnostics/model_parameters.txt) |

Flags: none.

<figure>
<img loading="lazy" src="/wiki/f/results/rtx-5060-dr2-quiescent-full-spectrum/225441-M10_225441/diagnostics/photometric_chi2.png" alt="M10_225441: photometric pull and chi-squared contribution per band">
<figcaption><code>photometric_chi2.png</code> Pull and chi-squared contribution for the 12 COSMOS2015 bands of galaxy M10_225441. Pull equals observed minus model over sigma. Uncertainty: sigma includes the 5 percent flux floor. Comparison: filled points use the posterior-median model. Open squares use the best sample with the fit's own sigma. Total chi-squared 19.1 over 12 bands gives 1.59 per band. Caveat: the spectrum dominates the joint fit, so the fit does not constrain the bands on their own.</figcaption>
</figure>

<figure>
<img loading="lazy" src="/wiki/f/results/rtx-5060-dr2-quiescent-full-spectrum/225441-M10_225441/diagnostics/spectral_chi2.png" alt="M10_225441: spectral pull, binned mean pull squared, cumulative chi-squared">
<figcaption><code>spectral_chi2.png</code> Pull per fitted pixel of the LEGA-C spectrum of galaxy M10_225441. Below it: mean pull squared in 25 Å bins and the cumulative chi-squared fraction against wavelength. Uncertainty: sigma includes the fitted calibration floor of 4.38 percent of the model flux. Comparison: the stored pull versus the pull at the best sample. Shaded bands mark masked pixels. Red points mark pixels with pull beyond 4 sigma. Total chi-squared 3780.7 over 3535 pixels, 0 outlier pixels. Caveat: the fitted floor absorbs model mismatch, so chi-squared near 1 does not prove a good model.</figcaption>
</figure>

<figure>
<img loading="lazy" src="/wiki/f/results/rtx-5060-dr2-quiescent-full-spectrum/225441-M10_225441/diagnostics/sf_timescales.png" alt="M10_225441: cumulative mass formed against lookback time with t10 to t90">
<figcaption><code>sf_timescales.png</code> Fraction of the final stellar mass of galaxy M10_225441 formed earlier than each lookback time. The line is the posterior median. The band is the 16-84 percent range over 400 draws. Comparison: points mark t10 to t90 with 16-84 percent (thick) and 2.5-97.5 percent (thin) intervals versus the universe age. t50 is 1.65 Gyr with a 16-84 percent range of 1.65 to 1.66 Gyr. Caveat: the 7-bin star-formation history model quantises these times to the bin edges.</figcaption>
</figure>

### 225678-M9_225678

| z | S/N | photometry χ²/N | spectrum χ²/N | f_calib | t50 [Gyr] | model |
| --- | --- | --- | --- | --- | --- | --- |
| 0.7326 | 12.3 | 6.49 | 1.170 | 4.55% | 5.06 | [parameters](/wiki/f/results/rtx-5060-dr2-quiescent-full-spectrum/225678-M9_225678/diagnostics/model_parameters.txt) |

Flags:

- photometry chi2/N 6.5 > 3
- 3 pixels with |pull| > 4

<figure>
<img loading="lazy" src="/wiki/f/results/rtx-5060-dr2-quiescent-full-spectrum/225678-M9_225678/diagnostics/photometric_chi2.png" alt="M9_225678: photometric pull and chi-squared contribution per band">
<figcaption><code>photometric_chi2.png</code> Pull and chi-squared contribution for the 12 COSMOS2015 bands of galaxy M9_225678. Pull equals observed minus model over sigma. Uncertainty: sigma includes the 5 percent flux floor. Comparison: filled points use the posterior-median model. Open squares use the best sample with the fit's own sigma. Total chi-squared 77.9 over 12 bands gives 6.49 per band. Caveat: the spectrum dominates the joint fit, so the fit does not constrain the bands on their own.</figcaption>
</figure>

<figure>
<img loading="lazy" src="/wiki/f/results/rtx-5060-dr2-quiescent-full-spectrum/225678-M9_225678/diagnostics/spectral_chi2.png" alt="M9_225678: spectral pull, binned mean pull squared, cumulative chi-squared">
<figcaption><code>spectral_chi2.png</code> Pull per fitted pixel of the LEGA-C spectrum of galaxy M9_225678. Below it: mean pull squared in 25 Å bins and the cumulative chi-squared fraction against wavelength. Uncertainty: sigma includes the fitted calibration floor of 4.55 percent of the model flux. Comparison: the stored pull versus the pull at the best sample. Shaded bands mark masked pixels. Red points mark pixels with pull beyond 4 sigma. Total chi-squared 4025.4 over 3441 pixels, 3 outlier pixels. Caveat: the fitted floor absorbs model mismatch, so chi-squared near 1 does not prove a good model.</figcaption>
</figure>

<figure>
<img loading="lazy" src="/wiki/f/results/rtx-5060-dr2-quiescent-full-spectrum/225678-M9_225678/diagnostics/sf_timescales.png" alt="M9_225678: cumulative mass formed against lookback time with t10 to t90">
<figcaption><code>sf_timescales.png</code> Fraction of the final stellar mass of galaxy M9_225678 formed earlier than each lookback time. The line is the posterior median. The band is the 16-84 percent range over 400 draws. Comparison: points mark t10 to t90 with 16-84 percent (thick) and 2.5-97.5 percent (thin) intervals versus the universe age. t50 is 5.06 Gyr with a 16-84 percent range of 4.15 to 5.65 Gyr. Caveat: the 7-bin star-formation history model quantises these times to the bin edges.</figcaption>
</figure>

### 226316-M9_226316

| z | S/N | photometry χ²/N | spectrum χ²/N | f_calib | t50 [Gyr] | model |
| --- | --- | --- | --- | --- | --- | --- |
| 0.6088 | 51.5 | 8.81 | 1.033 | 3.35% | 6.38 | [parameters](/wiki/f/results/rtx-5060-dr2-quiescent-full-spectrum/226316-M9_226316/diagnostics/model_parameters.txt) |

Flags:

- photometry chi2/N 8.8 > 3
- 1 pixels with |pull| > 4

<figure>
<img loading="lazy" src="/wiki/f/results/rtx-5060-dr2-quiescent-full-spectrum/226316-M9_226316/diagnostics/photometric_chi2.png" alt="M9_226316: photometric pull and chi-squared contribution per band">
<figcaption><code>photometric_chi2.png</code> Pull and chi-squared contribution for the 12 COSMOS2015 bands of galaxy M9_226316. Pull equals observed minus model over sigma. Uncertainty: sigma includes the 5 percent flux floor. Comparison: filled points use the posterior-median model. Open squares use the best sample with the fit's own sigma. Total chi-squared 105.7 over 12 bands gives 8.81 per band. Caveat: the spectrum dominates the joint fit, so the fit does not constrain the bands on their own.</figcaption>
</figure>

<figure>
<img loading="lazy" src="/wiki/f/results/rtx-5060-dr2-quiescent-full-spectrum/226316-M9_226316/diagnostics/spectral_chi2.png" alt="M9_226316: spectral pull, binned mean pull squared, cumulative chi-squared">
<figcaption><code>spectral_chi2.png</code> Pull per fitted pixel of the LEGA-C spectrum of galaxy M9_226316. Below it: mean pull squared in 25 Å bins and the cumulative chi-squared fraction against wavelength. Uncertainty: sigma includes the fitted calibration floor of 3.35 percent of the model flux. Comparison: the stored pull versus the pull at the best sample. Shaded bands mark masked pixels. Red points mark pixels with pull beyond 4 sigma. Total chi-squared 3702.3 over 3585 pixels, 1 outlier pixels. Caveat: the fitted floor absorbs model mismatch, so chi-squared near 1 does not prove a good model.</figcaption>
</figure>

<figure>
<img loading="lazy" src="/wiki/f/results/rtx-5060-dr2-quiescent-full-spectrum/226316-M9_226316/diagnostics/sf_timescales.png" alt="M9_226316: cumulative mass formed against lookback time with t10 to t90">
<figcaption><code>sf_timescales.png</code> Fraction of the final stellar mass of galaxy M9_226316 formed earlier than each lookback time. The line is the posterior median. The band is the 16-84 percent range over 400 draws. Comparison: points mark t10 to t90 with 16-84 percent (thick) and 2.5-97.5 percent (thin) intervals versus the universe age. t50 is 6.38 Gyr with a 16-84 percent range of 6.32 to 6.40 Gyr. Caveat: the 7-bin star-formation history model quantises these times to the bin edges.</figcaption>
</figure>

### 226721-M11_226721

| z | S/N | photometry χ²/N | spectrum χ²/N | f_calib | t50 [Gyr] | model |
| --- | --- | --- | --- | --- | --- | --- |
| 0.7373 | 29.0 | 3.37 | 1.132 | 4.88% | 3.40 | [parameters](/wiki/f/results/rtx-5060-dr2-quiescent-full-spectrum/226721-M11_226721/diagnostics/model_parameters.txt) |

Flags:

- photometry chi2/N 3.4 > 3
- 11 pixels with |pull| > 4

<figure>
<img loading="lazy" src="/wiki/f/results/rtx-5060-dr2-quiescent-full-spectrum/226721-M11_226721/diagnostics/photometric_chi2.png" alt="M11_226721: photometric pull and chi-squared contribution per band">
<figcaption><code>photometric_chi2.png</code> Pull and chi-squared contribution for the 12 COSMOS2015 bands of galaxy M11_226721. Pull equals observed minus model over sigma. Uncertainty: sigma includes the 5 percent flux floor. Comparison: filled points use the posterior-median model. Open squares use the best sample with the fit's own sigma. Total chi-squared 40.5 over 12 bands gives 3.37 per band. Caveat: the spectrum dominates the joint fit, so the fit does not constrain the bands on their own.</figcaption>
</figure>

<figure>
<img loading="lazy" src="/wiki/f/results/rtx-5060-dr2-quiescent-full-spectrum/226721-M11_226721/diagnostics/spectral_chi2.png" alt="M11_226721: spectral pull, binned mean pull squared, cumulative chi-squared">
<figcaption><code>spectral_chi2.png</code> Pull per fitted pixel of the LEGA-C spectrum of galaxy M11_226721. Below it: mean pull squared in 25 Å bins and the cumulative chi-squared fraction against wavelength. Uncertainty: sigma includes the fitted calibration floor of 4.88 percent of the model flux. Comparison: the stored pull versus the pull at the best sample. Shaded bands mark masked pixels. Red points mark pixels with pull beyond 4 sigma. Total chi-squared 3853.7 over 3405 pixels, 11 outlier pixels. Caveat: the fitted floor absorbs model mismatch, so chi-squared near 1 does not prove a good model.</figcaption>
</figure>

<figure>
<img loading="lazy" src="/wiki/f/results/rtx-5060-dr2-quiescent-full-spectrum/226721-M11_226721/diagnostics/sf_timescales.png" alt="M11_226721: cumulative mass formed against lookback time with t10 to t90">
<figcaption><code>sf_timescales.png</code> Fraction of the final stellar mass of galaxy M11_226721 formed earlier than each lookback time. The line is the posterior median. The band is the 16-84 percent range over 400 draws. Comparison: points mark t10 to t90 with 16-84 percent (thick) and 2.5-97.5 percent (thin) intervals versus the universe age. t50 is 3.40 Gyr with a 16-84 percent range of 2.78 to 3.75 Gyr. Caveat: the 7-bin star-formation history model quantises these times to the bin edges.</figcaption>
</figure>

### 227516-M10_227516

| z | S/N | photometry χ²/N | spectrum χ²/N | f_calib | t50 [Gyr] | model |
| --- | --- | --- | --- | --- | --- | --- |
| 0.7792 | 29.2 | 10.54 | 1.077 | 4.77% | 4.65 | [parameters](/wiki/f/results/rtx-5060-dr2-quiescent-full-spectrum/227516-M10_227516/diagnostics/model_parameters.txt) |

Flags:

- photometry chi2/N 10.5 > 3
- 4 pixels with |pull| > 4

<figure>
<img loading="lazy" src="/wiki/f/results/rtx-5060-dr2-quiescent-full-spectrum/227516-M10_227516/diagnostics/photometric_chi2.png" alt="M10_227516: photometric pull and chi-squared contribution per band">
<figcaption><code>photometric_chi2.png</code> Pull and chi-squared contribution for the 12 COSMOS2015 bands of galaxy M10_227516. Pull equals observed minus model over sigma. Uncertainty: sigma includes the 5 percent flux floor. Comparison: filled points use the posterior-median model. Open squares use the best sample with the fit's own sigma. Total chi-squared 126.5 over 12 bands gives 10.54 per band. Caveat: the spectrum dominates the joint fit, so the fit does not constrain the bands on their own.</figcaption>
</figure>

<figure>
<img loading="lazy" src="/wiki/f/results/rtx-5060-dr2-quiescent-full-spectrum/227516-M10_227516/diagnostics/spectral_chi2.png" alt="M10_227516: spectral pull, binned mean pull squared, cumulative chi-squared">
<figcaption><code>spectral_chi2.png</code> Pull per fitted pixel of the LEGA-C spectrum of galaxy M10_227516. Below it: mean pull squared in 25 Å bins and the cumulative chi-squared fraction against wavelength. Uncertainty: sigma includes the fitted calibration floor of 4.77 percent of the model flux. Comparison: the stored pull versus the pull at the best sample. Shaded bands mark masked pixels. Red points mark pixels with pull beyond 4 sigma. Total chi-squared 3970.1 over 3686 pixels, 4 outlier pixels. Caveat: the fitted floor absorbs model mismatch, so chi-squared near 1 does not prove a good model.</figcaption>
</figure>

<figure>
<img loading="lazy" src="/wiki/f/results/rtx-5060-dr2-quiescent-full-spectrum/227516-M10_227516/diagnostics/sf_timescales.png" alt="M10_227516: cumulative mass formed against lookback time with t10 to t90">
<figcaption><code>sf_timescales.png</code> Fraction of the final stellar mass of galaxy M10_227516 formed earlier than each lookback time. The line is the posterior median. The band is the 16-84 percent range over 400 draws. Comparison: points mark t10 to t90 with 16-84 percent (thick) and 2.5-97.5 percent (thin) intervals versus the universe age. t50 is 4.65 Gyr with a 16-84 percent range of 4.57 to 4.75 Gyr. Caveat: the 7-bin star-formation history model quantises these times to the bin edges.</figcaption>
</figure>

### 227630-M9_227630

| z | S/N | photometry χ²/N | spectrum χ²/N | f_calib | t50 [Gyr] | model |
| --- | --- | --- | --- | --- | --- | --- |
| 0.7296 | 19.1 | 4.00 | 1.119 | 3.93% | 3.00 | [parameters](/wiki/f/results/rtx-5060-dr2-quiescent-full-spectrum/227630-M9_227630/diagnostics/model_parameters.txt) |

Flags:

- photometry chi2/N 4.0 > 3

<figure>
<img loading="lazy" src="/wiki/f/results/rtx-5060-dr2-quiescent-full-spectrum/227630-M9_227630/diagnostics/photometric_chi2.png" alt="M9_227630: photometric pull and chi-squared contribution per band">
<figcaption><code>photometric_chi2.png</code> Pull and chi-squared contribution for the 12 COSMOS2015 bands of galaxy M9_227630. Pull equals observed minus model over sigma. Uncertainty: sigma includes the 5 percent flux floor. Comparison: filled points use the posterior-median model. Open squares use the best sample with the fit's own sigma. Total chi-squared 48.0 over 12 bands gives 4.00 per band. Caveat: the spectrum dominates the joint fit, so the fit does not constrain the bands on their own.</figcaption>
</figure>

<figure>
<img loading="lazy" src="/wiki/f/results/rtx-5060-dr2-quiescent-full-spectrum/227630-M9_227630/diagnostics/spectral_chi2.png" alt="M9_227630: spectral pull, binned mean pull squared, cumulative chi-squared">
<figcaption><code>spectral_chi2.png</code> Pull per fitted pixel of the LEGA-C spectrum of galaxy M9_227630. Below it: mean pull squared in 25 Å bins and the cumulative chi-squared fraction against wavelength. Uncertainty: sigma includes the fitted calibration floor of 3.93 percent of the model flux. Comparison: the stored pull versus the pull at the best sample. Shaded bands mark masked pixels. Red points mark pixels with pull beyond 4 sigma. Total chi-squared 3905.8 over 3490 pixels, 0 outlier pixels. Caveat: the fitted floor absorbs model mismatch, so chi-squared near 1 does not prove a good model.</figcaption>
</figure>

<figure>
<img loading="lazy" src="/wiki/f/results/rtx-5060-dr2-quiescent-full-spectrum/227630-M9_227630/diagnostics/sf_timescales.png" alt="M9_227630: cumulative mass formed against lookback time with t10 to t90">
<figcaption><code>sf_timescales.png</code> Fraction of the final stellar mass of galaxy M9_227630 formed earlier than each lookback time. The line is the posterior median. The band is the 16-84 percent range over 400 draws. Comparison: points mark t10 to t90 with 16-84 percent (thick) and 2.5-97.5 percent (thin) intervals versus the universe age. t50 is 3.00 Gyr with a 16-84 percent range of 2.95 to 3.12 Gyr. Caveat: the 7-bin star-formation history model quantises these times to the bin edges.</figcaption>
</figure>

### 227672-M10_227672

| z | S/N | photometry χ²/N | spectrum χ²/N | f_calib | t50 [Gyr] | model |
| --- | --- | --- | --- | --- | --- | --- |
| 0.6093 | 19.3 | 8.49 | 1.048 | 2.97% | 3.01 | [parameters](/wiki/f/results/rtx-5060-dr2-quiescent-full-spectrum/227672-M10_227672/diagnostics/model_parameters.txt) |

Flags:

- photometry chi2/N 8.5 > 3
- 2 pixels with |pull| > 4

<figure>
<img loading="lazy" src="/wiki/f/results/rtx-5060-dr2-quiescent-full-spectrum/227672-M10_227672/diagnostics/photometric_chi2.png" alt="M10_227672: photometric pull and chi-squared contribution per band">
<figcaption><code>photometric_chi2.png</code> Pull and chi-squared contribution for the 12 COSMOS2015 bands of galaxy M10_227672. Pull equals observed minus model over sigma. Uncertainty: sigma includes the 5 percent flux floor. Comparison: filled points use the posterior-median model. Open squares use the best sample with the fit's own sigma. Total chi-squared 101.9 over 12 bands gives 8.49 per band. Caveat: the spectrum dominates the joint fit, so the fit does not constrain the bands on their own.</figcaption>
</figure>

<figure>
<img loading="lazy" src="/wiki/f/results/rtx-5060-dr2-quiescent-full-spectrum/227672-M10_227672/diagnostics/spectral_chi2.png" alt="M10_227672: spectral pull, binned mean pull squared, cumulative chi-squared">
<figcaption><code>spectral_chi2.png</code> Pull per fitted pixel of the LEGA-C spectrum of galaxy M10_227672. Below it: mean pull squared in 25 Å bins and the cumulative chi-squared fraction against wavelength. Uncertainty: sigma includes the fitted calibration floor of 2.97 percent of the model flux. Comparison: the stored pull versus the pull at the best sample. Shaded bands mark masked pixels. Red points mark pixels with pull beyond 4 sigma. Total chi-squared 3726.9 over 3555 pixels, 2 outlier pixels. Caveat: the fitted floor absorbs model mismatch, so chi-squared near 1 does not prove a good model.</figcaption>
</figure>

<figure>
<img loading="lazy" src="/wiki/f/results/rtx-5060-dr2-quiescent-full-spectrum/227672-M10_227672/diagnostics/sf_timescales.png" alt="M10_227672: cumulative mass formed against lookback time with t10 to t90">
<figcaption><code>sf_timescales.png</code> Fraction of the final stellar mass of galaxy M10_227672 formed earlier than each lookback time. The line is the posterior median. The band is the 16-84 percent range over 400 draws. Comparison: points mark t10 to t90 with 16-84 percent (thick) and 2.5-97.5 percent (thin) intervals versus the universe age. t50 is 3.01 Gyr with a 16-84 percent range of 2.99 to 3.08 Gyr. Caveat: the 7-bin star-formation history model quantises these times to the bin edges.</figcaption>
</figure>

### 228215-M10_228215

| z | S/N | photometry χ²/N | spectrum χ²/N | f_calib | t50 [Gyr] | model |
| --- | --- | --- | --- | --- | --- | --- |
| 0.6109 | 36.8 | 9.45 | 1.125 | 2.90% | 3.27 | [parameters](/wiki/f/results/rtx-5060-dr2-quiescent-full-spectrum/228215-M10_228215/diagnostics/model_parameters.txt) |

Flags:

- photometry chi2/N 9.4 > 3
- 6 pixels with |pull| > 4

<figure>
<img loading="lazy" src="/wiki/f/results/rtx-5060-dr2-quiescent-full-spectrum/228215-M10_228215/diagnostics/photometric_chi2.png" alt="M10_228215: photometric pull and chi-squared contribution per band">
<figcaption><code>photometric_chi2.png</code> Pull and chi-squared contribution for the 12 COSMOS2015 bands of galaxy M10_228215. Pull equals observed minus model over sigma. Uncertainty: sigma includes the 5 percent flux floor. Comparison: filled points use the posterior-median model. Open squares use the best sample with the fit's own sigma. Total chi-squared 113.3 over 12 bands gives 9.45 per band. Caveat: the spectrum dominates the joint fit, so the fit does not constrain the bands on their own.</figcaption>
</figure>

<figure>
<img loading="lazy" src="/wiki/f/results/rtx-5060-dr2-quiescent-full-spectrum/228215-M10_228215/diagnostics/spectral_chi2.png" alt="M10_228215: spectral pull, binned mean pull squared, cumulative chi-squared">
<figcaption><code>spectral_chi2.png</code> Pull per fitted pixel of the LEGA-C spectrum of galaxy M10_228215. Below it: mean pull squared in 25 Å bins and the cumulative chi-squared fraction against wavelength. Uncertainty: sigma includes the fitted calibration floor of 2.90 percent of the model flux. Comparison: the stored pull versus the pull at the best sample. Shaded bands mark masked pixels. Red points mark pixels with pull beyond 4 sigma. Total chi-squared 4005.4 over 3559 pixels, 6 outlier pixels. Caveat: the fitted floor absorbs model mismatch, so chi-squared near 1 does not prove a good model.</figcaption>
</figure>

<figure>
<img loading="lazy" src="/wiki/f/results/rtx-5060-dr2-quiescent-full-spectrum/228215-M10_228215/diagnostics/sf_timescales.png" alt="M10_228215: cumulative mass formed against lookback time with t10 to t90">
<figcaption><code>sf_timescales.png</code> Fraction of the final stellar mass of galaxy M10_228215 formed earlier than each lookback time. The line is the posterior median. The band is the 16-84 percent range over 400 draws. Comparison: points mark t10 to t90 with 16-84 percent (thick) and 2.5-97.5 percent (thin) intervals versus the universe age. t50 is 3.27 Gyr with a 16-84 percent range of 3.06 to 3.46 Gyr. Caveat: the 7-bin star-formation history model quantises these times to the bin edges.</figcaption>
</figure>

### 228380-M10_228380

| z | S/N | photometry χ²/N | spectrum χ²/N | f_calib | t50 [Gyr] | model |
| --- | --- | --- | --- | --- | --- | --- |
| 0.6114 | 36.1 | 28.77 | 1.133 | 3.25% | 3.01 | [parameters](/wiki/f/results/rtx-5060-dr2-quiescent-full-spectrum/228380-M10_228380/diagnostics/model_parameters.txt) |

Flags:

- photometry chi2/N 28.8 > 3
- 5 pixels with |pull| > 4

<figure>
<img loading="lazy" src="/wiki/f/results/rtx-5060-dr2-quiescent-full-spectrum/228380-M10_228380/diagnostics/photometric_chi2.png" alt="M10_228380: photometric pull and chi-squared contribution per band">
<figcaption><code>photometric_chi2.png</code> Pull and chi-squared contribution for the 12 COSMOS2015 bands of galaxy M10_228380. Pull equals observed minus model over sigma. Uncertainty: sigma includes the 5 percent flux floor. Comparison: filled points use the posterior-median model. Open squares use the best sample with the fit's own sigma. Total chi-squared 345.3 over 12 bands gives 28.77 per band. Caveat: the spectrum dominates the joint fit, so the fit does not constrain the bands on their own.</figcaption>
</figure>

<figure>
<img loading="lazy" src="/wiki/f/results/rtx-5060-dr2-quiescent-full-spectrum/228380-M10_228380/diagnostics/spectral_chi2.png" alt="M10_228380: spectral pull, binned mean pull squared, cumulative chi-squared">
<figcaption><code>spectral_chi2.png</code> Pull per fitted pixel of the LEGA-C spectrum of galaxy M10_228380. Below it: mean pull squared in 25 Å bins and the cumulative chi-squared fraction against wavelength. Uncertainty: sigma includes the fitted calibration floor of 3.25 percent of the model flux. Comparison: the stored pull versus the pull at the best sample. Shaded bands mark masked pixels. Red points mark pixels with pull beyond 4 sigma. Total chi-squared 4044.0 over 3568 pixels, 5 outlier pixels. Caveat: the fitted floor absorbs model mismatch, so chi-squared near 1 does not prove a good model.</figcaption>
</figure>

<figure>
<img loading="lazy" src="/wiki/f/results/rtx-5060-dr2-quiescent-full-spectrum/228380-M10_228380/diagnostics/sf_timescales.png" alt="M10_228380: cumulative mass formed against lookback time with t10 to t90">
<figcaption><code>sf_timescales.png</code> Fraction of the final stellar mass of galaxy M10_228380 formed earlier than each lookback time. The line is the posterior median. The band is the 16-84 percent range over 400 draws. Comparison: points mark t10 to t90 with 16-84 percent (thick) and 2.5-97.5 percent (thin) intervals versus the universe age. t50 is 3.01 Gyr with a 16-84 percent range of 3.00 to 3.07 Gyr. Caveat: the 7-bin star-formation history model quantises these times to the bin edges.</figcaption>
</figure>

### 228717-M10_228717

| z | S/N | photometry χ²/N | spectrum χ²/N | f_calib | t50 [Gyr] | model |
| --- | --- | --- | --- | --- | --- | --- |
| 0.9399 | 14.3 | 16.42 | 0.976 | 6.45% | 4.59 | [parameters](/wiki/f/results/rtx-5060-dr2-quiescent-full-spectrum/228717-M10_228717/diagnostics/model_parameters.txt) |

Flags:

- photometry chi2/N 16.4 > 3
- 2 pixels with |pull| > 4

<figure>
<img loading="lazy" src="/wiki/f/results/rtx-5060-dr2-quiescent-full-spectrum/228717-M10_228717/diagnostics/photometric_chi2.png" alt="M10_228717: photometric pull and chi-squared contribution per band">
<figcaption><code>photometric_chi2.png</code> Pull and chi-squared contribution for the 12 COSMOS2015 bands of galaxy M10_228717. Pull equals observed minus model over sigma. Uncertainty: sigma includes the 5 percent flux floor. Comparison: filled points use the posterior-median model. Open squares use the best sample with the fit's own sigma. Total chi-squared 197.0 over 12 bands gives 16.42 per band. Caveat: the spectrum dominates the joint fit, so the fit does not constrain the bands on their own.</figcaption>
</figure>

<figure>
<img loading="lazy" src="/wiki/f/results/rtx-5060-dr2-quiescent-full-spectrum/228717-M10_228717/diagnostics/spectral_chi2.png" alt="M10_228717: spectral pull, binned mean pull squared, cumulative chi-squared">
<figcaption><code>spectral_chi2.png</code> Pull per fitted pixel of the LEGA-C spectrum of galaxy M10_228717. Below it: mean pull squared in 25 Å bins and the cumulative chi-squared fraction against wavelength. Uncertainty: sigma includes the fitted calibration floor of 6.45 percent of the model flux. Comparison: the stored pull versus the pull at the best sample. Shaded bands mark masked pixels. Red points mark pixels with pull beyond 4 sigma. Total chi-squared 3742.7 over 3835 pixels, 2 outlier pixels. Caveat: the fitted floor absorbs model mismatch, so chi-squared near 1 does not prove a good model.</figcaption>
</figure>

<figure>
<img loading="lazy" src="/wiki/f/results/rtx-5060-dr2-quiescent-full-spectrum/228717-M10_228717/diagnostics/sf_timescales.png" alt="M10_228717: cumulative mass formed against lookback time with t10 to t90">
<figcaption><code>sf_timescales.png</code> Fraction of the final stellar mass of galaxy M10_228717 formed earlier than each lookback time. The line is the posterior median. The band is the 16-84 percent range over 400 draws. Comparison: points mark t10 to t90 with 16-84 percent (thick) and 2.5-97.5 percent (thin) intervals versus the universe age. t50 is 4.59 Gyr with a 16-84 percent range of 4.27 to 5.18 Gyr. Caveat: the 7-bin star-formation history model quantises these times to the bin edges.</figcaption>
</figure>

### 229551-M11_229551

| z | S/N | photometry χ²/N | spectrum χ²/N | f_calib | t50 [Gyr] | model |
| --- | --- | --- | --- | --- | --- | --- |
| 0.6958 | 32.8 | 8.28 | 1.109 | 4.70% | 2.87 | [parameters](/wiki/f/results/rtx-5060-dr2-quiescent-full-spectrum/229551-M11_229551/diagnostics/model_parameters.txt) |

Flags:

- photometry chi2/N 8.3 > 3
- 12 pixels with |pull| > 4

<figure>
<img loading="lazy" src="/wiki/f/results/rtx-5060-dr2-quiescent-full-spectrum/229551-M11_229551/diagnostics/photometric_chi2.png" alt="M11_229551: photometric pull and chi-squared contribution per band">
<figcaption><code>photometric_chi2.png</code> Pull and chi-squared contribution for the 12 COSMOS2015 bands of galaxy M11_229551. Pull equals observed minus model over sigma. Uncertainty: sigma includes the 5 percent flux floor. Comparison: filled points use the posterior-median model. Open squares use the best sample with the fit's own sigma. Total chi-squared 99.3 over 12 bands gives 8.28 per band. Caveat: the spectrum dominates the joint fit, so the fit does not constrain the bands on their own.</figcaption>
</figure>

<figure>
<img loading="lazy" src="/wiki/f/results/rtx-5060-dr2-quiescent-full-spectrum/229551-M11_229551/diagnostics/spectral_chi2.png" alt="M11_229551: spectral pull, binned mean pull squared, cumulative chi-squared">
<figcaption><code>spectral_chi2.png</code> Pull per fitted pixel of the LEGA-C spectrum of galaxy M11_229551. Below it: mean pull squared in 25 Å bins and the cumulative chi-squared fraction against wavelength. Uncertainty: sigma includes the fitted calibration floor of 4.70 percent of the model flux. Comparison: the stored pull versus the pull at the best sample. Shaded bands mark masked pixels. Red points mark pixels with pull beyond 4 sigma. Total chi-squared 3841.7 over 3463 pixels, 12 outlier pixels. Caveat: the fitted floor absorbs model mismatch, so chi-squared near 1 does not prove a good model.</figcaption>
</figure>

<figure>
<img loading="lazy" src="/wiki/f/results/rtx-5060-dr2-quiescent-full-spectrum/229551-M11_229551/diagnostics/sf_timescales.png" alt="M11_229551: cumulative mass formed against lookback time with t10 to t90">
<figcaption><code>sf_timescales.png</code> Fraction of the final stellar mass of galaxy M11_229551 formed earlier than each lookback time. The line is the posterior median. The band is the 16-84 percent range over 400 draws. Comparison: points mark t10 to t90 with 16-84 percent (thick) and 2.5-97.5 percent (thin) intervals versus the universe age. t50 is 2.87 Gyr with a 16-84 percent range of 2.84 to 2.92 Gyr. Caveat: the 7-bin star-formation history model quantises these times to the bin edges.</figcaption>
</figure>

### 229883-M9_229883

| z | S/N | photometry χ²/N | spectrum χ²/N | f_calib | t50 [Gyr] | model |
| --- | --- | --- | --- | --- | --- | --- |
| 0.7280 | 22.6 | 8.40 | 1.167 | 4.25% | 3.61 | [parameters](/wiki/f/results/rtx-5060-dr2-quiescent-full-spectrum/229883-M9_229883/diagnostics/model_parameters.txt) |

Flags:

- photometry chi2/N 8.4 > 3
- 3 pixels with |pull| > 4

<figure>
<img loading="lazy" src="/wiki/f/results/rtx-5060-dr2-quiescent-full-spectrum/229883-M9_229883/diagnostics/photometric_chi2.png" alt="M9_229883: photometric pull and chi-squared contribution per band">
<figcaption><code>photometric_chi2.png</code> Pull and chi-squared contribution for the 12 COSMOS2015 bands of galaxy M9_229883. Pull equals observed minus model over sigma. Uncertainty: sigma includes the 5 percent flux floor. Comparison: filled points use the posterior-median model. Open squares use the best sample with the fit's own sigma. Total chi-squared 100.8 over 12 bands gives 8.40 per band. Caveat: the spectrum dominates the joint fit, so the fit does not constrain the bands on their own.</figcaption>
</figure>

<figure>
<img loading="lazy" src="/wiki/f/results/rtx-5060-dr2-quiescent-full-spectrum/229883-M9_229883/diagnostics/spectral_chi2.png" alt="M9_229883: spectral pull, binned mean pull squared, cumulative chi-squared">
<figcaption><code>spectral_chi2.png</code> Pull per fitted pixel of the LEGA-C spectrum of galaxy M9_229883. Below it: mean pull squared in 25 Å bins and the cumulative chi-squared fraction against wavelength. Uncertainty: sigma includes the fitted calibration floor of 4.25 percent of the model flux. Comparison: the stored pull versus the pull at the best sample. Shaded bands mark masked pixels. Red points mark pixels with pull beyond 4 sigma. Total chi-squared 4135.8 over 3544 pixels, 3 outlier pixels. Caveat: the fitted floor absorbs model mismatch, so chi-squared near 1 does not prove a good model.</figcaption>
</figure>

<figure>
<img loading="lazy" src="/wiki/f/results/rtx-5060-dr2-quiescent-full-spectrum/229883-M9_229883/diagnostics/sf_timescales.png" alt="M9_229883: cumulative mass formed against lookback time with t10 to t90">
<figcaption><code>sf_timescales.png</code> Fraction of the final stellar mass of galaxy M9_229883 formed earlier than each lookback time. The line is the posterior median. The band is the 16-84 percent range over 400 draws. Comparison: points mark t10 to t90 with 16-84 percent (thick) and 2.5-97.5 percent (thin) intervals versus the universe age. t50 is 3.61 Gyr with a 16-84 percent range of 3.15 to 3.99 Gyr. Caveat: the 7-bin star-formation history model quantises these times to the bin edges.</figcaption>
</figure>

### 230747-M13_230747

| z | S/N | photometry χ²/N | spectrum χ²/N | f_calib | t50 [Gyr] | model |
| --- | --- | --- | --- | --- | --- | --- |
| 0.6985 | 22.6 | 1.97 | 1.116 | 5.54% | 2.90 | [parameters](/wiki/f/results/rtx-5060-dr2-quiescent-full-spectrum/230747-M13_230747/diagnostics/model_parameters.txt) |

Flags:

- 4 pixels with |pull| > 4

<figure>
<img loading="lazy" src="/wiki/f/results/rtx-5060-dr2-quiescent-full-spectrum/230747-M13_230747/diagnostics/photometric_chi2.png" alt="M13_230747: photometric pull and chi-squared contribution per band">
<figcaption><code>photometric_chi2.png</code> Pull and chi-squared contribution for the 12 COSMOS2015 bands of galaxy M13_230747. Pull equals observed minus model over sigma. Uncertainty: sigma includes the 5 percent flux floor. Comparison: filled points use the posterior-median model. Open squares use the best sample with the fit's own sigma. Total chi-squared 23.7 over 12 bands gives 1.97 per band. Caveat: the spectrum dominates the joint fit, so the fit does not constrain the bands on their own.</figcaption>
</figure>

<figure>
<img loading="lazy" src="/wiki/f/results/rtx-5060-dr2-quiescent-full-spectrum/230747-M13_230747/diagnostics/spectral_chi2.png" alt="M13_230747: spectral pull, binned mean pull squared, cumulative chi-squared">
<figcaption><code>spectral_chi2.png</code> Pull per fitted pixel of the LEGA-C spectrum of galaxy M13_230747. Below it: mean pull squared in 25 Å bins and the cumulative chi-squared fraction against wavelength. Uncertainty: sigma includes the fitted calibration floor of 5.54 percent of the model flux. Comparison: the stored pull versus the pull at the best sample. Shaded bands mark masked pixels. Red points mark pixels with pull beyond 4 sigma. Total chi-squared 3974.1 over 3562 pixels, 4 outlier pixels. Caveat: the fitted floor absorbs model mismatch, so chi-squared near 1 does not prove a good model.</figcaption>
</figure>

<figure>
<img loading="lazy" src="/wiki/f/results/rtx-5060-dr2-quiescent-full-spectrum/230747-M13_230747/diagnostics/sf_timescales.png" alt="M13_230747: cumulative mass formed against lookback time with t10 to t90">
<figcaption><code>sf_timescales.png</code> Fraction of the final stellar mass of galaxy M13_230747 formed earlier than each lookback time. The line is the posterior median. The band is the 16-84 percent range over 400 draws. Comparison: points mark t10 to t90 with 16-84 percent (thick) and 2.5-97.5 percent (thin) intervals versus the universe age. t50 is 2.90 Gyr with a 16-84 percent range of 2.85 to 2.97 Gyr. Caveat: the 7-bin star-formation history model quantises these times to the bin edges.</figcaption>
</figure>

### 230983-M10_230983

| z | S/N | photometry χ²/N | spectrum χ²/N | f_calib | t50 [Gyr] | model |
| --- | --- | --- | --- | --- | --- | --- |
| 0.6961 | 21.7 | 4.69 | 1.034 | 4.26% | 5.51 | [parameters](/wiki/f/results/rtx-5060-dr2-quiescent-full-spectrum/230983-M10_230983/diagnostics/model_parameters.txt) |

Flags:

- photometry chi2/N 4.7 > 3

<figure>
<img loading="lazy" src="/wiki/f/results/rtx-5060-dr2-quiescent-full-spectrum/230983-M10_230983/diagnostics/photometric_chi2.png" alt="M10_230983: photometric pull and chi-squared contribution per band">
<figcaption><code>photometric_chi2.png</code> Pull and chi-squared contribution for the 12 COSMOS2015 bands of galaxy M10_230983. Pull equals observed minus model over sigma. Uncertainty: sigma includes the 5 percent flux floor. Comparison: filled points use the posterior-median model. Open squares use the best sample with the fit's own sigma. Total chi-squared 56.3 over 12 bands gives 4.69 per band. Caveat: the spectrum dominates the joint fit, so the fit does not constrain the bands on their own.</figcaption>
</figure>

<figure>
<img loading="lazy" src="/wiki/f/results/rtx-5060-dr2-quiescent-full-spectrum/230983-M10_230983/diagnostics/spectral_chi2.png" alt="M10_230983: spectral pull, binned mean pull squared, cumulative chi-squared">
<figcaption><code>spectral_chi2.png</code> Pull per fitted pixel of the LEGA-C spectrum of galaxy M10_230983. Below it: mean pull squared in 25 Å bins and the cumulative chi-squared fraction against wavelength. Uncertainty: sigma includes the fitted calibration floor of 4.26 percent of the model flux. Comparison: the stored pull versus the pull at the best sample. Shaded bands mark masked pixels. Red points mark pixels with pull beyond 4 sigma. Total chi-squared 3708.1 over 3586 pixels, 0 outlier pixels. Caveat: the fitted floor absorbs model mismatch, so chi-squared near 1 does not prove a good model.</figcaption>
</figure>

<figure>
<img loading="lazy" src="/wiki/f/results/rtx-5060-dr2-quiescent-full-spectrum/230983-M10_230983/diagnostics/sf_timescales.png" alt="M10_230983: cumulative mass formed against lookback time with t10 to t90">
<figcaption><code>sf_timescales.png</code> Fraction of the final stellar mass of galaxy M10_230983 formed earlier than each lookback time. The line is the posterior median. The band is the 16-84 percent range over 400 draws. Comparison: points mark t10 to t90 with 16-84 percent (thick) and 2.5-97.5 percent (thin) intervals versus the universe age. t50 is 5.51 Gyr with a 16-84 percent range of 4.93 to 5.91 Gyr. Caveat: the 7-bin star-formation history model quantises these times to the bin edges.</figcaption>
</figure>

### 231276-M9_231276

| z | S/N | photometry χ²/N | spectrum χ²/N | f_calib | t50 [Gyr] | model |
| --- | --- | --- | --- | --- | --- | --- |
| 0.6541 | 40.1 | 8.63 | 1.112 | 5.99% | 4.48 | [parameters](/wiki/f/results/rtx-5060-dr2-quiescent-full-spectrum/231276-M9_231276/diagnostics/model_parameters.txt) |

Flags:

- photometry chi2/N 8.6 > 3
- 5 pixels with |pull| > 4

<figure>
<img loading="lazy" src="/wiki/f/results/rtx-5060-dr2-quiescent-full-spectrum/231276-M9_231276/diagnostics/photometric_chi2.png" alt="M9_231276: photometric pull and chi-squared contribution per band">
<figcaption><code>photometric_chi2.png</code> Pull and chi-squared contribution for the 12 COSMOS2015 bands of galaxy M9_231276. Pull equals observed minus model over sigma. Uncertainty: sigma includes the 5 percent flux floor. Comparison: filled points use the posterior-median model. Open squares use the best sample with the fit's own sigma. Total chi-squared 103.5 over 12 bands gives 8.63 per band. Caveat: the spectrum dominates the joint fit, so the fit does not constrain the bands on their own.</figcaption>
</figure>

<figure>
<img loading="lazy" src="/wiki/f/results/rtx-5060-dr2-quiescent-full-spectrum/231276-M9_231276/diagnostics/spectral_chi2.png" alt="M9_231276: spectral pull, binned mean pull squared, cumulative chi-squared">
<figcaption><code>spectral_chi2.png</code> Pull per fitted pixel of the LEGA-C spectrum of galaxy M9_231276. Below it: mean pull squared in 25 Å bins and the cumulative chi-squared fraction against wavelength. Uncertainty: sigma includes the fitted calibration floor of 5.99 percent of the model flux. Comparison: the stored pull versus the pull at the best sample. Shaded bands mark masked pixels. Red points mark pixels with pull beyond 4 sigma. Total chi-squared 3917.7 over 3522 pixels, 5 outlier pixels. Caveat: the fitted floor absorbs model mismatch, so chi-squared near 1 does not prove a good model.</figcaption>
</figure>

<figure>
<img loading="lazy" src="/wiki/f/results/rtx-5060-dr2-quiescent-full-spectrum/231276-M9_231276/diagnostics/sf_timescales.png" alt="M9_231276: cumulative mass formed against lookback time with t10 to t90">
<figcaption><code>sf_timescales.png</code> Fraction of the final stellar mass of galaxy M9_231276 formed earlier than each lookback time. The line is the posterior median. The band is the 16-84 percent range over 400 draws. Comparison: points mark t10 to t90 with 16-84 percent (thick) and 2.5-97.5 percent (thin) intervals versus the universe age. t50 is 4.48 Gyr with a 16-84 percent range of 4.11 to 5.51 Gyr. Caveat: the 7-bin star-formation history model quantises these times to the bin edges.</figcaption>
</figure>

### 231544-M10_231544

| z | S/N | photometry χ²/N | spectrum χ²/N | f_calib | t50 [Gyr] | model |
| --- | --- | --- | --- | --- | --- | --- |
| 0.6548 | 26.1 | 2.85 | 1.065 | 2.75% | 2.95 | [parameters](/wiki/f/results/rtx-5060-dr2-quiescent-full-spectrum/231544-M10_231544/diagnostics/model_parameters.txt) |

Flags: none.

<figure>
<img loading="lazy" src="/wiki/f/results/rtx-5060-dr2-quiescent-full-spectrum/231544-M10_231544/diagnostics/photometric_chi2.png" alt="M10_231544: photometric pull and chi-squared contribution per band">
<figcaption><code>photometric_chi2.png</code> Pull and chi-squared contribution for the 12 COSMOS2015 bands of galaxy M10_231544. Pull equals observed minus model over sigma. Uncertainty: sigma includes the 5 percent flux floor. Comparison: filled points use the posterior-median model. Open squares use the best sample with the fit's own sigma. Total chi-squared 34.2 over 12 bands gives 2.85 per band. Caveat: the spectrum dominates the joint fit, so the fit does not constrain the bands on their own.</figcaption>
</figure>

<figure>
<img loading="lazy" src="/wiki/f/results/rtx-5060-dr2-quiescent-full-spectrum/231544-M10_231544/diagnostics/spectral_chi2.png" alt="M10_231544: spectral pull, binned mean pull squared, cumulative chi-squared">
<figcaption><code>spectral_chi2.png</code> Pull per fitted pixel of the LEGA-C spectrum of galaxy M10_231544. Below it: mean pull squared in 25 Å bins and the cumulative chi-squared fraction against wavelength. Uncertainty: sigma includes the fitted calibration floor of 2.75 percent of the model flux. Comparison: the stored pull versus the pull at the best sample. Shaded bands mark masked pixels. Red points mark pixels with pull beyond 4 sigma. Total chi-squared 3717.5 over 3492 pixels, 0 outlier pixels. Caveat: the fitted floor absorbs model mismatch, so chi-squared near 1 does not prove a good model.</figcaption>
</figure>

<figure>
<img loading="lazy" src="/wiki/f/results/rtx-5060-dr2-quiescent-full-spectrum/231544-M10_231544/diagnostics/sf_timescales.png" alt="M10_231544: cumulative mass formed against lookback time with t10 to t90">
<figcaption><code>sf_timescales.png</code> Fraction of the final stellar mass of galaxy M10_231544 formed earlier than each lookback time. The line is the posterior median. The band is the 16-84 percent range over 400 draws. Comparison: points mark t10 to t90 with 16-84 percent (thick) and 2.5-97.5 percent (thin) intervals versus the universe age. t50 is 2.95 Gyr with a 16-84 percent range of 2.88 to 3.00 Gyr. Caveat: the 7-bin star-formation history model quantises these times to the bin edges.</figcaption>
</figure>

### 231554-M13_231554

| z | S/N | photometry χ²/N | spectrum χ²/N | f_calib | t50 [Gyr] | model |
| --- | --- | --- | --- | --- | --- | --- |
| 0.6973 | 10.9 | 2.81 | 1.213 | 9.96% | 5.32 | [parameters](/wiki/f/results/rtx-5060-dr2-quiescent-full-spectrum/231554-M13_231554/diagnostics/model_parameters.txt) |

Flags:

- calibration floor at prior bound (10.0% of 10%)
- 4 pixels with |pull| > 4

<figure>
<img loading="lazy" src="/wiki/f/results/rtx-5060-dr2-quiescent-full-spectrum/231554-M13_231554/diagnostics/photometric_chi2.png" alt="M13_231554: photometric pull and chi-squared contribution per band">
<figcaption><code>photometric_chi2.png</code> Pull and chi-squared contribution for the 12 COSMOS2015 bands of galaxy M13_231554. Pull equals observed minus model over sigma. Uncertainty: sigma includes the 5 percent flux floor. Comparison: filled points use the posterior-median model. Open squares use the best sample with the fit's own sigma. Total chi-squared 33.7 over 12 bands gives 2.81 per band. Caveat: the spectrum dominates the joint fit, so the fit does not constrain the bands on their own.</figcaption>
</figure>

<figure>
<img loading="lazy" src="/wiki/f/results/rtx-5060-dr2-quiescent-full-spectrum/231554-M13_231554/diagnostics/spectral_chi2.png" alt="M13_231554: spectral pull, binned mean pull squared, cumulative chi-squared">
<figcaption><code>spectral_chi2.png</code> Pull per fitted pixel of the LEGA-C spectrum of galaxy M13_231554. Below it: mean pull squared in 25 Å bins and the cumulative chi-squared fraction against wavelength. Uncertainty: sigma includes the fitted calibration floor of 9.96 percent of the model flux. Comparison: the stored pull versus the pull at the best sample. Shaded bands mark masked pixels. Red points mark pixels with pull beyond 4 sigma. Total chi-squared 4349.0 over 3586 pixels, 4 outlier pixels. Caveat: the fitted floor absorbs model mismatch, so chi-squared near 1 does not prove a good model.</figcaption>
</figure>

<figure>
<img loading="lazy" src="/wiki/f/results/rtx-5060-dr2-quiescent-full-spectrum/231554-M13_231554/diagnostics/sf_timescales.png" alt="M13_231554: cumulative mass formed against lookback time with t10 to t90">
<figcaption><code>sf_timescales.png</code> Fraction of the final stellar mass of galaxy M13_231554 formed earlier than each lookback time. The line is the posterior median. The band is the 16-84 percent range over 400 draws. Comparison: points mark t10 to t90 with 16-84 percent (thick) and 2.5-97.5 percent (thin) intervals versus the universe age. t50 is 5.32 Gyr with a 16-84 percent range of 4.49 to 5.89 Gyr. Caveat: the 7-bin star-formation history model quantises these times to the bin edges.</figcaption>
</figure>

### 232005-M9_232005

| z | S/N | photometry χ²/N | spectrum χ²/N | f_calib | t50 [Gyr] | model |
| --- | --- | --- | --- | --- | --- | --- |
| 0.6111 | 29.0 | 7.22 | 1.109 | 2.86% | 3.05 | [parameters](/wiki/f/results/rtx-5060-dr2-quiescent-full-spectrum/232005-M9_232005/diagnostics/model_parameters.txt) |

Flags:

- photometry chi2/N 7.2 > 3
- 1 pixels with |pull| > 4

<figure>
<img loading="lazy" src="/wiki/f/results/rtx-5060-dr2-quiescent-full-spectrum/232005-M9_232005/diagnostics/photometric_chi2.png" alt="M9_232005: photometric pull and chi-squared contribution per band">
<figcaption><code>photometric_chi2.png</code> Pull and chi-squared contribution for the 12 COSMOS2015 bands of galaxy M9_232005. Pull equals observed minus model over sigma. Uncertainty: sigma includes the 5 percent flux floor. Comparison: filled points use the posterior-median model. Open squares use the best sample with the fit's own sigma. Total chi-squared 86.7 over 12 bands gives 7.22 per band. Caveat: the spectrum dominates the joint fit, so the fit does not constrain the bands on their own.</figcaption>
</figure>

<figure>
<img loading="lazy" src="/wiki/f/results/rtx-5060-dr2-quiescent-full-spectrum/232005-M9_232005/diagnostics/spectral_chi2.png" alt="M9_232005: spectral pull, binned mean pull squared, cumulative chi-squared">
<figcaption><code>spectral_chi2.png</code> Pull per fitted pixel of the LEGA-C spectrum of galaxy M9_232005. Below it: mean pull squared in 25 Å bins and the cumulative chi-squared fraction against wavelength. Uncertainty: sigma includes the fitted calibration floor of 2.86 percent of the model flux. Comparison: the stored pull versus the pull at the best sample. Shaded bands mark masked pixels. Red points mark pixels with pull beyond 4 sigma. Total chi-squared 3875.8 over 3494 pixels, 1 outlier pixels. Caveat: the fitted floor absorbs model mismatch, so chi-squared near 1 does not prove a good model.</figcaption>
</figure>

<figure>
<img loading="lazy" src="/wiki/f/results/rtx-5060-dr2-quiescent-full-spectrum/232005-M9_232005/diagnostics/sf_timescales.png" alt="M9_232005: cumulative mass formed against lookback time with t10 to t90">
<figcaption><code>sf_timescales.png</code> Fraction of the final stellar mass of galaxy M9_232005 formed earlier than each lookback time. The line is the posterior median. The band is the 16-84 percent range over 400 draws. Comparison: points mark t10 to t90 with 16-84 percent (thick) and 2.5-97.5 percent (thin) intervals versus the universe age. t50 is 3.05 Gyr with a 16-84 percent range of 2.95 to 3.33 Gyr. Caveat: the 7-bin star-formation history model quantises these times to the bin edges.</figcaption>
</figure>

### 232627-M13_232627

| z | S/N | photometry χ²/N | spectrum χ²/N | f_calib | t50 [Gyr] | model |
| --- | --- | --- | --- | --- | --- | --- |
| 0.6211 | 36.4 | 7.74 | 1.042 | 4.34% | 5.80 | [parameters](/wiki/f/results/rtx-5060-dr2-quiescent-full-spectrum/232627-M13_232627/diagnostics/model_parameters.txt) |

Flags:

- photometry chi2/N 7.7 > 3
- 5 pixels with |pull| > 4

<figure>
<img loading="lazy" src="/wiki/f/results/rtx-5060-dr2-quiescent-full-spectrum/232627-M13_232627/diagnostics/photometric_chi2.png" alt="M13_232627: photometric pull and chi-squared contribution per band">
<figcaption><code>photometric_chi2.png</code> Pull and chi-squared contribution for the 12 COSMOS2015 bands of galaxy M13_232627. Pull equals observed minus model over sigma. Uncertainty: sigma includes the 5 percent flux floor. Comparison: filled points use the posterior-median model. Open squares use the best sample with the fit's own sigma. Total chi-squared 92.9 over 12 bands gives 7.74 per band. Caveat: the spectrum dominates the joint fit, so the fit does not constrain the bands on their own.</figcaption>
</figure>

<figure>
<img loading="lazy" src="/wiki/f/results/rtx-5060-dr2-quiescent-full-spectrum/232627-M13_232627/diagnostics/spectral_chi2.png" alt="M13_232627: spectral pull, binned mean pull squared, cumulative chi-squared">
<figcaption><code>spectral_chi2.png</code> Pull per fitted pixel of the LEGA-C spectrum of galaxy M13_232627. Below it: mean pull squared in 25 Å bins and the cumulative chi-squared fraction against wavelength. Uncertainty: sigma includes the fitted calibration floor of 4.34 percent of the model flux. Comparison: the stored pull versus the pull at the best sample. Shaded bands mark masked pixels. Red points mark pixels with pull beyond 4 sigma. Total chi-squared 3674.8 over 3526 pixels, 5 outlier pixels. Caveat: the fitted floor absorbs model mismatch, so chi-squared near 1 does not prove a good model.</figcaption>
</figure>

<figure>
<img loading="lazy" src="/wiki/f/results/rtx-5060-dr2-quiescent-full-spectrum/232627-M13_232627/diagnostics/sf_timescales.png" alt="M13_232627: cumulative mass formed against lookback time with t10 to t90">
<figcaption><code>sf_timescales.png</code> Fraction of the final stellar mass of galaxy M13_232627 formed earlier than each lookback time. The line is the posterior median. The band is the 16-84 percent range over 400 draws. Comparison: points mark t10 to t90 with 16-84 percent (thick) and 2.5-97.5 percent (thin) intervals versus the universe age. t50 is 5.80 Gyr with a 16-84 percent range of 5.22 to 6.21 Gyr. Caveat: the 7-bin star-formation history model quantises these times to the bin edges.</figcaption>
</figure>

### 232890-M9_232890

| z | S/N | photometry χ²/N | spectrum χ²/N | f_calib | t50 [Gyr] | model |
| --- | --- | --- | --- | --- | --- | --- |
| 0.7657 | 12.6 | 2.65 | 1.111 | 3.99% | 3.00 | [parameters](/wiki/f/results/rtx-5060-dr2-quiescent-full-spectrum/232890-M9_232890/diagnostics/model_parameters.txt) |

Flags:

- 3 pixels with |pull| > 4

<figure>
<img loading="lazy" src="/wiki/f/results/rtx-5060-dr2-quiescent-full-spectrum/232890-M9_232890/diagnostics/photometric_chi2.png" alt="M9_232890: photometric pull and chi-squared contribution per band">
<figcaption><code>photometric_chi2.png</code> Pull and chi-squared contribution for the 12 COSMOS2015 bands of galaxy M9_232890. Pull equals observed minus model over sigma. Uncertainty: sigma includes the 5 percent flux floor. Comparison: filled points use the posterior-median model. Open squares use the best sample with the fit's own sigma. Total chi-squared 31.9 over 12 bands gives 2.65 per band. Caveat: the spectrum dominates the joint fit, so the fit does not constrain the bands on their own.</figcaption>
</figure>

<figure>
<img loading="lazy" src="/wiki/f/results/rtx-5060-dr2-quiescent-full-spectrum/232890-M9_232890/diagnostics/spectral_chi2.png" alt="M9_232890: spectral pull, binned mean pull squared, cumulative chi-squared">
<figcaption><code>spectral_chi2.png</code> Pull per fitted pixel of the LEGA-C spectrum of galaxy M9_232890. Below it: mean pull squared in 25 Å bins and the cumulative chi-squared fraction against wavelength. Uncertainty: sigma includes the fitted calibration floor of 3.99 percent of the model flux. Comparison: the stored pull versus the pull at the best sample. Shaded bands mark masked pixels. Red points mark pixels with pull beyond 4 sigma. Total chi-squared 3936.8 over 3545 pixels, 3 outlier pixels. Caveat: the fitted floor absorbs model mismatch, so chi-squared near 1 does not prove a good model.</figcaption>
</figure>

<figure>
<img loading="lazy" src="/wiki/f/results/rtx-5060-dr2-quiescent-full-spectrum/232890-M9_232890/diagnostics/sf_timescales.png" alt="M9_232890: cumulative mass formed against lookback time with t10 to t90">
<figcaption><code>sf_timescales.png</code> Fraction of the final stellar mass of galaxy M9_232890 formed earlier than each lookback time. The line is the posterior median. The band is the 16-84 percent range over 400 draws. Comparison: points mark t10 to t90 with 16-84 percent (thick) and 2.5-97.5 percent (thin) intervals versus the universe age. t50 is 3.00 Gyr with a 16-84 percent range of 2.97 to 3.07 Gyr. Caveat: the 7-bin star-formation history model quantises these times to the bin edges.</figcaption>
</figure>

### 232962-M11_232962

| z | S/N | photometry χ²/N | spectrum χ²/N | f_calib | t50 [Gyr] | model |
| --- | --- | --- | --- | --- | --- | --- |
| 0.6977 | 30.8 | 10.14 | 1.167 | 6.43% | 2.71 | [parameters](/wiki/f/results/rtx-5060-dr2-quiescent-full-spectrum/232962-M11_232962/diagnostics/model_parameters.txt) |

Flags:

- photometry chi2/N 10.1 > 3
- 5 pixels with |pull| > 4

<figure>
<img loading="lazy" src="/wiki/f/results/rtx-5060-dr2-quiescent-full-spectrum/232962-M11_232962/diagnostics/photometric_chi2.png" alt="M11_232962: photometric pull and chi-squared contribution per band">
<figcaption><code>photometric_chi2.png</code> Pull and chi-squared contribution for the 12 COSMOS2015 bands of galaxy M11_232962. Pull equals observed minus model over sigma. Uncertainty: sigma includes the 5 percent flux floor. Comparison: filled points use the posterior-median model. Open squares use the best sample with the fit's own sigma. Total chi-squared 121.7 over 12 bands gives 10.14 per band. Caveat: the spectrum dominates the joint fit, so the fit does not constrain the bands on their own.</figcaption>
</figure>

<figure>
<img loading="lazy" src="/wiki/f/results/rtx-5060-dr2-quiescent-full-spectrum/232962-M11_232962/diagnostics/spectral_chi2.png" alt="M11_232962: spectral pull, binned mean pull squared, cumulative chi-squared">
<figcaption><code>spectral_chi2.png</code> Pull per fitted pixel of the LEGA-C spectrum of galaxy M11_232962. Below it: mean pull squared in 25 Å bins and the cumulative chi-squared fraction against wavelength. Uncertainty: sigma includes the fitted calibration floor of 6.43 percent of the model flux. Comparison: the stored pull versus the pull at the best sample. Shaded bands mark masked pixels. Red points mark pixels with pull beyond 4 sigma. Total chi-squared 3964.4 over 3398 pixels, 5 outlier pixels. Caveat: the fitted floor absorbs model mismatch, so chi-squared near 1 does not prove a good model.</figcaption>
</figure>

<figure>
<img loading="lazy" src="/wiki/f/results/rtx-5060-dr2-quiescent-full-spectrum/232962-M11_232962/diagnostics/sf_timescales.png" alt="M11_232962: cumulative mass formed against lookback time with t10 to t90">
<figcaption><code>sf_timescales.png</code> Fraction of the final stellar mass of galaxy M11_232962 formed earlier than each lookback time. The line is the posterior median. The band is the 16-84 percent range over 400 draws. Comparison: points mark t10 to t90 with 16-84 percent (thick) and 2.5-97.5 percent (thin) intervals versus the universe age. t50 is 2.71 Gyr with a 16-84 percent range of 2.60 to 3.63 Gyr. Caveat: the 7-bin star-formation history model quantises these times to the bin edges.</figcaption>
</figure>

### 233129-M10_233129

| z | S/N | photometry χ²/N | spectrum χ²/N | f_calib | t50 [Gyr] | model |
| --- | --- | --- | --- | --- | --- | --- |
| 0.6186 | 75.5 | 14.53 | 1.057 | 2.60% | 2.62 | [parameters](/wiki/f/results/rtx-5060-dr2-quiescent-full-spectrum/233129-M10_233129/diagnostics/model_parameters.txt) |

Flags:

- photometry chi2/N 14.5 > 3
- 2 pixels with |pull| > 4

<figure>
<img loading="lazy" src="/wiki/f/results/rtx-5060-dr2-quiescent-full-spectrum/233129-M10_233129/diagnostics/photometric_chi2.png" alt="M10_233129: photometric pull and chi-squared contribution per band">
<figcaption><code>photometric_chi2.png</code> Pull and chi-squared contribution for the 12 COSMOS2015 bands of galaxy M10_233129. Pull equals observed minus model over sigma. Uncertainty: sigma includes the 5 percent flux floor. Comparison: filled points use the posterior-median model. Open squares use the best sample with the fit's own sigma. Total chi-squared 174.3 over 12 bands gives 14.53 per band. Caveat: the spectrum dominates the joint fit, so the fit does not constrain the bands on their own.</figcaption>
</figure>

<figure>
<img loading="lazy" src="/wiki/f/results/rtx-5060-dr2-quiescent-full-spectrum/233129-M10_233129/diagnostics/spectral_chi2.png" alt="M10_233129: spectral pull, binned mean pull squared, cumulative chi-squared">
<figcaption><code>spectral_chi2.png</code> Pull per fitted pixel of the LEGA-C spectrum of galaxy M10_233129. Below it: mean pull squared in 25 Å bins and the cumulative chi-squared fraction against wavelength. Uncertainty: sigma includes the fitted calibration floor of 2.60 percent of the model flux. Comparison: the stored pull versus the pull at the best sample. Shaded bands mark masked pixels. Red points mark pixels with pull beyond 4 sigma. Total chi-squared 3653.1 over 3456 pixels, 2 outlier pixels. Caveat: the fitted floor absorbs model mismatch, so chi-squared near 1 does not prove a good model.</figcaption>
</figure>

<figure>
<img loading="lazy" src="/wiki/f/results/rtx-5060-dr2-quiescent-full-spectrum/233129-M10_233129/diagnostics/sf_timescales.png" alt="M10_233129: cumulative mass formed against lookback time with t10 to t90">
<figcaption><code>sf_timescales.png</code> Fraction of the final stellar mass of galaxy M10_233129 formed earlier than each lookback time. The line is the posterior median. The band is the 16-84 percent range over 400 draws. Comparison: points mark t10 to t90 with 16-84 percent (thick) and 2.5-97.5 percent (thin) intervals versus the universe age. t50 is 2.62 Gyr with a 16-84 percent range of 2.59 to 2.65 Gyr. Caveat: the 7-bin star-formation history model quantises these times to the bin edges.</figcaption>
</figure>

### 233169-M9_233169

| z | S/N | photometry χ²/N | spectrum χ²/N | f_calib | t50 [Gyr] | model |
| --- | --- | --- | --- | --- | --- | --- |
| 0.6104 | 51.4 | 8.01 | 1.046 | 3.10% | 5.41 | [parameters](/wiki/f/results/rtx-5060-dr2-quiescent-full-spectrum/233169-M9_233169/diagnostics/model_parameters.txt) |

Flags:

- photometry chi2/N 8.0 > 3
- 4 pixels with |pull| > 4

<figure>
<img loading="lazy" src="/wiki/f/results/rtx-5060-dr2-quiescent-full-spectrum/233169-M9_233169/diagnostics/photometric_chi2.png" alt="M9_233169: photometric pull and chi-squared contribution per band">
<figcaption><code>photometric_chi2.png</code> Pull and chi-squared contribution for the 12 COSMOS2015 bands of galaxy M9_233169. Pull equals observed minus model over sigma. Uncertainty: sigma includes the 5 percent flux floor. Comparison: filled points use the posterior-median model. Open squares use the best sample with the fit's own sigma. Total chi-squared 96.1 over 12 bands gives 8.01 per band. Caveat: the spectrum dominates the joint fit, so the fit does not constrain the bands on their own.</figcaption>
</figure>

<figure>
<img loading="lazy" src="/wiki/f/results/rtx-5060-dr2-quiescent-full-spectrum/233169-M9_233169/diagnostics/spectral_chi2.png" alt="M9_233169: spectral pull, binned mean pull squared, cumulative chi-squared">
<figcaption><code>spectral_chi2.png</code> Pull per fitted pixel of the LEGA-C spectrum of galaxy M9_233169. Below it: mean pull squared in 25 Å bins and the cumulative chi-squared fraction against wavelength. Uncertainty: sigma includes the fitted calibration floor of 3.10 percent of the model flux. Comparison: the stored pull versus the pull at the best sample. Shaded bands mark masked pixels. Red points mark pixels with pull beyond 4 sigma. Total chi-squared 3661.0 over 3500 pixels, 4 outlier pixels. Caveat: the fitted floor absorbs model mismatch, so chi-squared near 1 does not prove a good model.</figcaption>
</figure>

<figure>
<img loading="lazy" src="/wiki/f/results/rtx-5060-dr2-quiescent-full-spectrum/233169-M9_233169/diagnostics/sf_timescales.png" alt="M9_233169: cumulative mass formed against lookback time with t10 to t90">
<figcaption><code>sf_timescales.png</code> Fraction of the final stellar mass of galaxy M9_233169 formed earlier than each lookback time. The line is the posterior median. The band is the 16-84 percent range over 400 draws. Comparison: points mark t10 to t90 with 16-84 percent (thick) and 2.5-97.5 percent (thin) intervals versus the universe age. t50 is 5.41 Gyr with a 16-84 percent range of 5.19 to 5.66 Gyr. Caveat: the 7-bin star-formation history model quantises these times to the bin edges.</figcaption>
</figure>

### 233902-M6_233902

| z | S/N | photometry χ²/N | spectrum χ²/N | f_calib | t50 [Gyr] | model |
| --- | --- | --- | --- | --- | --- | --- |
| 0.7293 | 19.1 | 3.20 | 1.098 | 5.84% | 4.44 | [parameters](/wiki/f/results/rtx-5060-dr2-quiescent-full-spectrum/233902-M6_233902/diagnostics/model_parameters.txt) |

Flags:

- photometry chi2/N 3.2 > 3
- 2 pixels with |pull| > 4

<figure>
<img loading="lazy" src="/wiki/f/results/rtx-5060-dr2-quiescent-full-spectrum/233902-M6_233902/diagnostics/photometric_chi2.png" alt="M6_233902: photometric pull and chi-squared contribution per band">
<figcaption><code>photometric_chi2.png</code> Pull and chi-squared contribution for the 12 COSMOS2015 bands of galaxy M6_233902. Pull equals observed minus model over sigma. Uncertainty: sigma includes the 5 percent flux floor. Comparison: filled points use the posterior-median model. Open squares use the best sample with the fit's own sigma. Total chi-squared 38.4 over 12 bands gives 3.20 per band. Caveat: the spectrum dominates the joint fit, so the fit does not constrain the bands on their own.</figcaption>
</figure>

<figure>
<img loading="lazy" src="/wiki/f/results/rtx-5060-dr2-quiescent-full-spectrum/233902-M6_233902/diagnostics/spectral_chi2.png" alt="M6_233902: spectral pull, binned mean pull squared, cumulative chi-squared">
<figcaption><code>spectral_chi2.png</code> Pull per fitted pixel of the LEGA-C spectrum of galaxy M6_233902. Below it: mean pull squared in 25 Å bins and the cumulative chi-squared fraction against wavelength. Uncertainty: sigma includes the fitted calibration floor of 5.84 percent of the model flux. Comparison: the stored pull versus the pull at the best sample. Shaded bands mark masked pixels. Red points mark pixels with pull beyond 4 sigma. Total chi-squared 3712.3 over 3382 pixels, 2 outlier pixels. Caveat: the fitted floor absorbs model mismatch, so chi-squared near 1 does not prove a good model.</figcaption>
</figure>

<figure>
<img loading="lazy" src="/wiki/f/results/rtx-5060-dr2-quiescent-full-spectrum/233902-M6_233902/diagnostics/sf_timescales.png" alt="M6_233902: cumulative mass formed against lookback time with t10 to t90">
<figcaption><code>sf_timescales.png</code> Fraction of the final stellar mass of galaxy M6_233902 formed earlier than each lookback time. The line is the posterior median. The band is the 16-84 percent range over 400 draws. Comparison: points mark t10 to t90 with 16-84 percent (thick) and 2.5-97.5 percent (thin) intervals versus the universe age. t50 is 4.44 Gyr with a 16-84 percent range of 3.88 to 5.49 Gyr. Caveat: the 7-bin star-formation history model quantises these times to the bin edges.</figcaption>
</figure>

### 236682-M5_236682

| z | S/N | photometry χ²/N | spectrum χ²/N | f_calib | t50 [Gyr] | model |
| --- | --- | --- | --- | --- | --- | --- |
| 0.7342 | 31.6 | 8.51 | 1.145 | 4.38% | 3.22 | [parameters](/wiki/f/results/rtx-5060-dr2-quiescent-full-spectrum/236682-M5_236682/diagnostics/model_parameters.txt) |

Flags:

- photometry chi2/N 8.5 > 3
- 2 pixels with |pull| > 4

<figure>
<img loading="lazy" src="/wiki/f/results/rtx-5060-dr2-quiescent-full-spectrum/236682-M5_236682/diagnostics/photometric_chi2.png" alt="M5_236682: photometric pull and chi-squared contribution per band">
<figcaption><code>photometric_chi2.png</code> Pull and chi-squared contribution for the 12 COSMOS2015 bands of galaxy M5_236682. Pull equals observed minus model over sigma. Uncertainty: sigma includes the 5 percent flux floor. Comparison: filled points use the posterior-median model. Open squares use the best sample with the fit's own sigma. Total chi-squared 102.1 over 12 bands gives 8.51 per band. Caveat: the spectrum dominates the joint fit, so the fit does not constrain the bands on their own.</figcaption>
</figure>

<figure>
<img loading="lazy" src="/wiki/f/results/rtx-5060-dr2-quiescent-full-spectrum/236682-M5_236682/diagnostics/spectral_chi2.png" alt="M5_236682: spectral pull, binned mean pull squared, cumulative chi-squared">
<figcaption><code>spectral_chi2.png</code> Pull per fitted pixel of the LEGA-C spectrum of galaxy M5_236682. Below it: mean pull squared in 25 Å bins and the cumulative chi-squared fraction against wavelength. Uncertainty: sigma includes the fitted calibration floor of 4.38 percent of the model flux. Comparison: the stored pull versus the pull at the best sample. Shaded bands mark masked pixels. Red points mark pixels with pull beyond 4 sigma. Total chi-squared 3877.2 over 3387 pixels, 2 outlier pixels. Caveat: the fitted floor absorbs model mismatch, so chi-squared near 1 does not prove a good model.</figcaption>
</figure>

<figure>
<img loading="lazy" src="/wiki/f/results/rtx-5060-dr2-quiescent-full-spectrum/236682-M5_236682/diagnostics/sf_timescales.png" alt="M5_236682: cumulative mass formed against lookback time with t10 to t90">
<figcaption><code>sf_timescales.png</code> Fraction of the final stellar mass of galaxy M5_236682 formed earlier than each lookback time. The line is the posterior median. The band is the 16-84 percent range over 400 draws. Comparison: points mark t10 to t90 with 16-84 percent (thick) and 2.5-97.5 percent (thin) intervals versus the universe age. t50 is 3.22 Gyr with a 16-84 percent range of 3.02 to 3.38 Gyr. Caveat: the 7-bin star-formation history model quantises these times to the bin edges.</figcaption>
</figure>

### 236994-M5_236994

| z | S/N | photometry χ²/N | spectrum χ²/N | f_calib | t50 [Gyr] | model |
| --- | --- | --- | --- | --- | --- | --- |
| 0.7297 | 31.8 | 16.09 | 1.151 | 4.36% | 2.87 | [parameters](/wiki/f/results/rtx-5060-dr2-quiescent-full-spectrum/236994-M5_236994/diagnostics/model_parameters.txt) |

Flags:

- photometry chi2/N 16.1 > 3
- 10 pixels with |pull| > 4

<figure>
<img loading="lazy" src="/wiki/f/results/rtx-5060-dr2-quiescent-full-spectrum/236994-M5_236994/diagnostics/photometric_chi2.png" alt="M5_236994: photometric pull and chi-squared contribution per band">
<figcaption><code>photometric_chi2.png</code> Pull and chi-squared contribution for the 12 COSMOS2015 bands of galaxy M5_236994. Pull equals observed minus model over sigma. Uncertainty: sigma includes the 5 percent flux floor. Comparison: filled points use the posterior-median model. Open squares use the best sample with the fit's own sigma. Total chi-squared 193.1 over 12 bands gives 16.09 per band. Caveat: the spectrum dominates the joint fit, so the fit does not constrain the bands on their own.</figcaption>
</figure>

<figure>
<img loading="lazy" src="/wiki/f/results/rtx-5060-dr2-quiescent-full-spectrum/236994-M5_236994/diagnostics/spectral_chi2.png" alt="M5_236994: spectral pull, binned mean pull squared, cumulative chi-squared">
<figcaption><code>spectral_chi2.png</code> Pull per fitted pixel of the LEGA-C spectrum of galaxy M5_236994. Below it: mean pull squared in 25 Å bins and the cumulative chi-squared fraction against wavelength. Uncertainty: sigma includes the fitted calibration floor of 4.36 percent of the model flux. Comparison: the stored pull versus the pull at the best sample. Shaded bands mark masked pixels. Red points mark pixels with pull beyond 4 sigma. Total chi-squared 3939.5 over 3423 pixels, 10 outlier pixels. Caveat: the fitted floor absorbs model mismatch, so chi-squared near 1 does not prove a good model.</figcaption>
</figure>

<figure>
<img loading="lazy" src="/wiki/f/results/rtx-5060-dr2-quiescent-full-spectrum/236994-M5_236994/diagnostics/sf_timescales.png" alt="M5_236994: cumulative mass formed against lookback time with t10 to t90">
<figcaption><code>sf_timescales.png</code> Fraction of the final stellar mass of galaxy M5_236994 formed earlier than each lookback time. The line is the posterior median. The band is the 16-84 percent range over 400 draws. Comparison: points mark t10 to t90 with 16-84 percent (thick) and 2.5-97.5 percent (thin) intervals versus the universe age. t50 is 2.87 Gyr with a 16-84 percent range of 2.84 to 2.92 Gyr. Caveat: the 7-bin star-formation history model quantises these times to the bin edges.</figcaption>
</figure>

### 237437-M6_237437

| z | S/N | photometry χ²/N | spectrum χ²/N | f_calib | t50 [Gyr] | model |
| --- | --- | --- | --- | --- | --- | --- |
| 0.7337 | 25.0 | 6.08 | 1.214 | 4.45% | 3.06 | [parameters](/wiki/f/results/rtx-5060-dr2-quiescent-full-spectrum/237437-M6_237437/diagnostics/model_parameters.txt) |

Flags:

- photometry chi2/N 6.1 > 3
- 6 pixels with |pull| > 4

<figure>
<img loading="lazy" src="/wiki/f/results/rtx-5060-dr2-quiescent-full-spectrum/237437-M6_237437/diagnostics/photometric_chi2.png" alt="M6_237437: photometric pull and chi-squared contribution per band">
<figcaption><code>photometric_chi2.png</code> Pull and chi-squared contribution for the 12 COSMOS2015 bands of galaxy M6_237437. Pull equals observed minus model over sigma. Uncertainty: sigma includes the 5 percent flux floor. Comparison: filled points use the posterior-median model. Open squares use the best sample with the fit's own sigma. Total chi-squared 72.9 over 12 bands gives 6.08 per band. Caveat: the spectrum dominates the joint fit, so the fit does not constrain the bands on their own.</figcaption>
</figure>

<figure>
<img loading="lazy" src="/wiki/f/results/rtx-5060-dr2-quiescent-full-spectrum/237437-M6_237437/diagnostics/spectral_chi2.png" alt="M6_237437: spectral pull, binned mean pull squared, cumulative chi-squared">
<figcaption><code>spectral_chi2.png</code> Pull per fitted pixel of the LEGA-C spectrum of galaxy M6_237437. Below it: mean pull squared in 25 Å bins and the cumulative chi-squared fraction against wavelength. Uncertainty: sigma includes the fitted calibration floor of 4.45 percent of the model flux. Comparison: the stored pull versus the pull at the best sample. Shaded bands mark masked pixels. Red points mark pixels with pull beyond 4 sigma. Total chi-squared 4203.0 over 3463 pixels, 6 outlier pixels. Caveat: the fitted floor absorbs model mismatch, so chi-squared near 1 does not prove a good model.</figcaption>
</figure>

<figure>
<img loading="lazy" src="/wiki/f/results/rtx-5060-dr2-quiescent-full-spectrum/237437-M6_237437/diagnostics/sf_timescales.png" alt="M6_237437: cumulative mass formed against lookback time with t10 to t90">
<figcaption><code>sf_timescales.png</code> Fraction of the final stellar mass of galaxy M6_237437 formed earlier than each lookback time. The line is the posterior median. The band is the 16-84 percent range over 400 draws. Comparison: points mark t10 to t90 with 16-84 percent (thick) and 2.5-97.5 percent (thin) intervals versus the universe age. t50 is 3.06 Gyr with a 16-84 percent range of 3.00 to 3.30 Gyr. Caveat: the 7-bin star-formation history model quantises these times to the bin edges.</figcaption>
</figure>

### 237641-M6_237641

| z | S/N | photometry χ²/N | spectrum χ²/N | f_calib | t50 [Gyr] | model |
| --- | --- | --- | --- | --- | --- | --- |
| 0.8579 | 19.3 | 3.11 | 1.139 | 6.25% | 2.81 | [parameters](/wiki/f/results/rtx-5060-dr2-quiescent-full-spectrum/237641-M6_237641/diagnostics/model_parameters.txt) |

Flags:

- photometry chi2/N 3.1 > 3
- 6 pixels with |pull| > 4

<figure>
<img loading="lazy" src="/wiki/f/results/rtx-5060-dr2-quiescent-full-spectrum/237641-M6_237641/diagnostics/photometric_chi2.png" alt="M6_237641: photometric pull and chi-squared contribution per band">
<figcaption><code>photometric_chi2.png</code> Pull and chi-squared contribution for the 12 COSMOS2015 bands of galaxy M6_237641. Pull equals observed minus model over sigma. Uncertainty: sigma includes the 5 percent flux floor. Comparison: filled points use the posterior-median model. Open squares use the best sample with the fit's own sigma. Total chi-squared 37.3 over 12 bands gives 3.11 per band. Caveat: the spectrum dominates the joint fit, so the fit does not constrain the bands on their own.</figcaption>
</figure>

<figure>
<img loading="lazy" src="/wiki/f/results/rtx-5060-dr2-quiescent-full-spectrum/237641-M6_237641/diagnostics/spectral_chi2.png" alt="M6_237641: spectral pull, binned mean pull squared, cumulative chi-squared">
<figcaption><code>spectral_chi2.png</code> Pull per fitted pixel of the LEGA-C spectrum of galaxy M6_237641. Below it: mean pull squared in 25 Å bins and the cumulative chi-squared fraction against wavelength. Uncertainty: sigma includes the fitted calibration floor of 6.25 percent of the model flux. Comparison: the stored pull versus the pull at the best sample. Shaded bands mark masked pixels. Red points mark pixels with pull beyond 4 sigma. Total chi-squared 3907.8 over 3432 pixels, 6 outlier pixels. Caveat: the fitted floor absorbs model mismatch, so chi-squared near 1 does not prove a good model.</figcaption>
</figure>

<figure>
<img loading="lazy" src="/wiki/f/results/rtx-5060-dr2-quiescent-full-spectrum/237641-M6_237641/diagnostics/sf_timescales.png" alt="M6_237641: cumulative mass formed against lookback time with t10 to t90">
<figcaption><code>sf_timescales.png</code> Fraction of the final stellar mass of galaxy M6_237641 formed earlier than each lookback time. The line is the posterior median. The band is the 16-84 percent range over 400 draws. Comparison: points mark t10 to t90 with 16-84 percent (thick) and 2.5-97.5 percent (thin) intervals versus the universe age. t50 is 2.81 Gyr with a 16-84 percent range of 2.74 to 2.90 Gyr. Caveat: the 7-bin star-formation history model quantises these times to the bin edges.</figcaption>
</figure>

### 238314-M5_238314

| z | S/N | photometry χ²/N | spectrum χ²/N | f_calib | t50 [Gyr] | model |
| --- | --- | --- | --- | --- | --- | --- |
| 0.7320 | 34.6 | 7.36 | 1.179 | 4.53% | 3.04 | [parameters](/wiki/f/results/rtx-5060-dr2-quiescent-full-spectrum/238314-M5_238314/diagnostics/model_parameters.txt) |

Flags:

- photometry chi2/N 7.4 > 3
- 7 pixels with |pull| > 4

<figure>
<img loading="lazy" src="/wiki/f/results/rtx-5060-dr2-quiescent-full-spectrum/238314-M5_238314/diagnostics/photometric_chi2.png" alt="M5_238314: photometric pull and chi-squared contribution per band">
<figcaption><code>photometric_chi2.png</code> Pull and chi-squared contribution for the 12 COSMOS2015 bands of galaxy M5_238314. Pull equals observed minus model over sigma. Uncertainty: sigma includes the 5 percent flux floor. Comparison: filled points use the posterior-median model. Open squares use the best sample with the fit's own sigma. Total chi-squared 88.3 over 12 bands gives 7.36 per band. Caveat: the spectrum dominates the joint fit, so the fit does not constrain the bands on their own.</figcaption>
</figure>

<figure>
<img loading="lazy" src="/wiki/f/results/rtx-5060-dr2-quiescent-full-spectrum/238314-M5_238314/diagnostics/spectral_chi2.png" alt="M5_238314: spectral pull, binned mean pull squared, cumulative chi-squared">
<figcaption><code>spectral_chi2.png</code> Pull per fitted pixel of the LEGA-C spectrum of galaxy M5_238314. Below it: mean pull squared in 25 Å bins and the cumulative chi-squared fraction against wavelength. Uncertainty: sigma includes the fitted calibration floor of 4.53 percent of the model flux. Comparison: the stored pull versus the pull at the best sample. Shaded bands mark masked pixels. Red points mark pixels with pull beyond 4 sigma. Total chi-squared 4027.5 over 3417 pixels, 7 outlier pixels. Caveat: the fitted floor absorbs model mismatch, so chi-squared near 1 does not prove a good model.</figcaption>
</figure>

<figure>
<img loading="lazy" src="/wiki/f/results/rtx-5060-dr2-quiescent-full-spectrum/238314-M5_238314/diagnostics/sf_timescales.png" alt="M5_238314: cumulative mass formed against lookback time with t10 to t90">
<figcaption><code>sf_timescales.png</code> Fraction of the final stellar mass of galaxy M5_238314 formed earlier than each lookback time. The line is the posterior median. The band is the 16-84 percent range over 400 draws. Comparison: points mark t10 to t90 with 16-84 percent (thick) and 2.5-97.5 percent (thin) intervals versus the universe age. t50 is 3.04 Gyr with a 16-84 percent range of 3.00 to 3.18 Gyr. Caveat: the 7-bin star-formation history model quantises these times to the bin edges.</figcaption>
</figure>

### 238580-M5_238580

| z | S/N | photometry χ²/N | spectrum χ²/N | f_calib | t50 [Gyr] | model |
| --- | --- | --- | --- | --- | --- | --- |
| 0.7304 | 24.3 | 7.11 | 1.151 | 6.16% | 5.91 | [parameters](/wiki/f/results/rtx-5060-dr2-quiescent-full-spectrum/238580-M5_238580/diagnostics/model_parameters.txt) |

Flags:

- photometry chi2/N 7.1 > 3
- 21 pixels with |pull| > 4

<figure>
<img loading="lazy" src="/wiki/f/results/rtx-5060-dr2-quiescent-full-spectrum/238580-M5_238580/diagnostics/photometric_chi2.png" alt="M5_238580: photometric pull and chi-squared contribution per band">
<figcaption><code>photometric_chi2.png</code> Pull and chi-squared contribution for the 12 COSMOS2015 bands of galaxy M5_238580. Pull equals observed minus model over sigma. Uncertainty: sigma includes the 5 percent flux floor. Comparison: filled points use the posterior-median model. Open squares use the best sample with the fit's own sigma. Total chi-squared 85.3 over 12 bands gives 7.11 per band. Caveat: the spectrum dominates the joint fit, so the fit does not constrain the bands on their own.</figcaption>
</figure>

<figure>
<img loading="lazy" src="/wiki/f/results/rtx-5060-dr2-quiescent-full-spectrum/238580-M5_238580/diagnostics/spectral_chi2.png" alt="M5_238580: spectral pull, binned mean pull squared, cumulative chi-squared">
<figcaption><code>spectral_chi2.png</code> Pull per fitted pixel of the LEGA-C spectrum of galaxy M5_238580. Below it: mean pull squared in 25 Å bins and the cumulative chi-squared fraction against wavelength. Uncertainty: sigma includes the fitted calibration floor of 6.16 percent of the model flux. Comparison: the stored pull versus the pull at the best sample. Shaded bands mark masked pixels. Red points mark pixels with pull beyond 4 sigma. Total chi-squared 4093.7 over 3557 pixels, 21 outlier pixels. Caveat: the fitted floor absorbs model mismatch, so chi-squared near 1 does not prove a good model.</figcaption>
</figure>

<figure>
<img loading="lazy" src="/wiki/f/results/rtx-5060-dr2-quiescent-full-spectrum/238580-M5_238580/diagnostics/sf_timescales.png" alt="M5_238580: cumulative mass formed against lookback time with t10 to t90">
<figcaption><code>sf_timescales.png</code> Fraction of the final stellar mass of galaxy M5_238580 formed earlier than each lookback time. The line is the posterior median. The band is the 16-84 percent range over 400 draws. Comparison: points mark t10 to t90 with 16-84 percent (thick) and 2.5-97.5 percent (thin) intervals versus the universe age. t50 is 5.91 Gyr with a 16-84 percent range of 5.89 to 5.92 Gyr. Caveat: the 7-bin star-formation history model quantises these times to the bin edges.</figcaption>
</figure>

### 240899-M6_240899

| z | S/N | photometry χ²/N | spectrum χ²/N | f_calib | t50 [Gyr] | model |
| --- | --- | --- | --- | --- | --- | --- |
| 0.7395 | 15.6 | 4.99 | 1.148 | 5.56% | 2.91 | [parameters](/wiki/f/results/rtx-5060-dr2-quiescent-full-spectrum/240899-M6_240899/diagnostics/model_parameters.txt) |

Flags:

- photometry chi2/N 5.0 > 3
- 4 pixels with |pull| > 4

<figure>
<img loading="lazy" src="/wiki/f/results/rtx-5060-dr2-quiescent-full-spectrum/240899-M6_240899/diagnostics/photometric_chi2.png" alt="M6_240899: photometric pull and chi-squared contribution per band">
<figcaption><code>photometric_chi2.png</code> Pull and chi-squared contribution for the 12 COSMOS2015 bands of galaxy M6_240899. Pull equals observed minus model over sigma. Uncertainty: sigma includes the 5 percent flux floor. Comparison: filled points use the posterior-median model. Open squares use the best sample with the fit's own sigma. Total chi-squared 59.9 over 12 bands gives 4.99 per band. Caveat: the spectrum dominates the joint fit, so the fit does not constrain the bands on their own.</figcaption>
</figure>

<figure>
<img loading="lazy" src="/wiki/f/results/rtx-5060-dr2-quiescent-full-spectrum/240899-M6_240899/diagnostics/spectral_chi2.png" alt="M6_240899: spectral pull, binned mean pull squared, cumulative chi-squared">
<figcaption><code>spectral_chi2.png</code> Pull per fitted pixel of the LEGA-C spectrum of galaxy M6_240899. Below it: mean pull squared in 25 Å bins and the cumulative chi-squared fraction against wavelength. Uncertainty: sigma includes the fitted calibration floor of 5.56 percent of the model flux. Comparison: the stored pull versus the pull at the best sample. Shaded bands mark masked pixels. Red points mark pixels with pull beyond 4 sigma. Total chi-squared 3995.2 over 3479 pixels, 4 outlier pixels. Caveat: the fitted floor absorbs model mismatch, so chi-squared near 1 does not prove a good model.</figcaption>
</figure>

<figure>
<img loading="lazy" src="/wiki/f/results/rtx-5060-dr2-quiescent-full-spectrum/240899-M6_240899/diagnostics/sf_timescales.png" alt="M6_240899: cumulative mass formed against lookback time with t10 to t90">
<figcaption><code>sf_timescales.png</code> Fraction of the final stellar mass of galaxy M6_240899 formed earlier than each lookback time. The line is the posterior median. The band is the 16-84 percent range over 400 draws. Comparison: points mark t10 to t90 with 16-84 percent (thick) and 2.5-97.5 percent (thin) intervals versus the universe age. t50 is 2.91 Gyr with a 16-84 percent range of 2.63 to 4.17 Gyr. Caveat: the 7-bin star-formation history model quantises these times to the bin edges.</figcaption>
</figure>

### 241189-M5_241189

| z | S/N | photometry χ²/N | spectrum χ²/N | f_calib | t50 [Gyr] | model |
| --- | --- | --- | --- | --- | --- | --- |
| 0.7287 | 29.0 | 6.24 | 1.113 | 3.96% | 3.23 | [parameters](/wiki/f/results/rtx-5060-dr2-quiescent-full-spectrum/241189-M5_241189/diagnostics/model_parameters.txt) |

Flags:

- photometry chi2/N 6.2 > 3
- 4 pixels with |pull| > 4

<figure>
<img loading="lazy" src="/wiki/f/results/rtx-5060-dr2-quiescent-full-spectrum/241189-M5_241189/diagnostics/photometric_chi2.png" alt="M5_241189: photometric pull and chi-squared contribution per band">
<figcaption><code>photometric_chi2.png</code> Pull and chi-squared contribution for the 12 COSMOS2015 bands of galaxy M5_241189. Pull equals observed minus model over sigma. Uncertainty: sigma includes the 5 percent flux floor. Comparison: filled points use the posterior-median model. Open squares use the best sample with the fit's own sigma. Total chi-squared 74.9 over 12 bands gives 6.24 per band. Caveat: the spectrum dominates the joint fit, so the fit does not constrain the bands on their own.</figcaption>
</figure>

<figure>
<img loading="lazy" src="/wiki/f/results/rtx-5060-dr2-quiescent-full-spectrum/241189-M5_241189/diagnostics/spectral_chi2.png" alt="M5_241189: spectral pull, binned mean pull squared, cumulative chi-squared">
<figcaption><code>spectral_chi2.png</code> Pull per fitted pixel of the LEGA-C spectrum of galaxy M5_241189. Below it: mean pull squared in 25 Å bins and the cumulative chi-squared fraction against wavelength. Uncertainty: sigma includes the fitted calibration floor of 3.96 percent of the model flux. Comparison: the stored pull versus the pull at the best sample. Shaded bands mark masked pixels. Red points mark pixels with pull beyond 4 sigma. Total chi-squared 3850.9 over 3459 pixels, 4 outlier pixels. Caveat: the fitted floor absorbs model mismatch, so chi-squared near 1 does not prove a good model.</figcaption>
</figure>

<figure>
<img loading="lazy" src="/wiki/f/results/rtx-5060-dr2-quiescent-full-spectrum/241189-M5_241189/diagnostics/sf_timescales.png" alt="M5_241189: cumulative mass formed against lookback time with t10 to t90">
<figcaption><code>sf_timescales.png</code> Fraction of the final stellar mass of galaxy M5_241189 formed earlier than each lookback time. The line is the posterior median. The band is the 16-84 percent range over 400 draws. Comparison: points mark t10 to t90 with 16-84 percent (thick) and 2.5-97.5 percent (thin) intervals versus the universe age. t50 is 3.23 Gyr with a 16-84 percent range of 3.02 to 3.41 Gyr. Caveat: the 7-bin star-formation history model quantises these times to the bin edges.</figcaption>
</figure>

### 243871-M13_243871

| z | S/N | photometry χ²/N | spectrum χ²/N | f_calib | t50 [Gyr] | model |
| --- | --- | --- | --- | --- | --- | --- |
| 0.7334 | 22.3 | 1.87 | 1.084 | 6.40% | 2.92 | [parameters](/wiki/f/results/rtx-5060-dr2-quiescent-full-spectrum/243871-M13_243871/diagnostics/model_parameters.txt) |

Flags:

- 1 pixels with |pull| > 4

<figure>
<img loading="lazy" src="/wiki/f/results/rtx-5060-dr2-quiescent-full-spectrum/243871-M13_243871/diagnostics/photometric_chi2.png" alt="M13_243871: photometric pull and chi-squared contribution per band">
<figcaption><code>photometric_chi2.png</code> Pull and chi-squared contribution for the 12 COSMOS2015 bands of galaxy M13_243871. Pull equals observed minus model over sigma. Uncertainty: sigma includes the 5 percent flux floor. Comparison: filled points use the posterior-median model. Open squares use the best sample with the fit's own sigma. Total chi-squared 22.4 over 12 bands gives 1.87 per band. Caveat: the spectrum dominates the joint fit, so the fit does not constrain the bands on their own.</figcaption>
</figure>

<figure>
<img loading="lazy" src="/wiki/f/results/rtx-5060-dr2-quiescent-full-spectrum/243871-M13_243871/diagnostics/spectral_chi2.png" alt="M13_243871: spectral pull, binned mean pull squared, cumulative chi-squared">
<figcaption><code>spectral_chi2.png</code> Pull per fitted pixel of the LEGA-C spectrum of galaxy M13_243871. Below it: mean pull squared in 25 Å bins and the cumulative chi-squared fraction against wavelength. Uncertainty: sigma includes the fitted calibration floor of 6.40 percent of the model flux. Comparison: the stored pull versus the pull at the best sample. Shaded bands mark masked pixels. Red points mark pixels with pull beyond 4 sigma. Total chi-squared 3837.7 over 3539 pixels, 1 outlier pixels. Caveat: the fitted floor absorbs model mismatch, so chi-squared near 1 does not prove a good model.</figcaption>
</figure>

<figure>
<img loading="lazy" src="/wiki/f/results/rtx-5060-dr2-quiescent-full-spectrum/243871-M13_243871/diagnostics/sf_timescales.png" alt="M13_243871: cumulative mass formed against lookback time with t10 to t90">
<figcaption><code>sf_timescales.png</code> Fraction of the final stellar mass of galaxy M13_243871 formed earlier than each lookback time. The line is the posterior median. The band is the 16-84 percent range over 400 draws. Comparison: points mark t10 to t90 with 16-84 percent (thick) and 2.5-97.5 percent (thin) intervals versus the universe age. t50 is 2.92 Gyr with a 16-84 percent range of 2.71 to 3.43 Gyr. Caveat: the 7-bin star-formation history model quantises these times to the bin edges.</figcaption>
</figure>

### 244239-M13_244239

| z | S/N | photometry χ²/N | spectrum χ²/N | f_calib | t50 [Gyr] | model |
| --- | --- | --- | --- | --- | --- | --- |
| 0.7378 | 24.5 | 3.83 | 1.113 | 5.26% | 3.04 | [parameters](/wiki/f/results/rtx-5060-dr2-quiescent-full-spectrum/244239-M13_244239/diagnostics/model_parameters.txt) |

Flags:

- photometry chi2/N 3.8 > 3
- 1 pixels with |pull| > 4

<figure>
<img loading="lazy" src="/wiki/f/results/rtx-5060-dr2-quiescent-full-spectrum/244239-M13_244239/diagnostics/photometric_chi2.png" alt="M13_244239: photometric pull and chi-squared contribution per band">
<figcaption><code>photometric_chi2.png</code> Pull and chi-squared contribution for the 12 COSMOS2015 bands of galaxy M13_244239. Pull equals observed minus model over sigma. Uncertainty: sigma includes the 5 percent flux floor. Comparison: filled points use the posterior-median model. Open squares use the best sample with the fit's own sigma. Total chi-squared 45.9 over 12 bands gives 3.83 per band. Caveat: the spectrum dominates the joint fit, so the fit does not constrain the bands on their own.</figcaption>
</figure>

<figure>
<img loading="lazy" src="/wiki/f/results/rtx-5060-dr2-quiescent-full-spectrum/244239-M13_244239/diagnostics/spectral_chi2.png" alt="M13_244239: spectral pull, binned mean pull squared, cumulative chi-squared">
<figcaption><code>spectral_chi2.png</code> Pull per fitted pixel of the LEGA-C spectrum of galaxy M13_244239. Below it: mean pull squared in 25 Å bins and the cumulative chi-squared fraction against wavelength. Uncertainty: sigma includes the fitted calibration floor of 5.26 percent of the model flux. Comparison: the stored pull versus the pull at the best sample. Shaded bands mark masked pixels. Red points mark pixels with pull beyond 4 sigma. Total chi-squared 3971.3 over 3568 pixels, 1 outlier pixels. Caveat: the fitted floor absorbs model mismatch, so chi-squared near 1 does not prove a good model.</figcaption>
</figure>

<figure>
<img loading="lazy" src="/wiki/f/results/rtx-5060-dr2-quiescent-full-spectrum/244239-M13_244239/diagnostics/sf_timescales.png" alt="M13_244239: cumulative mass formed against lookback time with t10 to t90">
<figcaption><code>sf_timescales.png</code> Fraction of the final stellar mass of galaxy M13_244239 formed earlier than each lookback time. The line is the posterior median. The band is the 16-84 percent range over 400 draws. Comparison: points mark t10 to t90 with 16-84 percent (thick) and 2.5-97.5 percent (thin) intervals versus the universe age. t50 is 3.04 Gyr with a 16-84 percent range of 3.00 to 3.14 Gyr. Caveat: the 7-bin star-formation history model quantises these times to the bin edges.</figcaption>
</figure>

### 244680-M13_244680

| z | S/N | photometry χ²/N | spectrum χ²/N | f_calib | t50 [Gyr] | model |
| --- | --- | --- | --- | --- | --- | --- |
| 0.9576 | 4.4 | 3.66 | 1.549 | 9.98% | 2.99 | [parameters](/wiki/f/results/rtx-5060-dr2-quiescent-full-spectrum/244680-M13_244680/diagnostics/model_parameters.txt) |

Flags:

- photometry chi2/N 3.7 > 3
- spectrum chi2/N 1.55 > 1.5
- calibration floor at prior bound (10.0% of 10%)
- 13 pixels with |pull| > 4

<figure>
<img loading="lazy" src="/wiki/f/results/rtx-5060-dr2-quiescent-full-spectrum/244680-M13_244680/diagnostics/photometric_chi2.png" alt="M13_244680: photometric pull and chi-squared contribution per band">
<figcaption><code>photometric_chi2.png</code> Pull and chi-squared contribution for the 12 COSMOS2015 bands of galaxy M13_244680. Pull equals observed minus model over sigma. Uncertainty: sigma includes the 5 percent flux floor. Comparison: filled points use the posterior-median model. Open squares use the best sample with the fit's own sigma. Total chi-squared 43.9 over 12 bands gives 3.66 per band. Caveat: the spectrum dominates the joint fit, so the fit does not constrain the bands on their own.</figcaption>
</figure>

<figure>
<img loading="lazy" src="/wiki/f/results/rtx-5060-dr2-quiescent-full-spectrum/244680-M13_244680/diagnostics/spectral_chi2.png" alt="M13_244680: spectral pull, binned mean pull squared, cumulative chi-squared">
<figcaption><code>spectral_chi2.png</code> Pull per fitted pixel of the LEGA-C spectrum of galaxy M13_244680. Below it: mean pull squared in 25 Å bins and the cumulative chi-squared fraction against wavelength. Uncertainty: sigma includes the fitted calibration floor of 9.98 percent of the model flux. Comparison: the stored pull versus the pull at the best sample. Shaded bands mark masked pixels. Red points mark pixels with pull beyond 4 sigma. Total chi-squared 5961.3 over 3849 pixels, 13 outlier pixels. Caveat: the fitted floor absorbs model mismatch, so chi-squared near 1 does not prove a good model.</figcaption>
</figure>

<figure>
<img loading="lazy" src="/wiki/f/results/rtx-5060-dr2-quiescent-full-spectrum/244680-M13_244680/diagnostics/sf_timescales.png" alt="M13_244680: cumulative mass formed against lookback time with t10 to t90">
<figcaption><code>sf_timescales.png</code> Fraction of the final stellar mass of galaxy M13_244680 formed earlier than each lookback time. The line is the posterior median. The band is the 16-84 percent range over 400 draws. Comparison: points mark t10 to t90 with 16-84 percent (thick) and 2.5-97.5 percent (thin) intervals versus the universe age. t50 is 2.99 Gyr with a 16-84 percent range of 2.88 to 3.12 Gyr. Caveat: the 7-bin star-formation history model quantises these times to the bin edges.</figcaption>
</figure>

### 244738-M11_244738

| z | S/N | photometry χ²/N | spectrum χ²/N | f_calib | t50 [Gyr] | model |
| --- | --- | --- | --- | --- | --- | --- |
| 0.6971 | 29.0 | 16.64 | 1.114 | 4.25% | 3.01 | [parameters](/wiki/f/results/rtx-5060-dr2-quiescent-full-spectrum/244738-M11_244738/diagnostics/model_parameters.txt) |

Flags:

- photometry chi2/N 16.6 > 3
- 11 pixels with |pull| > 4

<figure>
<img loading="lazy" src="/wiki/f/results/rtx-5060-dr2-quiescent-full-spectrum/244738-M11_244738/diagnostics/photometric_chi2.png" alt="M11_244738: photometric pull and chi-squared contribution per band">
<figcaption><code>photometric_chi2.png</code> Pull and chi-squared contribution for the 12 COSMOS2015 bands of galaxy M11_244738. Pull equals observed minus model over sigma. Uncertainty: sigma includes the 5 percent flux floor. Comparison: filled points use the posterior-median model. Open squares use the best sample with the fit's own sigma. Total chi-squared 199.7 over 12 bands gives 16.64 per band. Caveat: the spectrum dominates the joint fit, so the fit does not constrain the bands on their own.</figcaption>
</figure>

<figure>
<img loading="lazy" src="/wiki/f/results/rtx-5060-dr2-quiescent-full-spectrum/244738-M11_244738/diagnostics/spectral_chi2.png" alt="M11_244738: spectral pull, binned mean pull squared, cumulative chi-squared">
<figcaption><code>spectral_chi2.png</code> Pull per fitted pixel of the LEGA-C spectrum of galaxy M11_244738. Below it: mean pull squared in 25 Å bins and the cumulative chi-squared fraction against wavelength. Uncertainty: sigma includes the fitted calibration floor of 4.25 percent of the model flux. Comparison: the stored pull versus the pull at the best sample. Shaded bands mark masked pixels. Red points mark pixels with pull beyond 4 sigma. Total chi-squared 3835.1 over 3442 pixels, 11 outlier pixels. Caveat: the fitted floor absorbs model mismatch, so chi-squared near 1 does not prove a good model.</figcaption>
</figure>

<figure>
<img loading="lazy" src="/wiki/f/results/rtx-5060-dr2-quiescent-full-spectrum/244738-M11_244738/diagnostics/sf_timescales.png" alt="M11_244738: cumulative mass formed against lookback time with t10 to t90">
<figcaption><code>sf_timescales.png</code> Fraction of the final stellar mass of galaxy M11_244738 formed earlier than each lookback time. The line is the posterior median. The band is the 16-84 percent range over 400 draws. Comparison: points mark t10 to t90 with 16-84 percent (thick) and 2.5-97.5 percent (thin) intervals versus the universe age. t50 is 3.01 Gyr with a 16-84 percent range of 2.99 to 3.05 Gyr. Caveat: the 7-bin star-formation history model quantises these times to the bin edges.</figcaption>
</figure>

### 245252-M11_245252

| z | S/N | photometry χ²/N | spectrum χ²/N | f_calib | t50 [Gyr] | model |
| --- | --- | --- | --- | --- | --- | --- |
| 0.6944 | 44.2 | 22.75 | 1.102 | 4.23% | 3.02 | [parameters](/wiki/f/results/rtx-5060-dr2-quiescent-full-spectrum/245252-M11_245252/diagnostics/model_parameters.txt) |

Flags:

- photometry chi2/N 22.8 > 3
- 16 pixels with |pull| > 4

<figure>
<img loading="lazy" src="/wiki/f/results/rtx-5060-dr2-quiescent-full-spectrum/245252-M11_245252/diagnostics/photometric_chi2.png" alt="M11_245252: photometric pull and chi-squared contribution per band">
<figcaption><code>photometric_chi2.png</code> Pull and chi-squared contribution for the 12 COSMOS2015 bands of galaxy M11_245252. Pull equals observed minus model over sigma. Uncertainty: sigma includes the 5 percent flux floor. Comparison: filled points use the posterior-median model. Open squares use the best sample with the fit's own sigma. Total chi-squared 273.0 over 12 bands gives 22.75 per band. Caveat: the spectrum dominates the joint fit, so the fit does not constrain the bands on their own.</figcaption>
</figure>

<figure>
<img loading="lazy" src="/wiki/f/results/rtx-5060-dr2-quiescent-full-spectrum/245252-M11_245252/diagnostics/spectral_chi2.png" alt="M11_245252: spectral pull, binned mean pull squared, cumulative chi-squared">
<figcaption><code>spectral_chi2.png</code> Pull per fitted pixel of the LEGA-C spectrum of galaxy M11_245252. Below it: mean pull squared in 25 Å bins and the cumulative chi-squared fraction against wavelength. Uncertainty: sigma includes the fitted calibration floor of 4.23 percent of the model flux. Comparison: the stored pull versus the pull at the best sample. Shaded bands mark masked pixels. Red points mark pixels with pull beyond 4 sigma. Total chi-squared 3875.8 over 3516 pixels, 16 outlier pixels. Caveat: the fitted floor absorbs model mismatch, so chi-squared near 1 does not prove a good model.</figcaption>
</figure>

<figure>
<img loading="lazy" src="/wiki/f/results/rtx-5060-dr2-quiescent-full-spectrum/245252-M11_245252/diagnostics/sf_timescales.png" alt="M11_245252: cumulative mass formed against lookback time with t10 to t90">
<figcaption><code>sf_timescales.png</code> Fraction of the final stellar mass of galaxy M11_245252 formed earlier than each lookback time. The line is the posterior median. The band is the 16-84 percent range over 400 draws. Comparison: points mark t10 to t90 with 16-84 percent (thick) and 2.5-97.5 percent (thin) intervals versus the universe age. t50 is 3.02 Gyr with a 16-84 percent range of 3.00 to 3.07 Gyr. Caveat: the 7-bin star-formation history model quantises these times to the bin edges.</figcaption>
</figure>

### 245621-M11_245621

| z | S/N | photometry χ²/N | spectrum χ²/N | f_calib | t50 [Gyr] | model |
| --- | --- | --- | --- | --- | --- | --- |
| 0.7350 | 17.0 | 3.38 | 1.096 | 5.82% | 3.02 | [parameters](/wiki/f/results/rtx-5060-dr2-quiescent-full-spectrum/245621-M11_245621/diagnostics/model_parameters.txt) |

Flags:

- photometry chi2/N 3.4 > 3
- 10 pixels with |pull| > 4

<figure>
<img loading="lazy" src="/wiki/f/results/rtx-5060-dr2-quiescent-full-spectrum/245621-M11_245621/diagnostics/photometric_chi2.png" alt="M11_245621: photometric pull and chi-squared contribution per band">
<figcaption><code>photometric_chi2.png</code> Pull and chi-squared contribution for the 12 COSMOS2015 bands of galaxy M11_245621. Pull equals observed minus model over sigma. Uncertainty: sigma includes the 5 percent flux floor. Comparison: filled points use the posterior-median model. Open squares use the best sample with the fit's own sigma. Total chi-squared 40.5 over 12 bands gives 3.38 per band. Caveat: the spectrum dominates the joint fit, so the fit does not constrain the bands on their own.</figcaption>
</figure>

<figure>
<img loading="lazy" src="/wiki/f/results/rtx-5060-dr2-quiescent-full-spectrum/245621-M11_245621/diagnostics/spectral_chi2.png" alt="M11_245621: spectral pull, binned mean pull squared, cumulative chi-squared">
<figcaption><code>spectral_chi2.png</code> Pull per fitted pixel of the LEGA-C spectrum of galaxy M11_245621. Below it: mean pull squared in 25 Å bins and the cumulative chi-squared fraction against wavelength. Uncertainty: sigma includes the fitted calibration floor of 5.82 percent of the model flux. Comparison: the stored pull versus the pull at the best sample. Shaded bands mark masked pixels. Red points mark pixels with pull beyond 4 sigma. Total chi-squared 3881.2 over 3542 pixels, 10 outlier pixels. Caveat: the fitted floor absorbs model mismatch, so chi-squared near 1 does not prove a good model.</figcaption>
</figure>

<figure>
<img loading="lazy" src="/wiki/f/results/rtx-5060-dr2-quiescent-full-spectrum/245621-M11_245621/diagnostics/sf_timescales.png" alt="M11_245621: cumulative mass formed against lookback time with t10 to t90">
<figcaption><code>sf_timescales.png</code> Fraction of the final stellar mass of galaxy M11_245621 formed earlier than each lookback time. The line is the posterior median. The band is the 16-84 percent range over 400 draws. Comparison: points mark t10 to t90 with 16-84 percent (thick) and 2.5-97.5 percent (thin) intervals versus the universe age. t50 is 3.02 Gyr with a 16-84 percent range of 3.00 to 3.10 Gyr. Caveat: the 7-bin star-formation history model quantises these times to the bin edges.</figcaption>
</figure>

### 245763-M13_245763

| z | S/N | photometry χ²/N | spectrum χ²/N | f_calib | t50 [Gyr] | model |
| --- | --- | --- | --- | --- | --- | --- |
| 0.7542 | 9.4 | 4.87 | 1.138 | 9.22% | 5.71 | [parameters](/wiki/f/results/rtx-5060-dr2-quiescent-full-spectrum/245763-M13_245763/diagnostics/model_parameters.txt) |

Flags:

- photometry chi2/N 4.9 > 3
- 7 pixels with |pull| > 4

<figure>
<img loading="lazy" src="/wiki/f/results/rtx-5060-dr2-quiescent-full-spectrum/245763-M13_245763/diagnostics/photometric_chi2.png" alt="M13_245763: photometric pull and chi-squared contribution per band">
<figcaption><code>photometric_chi2.png</code> Pull and chi-squared contribution for the 12 COSMOS2015 bands of galaxy M13_245763. Pull equals observed minus model over sigma. Uncertainty: sigma includes the 5 percent flux floor. Comparison: filled points use the posterior-median model. Open squares use the best sample with the fit's own sigma. Total chi-squared 58.4 over 12 bands gives 4.87 per band. Caveat: the spectrum dominates the joint fit, so the fit does not constrain the bands on their own.</figcaption>
</figure>

<figure>
<img loading="lazy" src="/wiki/f/results/rtx-5060-dr2-quiescent-full-spectrum/245763-M13_245763/diagnostics/spectral_chi2.png" alt="M13_245763: spectral pull, binned mean pull squared, cumulative chi-squared">
<figcaption><code>spectral_chi2.png</code> Pull per fitted pixel of the LEGA-C spectrum of galaxy M13_245763. Below it: mean pull squared in 25 Å bins and the cumulative chi-squared fraction against wavelength. Uncertainty: sigma includes the fitted calibration floor of 9.22 percent of the model flux. Comparison: the stored pull versus the pull at the best sample. Shaded bands mark masked pixels. Red points mark pixels with pull beyond 4 sigma. Total chi-squared 4345.9 over 3820 pixels, 7 outlier pixels. Caveat: the fitted floor absorbs model mismatch, so chi-squared near 1 does not prove a good model.</figcaption>
</figure>

<figure>
<img loading="lazy" src="/wiki/f/results/rtx-5060-dr2-quiescent-full-spectrum/245763-M13_245763/diagnostics/sf_timescales.png" alt="M13_245763: cumulative mass formed against lookback time with t10 to t90">
<figcaption><code>sf_timescales.png</code> Fraction of the final stellar mass of galaxy M13_245763 formed earlier than each lookback time. The line is the posterior median. The band is the 16-84 percent range over 400 draws. Comparison: points mark t10 to t90 with 16-84 percent (thick) and 2.5-97.5 percent (thin) intervals versus the universe age. t50 is 5.71 Gyr with a 16-84 percent range of 5.19 to 5.98 Gyr. Caveat: the 7-bin star-formation history model quantises these times to the bin edges.</figcaption>
</figure>

### 245864-M11_245864

| z | S/N | photometry χ²/N | spectrum χ²/N | f_calib | t50 [Gyr] | model |
| --- | --- | --- | --- | --- | --- | --- |
| 0.6981 | 13.3 | 3.39 | 1.115 | 4.80% | 2.90 | [parameters](/wiki/f/results/rtx-5060-dr2-quiescent-full-spectrum/245864-M11_245864/diagnostics/model_parameters.txt) |

Flags:

- photometry chi2/N 3.4 > 3
- 9 pixels with |pull| > 4

<figure>
<img loading="lazy" src="/wiki/f/results/rtx-5060-dr2-quiescent-full-spectrum/245864-M11_245864/diagnostics/photometric_chi2.png" alt="M11_245864: photometric pull and chi-squared contribution per band">
<figcaption><code>photometric_chi2.png</code> Pull and chi-squared contribution for the 12 COSMOS2015 bands of galaxy M11_245864. Pull equals observed minus model over sigma. Uncertainty: sigma includes the 5 percent flux floor. Comparison: filled points use the posterior-median model. Open squares use the best sample with the fit's own sigma. Total chi-squared 40.7 over 12 bands gives 3.39 per band. Caveat: the spectrum dominates the joint fit, so the fit does not constrain the bands on their own.</figcaption>
</figure>

<figure>
<img loading="lazy" src="/wiki/f/results/rtx-5060-dr2-quiescent-full-spectrum/245864-M11_245864/diagnostics/spectral_chi2.png" alt="M11_245864: spectral pull, binned mean pull squared, cumulative chi-squared">
<figcaption><code>spectral_chi2.png</code> Pull per fitted pixel of the LEGA-C spectrum of galaxy M11_245864. Below it: mean pull squared in 25 Å bins and the cumulative chi-squared fraction against wavelength. Uncertainty: sigma includes the fitted calibration floor of 4.80 percent of the model flux. Comparison: the stored pull versus the pull at the best sample. Shaded bands mark masked pixels. Red points mark pixels with pull beyond 4 sigma. Total chi-squared 3928.0 over 3522 pixels, 9 outlier pixels. Caveat: the fitted floor absorbs model mismatch, so chi-squared near 1 does not prove a good model.</figcaption>
</figure>

<figure>
<img loading="lazy" src="/wiki/f/results/rtx-5060-dr2-quiescent-full-spectrum/245864-M11_245864/diagnostics/sf_timescales.png" alt="M11_245864: cumulative mass formed against lookback time with t10 to t90">
<figcaption><code>sf_timescales.png</code> Fraction of the final stellar mass of galaxy M11_245864 formed earlier than each lookback time. The line is the posterior median. The band is the 16-84 percent range over 400 draws. Comparison: points mark t10 to t90 with 16-84 percent (thick) and 2.5-97.5 percent (thin) intervals versus the universe age. t50 is 2.90 Gyr with a 16-84 percent range of 2.82 to 3.04 Gyr. Caveat: the 7-bin star-formation history model quantises these times to the bin edges.</figcaption>
</figure>

### 246149-M13_246149

| z | S/N | photometry χ²/N | spectrum χ²/N | f_calib | t50 [Gyr] | model |
| --- | --- | --- | --- | --- | --- | --- |
| 0.7345 | 26.6 | 7.52 | 1.082 | 6.13% | 3.58 | [parameters](/wiki/f/results/rtx-5060-dr2-quiescent-full-spectrum/246149-M13_246149/diagnostics/model_parameters.txt) |

Flags:

- photometry chi2/N 7.5 > 3
- 1 pixels with |pull| > 4

<figure>
<img loading="lazy" src="/wiki/f/results/rtx-5060-dr2-quiescent-full-spectrum/246149-M13_246149/diagnostics/photometric_chi2.png" alt="M13_246149: photometric pull and chi-squared contribution per band">
<figcaption><code>photometric_chi2.png</code> Pull and chi-squared contribution for the 12 COSMOS2015 bands of galaxy M13_246149. Pull equals observed minus model over sigma. Uncertainty: sigma includes the 5 percent flux floor. Comparison: filled points use the posterior-median model. Open squares use the best sample with the fit's own sigma. Total chi-squared 90.2 over 12 bands gives 7.52 per band. Caveat: the spectrum dominates the joint fit, so the fit does not constrain the bands on their own.</figcaption>
</figure>

<figure>
<img loading="lazy" src="/wiki/f/results/rtx-5060-dr2-quiescent-full-spectrum/246149-M13_246149/diagnostics/spectral_chi2.png" alt="M13_246149: spectral pull, binned mean pull squared, cumulative chi-squared">
<figcaption><code>spectral_chi2.png</code> Pull per fitted pixel of the LEGA-C spectrum of galaxy M13_246149. Below it: mean pull squared in 25 Å bins and the cumulative chi-squared fraction against wavelength. Uncertainty: sigma includes the fitted calibration floor of 6.13 percent of the model flux. Comparison: the stored pull versus the pull at the best sample. Shaded bands mark masked pixels. Red points mark pixels with pull beyond 4 sigma. Total chi-squared 3992.1 over 3689 pixels, 1 outlier pixels. Caveat: the fitted floor absorbs model mismatch, so chi-squared near 1 does not prove a good model.</figcaption>
</figure>

<figure>
<img loading="lazy" src="/wiki/f/results/rtx-5060-dr2-quiescent-full-spectrum/246149-M13_246149/diagnostics/sf_timescales.png" alt="M13_246149: cumulative mass formed against lookback time with t10 to t90">
<figcaption><code>sf_timescales.png</code> Fraction of the final stellar mass of galaxy M13_246149 formed earlier than each lookback time. The line is the posterior median. The band is the 16-84 percent range over 400 draws. Comparison: points mark t10 to t90 with 16-84 percent (thick) and 2.5-97.5 percent (thin) intervals versus the universe age. t50 is 3.58 Gyr with a 16-84 percent range of 3.12 to 3.91 Gyr. Caveat: the 7-bin star-formation history model quantises these times to the bin edges.</figcaption>
</figure>

### 248217-M13_248217

| z | S/N | photometry χ²/N | spectrum χ²/N | f_calib | t50 [Gyr] | model |
| --- | --- | --- | --- | --- | --- | --- |
| 0.6109 | 30.6 | 8.88 | 1.114 | 4.30% | 3.07 | [parameters](/wiki/f/results/rtx-5060-dr2-quiescent-full-spectrum/248217-M13_248217/diagnostics/model_parameters.txt) |

Flags:

- photometry chi2/N 8.9 > 3
- 7 pixels with |pull| > 4

<figure>
<img loading="lazy" src="/wiki/f/results/rtx-5060-dr2-quiescent-full-spectrum/248217-M13_248217/diagnostics/photometric_chi2.png" alt="M13_248217: photometric pull and chi-squared contribution per band">
<figcaption><code>photometric_chi2.png</code> Pull and chi-squared contribution for the 12 COSMOS2015 bands of galaxy M13_248217. Pull equals observed minus model over sigma. Uncertainty: sigma includes the 5 percent flux floor. Comparison: filled points use the posterior-median model. Open squares use the best sample with the fit's own sigma. Total chi-squared 106.6 over 12 bands gives 8.88 per band. Caveat: the spectrum dominates the joint fit, so the fit does not constrain the bands on their own.</figcaption>
</figure>

<figure>
<img loading="lazy" src="/wiki/f/results/rtx-5060-dr2-quiescent-full-spectrum/248217-M13_248217/diagnostics/spectral_chi2.png" alt="M13_248217: spectral pull, binned mean pull squared, cumulative chi-squared">
<figcaption><code>spectral_chi2.png</code> Pull per fitted pixel of the LEGA-C spectrum of galaxy M13_248217. Below it: mean pull squared in 25 Å bins and the cumulative chi-squared fraction against wavelength. Uncertainty: sigma includes the fitted calibration floor of 4.30 percent of the model flux. Comparison: the stored pull versus the pull at the best sample. Shaded bands mark masked pixels. Red points mark pixels with pull beyond 4 sigma. Total chi-squared 3996.9 over 3587 pixels, 7 outlier pixels. Caveat: the fitted floor absorbs model mismatch, so chi-squared near 1 does not prove a good model.</figcaption>
</figure>

<figure>
<img loading="lazy" src="/wiki/f/results/rtx-5060-dr2-quiescent-full-spectrum/248217-M13_248217/diagnostics/sf_timescales.png" alt="M13_248217: cumulative mass formed against lookback time with t10 to t90">
<figcaption><code>sf_timescales.png</code> Fraction of the final stellar mass of galaxy M13_248217 formed earlier than each lookback time. The line is the posterior median. The band is the 16-84 percent range over 400 draws. Comparison: points mark t10 to t90 with 16-84 percent (thick) and 2.5-97.5 percent (thin) intervals versus the universe age. t50 is 3.07 Gyr with a 16-84 percent range of 3.00 to 3.39 Gyr. Caveat: the 7-bin star-formation history model quantises these times to the bin edges.</figcaption>
</figure>

### 248829-M11_248829

| z | S/N | photometry χ²/N | spectrum χ²/N | f_calib | t50 [Gyr] | model |
| --- | --- | --- | --- | --- | --- | --- |
| 0.7635 | 19.7 | 4.75 | 1.184 | 4.90% | 2.86 | [parameters](/wiki/f/results/rtx-5060-dr2-quiescent-full-spectrum/248829-M11_248829/diagnostics/model_parameters.txt) |

Flags:

- photometry chi2/N 4.7 > 3
- 8 pixels with |pull| > 4

<figure>
<img loading="lazy" src="/wiki/f/results/rtx-5060-dr2-quiescent-full-spectrum/248829-M11_248829/diagnostics/photometric_chi2.png" alt="M11_248829: photometric pull and chi-squared contribution per band">
<figcaption><code>photometric_chi2.png</code> Pull and chi-squared contribution for the 12 COSMOS2015 bands of galaxy M11_248829. Pull equals observed minus model over sigma. Uncertainty: sigma includes the 5 percent flux floor. Comparison: filled points use the posterior-median model. Open squares use the best sample with the fit's own sigma. Total chi-squared 56.9 over 12 bands gives 4.75 per band. Caveat: the spectrum dominates the joint fit, so the fit does not constrain the bands on their own.</figcaption>
</figure>

<figure>
<img loading="lazy" src="/wiki/f/results/rtx-5060-dr2-quiescent-full-spectrum/248829-M11_248829/diagnostics/spectral_chi2.png" alt="M11_248829: spectral pull, binned mean pull squared, cumulative chi-squared">
<figcaption><code>spectral_chi2.png</code> Pull per fitted pixel of the LEGA-C spectrum of galaxy M11_248829. Below it: mean pull squared in 25 Å bins and the cumulative chi-squared fraction against wavelength. Uncertainty: sigma includes the fitted calibration floor of 4.90 percent of the model flux. Comparison: the stored pull versus the pull at the best sample. Shaded bands mark masked pixels. Red points mark pixels with pull beyond 4 sigma. Total chi-squared 4077.9 over 3443 pixels, 8 outlier pixels. Caveat: the fitted floor absorbs model mismatch, so chi-squared near 1 does not prove a good model.</figcaption>
</figure>

<figure>
<img loading="lazy" src="/wiki/f/results/rtx-5060-dr2-quiescent-full-spectrum/248829-M11_248829/diagnostics/sf_timescales.png" alt="M11_248829: cumulative mass formed against lookback time with t10 to t90">
<figcaption><code>sf_timescales.png</code> Fraction of the final stellar mass of galaxy M11_248829 formed earlier than each lookback time. The line is the posterior median. The band is the 16-84 percent range over 400 draws. Comparison: points mark t10 to t90 with 16-84 percent (thick) and 2.5-97.5 percent (thin) intervals versus the universe age. t50 is 2.86 Gyr with a 16-84 percent range of 2.81 to 2.93 Gyr. Caveat: the 7-bin star-formation history model quantises these times to the bin edges.</figcaption>
</figure>

### 250391-M11_250391

| z | S/N | photometry χ²/N | spectrum χ²/N | f_calib | t50 [Gyr] | model |
| --- | --- | --- | --- | --- | --- | --- |
| 0.8893 | 35.8 | 18.54 | 1.083 | 4.68% | 0.69 | [parameters](/wiki/f/results/rtx-5060-dr2-quiescent-full-spectrum/250391-M11_250391/diagnostics/model_parameters.txt) |

Flags:

- photometry chi2/N 18.5 > 3
- 17 pixels with |pull| > 4

<figure>
<img loading="lazy" src="/wiki/f/results/rtx-5060-dr2-quiescent-full-spectrum/250391-M11_250391/diagnostics/photometric_chi2.png" alt="M11_250391: photometric pull and chi-squared contribution per band">
<figcaption><code>photometric_chi2.png</code> Pull and chi-squared contribution for the 12 COSMOS2015 bands of galaxy M11_250391. Pull equals observed minus model over sigma. Uncertainty: sigma includes the 5 percent flux floor. Comparison: filled points use the posterior-median model. Open squares use the best sample with the fit's own sigma. Total chi-squared 222.5 over 12 bands gives 18.54 per band. Caveat: the spectrum dominates the joint fit, so the fit does not constrain the bands on their own.</figcaption>
</figure>

<figure>
<img loading="lazy" src="/wiki/f/results/rtx-5060-dr2-quiescent-full-spectrum/250391-M11_250391/diagnostics/spectral_chi2.png" alt="M11_250391: spectral pull, binned mean pull squared, cumulative chi-squared">
<figcaption><code>spectral_chi2.png</code> Pull per fitted pixel of the LEGA-C spectrum of galaxy M11_250391. Below it: mean pull squared in 25 Å bins and the cumulative chi-squared fraction against wavelength. Uncertainty: sigma includes the fitted calibration floor of 4.68 percent of the model flux. Comparison: the stored pull versus the pull at the best sample. Shaded bands mark masked pixels. Red points mark pixels with pull beyond 4 sigma. Total chi-squared 4169.5 over 3849 pixels, 17 outlier pixels. Caveat: the fitted floor absorbs model mismatch, so chi-squared near 1 does not prove a good model.</figcaption>
</figure>

<figure>
<img loading="lazy" src="/wiki/f/results/rtx-5060-dr2-quiescent-full-spectrum/250391-M11_250391/diagnostics/sf_timescales.png" alt="M11_250391: cumulative mass formed against lookback time with t10 to t90">
<figcaption><code>sf_timescales.png</code> Fraction of the final stellar mass of galaxy M11_250391 formed earlier than each lookback time. The line is the posterior median. The band is the 16-84 percent range over 400 draws. Comparison: points mark t10 to t90 with 16-84 percent (thick) and 2.5-97.5 percent (thin) intervals versus the universe age. t50 is 0.69 Gyr with a 16-84 percent range of 0.65 to 0.73 Gyr. Caveat: the 7-bin star-formation history model quantises these times to the bin edges.</figcaption>
</figure>

### 253688-M13_253688

| z | S/N | photometry χ²/N | spectrum χ²/N | f_calib | t50 [Gyr] | model |
| --- | --- | --- | --- | --- | --- | --- |
| 0.8370 | 4.8 | 1.89 | 2.554 | 9.99% | 2.05 | [parameters](/wiki/f/results/rtx-5060-dr2-quiescent-full-spectrum/253688-M13_253688/diagnostics/model_parameters.txt) |

Flags:

- spectrum chi2/N 2.55 > 1.5
- calibration floor at prior bound (10.0% of 10%)
- 65 pixels with |pull| > 4

<figure>
<img loading="lazy" src="/wiki/f/results/rtx-5060-dr2-quiescent-full-spectrum/253688-M13_253688/diagnostics/photometric_chi2.png" alt="M13_253688: photometric pull and chi-squared contribution per band">
<figcaption><code>photometric_chi2.png</code> Pull and chi-squared contribution for the 12 COSMOS2015 bands of galaxy M13_253688. Pull equals observed minus model over sigma. Uncertainty: sigma includes the 5 percent flux floor. Comparison: filled points use the posterior-median model. Open squares use the best sample with the fit's own sigma. Total chi-squared 22.6 over 12 bands gives 1.89 per band. Caveat: the spectrum dominates the joint fit, so the fit does not constrain the bands on their own.</figcaption>
</figure>

<figure>
<img loading="lazy" src="/wiki/f/results/rtx-5060-dr2-quiescent-full-spectrum/253688-M13_253688/diagnostics/spectral_chi2.png" alt="M13_253688: spectral pull, binned mean pull squared, cumulative chi-squared">
<figcaption><code>spectral_chi2.png</code> Pull per fitted pixel of the LEGA-C spectrum of galaxy M13_253688. Below it: mean pull squared in 25 Å bins and the cumulative chi-squared fraction against wavelength. Uncertainty: sigma includes the fitted calibration floor of 9.99 percent of the model flux. Comparison: the stored pull versus the pull at the best sample. Shaded bands mark masked pixels. Red points mark pixels with pull beyond 4 sigma. Total chi-squared 8479.7 over 3320 pixels, 65 outlier pixels. Caveat: the fitted floor absorbs model mismatch, so chi-squared near 1 does not prove a good model.</figcaption>
</figure>

<figure>
<img loading="lazy" src="/wiki/f/results/rtx-5060-dr2-quiescent-full-spectrum/253688-M13_253688/diagnostics/sf_timescales.png" alt="M13_253688: cumulative mass formed against lookback time with t10 to t90">
<figcaption><code>sf_timescales.png</code> Fraction of the final stellar mass of galaxy M13_253688 formed earlier than each lookback time. The line is the posterior median. The band is the 16-84 percent range over 400 draws. Comparison: points mark t10 to t90 with 16-84 percent (thick) and 2.5-97.5 percent (thin) intervals versus the universe age. t50 is 2.05 Gyr with a 16-84 percent range of 1.70 to 2.46 Gyr. Caveat: the 7-bin star-formation history model quantises these times to the bin edges.</figcaption>
</figure>

### 254350-M13_254350

| z | S/N | photometry χ²/N | spectrum χ²/N | f_calib | t50 [Gyr] | model |
| --- | --- | --- | --- | --- | --- | --- |
| 0.6692 | 13.5 | 5.68 | 1.122 | 9.26% | 3.07 | [parameters](/wiki/f/results/rtx-5060-dr2-quiescent-full-spectrum/254350-M13_254350/diagnostics/model_parameters.txt) |

Flags:

- photometry chi2/N 5.7 > 3
- 3 pixels with |pull| > 4

<figure>
<img loading="lazy" src="/wiki/f/results/rtx-5060-dr2-quiescent-full-spectrum/254350-M13_254350/diagnostics/photometric_chi2.png" alt="M13_254350: photometric pull and chi-squared contribution per band">
<figcaption><code>photometric_chi2.png</code> Pull and chi-squared contribution for the 12 COSMOS2015 bands of galaxy M13_254350. Pull equals observed minus model over sigma. Uncertainty: sigma includes the 5 percent flux floor. Comparison: filled points use the posterior-median model. Open squares use the best sample with the fit's own sigma. Total chi-squared 68.2 over 12 bands gives 5.68 per band. Caveat: the spectrum dominates the joint fit, so the fit does not constrain the bands on their own.</figcaption>
</figure>

<figure>
<img loading="lazy" src="/wiki/f/results/rtx-5060-dr2-quiescent-full-spectrum/254350-M13_254350/diagnostics/spectral_chi2.png" alt="M13_254350: spectral pull, binned mean pull squared, cumulative chi-squared">
<figcaption><code>spectral_chi2.png</code> Pull per fitted pixel of the LEGA-C spectrum of galaxy M13_254350. Below it: mean pull squared in 25 Å bins and the cumulative chi-squared fraction against wavelength. Uncertainty: sigma includes the fitted calibration floor of 9.26 percent of the model flux. Comparison: the stored pull versus the pull at the best sample. Shaded bands mark masked pixels. Red points mark pixels with pull beyond 4 sigma. Total chi-squared 4011.5 over 3576 pixels, 3 outlier pixels. Caveat: the fitted floor absorbs model mismatch, so chi-squared near 1 does not prove a good model.</figcaption>
</figure>

<figure>
<img loading="lazy" src="/wiki/f/results/rtx-5060-dr2-quiescent-full-spectrum/254350-M13_254350/diagnostics/sf_timescales.png" alt="M13_254350: cumulative mass formed against lookback time with t10 to t90">
<figcaption><code>sf_timescales.png</code> Fraction of the final stellar mass of galaxy M13_254350 formed earlier than each lookback time. The line is the posterior median. The band is the 16-84 percent range over 400 draws. Comparison: points mark t10 to t90 with 16-84 percent (thick) and 2.5-97.5 percent (thin) intervals versus the universe age. t50 is 3.07 Gyr with a 16-84 percent range of 2.88 to 4.40 Gyr. Caveat: the 7-bin star-formation history model quantises these times to the bin edges.</figcaption>
</figure>

### 255047-M13_255047

| z | S/N | photometry χ²/N | spectrum χ²/N | f_calib | t50 [Gyr] | model |
| --- | --- | --- | --- | --- | --- | --- |
| 0.8643 | 9.4 | 2.97 | 1.294 | 9.97% | 2.73 | [parameters](/wiki/f/results/rtx-5060-dr2-quiescent-full-spectrum/255047-M13_255047/diagnostics/model_parameters.txt) |

Flags:

- calibration floor at prior bound (10.0% of 10%)
- 3 pixels with |pull| > 4

<figure>
<img loading="lazy" src="/wiki/f/results/rtx-5060-dr2-quiescent-full-spectrum/255047-M13_255047/diagnostics/photometric_chi2.png" alt="M13_255047: photometric pull and chi-squared contribution per band">
<figcaption><code>photometric_chi2.png</code> Pull and chi-squared contribution for the 12 COSMOS2015 bands of galaxy M13_255047. Pull equals observed minus model over sigma. Uncertainty: sigma includes the 5 percent flux floor. Comparison: filled points use the posterior-median model. Open squares use the best sample with the fit's own sigma. Total chi-squared 35.6 over 12 bands gives 2.97 per band. Caveat: the spectrum dominates the joint fit, so the fit does not constrain the bands on their own.</figcaption>
</figure>

<figure>
<img loading="lazy" src="/wiki/f/results/rtx-5060-dr2-quiescent-full-spectrum/255047-M13_255047/diagnostics/spectral_chi2.png" alt="M13_255047: spectral pull, binned mean pull squared, cumulative chi-squared">
<figcaption><code>spectral_chi2.png</code> Pull per fitted pixel of the LEGA-C spectrum of galaxy M13_255047. Below it: mean pull squared in 25 Å bins and the cumulative chi-squared fraction against wavelength. Uncertainty: sigma includes the fitted calibration floor of 9.97 percent of the model flux. Comparison: the stored pull versus the pull at the best sample. Shaded bands mark masked pixels. Red points mark pixels with pull beyond 4 sigma. Total chi-squared 4921.6 over 3802 pixels, 3 outlier pixels. Caveat: the fitted floor absorbs model mismatch, so chi-squared near 1 does not prove a good model.</figcaption>
</figure>

<figure>
<img loading="lazy" src="/wiki/f/results/rtx-5060-dr2-quiescent-full-spectrum/255047-M13_255047/diagnostics/sf_timescales.png" alt="M13_255047: cumulative mass formed against lookback time with t10 to t90">
<figcaption><code>sf_timescales.png</code> Fraction of the final stellar mass of galaxy M13_255047 formed earlier than each lookback time. The line is the posterior median. The band is the 16-84 percent range over 400 draws. Comparison: points mark t10 to t90 with 16-84 percent (thick) and 2.5-97.5 percent (thin) intervals versus the universe age. t50 is 2.73 Gyr with a 16-84 percent range of 2.65 to 2.83 Gyr. Caveat: the 7-bin star-formation history model quantises these times to the bin edges.</figcaption>
</figure>

### 257455-M11_257455

| z | S/N | photometry χ²/N | spectrum χ²/N | f_calib | t50 [Gyr] | model |
| --- | --- | --- | --- | --- | --- | --- |
| 0.6657 | 36.0 | 7.60 | 1.127 | 5.41% | 2.84 | [parameters](/wiki/f/results/rtx-5060-dr2-quiescent-full-spectrum/257455-M11_257455/diagnostics/model_parameters.txt) |

Flags:

- photometry chi2/N 7.6 > 3
- 16 pixels with |pull| > 4

<figure>
<img loading="lazy" src="/wiki/f/results/rtx-5060-dr2-quiescent-full-spectrum/257455-M11_257455/diagnostics/photometric_chi2.png" alt="M11_257455: photometric pull and chi-squared contribution per band">
<figcaption><code>photometric_chi2.png</code> Pull and chi-squared contribution for the 12 COSMOS2015 bands of galaxy M11_257455. Pull equals observed minus model over sigma. Uncertainty: sigma includes the 5 percent flux floor. Comparison: filled points use the posterior-median model. Open squares use the best sample with the fit's own sigma. Total chi-squared 91.2 over 12 bands gives 7.60 per band. Caveat: the spectrum dominates the joint fit, so the fit does not constrain the bands on their own.</figcaption>
</figure>

<figure>
<img loading="lazy" src="/wiki/f/results/rtx-5060-dr2-quiescent-full-spectrum/257455-M11_257455/diagnostics/spectral_chi2.png" alt="M11_257455: spectral pull, binned mean pull squared, cumulative chi-squared">
<figcaption><code>spectral_chi2.png</code> Pull per fitted pixel of the LEGA-C spectrum of galaxy M11_257455. Below it: mean pull squared in 25 Å bins and the cumulative chi-squared fraction against wavelength. Uncertainty: sigma includes the fitted calibration floor of 5.41 percent of the model flux. Comparison: the stored pull versus the pull at the best sample. Shaded bands mark masked pixels. Red points mark pixels with pull beyond 4 sigma. Total chi-squared 3985.0 over 3537 pixels, 16 outlier pixels. Caveat: the fitted floor absorbs model mismatch, so chi-squared near 1 does not prove a good model.</figcaption>
</figure>

<figure>
<img loading="lazy" src="/wiki/f/results/rtx-5060-dr2-quiescent-full-spectrum/257455-M11_257455/diagnostics/sf_timescales.png" alt="M11_257455: cumulative mass formed against lookback time with t10 to t90">
<figcaption><code>sf_timescales.png</code> Fraction of the final stellar mass of galaxy M11_257455 formed earlier than each lookback time. The line is the posterior median. The band is the 16-84 percent range over 400 draws. Comparison: points mark t10 to t90 with 16-84 percent (thick) and 2.5-97.5 percent (thin) intervals versus the universe age. t50 is 2.84 Gyr with a 16-84 percent range of 2.81 to 2.88 Gyr. Caveat: the 7-bin star-formation history model quantises these times to the bin edges.</figcaption>
</figure>

### 258753-M13_258753

| z | S/N | photometry χ²/N | spectrum χ²/N | f_calib | t50 [Gyr] | model |
| --- | --- | --- | --- | --- | --- | --- |
| 0.9096 | 8.1 | 2.61 | 1.398 | 9.98% | 5.50 | [parameters](/wiki/f/results/rtx-5060-dr2-quiescent-full-spectrum/258753-M13_258753/diagnostics/model_parameters.txt) |

Flags:

- calibration floor at prior bound (10.0% of 10%)
- 4 pixels with |pull| > 4

<figure>
<img loading="lazy" src="/wiki/f/results/rtx-5060-dr2-quiescent-full-spectrum/258753-M13_258753/diagnostics/photometric_chi2.png" alt="M13_258753: photometric pull and chi-squared contribution per band">
<figcaption><code>photometric_chi2.png</code> Pull and chi-squared contribution for the 12 COSMOS2015 bands of galaxy M13_258753. Pull equals observed minus model over sigma. Uncertainty: sigma includes the 5 percent flux floor. Comparison: filled points use the posterior-median model. Open squares use the best sample with the fit's own sigma. Total chi-squared 31.4 over 12 bands gives 2.61 per band. Caveat: the spectrum dominates the joint fit, so the fit does not constrain the bands on their own.</figcaption>
</figure>

<figure>
<img loading="lazy" src="/wiki/f/results/rtx-5060-dr2-quiescent-full-spectrum/258753-M13_258753/diagnostics/spectral_chi2.png" alt="M13_258753: spectral pull, binned mean pull squared, cumulative chi-squared">
<figcaption><code>spectral_chi2.png</code> Pull per fitted pixel of the LEGA-C spectrum of galaxy M13_258753. Below it: mean pull squared in 25 Å bins and the cumulative chi-squared fraction against wavelength. Uncertainty: sigma includes the fitted calibration floor of 9.98 percent of the model flux. Comparison: the stored pull versus the pull at the best sample. Shaded bands mark masked pixels. Red points mark pixels with pull beyond 4 sigma. Total chi-squared 5339.1 over 3818 pixels, 4 outlier pixels. Caveat: the fitted floor absorbs model mismatch, so chi-squared near 1 does not prove a good model.</figcaption>
</figure>

<figure>
<img loading="lazy" src="/wiki/f/results/rtx-5060-dr2-quiescent-full-spectrum/258753-M13_258753/diagnostics/sf_timescales.png" alt="M13_258753: cumulative mass formed against lookback time with t10 to t90">
<figcaption><code>sf_timescales.png</code> Fraction of the final stellar mass of galaxy M13_258753 formed earlier than each lookback time. The line is the posterior median. The band is the 16-84 percent range over 400 draws. Comparison: points mark t10 to t90 with 16-84 percent (thick) and 2.5-97.5 percent (thin) intervals versus the universe age. t50 is 5.50 Gyr with a 16-84 percent range of 4.58 to 5.58 Gyr. Caveat: the 7-bin star-formation history model quantises these times to the bin edges.</figcaption>
</figure>

### 259737-M13_259737

| z | S/N | photometry χ²/N | spectrum χ²/N | f_calib | t50 [Gyr] | model |
| --- | --- | --- | --- | --- | --- | --- |
| 0.7028 | 14.7 | 8.56 | 1.527 | 9.99% | 3.02 | [parameters](/wiki/f/results/rtx-5060-dr2-quiescent-full-spectrum/259737-M13_259737/diagnostics/model_parameters.txt) |

Flags:

- photometry chi2/N 8.6 > 3
- spectrum chi2/N 1.53 > 1.5
- calibration floor at prior bound (10.0% of 10%)
- 32 pixels with |pull| > 4

<figure>
<img loading="lazy" src="/wiki/f/results/rtx-5060-dr2-quiescent-full-spectrum/259737-M13_259737/diagnostics/photometric_chi2.png" alt="M13_259737: photometric pull and chi-squared contribution per band">
<figcaption><code>photometric_chi2.png</code> Pull and chi-squared contribution for the 12 COSMOS2015 bands of galaxy M13_259737. Pull equals observed minus model over sigma. Uncertainty: sigma includes the 5 percent flux floor. Comparison: filled points use the posterior-median model. Open squares use the best sample with the fit's own sigma. Total chi-squared 102.8 over 12 bands gives 8.56 per band. Caveat: the spectrum dominates the joint fit, so the fit does not constrain the bands on their own.</figcaption>
</figure>

<figure>
<img loading="lazy" src="/wiki/f/results/rtx-5060-dr2-quiescent-full-spectrum/259737-M13_259737/diagnostics/spectral_chi2.png" alt="M13_259737: spectral pull, binned mean pull squared, cumulative chi-squared">
<figcaption><code>spectral_chi2.png</code> Pull per fitted pixel of the LEGA-C spectrum of galaxy M13_259737. Below it: mean pull squared in 25 Å bins and the cumulative chi-squared fraction against wavelength. Uncertainty: sigma includes the fitted calibration floor of 9.99 percent of the model flux. Comparison: the stored pull versus the pull at the best sample. Shaded bands mark masked pixels. Red points mark pixels with pull beyond 4 sigma. Total chi-squared 5484.3 over 3592 pixels, 32 outlier pixels. Caveat: the fitted floor absorbs model mismatch, so chi-squared near 1 does not prove a good model.</figcaption>
</figure>

<figure>
<img loading="lazy" src="/wiki/f/results/rtx-5060-dr2-quiescent-full-spectrum/259737-M13_259737/diagnostics/sf_timescales.png" alt="M13_259737: cumulative mass formed against lookback time with t10 to t90">
<figcaption><code>sf_timescales.png</code> Fraction of the final stellar mass of galaxy M13_259737 formed earlier than each lookback time. The line is the posterior median. The band is the 16-84 percent range over 400 draws. Comparison: points mark t10 to t90 with 16-84 percent (thick) and 2.5-97.5 percent (thin) intervals versus the universe age. t50 is 3.02 Gyr with a 16-84 percent range of 2.96 to 3.67 Gyr. Caveat: the 7-bin star-formation history model quantises these times to the bin edges.</figcaption>
</figure>

### 27068-M14_27068

| z | S/N | photometry χ²/N | spectrum χ²/N | f_calib | t50 [Gyr] | model |
| --- | --- | --- | --- | --- | --- | --- |
| 0.6783 | 21.2 | 14.01 | 1.131 | 4.74% | 2.57 | [parameters](/wiki/f/results/rtx-5060-dr2-quiescent-full-spectrum/27068-M14_27068/diagnostics/model_parameters.txt) |

Flags:

- photometry chi2/N 14.0 > 3
- 5 pixels with |pull| > 4

<figure>
<img loading="lazy" src="/wiki/f/results/rtx-5060-dr2-quiescent-full-spectrum/27068-M14_27068/diagnostics/photometric_chi2.png" alt="M14_27068: photometric pull and chi-squared contribution per band">
<figcaption><code>photometric_chi2.png</code> Pull and chi-squared contribution for the 12 COSMOS2015 bands of galaxy M14_27068. Pull equals observed minus model over sigma. Uncertainty: sigma includes the 5 percent flux floor. Comparison: filled points use the posterior-median model. Open squares use the best sample with the fit's own sigma. Total chi-squared 168.2 over 12 bands gives 14.01 per band. Caveat: the spectrum dominates the joint fit, so the fit does not constrain the bands on their own.</figcaption>
</figure>

<figure>
<img loading="lazy" src="/wiki/f/results/rtx-5060-dr2-quiescent-full-spectrum/27068-M14_27068/diagnostics/spectral_chi2.png" alt="M14_27068: spectral pull, binned mean pull squared, cumulative chi-squared">
<figcaption><code>spectral_chi2.png</code> Pull per fitted pixel of the LEGA-C spectrum of galaxy M14_27068. Below it: mean pull squared in 25 Å bins and the cumulative chi-squared fraction against wavelength. Uncertainty: sigma includes the fitted calibration floor of 4.74 percent of the model flux. Comparison: the stored pull versus the pull at the best sample. Shaded bands mark masked pixels. Red points mark pixels with pull beyond 4 sigma. Total chi-squared 3903.0 over 3452 pixels, 5 outlier pixels. Caveat: the fitted floor absorbs model mismatch, so chi-squared near 1 does not prove a good model.</figcaption>
</figure>

<figure>
<img loading="lazy" src="/wiki/f/results/rtx-5060-dr2-quiescent-full-spectrum/27068-M14_27068/diagnostics/sf_timescales.png" alt="M14_27068: cumulative mass formed against lookback time with t10 to t90">
<figcaption><code>sf_timescales.png</code> Fraction of the final stellar mass of galaxy M14_27068 formed earlier than each lookback time. The line is the posterior median. The band is the 16-84 percent range over 400 draws. Comparison: points mark t10 to t90 with 16-84 percent (thick) and 2.5-97.5 percent (thin) intervals versus the universe age. t50 is 2.57 Gyr with a 16-84 percent range of 2.50 to 2.65 Gyr. Caveat: the 7-bin star-formation history model quantises these times to the bin edges.</figcaption>
</figure>

### 31835-M14_31835

| z | S/N | photometry χ²/N | spectrum χ²/N | f_calib | t50 [Gyr] | model |
| --- | --- | --- | --- | --- | --- | --- |
| 0.6774 | 27.4 | 4.45 | 1.081 | 4.13% | 3.00 | [parameters](/wiki/f/results/rtx-5060-dr2-quiescent-full-spectrum/31835-M14_31835/diagnostics/model_parameters.txt) |

Flags:

- photometry chi2/N 4.5 > 3
- 1 pixels with |pull| > 4

<figure>
<img loading="lazy" src="/wiki/f/results/rtx-5060-dr2-quiescent-full-spectrum/31835-M14_31835/diagnostics/photometric_chi2.png" alt="M14_31835: photometric pull and chi-squared contribution per band">
<figcaption><code>photometric_chi2.png</code> Pull and chi-squared contribution for the 12 COSMOS2015 bands of galaxy M14_31835. Pull equals observed minus model over sigma. Uncertainty: sigma includes the 5 percent flux floor. Comparison: filled points use the posterior-median model. Open squares use the best sample with the fit's own sigma. Total chi-squared 53.4 over 12 bands gives 4.45 per band. Caveat: the spectrum dominates the joint fit, so the fit does not constrain the bands on their own.</figcaption>
</figure>

<figure>
<img loading="lazy" src="/wiki/f/results/rtx-5060-dr2-quiescent-full-spectrum/31835-M14_31835/diagnostics/spectral_chi2.png" alt="M14_31835: spectral pull, binned mean pull squared, cumulative chi-squared">
<figcaption><code>spectral_chi2.png</code> Pull per fitted pixel of the LEGA-C spectrum of galaxy M14_31835. Below it: mean pull squared in 25 Å bins and the cumulative chi-squared fraction against wavelength. Uncertainty: sigma includes the fitted calibration floor of 4.13 percent of the model flux. Comparison: the stored pull versus the pull at the best sample. Shaded bands mark masked pixels. Red points mark pixels with pull beyond 4 sigma. Total chi-squared 3845.3 over 3558 pixels, 1 outlier pixels. Caveat: the fitted floor absorbs model mismatch, so chi-squared near 1 does not prove a good model.</figcaption>
</figure>

<figure>
<img loading="lazy" src="/wiki/f/results/rtx-5060-dr2-quiescent-full-spectrum/31835-M14_31835/diagnostics/sf_timescales.png" alt="M14_31835: cumulative mass formed against lookback time with t10 to t90">
<figcaption><code>sf_timescales.png</code> Fraction of the final stellar mass of galaxy M14_31835 formed earlier than each lookback time. The line is the posterior median. The band is the 16-84 percent range over 400 draws. Comparison: points mark t10 to t90 with 16-84 percent (thick) and 2.5-97.5 percent (thin) intervals versus the universe age. t50 is 3.00 Gyr with a 16-84 percent range of 2.96 to 3.05 Gyr. Caveat: the 7-bin star-formation history model quantises these times to the bin edges.</figcaption>
</figure>

### 36550-M14_36550

| z | S/N | photometry χ²/N | spectrum χ²/N | f_calib | t50 [Gyr] | model |
| --- | --- | --- | --- | --- | --- | --- |
| 0.7386 | 8.0 | 2.13 | 1.228 | 9.92% | 2.92 | [parameters](/wiki/f/results/rtx-5060-dr2-quiescent-full-spectrum/36550-M14_36550/diagnostics/model_parameters.txt) |

Flags:

- calibration floor at prior bound (9.9% of 10%)
- 4 pixels with |pull| > 4

<figure>
<img loading="lazy" src="/wiki/f/results/rtx-5060-dr2-quiescent-full-spectrum/36550-M14_36550/diagnostics/photometric_chi2.png" alt="M14_36550: photometric pull and chi-squared contribution per band">
<figcaption><code>photometric_chi2.png</code> Pull and chi-squared contribution for the 12 COSMOS2015 bands of galaxy M14_36550. Pull equals observed minus model over sigma. Uncertainty: sigma includes the 5 percent flux floor. Comparison: filled points use the posterior-median model. Open squares use the best sample with the fit's own sigma. Total chi-squared 25.5 over 12 bands gives 2.13 per band. Caveat: the spectrum dominates the joint fit, so the fit does not constrain the bands on their own.</figcaption>
</figure>

<figure>
<img loading="lazy" src="/wiki/f/results/rtx-5060-dr2-quiescent-full-spectrum/36550-M14_36550/diagnostics/spectral_chi2.png" alt="M14_36550: spectral pull, binned mean pull squared, cumulative chi-squared">
<figcaption><code>spectral_chi2.png</code> Pull per fitted pixel of the LEGA-C spectrum of galaxy M14_36550. Below it: mean pull squared in 25 Å bins and the cumulative chi-squared fraction against wavelength. Uncertainty: sigma includes the fitted calibration floor of 9.92 percent of the model flux. Comparison: the stored pull versus the pull at the best sample. Shaded bands mark masked pixels. Red points mark pixels with pull beyond 4 sigma. Total chi-squared 4126.4 over 3361 pixels, 4 outlier pixels. Caveat: the fitted floor absorbs model mismatch, so chi-squared near 1 does not prove a good model.</figcaption>
</figure>

<figure>
<img loading="lazy" src="/wiki/f/results/rtx-5060-dr2-quiescent-full-spectrum/36550-M14_36550/diagnostics/sf_timescales.png" alt="M14_36550: cumulative mass formed against lookback time with t10 to t90">
<figcaption><code>sf_timescales.png</code> Fraction of the final stellar mass of galaxy M14_36550 formed earlier than each lookback time. The line is the posterior median. The band is the 16-84 percent range over 400 draws. Comparison: points mark t10 to t90 with 16-84 percent (thick) and 2.5-97.5 percent (thin) intervals versus the universe age. t50 is 2.92 Gyr with a 16-84 percent range of 2.79 to 3.04 Gyr. Caveat: the 7-bin star-formation history model quantises these times to the bin edges.</figcaption>
</figure>

### 37023-M14_37023

| z | S/N | photometry χ²/N | spectrum χ²/N | f_calib | t50 [Gyr] | model |
| --- | --- | --- | --- | --- | --- | --- |
| 0.7355 | 21.0 | 5.04 | 1.139 | 3.75% | 2.79 | [parameters](/wiki/f/results/rtx-5060-dr2-quiescent-full-spectrum/37023-M14_37023/diagnostics/model_parameters.txt) |

Flags:

- photometry chi2/N 5.0 > 3
- 3 pixels with |pull| > 4

<figure>
<img loading="lazy" src="/wiki/f/results/rtx-5060-dr2-quiescent-full-spectrum/37023-M14_37023/diagnostics/photometric_chi2.png" alt="M14_37023: photometric pull and chi-squared contribution per band">
<figcaption><code>photometric_chi2.png</code> Pull and chi-squared contribution for the 12 COSMOS2015 bands of galaxy M14_37023. Pull equals observed minus model over sigma. Uncertainty: sigma includes the 5 percent flux floor. Comparison: filled points use the posterior-median model. Open squares use the best sample with the fit's own sigma. Total chi-squared 60.5 over 12 bands gives 5.04 per band. Caveat: the spectrum dominates the joint fit, so the fit does not constrain the bands on their own.</figcaption>
</figure>

<figure>
<img loading="lazy" src="/wiki/f/results/rtx-5060-dr2-quiescent-full-spectrum/37023-M14_37023/diagnostics/spectral_chi2.png" alt="M14_37023: spectral pull, binned mean pull squared, cumulative chi-squared">
<figcaption><code>spectral_chi2.png</code> Pull per fitted pixel of the LEGA-C spectrum of galaxy M14_37023. Below it: mean pull squared in 25 Å bins and the cumulative chi-squared fraction against wavelength. Uncertainty: sigma includes the fitted calibration floor of 3.75 percent of the model flux. Comparison: the stored pull versus the pull at the best sample. Shaded bands mark masked pixels. Red points mark pixels with pull beyond 4 sigma. Total chi-squared 3863.2 over 3393 pixels, 3 outlier pixels. Caveat: the fitted floor absorbs model mismatch, so chi-squared near 1 does not prove a good model.</figcaption>
</figure>

<figure>
<img loading="lazy" src="/wiki/f/results/rtx-5060-dr2-quiescent-full-spectrum/37023-M14_37023/diagnostics/sf_timescales.png" alt="M14_37023: cumulative mass formed against lookback time with t10 to t90">
<figcaption><code>sf_timescales.png</code> Fraction of the final stellar mass of galaxy M14_37023 formed earlier than each lookback time. The line is the posterior median. The band is the 16-84 percent range over 400 draws. Comparison: points mark t10 to t90 with 16-84 percent (thick) and 2.5-97.5 percent (thin) intervals versus the universe age. t50 is 2.79 Gyr with a 16-84 percent range of 2.74 to 2.83 Gyr. Caveat: the 7-bin star-formation history model quantises these times to the bin edges.</figcaption>
</figure>

### 37219-M14_37219

| z | S/N | photometry χ²/N | spectrum χ²/N | f_calib | t50 [Gyr] | model |
| --- | --- | --- | --- | --- | --- | --- |
| 0.7347 | 15.0 | 2.82 | 1.096 | 4.17% | 2.92 | [parameters](/wiki/f/results/rtx-5060-dr2-quiescent-full-spectrum/37219-M14_37219/diagnostics/model_parameters.txt) |

Flags:

- 1 pixels with |pull| > 4

<figure>
<img loading="lazy" src="/wiki/f/results/rtx-5060-dr2-quiescent-full-spectrum/37219-M14_37219/diagnostics/photometric_chi2.png" alt="M14_37219: photometric pull and chi-squared contribution per band">
<figcaption><code>photometric_chi2.png</code> Pull and chi-squared contribution for the 12 COSMOS2015 bands of galaxy M14_37219. Pull equals observed minus model over sigma. Uncertainty: sigma includes the 5 percent flux floor. Comparison: filled points use the posterior-median model. Open squares use the best sample with the fit's own sigma. Total chi-squared 33.8 over 12 bands gives 2.82 per band. Caveat: the spectrum dominates the joint fit, so the fit does not constrain the bands on their own.</figcaption>
</figure>

<figure>
<img loading="lazy" src="/wiki/f/results/rtx-5060-dr2-quiescent-full-spectrum/37219-M14_37219/diagnostics/spectral_chi2.png" alt="M14_37219: spectral pull, binned mean pull squared, cumulative chi-squared">
<figcaption><code>spectral_chi2.png</code> Pull per fitted pixel of the LEGA-C spectrum of galaxy M14_37219. Below it: mean pull squared in 25 Å bins and the cumulative chi-squared fraction against wavelength. Uncertainty: sigma includes the fitted calibration floor of 4.17 percent of the model flux. Comparison: the stored pull versus the pull at the best sample. Shaded bands mark masked pixels. Red points mark pixels with pull beyond 4 sigma. Total chi-squared 3879.3 over 3540 pixels, 1 outlier pixels. Caveat: the fitted floor absorbs model mismatch, so chi-squared near 1 does not prove a good model.</figcaption>
</figure>

<figure>
<img loading="lazy" src="/wiki/f/results/rtx-5060-dr2-quiescent-full-spectrum/37219-M14_37219/diagnostics/sf_timescales.png" alt="M14_37219: cumulative mass formed against lookback time with t10 to t90">
<figcaption><code>sf_timescales.png</code> Fraction of the final stellar mass of galaxy M14_37219 formed earlier than each lookback time. The line is the posterior median. The band is the 16-84 percent range over 400 draws. Comparison: points mark t10 to t90 with 16-84 percent (thick) and 2.5-97.5 percent (thin) intervals versus the universe age. t50 is 2.92 Gyr with a 16-84 percent range of 2.86 to 3.00 Gyr. Caveat: the 7-bin star-formation history model quantises these times to the bin edges.</figcaption>
</figure>

### 37723-M14_37723

| z | S/N | photometry χ²/N | spectrum χ²/N | f_calib | t50 [Gyr] | model |
| --- | --- | --- | --- | --- | --- | --- |
| 0.7360 | 22.9 | 2.84 | 1.098 | 4.08% | 2.92 | [parameters](/wiki/f/results/rtx-5060-dr2-quiescent-full-spectrum/37723-M14_37723/diagnostics/model_parameters.txt) |

Flags:

- 3 pixels with |pull| > 4

<figure>
<img loading="lazy" src="/wiki/f/results/rtx-5060-dr2-quiescent-full-spectrum/37723-M14_37723/diagnostics/photometric_chi2.png" alt="M14_37723: photometric pull and chi-squared contribution per band">
<figcaption><code>photometric_chi2.png</code> Pull and chi-squared contribution for the 12 COSMOS2015 bands of galaxy M14_37723. Pull equals observed minus model over sigma. Uncertainty: sigma includes the 5 percent flux floor. Comparison: filled points use the posterior-median model. Open squares use the best sample with the fit's own sigma. Total chi-squared 34.1 over 12 bands gives 2.84 per band. Caveat: the spectrum dominates the joint fit, so the fit does not constrain the bands on their own.</figcaption>
</figure>

<figure>
<img loading="lazy" src="/wiki/f/results/rtx-5060-dr2-quiescent-full-spectrum/37723-M14_37723/diagnostics/spectral_chi2.png" alt="M14_37723: spectral pull, binned mean pull squared, cumulative chi-squared">
<figcaption><code>spectral_chi2.png</code> Pull per fitted pixel of the LEGA-C spectrum of galaxy M14_37723. Below it: mean pull squared in 25 Å bins and the cumulative chi-squared fraction against wavelength. Uncertainty: sigma includes the fitted calibration floor of 4.08 percent of the model flux. Comparison: the stored pull versus the pull at the best sample. Shaded bands mark masked pixels. Red points mark pixels with pull beyond 4 sigma. Total chi-squared 3743.3 over 3408 pixels, 3 outlier pixels. Caveat: the fitted floor absorbs model mismatch, so chi-squared near 1 does not prove a good model.</figcaption>
</figure>

<figure>
<img loading="lazy" src="/wiki/f/results/rtx-5060-dr2-quiescent-full-spectrum/37723-M14_37723/diagnostics/sf_timescales.png" alt="M14_37723: cumulative mass formed against lookback time with t10 to t90">
<figcaption><code>sf_timescales.png</code> Fraction of the final stellar mass of galaxy M14_37723 formed earlier than each lookback time. The line is the posterior median. The band is the 16-84 percent range over 400 draws. Comparison: points mark t10 to t90 with 16-84 percent (thick) and 2.5-97.5 percent (thin) intervals versus the universe age. t50 is 2.92 Gyr with a 16-84 percent range of 2.90 to 2.97 Gyr. Caveat: the 7-bin star-formation history model quantises these times to the bin edges.</figcaption>
</figure>

### 37843-M14_37843

| z | S/N | photometry χ²/N | spectrum χ²/N | f_calib | t50 [Gyr] | model |
| --- | --- | --- | --- | --- | --- | --- |
| 0.9694 | 6.5 | 8.70 | 1.064 | 6.57% | 3.02 | [parameters](/wiki/f/results/rtx-5060-dr2-quiescent-full-spectrum/37843-M14_37843/diagnostics/model_parameters.txt) |

Flags:

- photometry chi2/N 8.7 > 3
- 1 pixels with |pull| > 4

<figure>
<img loading="lazy" src="/wiki/f/results/rtx-5060-dr2-quiescent-full-spectrum/37843-M14_37843/diagnostics/photometric_chi2.png" alt="M14_37843: photometric pull and chi-squared contribution per band">
<figcaption><code>photometric_chi2.png</code> Pull and chi-squared contribution for the 12 COSMOS2015 bands of galaxy M14_37843. Pull equals observed minus model over sigma. Uncertainty: sigma includes the 5 percent flux floor. Comparison: filled points use the posterior-median model. Open squares use the best sample with the fit's own sigma. Total chi-squared 104.4 over 12 bands gives 8.70 per band. Caveat: the spectrum dominates the joint fit, so the fit does not constrain the bands on their own.</figcaption>
</figure>

<figure>
<img loading="lazy" src="/wiki/f/results/rtx-5060-dr2-quiescent-full-spectrum/37843-M14_37843/diagnostics/spectral_chi2.png" alt="M14_37843: spectral pull, binned mean pull squared, cumulative chi-squared">
<figcaption><code>spectral_chi2.png</code> Pull per fitted pixel of the LEGA-C spectrum of galaxy M14_37843. Below it: mean pull squared in 25 Å bins and the cumulative chi-squared fraction against wavelength. Uncertainty: sigma includes the fitted calibration floor of 6.57 percent of the model flux. Comparison: the stored pull versus the pull at the best sample. Shaded bands mark masked pixels. Red points mark pixels with pull beyond 4 sigma. Total chi-squared 4062.1 over 3817 pixels, 1 outlier pixels. Caveat: the fitted floor absorbs model mismatch, so chi-squared near 1 does not prove a good model.</figcaption>
</figure>

<figure>
<img loading="lazy" src="/wiki/f/results/rtx-5060-dr2-quiescent-full-spectrum/37843-M14_37843/diagnostics/sf_timescales.png" alt="M14_37843: cumulative mass formed against lookback time with t10 to t90">
<figcaption><code>sf_timescales.png</code> Fraction of the final stellar mass of galaxy M14_37843 formed earlier than each lookback time. The line is the posterior median. The band is the 16-84 percent range over 400 draws. Comparison: points mark t10 to t90 with 16-84 percent (thick) and 2.5-97.5 percent (thin) intervals versus the universe age. t50 is 3.02 Gyr with a 16-84 percent range of 2.99 to 3.10 Gyr. Caveat: the 7-bin star-formation history model quantises these times to the bin edges.</figcaption>
</figure>

### 38646-M14_38646

| z | S/N | photometry χ²/N | spectrum χ²/N | f_calib | t50 [Gyr] | model |
| --- | --- | --- | --- | --- | --- | --- |
| 0.9689 | 9.7 | 15.44 | 1.132 | 5.72% | 3.24 | [parameters](/wiki/f/results/rtx-5060-dr2-quiescent-full-spectrum/38646-M14_38646/diagnostics/model_parameters.txt) |

Flags:

- photometry chi2/N 15.4 > 3
- 1 pixels with |pull| > 4

<figure>
<img loading="lazy" src="/wiki/f/results/rtx-5060-dr2-quiescent-full-spectrum/38646-M14_38646/diagnostics/photometric_chi2.png" alt="M14_38646: photometric pull and chi-squared contribution per band">
<figcaption><code>photometric_chi2.png</code> Pull and chi-squared contribution for the 12 COSMOS2015 bands of galaxy M14_38646. Pull equals observed minus model over sigma. Uncertainty: sigma includes the 5 percent flux floor. Comparison: filled points use the posterior-median model. Open squares use the best sample with the fit's own sigma. Total chi-squared 185.3 over 12 bands gives 15.44 per band. Caveat: the spectrum dominates the joint fit, so the fit does not constrain the bands on their own.</figcaption>
</figure>

<figure>
<img loading="lazy" src="/wiki/f/results/rtx-5060-dr2-quiescent-full-spectrum/38646-M14_38646/diagnostics/spectral_chi2.png" alt="M14_38646: spectral pull, binned mean pull squared, cumulative chi-squared">
<figcaption><code>spectral_chi2.png</code> Pull per fitted pixel of the LEGA-C spectrum of galaxy M14_38646. Below it: mean pull squared in 25 Å bins and the cumulative chi-squared fraction against wavelength. Uncertainty: sigma includes the fitted calibration floor of 5.72 percent of the model flux. Comparison: the stored pull versus the pull at the best sample. Shaded bands mark masked pixels. Red points mark pixels with pull beyond 4 sigma. Total chi-squared 4322.2 over 3817 pixels, 1 outlier pixels. Caveat: the fitted floor absorbs model mismatch, so chi-squared near 1 does not prove a good model.</figcaption>
</figure>

<figure>
<img loading="lazy" src="/wiki/f/results/rtx-5060-dr2-quiescent-full-spectrum/38646-M14_38646/diagnostics/sf_timescales.png" alt="M14_38646: cumulative mass formed against lookback time with t10 to t90">
<figcaption><code>sf_timescales.png</code> Fraction of the final stellar mass of galaxy M14_38646 formed earlier than each lookback time. The line is the posterior median. The band is the 16-84 percent range over 400 draws. Comparison: points mark t10 to t90 with 16-84 percent (thick) and 2.5-97.5 percent (thin) intervals versus the universe age. t50 is 3.24 Gyr with a 16-84 percent range of 3.04 to 3.59 Gyr. Caveat: the 7-bin star-formation history model quantises these times to the bin edges.</figcaption>
</figure>

### 38648-M14_38648

| z | S/N | photometry χ²/N | spectrum χ²/N | f_calib | t50 [Gyr] | model |
| --- | --- | --- | --- | --- | --- | --- |
| 0.6743 | 52.7 | 16.59 | 1.081 | 5.01% | 1.65 | [parameters](/wiki/f/results/rtx-5060-dr2-quiescent-full-spectrum/38648-M14_38648/diagnostics/model_parameters.txt) |

Flags:

- photometry chi2/N 16.6 > 3
- 4 pixels with |pull| > 4

<figure>
<img loading="lazy" src="/wiki/f/results/rtx-5060-dr2-quiescent-full-spectrum/38648-M14_38648/diagnostics/photometric_chi2.png" alt="M14_38648: photometric pull and chi-squared contribution per band">
<figcaption><code>photometric_chi2.png</code> Pull and chi-squared contribution for the 12 COSMOS2015 bands of galaxy M14_38648. Pull equals observed minus model over sigma. Uncertainty: sigma includes the 5 percent flux floor. Comparison: filled points use the posterior-median model. Open squares use the best sample with the fit's own sigma. Total chi-squared 199.0 over 12 bands gives 16.59 per band. Caveat: the spectrum dominates the joint fit, so the fit does not constrain the bands on their own.</figcaption>
</figure>

<figure>
<img loading="lazy" src="/wiki/f/results/rtx-5060-dr2-quiescent-full-spectrum/38648-M14_38648/diagnostics/spectral_chi2.png" alt="M14_38648: spectral pull, binned mean pull squared, cumulative chi-squared">
<figcaption><code>spectral_chi2.png</code> Pull per fitted pixel of the LEGA-C spectrum of galaxy M14_38648. Below it: mean pull squared in 25 Å bins and the cumulative chi-squared fraction against wavelength. Uncertainty: sigma includes the fitted calibration floor of 5.01 percent of the model flux. Comparison: the stored pull versus the pull at the best sample. Shaded bands mark masked pixels. Red points mark pixels with pull beyond 4 sigma. Total chi-squared 3856.6 over 3566 pixels, 4 outlier pixels. Caveat: the fitted floor absorbs model mismatch, so chi-squared near 1 does not prove a good model.</figcaption>
</figure>

<figure>
<img loading="lazy" src="/wiki/f/results/rtx-5060-dr2-quiescent-full-spectrum/38648-M14_38648/diagnostics/sf_timescales.png" alt="M14_38648: cumulative mass formed against lookback time with t10 to t90">
<figcaption><code>sf_timescales.png</code> Fraction of the final stellar mass of galaxy M14_38648 formed earlier than each lookback time. The line is the posterior median. The band is the 16-84 percent range over 400 draws. Comparison: points mark t10 to t90 with 16-84 percent (thick) and 2.5-97.5 percent (thin) intervals versus the universe age. t50 is 1.65 Gyr with a 16-84 percent range of 1.65 to 1.68 Gyr. Caveat: the 7-bin star-formation history model quantises these times to the bin edges.</figcaption>
</figure>

### 38771-M14_38771

| z | S/N | photometry χ²/N | spectrum χ²/N | f_calib | t50 [Gyr] | model |
| --- | --- | --- | --- | --- | --- | --- |
| 0.6758 | 12.3 | 3.92 | 1.108 | 7.60% | 5.29 | [parameters](/wiki/f/results/rtx-5060-dr2-quiescent-full-spectrum/38771-M14_38771/diagnostics/model_parameters.txt) |

Flags:

- photometry chi2/N 3.9 > 3
- 16 pixels with |pull| > 4

<figure>
<img loading="lazy" src="/wiki/f/results/rtx-5060-dr2-quiescent-full-spectrum/38771-M14_38771/diagnostics/photometric_chi2.png" alt="M14_38771: photometric pull and chi-squared contribution per band">
<figcaption><code>photometric_chi2.png</code> Pull and chi-squared contribution for the 12 COSMOS2015 bands of galaxy M14_38771. Pull equals observed minus model over sigma. Uncertainty: sigma includes the 5 percent flux floor. Comparison: filled points use the posterior-median model. Open squares use the best sample with the fit's own sigma. Total chi-squared 47.0 over 12 bands gives 3.92 per band. Caveat: the spectrum dominates the joint fit, so the fit does not constrain the bands on their own.</figcaption>
</figure>

<figure>
<img loading="lazy" src="/wiki/f/results/rtx-5060-dr2-quiescent-full-spectrum/38771-M14_38771/diagnostics/spectral_chi2.png" alt="M14_38771: spectral pull, binned mean pull squared, cumulative chi-squared">
<figcaption><code>spectral_chi2.png</code> Pull per fitted pixel of the LEGA-C spectrum of galaxy M14_38771. Below it: mean pull squared in 25 Å bins and the cumulative chi-squared fraction against wavelength. Uncertainty: sigma includes the fitted calibration floor of 7.60 percent of the model flux. Comparison: the stored pull versus the pull at the best sample. Shaded bands mark masked pixels. Red points mark pixels with pull beyond 4 sigma. Total chi-squared 3932.8 over 3550 pixels, 16 outlier pixels. Caveat: the fitted floor absorbs model mismatch, so chi-squared near 1 does not prove a good model.</figcaption>
</figure>

<figure>
<img loading="lazy" src="/wiki/f/results/rtx-5060-dr2-quiescent-full-spectrum/38771-M14_38771/diagnostics/sf_timescales.png" alt="M14_38771: cumulative mass formed against lookback time with t10 to t90">
<figcaption><code>sf_timescales.png</code> Fraction of the final stellar mass of galaxy M14_38771 formed earlier than each lookback time. The line is the posterior median. The band is the 16-84 percent range over 400 draws. Comparison: points mark t10 to t90 with 16-84 percent (thick) and 2.5-97.5 percent (thin) intervals versus the universe age. t50 is 5.29 Gyr with a 16-84 percent range of 3.60 to 5.65 Gyr. Caveat: the 7-bin star-formation history model quantises these times to the bin edges.</figcaption>
</figure>

### 39865-M14_39865

| z | S/N | photometry χ²/N | spectrum χ²/N | f_calib | t50 [Gyr] | model |
| --- | --- | --- | --- | --- | --- | --- |
| 0.8291 | 6.8 | 2.66 | 1.106 | 7.63% | 3.72 | [parameters](/wiki/f/results/rtx-5060-dr2-quiescent-full-spectrum/39865-M14_39865/diagnostics/model_parameters.txt) |

Flags:

- 5 pixels with |pull| > 4

<figure>
<img loading="lazy" src="/wiki/f/results/rtx-5060-dr2-quiescent-full-spectrum/39865-M14_39865/diagnostics/photometric_chi2.png" alt="M14_39865: photometric pull and chi-squared contribution per band">
<figcaption><code>photometric_chi2.png</code> Pull and chi-squared contribution for the 12 COSMOS2015 bands of galaxy M14_39865. Pull equals observed minus model over sigma. Uncertainty: sigma includes the 5 percent flux floor. Comparison: filled points use the posterior-median model. Open squares use the best sample with the fit's own sigma. Total chi-squared 31.9 over 12 bands gives 2.66 per band. Caveat: the spectrum dominates the joint fit, so the fit does not constrain the bands on their own.</figcaption>
</figure>

<figure>
<img loading="lazy" src="/wiki/f/results/rtx-5060-dr2-quiescent-full-spectrum/39865-M14_39865/diagnostics/spectral_chi2.png" alt="M14_39865: spectral pull, binned mean pull squared, cumulative chi-squared">
<figcaption><code>spectral_chi2.png</code> Pull per fitted pixel of the LEGA-C spectrum of galaxy M14_39865. Below it: mean pull squared in 25 Å bins and the cumulative chi-squared fraction against wavelength. Uncertainty: sigma includes the fitted calibration floor of 7.63 percent of the model flux. Comparison: the stored pull versus the pull at the best sample. Shaded bands mark masked pixels. Red points mark pixels with pull beyond 4 sigma. Total chi-squared 3802.9 over 3438 pixels, 5 outlier pixels. Caveat: the fitted floor absorbs model mismatch, so chi-squared near 1 does not prove a good model.</figcaption>
</figure>

<figure>
<img loading="lazy" src="/wiki/f/results/rtx-5060-dr2-quiescent-full-spectrum/39865-M14_39865/diagnostics/sf_timescales.png" alt="M14_39865: cumulative mass formed against lookback time with t10 to t90">
<figcaption><code>sf_timescales.png</code> Fraction of the final stellar mass of galaxy M14_39865 formed earlier than each lookback time. The line is the posterior median. The band is the 16-84 percent range over 400 draws. Comparison: points mark t10 to t90 with 16-84 percent (thick) and 2.5-97.5 percent (thin) intervals versus the universe age. t50 is 3.72 Gyr with a 16-84 percent range of 2.70 to 4.65 Gyr. Caveat: the 7-bin star-formation history model quantises these times to the bin edges.</figcaption>
</figure>

### 77632-M15_77632

| z | S/N | photometry χ²/N | spectrum χ²/N | f_calib | t50 [Gyr] | model |
| --- | --- | --- | --- | --- | --- | --- |
| 0.8253 | 34.5 | 11.32 | 1.173 | 4.18% | 3.03 | [parameters](/wiki/f/results/rtx-5060-dr2-quiescent-full-spectrum/77632-M15_77632/diagnostics/model_parameters.txt) |

Flags:

- photometry chi2/N 11.3 > 3
- 10 pixels with |pull| > 4

<figure>
<img loading="lazy" src="/wiki/f/results/rtx-5060-dr2-quiescent-full-spectrum/77632-M15_77632/diagnostics/photometric_chi2.png" alt="M15_77632: photometric pull and chi-squared contribution per band">
<figcaption><code>photometric_chi2.png</code> Pull and chi-squared contribution for the 12 COSMOS2015 bands of galaxy M15_77632. Pull equals observed minus model over sigma. Uncertainty: sigma includes the 5 percent flux floor. Comparison: filled points use the posterior-median model. Open squares use the best sample with the fit's own sigma. Total chi-squared 135.8 over 12 bands gives 11.32 per band. Caveat: the spectrum dominates the joint fit, so the fit does not constrain the bands on their own.</figcaption>
</figure>

<figure>
<img loading="lazy" src="/wiki/f/results/rtx-5060-dr2-quiescent-full-spectrum/77632-M15_77632/diagnostics/spectral_chi2.png" alt="M15_77632: spectral pull, binned mean pull squared, cumulative chi-squared">
<figcaption><code>spectral_chi2.png</code> Pull per fitted pixel of the LEGA-C spectrum of galaxy M15_77632. Below it: mean pull squared in 25 Å bins and the cumulative chi-squared fraction against wavelength. Uncertainty: sigma includes the fitted calibration floor of 4.18 percent of the model flux. Comparison: the stored pull versus the pull at the best sample. Shaded bands mark masked pixels. Red points mark pixels with pull beyond 4 sigma. Total chi-squared 4025.6 over 3431 pixels, 10 outlier pixels. Caveat: the fitted floor absorbs model mismatch, so chi-squared near 1 does not prove a good model.</figcaption>
</figure>

<figure>
<img loading="lazy" src="/wiki/f/results/rtx-5060-dr2-quiescent-full-spectrum/77632-M15_77632/diagnostics/sf_timescales.png" alt="M15_77632: cumulative mass formed against lookback time with t10 to t90">
<figcaption><code>sf_timescales.png</code> Fraction of the final stellar mass of galaxy M15_77632 formed earlier than each lookback time. The line is the posterior median. The band is the 16-84 percent range over 400 draws. Comparison: points mark t10 to t90 with 16-84 percent (thick) and 2.5-97.5 percent (thin) intervals versus the universe age. t50 is 3.03 Gyr with a 16-84 percent range of 3.00 to 3.13 Gyr. Caveat: the 7-bin star-formation history model quantises these times to the bin edges.</figcaption>
</figure>

### 77745-M15_77745

| z | S/N | photometry χ²/N | spectrum χ²/N | f_calib | t50 [Gyr] | model |
| --- | --- | --- | --- | --- | --- | --- |
| 0.8256 | 30.7 | 5.56 | 1.146 | 4.68% | 4.58 | [parameters](/wiki/f/results/rtx-5060-dr2-quiescent-full-spectrum/77745-M15_77745/diagnostics/model_parameters.txt) |

Flags:

- photometry chi2/N 5.6 > 3
- 8 pixels with |pull| > 4

<figure>
<img loading="lazy" src="/wiki/f/results/rtx-5060-dr2-quiescent-full-spectrum/77745-M15_77745/diagnostics/photometric_chi2.png" alt="M15_77745: photometric pull and chi-squared contribution per band">
<figcaption><code>photometric_chi2.png</code> Pull and chi-squared contribution for the 12 COSMOS2015 bands of galaxy M15_77745. Pull equals observed minus model over sigma. Uncertainty: sigma includes the 5 percent flux floor. Comparison: filled points use the posterior-median model. Open squares use the best sample with the fit's own sigma. Total chi-squared 66.7 over 12 bands gives 5.56 per band. Caveat: the spectrum dominates the joint fit, so the fit does not constrain the bands on their own.</figcaption>
</figure>

<figure>
<img loading="lazy" src="/wiki/f/results/rtx-5060-dr2-quiescent-full-spectrum/77745-M15_77745/diagnostics/spectral_chi2.png" alt="M15_77745: spectral pull, binned mean pull squared, cumulative chi-squared">
<figcaption><code>spectral_chi2.png</code> Pull per fitted pixel of the LEGA-C spectrum of galaxy M15_77745. Below it: mean pull squared in 25 Å bins and the cumulative chi-squared fraction against wavelength. Uncertainty: sigma includes the fitted calibration floor of 4.68 percent of the model flux. Comparison: the stored pull versus the pull at the best sample. Shaded bands mark masked pixels. Red points mark pixels with pull beyond 4 sigma. Total chi-squared 3954.9 over 3450 pixels, 8 outlier pixels. Caveat: the fitted floor absorbs model mismatch, so chi-squared near 1 does not prove a good model.</figcaption>
</figure>

<figure>
<img loading="lazy" src="/wiki/f/results/rtx-5060-dr2-quiescent-full-spectrum/77745-M15_77745/diagnostics/sf_timescales.png" alt="M15_77745: cumulative mass formed against lookback time with t10 to t90">
<figcaption><code>sf_timescales.png</code> Fraction of the final stellar mass of galaxy M15_77745 formed earlier than each lookback time. The line is the posterior median. The band is the 16-84 percent range over 400 draws. Comparison: points mark t10 to t90 with 16-84 percent (thick) and 2.5-97.5 percent (thin) intervals versus the universe age. t50 is 4.58 Gyr with a 16-84 percent range of 3.80 to 5.13 Gyr. Caveat: the 7-bin star-formation history model quantises these times to the bin edges.</figcaption>
</figure>

### 84337-M4_84337

| z | S/N | photometry χ²/N | spectrum χ²/N | f_calib | t50 [Gyr] | model |
| --- | --- | --- | --- | --- | --- | --- |
| 0.8388 | 14.9 | 7.35 | 1.071 | 5.76% | 4.23 | [parameters](/wiki/f/results/rtx-5060-dr2-quiescent-full-spectrum/84337-M4_84337/diagnostics/model_parameters.txt) |

Flags:

- photometry chi2/N 7.3 > 3
- 3 pixels with |pull| > 4

<figure>
<img loading="lazy" src="/wiki/f/results/rtx-5060-dr2-quiescent-full-spectrum/84337-M4_84337/diagnostics/photometric_chi2.png" alt="M4_84337: photometric pull and chi-squared contribution per band">
<figcaption><code>photometric_chi2.png</code> Pull and chi-squared contribution for the 12 COSMOS2015 bands of galaxy M4_84337. Pull equals observed minus model over sigma. Uncertainty: sigma includes the 5 percent flux floor. Comparison: filled points use the posterior-median model. Open squares use the best sample with the fit's own sigma. Total chi-squared 88.2 over 12 bands gives 7.35 per band. Caveat: the spectrum dominates the joint fit, so the fit does not constrain the bands on their own.</figcaption>
</figure>

<figure>
<img loading="lazy" src="/wiki/f/results/rtx-5060-dr2-quiescent-full-spectrum/84337-M4_84337/diagnostics/spectral_chi2.png" alt="M4_84337: spectral pull, binned mean pull squared, cumulative chi-squared">
<figcaption><code>spectral_chi2.png</code> Pull per fitted pixel of the LEGA-C spectrum of galaxy M4_84337. Below it: mean pull squared in 25 Å bins and the cumulative chi-squared fraction against wavelength. Uncertainty: sigma includes the fitted calibration floor of 5.76 percent of the model flux. Comparison: the stored pull versus the pull at the best sample. Shaded bands mark masked pixels. Red points mark pixels with pull beyond 4 sigma. Total chi-squared 3956.2 over 3695 pixels, 3 outlier pixels. Caveat: the fitted floor absorbs model mismatch, so chi-squared near 1 does not prove a good model.</figcaption>
</figure>

<figure>
<img loading="lazy" src="/wiki/f/results/rtx-5060-dr2-quiescent-full-spectrum/84337-M4_84337/diagnostics/sf_timescales.png" alt="M4_84337: cumulative mass formed against lookback time with t10 to t90">
<figcaption><code>sf_timescales.png</code> Fraction of the final stellar mass of galaxy M4_84337 formed earlier than each lookback time. The line is the posterior median. The band is the 16-84 percent range over 400 draws. Comparison: points mark t10 to t90 with 16-84 percent (thick) and 2.5-97.5 percent (thin) intervals versus the universe age. t50 is 4.23 Gyr with a 16-84 percent range of 3.68 to 5.02 Gyr. Caveat: the 7-bin star-formation history model quantises these times to the bin edges.</figcaption>
</figure>

### 87207-M15_87207

| z | S/N | photometry χ²/N | spectrum χ²/N | f_calib | t50 [Gyr] | model |
| --- | --- | --- | --- | --- | --- | --- |
| 0.8325 | 7.5 | 3.28 | 1.207 | 9.82% | 4.60 | [parameters](/wiki/f/results/rtx-5060-dr2-quiescent-full-spectrum/87207-M15_87207/diagnostics/model_parameters.txt) |

Flags:

- photometry chi2/N 3.3 > 3
- calibration floor at prior bound (9.8% of 10%)
- 5 pixels with |pull| > 4

<figure>
<img loading="lazy" src="/wiki/f/results/rtx-5060-dr2-quiescent-full-spectrum/87207-M15_87207/diagnostics/photometric_chi2.png" alt="M15_87207: photometric pull and chi-squared contribution per band">
<figcaption><code>photometric_chi2.png</code> Pull and chi-squared contribution for the 12 COSMOS2015 bands of galaxy M15_87207. Pull equals observed minus model over sigma. Uncertainty: sigma includes the 5 percent flux floor. Comparison: filled points use the posterior-median model. Open squares use the best sample with the fit's own sigma. Total chi-squared 39.4 over 12 bands gives 3.28 per band. Caveat: the spectrum dominates the joint fit, so the fit does not constrain the bands on their own.</figcaption>
</figure>

<figure>
<img loading="lazy" src="/wiki/f/results/rtx-5060-dr2-quiescent-full-spectrum/87207-M15_87207/diagnostics/spectral_chi2.png" alt="M15_87207: spectral pull, binned mean pull squared, cumulative chi-squared">
<figcaption><code>spectral_chi2.png</code> Pull per fitted pixel of the LEGA-C spectrum of galaxy M15_87207. Below it: mean pull squared in 25 Å bins and the cumulative chi-squared fraction against wavelength. Uncertainty: sigma includes the fitted calibration floor of 9.82 percent of the model flux. Comparison: the stored pull versus the pull at the best sample. Shaded bands mark masked pixels. Red points mark pixels with pull beyond 4 sigma. Total chi-squared 4600.9 over 3813 pixels, 5 outlier pixels. Caveat: the fitted floor absorbs model mismatch, so chi-squared near 1 does not prove a good model.</figcaption>
</figure>

<figure>
<img loading="lazy" src="/wiki/f/results/rtx-5060-dr2-quiescent-full-spectrum/87207-M15_87207/diagnostics/sf_timescales.png" alt="M15_87207: cumulative mass formed against lookback time with t10 to t90">
<figcaption><code>sf_timescales.png</code> Fraction of the final stellar mass of galaxy M15_87207 formed earlier than each lookback time. The line is the posterior median. The band is the 16-84 percent range over 400 draws. Comparison: points mark t10 to t90 with 16-84 percent (thick) and 2.5-97.5 percent (thin) intervals versus the universe age. t50 is 4.60 Gyr with a 16-84 percent range of 4.31 to 4.89 Gyr. Caveat: the 7-bin star-formation history model quantises these times to the bin edges.</figcaption>
</figure>

### 88032-M15_88032

| z | S/N | photometry χ²/N | spectrum χ²/N | f_calib | t50 [Gyr] | model |
| --- | --- | --- | --- | --- | --- | --- |
| 0.8392 | 22.6 | 4.70 | 1.114 | 5.39% | 2.81 | [parameters](/wiki/f/results/rtx-5060-dr2-quiescent-full-spectrum/88032-M15_88032/diagnostics/model_parameters.txt) |

Flags:

- photometry chi2/N 4.7 > 3
- 3 pixels with |pull| > 4

<figure>
<img loading="lazy" src="/wiki/f/results/rtx-5060-dr2-quiescent-full-spectrum/88032-M15_88032/diagnostics/photometric_chi2.png" alt="M15_88032: photometric pull and chi-squared contribution per band">
<figcaption><code>photometric_chi2.png</code> Pull and chi-squared contribution for the 12 COSMOS2015 bands of galaxy M15_88032. Pull equals observed minus model over sigma. Uncertainty: sigma includes the 5 percent flux floor. Comparison: filled points use the posterior-median model. Open squares use the best sample with the fit's own sigma. Total chi-squared 56.3 over 12 bands gives 4.70 per band. Caveat: the spectrum dominates the joint fit, so the fit does not constrain the bands on their own.</figcaption>
</figure>

<figure>
<img loading="lazy" src="/wiki/f/results/rtx-5060-dr2-quiescent-full-spectrum/88032-M15_88032/diagnostics/spectral_chi2.png" alt="M15_88032: spectral pull, binned mean pull squared, cumulative chi-squared">
<figcaption><code>spectral_chi2.png</code> Pull per fitted pixel of the LEGA-C spectrum of galaxy M15_88032. Below it: mean pull squared in 25 Å bins and the cumulative chi-squared fraction against wavelength. Uncertainty: sigma includes the fitted calibration floor of 5.39 percent of the model flux. Comparison: the stored pull versus the pull at the best sample. Shaded bands mark masked pixels. Red points mark pixels with pull beyond 4 sigma. Total chi-squared 4064.3 over 3649 pixels, 3 outlier pixels. Caveat: the fitted floor absorbs model mismatch, so chi-squared near 1 does not prove a good model.</figcaption>
</figure>

<figure>
<img loading="lazy" src="/wiki/f/results/rtx-5060-dr2-quiescent-full-spectrum/88032-M15_88032/diagnostics/sf_timescales.png" alt="M15_88032: cumulative mass formed against lookback time with t10 to t90">
<figcaption><code>sf_timescales.png</code> Fraction of the final stellar mass of galaxy M15_88032 formed earlier than each lookback time. The line is the posterior median. The band is the 16-84 percent range over 400 draws. Comparison: points mark t10 to t90 with 16-84 percent (thick) and 2.5-97.5 percent (thin) intervals versus the universe age. t50 is 2.81 Gyr with a 16-84 percent range of 2.78 to 2.89 Gyr. Caveat: the 7-bin star-formation history model quantises these times to the bin edges.</figcaption>
</figure>

### 89072-M15_89072

| z | S/N | photometry χ²/N | spectrum χ²/N | f_calib | t50 [Gyr] | model |
| --- | --- | --- | --- | --- | --- | --- |
| 0.8370 | 7.1 | 2.31 | 1.154 | 9.88% | 2.93 | [parameters](/wiki/f/results/rtx-5060-dr2-quiescent-full-spectrum/89072-M15_89072/diagnostics/model_parameters.txt) |

Flags:

- calibration floor at prior bound (9.9% of 10%)
- 5 pixels with |pull| > 4

<figure>
<img loading="lazy" src="/wiki/f/results/rtx-5060-dr2-quiescent-full-spectrum/89072-M15_89072/diagnostics/photometric_chi2.png" alt="M15_89072: photometric pull and chi-squared contribution per band">
<figcaption><code>photometric_chi2.png</code> Pull and chi-squared contribution for the 12 COSMOS2015 bands of galaxy M15_89072. Pull equals observed minus model over sigma. Uncertainty: sigma includes the 5 percent flux floor. Comparison: filled points use the posterior-median model. Open squares use the best sample with the fit's own sigma. Total chi-squared 27.8 over 12 bands gives 2.31 per band. Caveat: the spectrum dominates the joint fit, so the fit does not constrain the bands on their own.</figcaption>
</figure>

<figure>
<img loading="lazy" src="/wiki/f/results/rtx-5060-dr2-quiescent-full-spectrum/89072-M15_89072/diagnostics/spectral_chi2.png" alt="M15_89072: spectral pull, binned mean pull squared, cumulative chi-squared">
<figcaption><code>spectral_chi2.png</code> Pull per fitted pixel of the LEGA-C spectrum of galaxy M15_89072. Below it: mean pull squared in 25 Å bins and the cumulative chi-squared fraction against wavelength. Uncertainty: sigma includes the fitted calibration floor of 9.88 percent of the model flux. Comparison: the stored pull versus the pull at the best sample. Shaded bands mark masked pixels. Red points mark pixels with pull beyond 4 sigma. Total chi-squared 4224.3 over 3661 pixels, 5 outlier pixels. Caveat: the fitted floor absorbs model mismatch, so chi-squared near 1 does not prove a good model.</figcaption>
</figure>

<figure>
<img loading="lazy" src="/wiki/f/results/rtx-5060-dr2-quiescent-full-spectrum/89072-M15_89072/diagnostics/sf_timescales.png" alt="M15_89072: cumulative mass formed against lookback time with t10 to t90">
<figcaption><code>sf_timescales.png</code> Fraction of the final stellar mass of galaxy M15_89072 formed earlier than each lookback time. The line is the posterior median. The band is the 16-84 percent range over 400 draws. Comparison: points mark t10 to t90 with 16-84 percent (thick) and 2.5-97.5 percent (thin) intervals versus the universe age. t50 is 2.93 Gyr with a 16-84 percent range of 2.82 to 3.12 Gyr. Caveat: the 7-bin star-formation history model quantises these times to the bin edges.</figcaption>
</figure>

### 89153-M15_89153

| z | S/N | photometry χ²/N | spectrum χ²/N | f_calib | t50 [Gyr] | model |
| --- | --- | --- | --- | --- | --- | --- |
| 0.8351 | 9.8 | 3.58 | 1.127 | 9.36% | 1.64 | [parameters](/wiki/f/results/rtx-5060-dr2-quiescent-full-spectrum/89153-M15_89153/diagnostics/model_parameters.txt) |

Flags:

- photometry chi2/N 3.6 > 3
- 4 pixels with |pull| > 4

<figure>
<img loading="lazy" src="/wiki/f/results/rtx-5060-dr2-quiescent-full-spectrum/89153-M15_89153/diagnostics/photometric_chi2.png" alt="M15_89153: photometric pull and chi-squared contribution per band">
<figcaption><code>photometric_chi2.png</code> Pull and chi-squared contribution for the 12 COSMOS2015 bands of galaxy M15_89153. Pull equals observed minus model over sigma. Uncertainty: sigma includes the 5 percent flux floor. Comparison: filled points use the posterior-median model. Open squares use the best sample with the fit's own sigma. Total chi-squared 43.0 over 12 bands gives 3.58 per band. Caveat: the spectrum dominates the joint fit, so the fit does not constrain the bands on their own.</figcaption>
</figure>

<figure>
<img loading="lazy" src="/wiki/f/results/rtx-5060-dr2-quiescent-full-spectrum/89153-M15_89153/diagnostics/spectral_chi2.png" alt="M15_89153: spectral pull, binned mean pull squared, cumulative chi-squared">
<figcaption><code>spectral_chi2.png</code> Pull per fitted pixel of the LEGA-C spectrum of galaxy M15_89153. Below it: mean pull squared in 25 Å bins and the cumulative chi-squared fraction against wavelength. Uncertainty: sigma includes the fitted calibration floor of 9.36 percent of the model flux. Comparison: the stored pull versus the pull at the best sample. Shaded bands mark masked pixels. Red points mark pixels with pull beyond 4 sigma. Total chi-squared 3847.9 over 3414 pixels, 4 outlier pixels. Caveat: the fitted floor absorbs model mismatch, so chi-squared near 1 does not prove a good model.</figcaption>
</figure>

<figure>
<img loading="lazy" src="/wiki/f/results/rtx-5060-dr2-quiescent-full-spectrum/89153-M15_89153/diagnostics/sf_timescales.png" alt="M15_89153: cumulative mass formed against lookback time with t10 to t90">
<figcaption><code>sf_timescales.png</code> Fraction of the final stellar mass of galaxy M15_89153 formed earlier than each lookback time. The line is the posterior median. The band is the 16-84 percent range over 400 draws. Comparison: points mark t10 to t90 with 16-84 percent (thick) and 2.5-97.5 percent (thin) intervals versus the universe age. t50 is 1.64 Gyr with a 16-84 percent range of 1.62 to 1.71 Gyr. Caveat: the 7-bin star-formation history model quantises these times to the bin edges.</figcaption>
</figure>

### 91529-M12_91529

| z | S/N | photometry χ²/N | spectrum χ²/N | f_calib | t50 [Gyr] | model |
| --- | --- | --- | --- | --- | --- | --- |
| 0.8406 | 34.8 | 5.12 | 1.106 | 4.60% | 2.26 | [parameters](/wiki/f/results/rtx-5060-dr2-quiescent-full-spectrum/91529-M12_91529/diagnostics/model_parameters.txt) |

Flags:

- photometry chi2/N 5.1 > 3
- 2 pixels with |pull| > 4

<figure>
<img loading="lazy" src="/wiki/f/results/rtx-5060-dr2-quiescent-full-spectrum/91529-M12_91529/diagnostics/photometric_chi2.png" alt="M12_91529: photometric pull and chi-squared contribution per band">
<figcaption><code>photometric_chi2.png</code> Pull and chi-squared contribution for the 12 COSMOS2015 bands of galaxy M12_91529. Pull equals observed minus model over sigma. Uncertainty: sigma includes the 5 percent flux floor. Comparison: filled points use the posterior-median model. Open squares use the best sample with the fit's own sigma. Total chi-squared 61.4 over 12 bands gives 5.12 per band. Caveat: the spectrum dominates the joint fit, so the fit does not constrain the bands on their own.</figcaption>
</figure>

<figure>
<img loading="lazy" src="/wiki/f/results/rtx-5060-dr2-quiescent-full-spectrum/91529-M12_91529/diagnostics/spectral_chi2.png" alt="M12_91529: spectral pull, binned mean pull squared, cumulative chi-squared">
<figcaption><code>spectral_chi2.png</code> Pull per fitted pixel of the LEGA-C spectrum of galaxy M12_91529. Below it: mean pull squared in 25 Å bins and the cumulative chi-squared fraction against wavelength. Uncertainty: sigma includes the fitted calibration floor of 4.60 percent of the model flux. Comparison: the stored pull versus the pull at the best sample. Shaded bands mark masked pixels. Red points mark pixels with pull beyond 4 sigma. Total chi-squared 4226.2 over 3821 pixels, 2 outlier pixels. Caveat: the fitted floor absorbs model mismatch, so chi-squared near 1 does not prove a good model.</figcaption>
</figure>

<figure>
<img loading="lazy" src="/wiki/f/results/rtx-5060-dr2-quiescent-full-spectrum/91529-M12_91529/diagnostics/sf_timescales.png" alt="M12_91529: cumulative mass formed against lookback time with t10 to t90">
<figcaption><code>sf_timescales.png</code> Fraction of the final stellar mass of galaxy M12_91529 formed earlier than each lookback time. The line is the posterior median. The band is the 16-84 percent range over 400 draws. Comparison: points mark t10 to t90 with 16-84 percent (thick) and 2.5-97.5 percent (thin) intervals versus the universe age. t50 is 2.26 Gyr with a 16-84 percent range of 2.22 to 2.30 Gyr. Caveat: the 7-bin star-formation history model quantises these times to the bin edges.</figcaption>
</figure>

### 92132-M12_92132

| z | S/N | photometry χ²/N | spectrum χ²/N | f_calib | t50 [Gyr] | model |
| --- | --- | --- | --- | --- | --- | --- |
| 0.7475 | 16.1 | 7.16 | 1.126 | 6.63% | 2.69 | [parameters](/wiki/f/results/rtx-5060-dr2-quiescent-full-spectrum/92132-M12_92132/diagnostics/model_parameters.txt) |

Flags:

- photometry chi2/N 7.2 > 3
- 2 pixels with |pull| > 4

<figure>
<img loading="lazy" src="/wiki/f/results/rtx-5060-dr2-quiescent-full-spectrum/92132-M12_92132/diagnostics/photometric_chi2.png" alt="M12_92132: photometric pull and chi-squared contribution per band">
<figcaption><code>photometric_chi2.png</code> Pull and chi-squared contribution for the 12 COSMOS2015 bands of galaxy M12_92132. Pull equals observed minus model over sigma. Uncertainty: sigma includes the 5 percent flux floor. Comparison: filled points use the posterior-median model. Open squares use the best sample with the fit's own sigma. Total chi-squared 85.9 over 12 bands gives 7.16 per band. Caveat: the spectrum dominates the joint fit, so the fit does not constrain the bands on their own.</figcaption>
</figure>

<figure>
<img loading="lazy" src="/wiki/f/results/rtx-5060-dr2-quiescent-full-spectrum/92132-M12_92132/diagnostics/spectral_chi2.png" alt="M12_92132: spectral pull, binned mean pull squared, cumulative chi-squared">
<figcaption><code>spectral_chi2.png</code> Pull per fitted pixel of the LEGA-C spectrum of galaxy M12_92132. Below it: mean pull squared in 25 Å bins and the cumulative chi-squared fraction against wavelength. Uncertainty: sigma includes the fitted calibration floor of 6.63 percent of the model flux. Comparison: the stored pull versus the pull at the best sample. Shaded bands mark masked pixels. Red points mark pixels with pull beyond 4 sigma. Total chi-squared 4297.6 over 3817 pixels, 2 outlier pixels. Caveat: the fitted floor absorbs model mismatch, so chi-squared near 1 does not prove a good model.</figcaption>
</figure>

<figure>
<img loading="lazy" src="/wiki/f/results/rtx-5060-dr2-quiescent-full-spectrum/92132-M12_92132/diagnostics/sf_timescales.png" alt="M12_92132: cumulative mass formed against lookback time with t10 to t90">
<figcaption><code>sf_timescales.png</code> Fraction of the final stellar mass of galaxy M12_92132 formed earlier than each lookback time. The line is the posterior median. The band is the 16-84 percent range over 400 draws. Comparison: points mark t10 to t90 with 16-84 percent (thick) and 2.5-97.5 percent (thin) intervals versus the universe age. t50 is 2.69 Gyr with a 16-84 percent range of 2.63 to 2.76 Gyr. Caveat: the 7-bin star-formation history model quantises these times to the bin edges.</figcaption>
</figure>

### 93943-M2_93943

| z | S/N | photometry χ²/N | spectrum χ²/N | f_calib | t50 [Gyr] | model |
| --- | --- | --- | --- | --- | --- | --- |
| 0.8800 | 13.1 | 9.15 | 1.011 | 3.72% | 1.65 | [parameters](/wiki/f/results/rtx-5060-dr2-quiescent-full-spectrum/93943-M2_93943/diagnostics/model_parameters.txt) |

Flags:

- photometry chi2/N 9.2 > 3
- 5 pixels with |pull| > 4

<figure>
<img loading="lazy" src="/wiki/f/results/rtx-5060-dr2-quiescent-full-spectrum/93943-M2_93943/diagnostics/photometric_chi2.png" alt="M2_93943: photometric pull and chi-squared contribution per band">
<figcaption><code>photometric_chi2.png</code> Pull and chi-squared contribution for the 12 COSMOS2015 bands of galaxy M2_93943. Pull equals observed minus model over sigma. Uncertainty: sigma includes the 5 percent flux floor. Comparison: filled points use the posterior-median model. Open squares use the best sample with the fit's own sigma. Total chi-squared 109.8 over 12 bands gives 9.15 per band. Caveat: the spectrum dominates the joint fit, so the fit does not constrain the bands on their own.</figcaption>
</figure>

<figure>
<img loading="lazy" src="/wiki/f/results/rtx-5060-dr2-quiescent-full-spectrum/93943-M2_93943/diagnostics/spectral_chi2.png" alt="M2_93943: spectral pull, binned mean pull squared, cumulative chi-squared">
<figcaption><code>spectral_chi2.png</code> Pull per fitted pixel of the LEGA-C spectrum of galaxy M2_93943. Below it: mean pull squared in 25 Å bins and the cumulative chi-squared fraction against wavelength. Uncertainty: sigma includes the fitted calibration floor of 3.72 percent of the model flux. Comparison: the stored pull versus the pull at the best sample. Shaded bands mark masked pixels. Red points mark pixels with pull beyond 4 sigma. Total chi-squared 3877.6 over 3836 pixels, 5 outlier pixels. Caveat: the fitted floor absorbs model mismatch, so chi-squared near 1 does not prove a good model.</figcaption>
</figure>

<figure>
<img loading="lazy" src="/wiki/f/results/rtx-5060-dr2-quiescent-full-spectrum/93943-M2_93943/diagnostics/sf_timescales.png" alt="M2_93943: cumulative mass formed against lookback time with t10 to t90">
<figcaption><code>sf_timescales.png</code> Fraction of the final stellar mass of galaxy M2_93943 formed earlier than each lookback time. The line is the posterior median. The band is the 16-84 percent range over 400 draws. Comparison: points mark t10 to t90 with 16-84 percent (thick) and 2.5-97.5 percent (thin) intervals versus the universe age. t50 is 1.65 Gyr with a 16-84 percent range of 1.64 to 1.66 Gyr. Caveat: the 7-bin star-formation history model quantises these times to the bin edges.</figcaption>
</figure>

### 94494-M2_94494

| z | S/N | photometry χ²/N | spectrum χ²/N | f_calib | t50 [Gyr] | model |
| --- | --- | --- | --- | --- | --- | --- |
| 0.7401 | 30.6 | 6.15 | 1.044 | 4.04% | 2.90 | [parameters](/wiki/f/results/rtx-5060-dr2-quiescent-full-spectrum/94494-M2_94494/diagnostics/model_parameters.txt) |

Flags:

- photometry chi2/N 6.2 > 3
- 4 pixels with |pull| > 4

<figure>
<img loading="lazy" src="/wiki/f/results/rtx-5060-dr2-quiescent-full-spectrum/94494-M2_94494/diagnostics/photometric_chi2.png" alt="M2_94494: photometric pull and chi-squared contribution per band">
<figcaption><code>photometric_chi2.png</code> Pull and chi-squared contribution for the 12 COSMOS2015 bands of galaxy M2_94494. Pull equals observed minus model over sigma. Uncertainty: sigma includes the 5 percent flux floor. Comparison: filled points use the posterior-median model. Open squares use the best sample with the fit's own sigma. Total chi-squared 73.8 over 12 bands gives 6.15 per band. Caveat: the spectrum dominates the joint fit, so the fit does not constrain the bands on their own.</figcaption>
</figure>

<figure>
<img loading="lazy" src="/wiki/f/results/rtx-5060-dr2-quiescent-full-spectrum/94494-M2_94494/diagnostics/spectral_chi2.png" alt="M2_94494: spectral pull, binned mean pull squared, cumulative chi-squared">
<figcaption><code>spectral_chi2.png</code> Pull per fitted pixel of the LEGA-C spectrum of galaxy M2_94494. Below it: mean pull squared in 25 Å bins and the cumulative chi-squared fraction against wavelength. Uncertainty: sigma includes the fitted calibration floor of 4.04 percent of the model flux. Comparison: the stored pull versus the pull at the best sample. Shaded bands mark masked pixels. Red points mark pixels with pull beyond 4 sigma. Total chi-squared 3685.9 over 3530 pixels, 4 outlier pixels. Caveat: the fitted floor absorbs model mismatch, so chi-squared near 1 does not prove a good model.</figcaption>
</figure>

<figure>
<img loading="lazy" src="/wiki/f/results/rtx-5060-dr2-quiescent-full-spectrum/94494-M2_94494/diagnostics/sf_timescales.png" alt="M2_94494: cumulative mass formed against lookback time with t10 to t90">
<figcaption><code>sf_timescales.png</code> Fraction of the final stellar mass of galaxy M2_94494 formed earlier than each lookback time. The line is the posterior median. The band is the 16-84 percent range over 400 draws. Comparison: points mark t10 to t90 with 16-84 percent (thick) and 2.5-97.5 percent (thin) intervals versus the universe age. t50 is 2.90 Gyr with a 16-84 percent range of 2.87 to 2.93 Gyr. Caveat: the 7-bin star-formation history model quantises these times to the bin edges.</figcaption>
</figure>

### 97310-M2_97310

| z | S/N | photometry χ²/N | spectrum χ²/N | f_calib | t50 [Gyr] | model |
| --- | --- | --- | --- | --- | --- | --- |
| 0.9428 | 6.9 | 3.45 | 0.972 | 5.18% | 1.75 | [parameters](/wiki/f/results/rtx-5060-dr2-quiescent-full-spectrum/97310-M2_97310/diagnostics/model_parameters.txt) |

Flags:

- photometry chi2/N 3.4 > 3
- 1 pixels with |pull| > 4

<figure>
<img loading="lazy" src="/wiki/f/results/rtx-5060-dr2-quiescent-full-spectrum/97310-M2_97310/diagnostics/photometric_chi2.png" alt="M2_97310: photometric pull and chi-squared contribution per band">
<figcaption><code>photometric_chi2.png</code> Pull and chi-squared contribution for the 12 COSMOS2015 bands of galaxy M2_97310. Pull equals observed minus model over sigma. Uncertainty: sigma includes the 5 percent flux floor. Comparison: filled points use the posterior-median model. Open squares use the best sample with the fit's own sigma. Total chi-squared 41.4 over 12 bands gives 3.45 per band. Caveat: the spectrum dominates the joint fit, so the fit does not constrain the bands on their own.</figcaption>
</figure>

<figure>
<img loading="lazy" src="/wiki/f/results/rtx-5060-dr2-quiescent-full-spectrum/97310-M2_97310/diagnostics/spectral_chi2.png" alt="M2_97310: spectral pull, binned mean pull squared, cumulative chi-squared">
<figcaption><code>spectral_chi2.png</code> Pull per fitted pixel of the LEGA-C spectrum of galaxy M2_97310. Below it: mean pull squared in 25 Å bins and the cumulative chi-squared fraction against wavelength. Uncertainty: sigma includes the fitted calibration floor of 5.18 percent of the model flux. Comparison: the stored pull versus the pull at the best sample. Shaded bands mark masked pixels. Red points mark pixels with pull beyond 4 sigma. Total chi-squared 3700.7 over 3806 pixels, 1 outlier pixels. Caveat: the fitted floor absorbs model mismatch, so chi-squared near 1 does not prove a good model.</figcaption>
</figure>

<figure>
<img loading="lazy" src="/wiki/f/results/rtx-5060-dr2-quiescent-full-spectrum/97310-M2_97310/diagnostics/sf_timescales.png" alt="M2_97310: cumulative mass formed against lookback time with t10 to t90">
<figcaption><code>sf_timescales.png</code> Fraction of the final stellar mass of galaxy M2_97310 formed earlier than each lookback time. The line is the posterior median. The band is the 16-84 percent range over 400 draws. Comparison: points mark t10 to t90 with 16-84 percent (thick) and 2.5-97.5 percent (thin) intervals versus the universe age. t50 is 1.75 Gyr with a 16-84 percent range of 1.66 to 2.01 Gyr. Caveat: the 7-bin star-formation history model quantises these times to the bin edges.</figcaption>
</figure>

### 98104-M12_98104

| z | S/N | photometry χ²/N | spectrum χ²/N | f_calib | t50 [Gyr] | model |
| --- | --- | --- | --- | --- | --- | --- |
| 0.9814 | 6.6 | 4.06 | 1.554 | 9.98% | 3.00 | [parameters](/wiki/f/results/rtx-5060-dr2-quiescent-full-spectrum/98104-M12_98104/diagnostics/model_parameters.txt) |

Flags:

- photometry chi2/N 4.1 > 3
- spectrum chi2/N 1.55 > 1.5
- calibration floor at prior bound (10.0% of 10%)
- 14 pixels with |pull| > 4

<figure>
<img loading="lazy" src="/wiki/f/results/rtx-5060-dr2-quiescent-full-spectrum/98104-M12_98104/diagnostics/photometric_chi2.png" alt="M12_98104: photometric pull and chi-squared contribution per band">
<figcaption><code>photometric_chi2.png</code> Pull and chi-squared contribution for the 12 COSMOS2015 bands of galaxy M12_98104. Pull equals observed minus model over sigma. Uncertainty: sigma includes the 5 percent flux floor. Comparison: filled points use the posterior-median model. Open squares use the best sample with the fit's own sigma. Total chi-squared 48.7 over 12 bands gives 4.06 per band. Caveat: the spectrum dominates the joint fit, so the fit does not constrain the bands on their own.</figcaption>
</figure>

<figure>
<img loading="lazy" src="/wiki/f/results/rtx-5060-dr2-quiescent-full-spectrum/98104-M12_98104/diagnostics/spectral_chi2.png" alt="M12_98104: spectral pull, binned mean pull squared, cumulative chi-squared">
<figcaption><code>spectral_chi2.png</code> Pull per fitted pixel of the LEGA-C spectrum of galaxy M12_98104. Below it: mean pull squared in 25 Å bins and the cumulative chi-squared fraction against wavelength. Uncertainty: sigma includes the fitted calibration floor of 9.98 percent of the model flux. Comparison: the stored pull versus the pull at the best sample. Shaded bands mark masked pixels. Red points mark pixels with pull beyond 4 sigma. Total chi-squared 5912.6 over 3804 pixels, 14 outlier pixels. Caveat: the fitted floor absorbs model mismatch, so chi-squared near 1 does not prove a good model.</figcaption>
</figure>

<figure>
<img loading="lazy" src="/wiki/f/results/rtx-5060-dr2-quiescent-full-spectrum/98104-M12_98104/diagnostics/sf_timescales.png" alt="M12_98104: cumulative mass formed against lookback time with t10 to t90">
<figcaption><code>sf_timescales.png</code> Fraction of the final stellar mass of galaxy M12_98104 formed earlier than each lookback time. The line is the posterior median. The band is the 16-84 percent range over 400 draws. Comparison: points mark t10 to t90 with 16-84 percent (thick) and 2.5-97.5 percent (thin) intervals versus the universe age. t50 is 3.00 Gyr with a 16-84 percent range of 2.95 to 3.08 Gyr. Caveat: the 7-bin star-formation history model quantises these times to the bin edges.</figcaption>
</figure>
