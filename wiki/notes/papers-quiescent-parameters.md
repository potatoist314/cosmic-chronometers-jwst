---
title: Literature values: LEGA-C quiescent galaxies
date: 2026-09-15
section: Literature
theme: Background reading
tags: [papers, quiescent, lega-c]
job:
source: papers/quiescent populations/README.md
---

<div id="a-lega-c-quiescent-sample"></div>

## LEGA-C quiescent sample

| Item | DR3 ([van der Wel+2021](https://arxiv.org/abs/2108.00744)) | Project sample |
| --- | --- | --- |
| Release | DR3: 4081 spectra, 3741 galaxies | DR2 ([Straatman+2018](https://arxiv.org/abs/1809.08236), VizieR J/ApJS/239/27) |
| Redshift | 0.6 < z < 1.0 | median 0.73 |
| Spectra | VIMOS, R ~ 2500, 6300–8800 Å, S/N ~ 20 per Å | same |
| Mass limit | log M⋆ ≳ 10.4 | median log M⋆ 11.11 |
| σ⋆ 16/50/84 | 127 / 166 / 207 km/s | median 204 km/s |
| Quiescent selection | UVJ ([Muzzin+2013](https://arxiv.org/abs/1303.4409)): 1208 galaxies | NUVrJ + emission-line veto: 187 galaxies (`scripts/run_ceridwen_vast_multi_gpu.py:79-137`) |

<div id="b-reference-values-for-lega-c-quiescent-galaxies-by-paper"></div>

## Reference values for LEGA-C quiescent galaxies, by paper

| Paper | N | z | Method | log M⋆ | Age | [Z/H] or [Fe/H] | [α/Fe] or [Mg/Fe] |
| --- | --- | --- | --- | --- | --- | --- | --- |
| [Borghi+2022a](https://arxiv.org/abs/2106.14894) | 140 | ~0.7 | Lick indices, SSP | > 10.4 | 2–4 Gyr SSP-equivalent, declining with z | [Z/H] 0.08 ± 0.18 | 0.13 ± 0.11 |
| [Beverage+2021](https://arxiv.org/abs/2105.12750) | 65 | 0.59–0.75 | alf | massive | marginal rise with M⋆ | [Fe/H], [Mg/H] track M⋆/Re, not M⋆; ~0.2 dex below z~0 | [Mg/Fe] flat in M⋆ and M⋆/Re |
| [Beverage+2023](https://arxiv.org/abs/2303.03412) | 135 | ~0.7 | alf, σ stacks | σ 150–250 km/s | rises with σ | Z rises with σ; 0.05 dex precision | [X/Fe] trends mild or absent |
| [Bevacqua+2023](https://arxiv.org/abs/2308.03441) | 183 | 0.60–0.75 | Mgb, Fe4383 | 10.4–11.6 | – | – | +0.24 ± 0.01; 91% supersolar; no trend with Z, M⋆, σ |
| [Bevacqua+2024](https://arxiv.org/abs/2407.12704) | 637 | 0.6–1.0 | full spectrum, mass-weighted | 10.4–11.7 | – | mass-dependent lower bound (MEME) | – |
| [Gallazzi+2026 I](https://arxiv.org/abs/2512.07952) / [II](https://arxiv.org/abs/2511.11805) | 552 | 0.6–0.77 | indices + rizYJ, Bayesian | > 10 | bimodal across ~1e11 M☉; transition at log σ 2.3 | steep→flat at 10^10.8; no QG evolution to SDSS | – |
| [Cheng+2025](https://arxiv.org/abs/2505.08858) | ~700 | 0.6–1.0 | alf | 10.2–11.8 | rises with U−V | [Fe/H] higher at redder U−V, bluer V−J | – |
| [Cheng+2024](https://arxiv.org/abs/2407.10974) | 456 | 0.6–1.0 | alf, resolved | 10.3–11.8 | flat gradient | d[Fe/H]/dlog Re −0.05 observed, ~−0.15 intrinsic | flat gradient |
| [Barone+2022](https://arxiv.org/abs/2107.01054) | LEGA-C + SAMI | 0.60–0.76 | indices | – | no age–Σ relation at z~0.7 | [Z/H] tracks M⋆/Re | – |
| [Kaushal+2024](https://arxiv.org/abs/2307.03725) | 1244 | 0.6–1.0 | Bagpipes, Prospector | median 11.2 | t50, t90 mass-independent | – | – |
| [Nersesian+2025](https://arxiv.org/abs/2502.03021) / [2026](https://arxiv.org/abs/2512.10383) | 2908 | 0.6–1.0 | Prospector | > 9 | QG 1.1 Gyr older than SFG; τ_q 1.23 Gyr (0.13 compact PSB) | large QG near solar; compact metal-rich | – |
| [Cappellari 2023](https://arxiv.org/abs/2208.14974) | 3200 | 0.6–1.0 | pPXF + 28 bands | > 10.5 | quench threshold σ⋆ > 200 km/s | [M/H] on σ, then age | – |

<div id="c-z-0-anchors-and-other-redshifts"></div>

## z~0 anchors and other redshifts

| Reference | Sample | Result |
| --- | --- | --- |
| [Gallazzi+2005](https://arxiv.org/abs/astro-ph/0506539) | SDSS | mass–metallicity and age–mass relations; transition 3e9–3e10 M☉ |
| [Thomas+2005](https://arxiv.org/abs/astro-ph/0410209), [2010](https://arxiv.org/abs/0912.0259) | local early types | [α/Fe]–σ slope ~0.2; environment-independent |
| [Conroy+2014](https://arxiv.org/abs/1303.6629) | SDSS stacks, σ 90–300 km/s | [Fe/H] varies < 0.1 dex; [Mg/Fe] 0.0→0.25; ages 6–12 Gyr |
| [McDermid+2015](https://arxiv.org/abs/1501.03723) | ATLAS3D | compact galaxies older, metal-richer, more α-enhanced |
| [Gallazzi+2014](https://arxiv.org/abs/1404.5624) | z~0.7, E-CDFS | −0.28 dex age, −0.13 dex Z versus SDSS; QGs need no further enrichment |
| [Choi+2014](https://arxiv.org/abs/1403.4932) | SDSS + AGES, 0.1 < z < 0.7 | stacked abundances across redshift |
| [Kriek+2019](https://arxiv.org/abs/1907.04327) | z~1.4 | [Fe/H] −0.2 dex; [Mg/Fe] up to 0.44 |
| [Carnall+2022](https://arxiv.org/abs/2108.13430) | 1.0 < z < 1.3 | [Z/H] −0.13 ± 0.08 (Bagpipes), 0.04 ± 0.14 (alf); [Fe/H] −0.18 ± 0.08 |
| [Estrada-Carpenter+2019](https://arxiv.org/abs/1810.02824) | 1 < z < 1.8 | roughly solar metallicity |
| [Beverage+2024](https://arxiv.org/abs/2312.05307) | z 1.4 / 2.1 | [Fe/H] −0.2 / −0.3; [Mg/Fe] 0.3 / 0.5 |
| Reviews | [Renzini 2006](https://arxiv.org/abs/astro-ph/0603479), [Conroy 2013](https://arxiv.org/abs/1301.7095), [Cappellari 2016](https://arxiv.org/abs/1602.04267) | ARA&A |

<div id="d-ceridwen-dr2-medians-against-the-literature"></div>

## Ceridwen DR2 medians against the literature

| Quantity | Ceridwen DR2 median (N=187) | Literature at z~0.7 |
| --- | --- | --- |
| log M⋆ | 11.11 | Kaushal+2024 QG median 11.2 |
| σ⋆ | 204 km/s | DR3 median 166 km/s; Kaushal+2024 QG ~200 km/s |
| Age | 3.02 Gyr, mass-weighted | Borghi+2022a 2–4 Gyr SSP-equivalent; Ceridwen +0.26 Gyr above Borghi on the 68-galaxy overlap |
| Metallicity | log Z −1.76, absolute; solar reference open ([roadmap: metallicity](/wiki/roadmap/#metallicity)) | Borghi+2022a [Z/H] 0.08; Beverage, Cheng [Fe/H] ~ −0.1 to 0.0 |
| [α/Fe] | 0.05 | Bevacqua+2023 +0.24; Borghi+2022a +0.13; Beverage [Mg/Fe] ~0.2–0.3 |

Source: `results/dr2-quiescent-summary.csv`; figures in [DR2 quiescent sample](/wiki/n/dr2-quiescent-sample/). [Literature comparison](/wiki/roadmap/#literature-comparison).

<div id="why-this-matters-here"></div>
