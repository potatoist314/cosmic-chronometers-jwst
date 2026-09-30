---
kind: experiment
id: e-mask-all-ca
title: M1_210210 with every Ca feature masked
date: 2026-09-30
results_at:
origin: new
status: planned
question: q-dust-index-railing
related_questions: q-fitting-choices
follow_up:
features: emission_lines, ssp_grid
finding: M1_210210 neb_maskca: model Ca II K / H deeper than the data by 18.8% / 14.9% at the unfitted pixels within ±7 Å; alpha-MC [alpha/Fe] scales Ca with Mg, so [Ca/Fe] = [Mg/Fe]; host-ISM Ca II absorption has the opposite sign; all-Ca mask fit not run
---

## Context

M1_210210, LEGA-C DR2, \(z_{\mathrm{cat}} = 0.6542\). Fitted rest-frame range 3747.6–5220.2 Å (observed 6199–8635 Å). All wavelengths below vacuum unless marked air.

Grid `amist_c3k_hr_krou_afe`: α-MC (Park et al. 2025, arXiv:2410.21375, Sec. 1). The \([\alpha/\mathrm{Fe}]\) axis scales O, Ne, Mg, Si, S, Ar, Ca and Ti uniformly at fixed \([\mathrm{Fe}/\mathrm{H}]\); model \([\mathrm{Ca}/\mathrm{Fe}] = [\mathrm{Mg}/\mathrm{Fe}]\). Conroy, Graves & van Dokkum 2014 (arXiv:1303.6629, Sec. 5.2), SDSS early-type galaxy stacks: "Ca tracks Fe closely over the full sample".

Arm `neb_maskca` of `e-nebular-grid` masks Ca II K 3934.77 Å and Ca II H 3969.59 Å at ±1500 km/s. At those unfitted pixels, summed (observed − posterior-median model)/model within ±7 Å rest of each centre: +18.8% (K), +14.9% (H). Model lines deeper than data. Source: `results/m1-210210-nebular-2026-09-30/run/fits/neb_maskca/210210-M1_210210/ceridwen_derived_outputs.h5`; datasets `spectrum/observed` and `spectrum/posterior_q50`.

Same ratio in velocity shells \(|\Delta v|\) 0–500 / 500–1000 / 1000–1500 km/s: K +19.4% / +4.0% / +0.5%; H +15.5% / +4.7% / +1.7%. In 1500–2000 km/s: K −1.0%, H −0.7%. Arm `neb` (Ca fitted): same ±7 Å ratio +1.6% (K), +7.5% (H).

Ca II absorption by gas in the galaxy adds to the observed stellar line; sign opposite to the residual. Sardane, Turnshek & Rao 2015 (arXiv:1504.02029, abstract): SDSS Ca II absorbers, sample threshold \(W_0(3934) \ge 0.16\) Å, two populations divided at 0.7 Å. Milky Way Ca II at observed 3934.77 and 3969.59 Å, outside the fitted observed range.

Hε 3971.20 Å (NIST ASD): 1.6 Å from Ca II H, inside the H window. K window: no Balmer line.

\([\mathrm{Ca}/\mathrm{Fe}]\) near solar while \([\mathrm{Mg}/\mathrm{Fe}]\) rises with \(\sigma\): Conroy, Graves & van Dokkum 2014 (arXiv:1303.6629, Sec. 5.2, Fig. 13); Johansson, Thomas & Maraston 2012 (arXiv:1112.0322, Sec. 5.9, Fig. 13; Sec. 7: flat, 0.1–0.2 dex below \([\mathrm{Mg}/\mathrm{Fe}]\)); Parikh et al. 2019 (arXiv:1812.02753, Sec. 4.3, Fig. 9: Ca follows Fe); Graves et al. 2007 (arXiv:0707.1523, abstract).

Beverage et al. 2023 (arXiv:2303.03412, Sec. 7): Mg enhanced, Si/Ca/Ti solar at \(z \sim 0.7\) and 0. Prochaska, Rose & Schiavon 2005 (arXiv:astro-ph/0509764, Sec. 6): Ca4227r index raises \([\mathrm{Ca}/\mathrm{Fe}]\) 0.3 dex; Lick Ca4227 CN-contaminated. Bensby et al. 2014 (arXiv:1309.2631, Fig. 15): MW \([\mathrm{X}/\mathrm{Fe}]\) plateaus. Iwamoto et al. 1999 (arXiv:astro-ph/0002337, Sec. 5, Table 3): SNIa W7 Si–Ca; SNII O/Mg-rich.

