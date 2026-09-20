---
title: SFH continuity prior and its variants
date: 2026-09-21
section: Literature
theme: Background reading
tags: [sfh, priors, continuity, rising-prior, prospector, literature]
job:
---

[Question record](/wiki/q/q-rising-continuity-prior/) · [Meeting note](/wiki/n/meeting-2026-09-17-jonah-powley/)

Jonah Powley’s rising continuity prior most likely comes from Turner et al. 2025: high confidence, not confirmed by him.

| Variant | Paper | Centre of \(x_n\) | \(\sigma\), \(\nu\) | Reported effect on age and mass |
|---|---|---|---|---|
| Flat continuity | Leja 2019 | \(0\) | \(0.3\), \(2\) | Across priors: age up to 0.3–0.5 dex, mass ~0.1 dex |
| Dirichlet | Leja 2019 | Constant-SFR expectation | — | Included in Leja’s comparison |
| Bursty continuity | Tacchella 2022 | \(0\) | \(1.0\), \(2\) | Lower mass for low-mass galaxies |
| Constant rising tilt | de Graaff 2024 | \(+0.3\) | \(0.3\), \(2\) | ~550 Myr retained, mass robust |
| Halo-accretion tilt | Turner 2025 | \(\mu_n(z)\) | \(0.3\), \(2\) | Age 1.6 → 1.4 Gyr |
| Cosmic-SFRD tilt | Wang 2023 | Cosmic SFRD with mass shift | Prospector-alpha unchanged | Smaller mean age and mass biases |
| Early formation | Suess 2022a, 2022b | Quiescent UniverseMachine SFH | \(0.3\), \(1\) | Higher mass, early formation |

<details>
<summary>Convention</summary>

\[
x_n=\log_{10}\!\left(\frac{\mathrm{SFR}_n}{\mathrm{SFR}_{n+1}}\right),
\qquad n=1,\ldots,N-1.
\]

- \(N\): number of constant-SFR bins.
- \(n\): bin index. Bin \(1\): most recent lookback-time bin.
- \(\mathrm{SFR}_n\): star-formation rate in bin \(n\).
- \(x_n\): adjacent-bin logarithmic SFR ratio.
- \(x_n>0\): higher SFR in the younger bin, rising with cosmic time.
- \(N\)-th free parameter: log total mass formed.
- \(\log_{10}\): base-10 logarithm. \(\ln\): natural logarithm.
- SFH: star-formation history. SFRD: star-formation-rate density. sSFR: specific SFR.
- \(z\): redshift. \(M_\star\): stellar mass. \(M_\odot\): solar mass.
- Prospector: `prospect/models/transforms.py:196`, `logsfr_ratios_to_masses` docstring.
- Ceridwen: `ceridwen/ceridwen/model/transforms.py:79`, `logsfr_ratios_to_sfh` docstring.

</details>

<details>
<summary>Continuity prior</summary>

- Leja 2019, Eq. 4, PDF as printed:

\[
\mathrm{PDF}(x,\nu)=
\frac{\Gamma((\nu+1)/2)}
{\sqrt{\nu\pi}\,\Gamma(\nu/2)}
\left(1+\frac{(x/\sigma)^2}{\nu}\right)^{-(\nu+1)/2}.
\]

- \(\mathrm{PDF}\): probability-density function. \(x\): one adjacent-bin log SFR ratio.
- \(\Gamma\): gamma function. \(\pi\): circle constant.
- \(\sigma=0.3\) dex: scale. \(\nu=2\): degrees of freedom. Mean \(0\).
- Constant \(\mathrm{SFR}(t)\) expectation, with \(t\) denoting time.
- Symmetric prior in age and sSFR.
- Appendix B: \(\nu=2\) “similar to, but slightly wider” than the Illustris log-ratio distribution.
- Illustris ratios: \(\log(\mathrm{SFR}(t)/\mathrm{SFR}(t+dt))\), with \(dt\) the time separation.
- Non-zero mean permitted to mimic cosmic SFRD.
- Illustris distribution centre changes with \(dt\), reflecting higher earlier SFRs.
- Centre shift omitted “to keep the findings general”.
- Prospector `prospect/models/templates.py:98-123`, `adjust_continuity_agebins`: `priors.StudentT(mean=0, scale=0.3, df=2)`.
- `prospect/models/templates.py:539-560`: `TemplateLibrary["continuity_sfh"]`.
- `prospect/models/priors.py:560`: `priors.StudentT`.
- Ceridwen project prior: Student-t\((0,0.3,\mathrm{df}\ 2)\), \(7\) ratios, \(8\) bins.

</details>

<details>
<summary>Rising variants</summary>

