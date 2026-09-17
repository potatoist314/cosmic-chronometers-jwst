---
title: Current default model
date: 2026-09-15
section: Codebase
tags: [ceridwen, priors, parameters]
job:
theme: Model and code reference
status: obsolete
superseded_by: papers-quiescent-parameters
---

<p class="default-model-meta">Full spectrum + total photometry · 14 free values · 15 September 2026</p>

<table class="default-parameter-table" aria-label="Default sampled parameters">
<thead><tr><th scope="col">Parameter</th><th scope="col">Default prior</th><th scope="col">Physical meaning</th></tr></thead>
<tbody>
<tr data-parameter="logmass" data-count="1"><th scope="row">Formed stellar mass<code>logmass</code></th><td data-label="Default prior">\(\operatorname{Uniform}(8,\allowbreak 13)\)</td><td data-label="Physical meaning">\(\log_{10}\) of total mass formed in solar masses, before stellar mass loss.</td></tr>
<tr data-parameter="Z" data-count="1"><th scope="row">Metallicity coordinate<code>Z</code></th><td data-label="Default prior">\(\operatorname{Uniform}(-4.2327283,\allowbreak -1.2329283)\)<small>Grid limits inset by 0.0001 dex; endpoints rounded here.</small></td><td data-label="Physical meaning">Stored as \([\mathrm{Fe}/\mathrm{H}]+\log_{10}(0.0185)\). Add 1.7328283 to recover \([\mathrm{Fe}/\mathrm{H}]\). Total metallicity also depends on <code>afe</code>.</td></tr>
<tr data-parameter="afe" data-count="1"><th scope="row">Alpha enhancement<code>afe</code></th><td data-label="Default prior">\(\operatorname{Uniform}(-0.2,\allowbreak 0.6)\)</td><td data-label="Physical meaning">\([\alpha/\mathrm{Fe}]\) in dex, shared by all stellar ages.</td></tr>
<tr data-parameter="logsfr_ratios" data-count="7"><th scope="row">SFH ratios \(\times\) 7<code>logsfr_ratios[0:7]</code></th><td data-label="Default prior">Independent Student-t<small>Centre 0, scale 0.3 dex, df = 2; unbounded.</small></td><td data-label="Physical meaning">\(\log_{10}(\mathrm{SFR}_i/\mathrm{SFR}_{i+1})\) across eight lookback-time nodes. Positive means more recent star formation exceeds the next older node.</td></tr>
<tr data-parameter="diffuse_tau_kc" data-count="1"><th scope="row">Diffuse dust strength<code>diffuse_tau_kc</code></th><td data-label="Default prior">\(\operatorname{Uniform}(0,\allowbreak 0.2)\)</td><td data-label="Physical meaning">Optical-depth normalization of the Kriek–Conroy curve, approximately the optical depth at 5500 \(\text{\AA}\). Attenuation multiplies the spectrum by \(\exp(-\tau(\lambda))\).</td></tr>
<tr data-parameter="diffuse_dust_index" data-count="1"><th scope="row">Dust slope<code>diffuse_dust_index</code></th><td data-label="Default prior">\(\operatorname{Uniform}(-1.0,\allowbreak 0.4)\)</td><td data-label="Physical meaning">Power-law tilt about 5500 \(\text{\AA}\); more negative gives steeper blue attenuation. The UV bump strength is tied to this slope.</td></tr>
<tr data-parameter="log_f_calib" data-count="1"><th scope="row">Extra spectral error<code>log_f_calib</code></th><td data-label="Default prior">\(\operatorname{Uniform}(\ln 0.01,\allowbreak \ln 0.10)\)<small>Log-uniform fraction: 1–10%.</small></td><td data-label="Physical meaning">Natural log of the extra model-flux fraction added in quadrature to spectral errors: \(\mathrm{variance}=\sigma_{\mathrm{obs}}^2+(\exp(\mathrm{log\_f\_calib})\times\mathrm{model})^2\).</td></tr>
<tr data-parameter="spectrum_scaling" data-count="1"><th scope="row">Spectrum normalization<code>spectrum_scaling</code></th><td data-label="Default prior">\(\operatorname{Normal}(1,\sigma=0.3)\)<small>Truncated to [0.2, 3.0].</small></td><td data-label="Physical meaning">Multiplies the model spectrum relative to the photometry. Photometric predictions retain the mass normalization.</td></tr>
</tbody>
</table>

