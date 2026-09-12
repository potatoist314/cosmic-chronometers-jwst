---
kind: experiment
id: e-quiescent-mock
title: Quiescent mock: agreed intrinsic parameters
date: 2026-09-12
origin: new
status: planned
question: q-mock-recovery
---

## Before delegation

```json
[
  {
    "date": "2026-09-12",
    "text": "let's setup a suite of mock/injections. before that, let's go through what this actually means at a granular level"
  },
  {
    "date": "2026-09-12",
    "text": "okay, let's decide on a theta true, and add redshift, broadening etc after. we can inject noise at varying amounts, 1%, 5%, 10%"
  },
  {
    "date": "2026-09-12",
    "text": "i just need you to give me a set of theta with a good physical explanation (eg most early passive quiescent galaxies are around this mass, etc.). keep the explanation in plain english, not a fan of the current style"
  },
  {
    "date": "2026-09-12",
    "text": "okay. i agree with this. save this in the wiki in the appropriate section"
  }
]
```

## Execution plan

### Approved intrinsic truth

Liu Hao approved this representative quiescent galaxy on 2026-09-12.
The values below specify the injected galaxy. Fitting priors remain undecided.

| Parameter | Value |
| --- | --- |
| logmass | 11.2 |
| Z | -1.75 |
| afe | 0.25 |
| logsfr_ratios | [0,0,0,0,-2.5,0,0] |
| diffuse_tau_kc | 0.15 |
| diffuse_dust_index | -0.5 |

### Physical explanation

A massive galaxy that formed about 160 billion solar masses of stars, slightly
more metal-rich than the Sun. Its alpha enhancement is close to the measured
LEGA-C quiescent average of 0.24. These are representative choices informed by
[Bevacqua et al. (2023), abstract and section 6](https://arxiv.org/abs/2308.03441)
and [Nersesian et al. (2025), section 5](https://arxiv.org/html/2502.03021v1).

It formed stars much more actively in the past, with negligible formation during
the last billion years: a simple old, passive galaxy. This history is our chosen
mock, not a measured population-average SFH.

A little remaining dust, with stronger attenuation toward the blue. The dust
values are reasonable examples given the low dust amounts and steeper curves
observed in quiescent LEGA-C galaxies
([Nersesian et al. 2025, sections 4.2 and 5](https://arxiv.org/html/2502.03021v1)).

### Parameter conventions and remaining choices

- logmass is log10 of total formed mass in solar masses, before stellar mass loss.
- Z is log10 absolute total metallicity: -1.75 means about 0.0178, or 1.25 times
  solar using Z_sun=0.0142. afe is [alpha/Fe] in dex.
- The current eight SFH nodes are [0, 0.03, 0.1, 0.3, 1, 3, 5, t_universe] Gyr
  before observation. Each logsfr_ratios entry is log10(SFR[i]/SFR[i+1]).
  The oldest node depends on the redshift, which remains to be chosen.
- Keep this intrinsic truth for the planned 1%, 5%, and 10% noise cases.
- Redshift, broadening, and the precise noise prescription remain undecided.
  The percentages do not yet specify the reference flux or affected observations.

## Runs

```json
[]
```

## References

- [Bevacqua et al. (2023): LEGA-C quiescent masses and alpha enhancement; abstract and section 6](https://arxiv.org/abs/2308.03441)
- [Nersesian et al. (2025): quiescent metallicity and dust; sections 4.2 and 5](https://arxiv.org/html/2502.03021v1)
- [Tacchella et al. (2022): Z_sun=0.0142 convention; section 3.1](https://arxiv.org/html/2102.12494)
- [Integrated fitting notebook: lookback_template and sfh_from_ratios](notebooks/ceridwen_integrated_photometry_spectra.ipynb)
- [SFH transform: logsfr_ratios_to_sfh](ceridwen/ceridwen/model/transforms.py)
