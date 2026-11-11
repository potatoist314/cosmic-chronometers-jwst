---
kind: question
id: q-afe-age-chronometer
title: Low alpha/Fe, Mg b and the chronometer age slope
date: 2026-11-10
origin: existing
status: open
---

## Context

### Answer

- **Fit every galaxy on the same rest-frame window (4074.5–4666.1 Å) and both problems go away.** Median \([\alpha/\mathrm{Fe}]\) is +0.21 with no redshift trend (\(\rho=-0.11\)). The age–redshift slope is −4.60 (−5.56 to −3.60) Gyr per unit redshift against −5.31 expected.
- **The full-spectrum fits go wrong because of pixels outside that window.** Which of those pixels a galaxy has changes with redshift.
- **The method recovers a known slope.** On mock galaxies with a true slope of −5.24, full-spectrum fits give −5.63, and the prior does not flatten it.

### Terms

- **Slope:** straight line through the posterior median mass-weighted ages against \(z\), in Gyr per unit redshift. Ranges are galaxy-bootstrap 16–84% unless stated.
- **Expected:** the same line through the Planck18 age of the universe at the same redshifts.
- **Normal model:** production defaults, \([\alpha/\mathrm{Fe}]\) free, no carbon or nitrogen parameter.
- **Pull:** summed (observed − model) / uncertainty over a band, divided by \(\sqrt{N_\mathrm{pixels}}\). Negative means the model absorption is too weak.

### Common window against full spectrum

| Fit | Galaxies | Slope | 16–84% | Median \([\alpha/\mathrm{Fe}]\) | \(\rho([\alpha/\mathrm{Fe}], z)\) |
| --- | --- | --- | --- | --- | --- |
| Normal model, full spectrum | 108 | −2.09 | −3.13 to −0.99 | +0.01 | −0.42 |
| Normal model, 4074.5–4666.1 Å | 110 | −4.60 | −5.56 to −3.60 | +0.21 | −0.11 |
| Carbon and nitrogen free, 4074.5–4666.1 Å | 110 | −5.37 | −6.29 to −4.41 | +0.14 | −0.04 |

- Expected slope: −5.31.
- 108 of the 110 window galaxies are valid in every compared arm. On those 108 the window slopes are −4.62 and −5.39.
- With carbon and nitrogen free the window slope gives \(H=106\) (90–129) \(\mathrm{km\,s^{-1}\,Mpc^{-1}}\) at \(z=0.725\). The Planck18 line over the same galaxies gives 107. Planck18 \(H(z=0.728)\) is 102.5.

### Rest-frame coverage changes with redshift

- The fitted observed range is similar for every galaxy: median 6357–8818 Å. Redshift then sets the rest-frame range.
- The lowest-redshift third (median \(z=0.675\)) covers rest 3882–5387 Å. The highest third (median \(z=0.890\)) covers 3421–4692 Å.
- Low-redshift fits include \(\mathrm{H}\beta\), Fe5015, Mg b and the Fe lines beyond, but not the far blue. The median high-redshift fit has the far blue and ends before all of those.
- The model does not match real spectra equally well everywhere. For the 61 galaxies with Mg b, the Mg b pull is −3.28 and the \(\mathrm{C}_2\) 4668 pull is −5.20.
- Each mismatched region pushes the fit its own way, so low- and high-redshift galaxies get different errors.
- A difference in error between low and high redshift looks the same as a trend with redshift.
- On a common window the model is still imperfect, but the error is the same for every galaxy. A slope depends only on differences between galaxies, so a shared error cancels.

### Window extensions

Normal model. Changes are medians of the extended fit minus the 4074.5–4666.1 Å fit of the same galaxy.

| Window (Å) | Adds | Galaxies | \(\Delta[\alpha/\mathrm{Fe}]\) | \(\Delta\)age (Gyr) | \(\Delta[\mathrm{Fe}/\mathrm{H}]\) | Slope change (16–84%) |
| --- | --- | --- | --- | --- | --- | --- |
| 3742.9–4666.1 | H10, H9, H8 | 60 | −0.18 | +0.01 | +0.02 | +0.47 (−0.27 to +1.27) |
| 4074.5–4893.0 | \(\mathrm{C}_2\) 4668, \(\mathrm{H}\beta\) | 96 | −0.12 | +0.01 | +0.01 | +0.28 (−0.34 to +0.90) |
| 4074.5–5207.9 | \(\mathrm{C}_2\) 4668, \(\mathrm{H}\beta\), Fe5015, Mg b | 46 | −0.16 | −0.96 | +0.21 | +2.15 (+0.45 to +3.78) |

