---
title: Data pipeline
date: 2026-08-30
section: Codebase
tags: [legac, dr2, data]
job: 
old: _old/codebase/data-pipeline.html
---

### Active Ceridwen flow

- **LEGA-C DR2**Spectrum or published stellar indices
- **COSMOS2015**Matched photometry
- **Ceridwen SSP grid**Published population spectra

1. **Observation objects**Spectrum or StellarIndices, plus Photometry
2. **SedModel**Shared prediction
3. **BlackJAX NSS**Sampled posterior

Borghi Table 4 supplies a separate reference comparison.

<figure>
<figcaption>Three source products enter the active fit through documented conversions.</figcaption>
</figure>

### Raw catalogues

`data/raw/borghi2022/vizier_J-ApJ-927-164_table4.tsv` contains 140 unique galaxies. It includes published ages, `[Z/H]`, `[alpha/Fe]`, coordinates, and errors. It does not include redshift, velocity dispersion, or indices (`data/raw/borghi2022/README.md`). The active workflow uses these values for reference comparisons.

`data/raw/legac_dr2/legaCdr2.fits.gz` contains 1,988 spectrum rows. It supplies redshifts, velocity dispersions, flags, coordinates, spectrum filenames, and published stellar indices. Repeat observations make some object IDs nonunique (`data/raw/legac_dr2/README.md`).

`data/raw/cosmos2015/` contains positional matches for NUVrJ selection and broadband fluxes. Each catalogue row matches a LEGA-C spectrum row. Therefore, an object can occur more than once (`data/raw/cosmos2015/README.md`).

### Selection and comparison tables

The production selection contains 194 eligible spectrum rows. Seven objects have a repeated eligible spectrum. The runner keeps the highest-S/N row for each `OBJECT`, which leaves 187 galaxy fits. Observed 4000-A coverage is recorded but does not remove a target (`scripts/run_ceridwen_vast_multi_gpu.py:79-137`).

The builder parses and checks exactly 140 Borghi IDs (`scripts/build_borghi2022_legac_dr2_subset.py:109-122`). It indexes every LEGA-C row by `OBJECT` (`lines 194-204`). It retains all matching spectrum rows. It also checks that every coordinate match is within 0.1 arcsec (`lines 209-264`).

The result contains 143 spectrum rows for 140 galaxies. Two objects with repeat spectra cross the strict 215 km/s boundary. The object audit marks these objects as ambiguous (`data/processed/borghi2022_legac_dr2/README.md`).

### Spectrum files

Each LEGA-C FITS file stores one binary-table row. The row cells contain these arrays:

- `WAVE`: observed-frame air wavelength in Angstrom.
- `FLUX`, `ERR`: `10^-19 erg s^-1 cm^-2 Angstrom^-1`.
- `QUAL` contains the bad-pixel flag. A nonzero value marks a bad pixel.

The downloader checks these columns and the single-row structure (`scripts/download_legac_dr2_spectra.py:64-79`). The spectrum notebook converts air wavelengths to vacuum wavelengths. It also converts `F_lambda` to `F_nu` before it creates a Ceridwen `Spectrum`. See the headings “Load the same high-S/N test galaxy” and “Build the native-resolution spectrum.”

The spectra-only notebook first removes invalid pixels, nebular-line regions, and the telluric region. Full mode retains 3,523 likelihood pixels. Feature mode retains 1,924 pixels from complete LEGA-C feature bandpasses. Overlapping windows form one union, so a pixel occurs once. The compact `Spectrum` also contains two masked endpoint pixels. These pixels preserve the native smoothing boundaries.

`notebooks/ceridwen_test_spectra.ipynb` · “Build the native-resolution spectrum” · `LEGAC_FEATURE_BANDS_AIR`, `fit_pixel_mask`, and `compact_indices`

### Published stellar indices

The integrated notebook can use 13 LEGA-C Lick measurements and `Dn4000` instead of native spectral pixels. It reads the catalogue values and one-sigma errors. Invalid or missing rows are masked. The four configured targets retain 14, 10, 14, and 13 indices, respectively.

These catalogue values are emission corrected. The likelihood uses their published diagonal uncertainties because the catalogue does not provide an index covariance matrix. This assumption ignores correlations between indices that share continuum bands.

### Photometry

The photometry downloader queries within one arcsecond and calculates the separations. It sorts candidates by LEGA-C index and separation. It retains the nearest candidate (`scripts/download_cosmos2015_legac_dr2_photometry.py:61-99`). The selected aperture fluxes use microJy (`lines 110-113`). The joint notebook converts microJy to AB maggies. It also adds a five-percent uncertainty floor. Both spectroscopy modes fit all 12 bands. Full-spectrum mode fits a separate `spectrum_scaling` parameter for the measured slit spectrum.

### Data contracts entering Ceridwen

- `Photometry.flux` is a one-dimensional array of AB maggies.
- `Photometry.uncertainty` has the same shape and units.
- `Spectrum.wavelength` contains observed-frame vacuum wavelengths in Angstrom.
- `Spectrum.flux` contains observed `F_nu` that is compatible with the model prediction.
- `Spectrum.mask` is `True` for each pixel that contributes to the likelihood.
- `StellarIndices.flux` contains equivalent widths, magnitudes, and `Dn4000` in one aligned vector.
- `StellarIndices.mask` includes only finite catalogue measurements with positive uncertainty.

The base observation checks that the arrays are one-dimensional and aligned. It masks nonfinite flux and nonpositive uncertainty (`ceridwen/ceridwen/observation/base.py:189-231`).

### Examples

`scripts/build_borghi2022_legac_dr2_subset.py:194-213 · main`

```
rows_by_id: dict[int, list[int]] = defaultdict(list)
for index, object_id in enumerate(dr2["OBJECT"]):
    rows_by_id[int(object_id)].append(index)

missing_ids = [
    int(row["[MMS2013]"].strip())
    for row in borghi_rows
    if not rows_by_id[int(row["[MMS2013]"].strip())]
]
if missing_ids:
    raise ValueError(f"Borghi IDs missing from LEGA-C DR2: {missing_ids}")

output_rows: list[dict[str, str | int]] = []
separations: list[float] = []

for borghi in borghi_rows:
    object_id = int(borghi["[MMS2013]"].strip())
    match_indices = sorted(
        rows_by_id[object_id], key=lambda i: str(dr2["SPECT_ID"][i])
    )`
```

**Documented contract:** The module docstring defines this script as the Borghi Table 4 to LEGA-C DR2 join (`scripts/build_borghi2022_legac_dr2_subset.py:2`).

**Why it matters:** `rows_by_id` maps one galaxy ID to a list of rows. This type choice preserves repeat spectra during the join.

`scripts/download_cosmos2015_legac_dr2_photometry.py:87-97 · download_cosmos2015`

```
order = np.lexsort(
    (
        np.asarray(candidates["MATCH_SEP_ARCSEC"]),
        np.asarray(candidates["LEGAC_INDEX"]),
    )
)
candidates = candidates[order]
_, nearest = np.unique(
    np.asarray(candidates["LEGAC_INDEX"]), return_index=True
)
matched_batches.append(candidates[np.sort(nearest)])`
```

**Documented contract:** The function docstring requires the nearest COSMOS2015 match within one arcsecond (`scripts/download_cosmos2015_legac_dr2_photometry.py:62`).

**Why it matters:** The sort groups candidates by LEGA-C row and then by separation. Therefore, `np.unique(..., return_index=True)` selects the nearest candidate in each group.
