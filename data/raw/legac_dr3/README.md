# Raw LEGA-C DR3 data

- Main file: `legac_DR3.fits`.
- It contains 4,081 spectra of 3,741 galaxies and 112 catalogue columns.
- A galaxy can have multiple spectra; `SPECT_ID` (mask number + target ID) identifies each spectrum, unchanged for spectra shared with DR2.
- `ESO_DR3_release_description.pdf` documents release content and catalogue columns: [ESO release description 185](https://www.eso.org/rm/api/v1/public/releaseDescriptions/185).
- Source: ESO archive, collection LEGA-C; listed by <https://archive.eso.org/tap_obs>, served by `https://dataportal.eso.org/dataPortal/file/<archive id>`.
- Paper: van der Wel et al. (2021), ApJS 256, 44, arXiv:2108.00744.
- Downloaded on 2026-11-11 with `ceridwen/.venv/bin/python scripts/download_legac_dr3.py`; do not edit these raw files. Re-run to restore; existing files are skipped.
- Column changes: `Z` replaces `z`; `SIGMA_STARS_PRIME_ERR` replaces `SIGMA_STARS_PRIME_err`; other DR2 `_err` suffixes become `_ERR`.
- No `f_use`, `f_ppxf`, `f_z`, `f_spec`, or `f_int`.
- `FLAG_PRIMARY`: 1 primary target, 0 filler.
- `FLAG_SPEC`: 0 good, 1 mid-IR/X-ray AGN, 2 photometric flux calibration error.
- `FLAG_MORPH`: 0 good, 1 unresolved multiple or irregular, 2 secondary at different z (van der Wel et al. 2021, Sect. 4.2).
- DR3 excludes 72 DR2 spectra: stars and failed spectra.
- All DR1/DR2 spectra were re-reduced (van der Wel et al. 2021, Sect. 2.2): HST Sérsic–Moffat extraction; per-mask H2O/O2 telluric templates, shifted/smoothed per galaxy, with variance propagation.
- Calibration uses bagpipes UltraVISTA BVrizYJ fits, revised zero points, and fifth-order Legendre template/spectrum corrections to spectrum and variance. DR2 used FAST and fifth-order polynomials (Straatman et al. 2018, Sect. 2).
- The release description says fifteenth-order calibration; the paper uses fifteenth-order only for index modelling.
- Catalogue uncertainties are scaled by 1.25–2 from duplicates (van der Wel et al. 2021, Appendix C).

## `sp/` — the 1D spectra

- 4,081 files, one per catalogue row, ~627 MB total.
- Filenames follow `Filename`, e.g. `legac_M1_210210_v3.0.fits`.
- Gitignored: too large to track.
- Format: HDU 1, single-row binary table; `data['WAVE'][0]`.
- Columns: `WAVE` (angstrom, dry air, topocentric), `FLUX`/`ERR` (1e-19 erg s-1 cm-2 angstrom-1), `QUAL`.
- `QUAL = 1`: discard; accompanies `ERR = 0`.
- Header: `SPEC_RES = 2500`.