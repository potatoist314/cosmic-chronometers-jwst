#!/usr/bin/env python3
"""Join Borghi et al. (2022) Table 4 to matching LEGA-C DR2 spectra."""

from __future__ import annotations

import csv
import math
from collections import Counter, defaultdict
from pathlib import Path

import astropy.units as u
import numpy as np
from astropy.coordinates import SkyCoord
from astropy.table import Table


PROJECT_ROOT = Path(__file__).resolve().parents[1]
BORGH_INPUT = PROJECT_ROOT / "data/raw/borghi2022/vizier_J-ApJ-927-164_table4.tsv"
LEGAC_INPUT = PROJECT_ROOT / "data/raw/legac_dr2/legaCdr2.fits.gz"
OUTPUT = (
    PROJECT_ROOT / "data/processed/borghi2022_legac_dr2/"
    "borghi2022_legac_dr2_spectrum_matches.tsv"
)
LOW_SIGMA_OUTPUT = (
    PROJECT_ROOT / "data/processed/borghi2022_legac_dr2/"
    "borghi2022_legac_dr2_sigma_lt_215_spectrum_matches.tsv"
)
HIGH_SIGMA_OUTPUT = (
    PROJECT_ROOT / "data/processed/borghi2022_legac_dr2/"
    "borghi2022_legac_dr2_sigma_gt_215_spectrum_matches.tsv"
)
SIGMA_AUDIT_OUTPUT = (
    PROJECT_ROOT / "data/processed/borghi2022_legac_dr2/"
    "borghi2022_legac_dr2_sigma_split_object_audit.tsv"
)

SIGMA_SPLIT_KM_S = 215.0


# CN1 and CN2 are magnitude-defined molecular indices; D4000_N is a ratio.
# The remaining public DR2 Lick indices are equivalent widths in angstroms.
LICK_COLUMNS = [
    ("LICK_CN1", "dr2_lick_cn1_mag"),
    ("LICK_CN2", "dr2_lick_cn2_mag"),
    ("LICK_CA4227", "dr2_lick_ca4227_angstrom"),
    ("LICK_G4300", "dr2_lick_g4300_angstrom"),
    ("LICK_FE4383", "dr2_lick_fe4383_angstrom"),
    ("LICK_CA4455", "dr2_lick_ca4455_angstrom"),
    ("LICK_FE4531", "dr2_lick_fe4531_angstrom"),
    ("LICK_C4668", "dr2_lick_c4668_angstrom"),
    ("LICK_HB", "dr2_lick_hb_angstrom"),
    ("LICK_HD_A", "dr2_lick_hd_a_angstrom"),
    ("LICK_HG_A", "dr2_lick_hg_a_angstrom"),
    ("LICK_HD_F", "dr2_lick_hd_f_angstrom"),
    ("LICK_HG_F", "dr2_lick_hg_f_angstrom"),
    ("LICK_D4000_N", "dr2_lick_d4000_n"),
]

DIRECT_DR2_COLUMNS = [
    ("z", "dr2_z_spec", ".6f"),
    ("SIGMA_STARS_PRIME", "dr2_sigma_stars_prime_km_s", ".1f"),
    ("SIGMA_STARS_PRIME_err", "dr2_sigma_stars_prime_err_km_s", ".1f"),
    ("f_primary", "dr2_f_primary", ".0f"),
    ("f_use", "dr2_f_use", ".0f"),
    ("f_spec", "dr2_f_spec", ".0f"),
    ("f_z", "dr2_f_z", ".0f"),
    ("f_ppxf", "dr2_f_ppxf", ".0f"),
    ("f_int", "dr2_f_int", ".0f"),
    ("SN", "dr2_sn_per_pixel", ".1f"),
    ("SN_RF_4000", "dr2_sn_rf_4000_per_pixel", ".1f"),
    ("SN_OBS_8030", "dr2_sn_obs_8030_per_pixel", ".1f"),
]

