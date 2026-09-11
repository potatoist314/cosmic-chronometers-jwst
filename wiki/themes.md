# Themes

## Single-fit accuracy

Which fitting choices improve individual galaxy estimates?

### Calibration polynomial
note: calibration-polynomial-dr2

| arm | change | status | result |
| --- | --- | --- | --- |
| `baseline` | reference fit without spectrum shape correction | dropped | poor fit to the photometry |
| `poly3` | adds a smooth spectrum shape correction | dropped | poor fit to the photometry despite spectrum shape correction |
| `poly3_total` | adds shape correction and whole-galaxy photometry | adopted | has the best photometric fit in all six galaxies |

### Tilt origin
note: ceridwen-results

| arm | change | status | result |
| --- | --- | --- | --- |
| `tilt-origin` | corrects the photometry used to anchor spectra | inconclusive | corrected photometry removes tilt in only one tested galaxy |

### Fit-accuracy knobs
note: fit-accuracy-knobs

| arm | change | status | result |
| --- | --- | --- | --- |
| `seed_rep1-3` | repeats reference fits with different random seeds | inconclusive | repeated ages differ by up to 1.20 error bars |
| `floor20` | raises the allowed extra spectrum noise | dropped | inflates the error term without changing ages or metals |
| `dust_free` | dust curve slope left free | adopted | improves fit and evidence while shifting a physics parameter |
| `no_irac` | removes the two longest-wavelength photometry bands | dropped | worsens the fit to the remaining photometry |
| `mask_cn` | excludes carbon and nitrogen absorption regions | dropped | worsens agreement with measured absorption strengths |
| `sfh_cont` | favours smoother changes in star formation | adopted | widens implausibly narrow age error bars |
| `emis_wide` | excludes more regions around possible emission lines | dropped | removes information without fixing Balmer emission infill |
| `tau_cn` | favours moderate dust amounts over equal weighting | dropped | leaves physical estimates effectively unchanged |
| `dust_wide` | allows a wider range of dust slopes | dropped | drives dust slopes toward the new limit |
| `new_default_rep1-2` | repeats new defaults with different random seeds | inconclusive | repeated ages differ by up to 0.34 error bars |

### Free redshift and dispersion
note: redshift-sigma-wiggle

| arm | change | status | result |
| --- | --- | --- | --- |
| `zsig` | lets spectral line positions and widths vary | dropped | leaves ages and metals within their reference error bars |

### New defaults on the full sample
note: dr2-new-defaults

| arm | change | status | result |
| --- | --- | --- | --- |
| `new_default` | combines smoother star formation with free dust slope | adopted | gains stronger statistical support across the full sample |

### Absorption-line mask
note: absorption-line-mask

| arm | change | status | result |
| --- | --- | --- | --- |
| `features` | fits only regions around absorption lines | dropped | shifts metal estimates far beyond full-spectrum error bars |
| `features_downweight` | reduces weight outside absorption lines | dropped | shifts metal estimates far beyond full-spectrum error bars |

## Validation on mocks

Do fitted parameters recover known injected values?

### Tilt recovery
note: calibration-polynomial-dr2

| arm | change | status | result |
| --- | --- | --- | --- |
| `mock_tilt4_baseline` | fits an artificial tilt without shape correction | dropped | overestimates dust far beyond the error bar |
| `mock_tilt4_poly3` | adds shape correction to the tilted mock | adopted | recovers the injected dust within the error bar |

### SFH recovery
note: fit-accuracy-knobs

| arm | change | status | result |
| --- | --- | --- | --- |
| `mock_tilt4_sfh_cont` | favours smoother star formation in the tilted mock | inconclusive | worsens recovery on a mock favouring the reference assumptions |

### New-default recovery
note: fit-accuracy-knobs

| arm | change | status | result |
| --- | --- | --- | --- |
| `mock_tilt4_new_default` | applies both new defaults to the tilted mock | planned | cannot start without the injected dust curve slope |

### Absorption-mask mocks
note: absorption-line-mask

| arm | change | status | result |
| --- | --- | --- | --- |
| `mask mock grid` | varies absorption masks across artificial tilts and noise | dropped | retains tilt bias despite removing or reducing other pixels |

### Injection recovery

| arm | change | status | result |
| --- | --- | --- | --- |
| — | tests recovery of known inputs across the sample | planned | full-sample injection test not yet run |

## Sample and data

Which galaxies, spectra, and photometry enter the fits?

## Population results

How do inferred ages and assembly histories vary across galaxies?

## Compute

What resources and runtime do the fits require?

## Model and code reference

Which model assumptions, priors, and implementations define the fits?

## Background reading

Which published studies inform the models and comparisons?
