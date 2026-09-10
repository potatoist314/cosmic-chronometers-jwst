# Session: LEGA-C DR2 1D spectra on disk and loaded in the SED notebook

- **Date:** 2026-08-04
- **Project phase:** Exploratory SED-fitting branch (`notebooks/03_sed_fitting.ipynb`)
- **Session status:** completed
- **Primary goal:** All 1988 LEGA-C DR2 1D spectra retrieved reproducibly into
  `data/raw/legac_dr2/sp/`, and one bona-fide-passive spectrum loaded and plotted
  in `notebooks/03_sed_fitting.ipynb` with its per-pixel S/N checked against the
  catalogue.

## Why this session matters

Every measurement used so far has come from the DR2 *catalogue*: Lick indices,
emission-line EWs, velocity dispersions, S/N. The spectra themselves have never
been opened in this project. Both live branches now need them:

- the Lick branch, because `2026-08-03-audit-borghi-sample-selection-4.md`
  established that Borghi measured indices from the spectra with PyLick rather
  than reading the public catalogue columns, and the current fit has reduced
  χ² ≈ 18 for object 207825;
- the SED branch, because a Prospector spectral fit needs the observed spectrum
  as its data vector.

This session does only the data step, so that neither branch starts by guessing
the file format, the bad-pixel convention, or the flux units.

## Starting point

- **Last verified state:** `2026-08-04-create-sed-fitting-notebook.md` closed
  with `notebooks/03_sed_fitting.ipynb` as an exact truncated copy of notebook 02
  through the Dn4000-vs-[OII] plot (cell `64d80659`), with one empty trailing
  code cell `73377a91` and no SED-fitting code.
- **Relevant files or notebook sections:** `scripts/` (new download script),
  `data/raw/legac_dr2/`, `.gitignore`, and the cells after `64d80659` in
  `notebooks/03_sed_fitting.ipynb`.
- **Inputs and provenance:** LEGA-C DR2 (Straatman et al. 2018, ApJS 239, 27).
  Catalogue already in `data/raw/legac_dr2/legaCdr2.fits.gz`; spectra from the
  CDS mirror of VizieR `J/ApJS/239/27`, directory `sp/`, which the VizieR ReadMe
  records as the 1988 individual reduced 1D spectra downloaded from
  <http://www.mpia.de/home/legac/>. Format documented in
  `data/raw/legac_dr2/ESO_DR2_release_description.pdf` §Data Format.
- **Open question or uncertainty:** whether the flux units, the ESO Phase 3
  single-row table layout, and the `QUAL`/`ERR` bad-pixel convention are being
  read correctly — a silent error here would propagate into every downstream fit.

## Definition of done

1. `ls data/raw/legac_dr2/sp | wc -l` gives 1988, total ≈205 MB, and a second run
   of the script downloads nothing.
2. `git status --short` does not list the spectra.
3. In a fresh kernel, `notebooks/03_sed_fitting.ipynb` loads the highest-`SN`
   bona-fide-passive spectrum, plots it with masked pixels marked and the
   observed 4000 (1+z) Å break in the right place, and prints a median per-pixel
   S/N of order 10–50 that is comparable to that row's catalogue `SN`.

## Scope

- **In scope:** the download script, `.gitignore` and README provenance, and two
  notebook cells (loader + one-galaxy check).
- **Out of scope:** index re-measurement, PyLick, any Prospector model, changes
  to the selection cuts, rest-frame conversion, and 2D spectra (only 1D products
  are released through this channel).

## Planned tasks

### 1. `scripts/download_legac_dr2_spectra.py`

- **Status:** planned
- **Purpose:** make the spectra a documented, regenerable input rather than an
  ad-hoc download. `data/raw/cosmos2015/README.md` already records the cost of
  the alternative: that cross-match has no script and cannot be reproduced.
- **Work:** read the `Filename` column from the DR2 catalogue, validate the 1988
  names against `legac_M<mask>_<id>_v2.0.fits`, fetch each from
  `https://cdsarc.cds.unistra.fr/ftp/J/ApJS/239/27/sp/`, skip files already
  present, download via a `.part` temporary and `os.replace` so an interrupted
  run cannot leave truncated FITS behind.
- **Expected artifact:** the script, `data/raw/legac_dr2/sp/` with 1988 files, a
  `.gitignore` entry, and a provenance section in
  `data/raw/legac_dr2/README.md`.
- **Trustworthiness check:** each newly downloaded file is opened and asserted to
  carry `WAVE`, `FLUX`, `ERR`, `QUAL` in a one-row HDU 1; the run ends by
  asserting 1988 files present. Re-running must download zero files.