- **de Graaff: constant tilt**
- Methods, “Star formation history testing”: every ratio mean shifted from \(0.0\) to \(0.3\).
- \(\sigma=0.3\), \(\nu=2\), \(14\) bins.
- Prior centre: each younger bin has \(2\times\) the next older bin’s SFR.
- Cited motivation: Papovich et al. 2011, Behroozi et al. 2019.
- No released code for this variant. Prospector argument change: `mean=0.3` in `priors.StudentT`.

- **Turner: halo-accretion tilt**
- Section 3.3, Eqs. 3–4. Dekel et al. 2013 accretion relation, Einstein–de Sitter regime:

\[
\dot M_{\mathrm h}\propto
M_{\mathrm h,0}\exp[-\alpha(z-z_0)](1+z)^\mu,
\qquad
\alpha=\frac45,\quad \mu=\frac52.
\]

- \(\dot M_{\mathrm h}\): halo mass-accretion rate.
- \(M_{\mathrm h,0}\): halo mass at reference redshift \(z_0\).
- \(\alpha\): exponential coefficient. \(\mu\): redshift-power exponent.
- \(\exp\): exponential function. \(\propto\): proportionality.

\[
\mathrm{SFR}(z)\propto
\exp\!\left[-\frac45(z-z_{\mathrm{obs}})\right](1+z)^{5/2}.
\]

\[
\mu_n=
\log_{10}\!\left(\frac{\mathrm{SFR}(z_n)}
{\mathrm{SFR}(z_{n+1})}\right)
=
-\frac{4(z_n-z_{n+1})}{5\ln 10}
+\frac52\log_{10}\!\left(\frac{1+z_n}{1+z_{n+1}}\right).
\]

- \(z_{\mathrm{obs}}\): observation redshift. \(z_n\): mean redshift of bin \(n\).
- \(\mu_n\): Student-t centre for ratio \(x_n\), distinct from exponent \(\mu\).
- \(\sigma=0.3\), \(\nu=2\) unchanged.
- \(z_{\mathrm{obs}}=3.2\): SFR at \(z=10\) lower by factor \(\approx20\), evaluated ratio \(20.8\).

\[
\frac{d\ln\mathrm{SFR}}{dz}
=-\frac45+\frac{5/2}{1+z}=0
\quad\text{at}\quad z=2.125.
\]

- Centre rising with cosmic time for \(z>2.125\), falling for \(z<2.125\).
- At \(z_{\mathrm{obs}}\approx0.7\): centre peaks at \(z=2.125\).
- Turner’s distinctions: de Graaff’s fixed adjacent-bin increase, Wang’s cosmic-SFRD prior.
- Paper: no repository named.
- Same equation: `jakobhelton/jwst_program_id_08544`, `PID08544_Prospector_helper.py:1062-1105`, `adjust_agebins`, `sfh_type='Rising'`.
- Lines `1084-1085`:

```python
sfr_z = np.exp(-alpha*(zbins - zred))*np.power(1.0 + zbins, 2.5)
baseline_sfr_ratios = np.log10(sfr_z[0:-1]/sfr_z[1::])
```

- `alpha=0.8`, `zred`: observation redshift.
- `zbins`: redshifts at bin mean lookback times.
- Function defaults: scale \(1.0\), not \(0.3\), and `df=2`.

- **Wang: cosmic-SFRD tilt**
- Eqs. 3–4: bin expectations matched to Behroozi et al. 2019 cosmic SFRD.
- Student-t about each mean unchanged from Prospector-alpha.
- Rising at early times, falling at late times.
- Mass dependence:

\[
\log(t_{\mathrm{start}}/\mathrm{Gyr})
=
\log(t_{\mathrm{univ}}(z)/\mathrm{Gyr})+\delta_m,
\]

\[
\delta_m=
\begin{cases}
-0.6, & \log M<9,\\
\frac13\log M-3.6, & 9\leq\log M\leq12,\\
0.4, & \log M>12.
\end{cases}
\]

- \(t_{\mathrm{start}}\): mass-shifted start-time parameter.
- \(t_{\mathrm{univ}}(z)\): universe age at redshift \(z\).
- \(\log M\): logarithmic stellar mass in solar units. \(\delta_m\): logarithmic time shift.
- Higher-mass galaxies: earlier formation.
- Paper: \(-0.6\) to \(0.4\). Released code: \(-0.2\) to \(0.8\).
- Prospector `prospect/models/priors_beta.py:1537`: `delta_t_dex(m, mlims=[9, 12], dlims=[-0.2, 0.8])`.
- `prospect/models/priors_beta.py:1551`: `expe_logsfr_ratios`.
- `prospect/models/priors_beta.py:793`: `DymSFH`.
- Ratio draws: `FastTruncatedEvenStudentTFreeDeg2`.

