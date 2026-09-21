---
title: Model
date: 2026-09-17
section: Literature
theme: Background reading
tags: [model, assumptions, settings, priors, parameters, defaults, papers, quiescent, lega-c]
job:
source: papers/quiescent populations/README.md
figures: [literature-vs-ceridwen.png]
---

## Sample and data

<dl class="model-group">
<div class="model-row"><span class="model-s">Parent match</span><span class="model-v">DR2 × COSMOS2015; <code>f_use</code> 1, <code>f_ppxf</code> 0, <code>f_z</code> 0, <code>f_int</code> 0, S/N &gt; 0, 0.6 ≤ z &lt; 1.0, rest NUV, r, J present · 1328</span><span class="model-w"></span><span class="model-f"></span></div>
<div class="model-row"><span class="model-s">Passive</span><span class="model-v">NUV − r &gt; 3 (r − J) + 1 and NUV − r &gt; 3.1 · 609</span><span class="model-w"></span><span class="model-f"></span></div>
<div class="model-row"><span class="model-s">Weak [O II]</span><span class="model-v">EW([O II] 3727) &gt; −5 \(\text{\AA}\) or missing · 454</span><span class="model-w"></span><span class="model-f"></span></div>
<div class="model-row"><span class="model-s">No emission detected</span><span class="model-v">\(\lvert \mathrm{EW}/\sigma_{\mathrm{EW}} \rvert\) &lt; 3 for [O II] 3727 and [O III] 5007 · 349</span><span class="model-w"></span><span class="model-f"></span></div>
<div class="model-row"><span class="model-s">Clean photometry</span><span class="model-v">COSMOS2015 Area 0, Sat 0, Cfl 1, Flag 0 · 194</span><span class="model-w"></span><span class="model-f"></span></div>
<div class="model-row"><span class="model-s">One spectrum per object</span><span class="model-v">Highest S/N kept · 187</span><span class="model-w"></span><span class="model-f"></span></div>
<details class="model-row"><summary><span class="model-s">Pixels</span><span class="model-v"><code>QUAL</code> 0, error &gt; 0, finite flux; over 3000 good pixels; fitted &gt; 0.7 × good</span><span class="model-w"></span><span class="model-f"></span></summary><ul><li><i>source</i> guard set when the line and CN masks were added · <a href="/wiki/n/fit-accuracy-knobs/">accuracy knobs</a></li></ul></details>
<div class="model-row"><span class="model-s">Units</span><span class="model-v">Air to vacuum; \(10^{-19}\) erg s\(^{-1}\) cm\(^{-2}\) \(\text{\AA}\)\(^{-1}\) to \(F_\nu\) cgs</span><span class="model-w"></span><span class="model-f"></span></div>
<div class="model-row"><span class="model-s">Resolution</span><span class="model-v">FITS <code>SPEC_RES</code> as FWHM resolving power; sampled \(\sigma_\star\) as line-of-sight broadening; CSP broadening 0</span><span class="model-w"></span><span class="model-f"></span></div>
<details class="model-row"><summary><span class="model-s">Emission-line mask</span><span class="model-v">± 1500 \(\mathrm{km\,s^{-1}}\) around [O II] 3726, 3729, H\(\beta\), [O III] 4959, 5007</span><span class="model-w">no nebular model</span><span class="model-f"></span></summary><ul><li><i>tested</i> adding [Ne III] 3869, H\(\epsilon\), H\(\delta\), H\(\gamma\): 181–488 pixels removed; age moves 13.7 half-widths on M4_108989 · <a href="/wiki/e/e-emission-mask/">emis_wide</a></li></ul></details>
<div class="model-row"><span class="model-s">Telluric mask</span><span class="model-v">7590–7660 \(\text{\AA}\) air, A band</span><span class="model-w"></span><span class="model-f"></span></div>
<details class="model-row"><summary><span class="model-s">Fitted pixels</span><span class="model-v">All valid pixels; no rest windows</span><span class="model-w"></span><span class="model-f"></span></summary><ul><li><i>tested</i> CN and C4668 windows masked: spectral \(\chi^2\) −14 median; \([\alpha/\mathrm{Fe}]\) moves 4.0 half-widths on M5_172669 · <a href="/wiki/e/e-cn-mask/">mask_cn</a></li><li><i>tested</i> absorption-feature pixels only: large real-target shifts · <a href="/wiki/e/e-absorption-masks/">absorption masks</a></li></ul></details>
<details class="model-row"><summary><span class="model-s">Photometry</span><span class="model-v">COSMOS2015 total flux, 12 bands u* to 4.5 µm</span><span class="model-w">aperture optical + total IRAC: SED too red</span><span class="model-f"></span></summary><ul><li><i>how</i> 3″ aperture flux × \(10^{-0.4\,c}\); \(c\) = per-object aperture-to-total offset + Galactic extinction + Laigle+2016 Table 3 zero point</li><li><i>how</i> offset on the ten optical and NIR bands only; IRAC already total; −0.16 to −0.60 mag on the six reference galaxies</li><li><i>tested</i> <code>cosmos_ap3</code>, 3″ apertures without the offset: <code>poly3_total</code> has the smallest photometric \(\chi^2\) in each target · <a href="/wiki/e/e-calibration-photometry/">photometry arms</a></li><li><i>tested</i> IRAC dropped: four of six barely move; M5_173928 jumps to another solution · <a href="/wiki/e/e-irac-removal/">no_irac</a></li><li><i>source</i> switch <code>CERIDWEN_PHOTOMETRY</code>, since 3 Sep 2026</li></ul></details>
<div class="model-row"><span class="model-s">Photometric errors</span><span class="model-v">5% of flux added in quadrature; all 12 bands fitted</span><span class="model-w"></span><span class="model-f"></span></div>
</dl>

