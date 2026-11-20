---
title: Meeting with Sandro
date: 2026-11-20
section: Meetings
theme: Population results
tags: [meeting, cosmic-chronometers, surveys, sfh-prior, ceridwen]
job: t_b2c873b9
---

[Original handwriting](/f/reports/meeting-2026-11-20-sandro.pdf) · [20 November 2026 check-in](/checkins/2026-11-20/)

<details open id="corrected-meeting-notes">
<summary>Meeting notes</summary>

### Mergers, ex-situ accretion and progenitor bias

- A star-formation history cannot fully model the effect of mergers.
- Stars can accrete from satellites or from the halo.
- \(f_{\text{ex-situ}}\) (stars accreted from external halos) reaches \(30\text{–}50\%\) today around \(10^{11}\,M_\odot\), very high for massive galaxies. At \(z \approx 1\), it is \(10\text{–}40\%\) (\(1/3\) accreted).
- Discuss \(f_{\text{ex-situ}}\) in the paper rather than modelling it.
- How does this change the progenitor bias?
- Cut by velocity dispersion (\(\sigma_\star\), cutoff 250) to select the most massive galaxies.
- Plot \(t_{50}\) against \(\sigma_\star\) and \(t_{80}\) against \(\sigma_\star\).

### Downsizing

- Downsizing is not physical and does not account for mergers.
- The mass-assembly figure by stellar mass matches existing literature and builds trust in the model.

### SDSS and cosmology

- Look at SDSS (\(z = 0\text{–}0.3\), most at \(z < 0.01\)) and its sub-surveys.
- The sub-surveys are IFU surveys, which get messy.
- SDSS has tens of thousands of clean passive galaxies. Start with an initial few to build the data pipeline.
- SDSS gives a low-redshift anchor to compare against \(H_0\).
- Look again into \(w_0 w_a\mathrm{CDM}\). Testing cosmological models requires multiple redshift ranges, because this models the evolution of \(H(z)\) over time.

### Surveys

- ★ SDSS (\(z = 0\text{–}0.3\)) and GAMA (\(z \approx 0.4\)): very cool.
- VANDELS (\(z \approx 1\text{–}1.5\)): nice to have.
- DJA (Dawn JWST Archive, NIRCam and NIRSpec data): could find quiescent galaxies there.
- The Ito and Baker papers already searched for quiescent galaxies (tens of galaxies). The Dawn Archive already aggregates Heavy Metal (tens of galaxies), EXCELS and Blue Jay.
- NIRSpec has prism (\(R \sim 100\)) and medium grating (\(R \sim 1000\)) modes. Many photometric observations exist, with few high-resolution spectra. Use medium grating only for JWST.
- MJ looks into systematics of 2–3 galaxies, though that is less important.
- Self-consistently fit one model across different redshift ranges with identical settings and the \(\alpha\)-enhanced grid. This is new.
- Survey order (not strict, pending suitability checks): SDSS, GAMA, JWST, then VANDELS.

### SFH bins and priors

- ★ Sandro asked about the number of SFH bins. Test more or finer bins on 10 test galaxies first to see whether the age slope or age systematics shift.
- Test how systematics change with different priors.
- In \(\log(\mathrm{SFR}_{i+1}/\mathrm{SFR}_i) = \mathrm{ST}(\mu, \sigma)\), the flat continuity prior sets \(\mu = 0\). Setting \(\mu = f(z)\) gives an ★ SFMS prior.
- The SFMS prior gives a more informed, physically more realistic constraint. It might help even as a systematic test. Liu Hao will ask other group members for it.

Summary of next work:

1. Run both priors to understand systematics. Sandro prefers the SFMS prior, and comparing both gives a discussion point.
2. Fit across surveys: SDSS, GAMA, VANDELS and DJA.

### Key figures in the paper

Heading written as "6 key figures in paper" with five items listed:

1. Show example fits and posterior from every survey.
2. Include mass-assembly figures to build trust.
3. Show the \(H(z)\) slope (main claim: \(H(z)\) from ages across redshift).
4. Include a progenitor-bias figure (to come later).
5. Show \(\Lambda\mathrm{CDM}\) and \(w_0/w_a\) (**nice as a bonus**).

### Schedule

- Meet on Fridays (ad hoc, no strict schedule).

</details>

<details>
<summary>Original transcription</summary>

### Page 1

- Sketch: vertical axis SFR, horizontal axis t lookback. A black curve peaks at shorter lookback time and a red curve peaks at longer lookback time.
- SFH can't fully model the effect of merger.
- Star accretion from satellites → Could be accreted from halo.
- f_exitu (accreted from external halos).
- 10^11 M☉ ~ f_exitu 30–50% [written 30-50°] today. Very high for massive galaxies.

### Page 2

- z ≈ 1, 10–40% (1/3 accreted).
- Red: How does this change the progenitor bias?
- Red: Cut by velocity dispersion (250 σ*) → most massive.
- Blue: two blank axis sketches, t_50 against σ* and t_80 against σ*.

### Page 3