</details>

<details>
<summary>Dirichlet, bursty and early-formation variants</summary>

- **Dirichlet**
- Leja 2019, Section II.2.2, Eq. 3. Introduced in Leja et al. 2017.
- \(f_n\) below: fractions called \(x_n\) in that formulation, distinct from log SFR ratios.

\[
(f_1,\ldots,f_N)\sim
\operatorname{Dirichlet}(\alpha_D,\ldots,\alpha_D),
\qquad
0<f_n<1,\qquad \sum_{n=1}^{N}f_n=1.
\]

\[
m_n=\frac{f_n t_n}{\sum_{j=1}^{N}f_j t_j}.
\]

- \(f_n\): SFR fraction. \(m_n\): formed-mass fraction.
- \(t_n\): bin width. \(j\): summation index. \(\alpha_D\): symmetric concentration.
- Tested \(\alpha_D\): \(0.2\) and \(1\).
- \(\alpha_D<1\): weight concentrated in one bin, bursty.
- \(\alpha_D\geq1\): more evenly distributed fractions.
- Constant-SFR expectation. No adjacent-bin continuity.
- `prospect/models/templates.py:67-93`: `adjust_dirichlet_agebins`, Beta priors on `z_fraction`.
- `prospect/models/templates.py:659`: `dirichlet_sfh` template.
- `prospect/models/transforms.py:402`: `zfrac_to_masses`.

- **Bursty continuity**
- Tacchella 2022, Section III.2:

\[
x_n\sim\operatorname{StudentT}
(\mathrm{mean}=0,\ \mathrm{scale}=1.0,\ \mathrm{df}=2).
\]

- Same Student-t family. Scale \(1.0\) instead of \(0.3\).
- No separate class. `priors.StudentT` with `scale=1.0`.

- **Early formation**
- Suess 2022a, 2022b:

\[
x_n\sim\operatorname{StudentT}
(\mathrm{centre}=\mu_n^{\mathrm{UM}},\
\mathrm{scale}=0.3,\
\mathrm{df}=1),
\qquad
\mu_n^{\mathrm{UM}}=
\log_{10}\!\left(
\frac{\mathrm{SFR}^{\mathrm{UM}}_n}
{\mathrm{SFR}^{\mathrm{UM}}_{n+1}}
\right).
\]

- \(\mathrm{SFR}^{\mathrm{UM}}_n\): UniverseMachine SFR in bin \(n\).
- \(\mu_n^{\mathrm{UM}}\): corresponding log-ratio centre.
- UniverseMachine: Behroozi et al. 2019, quiescent \(M_\star=10^{11}\,M_\odot\) galaxy at target redshift.
- Width \(0.3\) dex, \(\nu=1\), not \(2\).
- \(9\) bins: \(3\) fixed old, \(5\) flexible equal-mass bins over the last \(2\) Gyr.
- Final bin: free length.
- Bulk of star formation early, lower SFR at observation.
- More allowed early mass, relatively high stellar mass.
- Low recent-burst mass fractions, saturating near \(60\%\).
- `prospect/models/templates.py:607-652`: `continuity_psb_sfh`.
- Template defaults: StudentT mean \(0\), scale \(0.3\), `df=1`. UniverseMachine centres supplied by the user.
- `prospect/models/transforms.py:284`: `logsfr_ratios_to_masses_psb`.
- `prospect/models/transforms.py:323`: `psb_logsfr_ratios_to_agebins`.

</details>

<details>
<summary>Reported effects on age and mass</summary>

- **Leja 2019:** mock photometry, S/N \(25\), logM / Dirichlet / continuity comparison.
- Mass variation \(\sim0.1\) dex. Age and SFR posterior medians: differences up to \(0.3\)–\(0.5\) dex.
- Real galaxies, continuity versus logM: age scatter \(0.25\) dex.
- Turner 2025 citing Leja 2019b: flat continuity favours median stellar age half the universe age.

- **Tacchella 2022:** \(z=9\)–\(11\), masses and SFRs within factor \(3\) across four priors.
- Bayes factors near \(1\). Bursty relative to continuity: \(0.7^{+0.7}_{-0.1}\).
- Low-mass galaxies: lower \(M_\star\), higher SFR with bursty continuity.

- **de Graaff:** RUBIES-EGS-QG-1, \(z=4.9\).
- Formation time \(t_{\mathrm{form}}\): “largely insensitive”. Fitted age still \(\sim550\) Myr.
- Slight increase in SFR and formation time. Stellar mass robust to SFH prior choice.