## Fixed settings

<table class="default-parameter-table default-fixed-table" aria-label="Fixed model settings">
<thead><tr><th scope="col">Setting</th><th scope="col">Default</th></tr></thead>
<tbody>
<tr><th scope="row">Redshift and broadening</th><td data-label="Default">Catalogue redshift and stellar velocity dispersion. <code>Spectrum</code> applies the broadening; CSP broadening is zero.</td></tr>
<tr><th scope="row">SSP grid and IMF</th><td data-label="Default"><code>amist_c3k_hr_krou_afe</code>: aMIST v2.5, C3K v2.3 high resolution, Kroupa IMF.</td></tr>
<tr><th scope="row">SFH and abundances</th><td data-label="Default">Eight nodes at 0, 0.03, 0.1, 0.3, 1, 3, 5 and the Universe's age at catalogue redshift, in Gyr lookback time. Step interpolation; <code>Z</code> and <code>afe</code> constant across ages.</td></tr>
<tr><th scope="row">Dust and emission</th><td data-label="Default">Diffuse attenuation on. Birth-cloud dust, dust emission and IGM attenuation off. No nebular emission in <code>CSPBasis_afe</code>.</td></tr>
<tr><th scope="row">Photometry</th><td data-label="Default">Twelve COSMOS2015 total-flux bands. A fixed 5% of observed flux is added in quadrature to each photometric error.</td></tr>
</tbody>
</table>

## Marginalised calibration

<table class="default-parameter-table" aria-label="Marginalised calibration prior">
<thead><tr><th scope="col">Parameter</th><th scope="col">Default prior</th><th scope="col">Physical meaning</th></tr></thead>
<tbody>
<tr><th scope="row">Chebyshev coefficients \(\times\) 3<small>\(a_1,a_2,a_3\)</small></th><td data-label="Default prior">Independent \(\operatorname{Normal}(0,\sigma=0.1)\)</td><td data-label="Physical meaning">Multiply the spectrum by \(P(x)=1+a_1T_1(x)+a_2T_2(x)+a_3T_3(x)\), over the fitted wavelength range. Integrated out analytically; excluded from the 14 sampled values.</td></tr>
</tbody>
</table>

<p class="default-model-sources">Sources: <a href="/wiki/f/notebooks/ceridwen_integrated_photometry_spectra.ipynb" title="ceridwen_integrated_photometry_spectra.ipynb · cells 2, 12, 14, 16, 18, 20 (zero-based) · configuration, joint_priors, calibration_polynomial">Notebook defaults</a> · <a href="/wiki/f/ceridwen/scripts_afe/build_afe_hr_grid.py#L134" title="ceridwen/scripts_afe/build_afe_hr_grid.py:134–155 · ssp_lgmet and SSP metadata">Grid units</a> · <a href="/wiki/f/ceridwen/ceridwen/model/transforms.py#L79" title="ceridwen/ceridwen/model/transforms.py:79–169 · logsfr_ratios_to_sfh">SFH</a> · <a href="/wiki/f/external/sedpy_jax/sedpy_jax/attenuation_dust.py#L354" title="external/sedpy_jax/sedpy_jax/attenuation_dust.py:354–399 · kriek_conroy">Dust</a> · <a href="/wiki/f/ceridwen/ceridwen/sampler/priors.py" title="ceridwen/ceridwen/sampler/priors.py · ClippedNormal, StudentT">Distributions</a> · <a href="/wiki/f/ceridwen/ceridwen/likelihood/noise_model.py#L325" title="ceridwen/ceridwen/likelihood/noise_model.py:325–331 · DiagonalNoiseModel">Spectral error</a> · <a href="/wiki/f/ceridwen/ceridwen/likelihood/calibration.py#L82" title="ceridwen/ceridwen/likelihood/calibration.py:82–180 · PolynomialCalibration">Calibration</a></p>
