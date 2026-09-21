# Raw COSMOS2020 photometry

- Files: `cosmos2020_classic_legac_dr2_1arcsec.fits`, 1931 rows, 763 columns; `cosmos2020_farmer_legac_dr2_1arcsec.fits`, 1630 rows.
- Source: Weaver et al. (2022), ApJS 258, 11, arXiv:2110.13923.
- Retrieved every column via `astroquery` from VizieR:
  - `J/ApJS/258/11/classic`: `COSMOS2020_CLASSIC_R1_v2.1_p3`.
  - `J/ApJS/258/11/farmer`: `COSMOS2020_FARMER_R1_v2.2_p3`, correction dated 2023-03-29.
- Script: `uv run python scripts/download_cosmos2020_cosmos2025_legac_dr2_photometry.py`.
- Cross-match: all 1988 `RAJ2000`/`DECJ2000` rows in `data/raw/legac_dr2/legaCdr2.fits.gz`; radius 1 arcsec; nearest match kept; batches of 200.
- Rows are per LEGA-C spectrum.
- Downloaded 2026-09-21; do not edit.

## Catalogues

- [IRSA](https://irsa.ipac.caltech.edu/data/COSMOS/tables/cosmos2020/), not downloaded:
  - `COSMOS2020_CLASSIC_R1_v2.2_p3.fits.gz`: 3.9 GB.
  - `COSMOS2020_FARMER_R1_v2.2_p3.fits.gz`: 2.0 GB.
- IRSA transfer rate: 0.37 MB/s on 2026-09-21.
- DR4.1.1 release note: v2.2 changes Farmer magnitude errors only; Classic is unaffected.
- Also distributed through [cosmos2020.calet.org](https://cosmos2020.calet.org/) (registration form) and ESO Phase 3 (UltraVISTA DR4.1.1).

## Columns

- VizieR flux precision: 0.01 uJy; magnitudes: four decimals.
- `scripts/compare_cosmos_photometry.py` takes fluxes from magnitudes.
- Classic: 2″ and 3″ aperture fluxes in uJy; `totaloff2` / `totaloff3` give aperture-to-total offsets in mag per object.
- Classic IRAC (IRACLEAN) and GALEX fluxes are total.
- Farmer: total model fluxes; `FModel`: `0` = OK, `1` = failed to converge (null fluxes), `2` = drifted.
- Fluxes include neither Milky Way extinction correction nor zero-point offsets; Weaver et al. (2022) Table 3 lists the offsets.
- Flux errors include correlated-noise factors.

