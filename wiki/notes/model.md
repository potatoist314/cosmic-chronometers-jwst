---
title: Literature values: LEGA-C quiescent galaxies
date: 2026-09-17
section: Literature
theme: Background reading
tags: [papers, quiescent, lega-c, priors, parameters, defaults]
job:
source: papers/quiescent populations/README.md
figures: [literature-vs-ceridwen.png]
---

<figure>
<img src="figures/papers-quiescent-parameters/literature-vs-ceridwen.png" alt="One row per literature paper for age, metallicity and alpha enhancement, with the Ceridwen DR2 sample median and 16-84 spread as the blue top row">
<figcaption>Age, metallicity and alpha-enhancement panels: redshift-ordered literature-paper rows; grey bars: quoted ranges/\(\pm\)1\(\sigma\); blue top row: 187-galaxy Ceridwen DR2 median (also vertical line), 16–84 percentile across-galaxy spread; circles: \([\mathrm{Z}/\mathrm{H}]\)/\([\alpha/\mathrm{Fe}]\); squares: \([\mathrm{Fe}/\mathrm{H}]\)/\([\mathrm{Mg}/\mathrm{Fe}]\); Ceridwen \([\mathrm{Fe}/\mathrm{H}]\) = Z + 1.7328 (grid’s built-in solar reference).</figcaption>
</figure>

## Prospector reference: Jonah Powley

| Parameter | His prior | Ceridwen production |
| --- | --- | --- |
| Dust law | Kriek & Conroy (`dust_type` 4) | Kriek–Conroy diffuse law |
| Dust index | Free, TopHat(−1.2, 0.4) | Uniform(−1.0, 0.4) |
| \(\tau_{\mathrm{dust},2}\) | Free, ClippedNormal(0.3, 1.0) on [0, 4] | Uniform(0, 0.2); Ceridwen's documented default matches his prior |
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

## Physical parameters

| Quantity | Prior | DR2 median (187) | Literature at z~0.7 | Decided |
| --- | --- | --- | --- | --- |
| \(\log M_\star\) formed | Uniform(8, 13) | 11.34 | Kaushal+2024 QG median 11.2; Borghi+2022a > 10.4; Cappellari 2023 > 10.5 | |
| \([\mathrm{Fe}/\mathrm{H}]\) | Uniform(−2.5, 0.5), 13 grid nodes; grid Z = \([\mathrm{Fe}/\mathrm{H}]\) − 1.7328 | −0.18 | Borghi+2022a \([\mathrm{Z}/\mathrm{H}]\) 0.08 \(\pm\) 0.18; Beverage+2021 ~0.2 dex below z~0; Cheng+2025 higher at redder U−V; Gallazzi+2026 no QG evolution to SDSS | |
| \([\alpha/\mathrm{Fe}]\) | Uniform(−0.2, 0.6), 5 grid nodes | −0.05 | Bevacqua+2023 +0.24 \(\pm\) 0.01, 91% supersolar; Borghi+2022a +0.13 \(\pm\) 0.11; Beverage+2023 \([\mathrm{Mg}/\mathrm{Fe}]\) ~0.2–0.3 | |
| SFH ratios \(\times\) 7 | Student-t(0, 0.3 dex, df 2), unbounded | \(t_{50}\) 5.03 Gyr, \(t_{80}-t_{20}\) 2.55 Gyr | Kaushal+2024 \(t_{50}\), \(t_{90}\) mass-independent; Nersesian+2025 \(\tau_q\) 1.23 Gyr | |
| \(\tau_{\mathrm{dust}}\) at 5500 \(\text{\AA}\) | Uniform(0, 0.2); the 187-galaxy run used Uniform(0, 2) | 0.45; 184 of 187 above 0.2 | | |
| Dust slope | Uniform(−1.0, 0.4) | | | |
| \(\sigma_\star\) | Fixed at DR2; with `CERIDWEN_FREE_SIGMA=1`, Normal(DR2, error) clipped at \(\pm\) 3 times the error | 204 \(\mathrm{km\,s^{-1}}\) | DR3 16/50/84: 127/166/207 \(\mathrm{km\,s^{-1}}\); Kaushal+2024 QG ~200; Cappellari 2023 quenched above 200; Gallazzi+2026 age transition at \(\log\sigma\) 2.3 | Liu Hao, 15 Sep 2026 meeting |
| Redshift | Fixed at catalogue z | 0.73 | | |
| Age, mass-weighted | Derived | 4.81 Gyr | Borghi+2022a 2–4 Gyr SSP-equivalent, Ceridwen +1.29 Gyr for the 68-galaxy overlap; Beverage+2023 rises with \(\sigma\); Nersesian+2025 QG 1.1 Gyr older than SFG; Barone+2022 no age–\(\Sigma\) relation | |

## Sample

| Step | Rule | N |
| --- | --- | --- |
| DR2 spectra matched to COSMOS2015 | `f_use` 1, `f_ppxf` 0, `f_z` 0, `f_int` 0, S/N > 0, 0.6 ≤ z < 1.0, rest NUV, r and J magnitudes present | 1328 |
| NUVrJ passive | NUV − r > 3 (r − J) + 1 and NUV − r > 3.1 | 609 |
| Weak [O II] | EW([O II] 3727) > −5 \(\text{\AA}\) or missing | 454 |
| No emission detected | \(\lvert \mathrm{EW}/\sigma_{\mathrm{EW}} \rvert < 3\) for [O II] 3727 and [O III] 5007 | 349 |
| Clean photometry | COSMOS2015 Area 0, Sat 0, Cfl 1, Flag 0 | 194 |
| One spectrum per object | Highest S/N kept | 187 |