OUTPUT_COLUMNS = [
    "mms2013_id",
    "dr2_spect_id",
    "dr2_spectrum_filename",
    "dr2_observations_for_object",
    "dr2_ra_j2000_deg",
    "dr2_dec_j2000_deg",
    "match_separation_arcsec",
    "dr2_z_spec",
    "dr2_sigma_stars_prime_km_s",
    "dr2_sigma_stars_prime_err_km_s",
    "sigma_regime_215_km_s",
    "borghi_age_gyr",
    "borghi_age_err_lower_gyr",
    "borghi_age_err_upper_gyr",
    "borghi_z_over_h_dex",
    "borghi_z_over_h_err_lower_dex",
    "borghi_z_over_h_err_upper_dex",
    "borghi_alpha_over_fe_dex",
    "borghi_alpha_over_fe_err_lower_dex",
    "borghi_alpha_over_fe_err_upper_dex",
    *[output for _, output, _ in DIRECT_DR2_COLUMNS[3:]],
    *[name for source, output in LICK_COLUMNS for name in (output, f"{output}_err")],
]

SIGMA_AUDIT_COLUMNS = [
    "mms2013_id",
    "dr2_observations_for_object",
    "dr2_spect_ids",
    "dr2_sigma_stars_prime_values_km_s",
    "sigma_regime_215_km_s",
    "sigma_split_note",
]


def read_borghi_rows(path: Path) -> list[dict[str, str]]:
    lines = path.read_text(encoding="ascii").splitlines()
    header_index = next(
        i for i, line in enumerate(lines) if line.startswith("[MMS2013]\t")
    )
    reader = csv.DictReader(lines[header_index:], delimiter="\t")
    rows = [row for row in reader if row["[MMS2013]"].strip().isdigit()]
    ids = [int(row["[MMS2013]"].strip()) for row in rows]
    if len(ids) != 140 or len(set(ids)) != 140:
        raise ValueError(
            f"Expected 140 unique Borghi IDs, found {len(ids)} rows and "
            f"{len(set(ids))} unique IDs"
        )
    return rows


def format_number(value: object, format_spec: str = ".9g") -> str:
    if np.ma.is_masked(value):
        return "NaN"
    number = float(value)
    if not math.isfinite(number):
        return "NaN"
    return format(number, format_spec)


def borghi_number(row: dict[str, str], column: str) -> str:
    return format_number(float(row[column].strip()), ".3f")


def classify_sigma(value: object) -> str:
    if np.ma.is_masked(value):
        raise ValueError("Cannot apply the velocity-dispersion split to a masked value")
    sigma = float(value)
    if not math.isfinite(sigma):
        raise ValueError(
            "Cannot apply the velocity-dispersion split to a non-finite value"
        )
    if sigma < SIGMA_SPLIT_KM_S:
        return "low_sigma"
    if sigma > SIGMA_SPLIT_KM_S:
        return "high_sigma"
    raise ValueError(
        "A spectrum has sigma = 215 km/s, but the papers label the regimes "
        "with strict < and > inequalities"
    )


def write_tsv(
    path: Path,
    rows: list[dict[str, str | int]],
    columns: list[str],
    comments: list[str],
) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as handle:
        for comment in comments:
            handle.write(f"# {comment}\n")
        writer = csv.DictWriter(
            handle,
            fieldnames=columns,
            delimiter="\t",
            lineterminator="\n",
        )
        writer.writeheader()
        writer.writerows(rows)


