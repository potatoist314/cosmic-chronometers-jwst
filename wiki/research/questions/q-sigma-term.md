---
kind: question
id: q-sigma-term
title: The velocity-dispersion term in the chronometer line
date: 2026-11-17
origin: new
status: open
---

## Context

[C/N free](wiki/notes/model.md#cn-responses) unless marked. \(H\) in km/s/Mpc, ranges 16–84%.

**What it is.** Plain line: age \(= a + b\,z\). With the term: age \(= a + b\,z + c\log_{10}\sigma_\star\). \(H\) comes from \(b\). \(\sigma_\star\), the stellar velocity dispersion, is the LEGA-C catalogue value (line widths), not an age-fit output.

**Why \(b\) changes.** At fixed \(z\), higher \(\sigma_\star\) is older: \(c=3.05\) (2.56 to 3.52) Gyr per dex (factor 10). \(\sigma_\star\) rises with \(z\). The correlation is 0.19 in the 194 and 0.21 in all DR3 primary targets at \(z\) 0.6–1.0. At fixed COSMOS2020 mass it is 0.09. So the high-\(z\) end is older, and the plain line flattens.

| \(H\) at \(z_\mathrm{eff}=0.77\) | 194 | 333 |
| --- | --- | --- |
| Plain line | 107 (95 to 122) | 108 (99 to 120) |
| \(\log\sigma_\star\) term | 94 (86 to 103) | 95 (88 to 103) |
| \(\sigma_\star\) thirds, common slope | 95 (87 to 105) | 96 (89 to 104) |
| COSMOS2020 \(\log M_\star\) term | 93 (85 to 103) | 95 (88 to 103) |
| Planck18 | 105.4 | 105.3 |

333: the 194 plus 153 added DR3 galaxies, less 14 flagged saturated or bad-area in COSMOS2015. Thirds: one slope, an intercept per third.

**Binning.** Papers bin by \(\sigma_\star\) or mass instead. Bins assume no shape. The term assumes a straight line in \(\log\sigma_\star\), the same at every \(z\). The papers' binned differences give 66 to 117 on the 194, by \(z\)-bin choice.

| Mocks, plain arm, 194 | Slope change (Gyr per unit \(z\)), no relation | Width against plain line | Injected relation removed |
| --- | --- | --- | --- |
| \(\sigma_\star\) halves, common slope | −0.07 (−0.11 to −0.02) | 0.98 | 58% |
| \(\sigma_\star\) thirds, common slope | −0.04 (−0.10 to +0.03) | 1.00 | 84% |
| \(\log\sigma_\star\) term | −0.04 (−0.10 to +0.01) | 0.99 | 100% |

Mocks: simulated spectra of known age, fitted like the data. Injected: 3.19 Gyr per dex added to the fitted ages.

**Overfitting checks.** \(c\) is 6σ from zero. On the 153 added galaxies alone, \(c=3.74\) (3.22 to 4.26), 0.98σ from the 194. Scatter about the line: 0.80 Gyr, 0.73 Gyr with the term.

**Open.** If our fits make high-\(\sigma_\star\) galaxies look older, the term corrects a fit artefact, not a population effect. The COSMOS2020 mass term (photometric mass) gives the same \(H\).

## Your words

```json
[
  {
    "date": "2026-11-17",
    "text": "i don't understand how the velocity dispersion term works",
    "display_text": "I don't understand how the velocity dispersion term works."
  },
  {
    "date": "2026-11-17",
    "text": "more crudely?"
  },
  {
    "date": "2026-11-17",
    "text": "is the term overfitting?",
    "display_text": "Is the term overfitting?"
  },
  {
    "date": "2026-11-17",
    "text": "i don't fully understand this - put it on the wiki but i can't say much until i really understand this",
    "display_text": "I don't fully understand this. Put it on the wiki, but I can't say much until I really understand this."
  }
]
```

## References

- \(H\), 194 and 333: [estimators.csv](results/sigma-split-2026-11-16/more-galaxies-2026-11-17/estimators.csv), C/N-free rows of samples `194` and `combined without saturation or bad area`. The 194 also in [headline.csv](results/sigma-split-2026-11-16/headline.csv).
- \(c\) and scatter: [split-plane.csv](results/sigma-split-2026-11-16/split-plane.csv), `coefficient`, `scatter_plain`, `scatter_plane`. Plain arm \(c=3.19\) (2.69 to 3.69), scatter 0.87 to 0.80 Gyr.
- \(c\) on the 153 added galaxies: [gained-minus-194.csv](results/sigma-split-2026-11-16/more-galaxies-2026-11-17/gained-minus-194.csv), row `covariate coefficient`. Plain arm 3.46 (3.02 to 3.92), 0.4σ.
- \(z_\mathrm{eff}\), the redshift of each \(H\) value: 0.775 (194), 0.773 (333). Mass term: 190 and 327 galaxies with a COSMOS2020 mass.
- Correlation of \(\log\sigma_\star\) with \(z\) (Pearson): [selection-check.csv](results/sigma-split-2026-11-16/selection-check.csv). DR3 primary sample: 2826 galaxies.
- Binned differences: [binned-difference.csv](results/sigma-split-2026-11-16/binned-difference.csv), C/N-free `log_sigma_star` rows, equal-count 66, equal-width 117 \(z\) bins.
- Mocks: [mock-split.csv](results/sigma-split-2026-11-16/mock-split.csv), plain `log_sigma_star` rows. Removed share from each estimator's slope with and without the injection.
- Published binned splits: [literature.csv](results/sigma-split-2026-11-16/literature.csv), Borghi+2022b Sect. 2, Jiao+2023 Sect. 5.1–5.2, Moresco+2012 Sect. 2, Moresco+2016 Sect. 3. Common slope across \(\sigma_\star\) strata, Alvarez+2026 Sect. 4.4.
- \(\sigma_\star\): LEGA-C DR3 column `SIGMA_STARS_PRIME`, “observed stellar velocity dispersion”, “velocity RMSs (line widths)” ([ESO release description](data/raw/legac_dr3/ESO_DR3_release_description.pdf), p. 1 and p. 6).
- Script: [sigma_split.py](results/sigma-split-2026-11-16/sigma_split.py). Chronometer: [q-afe-age-chronometer](wiki/research/questions/q-afe-age-chronometer.md). Progenitor bias: [q-progenitor-bias](wiki/research/questions/q-progenitor-bias.md).

## Decisions

```json
[]
```
