# Raw LEGA-C DR2 data

- Main file: `legaCdr2.fits.gz`.
- It contains 1,988 spectra with redshifts, velocity dispersions, Lick indices, and errors.
- A galaxy can have more than one spectrum; `SPECT_ID` identifies each spectrum.
- `VizieR_ReadMe.txt` explains the catalogue columns.
- `ESO_DR2_release_description.pdf` is the official ESO documentation.
- Source: <https://doi.org/10.18727/archive/39>
- Downloaded on 2026-07-21; do not edit these raw files.
- Rebuild the processed tables with `.venv/bin/python scripts/build_borghi2022_legac_dr2_subset.py`.