## Stellar model, SFH and dust

<dl class="model-group">
<div class="model-row"><span class="model-s">Isochrones <span class="model-tag">inherited</span></span><span class="model-v">aMIST v2.5, \(\alpha\)-variable</span><span class="model-w"></span><span class="model-f"></span></div>
<div class="model-row"><span class="model-s">Spectral library <span class="model-tag">inherited</span></span><span class="model-v">C3K v2.3 high resolution, R ≈ 6000</span><span class="model-w"></span><span class="model-f"></span></div>
<div class="model-row"><span class="model-s">IMF <span class="model-tag">inherited</span></span><span class="model-v">Kroupa 2001</span><span class="model-w"></span><span class="model-f"></span></div>
<div class="model-row"><span class="model-s">Abundance scale <span class="model-tag">inherited</span></span><span class="model-v">Solar Z 0.0185; \([\mathrm{Fe}/\mathrm{H}]\) = grid Z + 1.7328</span><span class="model-w"></span><span class="model-f"></span></div>
<div class="model-row"><span class="model-s">Grid</span><span class="model-v"><code>amist_c3k_hr_krou_afe</code>: 13 \([\mathrm{Fe}/\mathrm{H}]\) × 5 \([\alpha/\mathrm{Fe}]\) × 107 age nodes</span><span class="model-w"></span><span class="model-f"></span></div>
<div class="model-row"><span class="model-s">\(\log M_\star\) formed</span><span class="model-v">Uniform(8, 13)</span><span class="model-w"></span><span class="model-f"></span></div>
<div class="model-row"><span class="model-s">\([\mathrm{Fe}/\mathrm{H}]\)</span><span class="model-v">Uniform(−2.5, 0.5)</span><span class="model-w">grid limits</span><span class="model-f"></span></div>
<details class="model-row"><summary><span class="model-s">\([\alpha/\mathrm{Fe}]\)</span><span class="model-v">Uniform(−0.2, 0.6)</span><span class="model-w">grid limits</span><span class="model-f"><b class="model-flag" title="Known problem">!</b></span></summary><ul><li><i>problem</i> within 0.03 of the −0.2 grid edge in 2 of 6 at order 10 (M4_108989 −0.183, M5_173928 −0.172) and at order 3 (M1_206545 −0.197, M4_108989 −0.186) · <a href="/wiki/n/calibration-order/">calibration order</a></li><li><i>problem</i> CN and C4668 residuals of −5 to −7.5 \(\sigma\) on the same two galaxies · <a href="/wiki/n/fit-accuracy-knobs/">accuracy knobs</a></li></ul></details>
<div class="model-row"><span class="model-s">Abundances over age <span class="model-tag">inherited</span></span><span class="model-v">\([\mathrm{Fe}/\mathrm{H}]\) and \([\alpha/\mathrm{Fe}]\) constant</span><span class="model-w"></span><span class="model-f"></span></div>
<div class="model-row"><span class="model-s">SFH nodes</span><span class="model-v">0, 0.03, 0.1, 0.3, 1, 3, 5 Gyr and the age of the Universe at z; step interpolation</span><span class="model-w"></span><span class="model-f"></span></div>
<details class="model-row"><summary><span class="model-s">SFH prior</span><span class="model-v">Student-t(0, 0.3 dex, df 2) on 7 log ratios</span><span class="model-w">Liu Hao, 6 Sep 2026</span><span class="model-f"></span></summary><ul><li><i>tested</i> Uniform(−3, 3): Student-t raises age in 5 of 6, widens every interval, \(\ln Z\) falls 0.7–6.8 · <a href="/wiki/e/e-sfh-prior/">sfh_cont</a></li><li><i>note</i> rising continuity prior raised by Jonah Powley · <a href="/wiki/n/meeting-2026-09-17-jonah-powley/">17 Sep 2026 meeting</a></li><li><i>papers</i> continuity, rising and other variants · <a href="/wiki/n/sfh-continuity-prior-variants/">SFH continuity prior and its variants</a></li></ul></details>
<details class="model-row"><summary><span class="model-s">Redshift</span><span class="model-v">Uniform(\(z_{\mathrm{cat}}\) − 0.1, \(z_{\mathrm{cat}}\) + 0.1)</span><span class="model-w">Liu Hao, 17 Sep 2026</span><span class="model-f"></span></summary><ul><li><i>how</i> spectrum read from the \(z_{\mathrm{cat}}\) prediction at stretched wavelengths; filter projection, emission-line mask and SFH age grid stay at \(z_{\mathrm{cat}}\); distance factor uses the sampled z · ceridwen <code>c540bc7</code></li><li><i>note</i> fixed at catalogue z until 17 Sep 2026; no fit under this prior yet</li><li><i>tested</i> Normal, 100 \(\mathrm{km\,s^{-1}}\): age shifts small in four targets · <a href="/wiki/e/e-redshift-dispersion/">zsig</a></li><li><i>speed</i> exact \(z\) lookup indices · baked runtime default <code>5f2c316</code> · <a href="/wiki/e/e-runtime-z-sigma-speed/">speed</a></li></ul></details>
<details class="model-row"><summary><span class="model-s">\(\sigma_\star\)</span><span class="model-v">Normal(DR2, error) clipped at ± 3 errors</span><span class="model-w">Liu Hao, 17 Sep 2026</span><span class="model-f"></span></summary><ul><li><i>note</i> fixed at DR2 unless <code>CERIDWEN_FREE_SIGMA=1</code> until 17 Sep 2026; switch removed</li><li><i>why</i> fit it as a broadening parameter · <a href="/wiki/n/meeting-2026-09-15-mj-park-sandro/">15 Sep 2026 meeting</a></li><li><i>tested</i> Normal(DR2, 0.2 DR2): M5_173928 reaches the upper bound · <a href="/wiki/e/e-redshift-dispersion/">zsig</a></li><li><i>speed</i> precomputed smoothing interpolation and instrument taper · baked runtime default <code>5f2c316</code> · <a href="/wiki/e/e-runtime-z-sigma-speed/">speed</a></li></ul></details>
<details class="model-row"><summary><span class="model-s">Dust law <span class="model-tag">inherited</span></span><span class="model-v">Kriek &amp; Conroy 2013, one diffuse screen; \(A_V = 1.086\,\tau\)</span><span class="model-w"></span><span class="model-f"></span></summary><ul><li><i>how</i> \(\tau_\lambda = \tau\,[k_{\mathrm{Calzetti}}(\lambda) + D(\lambda)]/4.05 \times (\lambda/5500\,\text{\AA})^{\delta}\)</li><li><i>how</i> bump at 2175 \(\text{\AA}\), width 350 \(\text{\AA}\), strength \(E_b = 0.85 - 1.9\,\delta\)</li><li><i>source</i> <code>sedpy_jax.attenuation_dust.kriek_conroy</code> through <code>DiffuseDust</code></li></ul></details>
<details class="model-row"><summary><span class="model-s">\(\tau_{\mathrm{dust}}\) at 5500 \(\text{\AA}\)</span><span class="model-v">Uniform(0, 1)</span><span class="model-w">Liu Hao, 17 Sep 2026</span><span class="model-f"></span></summary><ul><li><i>note</i> Uniform(0, 2) until 7 Sep 2026; Uniform(0, 0.2) from 7 to 17 Sep 2026 (c053f85); no reason recorded</li><li><i>todo</i> railing check under Uniform(0, 1) · <a href="/wiki/p/tau-dust-railing/">roadmap</a></li><li><i>tested</i> Uniform(0, 0.2): median 0.187–0.199 in 6 of 6 at orders 3 and 10; 5–95% within 0.14–0.20 at order 3 · <a href="/wiki/n/calibration-order/">calibration order</a></li><li><i>tested</i> Uniform(0, 2): medians 0.31–0.49 on the six reference galaxies; 187-galaxy median 0.45, 184 of 187 above 0.2 · <a href="/wiki/n/dr2-quiescent-sample/">DR2 sample</a></li><li><i>tested</i> ClippedNormal(0.3, 1.0) on [0, 4] against Uniform(0, 2): medians equal to two decimals · <a href="/wiki/e/e-dust-amount-prior/">tau_cn</a></li></ul></details>
<details class="model-row"><summary><span class="model-s">Dust slope \(\delta\)</span><span class="model-v">Uniform(−1.0, 0.4)</span><span class="model-w">Ceridwen documented default</span><span class="model-f"><b class="model-flag" title="Known problem">!</b></span></summary><ul><li><i>why</i> Liu Hao, 6 Sep 2026, after the stage-1 results · <a href="/wiki/n/fit-accuracy-knobs/">accuracy knobs</a></li><li><i>problem</i> median within 0.03 of the −1.0 bound in 4 of 6 at order 10; within 0.12 in 5 of 6 at order 3 · <a href="/wiki/n/calibration-order/">calibration order</a></li><li><i>tested</i> fixed −0.7: free slope lowers photometric \(\chi^2\) in 5 of 6; \(\ln Z\) +0.8 to +14.8 · <a href="/wiki/e/e-dust-slope/">dust_free</a></li><li><i>tested</i> Uniform(−2.0, 0.5): three galaxies follow the bound to −1.75…−1.94; \([\mathrm{Fe}/\mathrm{H}]\) up to +24 half-widths; dropped · <a href="/wiki/e/e-dust-slope/">dust_wide</a></li><li><i>papers</i> Tacchella+2022 (−1.0, 0.4), reason given for 0.4 only; Leja+2017 (−2.2, 0.4); Kriek &amp; Conroy 2013 measured −0.8 to 0.2</li></ul></details>
<details class="model-row"><summary><span class="model-s">Off <span class="model-tag">inherited</span></span><span class="model-v">Birth-cloud dust, dust emission, nebular emission, AGN, IGM</span><span class="model-w"></span><span class="model-f"></span></summary><ul><li><i>note</i> dust emission and AGN torus raised for the IRAC bands · <a href="/wiki/n/meeting-2026-09-17-jonah-powley/">17 Sep 2026 meeting</a></li></ul></details>
</dl>

