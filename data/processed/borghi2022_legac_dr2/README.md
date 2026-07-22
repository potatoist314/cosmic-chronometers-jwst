# Ready-to-use Borghi + LEGA-C tables

- `borghi2022_legac_dr2_spectrum_matches.tsv`: everything joined together (143 spectra for 140 galaxies).
- `borghi2022_legac_dr2_sigma_lt_215_spectrum_matches.tsv`: low-dispersion spectra, `sigma < 215 km/s` (71 rows).
- `borghi2022_legac_dr2_sigma_gt_215_spectrum_matches.tsv`: high-dispersion spectra, `sigma > 215 km/s` (72 rows).
- `borghi2022_legac_dr2_sigma_split_object_audit.tsv`: one row per galaxy showing whether its spectra agree on the split.
- Galaxies 124233 and 219831 have repeat spectra on opposite sides of 215 km/s, so they are marked ambiguous.
- Each joined row includes age, redshift, velocity dispersion, Lick indices, errors, and quality flags.
- Missing measurements are `NaN`; units are written in the column names.
- Rebuild everything with `.venv/bin/python scripts/build_borghi2022_legac_dr2_subset.py`.
