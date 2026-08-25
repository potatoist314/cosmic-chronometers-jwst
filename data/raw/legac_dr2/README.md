# Raw LEGA-C DR2 data

- Main file: `legaCdr2.fits.gz`.
- It contains 1,988 spectra with redshifts, velocity dispersions, Lick indices, and errors.
- A galaxy can have more than one spectrum; `SPECT_ID` identifies each spectrum.
- `VizieR_ReadMe.txt` explains the catalogue columns.
- `ESO_DR2_release_description.pdf` is the official ESO documentation.
- Source: <https://doi.org/10.18727/archive/39>
- Downloaded on 2026-07-21; do not edit these raw files.
- Rebuild the processed tables with `.venv/bin/python scripts/build_borghi2022_legac_dr2_subset.py`.

## `sp/` — the 1D spectra

- 1,988 files, one per catalogue row, ~205 MB total.
- The file for a row is its `Filename` column value, e.g. `legac_M1_126153_v2.0.fits`.
- Source: <https://cdsarc.cds.unistra.fr/ftp/J/ApJS/239/27/sp/>, the VizieR mirror
  for Straatman et al. (2018) of the spectra released at
  <http://www.mpia.de/home/legac/>.
- Downloaded on 2026-08-04 with `uv run python scripts/download_legac_dr2_spectra.py`;
  re-run that to restore the directory. It skips files already present.
- Gitignored: too large to track. The script and this section are the provenance record.
- Format: HDU 1 is a binary table with a *single* row whose four cells each hold
  the whole 6,166-element array — `data['WAVE'][0]`, not `data['WAVE']`.
- Columns: `WAVE` (angstrom, air, topocentric), `FLUX` and `ERR`
  (1e-19 erg s-1 cm-2 angstrom-1), `QUAL` (integer flag).
- `QUAL = 1` marks a pixel to discard, and is equivalent to `ERR = 0`. Per the
  release description, `ERR = 0` does not mean a small error.
- `WAVE` spans 5800-9499 angstrom but real coverage is the header's
  `WAVELMIN`/`WAVELMAX`, 6332-8900 angstrom; the padding is flagged in `QUAL`.
