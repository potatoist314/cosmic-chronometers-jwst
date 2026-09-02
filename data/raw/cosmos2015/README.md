# Raw COSMOS2015 photometry

Rest-frame absolute magnitudes for the NUVrJ diagram in Borghi et al. (2022a)
Figure 1, upper-left panel. LEGA-C DR2 carries no photometry, so Paper I §2
takes these colors from COSMOS2015.

- Main file: `cosmos2015_legac_dr2_xmatch_1arcsec.fits`, 1985 rows.
- Source catalogue: Laigle et al. (2016), ApJS 224, 24.
- Retrieved from VizieR `J/ApJS/224/24/cosmos2015` via `astroquery`.
- Positional cross-match against all 1988 `RAJ2000`/`DECJ2000` entries in
  `data/raw/legac_dr2/legaCdr2.fits.gz`, radius 1 arcsec, queried in batches of
  200. Rows are per LEGA-C *spectrum*, so galaxies with repeat spectra appear
  more than once.
- Downloaded on 2026-07-29; do not edit these raw files.

## Columns

`RAJ2000`, `DEJ2000`, `NUVMag` (M_NUV), `RMag` (M_r), `JMag` (M_J), `NUV-R`
(dust-corrected M_NUV − M_r at zPDF), `zPDF`, `MassMed`, `OType`.

Absolute magnitudes use `-99.99` as a null. `NUV-R` uses `-999.9`.

## Known discrepancy

Applying the Ilbert et al. (2013) cut — (NUV−r) > 3(r−J) + 1 and (NUV−r) > 3.1 —
to `NUVMag − RMag` and `RMag − JMag` selects 750 sources. Paper I reports 658 in
its photometric passive sample. The gap is unexplained; candidates are the
`NUV-R` dust-corrected column rather than the raw magnitude difference, the
quality flags Paper I applies before the color cut, and the fact that these rows
are per spectrum rather than per galaxy.

## `cosmos2015_legac_dr2_apertures_1arcsec.fits`

Same cross-match, 1982 rows, downloaded on 2026-09-02 with
`uv run python scripts/download_legac_dr2_aperture_photometry.py`. Columns: the
2" and 3" aperture fluxes and errors of u, B, V, r, i+, z++, Y, J, H, Ks (uJy),
the total IRAC 3.6 and 4.5 um fluxes, the per-object aperture-to-total
magnitude offset `Offset` (`MAG_AUTO - MAG_APER3`, negative), `E(B-V)`, the
Ks AUTO magnitude and the quality flags. Laigle et al. (2016) Table 3 gives the
per-band systematic offsets and extinction factors that complete the total
magnitude; `scripts/calibration_polynomial_experiment.py` carries them.
