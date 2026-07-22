## Data

- `data/raw/borghi2022/` — the 140-object machine-readable Table 4 of stellar
  population properties from Borghi et al. (2022), downloaded from VizieR.
  The directory README records the paper and dataset DOIs, retrieval details,
  checksum, and the fact that redshifts are not included in this table.
- `data/raw/legac_dr2/` — the complete 1,988-spectrum LEGA-C DR2 FITS
  catalogue, its VizieR ReadMe, and ESO's release documentation.
- `data/processed/borghi2022_legac_dr2/` — the reproducible match of the 140
  Borghi objects to DR2 redshifts, stellar velocity dispersions, public
  Lick/IDS indices, uncertainties, and quality flags, plus the paper's strict
  low/high velocity-dispersion split at 215 km/s and an object-level audit of
  repeat spectra that cross the threshold.

Rebuild the matched table with:

```text
.venv/bin/python scripts/build_borghi2022_legac_dr2_subset.py
```

## External resources

- `external/CCcovariance/` (git submodule, https://gitlab.com/mmoresco/CCcovariance) —
  Moresco's reference implementation for estimating the cosmic chronometer
  statistical + systematic covariance matrix (metallicity, residual young
  component, SFH/IMF/stellar library/SPS model terms), with example notebooks
  and the underlying `H(z)` data tables. Relevant to Phase 2 (published
  cosmic-chronometer reproduction) and to treating covariance explicitly per
  `AGENTS.md`.

  After cloning this repository, initialize it with:

  ```
  git submodule update --init --recursive
  ```