## Calibration, noise and sampler

<dl class="model-group">
<details class="model-row"><summary><span class="model-s">Calibration polynomial</span><span class="model-v">Chebyshev order 10; Normal(0, 0.1); no constant; marginalised</span><span class="model-w">Liu Hao, 17 Sep 2026</span><span class="model-f"></span></summary><ul><li><i>why</i> “Order 10 has speed-ups implemented and should be the default for future fits.” · <a href="/wiki/e/e-calibration-order/">orders 3, 5, 10</a></li><li><i>note</i> order 3 from 6 Sep to 17 Sep 2026; the accuracy-knob arms cited on this page ran at order 3 · <a href="/wiki/n/fit-accuracy-knobs/">accuracy knobs</a></li><li><i>tested</i> order 0 and order 3 on 3″ apertures: <code>poly3_total</code> has the smallest photometric \(\chi^2\) in each target · <a href="/wiki/e/e-calibration-photometry/">photometry arms</a></li><li><i>tested</i> orders 5 and 10: \(\ln Z\) +20 to +555 at order 10; \(t_{50}\) half-width 0.00–0.01 Gyr on two galaxies · <a href="/wiki/e/e-calibration-order/">orders 3, 5, 10</a></li><li><i>rule</i> order ≈ range / 100 \(\text{\AA}\); shortest mode ≥ 100 \(\text{\AA}\) allows order 24 · <a href="/wiki/n/meeting-2026-09-15-mj-park-sandro/">15 Sep 2026 meeting</a></li></ul></details>
<div class="model-row"><span class="model-s">Spectrum scaling</span><span class="model-v">Normal(1, 0.3) clipped to [0.2, 3]</span><span class="model-w"></span><span class="model-f"></span></div>
<details class="model-row"><summary><span class="model-s">\(f_{\mathrm{calib}}\)</span><span class="model-v">log-uniform 1–10%; \(\sigma_{\mathrm{eff}}^2 = \sigma_{\mathrm{obs}}^2 + (f_{\mathrm{calib}}\,\lvert\mu\rvert)^2\)</span><span class="model-w"></span><span class="model-f"><b class="model-flag" title="Known problem">!</b></span></summary><ul><li><i>problem</i> “90% hits upper bound” · <a href="/wiki/n/meeting-2026-09-15-mj-park-sandro/">15 Sep 2026 meeting</a></li><li><i>problem</i> M12_98104 at 9.98% at orders 3 and 10; M5_173928 9.18% at order 3, 7.01% at order 10 · <a href="/wiki/n/calibration-order/">calibration order</a></li><li><i>tested</i> ceiling 20%: M12_98104 9.98 → 14.59%, \(\ln Z\) +86.6; M5_173928 stays at 8.99% · <a href="/wiki/e/e-noise-floor/">floor20</a></li></ul></details>
<div class="model-row"><span class="model-s">Likelihood</span><span class="model-v">Diagonal Gaussian, photometry and spectrum; spectrum with \(f_{\mathrm{calib}}\) and the marginalised polynomial</span><span class="model-w"></span><span class="model-f"></span></div>
<details class="model-row"><summary><span class="model-s">Nested sampler</span><span class="model-v">BlackJAX NSS: 500 live, 65 inner steps, 100 deleted, \(\ln Z\) tolerance −5</span><span class="model-w"></span><span class="model-f"></span></summary><ul><li><i>why</i> 65 inner steps kept, not the 5 n rule's 70, so only priors differ between arms · <a href="/wiki/n/fit-accuracy-knobs/">accuracy knobs</a></li><li><i>note</i> 16 sampled parameters since 17 Sep 2026; the 5 n rule gives 80</li><li><i>tested</i> seed repeats: age moves up to 1.20 half-widths, \(\ln Z\) up to 2.0 · <a href="/wiki/e/e-seed-repeatability/">seed_rep</a></li></ul></details>
<div class="model-row"><span class="model-s">Seeds</span><span class="model-v">Sampler 20260812; posterior draws 20260813</span><span class="model-w"></span><span class="model-f"></span></div>
<div class="model-row"><span class="model-s">Pass rule</span><span class="model-v">Finite \(\ln Z\) and error; posterior-weight ESS ≥ 200</span><span class="model-w"></span><span class="model-f"></span></div>
<div class="model-row"><span class="model-s">Posterior draws</span><span class="model-v">2000 equal-weight; 400 evenly spaced rows for derived quantities</span><span class="model-w"></span><span class="model-f"></span></div>
</dl>

