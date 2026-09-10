# Themes

## Single-fit accuracy

Which fitting choices improve individual galaxy estimates?

| experiment | arm | status | result | note |
| --- | --- | --- | --- | --- |
| Generation 1 | `baseline` | dropped | M4_108989 photometric χ² was 139.1 with order 0 and cosmos_ap3 | calibration-polynomial-dr2 |
| Generation 1 | `poly3` | dropped | M4_108989 photometric χ² was 152.6 with order 3 and cosmos_ap3 | calibration-polynomial-dr2 |
| Generation 1 | `poly3_total` | adopted | M4_108989 photometric χ² fell to 12.8 with order 3 and cosmos_total | calibration-polynomial-dr2 |
| Tilt origin | `tilt-origin` | inconclusive | Corrected aperture photometry shifted M4 tilt from −20% to +0.4% | ceridwen-results |
| Generation 2 | `seed_rep1-3` | inconclusive | Age scatter reached 1.20 reference posterior half-widths across six repeats | fit-accuracy-knobs |
| Generation 2 | `floor20` | dropped | M12_98104 f_calib rose from 9.98% to 14.59% with negligible physics shifts | fit-accuracy-knobs |
| Generation 2 | `dust_free` | adopted | Median photometric χ² fell by 10.7 | fit-accuracy-knobs |
| Generation 2 | `no_irac` | dropped | M5_173928 remaining-band χ² worsened by 87 | fit-accuracy-knobs |
| Generation 2 | `mask_cn` | dropped | Mean absolute Lick residual rose from 2.31σ to 2.47σ | fit-accuracy-knobs |
| Generation 2 | `sfh_cont` | adopted | Age uncertainties widened three to six times for implausibly tight uniform-prior fits | fit-accuracy-knobs |
| Generation 2 | `emis_wide` | dropped | M4_108989 age shifted 13.7 reference half-widths after masking Balmer lines | fit-accuracy-knobs |
| Redshift and dispersion | `zsig` | dropped | Only M5_173928 dust shifted by more than 1σ among physical parameters | redshift-sigma-wiggle |
| Generation 3 | `new_default` | adopted | Median age increased by 1.23 Gyr across 187 galaxies | dr2-new-defaults |
| Generation 3 | `new_default_rep1-2` | inconclusive | Age scatter reached 0.34 reference posterior half-widths across four repeats | fit-accuracy-knobs |
| Generation 3 | `tau_cn` | dropped | Every physics shift stayed at or below 0.5 posterior half-widths | fit-accuracy-knobs |
| Generation 3 | `dust_wide` | dropped | M1_206545 dust index followed the widened bound from −0.99 to −1.90 | fit-accuracy-knobs |
| Absorption-line mask | `features` | dropped | M5_172669 log Z shifted −21.7 full-spectrum σ | absorption-line-mask |
| Absorption-line mask | `features_downweight` | dropped | M5_172669 log Z shifted −21.8 full-spectrum σ | absorption-line-mask |

## Validation on mocks

Do fitted parameters recover known injected values?

| experiment | arm | status | result | note |
| --- | --- | --- | --- | --- |
| Tilt recovery | `mock_tilt4_baseline` | dropped | Recovered dust optical depth was 0.151 ± 0.004 against truth 0.011 | calibration-polynomial-dr2 |
| Tilt recovery | `mock_tilt4_poly3` | adopted | Recovered dust optical depth was 0.023 ± 0.016 against truth 0.011 | calibration-polynomial-dr2 |
| SFH recovery | `mock_tilt4_sfh_cont` | inconclusive | Recorded age pull increased from 0.64 to 1.82 under the continuity prior | fit-accuracy-knobs |
| New-default recovery | `mock_tilt4_new_default` | planned | Two attempts aborted before sampling because mock truth lacked diffuse_dust_index | fit-accuracy-knobs |
| Absorption-mask mocks | `mask mock grid` | dropped | Masked modes retained tilt bias across the 36-fit grid | absorption-line-mask |
| Injection recovery | — | planned | full-sample injection test not yet run | |

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