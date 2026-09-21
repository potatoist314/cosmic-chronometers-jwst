---
kind: question
id: q-emission-lines
title: Should the fits model, mask or ignore emission lines, and on what physical grounds?
date: 2026-09-21
origin: new
status: open
---

## Context

- Open decision: model, mask or ignore emission lines in the Ceridwen fits; physically justified reason required; not decided.
- Current state: mask of \(\pm1500\,\mathrm{km\,s^{-1}}\) around \([\mathrm{O\,II}]\) \(3726,3729\), \(\mathrm{H}\beta\), \([\mathrm{O\,III}]\) \(4959,5007\); nebular emission off in the production fit.
- Model option: `ceridwen.neb.NebularModel`; FSPS-style CLOUDY-grid model scaled by ionising photon rate \(Q\) from stellar ages inside the CLOUDY age grid; unused in the production notebook; no other emission-line model found in `ceridwen/ceridwen`.
- DR2 catalogue: 187 fitted galaxies matched by `SPECT_ID`; `Hb_EW`, `Hg_EW`, `Hd_EW` emission-line equivalent widths from the LEGA-C joint stellar-plus-gas pPXF fit (Straatman+2018, section 3.1); negative values indicate emission.
- At \(|\mathrm{EW}/\mathrm{err}|\geq3\): \(\mathrm{H}\beta\), 2 galaxies (`M13_253688` \(-5.8\,\text{\AA}\), `M15_89153` \(-8.1\,\text{\AA}\)); \(\mathrm{H}\gamma\), 7; \(\mathrm{H}\delta\), 13. Catalogue entries only where the line search found a line; counts are lower limits.
- 154 of 187 galaxies: neither an \([\mathrm{O\,II}]\) nor an \([\mathrm{O\,III}]\) equivalent width; blank values pass the \(|\mathrm{EW}/\sigma_{\mathrm{EW}}|<3\) sample cut.
- Balmer emission equivalent widths: residuals after the LEGA-C stellar-template fit; dependent on its stellar model’s Balmer absorption depth; model-dependent, not direct (ESO DR2 release description; attribution from Liu Hao’s brief, source not read here). Much weaker dependence for \([\mathrm{O\,II}]\) and \([\mathrm{O\,III}]\); little stellar absorption at those wavelengths.

Independence of the evidence, from the 2026-09-21 chat explanation:

- (1) DR2 Balmer-emission EWs: partly circular, dependent on LEGA-C stellar-model Balmer absorption depths.
- (2) \([\mathrm{O\,II}]\)/\([\mathrm{O\,III}]\): nearly model-free, little stellar absorption; empirical \(\mathrm{H}\beta\) bound: approximately \(0.6\times[\mathrm{O\,III}]\,5007\), range \(0.33–1.25\) (Trager+2000a).
- (3) Recombination-fixed Case B ratios: \(\mathrm{H}\gamma/\mathrm{H}\beta\approx0.47\), \(\mathrm{H}\delta/\mathrm{H}\beta\approx0.26\) (textbook, unverified); gas: \(\mathrm{H}\beta\) easiest to detect.
- (4) \(|\mathrm{EW}/\mathrm{err}|\geq3\): \(\mathrm{H}\delta/\mathrm{H}\gamma/\mathrm{H}\beta\) counts \(13/7/2\); reverse order, suggesting stellar-template mismatch over gas, subject to recount.
- (5) No-mask Ceridwen fit: self-test, not truth-test.
- Recount: fitted galaxies with catalogued EW_err for \(\mathrm{H}\beta\), \(\mathrm{H}\gamma\), \(\mathrm{H}\delta\): \(117\) of \(187\), \(z=0.60–0.89\); respective counts \(2/5/10\).
- Coverage by all three Lick indices present: \(129\); respective counts \(2/7/13\).
- \(2\) \(\mathrm{H}\beta\) detections (M13_253688, M15_89153, \(z=0.84\)): \(\mathrm{H}\gamma\) and \(\mathrm{H}\delta\) below \(3\sigma\).
- \(10\) \(\mathrm{H}\delta\) detections: catalogued \(\mathrm{H}\beta\) emission \(0.00–0.44\,\text{\AA}\) or blank.
- EW versus flux ratios: continuum-ratio factor.

## Your words

```json
[
  {
    "date": "2026-09-21",
    "text": "okay, add this to one of the research priorities on the wiki, priority of 9, to either model, mask, or ignore emission lines, but with a physically justified reason.",
    "display_text": "Okay, add this to one of the research priorities on the wiki, priority of 9: to either model, mask, or ignore emission lines, but with a physically justified reason."
  },
  {
    "date": "2026-09-21",
    "text": "this seems really circular? using a model to decide what a sed model should do? or is there some independence i'm not seeing here",
    "display_text": "This seems really circular? Using a model to decide what an SED model should do? Or is there some independence I'm not seeing here?"
  },
  {
    "date": "2026-09-21",
    "text": "ugh. add this explanation to the wiki priority 9 item.",
    "display_text": "Ugh. Add this explanation to the wiki priority 9 item."
  }
]
```

## References

- [weak-emission-quiescent](wiki/notes/weak-emission-quiescent.md)
- [e-weak-emission-literature](wiki/research/experiments/e-weak-emission-literature.md)
- [e-emission-mask](wiki/research/experiments/e-emission-mask.md)
- [e-no-emission-mask](wiki/research/experiments/e-no-emission-mask.md), `results/no-emission-mask`
- `ceridwen/ceridwen/neb/NebularGridModel.py`
- `scripts/absorption_mask_analysis.py:71-75`
- Roadmap task `emission-lines-model-mask-ignore`, [direction](wiki/research/direction.md)

## Decisions

```json
[]
```