def main() -> None:
    borghi_rows = read_borghi_rows(BORGH_INPUT)
    dr2 = Table.read(LEGAC_INPUT)

    required_dr2 = {
        "OBJECT",
        "SPECT_ID",
        "Filename",
        "RAJ2000",
        "DECJ2000",
        *[source for source, _, _ in DIRECT_DR2_COLUMNS],
        *[source for source, _ in LICK_COLUMNS],
        *[f"{source}_err" for source, _ in LICK_COLUMNS],
    }
    missing_columns = required_dr2.difference(dr2.colnames)
    if missing_columns:
        raise ValueError(f"LEGA-C DR2 input is missing columns: {missing_columns}")

    rows_by_id: dict[int, list[int]] = defaultdict(list)
    for index, object_id in enumerate(dr2["OBJECT"]):
        rows_by_id[int(object_id)].append(index)

    missing_ids = [
        int(row["[MMS2013]"].strip())
        for row in borghi_rows
        if not rows_by_id[int(row["[MMS2013]"].strip())]
    ]
    if missing_ids:
        raise ValueError(f"Borghi IDs missing from LEGA-C DR2: {missing_ids}")

    output_rows: list[dict[str, str | int]] = []
    separations: list[float] = []

    for borghi in borghi_rows:
        object_id = int(borghi["[MMS2013]"].strip())
        match_indices = sorted(
            rows_by_id[object_id], key=lambda i: str(dr2["SPECT_ID"][i])
        )
        borghi_coord = SkyCoord(
            float(borghi["RAJ2000"]) * u.deg,
            float(borghi["DEJ2000"]) * u.deg,
        )

        for index in match_indices:
            match = dr2[index]
            dr2_coord = SkyCoord(
                float(match["RAJ2000"]) * u.deg,
                float(match["DECJ2000"]) * u.deg,
            )
            separation = float(borghi_coord.separation(dr2_coord).arcsec)
            separations.append(separation)

            result: dict[str, str | int] = {
                "mms2013_id": object_id,
                "dr2_spect_id": str(match["SPECT_ID"]).strip(),
                "dr2_spectrum_filename": str(match["Filename"]).strip(),
                "dr2_observations_for_object": len(match_indices),
                "dr2_ra_j2000_deg": format_number(match["RAJ2000"], ".6f"),
                "dr2_dec_j2000_deg": format_number(match["DECJ2000"], ".6f"),
                "match_separation_arcsec": format(separation, ".6f"),
                "borghi_age_gyr": borghi_number(borghi, "Age"),
                "borghi_age_err_lower_gyr": borghi_number(borghi, "e16-Age"),
                "borghi_age_err_upper_gyr": borghi_number(borghi, "e84-Age"),
                "borghi_z_over_h_dex": borghi_number(borghi, "[Z/H]"),
                "borghi_z_over_h_err_lower_dex": borghi_number(borghi, "e16-[Z/H]"),
                "borghi_z_over_h_err_upper_dex": borghi_number(borghi, "e84-[Z/H]"),
                "borghi_alpha_over_fe_dex": borghi_number(borghi, "[a/Fe]"),
                "borghi_alpha_over_fe_err_lower_dex": borghi_number(
                    borghi, "e16-[a/Fe]"
                ),
                "borghi_alpha_over_fe_err_upper_dex": borghi_number(
                    borghi, "e84-[a/Fe]"
                ),
            }

            for source, output, format_spec in DIRECT_DR2_COLUMNS:
                result[output] = format_number(match[source], format_spec)
            result["sigma_regime_215_km_s"] = classify_sigma(match["SIGMA_STARS_PRIME"])
            for source, output in LICK_COLUMNS:
                result[output] = format_number(match[source], ".6f")
                result[f"{output}_err"] = format_number(match[f"{source}_err"], ".6f")

            output_rows.append(result)

    max_separation = max(separations)
    if max_separation > 0.1:
        raise ValueError(
            f"Largest coordinate separation is {max_separation:.3f} arcsec"
        )

    low_sigma_rows = [
        row for row in output_rows if row["sigma_regime_215_km_s"] == "low_sigma"
    ]
    high_sigma_rows = [
        row for row in output_rows if row["sigma_regime_215_km_s"] == "high_sigma"
    ]

    output_rows_by_object: dict[int, list[dict[str, str | int]]] = defaultdict(list)
    for row in output_rows:
        output_rows_by_object[int(row["mms2013_id"])].append(row)

    sigma_audit_rows: list[dict[str, str | int]] = []
    for object_id in sorted(output_rows_by_object):
        object_rows = sorted(
            output_rows_by_object[object_id], key=lambda row: str(row["dr2_spect_id"])
        )
        regimes = {str(row["sigma_regime_215_km_s"]) for row in object_rows}
        if len(regimes) == 1:
            object_regime = next(iter(regimes))
            note = (
                "single_spectrum"
                if len(object_rows) == 1
                else "repeat_spectra_agree_on_regime"
            )
        else:
            object_regime = "ambiguous_repeat_spectra"
            note = "repeat_spectra_straddle_215_km_s"

        sigma_audit_rows.append(
            {
                "mms2013_id": object_id,
                "dr2_observations_for_object": len(object_rows),
                "dr2_spect_ids": ";".join(
                    str(row["dr2_spect_id"]) for row in object_rows
                ),
                "dr2_sigma_stars_prime_values_km_s": ";".join(
                    str(row["dr2_sigma_stars_prime_km_s"]) for row in object_rows
                ),
                "sigma_regime_215_km_s": object_regime,
                "sigma_split_note": note,
            }
        )

    write_tsv(
        OUTPUT,
        output_rows,
        OUTPUT_COLUMNS,
        [
            "One row per matching LEGA-C DR2 spectrum record; repeated objects are retained.",
            "The paper split is low_sigma for sigma < 215 km/s and high_sigma for sigma > 215 km/s.",
            "Missing source values are written as NaN.",
        ],
    )
    split_comments = [
        "Spectrum-level subset of the Borghi (2022)-LEGA-C DR2 match.",
        "The 215 km/s split uses the measured SIGMA_STARS_PRIME point estimate, as in the papers.",
        "Repeat spectra are retained; consult the object audit before treating rows as unique galaxies.",
        "Missing source values are written as NaN.",
    ]
    write_tsv(
        LOW_SIGMA_OUTPUT,
        low_sigma_rows,
        OUTPUT_COLUMNS,
        [
            "Paper velocity-dispersion regime: sigma < 215 km/s (low_sigma).",
            *split_comments,
        ],
    )
    write_tsv(
        HIGH_SIGMA_OUTPUT,
        high_sigma_rows,
        OUTPUT_COLUMNS,
        [
            "Paper velocity-dispersion regime: sigma > 215 km/s (high_sigma).",
            *split_comments,
        ],
    )
    write_tsv(
        SIGMA_AUDIT_OUTPUT,
        sigma_audit_rows,
        SIGMA_AUDIT_COLUMNS,
        [
            "One row per unique Borghi (2022) galaxy.",
            "ambiguous_repeat_spectra means public DR2 repeat spectra fall on opposite sides of 215 km/s.",
            "No preferred repeat-spectrum SPECT_ID is documented in the papers, so no silent object-level assignment is made.",
        ],
    )

    repeated = sum(
        len(rows_by_id[int(row["[MMS2013]"].strip())]) > 1 for row in borghi_rows
    )
    audit_counts = Counter(
        str(row["sigma_regime_215_km_s"]) for row in sigma_audit_rows
    )
    print(
        f"Wrote {len(output_rows)} DR2 spectrum records for "
        f"{len(borghi_rows)} Borghi objects to {OUTPUT.relative_to(PROJECT_ROOT)}"
    )
    print(
        f"Spectrum-level sigma split: {len(low_sigma_rows)} low (<215), "
        f"{len(high_sigma_rows)} high (>215)"
    )
    print(
        "Object-level audit: "
        f"{audit_counts['low_sigma']} low, {audit_counts['high_sigma']} high, "
        f"{audit_counts['ambiguous_repeat_spectra']} ambiguous"
    )
    print(f"Objects with repeated DR2 spectra: {repeated}")
    print(f"Maximum coordinate separation: {max_separation:.6f} arcsec")


if __name__ == "__main__":
    main()