## Derived quantities and cosmology

<dl class="model-group">
<div class="model-row"><span class="model-s">Bin masses</span><span class="model-v">Trapezoidal integral of the SFR over each of the 7 intervals</span><span class="model-w"></span><span class="model-f"></span></div>
<div class="model-row"><span class="model-s">Mass-weighted age</span><span class="model-v">Bin masses weighted by interval midpoints</span><span class="model-w"></span><span class="model-f"></span></div>
<div class="model-row"><span class="model-s">\(t_{20}\), \(t_{50}\), \(t_{80}\)</span><span class="model-v">Lookback time younger than which 20, 50 or 80% of the formed mass was formed; \(\Delta t = t_{80} - t_{20}\)</span><span class="model-w"></span><span class="model-f"></span></div>
<div class="model-row"><span class="model-s">\([\mathrm{Fe}/\mathrm{H}]\)</span><span class="model-v">Grid Z + 1.7328283</span><span class="model-w"></span><span class="model-f"></span></div>
<div class="model-row"><span class="model-s">\(f_{\mathrm{calib}}\)</span><span class="model-v">Reported in percent</span><span class="model-w"></span><span class="model-f"></span></div>
<div class="model-row"><span class="model-s">Summaries</span><span class="model-v">Percentiles 16, 50, 84</span><span class="model-w"></span><span class="model-f"></span></div>
<div class="model-row"><span class="model-s">Cosmology <span class="model-tag">inherited</span></span><span class="model-v">Planck 2018, <code>ceridwen.cosmology.age_gyr</code></span><span class="model-w"></span><span class="model-f"></span></div>
</dl>


