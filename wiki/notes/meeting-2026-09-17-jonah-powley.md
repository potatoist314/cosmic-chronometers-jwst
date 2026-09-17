---
title: Meeting with Jonah Powley
date: 2026-09-17
section: Meetings
theme: Single-fit accuracy
tags: [meeting, prospector, quiescent, priors, dust]
job:
---

[Original handwriting](/wiki/f/reports/meeting-2026-09-17-student-group-jonah-powley.pdf), pages 4–9 · [Student group meeting](/wiki/n/meeting-2026-09-17-student-group/), pages 1–3 of the same file.

<details open id="corrected-meeting-notes">
<summary>Meeting notes</summary>

#### Star-formation-history prior

- The Student-t SFH prior, \(T(\mu_{\mathrm{SFH}}, \sigma, 3)\), has 3 degrees of freedom. For a physically motivated rising star-formation rate, define a higher prior where you physically expect more star formation. ★ This has a strong impact on stellar age.
- There is a huge dependence on the SFH prior! ★ Look into the rising continuity prior. His rising continuity prior comes from another paper.
- The photographed figure shows stellar age for SFH prior (rising, flat) against stellar abundance (solar-scaled, \(\alpha\)-enhanced): 1.19, 1.07, 1.46 and 1.39 Gyr.
- prospect utils is on GitHub. He made a function to define age bins more explicitly, but it is probably not helpful.

#### Abundances and lines

- The Mg b absorption line is the main constraint for \(\alpha/\mathrm{Fe}\).
- Ca I [?] can be masked because of potential IGM contamination.
- ★ Generally, age estimates get older for non-\(\alpha\)-enhanced spectra.
- \(\alpha\)-enhancement gives a better formation-timescale constraint and more confidence in the physical formation mechanism.

#### Dust and infrared

- For dust, he uses Kriek & Conroy (modified Calzetti). His \(\tau_{\mathrm{dust},2}\) is around 0.77.
- ★ Given the infrared photometry, I should look into turning on dust emission. ★ AGN torus emission could contribute infrared emission.
- ★ For infrared data, AGN torus and dust emission make a more physical model.
- ★ Photometry massively changed the mass and dust constraints in his example fit.

#### His setup

- ★ Jonah sent me his priors and his first-year PhD report. Get him to send the report.
- ★ What is \(f_{\mathrm{AGN}}\)? ★ Is his AGN torus parameter uniform in log space? ★ His redshift is a free parameter with [the handwriting stops here].

#### Other

- Try IFU fitting (slightly more complicated).
- Can I generate the median, best-fit, q16 and q84 spectrum output?
- ★ Data reduction matters.
- The SFH for mergers could be super messy; you cannot see this from the SFH.
- GN-z11, the famous galaxy? A possible progenitor?

</details>

<details id="original-transcription">
<summary>Original transcription</summary>

### Page 4

- → T(μ_SFH, σ [?], 3). Margin: “a/w 3” [3 degrees of freedom].
- Student t SFH → physically motivated rising star formation rate. Define higher prior where you expect physically more star formation.
- Blue ★: Strong impact on stellar age.
- Get him to send report.
- Mg b absorption line is main constraint for α/Fe.
- Ca I [?] can be masked b/c of potential IGM contamination.

### Page 5

- ★ Generally age estimates get older for non α-enhancement spectra.
- Try IFU fitting (slightly more complicated).
- Photograph of a figure: a 2×2 grid of stellar age [Gyr] for SFH prior (Rising, Flat) against stellar abundance (Solar-scaled, α-enhanced): Rising/Solar-scaled 1.19 +0.06 −0.03; Rising/α-enhanced 1.07 +0.08 −0.20; Flat/Solar-scaled 1.46 +0.10 −0.10; Flat/α-enhanced 1.39 +0.13 −0.14. Caption fragment: “…e to SPS modelling. Left panel: SFHs from models … solar-scaled (green) and α-enhanced (purple) stellar…”.
- SFH prior has huge dependence! → Blue: Look into rising continuity prior ★
- prospect utils github.
- He made function to define age bins more explicitly (but probably not helpful).

### Page 6

- His rising continuity prior comes from another paper.
- Can I generate the median, best fit, q16 q84 spectrum output?
- Data reduction matters ★
- SFH for mergers could be super messy (you can't see this from SFH).
- GN-z11 famous galaxy? Possible progenitor?

### Page 7

- α-enhancement ⇒ better formation timescale constraint ⇒ more confidence on physical formation mechanism.
- Dust ⇒ He uses Kriek Conroy (modified Calzetti).
- ★ Given infrared photometry, I should look into turning on dust emission.
- ★ AGN torus emission could contribute infrared emission.

### Page 8

- ★ Jonah sent me his priors and his 1st year PhD report.
- ★ What is fagn?
- ★ His AGN torus parameter is uniform in log space?
- ★ His redshift is a free parameter with [the handwriting stops here].
- ★ Photometry massively changed mass and dust constraints in his example fit.
- His tau dust 2 is around 0.77.
- ★ Infrared data → (page 9) ① AGN torus ② Dust emission } “More physical model”.

</details>

<details id="source-and-review">
<summary>Sources</summary>

- [Original handwritten notes](/wiki/f/reports/meeting-2026-09-17-student-group-jonah-powley.pdf), pages 4–9 of a nine-page file exported on 17 September 2026; pages 1–3 are the [student group meeting](/wiki/n/meeting-2026-09-17-student-group/). The page-4 boundary is a reading of the notes, not marked in them; the meeting date is not written in the notes.
- Clarifications, 17 September 2026: “CIRCI and Ca I are correctly marked. it's IGM contamination. student t df 3 means it should have 3 degrees of freedom.”
- Original request: “/Users/liuhao/Downloads/group\ student\ meeting.pdf Here's notes from another two meetings: first with a general student group meeting (and some general questions I had after hearing about what others were working on), and next notes from a meeting with Jonah Powley who works extensively with prospector SED fitting and passive quiescent galaxies”

</details>