- **Turner 2025:** ZF-UDS-7329, \(z=3.2\), C3K.
- Median age: \(1.6\) Gyr flat → \(1.4\) Gyr rising, \(\sim200\) Myr younger.
- Formation redshift: \(z\approx11\) → \(z\approx8\).
- Mass-weighted ages across priors: \(1.3\)–\(1.8\) Gyr.
- Other parameters consistent within \(\sim1\sigma\), with \(\sigma\) denoting uncertainty here.
- Rising solution: younger, dustier.
- Reduced chi-squared: \(0.37\) flat, \(0.42\) rising.
- SFR at \(z=10\)–\(20\): \(\sim600\,M_\odot/\mathrm{yr}\) flat, \(\sim40\,M_\odot/\mathrm{yr}\) rising.
- Appendix D, single stellar population (SSP) mocks:
- \(1.5\) Gyr SSP: flat overestimate \(\sim250\) Myr, rising underestimate \(\sim100\) Myr.
- \(1.9\) Gyr SSP: flat recovery, rising underestimate \(\sim500\) Myr.
- Rising prior: forced age \(\lesssim1.4\) Gyr.
- Section 5.4: \(1.0\) Gyr population with \([\alpha/\mathrm{Fe}]=0.4\) can resemble a \(1.5\) Gyr solar-scaled population.

- **Wang 2023:** mock JWST photometry.
- Smaller mean biases in mass, mass-weighted age and SFR than uniform priors.
- Scatter unchanged. Uniform priors: age–mass–redshift degeneracy.

- **Suess 2022a, 2022b:** relatively high stellar mass, recent-burst fractions saturating near \(60\%\).
- 2022b mocks, non-parametric models: mass offsets \(<0.02\) dex, scatter \(\lesssim0.1\) dex.

</details>

<details>
<summary>Name conflicts</summary>

- “Rising prior”, de Graaff: constant \(+0.3\) dex per ratio.
- “Rising prior”, Turner: redshift-dependent halo-accretion centre.
- “Rising prior”, Wang: cosmic-SFRD centre with mass shift, rising only at early times.
- Leja 2019: logM prior also called rising by construction.
- “Continuity”: \(\nu=2\) in Leja, Tacchella, de Graaff and Turner.
- Suess and `continuity_psb_sfh`: \(\nu=1\).
- Meeting note: \(T(\mu_{\mathrm{SFH}},\sigma,3)\), with \(\mu_{\mathrm{SFH}}\) the centre and \(3\) degrees of freedom.
- Papers above: Student-t degrees of freedom \(2\) or \(1\).

</details>

<details>
<summary>Source of Jonah Powley's prior</summary>

- Most likely Turner et al. 2025. Confidence: high, not confirmed by him.
- Turner’s exact terms: “rising continuity prior”, “flat continuity prior”.
- Powley’s figure labels: Rising / Flat.
- Turner: \(1.4\) Gyr rising versus \(1.6\) Gyr flat.
- Powley: \(1.07\)–\(1.19\) versus \(1.39\)–\(1.46\) Gyr.
- Same direction of shift, \(\sim0.2\)–\(0.3\) Gyr, at similar ages.
- Turner Section 5.4: alpha-enhancement versus solar-scaled models, the other axis of Powley’s figure.
- Powley and Turner co-author Sandro Tacchella: [Kavli Institute for Cosmology Cambridge 2026 symposium LOC](https://www.kicc.cam.ac.uk/events/kavli-astrophysics-symposium-2026).
- Not settled: exact centres, \(\sigma\), \(\nu\), bin edges.
- Meeting note: \(3\) degrees of freedom. SFH code absent from the supplied excerpt.
- de Graaff’s constant \(+0.3\): not excluded without Powley’s parameter file.

</details>

<details>
<summary>References</summary>

- [Leja, Carnall, Johnson, Conroy & Speagle 2019](https://arxiv.org/abs/1811.03637), ApJ 876, 3. Eqs. 3–4, Section II.2.2, Appendix B.
- [Tacchella et al. 2022](https://arxiv.org/abs/2111.05351), Section III.2.
- [de Graaff et al.](https://arxiv.org/abs/2404.05683), Methods, “Star formation history testing”.
- [Turner, Tacchella, D’Eugenio et al. 2025](https://arxiv.org/abs/2410.05377), MNRAS 537, 1826. Sections 3.3 and 5.4, Eqs. 3–4, Appendix D.
- [Wang et al. 2023](https://arxiv.org/abs/2302.08486), Eqs. 3–4.
- [Suess et al. 2022a](https://arxiv.org/abs/2111.14878).
- [Suess et al. 2022b](https://arxiv.org/abs/2207.02883).
- [bd-j/prospector](https://github.com/bd-j/prospector), commit `a78d153`.
- [jakobhelton/jwst_program_id_08544](https://github.com/jakobhelton/jwst_program_id_08544), commit `725d2cd`.

</details>