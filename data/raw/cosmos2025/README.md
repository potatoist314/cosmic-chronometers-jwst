# Raw COSMOS2025 (COSMOS-Web DR1) photometry

- File: `cosmos2025_phot_legac_dr2_1arcsec.fits`, 1258 rows.
- Source: Shuntov et al. (2025), A&A 704, A339, arXiv:2506.03243.
- Retrieved every column from VizieR `J/A+A/704/A339/phot` via `astroquery`.
- Script: `uv run python scripts/download_cosmos2020_cosmos2025_legac_dr2_photometry.py`.
- Cross-match: all 1988 `RAJ2000`/`DECJ2000` rows in `data/raw/legac_dr2/legaCdr2.fits.gz`; radius 1 arcsec; nearest match kept; batches of 200.
- Rows are per LEGA-C spectrum.
- Downloaded 2026-09-21; do not edit.
- Footprint: JWST COSMOS-Web, 0.54 deg²; MIRI, 0.2 deg².
- LEGA-C rows outside the footprint have no match.

## Catalogue

- `COSMOSWeb_mastercatalog_v1.1.fits` at [cosmos2025.iap.fr](https://cosmos2025.iap.fr/); name, email and CAPTCHA required; not downloaded.
- v1.1 (2026-05-04): recomputed photometry and photo-z following MIRI photometry corrections in tiles B5, B9 and B10.
- VizieR does not state the catalogue version.

## Columns

- `Flux-mod-<band>`: total SE++ model flux in uJy.
- `e_Flux-u-mod`: uncalibrated error; `e_Flux-c-mod`: calibrated error.
- Null: `-998`; secure selection: `warn-flag = 0`.
- Bands: CFHT u*; HSC g r i z y + 3 NB; UltraVISTA Y J H Ks NB118; Suprime-Cam 12 IA/IB + 2 NB; IRAC ch1–4; HST F814W; NIRCam F115W F150W F277W F444W; MIRI F770W.
- No GALEX or `E(B-V)` column.