## Literature

<figure>
<img src="figures/model/literature-vs-ceridwen.png" alt="One row per literature paper for age, metallicity and alpha enhancement, with the Ceridwen DR2 sample median and 16-84 spread as the blue top row">
<figcaption>Age, metallicity and alpha-enhancement panels: redshift-ordered literature-paper rows; grey bars: quoted ranges/\(\pm\)1\(\sigma\); blue top row: 187-galaxy Ceridwen DR2 median (also vertical line), 16–84 percentile across-galaxy spread; circles: \([\mathrm{Z}/\mathrm{H}]\)/\([\alpha/\mathrm{Fe}]\); squares: \([\mathrm{Fe}/\mathrm{H}]\)/\([\mathrm{Mg}/\mathrm{Fe}]\); Ceridwen \([\mathrm{Fe}/\mathrm{H}]\) = Z + 1.7328 (grid’s built-in solar reference).</figcaption>
</figure>

### Values at z ~ 0.7

| Quantity | DR2 median (187) | Literature at z~0.7 |
| --- | --- | --- |
| \(\log M_\star\) formed | 11.34 | Kaushal+2024 QG median 11.2; Borghi+2022a > 10.4; Cappellari 2023 > 10.5 |
| \([\mathrm{Fe}/\mathrm{H}]\) | −0.18 | Borghi+2022a \([\mathrm{Z}/\mathrm{H}]\) 0.08 \(\pm\) 0.18; Beverage+2021 ~0.2 dex below z~0; Cheng+2025 higher at redder U−V; Gallazzi+2026 no QG evolution to SDSS |
| \([\alpha/\mathrm{Fe}]\) | −0.05 | Bevacqua+2023 +0.24 \(\pm\) 0.01, 91% supersolar; Borghi+2022a +0.13 \(\pm\) 0.11; Beverage+2023 \([\mathrm{Mg}/\mathrm{Fe}]\) ~0.2–0.3 |
| SFH | \(t_{50}\) 5.03 Gyr, \(t_{80}-t_{20}\) 2.55 Gyr | Kaushal+2024 \(t_{50}\), \(t_{90}\) mass-independent; Nersesian+2025 \(\tau_q\) 1.23 Gyr |
| \(\tau_{\mathrm{dust}}\) at 5500 \(\text{\AA}\) | 0.45 under Uniform(0, 2); 184 of 187 above 0.2 | Jonah Powley's Prospector fit: about 0.77 |
| \(\sigma_\star\) | 204 \(\mathrm{km\,s^{-1}}\) | DR3 16/50/84: 127/166/207 \(\mathrm{km\,s^{-1}}\); Kaushal+2024 QG ~200; Cappellari 2023 quenched above 200; Gallazzi+2026 age transition at \(\log\sigma\) 2.3 |
| Age, mass-weighted | 4.81 Gyr | Borghi+2022a 2–4 Gyr SSP-equivalent, Ceridwen +1.29 Gyr for the 68-galaxy overlap; Beverage+2023 rises with \(\sigma\); Nersesian+2025 QG 1.1 Gyr older than SFG; Barone+2022 no age–\(\Sigma\) relation |

