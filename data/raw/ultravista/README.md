# Raw UltraVISTA photometry (Muzzin et al. 2013)

The photometric SED that LEGA-C DR2 used to flux-calibrate every spectrum
(ESO DR2 release description, "Data Reduction and Calibration").

- Main file: `ultravista_legac_dr2_1arcsec.fits`, 1988 rows, one per LEGA-C
  DR2 spectrum (`LEGAC_INDEX` is the row number in `legaCdr2.fits.gz`).
- Source catalogue: Muzzin et al. (2013), ApJS 206, 8, VizieR `J/ApJS/206/8/catalog`.
- Nearest match within one arcsecond of `RAJ2000`/`DECJ2000`; `MATCH_SEP_ARCSEC`
  records the separation. `Seq` equals the LEGA-C `OBJECT` id.
- Flux columns (u, B, V, r+, i+, z+, Y, J, H, Ks, IRAC 1-2 and the intermediate
  bands IA679, IB709, IA738, IA767, IB827) are the catalogue's 2.1" aperture
  fluxes on PSF-matched images,
  converted to microjansky (the catalogue zero point is 25 AB). Total flux in
  any band is `flux * FKstot / FKs`, as the catalogue ReadMe prescribes.
- Downloaded on 2026-09-02 with
  `uv run python scripts/download_legac_dr2_aperture_photometry.py`; gitignored,
  re-run the script to restore it. Do not edit these raw files.
