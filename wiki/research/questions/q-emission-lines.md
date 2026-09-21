---
kind: question
id: q-emission-lines
title: Should the fits model, mask or ignore emission lines, and on what physical grounds?
date: 2026-09-21
origin: new
status: open
---

## Context

The open decision is whether the Ceridwen fits model, mask or ignore emission lines, on a physically justified reason. It is not decided.

### What the fits do now

- The production fit masks velocities within 1500 kilometres per second on either side of \([\mathrm{O\,II}]\) at 3726 and 3729 \(\text{\AA}\), \(\mathrm{H}\beta\), and \([\mathrm{O\,III}]\) at 4959 and 5007 \(\text{\AA}\).
- Nebular emission is switched off in the production fit.
- The sample cut keeps galaxies whose \([\mathrm{O\,II}]\) and \([\mathrm{O\,III}]\) equivalent widths are both below three times their uncertainty.
- Of the 187 fitted galaxies, 154 have neither an \([\mathrm{O\,II}]\) nor an \([\mathrm{O\,III}]\) equivalent width in the catalogue.
- A blank equivalent width passes the sample cut.

### What the catalogue shows

- The 187 fitted galaxies were matched to the DR2 catalogue by spectrum identifier.
- The equivalent widths of \(\mathrm{H}\beta\), \(\mathrm{H}\gamma\) and \(\mathrm{H}\delta\) emission come from the LEGA-C team's joint fit of stellar templates and gas lines, described in section 3.1 of Straatman et al. 2018.
- Negative equivalent widths indicate emission.
- Each Balmer value measures what remains after the stellar model, according to the ESO DR2 release description reported in Liu Hao's brief (unverified: the release description was not read).
- Each Balmer value therefore depends on the absorption depth in that stellar model (unverified).
- This model dependence makes the Balmer measurements partly circular as evidence (unverified).
- The catalogue lists a line only where its search found one.
- All line counts are therefore lower limits.
- At \(3\sigma\) or more, 2 galaxies have \(\mathrm{H}\beta\) emission, 7 have \(\mathrm{H}\gamma\) emission and 13 have \(\mathrm{H}\delta\) emission.
- M13_253688 has a \(\mathrm{H}\beta\) equivalent width of \(-5.8\,\text{\AA}\) at \(z = 0.84\).
- M15_89153 has a \(\mathrm{H}\beta\) equivalent width of \(-8.1\,\text{\AA}\) at \(z = 0.84\).
- \(\mathrm{H}\beta\) leaves the LEGA-C wavelength range above approximately \(z = 0.8\).
- The counts were therefore repeated for galaxies whose spectra cover all three Balmer lines.
- Of the 187 galaxies, 117 have a catalogued uncertainty for all three lines.
- These 117 galaxies span \(z = 0.60\) to \(z = 0.89\).
- Among these galaxies, 2 have \(\mathrm{H}\beta\) emission at \(3\sigma\) or more, 5 have \(\mathrm{H}\gamma\) emission and 10 have \(\mathrm{H}\delta\) emission.
- Requiring all three Lick indices instead gives 129 galaxies.
- Among these 129 galaxies, 2 have \(\mathrm{H}\beta\) emission at \(3\sigma\) or more, 7 have \(\mathrm{H}\gamma\) emission and 13 have \(\mathrm{H}\delta\) emission.
- Both galaxies with \(\mathrm{H}\beta\) emission have \(\mathrm{H}\gamma\) and \(\mathrm{H}\delta\) below \(3\sigma\).
- In the 10 galaxies with \(\mathrm{H}\delta\) emission, the catalogued \(\mathrm{H}\beta\) emission is between \(0.00\) and \(0.44\,\text{\AA}\), or blank.
- Recombination physics fixes the Balmer line ratios.
- For Case B, the \(\mathrm{H}\gamma\) flux is about 0.47 times the \(\mathrm{H}\beta\) flux (unverified: textbook value).
- For Case B, the \(\mathrm{H}\delta\) flux is about 0.26 times the \(\mathrm{H}\beta\) flux (unverified: textbook value).
- Real gas therefore makes \(\mathrm{H}\beta\) the easiest Balmer line to detect.
- The catalogue shows the reverse order, which points to stellar-template mismatch rather than gas.
- Equivalent-width ratios differ from flux ratios by the ratio of the continuum levels.