One \([\alpha/\mathrm{Fe}]\) axis scales \(\alpha\) elements for isochrone and opacity consistency: α-MC (arXiv:2410.21375, Sec. 2.1; Sec. 1 caveat); MILES (Vazdekis et al. 2015, arXiv:1504.08032, Sec. 2.3.2, +0.4); sMILES (Knowles et al. 2023, arXiv:2306.05942, Sec. 2.1.2, lockstep for atmosphere consistency). Separate Ca exists: TMJ11 index tables (arXiv:1010.4569, Sec. 3.5, \([\mathrm{X}/\alpha]\) including Ca); alf spectra (arXiv:1205.6473, Sec. 3).

Existing artefacts: alf code and models (github.com/cconroy20/alf; manual Sec. 1.1: ~100 CPU-hr per converged fit; continuum-normalized only); sMILES SSPs public (miles.iac.es) but lockstep; TMJ tables public (indices only); index analyses use Mgb plus Fe4383 without Ca (Bevacqua et al. 2023, arXiv:2308.03441).

That ISM term is small: quiescent \(A_V < 0.5\) (Kriek & Conroy 2013, arXiv:1308.1099); ISM Na D 0.1–0.5 Å at \(E(B-V)\) 0.02–0.05 against ~4 Å stellar (Poznanski et al. 2012, arXiv:1206.6107, Eq. 9); Ca II absorbers split at 0.7 Å with dust depletion (arXiv:1504.02029).

Jonah Powley meeting, 2026-09-17: “Ca I can be masked because of potential IGM contamination” (see References). The ISM check covers host-galaxy ISM absorption (sign, size) and Milky Way foreground position; it does not cover intervening IGM absorbers on the sightline.

## Before delegation

```json
[
  {
    "date": "2026-09-30",
    "text": "tell me more about Ca tracking Fe instead of being like other alpha elements. is this well known? if so, why does all the alpha enhanced ssp grids just treat it together?",
    "display_text": "Tell me more about Ca tracking Fe instead of being like other alpha elements. Is this well known? If so, why do all the alpha-enhanced SSP grids just treat it together?",
    "source_ref": "Relayed by the Astronomy lead"
  },
  {
    "date": "2026-09-30",
    "text": "what about the impact of ISM? someone mentioned Ca might be contaminated by ISM but they were very unsure",
    "display_text": "What about the impact of ISM? Someone mentioned Ca might be contaminated by ISM but they were very unsure.",
    "source_ref": "Relayed by the Astronomy lead"
  },
  {
    "date": "2026-09-30",
    "text": "i was told to mask all Ca",
    "display_text": "I was told to mask all Ca.",
    "source_ref": "Relayed by the Astronomy lead"
  }
]
```

## Execution plan