## Spectrum and photometry

| Item | Setting |
| --- | --- |
| Pixels | DR2 `QUAL` 0, error > 0, finite flux; other pixels assigned uncertainty 1 and masked; over 3000 good pixels required, with fitted pixels above 0.7 × good pixels |
| Units | Air to vacuum wavelengths; \(10^{-19}\) erg s\(^{-1}\) cm\(^{-2}\) \(\text{\AA}^{-1}\) to \(F_\nu\) cgs |
| Resolution | FITS `SPEC_RES` as FWHM resolving power; DR2 \(\sigma_\star\) applied as line-of-sight broadening; CSP broadening 0 |
| Emission-line mask | \(\pm\) 1500 \(\mathrm{km\,s^{-1}}\) at catalogue z around rest 3726.0, 3728.8, 4861.3, 4958.9, 5006.8 \(\text{\AA}\) ([O II], H\(\beta\), [O III]); no nebular model |
| Telluric mask | 7590–7660 \(\text{\AA}\) air, A band |
| Fitted pixels | All valid pixels; no extra rest windows |
| Photometry | 12 COSMOS2015 bands u*, B, V, r+, i+, z+, Y, J, H, Ks, 3.6, 4.5 µm; 3″ apertures scaled to total by the per-object offset (optical and NIR), Galactic extinction with Laigle+2016 coefficients, Table 3 zero-point offsets; IRAC already total; µJy to maggies |
| Photometric errors | 5% of flux added in quadrature; all 12 bands fitted |

## Model and calibration

| Item | Setting | Decided |
| --- | --- | --- |
| Grid | `amist_c3k_hr_krou_afe`: aMIST v2.5, C3K v2.3 high resolution (R ≈ 6000), Kroupa 2001 IMF; 13 metallicity, 5 \([\alpha/\mathrm{Fe}]\) and 107 age nodes | |
| SFH | Eight lookback nodes: 0, 0.03, 0.1, 0.3, 1, 3, 5 Gyr and the age of the Universe at z; step interpolation; \([\mathrm{Fe}/\mathrm{H}]\) and \([\alpha/\mathrm{Fe}]\) constant over age | |
| Dust | Kriek–Conroy diffuse law with free slope; birth-cloud dust, dust emission, IGM and nebular emission off | |
| Calibration polynomial | Chebyshev order 10 over the fitted range; coefficients Normal(0, 0.1); no constant term; marginalised analytically. Order 3 until 17 Sep 2026. | Liu Hao, 17 Sep 2026; order 3 from 6 Sep 2026; orders 5 and 10 tested 15 Sep 2026. |
| Spectrum scaling | Normal(1, 0.3) clipped to [0.2, 3], sampled | |
| Extra spectral error | \(\log f_{\mathrm{calib}}\) Uniform(ln 0.01, ln 0.10); \(\sigma_{\mathrm{eff}}^2 = \sigma_{\mathrm{obs}}^2 + (f_{\mathrm{calib}}\,\lvert\mu\rvert)^2\) with model flux \(\mu\) | Under review since the 15 Sep 2026 meeting |

## Sampler

| Item | Setting |
| --- | --- |
| Likelihood | Diagonal Gaussian for photometry; diagonal Gaussian with the fractional term and the marginalised polynomial for the spectrum |
| Nested sampler | BlackJAX NSS: 500 live points, 65 inner steps, 100 deleted per step, log Z tolerance −5, checkpoint every 1200 s, seed 20260812 |
| Pass rule | Finite log Z and error; posterior-weight ESS ≥ 200 |
| Posterior draws | 2000 equal-weight draws (seed 20260813); 400 evenly spaced rows for derived quantities |

## Derived quantities

| Quantity | Definition |
| --- | --- |
| Bin masses | Trapezoidal integral of the SFR over each of the 7 intervals; fractions of the total formed mass |
| Mass-weighted age | Bin masses weighted by the interval midpoints |
| \(t_{20}\), \(t_{50}\), \(t_{80}\) | Lookback time younger than which 20, 50 or 80% of the formed mass was formed; \(\Delta t = t_{80} - t_{20}\) |
| \([\mathrm{Fe}/\mathrm{H}]\) | Grid Z + 1.7328283 (solar Z 0.0185) |
| \(f_{\mathrm{calib}}\) | Reported in percent |
| Summaries | Percentiles: 16, 50 and 84 |

## Other redshifts

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

Sources: `notebooks/ceridwen_integrated_photometry_spectra.ipynb` cells 2, 6, 8, 12, 14, 16, 18, 20, 22 and 30 (zero-based); `scripts/build_dr2_quiescent_summary.py`; `ceridwen/ceridwen/likelihood/noise_model.py`; `ceridwen/scripts_afe/build_afe_hr_grid.py`; `results/dr2-quiescent-new-defaults-summary.csv`; the 187-galaxy prior from `results/dr2-quiescent-new-defaults/123161-M4_123161/M4_123161_executed.ipynb`. Figures in [DR2 quiescent sample](/wiki/n/dr2-quiescent-sample/); [literature comparison](/wiki/roadmap/#literature-comparison); earlier reference: [Current default model](/wiki/n/default-fit-parameters/).

</details>