### 2. Loader and one-galaxy check in `03_sed_fitting.ipynb`

- **Status:** planned
- **Purpose:** establish the correct way to read a LEGA-C spectrum once, in the
  notebook, before anything is fitted to one.
- **Work:** `load_spectrum(filename)` returning `wave, flux, err, good` with
  `good = (QUAL == 0) & isfinite(FLUX)`; then plot the highest-`SN`
  bona-fide-passive spectrum and print its measured median `flux/err`.
- **Expected artifact:** two cells after `64d80659`, one figure, one printed
  number.
- **Trustworthiness check:** the measured median per-pixel S/N against the
  catalogue `SN` for the same row. The break must appear at 4000 (1+z) Å, not at
  4000 Å.

## Predictions before calculation

- Median per-pixel S/N should land near the survey's advertised
  S/N ≈ 20 Å⁻¹, i.e. roughly 15 per 0.6 Å pixel, and the catalogue `SN` for the
  best row should be in the same range.
- Masked pixels should be concentrated at the two ends of the `WAVE` array,
  because the array spans 5800–9499 Å while the header's `WAVELMIN`/`WAVELMAX`
  give real coverage as only 6332–8900 Å. If masked pixels are instead spread
  uniformly through the continuum, the mask is being read wrongly.

## Working log

- **Facts established by direct inspection before coding (in-memory fetch of
  `legac_M1_126153_v2.0.fits`, nothing written to disk):**
  HDU 1 is `PHASE3SPECTRA`, a binary table with **one row** whose four cells each
  hold the whole 6166-element array, so the arrays are `data['WAVE'][0]` — omitting
  the `[0]` silently yields shape `(1, 6166)`. Columns are `WAVE` (Å),
  `FLUX` and `ERR` (10⁻¹⁹ erg s⁻¹ cm⁻² Å⁻¹) and `QUAL` (int16).
  `QUAL == 1` is exactly equivalent to `ERR == 0` (verified identical; 2184 of
  6166 pixels in that file), and per the release description `ERR == 0` means
  *discard the pixel*, not "very small error". Header carries
  `SPECSYS = 'TOPOCENT'`, `SPEC_RES = 2500`, `SPEC_BIN` 0.6 Å/pixel,
  `FLUXCAL = 'ABSOLUTE'`, `TOT_FLUX = False`.
- **Sample size, recomputed outside the notebook from the same cuts:** `parent`
  1617 → `photometric_passive` 666 → `spectrophotometric_passive` 492 →
  `bona_fide_passive` 381 rows / 372 unique `OBJECT` / 381 unique `Filename`.
  Decision: download all 1988 spectra rather than only these 381, so that
  `data/raw/` does not depend on selection cuts that are still being revised.

## Session close-out

- **Final status:** completed

- **Accomplished:** both planned tasks. All 1988 spectra are in
  `data/raw/legac_dr2/sp/` (208.8 MB), the script re-runs with
  `Downloaded 0 (0.0 MB), already present 1988`, `git check-ignore` confirms the
  directory is excluded, and the notebook's two new cells run in a fresh kernel.
  Notebook evidence is a headless `nbconvert --execute` run of
  `03_sed_fitting.ipynb` to a scratch copy, so the committed notebook still
  carries no output for the new cells until they are run interactively.

- **Key results and interpretation:**
  - **The loader is validated.** For `M1_207825` at z = 0.6968,
    `median(flux[good] / err[good])` = 70.1 against the catalogue's `SN` = 70.0.
    Repeating that over 40 random DR2 rows gives a median disagreement of 0.85%,
    so `SN` simply *is* the median per-pixel S/N over unflagged pixels. Units,
    the single-row `[0]` indexing, and the mask are therefore all correct.
  - **The 4000 Å break lands exactly where the redshift puts it**, 6787 Å, with
    the continuum stepping from ≈100 to ≈170 in flux units across it and Ca II
    H&K visible just blueward. Flagged pixels fall only at the two padded ends of
    the array and on the 7620 Å telluric O₂ A-band — not scattered through the
    continuum, which was the prediction.
  - **Coverage is per-spectrum, not per-survey.** `M1_207825` covers
    6283–8735 Å, not the 6332–8900 Å of the file whose header was inspected first.
    A pre-filter built on the nominal range is therefore wrong: the first version
    of the check selected `M5_172669` (z = 0.6037, break at 6415 Å) whose own
    coverage starts near 6570 Å, so the break fell inside the flagged padding and
    the check was vacuous. Fixed by testing the break against each spectrum's own
    good pixels. Anything that assumes a fixed wavelength grid across the sample
    — index bandpasses, a common rest-frame grid, a Prospector wavelength mask —
    has to be built per spectrum.
  - **Two facts about the selection, found incidentally and not acted on:**
    (i) the highest-`SN` row of `bona_fide_passive` is `M11_231636` at z = 0.3458,
    a filler, and 5 of the 381 rows sit below z = 0.6, because the notebook's
    quality cut uses `f_ppxf`/`f_z`/`f_int`/`SN` but not `f_primary`;
    (ii) the catalogue's `SN` reaches 57082 for `M2_130902`, and the spectrum
    confirms it — measured 57478, from a genuinely pathological `ERR` array
    against a normal median flux of 49.3. Those rows pass `SN > 0` and would be
    preferred by `sort_values('SN')` when choosing among repeat spectra. One of
    the 40 random rows also disagreed with its catalogue `SN` by 158%,
    uninvestigated.