- Comparison: one new arm `neb_maskallca` for M1_210210 against `neb_maskca`.
- Baseline: same data, seed 20260927, 14 SFH bins; SFH-basis fast path on.
- Model: nebular grid `~/.ceridwen/grids/amist_c3k_hr_krou_afe_nebular.h5`; priors `diffuse_delta` Uniform(−3, 0.4) and `diffuse_Ebump` Uniform(0, 12).
- Controlled change: `emission_lines = [3726.0, 3728.8, 3934.77, 3969.59, 4227.92, 4958.9, 5006.8]`. Notebook masks each entry at ±1500 km/s (`dv=1500.0`, cell 6). No code change.
- Mask list: NIST ASD vacuum wavelength; lower level; window. Ca II K 3934.77 Å; ground level; 3915.1–3954.5 Å.
- Mask list: Ca II H 3969.59 Å; ground level; 3949.7–3989.5 Å.
- Mask list: Ca I 4227.92 Å (4226.73 Å air); ground level; 4206.8–4249.1 Å. Window contains Lick Ca4227 band 4222.250–4234.750 Å air = 4223.44–4235.94 Å vacuum (Trager et al. 1998, arXiv:astro-ph/9712258, Table 2: measures Ca, (C)).
- Width: at \(\sigma = 263\) km/s, Gaussian FWHM 619 km/s, 8.1 Å at 3934.77 Å; ±1500 km/s is ±19.7 Å, \(\pm 5.7\sigma\). Shell ratios fall to +0.5% (K) and +1.7% (H) at 1000–1500 km/s.
- Fitted pixels: 3657 in `neb`; 3452 in `neb_maskca`; 3335 with the list above.
- Not in the list: Lick Ca4455 band 4452.125–4474.625 Å air = 4453.37–4475.88 Å vacuum. Trager et al. 1998 Table 2: measures (Fe), (C), Cr. Thomas, Maraston & Bender 2003 (arXiv:astro-ph/0209250, Sec. 3.1.3): "Ca4455 is insensitive to Ca abundance", with Fe and Cr the dominant contributors. Masking at ±1500 km/s about 4464.63 Å removes 123 more pixels.
- Not in the list: Ca I lines from excited levels, NIST ASD lower level 15,158–23,652 cm⁻¹: 4284.22–4319.86 Å (inside Lick G4300 band 4281.375–4316.375 Å air; Trager Table 2: measures C, (O)), 4426.68–4457.86, 4579.83–4587.25, 4879.49, 5043.03, 5190.30 Å.
- Not in the list: Ca II 3737.96 Å, lower level 25,414 cm⁻¹; centre below fitted range.
- Not in the list: Ca II triplet near 8500–8662 Å; outside fitted range.
- Hardware and outputs: Vast.ai RTX 5090, $1 cap; config `results/m1-210210-maskallca-2026-09-30/experiment.json` (not yet written); outputs under `results/m1-210210-maskallca-2026-09-30/run/fits/neb_maskallca/210210-M1_210210/`.
- Run command: `python3 scripts/experiment.py run results/m1-210210-maskallca-2026-09-30/experiment.json --gpu "RTX 5090" --output results/m1-210210-maskallca-2026-09-30/run`.

## Amendments

```json
[]
```

## Runs

```json
[
  {
    "id": "neb-maskallca-m1-210210",
    "arm": "neb_maskallca",
    "status": "planned"
  }
]
```

## Figures

```json
[]
```

## Measurements

## Results

## Caveats

## References

- [q-dust-index-railing](wiki/research/questions/q-dust-index-railing.md)
- [q-fitting-choices](wiki/research/questions/q-fitting-choices.md)
- [e-nebular-grid](wiki/research/experiments/e-nebular-grid.md)
- [Park et al. 2025](https://arxiv.org/abs/2410.21375)
- [Conroy, Graves & van Dokkum 2014](https://arxiv.org/abs/1303.6629)
- [Trager et al. 1998](https://arxiv.org/abs/astro-ph/9712258)
- [Thomas, Maraston & Bender 2003](https://arxiv.org/abs/astro-ph/0209250)
- [Sardane, Turnshek & Rao 2015](https://arxiv.org/abs/1504.02029)
- [NIST Atomic Spectra Database](https://physics.nist.gov/PhysRefData/ASD/lines_form.html)
- [Johansson, Thomas & Maraston 2012](https://arxiv.org/abs/1112.0322)
- [Parikh et al. 2019](https://arxiv.org/abs/1812.02753)
- [Beverage et al. 2023](https://arxiv.org/abs/2303.03412)
- [Graves et al. 2007](https://arxiv.org/abs/0707.1523)
- [Prochaska, Rose & Schiavon 2005](https://arxiv.org/abs/astro-ph/0509764)
- [Bensby et al. 2014](https://arxiv.org/abs/1309.2631)
- [Iwamoto et al. 1999](https://arxiv.org/abs/astro-ph/0002337)
- [Vazdekis et al. 2015](https://arxiv.org/abs/1504.08032)
- [Knowles et al. 2023](https://arxiv.org/abs/2306.05942)
- [Thomas, Maraston & Johansson 2011](https://arxiv.org/abs/1010.4569)
- [Conroy & van Dokkum 2012](https://arxiv.org/abs/1205.6473)
- [Poznanski, Prochaska & Bloom 2012](https://arxiv.org/abs/1206.6107)
- [Kriek & Conroy 2013](https://arxiv.org/abs/1308.1099)
- [Bevacqua et al. 2023](https://arxiv.org/abs/2308.03441)
- [alf](https://github.com/cconroy20/alf)
- [Meeting with Jonah Powley](wiki/notes/meeting-2026-09-17-jonah-powley.md)

## Your interpretation

```json
[]
```

## Next decision

```json
[]
```