### What is model-free

- \([\mathrm{O\,II}]\) and \([\mathrm{O\,III}]\) are nearly independent of the stellar model because stars produce little absorption at those wavelengths.
- These lines bound \(\mathrm{H}\beta\) emission through an empirical ratio.
- Trager et al. 2000a give \(\mathrm{H}\beta\) emission as about 0.6 times \([\mathrm{O\,III}]\) at \(5007\,\text{\AA}\), with a ratio ranging from 0.33 to 1.25.

### What Ceridwen's NebularModel can and cannot do

- Ceridwen has a nebular emission model.
- Ceridwen's nebular model is switched off in the production fits.
- It uses the CLOUDY tables that ship with FSPS.
- The MIST tables contain 11 metallicities, 10 ages and 7 ionisation parameters.
- The FSPS documentation says Nell Byler computed the tables.
- Liu Hao's brief attributes the tables to Byler et al. 2017 (unverified: the paper was not read).
- The tables describe young star clusters ionised by young massive stars (unverified: the paper was not read).
- The tables contain no post-AGB stars and no other old-star (LIER-type) ionising source (unverified: the paper was not read).
- The ages in the local MIST tables were read directly.
- The continuum table spans 0.5 to 20 million years.
- The line table spans 1 to 20 million years.
- The maximum age is 20 million years, not approximately 10 million years.
- The model gives emission only to stellar populations whose ages lie within the table range.
- The model stops with an error if any population older than 320 million years is marked as young.
- Old populations therefore cannot carry emission in this model.
- Switching the model on cannot produce emission from old stars.
- Fitting any Balmer emission with this model requires adding young stars.
- Adding those young stars biases the star-formation history and the age.
- The modelling option therefore means new tables with an old-star ionising source or an empirical Gaussian line model, rather than Ceridwen's existing nebular model.

### The no-mask fit

- A fit of M1_210210 without the emission-line mask is running under the record e-no-emission-mask.
- This fit compares the Ceridwen model with itself under two masks.
- This fit does not compare the model with the truth.
- An earlier test recorded as e-emission-mask widened the mask to include \([\mathrm{Ne\,III}]\), \(\mathrm{H}\epsilon\), \(\mathrm{H}\delta\) and \(\mathrm{H}\gamma\).

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
  },
  {
    "date": "2026-09-21",
    "text": "but does the model account for AGB ionisation, or just the classic UV ionisation",
    "display_text": "But does the model account for AGB ionisation, or just the classic UV ionisation?"
  },
  {
    "date": "2026-09-21",
    "text": "very annoying - add this new info to the wiki",
    "display_text": "Very annoying - add this new info to the wiki."
  }
]
```

## References

- [weak-emission-quiescent](wiki/notes/weak-emission-quiescent.md)
- [e-weak-emission-literature](wiki/research/experiments/e-weak-emission-literature.md)
- [e-emission-mask](wiki/research/experiments/e-emission-mask.md)
- [e-no-emission-mask](wiki/research/experiments/e-no-emission-mask.md), `results/no-emission-mask`
- Catalogue: `data/raw/legac_dr2/legaCdr2.fits.gz`, columns `Hb_EW`, `Hg_EW`, `Hd_EW`, `OII_3727_EW`, `OIII_5007_EW` and their `_err`; matched on `SPECT_ID` to `spect_id` in `results/dr2-quiescent-new-defaults-summary.csv`
- Sample cut: `scripts/absorption_mask_analysis.py:71-75`
- Nebular model: `ceridwen/ceridwen/neb/NebularGridModel.py:355-380`, `young_mask`, `RuntimeError` above 3.2e8 yr
- CLOUDY tables: `external/fsps/nebular/ZAU_ND_mist.cont`, `external/fsps/nebular/ZAU_ND_mist.lines` (`$SPS_HOME/nebular`); `external/fsps/README.md`
- Straatman+2018, [arXiv:1809.08236](https://arxiv.org/abs/1809.08236), section 3.1; Trager+2000a, [arXiv:astro-ph/0001072](https://arxiv.org/abs/astro-ph/0001072)
- Roadmap task `emission-lines-model-mask-ignore`, [direction](wiki/research/direction.md)

## Decisions

```json
[]
```