- **Files changed or created:**
  - `scripts/download_legac_dr2_spectra.py` (new)
  - `data/raw/legac_dr2/sp/` (new, 1988 files, gitignored)
  - `.gitignore`, `data/raw/legac_dr2/README.md` (provenance section)
  - `notebooks/03_sed_fitting.ipynb` — three cells after `64d80659`: format
    bullets (`73377a91`), `load_spectrum` (`0c0d3e7e`), one-galaxy check
    (`caff961a`)

- **Not completed:** nothing planned. The `SN` anomalies above are recorded, not
  resolved.

- **Plan deviations:** two. The break-coverage test had to move from a fixed
  wavelength pre-filter to a per-spectrum check, for the reason above. Separately,
  `NotebookEdit` left `execution_count` and `outputs` keys on the cell it
  converted from code to markdown, which made the notebook JSON fail
  `nbformat.validate`; the keys were stripped and the notebook now validates.

- **Decisions made:**
  - Download all 1988 spectra rather than the 381 selected, so `data/raw/` does
    not depend on cuts that are still being revised.
  - `good` combines `QUAL == 0` with `ERR > 0`. They were verified equivalent on
    one file, but keeping both makes the `flux / err` division safe without
    relying on that equivalence holding in all 1988.
  - Return the flag alongside the full arrays rather than pre-filtered arrays, so
    no pixel is dropped before it has been looked at.
  - Loader stays in the notebook. It moves to `src/` when the Lick branch in
    `02_differential_ages.ipynb` also needs it.

- **Exact next starting point:** `notebooks/03_sed_fitting.ipynb` after cell
  `caff961a`, with `load_spectrum` available and validated. The spectra are on
  disk for all 1988 rows, so nothing blocks either branch on data access.

- **Recommended next-session goal:** decide the SED-fitting objective and its
  data vector before writing any Prospector code — specifically, whether the fit
  uses the spectrum alone, the COSMOS2015 photometry alone, or both, and how the
  free normalisation demanded by `TOT_FLUX = False` is parameterised. The
  per-spectrum coverage result means that choice also fixes which rest-frame
  wavelength range is common to the sample.

## Deferred conventions, recorded here rather than in the notebook

These are all consequences of the header keywords above. None is acted on this
session, but each will matter to whichever branch uses the spectra next.

- **Rest frame:** `wave_rest = wave / (1+z)` and `F_λ,rest = F_λ,obs × (1+z)`.
  Not applied in the loader.
- **Reference frame:** `SPECSYS = 'TOPOCENT'` means no barycentric correction has
  been applied. That is ≲30 km/s, about 0.8 Å at 8000 Å — small against the
  120 km/s resolution element, but not zero.
- **Air vs vacuum:** `WAVE` is air (the release description states wavelengths are
  measured in dry air). Air→vacuum is ≈2.2 Å at 8000 Å, ≈3.7 pixels. Lick indices
  are defined in air, so index work needs no conversion, but the convention of
  whichever SPS library Prospector is configured with must be checked before
  fitting a spectrum.
- **Flux normalisation:** `TOT_FLUX = False`, and the release description reports
  slit losses of 10–40% with the calibration tied to the shape of the UltraVISTA
  photometric SED (≈5% accuracy per galaxy). The absolute scale is therefore not
  total galaxy flux; a Prospector spectral fit needs a free normalisation or
  calibration polynomial rather than trusting it.
- **Rest-frame coverage varies across the sample:** 6332–8900 Å observed maps to
  ≈3960–5560 Å at z = 0.6 but ≈3170–4450 Å at z = 1.0. Which Lick indices and
  which SED features are measurable is therefore redshift-dependent.