- \([\alpha/\mathrm{Fe}]\) drops whichever way the window grows, so the low \([\alpha/\mathrm{Fe}]\) is not one bad band.
- Age moves only when the Fe5015 and Mg b region (4893–5208 Å) comes in. Those fits are 0.96 Gyr younger and 0.21 dex more metal-rich.
- Only galaxies at \(z\le0.750\) cover that region (46 of the 110). Their ages drop and the slope flattens.
- Not isolated: the 54 galaxies without Mg b are 0.84 Gyr younger in full-spectrum fits than on the common window. The extensions to 3743 Å and 4893 Å move their ages by +0.01 and +0.06 Gyr. The pixels responsible are bluer than 3743 Å or redder than 4893 Å.

### All 135 galaxies, full spectrum

| Setup | Galaxies | Slope | 16–84% | Expected |
| --- | --- | --- | --- | --- |
| Normal model | 135 | −1.55 | −2.23 to −0.88 | −5.17 |
| Carbon mask (CN4150, G4300, Fe4383, \(\mathrm{C}_2\) 4668) | 135 | −2.72 | −3.40 to −2.04 | −5.17 |
| Carbon and nitrogen free | 135 | +0.97 | +0.20 to +1.75 | −5.17 |
| Same, \([\alpha/\mathrm{Fe}]\) fixed at +0.25 | 135 | +1.18 | +0.42 to +1.95 | −5.17 |
| Same, every galaxy on 4155.0–4438.1 Å | 130 | −3.77 | −4.42 to −3.09 | −5.19 |

- Freeing carbon and nitrogen raises median \([\alpha/\mathrm{Fe}]\). The 61 galaxies with Mg b in range go from +0.08 to +0.21. The 74 without go from −0.16 to −0.05.
- It also opens an age gap at fixed redshift: the Mg b group is 0.99 Gyr (0.79 to 1.19) younger. The Mg b group sits at lower redshift, so the gap flips the slope positive.
- With that step fitted alongside, the slope is −2.18 (−3.10 to −1.27).
- Cutting the 61 Mg b galaxies at 5144 Å lowers their \([\alpha/\mathrm{Fe}]\) by 0.11 (normal model) or 0.22 (carbon and nitrogen free).

### Carbon and nitrogen

- **Mocks, normal model:** truth is \([\alpha/\mathrm{Fe}]\) +0.2 and age 3.59 Gyr. Carbon +0.15 dex lowers fitted \([\alpha/\mathrm{Fe}]\) by 0.11 and raises age by 0.60 Gyr. Carbon +0.30 gives −0.25 and +0.91 Gyr. Nitrogen +0.30 gives −0.06 and −0.86 Gyr.
- **Mocks, carbon and nitrogen free:** \([\alpha/\mathrm{Fe}]\) comes back within 0.004 with Mg b in range and within 0.020 without.
- **Mocks, carbon mask:** the bias stays. At carbon +0.30 and nitrogen +0.60 it is −0.33 masked against −0.34 unmasked.
- **Real spectra, 61 galaxies with Mg b:** freeing carbon and nitrogen moves the CN4150 pull from −1.68 to −0.54. \(\mathrm{C}_2\) 4668 goes from −5.20 to −5.56. G4300 is already too strong: +1.74 before, +1.83 after.
- Theoretical models give weaker \(\mathrm{C}_2\) 4668 than MILES spectra ([Park et al. 2025](papers/spectral%20fitting/Alpha-MC%20-%20Self-consistent%20Alpha-enhanced%20Stellar%20Population%20Models%20Covering%20a%20Wide%20Range%20of%20Age,%20Metallicity,%20and%20Wavelength.pdf), §3.3.2).
- Mg b plus the four carbon bands hold 7.5% of the \(\chi^2\) excess of the 135 normal-model fits. 92.5% is elsewhere.

### Which pixels set \([\alpha/\mathrm{Fe}]\) and age

Linear response at the posterior medians, five test galaxies with Mg b, normal model. Push: the linearised shift that each region gives \([\alpha/\mathrm{Fe}]\).

| Part of spectrum | Share of data information on \([\alpha/\mathrm{Fe}]\) | Push on \([\alpha/\mathrm{Fe}]\) (dex) |
| --- | --- | --- |
| Mg b | 20.0% | +0.060 |
| CN4150, G4300, Fe4383, \(\mathrm{C}_2\) 4668 | 20.9% | −0.067 |
| Spectrum outside the defined features | 40.3% | +0.006 |

- Age: the star-formation-history prior carries 67% of the information. Of the data's share, Mg b carries 1.3% and the four carbon bands 37%.

### Mock chronometer

Ten test galaxies, three noise seeds each, one formation time. True slope −5.24. Ranges are 95% galaxy bootstrap. Injected mocks have carbon +0.15 and nitrogen +0.30 dex.