<details>
<summary>Prospector reference: Jonah Powley</summary>

| Parameter | His prior | Ceridwen production |
| --- | --- | --- |
| Dust law | Kriek & Conroy (`dust_type` 4) | Kriek–Conroy diffuse law |
| Dust index | Free, TopHat(−1.2, 0.4) | Uniform(−1.0, 0.4) |
| \(\tau_{\mathrm{dust},2}\) | Free, ClippedNormal(0.3, 1.0) on [0, 4] | Uniform(0, 1); Ceridwen's documented default matches his prior |
| Birth-cloud dust | `dust1` derived by `convert_to_dust1` (absent from the excerpt); `dust1_fraction` free, ClippedNormal(1.0, 0.3) on [0, 2] | Off |
| Dust emission (`add_duste`) | \(U_{\mathrm{min}}\) ClippedNormal(1, 10) on [0.1, 25]; \(q_{\mathrm{PAH}}\) ClippedNormal(2, 2) on [0, 7]; \(\log_{10}\gamma\) ClippedNormal(−2, 1) on [−4, 0], \(\gamma\) derived | Off |
| AGN torus (`add_agn`) | \(\log_{10} f_{\mathrm{AGN}}\) TopHat(−5, \(\log_{10} 3\)); \(\log_{10}\tau_{\mathrm{AGN}}\) TopHat(\(\log_{10} 5\), \(\log_{10} 150\)); linear values derived | Not modelled |

<details>
<summary>His code, as sent</summary>

