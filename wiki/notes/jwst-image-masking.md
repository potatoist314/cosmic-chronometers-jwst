---
title: JWST image masking — handwritten notes
date: 2026-09-14
section: Masking
theme: Sample and data
tags: [jwst, nircam, masking, handwritten-notes]
job:
---

Inspect each GIF, draw the artifact mask in GIMP, then export the mask for FITS conversion.

[Original handwritten PDF](/wiki/f/masking/masking.pdf)

<details open>
<summary>Masking workflow</summary>

### Inspect the exposures

Inspect each GIF frame by frame, using the inspection table. Group observations by position angle (PA) and time. One observation may contain multiple visit groups. Inspect the whole sensor group, including short- and long-wavelength images. A blank entry is OK; note artifacts when present. [Pages 2, 4–5]

A cosmic-ray artifact may appear in only one frame. Mask that individual artifact. Masked data are “completely NOT processed.” Offsets between dithers can leave a source unmasked in another frame, making that frame usable. [Pages 5, 7]

### Draw and export the mask

1. Save the first frame of each inspected GIF as a PNG in a folder.
2. Sort by filename. The example `1_2201` has arrows labelled “Visit” and “Group”, but the exact filename fields are unclear.
3. Open the PNG in GIMP and add an extra layer.
4. Draw the mask by hand on that layer at 100% opacity.
5. Export only the mask layer as a PNG into a new folder. Retain the same filename format. Shortcut: “CMD shift E”.
6. Crop to the rightmost panel, where the mask was drawn. He has a script for the exact crop.
7. Make N duplicates based on N observations.
8. Convert the folder of PNG masks to FITS and compress it. Example: about 550 MB before compression and 600 kB afterward, because the data are binary 0/1.

[Pages 5–7]

### Handoff

Send the FITS mask file to him. He will handle masking for alignment with Gaia astrometry and send a masking tutorial and artifact types. [Page 7]

</details>

<details>
<summary>Observing context</summary>

### NIRCam and filters

SW: short wavelength. LW: long wavelength. A2 and A4 sit above A1 and A3 in the sketch. A red outline surrounds the four boxes, labelled A5: “Combine 4 modules to become A5”. [Page 1]

“NIRCam — 8 modules.” Pixel scales: 0.031 and 0.063 arcsec/pixel. “LW has half resolution.”

Long-wavelength filters: higher transmission and wide bandpasses, leading to high S/N and fainter limiting magnitudes. Approximately 20% throughput at SW. [Pages 1–2]

### Fields and comparison data

The example program identifier reads `JW 018370` [unclear digit grouping]. The historical Hubble CANDELS field list is COSMOS, UDS, EGS, GOODS-S and GOODS-N. COSMOS has a red “relatively larger area” annotation. A blue bracket describes existing observations as shallow, with low S/N. [Pages 2–3]

JADES observes GOODS-S and GOODS-N with substantial GTO time: high exposure, narrow area and high depth. NIRCam and NIRSpec data. Hubble data extend only to 1.6 micron. Match HST to JWST data for Lyman-alpha dropout bands. Cross-check Rubin, LSST and Euclid data. [Page 3]

### Observation grouping

Depth: limiting magnitude at 5 sigma. Group observations by PA and time. “PA tolerance ≈ ±3° / ±30 days.” Visit groups, observations and exposure counts; sometimes he omits a zero. [Page 4]

</details>

<details>
<summary>Page-by-page transcription</summary>

### Page 1

- [Black] NIRCam — 8 modules. SW — short λ. LW — long λ.
- [Diagram] A2, A4 in the top row. A1, A3 in the bottom row. [Red outline around all four, labelled A5.]
- [Red] A5 — combine 4 modules to become A5.
- [Black, left of diagram notes] 0.031″/px. 0.063″/px.
- [Black] A1–4, for SW; the CCD modules are used one at a time.
- [Black] LW has half resolution.
- [Black] Artifact list; long.
- [Heading] NIRCam filters.
- [Black, continues on page 2] Long-IR has much higher…

### Page 2

- [Continuation] …transmission; with wide filter bandpass ⇒ high S/N.
- So LW can reach much higher mag. Only ≈20% throughput at SW.
- Masking using GIMP.
- [Indented] Inspect the GIF (inspection table!!) per frame!!
- [Heading] Observations.
- JW 018370 [unclear digit grouping]. [Arrow: program ID.]
- Hubble fields (historical). [Continues on page 3.]

### Page 3

- [Black] Hubble CANDELS: 1. COSMOS; 2. UDS; 3. EGS; 4. GOODS-S; 5. GOODS-N.
- [Red, COSMOS] Relatively larger area.
- [Blue, bracket beside field list] Shallow existing observations; but lower S/N.
- [Red, bracket beside GOODS-S and GOODS-N] JADES observes in these fields (lots of GTO time).
- [Red] JADES is high exposure, narrow, high depth. NIRCam. NIRSpec data.
- [Blue, bracket under field list] Hubble data only exist to 1.6 micron.
- [Blue] Match HST data to JWST data to match Lyman-α dropout bands.
- [Black] Rubin, LSST, Euclid data to cross-check.

### Page 4

- [Black] Depth (limiting mag, 5σ).
- Position angle (PA).
- One observing program: data is separated according to PA and time.
- [Red] PA tolerance ≈ ±3° / ±30 days.
- [Black] Visit groups, observations.
- Sometimes he’s lazy and doesn’t write a 0.
- # Exp: number of exposures.
- One observation might have multiple visit groups.

### Page 5

- [Black] Entire sensor group (short to long included).
- [Red] If blank, OK; artifacts are noted.
- Cosmic-ray artifact might only appear in a single frame ⇒ just mask that single cosmic ray.
- Masked data is completely NOT processed.
- GIFs used for inspection; then we save into PNGs.
- Save first frame of GIF as PNG to proceed with masking. [“First frame” underlined.]
- Inspect GIFs, generate first frame into folder.

### Page 6

- [Red] `1_2201`. [Arrows below the example labelled “Visit” and “Group”. Their exact extent is unclear.]
- Just sort by name; rank for largest obs (number). [The last parenthetical word is probably “number”.]
- Open the file in GIMP.
- Make an extra layer.
- And draw 100% opacity on top of it (draw by hand).
- Export (CMD shift E).
- Export to new folder; export mask layer only as PNG.
- Save in the same name format.
- Mask is only on rightmost panel; then you have to crop to appropriate [word ends here].
- He has script to crop it exactly.
- Make N duplicates based on N observations.

### Page 7

- [Red] The whole folder of PNG can be converted to a FITS and zipped.
- FITS file is huge (550 MB) before compression; after compression only 600 kB → highly compressible due to being 0/1 files.
- Send FITS masking file to him.
- [Black] He will do masking for alignment for Gaia astrometry.
- Masking is often offset → like over dither; if one frame captures unmasked → usable. [Compressed wording retained.]
- He will send me a masking tutorial and artifact types.

</details>

<details>
<summary>Source and request</summary>

- Source: [masking/masking.pdf](/wiki/f/masking/masking.pdf), pages 1–7.
- Original request: “just uploaded some handwritten notes regarding JWST masking masking - transcribe and basically save the notes into some human readable explanation on the astro wiki”

</details>