| Mock | Fit | Window (Å) | Slope | 95% | \([\alpha/\mathrm{Fe}]\) bias |
| --- | --- | --- | --- | --- | --- |
| Model matches | Normal | Full spectrum | −5.63 | −6.30 to −3.41 | −0.01 |
| Injected | Normal | Full spectrum | −5.94 | −6.99 to −3.34 | −0.21 |
| Injected | Carbon and nitrogen free | Full spectrum | −5.49 | −6.42 to −3.86 | −0.01 |
| Model matches | Normal | 4155.0–4438.1 | −3.41 | −4.31 to −0.93 | +0.01 |
| Injected | Normal | 4155.0–4438.1 | −4.35 | −6.04 to −2.33 | −0.21 |
| Model matches | Normal | 4074.5–4666.1 | −4.54 | −5.53 to −3.29 | +0.02 |
| Injected | Normal | 4074.5–4666.1 | −4.08 | −5.82 to −2.49 | −0.16 |
| Injected | Carbon and nitrogen free | 4074.5–4666.1 | −3.55 | −4.44 to −1.86 | +0.03 |

- Full-spectrum mock ages come out 0.57 Gyr too old in the lower-redshift half and 0.54 Gyr in the upper half. Both ends shift by the same amount, so the slope does not change.
- A wider prior (Student-t scale 1.0 instead of 0.3) lowers the offset to 0.23 and 0.32 Gyr. The prior alone has a slope of −2.28.
- On 4074.5–4666.1 Å the mocks turn a true −5.24 into −4.54. The real galaxies give −4.60 there.
- With carbon and nitrogen free on that window the mocks give −3.55. The real galaxies give −5.37.

### Oldest galaxies only

Common-window fits, normal model, 110 galaxies, expected −5.31. Each slope goes through the oldest fraction of every redshift bin.

| Oldest fraction | 4 bins | 5 bins | 6 bins |
| --- | --- | --- | --- |
| Half | −3.82 | −4.70 | −4.60 |
| Third | −4.83 | −4.19 | −5.71 |
| Quarter | −4.98 | −4.92 | −6.21 |
| Fifth | −4.91 | −5.94 | −6.78 |

- All twelve 16–84% ranges contain the expected −5.31.
- Their half-widths are 1.1 to 2.2, against 1.0 for the all-galaxy slope: no gain in precision with 110 galaxies.
- Each point is set by 4 to 14 galaxies.

### Limits

- **Prior:** window fits lean on the prior more. The posterior age width is 1.29 times the full-spectrum width for the same galaxy.
- **\([\alpha/\mathrm{Fe}]\) without Mg b:** the +0.21 comes from a window without Mg b. Mocks that match the model recover \([\alpha/\mathrm{Fe}]\) there (+0.02). Mocks with extra carbon and nitrogen come out 0.16 low.
- **Precision:** the slope range is about ±1.0, which gives \(H=123\) (102–158) \(\mathrm{km\,s^{-1}\,Mpc^{-1}}\) for the normal model.
- **Mg b window:** a common window that includes Mg b (4074.5–5207.9 Å) keeps 46 galaxies at \(z\le0.750\). It gives −7.23 (−9.91 to −4.43) against −5.92 expected.

## Your words

```json
[
  {
    "date": "2026-11-10",
    "text": "fundamentally i'm not getting the alpha/fe i expect from my fits, it's too low because Mg b is not being predicted correctly, but i can't seem to do much about it because that's just how the full spectrum fitting is and if i keep masking arbitrary bands there may as well be no benefit to doing full spectrum fitting. and somewhere along the way this is messing with age so i'm not seeing the overall hubble constant age results i want from the cosmic chronometer"
  }
]
```

## References

- Real galaxies, 135-galaxy arms, common windows and window extensions: [REPORT.md](results/chronometer-135-2026-11-10/REPORT.md), sections "Age–redshift slope", "Rest-frame windows" and "Window extensions".
- Fitted rest-frame and observed ranges: [per-fit.csv](results/chronometer-135-2026-11-10/per-fit.csv), columns `fit_rest_min`, `fit_rest_max` and `z` of the 135 normal-model fits.
- Carbon and nitrogen mocks, residual pulls, \(\chi^2\) excess, linear response, prior slope and mock chronometer: [REPORT.md](results/cn-response-2026-11-10/REPORT.md), experiments 4 and 6 to 11.
- Oldest galaxies: [REPORT.md](results/oldest-envelope-2026-11-11/REPORT.md), "Grid, own valid fits". Ranges: [envelope-slopes.csv](results/oldest-envelope-2026-11-11/envelope-slopes.csv).
- \(H=-977.79/((1+z)\,\mathrm{slope})\) \(\mathrm{km\,s^{-1}\,Mpc^{-1}}\): [Jimenez & Loeb 2002](https://arxiv.org/abs/astro-ph/0106145), eq. 2.
- [Park et al. 2025](papers/spectral%20fitting/Alpha-MC%20-%20Self-consistent%20Alpha-enhanced%20Stellar%20Population%20Models%20Covering%20a%20Wide%20Range%20of%20Age,%20Metallicity,%20and%20Wavelength.pdf), §3.3.2.