```python
# Dust attenuation
    model_params["dust_type"]["init"] = 4
    model_params["dust_index"] = dict(N=1, isfree=True, init=0.0, prior=priors.TopHat(mini=-1.2, maxi=0.4))
    model_params["dust2"]["prior"] = priors.ClippedNormal(mean=0.3, sigma=1.0, mini=0.0, maxi=4.0)
    model_params["dust2"]["isfree"] = True
    model_params["dust1"] = dict(N=1, isfree=False, init=0, prior=None, depends_on=convert_to_dust1)
    model_params["dust1_fraction"] = dict(N=1, isfree=True, init=1.0, prior=priors.ClippedNormal(mean=1.0, sigma=0.3, mini=0.0, maxi=2.0))

    # Dust emission
    if add_duste:
        model_params["add_dust_emission"] = dict(N=1, isfree=False, init=True)
        model_params["duste_umin"] = dict(N=1, isfree=True, init=1.0, prior=priors.ClippedNormal(mean=1.0, sigma=10.0, mini=0.1, maxi=25.0))
        model_params["duste_qpah"] = dict(N=1, isfree=True, init=2.0, prior=priors.ClippedNormal(mean=2.0, sigma=2.0, mini=0.0, maxi=7.0))
        model_params["log_duste_gamma"] = dict(N=1, isfree=True, init=-2.0, prior=priors.ClippedNormal(mean=-2.0, sigma=1.0, mini=-4.0, maxi=0.0))
        model_params["duste_gamma"] = dict(N=1, isfree=False, init=0.01, depends_on=get_duste_gamma_from_log)

    # AGN torus emission
    if add_agn:
        model_params["add_agn"] = dict(N=1, isfree=False, init=True)
        model_params["log_fagn"] = dict(N=1, isfree=True, init=-2.0, prior=priors.TopHat(mini=-5.0, maxi=np.log10(3.0)))
        model_params["fagn"] = dict(N=1, isfree=False, init=0.01, depends_on=get_fagn_from_log)
        model_params["log_agn_tau"] = dict(N=1, isfree=True, init=1.0, prior=priors.TopHat(mini=np.log10(5.0), maxi=np.log10(150.0)))
        model_params["agn_tau"] = dict(N=1, isfree=False, init=1.0, depends_on=get_agn_tau_from_log)

def get_fagn_from_log(log_fagn=None, **extras):
    """Convert log10(fagn) back to linear fagn."""
    return 10**log_fagn


def get_agn_tau_from_log(log_agn_tau=None, **extras):
    """Convert log10(tau_agn) back to linear tau_agn."""
    return 10**log_agn_tau


def get_duste_gamma_from_log(log_duste_gamma=None, **extras):
    """Convert log10(duste_gamma) back to linear duste_gamma."""
    return 10**log_duste_gamma
```

</details>

</details>

### Other redshifts

| Reference | Sample | Result |
| --- | --- | --- |
| Gallazzi+2005 | SDSS | mass–metallicity and age–mass relations; transition 3e9–3e10 \(M_\odot\) |
| Thomas+2005, 2010 | local early types | \([\alpha/\mathrm{Fe}]\)–\(\sigma\) slope ~0.2; environment-independent |
| Conroy+2014 | SDSS stacks, \(\sigma\) 90–300 \(\mathrm{km\,s^{-1}}\) | \([\mathrm{Fe}/\mathrm{H}]\) varies < 0.1 dex; \([\mathrm{Mg}/\mathrm{Fe}]\) 0.0→0.25; ages 6–12 Gyr |
| McDermid+2015 | ATLAS3D | compact galaxies older, metal-richer, more \(\alpha\)-enhanced |
| Gallazzi+2014 | z~0.7, E-CDFS | −0.28 dex age, −0.13 dex Z versus SDSS; QGs need no further enrichment |
| Choi+2014 | SDSS + AGES, \(0.1<z<0.7\) | stacked abundances across redshift |
| Kriek+2019 | z~1.4 | \([\mathrm{Fe}/\mathrm{H}]\) −0.2 dex; \([\mathrm{Mg}/\mathrm{Fe}]\) up to 0.44 |
| Carnall+2022 | \(1.0<z<1.3\) | \([\mathrm{Z}/\mathrm{H}]\) −0.13 \(\pm\) 0.08 (Bagpipes), 0.04 \(\pm\) 0.14 (alf); \([\mathrm{Fe}/\mathrm{H}]\) −0.18 \(\pm\) 0.08 |
| Estrada-Carpenter+2019 | \(1<z<1.8\) | roughly solar metallicity |
| Beverage+2024 | z 1.4 / 2.1 | \([\mathrm{Fe}/\mathrm{H}]\) −0.2 / −0.3; \([\mathrm{Mg}/\mathrm{Fe}]\) 0.3 / 0.5 |
| Reviews | Renzini 2006, Conroy 2013, Cappellari 2016 | ARA&A |

<details>
<summary>References</summary>

