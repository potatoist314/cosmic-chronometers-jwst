---
title: Weak emission in quiescent galaxies
date: 2026-09-21
section: Paper drafts
theme: Background reading
tags: [literature, emission-lines, masking, dr2-quiescent-sample]
job:
---

## Ceridwen sample and mask

| Item | Value | Check |
|---|---|---|
| Selection; `scripts/absorption_mask_analysis.py:71-75` | \(\mathrm{EW}([\mathrm{O\,II}])>-5\ \text{\AA}\) or missing; then drop \(\lvert\mathrm{EW}/\sigma_{\mathrm{EW}}\rvert\geq3\) in \([\mathrm{O\,II}]\,3727\) or \([\mathrm{O\,III}]\,5007\); missing \(\mathrm{EW}\) passes both tests | repo |
| DR2 catalogue; [Straatman+2018](https://arxiv.org/abs/1809.08236) | Fluxes and \(\mathrm{EW}\) only “at locations where an emission line was found”; missing values `NaN` | PDF |
| Fitted sample | 187 galaxies; `data/raw/legac_dr2/legaCdr2.fits.gz`; negative \(\mathrm{EW}\) = emission | repo |
| Catalogue coverage | \([\mathrm{O\,II}]\) \(\mathrm{EW}\): 13 present, 174 missing; \([\mathrm{O\,III}]\,5007\): 20 present, 167 missing; both missing in 154; all 59 galaxies at \(z<0.69\) missing \([\mathrm{O\,II}]\) \(\mathrm{EW}\) | repo |
| Uncertainties without equivalent widths | \(\sigma_{\mathrm{EW}}\) without \(\mathrm{EW}\): further 60 \([\mathrm{O\,II}]\), 81 \([\mathrm{O\,III}]\) galaxies | repo |
| Present \([\mathrm{O\,II}]\) values | \(\mathrm{EW}\) −0.05 to \(-3.32\ \text{\AA}\); median \(-2.06\ \text{\AA}\); median \(\sigma_{\mathrm{EW}}=1.17\ \text{\AA}\); largest \(\lvert\mathrm{EW}/\sigma\rvert=2.74\) | repo |
| Present \([\mathrm{O\,III}]\,5007\) values | \(\mathrm{EW}\) −0.18 to \(-1.77\ \text{\AA}\); median \(-0.46\ \text{\AA}\); median \(\sigma_{\mathrm{EW}}=0.28\ \text{\AA}\); largest \(\lvert\mathrm{EW}/\sigma\rvert=2.93\) | repo |
| Balmer catalogue; [Straatman+2018](https://arxiv.org/abs/1809.08236) | Balmer emission \(\mathrm{EW}\) outside selection; at \(\lvert\mathrm{EW}/\sigma_{\mathrm{EW}}\rvert\geq3\): \(\mathrm{H}\beta\) 2 of 26 catalogued (`M13_253688`: \(-5.76\ \text{\AA}\); `M15_89153`: \(-8.08\ \text{\AA}\); both \(z=0.84\)); \(\mathrm{H}\gamma\) 7 of 32; \(\mathrm{H}\delta\) 13 of 40; median catalogued \(\mathrm{EW}\): \(\mathrm{H}\gamma\) \(-0.54\ \text{\AA}\), \(\mathrm{H}\delta\) \(-0.56\ \text{\AA}\); robust Balmer absorption only for Balmer emission flux \(<10^{-16}\ \mathrm{erg\,cm^{-2}\,s^{-1}}\) | repo |
| Parent sample | `f_use = 1`; \(0.6\leq z<1.0\); 1389 galaxies; \([\mathrm{O\,II}]\) \(\mathrm{EW}\) present: 20% at \(z=0.60\text{–}0.69\), 46% at \(0.69\text{–}0.80\), 80% at \(0.80\text{–}1.0\); \([\mathrm{O\,III}]\,5007\) present: 56%, 27%, 1%, respectively | repo |
| Expected \(\mathrm{H}\beta\) emission | Individually undetected LEGA-C quiescent galaxy: \((0.6\text{ to }0.7)\times0.24\ \text{\AA}=0.14\text{ to }0.17\ \text{\AA}\); below \(0.39\ \text{\AA}\) stack limit | derived |
| \(\mathrm{H}\beta\) mask | \(\pm1500\ \mathrm{km\,s^{-1}}\): \(4837\text{–}4886\ \text{\AA}\); Lick \(\mathrm{H}\beta\) band \(4847.875\text{–}4876.625\ \text{\AA}\) inside mask ([Trager+2000a](https://arxiv.org/abs/astro-ph/0001072), table); \(\mathrm{H}\beta\) infill outside likelihood | derived |
| Unmasked lines | \(\mathrm{H}\gamma\), \(\mathrm{H}\delta\), \(\mathrm{H}\epsilon\), \([\mathrm{Ne\,III}]\,3869\) | repo |
| Case B flux ratios | \(\mathrm{H}\gamma/\mathrm{H}\beta=0.47\); \(\mathrm{H}\delta/\mathrm{H}\beta=0.26\) | textbook |
| Unmasked infill | With \(\mathrm{H}\beta=0.14\text{–}0.17\ \text{\AA}\): \(\mathrm{H}\gamma\) about \(0.07\text{–}0.08\ \text{\AA}\), \(\mathrm{H}\delta\) about \(0.04\ \text{\AA}\); before continuum ratio | derived |
| Mask width; [van der Wel+2021](https://arxiv.org/abs/2108.00744) | Half-width \(1500\ \mathrm{km\,s^{-1}}\); DR3 median gas dispersion \(128\ \mathrm{km\,s^{-1}}\), stellar \(161\ \mathrm{km\,s^{-1}}\) | PDF |
| Recorded test; model page, `emis_wide` | Adding \([\mathrm{Ne\,III}]\), \(\mathrm{H}\epsilon\), \(\mathrm{H}\delta\), \(\mathrm{H}\gamma\): 181–488 pixels removed; age shift 13.7 half-widths for `M4_108989` | repo |

## Incidence and strength

| Source | Sample | Result | Check |
|---|---|---|---|
| [Yan+2006](https://arxiv.org/abs/astro-ph/0512446) | SDSS DR4 red galaxies; \(z=0.05\text{–}0.1\); \(3''\) fibre | Detection \(\geq3\sigma\) in \(\mathrm{EW}\); 52.2% emission detected; 47.8% neither \([\mathrm{O\,II}]\) nor \(\mathrm{H}\alpha\) detected (27000 galaxies); LINER-like at least 28.8%; dusty star-forming about 6.5%; star-forming ratios only about 6%; LINER-like and line-free galaxies: one red sequence, differing only in line strength | PDF |
| [Sarzi+2006](https://arxiv.org/abs/astro-ph/0511307) | SAURON V; 48 E/S0 | Simultaneous stellar-spectrum and line fit; \(\mathrm{EW}\) detection limit \(0.1\ \text{\AA}\), set by template mismatch; emission in 75%, 55% in Virgo | PDF |
| [Kuntschner+2006](https://arxiv.org/abs/astro-ph/0602192) | SAURON VI; 48 galaxies | 5 without emission above limit; \([\mathrm{O\,III}]\) amplitude-over-noise cut 4: \(0.1\ \text{\AA}\) central, about \(0.2\ \text{\AA}\) outer; \(\mathrm{H}\beta\) limits \(0.06\ \text{\AA}\) inner, \(0.2\ \text{\AA}\) outer; \(\mathrm{H}\beta\) searched only where \([\mathrm{O\,III}]\) found | PDF |
| Gonzalez 1993; UC Santa Cruz PhD thesis; via [Trager+2000a](https://arxiv.org/abs/astro-ph/0001072) | G93; \(R_e/8\) aperture | Emission nearly always below a few tenths of an \(\text{\AA}\) (Fig. 4.10); median \([\mathrm{O\,III}]\,5007\) \(\mathrm{EW}=0.17\ \text{\AA}\) | not read |
| [Cid Fernandes+2011](https://arxiv.org/abs/1012.4426) | SDSS classes | Retired: \(W(\mathrm{H}\alpha)<3\ \text{\AA}\); passive, line-less: \(W(\mathrm{H}\alpha)\) and \(W([\mathrm{N\,II}])<0.5\ \text{\AA}\) | PDF |
| [Belfiore+2016](https://arxiv.org/abs/1605.07189) | 646 MaNGA galaxies | Extended \(\mathrm{kpc}\)-scale LIER emission in quiescent galaxies; radially flat \(\mathrm{EW}(\mathrm{H}\alpha)<3\ \text{\AA}\); line emission following stellar continuum | PDF |

## Power source

| Source | Sample | Result | Check |
|---|---|---|---|
| [Sarzi+2010](https://arxiv.org/abs/0912.0275) | SAURON | Hot old stars: tight stellar-surface-brightness–\(\mathrm{H}\beta\)-flux correlation; within-galaxy \(\mathrm{H}\beta\) \(\mathrm{EW}\) fluctuations averaging 32% around mean; pAGB best candidate on ionising-balance grounds | PDF |
| [Yan & Blanton 2012](https://arxiv.org/abs/1109.1280) | Extended emission | \(\mathrm{H}\alpha\) surface brightness \(\propto r^{-1.28}\); ionisation parameter increasing outwards; sources following stellar density reproducing line-ratio gradients; post-AGB ionisation-parameter deficit | PDF |
| [Stasinska+2008](https://arxiv.org/abs/0809.1341) | Retired galaxies | Ionisation by hot post-AGB stars and white dwarfs | PDF |
| [Singh+2013](https://arxiv.org/abs/1308.4271) | 48 CALIFA LINER-like galaxies | Radial line profiles inconsistent with central point source | PDF |
| [Sarzi+2010](https://arxiv.org/abs/0912.0275) | Handful of objects with radio or X-ray cores | Weak AGN confined to central \(2\text{–}3''\) | PDF |
| [Yan & Blanton 2012](https://arxiv.org/abs/1109.1280) | Apertures \(>100\ \mathrm{pc}\) | AGN ruled out as dominant source | PDF |
| [Yan+2006](https://arxiv.org/abs/astro-ph/0512446) | SDSS red galaxies | Diagnostic ratios classed as AGN-like: LINER, transition, Seyfert; source unidentified | PDF |
| [Sarzi+2010](https://arxiv.org/abs/0912.0275) | SAURON | Fast shocks unimportant; required velocities unreached in these potentials | PDF |
| [Yan & Blanton 2012](https://arxiv.org/abs/1109.1280) | Extended emission | Differences between line widths disfavouring shocks | PDF |
| [Sarzi+2010](https://arxiv.org/abs/0912.0275) | SAURON | OB stars dominant in 10%; recently formed subcomponent's pAGB stars powering another 10% | PDF |
| [Yan+2006](https://arxiv.org/abs/astro-ph/0512446) | Red galaxies | Star formation: about 6% | PDF |

## Ratio to \([\mathrm{O\,III}]\)

| Source | Sample | Result | Check |
|---|---|---|---|
| Gonzalez 1993; via [Trager+2000a](https://arxiv.org/abs/astro-ph/0001072) | G93 | \(\mathrm{EW}(\mathrm{H}\beta_{\mathrm{em}})/\mathrm{EW}([\mathrm{O\,III}]\,5007)\) about 0.7; correction \(\Delta\mathrm{H}\beta=0.7\,\mathrm{EW}([\mathrm{O\,III}]\,5007)\) | not read |
| [Trager+2000a](https://arxiv.org/abs/astro-ph/0001072) | 27 E to S0− galaxies; G93 plus Ho+1997; \(\mathrm{EW}(\mathrm{H}\alpha)>1\ \text{\AA}\) | Ratio 0.33 to 1.25; median 0.60; proposed coefficient 0.6 rather than 0.7; published G93 data retaining 0.7 correction | PDF |
| [Kuntschner+2006](https://arxiv.org/abs/astro-ph/0602192) | SAURON | Median 0.67; range 0.3 to 2.3; variation across each galaxy; weak evidence for decline at large \([\mathrm{O\,III}]\); NGC 3032: 2.1 (star formation); correction accuracy doubtful for individual galaxies | PDF |
| [Sarzi+2010](https://arxiv.org/abs/0912.0275) | SAURON | \(\log([\mathrm{O\,III}]/\mathrm{H}\beta)=0\text{ to }0.5\): 75% of values | PDF |
| [Maseda+2021](https://arxiv.org/abs/2110.00009) | \([\mathrm{O\,II}]\)-detected quiescent stack | \(\mathrm{H}\beta\) 0.39 / \([\mathrm{O\,III}]\) 0.51 = 0.76 | derived |

## Infill and age

| Source | Sample | Result | Check |
|---|---|---|---|
| [Trager+2000a](https://arxiv.org/abs/astro-ph/0001072) | Typical galaxies | Infill: lower \(\mathrm{H}\beta\) index, higher SSP age; \(0.02\ \text{\AA}\) in \(\mathrm{H}\beta\): about 3% in age; ratio scatter: age errors about ±9%; \(\mathrm{H}\beta\) errors \(\lesssim0.1\ \text{\AA}\) required for ages to 10% | PDF |
| [Trager+2000a](https://arxiv.org/abs/astro-ph/0001072), Appendix B | Uncorrected sample | Higher ages for a few strong-\([\mathrm{O\,III}]\) galaxies; broad age distribution little changed; infill ruled out as cause of whole age spread | PDF |
| Gonzalez 1993; via [Trager+2000a](https://arxiv.org/abs/astro-ph/0001072) | G93 median | Correction: \((0.6\text{ to }0.7)\times0.17\ \text{\AA}=0.10\text{ to }0.12\ \text{\AA}\) | derived |
| [Straatman+2018](https://arxiv.org/abs/1809.08236); [van der Wel+2021](https://arxiv.org/abs/2108.00744) | LEGA-C DR2; DR3 | Lick indices after best-fit emission-line-model subtraction; DR3 line-flux systematic uncertainty of order 15% | PDF |
| [Gallazzi+2026 I](https://arxiv.org/abs/2512.07952) | LEGA-C DR3 indices | “Uncertainties in corrections for emission line infill” | PDF |

## Redshift 0.6–0.9

| Source | Sample | Result | Check |
|---|---|---|---|
| [Maseda+2021](https://arxiv.org/abs/2110.00009) | LEGA-C; \(z\) about 0.85; UVJ-quiescent | 59% with \([\mathrm{O\,II}]\) above \(1.5\ \text{\AA}\) completeness limit | PDF |
| [Maseda+2021](https://arxiv.org/abs/2110.00009) | Median stack below limit | \([\mathrm{O\,II}]\): \(0.59\pm0.052\ \text{\AA}\); \([\mathrm{O\,III}]\): \(0.24\pm0.037\ \text{\AA}\); \(\mathrm{H}\beta<0.39\ \text{\AA}\) (\(3\sigma\)); \([\mathrm{Ne\,III}]<0.063\ \text{\AA}\) | PDF |
| [Maseda+2021](https://arxiv.org/abs/2110.00009) | Detected stack | \([\mathrm{O\,II}]\): \(4.6\pm0.15\ \text{\AA}\); \(\mathrm{H}\beta\): \(0.39\pm0.093\ \text{\AA}\); \([\mathrm{O\,III}]\): \(0.51\pm0.17\ \text{\AA}\); \([\mathrm{Ne\,III}]\): \(0.16\pm0.062\ \text{\AA}\) | PDF |
| [Maseda+2021](https://arxiv.org/abs/2110.00009) | Stack individually below \(0.3\ \text{\AA}\) | \([\mathrm{O\,II}]\) detected at \(>3\sigma\) | PDF |
| [Maseda+2021](https://arxiv.org/abs/2110.00009) | LEGA-C quiescent; GAMA comparison | \([\mathrm{O\,II}]\) luminosity per stellar mass: 3 times \(z<0.1\) GAMA value; star formation unlikely to supply most ionising photons; AGN and evolved-star shares unquantified | PDF |
| [Borghi+2022a](https://arxiv.org/abs/2106.14894) | LEGA-C passive candidates after NUVrJ selection | About one third with significant \([\mathrm{O\,II}]\); cut at \(\mathrm{EW}([\mathrm{O\,II}])>5\ \text{\AA}\), plus visual \([\mathrm{O\,II}]\) and \([\mathrm{O\,III}]\) inspection | PDF |
| [Yan+2006](https://arxiv.org/abs/astro-ph/0512446) | Red galaxies; \(z\) about 1 | \([\mathrm{O\,II}]\) not a star-formation proxy; post-starburst samples cut on \([\mathrm{O\,II}]\) incomplete | PDF |
| Papers read | Quiescent galaxies; \(z=0.6\text{–}0.9\) | Diagnostic-diagram line ratios not found | repo |

## Citation check

| Citation | Claim as given | Paper | Check |
|---|---|---|---|
| [Yan+2006](https://arxiv.org/abs/astro-ph/0512446) | Faint emission common in red-sequence galaxies | 52.2% of SDSS red galaxies detected at \(\geq3\sigma\), mostly LINER-like; no statement on emission below detection; ratios classed as AGN-like | PDF |
| [Yan & Blanton 2012](https://arxiv.org/abs/1109.1280) | Extended emission, not AGN | Confirmed: extended, \(r^{-1.28}\); AGN ruled out as dominant; shocks disfavoured; post-AGB favoured with ionisation-parameter deficit | PDF |
| [Sarzi+2010](https://arxiv.org/abs/0912.0275) | Post-AGB stars power it | Confirmed; 75% detection rate and \(0.1\ \text{\AA}\) limit in [Sarzi+2006](https://arxiv.org/abs/astro-ph/0511307), not Sarzi+2010 | PDF |
| Gonzalez 1993 | \(\mathrm{H}\beta\) emission about \(0.6\times[\mathrm{O\,III}]\) | G93 coefficient 0.7, quoted by [Trager+2000a](https://arxiv.org/abs/astro-ph/0001072); thesis not read | not read |
| [Trager+2000](https://arxiv.org/abs/astro-ph/0001072) | \(0.6\times[\mathrm{O\,III}]\,5007\) | Confirmed in Trager+2000a (Paper I): median 0.60 of 27 galaxies, range 0.33–1.25; proposed improvement on G93's 0.7; G93 data not re-corrected | PDF |
| [Kuntschner+2006](https://arxiv.org/abs/astro-ph/0602192) | Ratio varies | Confirmed: median 0.67, range 0.3–2.3; variation within galaxies | PDF |

<details><summary>Check marks</summary>

- PDF: read in the paper's arXiv PDF.
- not read: paper text not obtained; the claim is reported by another paper.
- derived: arithmetic on the cited numbers, not stated in a paper.
- textbook: standard value, not checked in a paper.
- repo: read from this repository

</details>
