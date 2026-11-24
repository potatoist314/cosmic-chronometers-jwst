---
title: Spectral masks in the chronometer fits
date: 2026-11-24
section: Masking
theme: Model and code reference
tags: [mask, chronometer, legac-dr3, sdss-dr17, ceridwen]
job: t_1f2c8d13
---

Pixels removed from each chronometer fit (2026-11-24). Rest wavelengths are vacuum. Line masks span the centre ± 1500 km/s. Windows: SDSS DR17 3604.0–7079.3 Å, LEGA-C DR3 4074.5–4666.1 Å. \(\mathrm{H}\beta\), [O II] and [O III] stay unmasked.

| Mask | Range | Surveys | Physical reason | Source |
| --- | --- | --- | --- | --- |
| Flagged pixels | LEGA-C: `QUAL` = 1 or error = 0. SDSS: `IVAR` = 0 or BRIGHTSKY. | LEGA-C DR3, SDSS DR17 | LEGA-C: imperfect sky subtraction. SDSS: very bad conditions, or sky above flux + 10 × error. | LEGA-C DR3 release description (ESO), Data Format. [SDSS DR17 SPPIXMASK](https://www.sdss4.org/dr17/algorithms/bitmasks/). |
| Telluric band | 7590–7660 Å observed, air (7592.09–7662.11 Å vacuum) | LEGA-C DR3, SDSS DR17 | \(\mathrm{O}_2\) A band of the atmosphere | van der Wel et al. 2021, [arXiv:2108.00744](https://arxiv.org/abs/2108.00744), §2.2.2 |
| Ca II K | 3915.08–3954.46 Å rest | SDSS DR17. LEGA-C DR3 in the window from 3850.0 Å. | Liu Hao, 2026-09-30: "i was told to mask all Ca". The grid ties Ca to \([\alpha/\mathrm{Fe}]\). In early-type galaxies "Ca tracks Fe". Park et al. 2025: "Since our \(\alpha\)-enhanced models do not track individual \(\alpha\) abundances, one should be careful in fitting spectra including Ca indices." | [e-mask-all-ca](/e/e-mask-all-ca/). Park et al. 2025, ApJ 994:165, [doi:10.3847/1538-4357/ae0cba](https://doi.org/10.3847/1538-4357/ae0cba), §2.1, §2.4. Conroy, Graves & van Dokkum 2014, [arXiv:1303.6629](https://arxiv.org/abs/1303.6629), §5.2. |
| Ca II H | 3946.75–3993.18 Å rest. Contains \(\mathrm{H}\varepsilon\) 3971.20 Å and [Ne III] 3968.65 Å. | As Ca II K | As Ca II K | As Ca II K. \(\mathrm{H}\varepsilon\): NIST ASD. [Ne III]: FSPS `emlines_info.dat`. |
| Ca I 4227 | 4206.77–4249.07 Å rest | LEGA-C DR3, SDSS DR17 | As Ca II K. Jonah Powley, 2026-09-17: "Ca I can be masked because of potential IGM contamination". Ca4227 in the grid grows much stronger with \([\alpha/\mathrm{Fe}]\). Park et al. 2025: "Since our \(\alpha\)-enhanced models do not track individual \(\alpha\) abundances, one should be careful in fitting spectra including Ca indices." | [e-mask-all-ca](/e/e-mask-all-ca/). Park et al. 2025, §2.4, §3.2.3. |
| Na D | 5878.50–5911.01 Å rest (Lick band, 5876.875–5909.375 Å air) | SDSS DR17 | Liu Hao, 2026-11-24: "okay, mask na d". No free Na in the model. \([\mathrm{Na/Fe}]\) is −0.16 to +0.43 in early-type galaxies. Interstellar gas absorbs at 5895 Å. Data below model in 49 of 49 SDSS fits. | Conroy, Graves & van Dokkum 2014, §5.2. Trager et al. 1998, [arXiv:astro-ph/9712258](https://arxiv.org/abs/astro-ph/9712258), Table 2. `results/sdss-mask-nad-2026-11-24`. |