- Blue: Downsizing not physical.
- Blue: Doesn't account for mergers.
- Red: Look at SDSS and sub surveys. z = 0–0.3 [underlined]. Most are z < 0.01.
- Red: Sub surveys are IFU surveys and this gets messy.
- Red: Find nice passive galaxies from SDSS ⇒ tens of thousands.
- Red: Good to have SDSS and anchor, compare to H_0.
- Blue: Again look into W_A W_0 CDM (continues onto page 4).

### Page 4

- Blue, continuing from page 3: → I would need multiple redshift ranges to test cosmological models over time, since this models H(z) evolution over time.

### Page 5

- Heading: "Surveys" [underlined].
- SDSS, z = 0–0.3, and GAMA, z ≈ 0.4, grouped by a red brace: ★ Very cool.
- VANDLES, z ≈ 1–1.5 — red: ⇒ Nice to have.
- DJA = Dawn JWST Archive (NIRCam + NIRSpec data) — red: ⇒ Could find.
- Ito, Baker papers — red: They already searched for quiescent galaxies.
- Red: ≈ 10s of galaxies, branching in blue to: Heavy Metal (≈ 10s of galaxies), Excel, Blue Jay.
- Blue brace under the three: Already aggregated in Dawn Archive.

### Page 6

- Blue: NIRSpec modes — Prism: R ~ 100 spectra. Grating: Medium: R ~ 1000.
- Blue: Many photometric observations, but few high resolution spectra.
- MJ looks into systematics of 2–3 galaxies (but not so important).
- Just self-consistently fit same model for different z-ranges (this is new).
- Red: ★ He has a question on number of SFH bins.
- Red: Just try to change binning (continues onto page 7).

### Page 7

- Red, continuing from page 6: "and see if" [unfinished].
- Red: Try and see what happens to systematics with different priors.
- Sketch: axes with a horizontal blue line labelled "Prior" and a red peaked curve rising above it and falling back to the horizontal axis.
- log (SFR_{i+1} / SFR_i) = ST(μ, σ), with μ = 0.
- Red: You can put μ = f(z).
- Red: SFMS prior ★.

### Page 8

- Red: This is more informed and physically more realistic.
- Red: Might be better even if only systematic.
- Heading: "Tldr:"
- ① Both priors (gives systematics understanding) — He prefers SFMS prior — But this provides a discussion.
- ② Fit across surveys: SDSS, GAMA, Vandles, DJA.

### Page 9

- Heading: "6 key figures in paper" [five items listed].
- ① Show example fits and posterior from every survey.
- ② Some mass-assembly figures (build up trust).
- ③ H(z) slope.
- ④ Progenitor bias figure.
- ⑤ Λ-CDM w_0/w_a would be nice as a bonus ["as a" underlined, "bonus" double-underlined].
- Meet on Fridays.

</details>

<details>
<summary>Original clarifications</summary>

- Paper's main claim: "H(z) from ages" (fit passive galaxies across surveys with one model, ages across redshift, H(z) from how age changes with redshift).
- Novelty: "One model, all surveys", "Alpha-enhanced grid".
- Mergers: "the point about mass matched galaxies at different redshifts not being the same population seems about right. i'm not quite sure if velocity dispersion does in fact change less in mergers, but sorting galaxies by velocity dispersion with 250 as the cutoff seems like it's good practice to do regardless."
- Downsizing remark: "not important, just a little nitpick he has lol. he says the existing mass assembly by stellar mass figure is well backed up by existing literature (look into it a little maybe?) and so this should be a good vote of confidence, or "builds trust" that the model is physically accurate and reliable"
- Turner et al. 2025 rising prior: "ignore turner, you can remove from roadmap. seems to be a prior specific to this research group" (removed 2026-11-20).
- SFMS prior: "i'll ask other members of the group for it, don't build anything yourself"
- SFH bins: "most model and parameter choices seem fine, but he was still interested in if more/finer SFH bins would shift age results. worth seeing if age slope or age systematics vary across number of bins". Sample: "10 test galaxies first".
- Progenitor-bias figure: "i'm not sure yet. this can come later"
- Ex-situ fraction: "discuss only, it's just an interesting point, but it seems very hard to model and account for"
- SDSS size: "well, let's fit an initial few to build up the data pipeline. i don't have the credit budget to fit thousands, so let's experiment first". Pilot galaxies: "Any clean passive ones".
- Survey order: "SDSS, GAMA, JWST, then VANDELS. you don't necessarily have to follow this strictly, let's see how suitable the surveys are to these kind of modelling and fitting first"
- JWST data: "Medium grating only".
- Settings across surveys: "let's do identical settings for now. this are not necessarily the final settings but i'd like consistent settings across different surveys"
- Next goals: SFH-bin test, first SDSS fits. "there's no strict meeting schedule, it's ad hoc, but these are the immediate next goals to work towards"

</details>

<details id="source-and-review">
<summary>Sources</summary>

- [Original handwritten notes](/f/reports/meeting-2026-11-20-sandro.pdf), pages 1–9 (copied from `/Users/liuhao/Downloads/20 notebook.pdf`).
- [20 November 2026 check-in](/checkins/2026-11-20/).
- Original request (20 November 2026): "here is the discussion i had with my supervisor today. Where should today's meeting go on the wiki: Meeting note"

</details>
