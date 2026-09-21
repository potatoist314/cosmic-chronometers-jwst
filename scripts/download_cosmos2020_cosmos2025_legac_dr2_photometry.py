#!/usr/bin/env python3
"""Download COSMOS2020 and COSMOS2025 photometry matched to the LEGA-C DR2 catalogue."""

from pathlib import Path

import astropy.units as u
import numpy as np
from astropy.coordinates import SkyCoord
from astropy.table import Column, Table, vstack
from astroquery.vizier import Vizier


PROJECT_ROOT = Path(__file__).resolve().parents[1]
LEGAC_PATH = PROJECT_ROOT / "data/raw/legac_dr2/legaCdr2.fits.gz"
RAW = PROJECT_ROOT / "data/raw"
# VizieR table -> output file. Every column of each table is kept.
CATALOGS = {
    # Weaver et al. (2022), ApJS 258, 11; COSMOS2020_CLASSIC_R1_v2.1_p3
    "J/ApJS/258/11/classic": RAW / "cosmos2020/cosmos2020_classic_legac_dr2_1arcsec.fits",
    # Weaver et al. (2022); COSMOS2020_FARMER_R1_v2.2_p3, corrected 2023-03-29
    "J/ApJS/258/11/farmer": RAW / "cosmos2020/cosmos2020_farmer_legac_dr2_1arcsec.fits",
    # Shuntov et al. (2025), A&A 704, A339; COSMOS-Web DR1 photometry table
    "J/A+A/704/A339/phot": RAW / "cosmos2025/cosmos2025_phot_legac_dr2_1arcsec.fits",
}


def download_matches(legac: Table, catalog: str, batch_size: int = 200) -> Table:
    """Return each LEGA-C row's nearest match in `catalog` within one arcsecond."""
    coords = SkyCoord(legac["RAJ2000"], legac["DECJ2000"], unit="deg")
    vizier = Vizier(columns=["**", "_q"], row_limit=-1)
    matched_batches = []

    for start in range(0, len(legac), batch_size):
        stop = min(start + batch_size, len(legac))
        result = vizier.query_region(
            coords[start:stop], radius=1 * u.arcsec, catalog=catalog
        )
        if not result:
            continue

        candidates = result[0]
        candidates["LEGAC_INDEX"] = (
            np.asarray(candidates["_q"], dtype=int) - 1 + start
        )
        indices = np.asarray(candidates["LEGAC_INDEX"], dtype=int)
        candidate_coords = SkyCoord(
            candidates["RAJ2000"], candidates["DEJ2000"], unit="deg"
        )
        candidates["MATCH_SEP_ARCSEC"] = coords[indices].separation(
            candidate_coords
        ).arcsec

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
        matched_batches.append(candidates[np.sort(nearest)])

    photometry = vstack(matched_batches, metadata_conflicts="silent")
    indices = np.asarray(photometry["LEGAC_INDEX"], dtype=int)
    extra_columns = [
        ("OBJECT", np.asarray(legac["OBJECT"][indices])),
        ("SPECT_ID", np.asarray(legac["SPECT_ID"][indices]).astype(str)),
        ("LEGAC_RA_DEG", np.asarray(legac["RAJ2000"][indices])),
        ("LEGAC_DEC_DEG", np.asarray(legac["DECJ2000"][indices])),
    ]
    for position, (name, values) in enumerate(extra_columns, start=1):
        photometry.add_column(Column(values, name=name), index=position)

    photometry.meta["CATALOG"] = f"VizieR {catalog}"
    photometry.meta["MATCHRAD"] = "1 arcsec; nearest match retained"
    return photometry


def main() -> None:
    legac = Table.read(LEGAC_PATH)
    for catalog, output_path in CATALOGS.items():
        if output_path.exists():
            print(f"Already downloaded: {output_path.relative_to(PROJECT_ROOT)}")
            continue
        photometry = download_matches(legac, catalog)
        output_path.parent.mkdir(parents=True, exist_ok=True)
        photometry.write(output_path)
        print(
            f"Wrote {len(photometry)} matches to {output_path.relative_to(PROJECT_ROOT)}"
        )


if __name__ == "__main__":
    main()