- Barone+2022, [arXiv:2107.01054](https://arxiv.org/abs/2107.01054): LEGA-C + SAMI, z 0.60–0.76, indices.
- Bevacqua+2023, [arXiv:2308.03441](https://arxiv.org/abs/2308.03441): 183 galaxies, z 0.60–0.75, Mg b + Fe4383.
- Bevacqua+2024, [arXiv:2407.12704](https://arxiv.org/abs/2407.12704): 637 galaxies, z 0.6–1.0, full spectrum, mass-weighted.
- Beverage+2021, [arXiv:2105.12750](https://arxiv.org/abs/2105.12750): 65 galaxies, z 0.59–0.75, alf.
- Beverage+2023, [arXiv:2303.03412](https://arxiv.org/abs/2303.03412): 135 galaxies, z ~0.7, alf, \(\sigma\) stacks.
- Beverage+2024, [arXiv:2312.05307](https://arxiv.org/abs/2312.05307): z 1.4 and 2.1.
- Borghi+2022a, [arXiv:2106.14894](https://arxiv.org/abs/2106.14894): 140 galaxies, z ~0.7, Lick indices, SSP.
- Cappellari 2016, [arXiv:1602.04267](https://arxiv.org/abs/1602.04267): ARA&A review.
- Cappellari 2023, [arXiv:2208.14974](https://arxiv.org/abs/2208.14974): 3200 galaxies, z 0.6–1.0, pPXF + 28 bands.
- Carnall+2022, [arXiv:2108.13430](https://arxiv.org/abs/2108.13430): z 1.0–1.3.
- Cheng+2024, [arXiv:2407.10974](https://arxiv.org/abs/2407.10974): 456 galaxies, z 0.6–1.0, alf, resolved.
- Cheng+2025, [arXiv:2505.08858](https://arxiv.org/abs/2505.08858): ~700 galaxies, z 0.6–1.0, alf.
- Choi+2014, [arXiv:1403.4932](https://arxiv.org/abs/1403.4932): SDSS + AGES, z 0.1–0.7.
- Conroy 2013, [arXiv:1301.7095](https://arxiv.org/abs/1301.7095): ARA&A review.
- Conroy+2014, [arXiv:1303.6629](https://arxiv.org/abs/1303.6629): SDSS stacks.
- Estrada-Carpenter+2019, [arXiv:1810.02824](https://arxiv.org/abs/1810.02824): z 1–1.8.
- Gallazzi+2005, [arXiv:astro-ph/0506539](https://arxiv.org/abs/astro-ph/0506539): SDSS.
- Gallazzi+2014, [arXiv:1404.5624](https://arxiv.org/abs/1404.5624): z ~0.7, E-CDFS.
- Gallazzi+2026 I, [arXiv:2512.07952](https://arxiv.org/abs/2512.07952) and II, [arXiv:2511.11805](https://arxiv.org/abs/2511.11805): 552 galaxies, z 0.6–0.77, indices + rizYJ.
- Kaushal+2024, [arXiv:2307.03725](https://arxiv.org/abs/2307.03725): 1244 galaxies, z 0.6–1.0, Bagpipes + Prospector.
- Kriek+2019, [arXiv:1907.04327](https://arxiv.org/abs/1907.04327): z ~1.4.
- Laigle+2016, [arXiv:1604.02350](https://arxiv.org/abs/1604.02350): COSMOS2015 catalogue.
- McDermid+2015, [arXiv:1501.03723](https://arxiv.org/abs/1501.03723): ATLAS3D.
- Muzzin+2013, [arXiv:1303.4409](https://arxiv.org/abs/1303.4409): UVJ selection.
- Nersesian+2025, [arXiv:2502.03021](https://arxiv.org/abs/2502.03021) and 2026, [arXiv:2512.10383](https://arxiv.org/abs/2512.10383): 2908 galaxies, z 0.6–1.0, Prospector.
- Renzini 2006, [arXiv:astro-ph/0603479](https://arxiv.org/abs/astro-ph/0603479): ARA&A review.
- Straatman+2018, [arXiv:1809.08236](https://arxiv.org/abs/1809.08236): LEGA-C DR2, VizieR J/ApJS/239/27.
- Thomas+2005, [arXiv:astro-ph/0410209](https://arxiv.org/abs/astro-ph/0410209) and 2010, [arXiv:0912.0259](https://arxiv.org/abs/0912.0259): local early types.
- van der Wel+2021, [arXiv:2108.00744](https://arxiv.org/abs/2108.00744): LEGA-C DR3, 4081 spectra, 3741 galaxies, VIMOS R ~ 2500, 6300–8800 \(\text{\AA}\), UVJ quiescent 1208.

Sources: `notebooks/ceridwen_integrated_photometry_spectra.ipynb` cells 2 (`SETTINGS`, `PRIORS`), 4, 6, 8, 10, 12 and 20 (zero-based); `scripts/build_dr2_quiescent_summary.py`; `ceridwen/ceridwen/likelihood/noise_model.py`; `ceridwen/scripts_afe/build_afe_hr_grid.py`; `results/dr2-quiescent-new-defaults-summary.csv`; the 187-galaxy prior from `results/dr2-quiescent-new-defaults/123161-M4_123161/M4_123161_executed.ipynb`. Figures in [DR2 quiescent sample](/wiki/n/dr2-quiescent-sample/); [literature comparison](/wiki/roadmap/#literature-comparison); earlier reference: [Current default model](/wiki/n/default-fit-parameters/); page contract: `wiki/research/model-page-spec.md`.

</details>
