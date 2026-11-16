#!/usr/bin/env python3
"""C/N-free fits of the common-window chronometer mocks: recoveries, slopes, and the paired difference from the plain fits.

The mocks, truths, design and the plain per-mock table are those of results/mock-chronometer-window-2026-11-13.
"""
from __future__ import annotations

import csv
import json
from pathlib import Path
import sys

import h5py
import numpy as np

OUT = Path(__file__).resolve().parent
PLAIN = OUT.parent / "mock-chronometer-window-2026-11-13"
sys.path.insert(0, str(PLAIN))
import mocks as m  # noqa: E402  (sets the CPU JAX environment and the project root)

from ceridwen.fit import load_result_h5  # noqa: E402
from scripts.absorption_mask_analysis import weighted_quantiles  # noqa: E402  (as window-194-fits.csv)
from scripts.experiment import validate_result  # noqa: E402

ARM = "mock_cn_free_w"


def column(rows, name):
    return np.array([r[name] for r in rows], dtype=float)


def per_mock():
    """The rows of the plain per-mock table, from the C/N-free fits, with the C and N quantiles added."""
    rows = []
    for row in m.read_design():
        found = list((OUT / "runs").glob(f'*/fits/{ARM}/{row["object_id"]}-{row["target"]}'))
        if not found:
            continue
        directory, = found
        validate_result(directory)
        truth = json.loads((PLAIN / "truths" / f'{row["target"]}.json').read_text())
        assert m.sha(m.ROOT / truth["mock"]) == truth["mock_sha256"]
        data = np.load(m.ROOT / truth["mock"])
        with h5py.File(directory / "ceridwen_derived_outputs.h5") as stored:
            assert int(stored.attrs["random_seed"]) == m.FIT_SEED and float(stored.attrs["redshift"]) == row["z"]
            mask = np.asarray(stored["spectrum/mask"])
            np.testing.assert_array_equal(mask, data["spectrum_mask"])
            np.testing.assert_array_equal(np.asarray(stored["spectrum/observed"])[mask], data["spectrum_flux"][mask])
            np.testing.assert_array_equal(np.asarray(stored["photometry/observed"]), data["photometry_flux"])
            names = stored["summary/parameter"].asstr()[:]
            q = {k: dict(zip(names, stored[f"summary/{k}"][:])) for k in ("q16", "q50", "q84")}
        age = [float(q[k]["mass-weighted age [Gyr]"]) for k in q]
        fit = load_result_h5(directory / "ceridwen_result.h5")
        abundances = {f"{p}_{k}": v for p in ("cfe", "nfe") for k, v in zip(
            ("q16", "q50", "q84"), weighted_quantiles(np.asarray(fit.samples[p]).ravel(), np.asarray(fit.log_weights)))}
        rows.append(dict(rank=row["rank"], target=row["target"], shape=row["shape"], subset=row["subset"], z=row["z"],
                         sn=truth["sn_mock_statistical"], true_age_gyr=truth["true_age_gyr"],
                         ssp_weight_age_gyr=truth["ssp_weight_age_gyr"], age_q16=age[0],
                         age_q50=age[1], age_q84=age[2], age_bias_gyr=age[1] - truth["true_age_gyr"],
                         age_truth_inside=age[0] <= truth["true_age_gyr"] <= age[2],
                         afe_q50=float(q["q50"]["afe"]), afe_bias=float(q["q50"]["afe"]) - m.TRUE_AFE,
                         feh_q50=float(q["q50"]["logzsol"]), feh_bias=float(q["q50"]["logzsol"]) - m.TRUE_FEH,
                         path=str(directory.relative_to(m.ROOT)), **abundances))
    return rows


def slope_row(group, chosen):
    """One row of the plain slopes.csv."""
    z, age, true, bias = (column(chosen, n) for n in ("z", "age_q50", "true_age_gyr", "age_bias_gyr"))
    fit, exact = m.line_fit(z, age), m.line_fit(z, true)
    return dict(group=group, mocks=len(chosen), true_slope=exact["slope"], recovered_slope=fit["slope"],
                slope_q16=fit["q16"], slope_q84=fit["q84"], slope_q025=fit["q025"], slope_q975=fit["q975"],
                recovered_over_true=fit["slope"] / exact["slope"], residual_scatter_gyr=fit["scatter"],
                median_age_bias_gyr=float(np.median(bias)), mean_age_bias_gyr=float(bias.mean()),
                age_truth_inside=int(sum(str(r["age_truth_inside"]) == "True" for r in chosen)),
                median_afe_bias=float(np.median(column(chosen, "afe_bias"))),
                median_feh_bias=float(np.median(column(chosen, "feh_bias"))))


def spread(values):
    """Median, 16% and 84% of the mocks, mean and its standard error."""
    q = np.quantile(values, [0.5, 0.16, 0.84])
    return dict(median=float(q[0]), q16=float(q[1]), q84=float(q[2]), mean=float(values.mean()),
                standard_error=float(values.std(ddof=1) / np.sqrt(len(values))))


def main():
    free = per_mock()
    m.table(OUT / "per-mock.csv", free)
    plain_rows = {r["target"]: r for r in csv.DictReader((PLAIN / "per-mock.csv").open())}
    plain = [plain_rows[r["target"]] for r in free]  # the plain fits of the same mocks
    groups = [(g, [i for i, r in enumerate(free) if g in ("all", r["shape"])]) for g in ("all", *m.SHAPES)]
    groups = [(g, index) for g, index in groups if len(index) >= 5]

    slopes, paired_slopes = [], []
    for group, index in groups:
        a, b = [free[i] for i in index], [plain[i] for i in index]
        row = slope_row(group, a)
        slopes.append(dict(row, median_cfe=float(np.median(column(a, "cfe_q50"))),
                           median_nfe=float(np.median(column(a, "nfe_q50")))))
        reference = slope_row(group, b)
        # The slope is linear in the ages: the slope of the age difference is the paired slope difference.
        difference = m.line_fit(column(a, "z"), column(a, "age_q50") - column(b, "age_q50"))
        summary = dict(group=group, mocks=len(index), true_slope=row["true_slope"],
                       plain_slope=reference["recovered_slope"], plain_slope_q16=reference["slope_q16"],
                       plain_slope_q84=reference["slope_q84"], plain_over_true=reference["recovered_over_true"],
                       cn_free_slope=row["recovered_slope"], cn_free_slope_q16=row["slope_q16"],
                       cn_free_slope_q84=row["slope_q84"], cn_free_over_true=row["recovered_over_true"],
                       slope_difference=difference["slope"], slope_difference_q16=difference["q16"],
                       slope_difference_q84=difference["q84"], slope_difference_q025=difference["q025"],
                       slope_difference_q975=difference["q975"])
        for label, name in (("age_bias_gyr", "age_bias_gyr"), ("afe_bias", "afe_bias"), ("feh_bias", "feh_bias")):
            change = spread(column(a, name) - column(b, name))
            summary |= {f"plain_median_{label}": float(np.median(column(b, name))),
                        f"cn_free_median_{label}": float(np.median(column(a, name))),
                        **{f"{label}_difference_{k}": v for k, v in change.items()}}
        for p in ("cfe", "nfe"):
            summary |= {f"{p}_{k}": v for k, v in spread(column(a, f"{p}_q50")).items()}
            summary[f"{p}_zero_inside"] = int(sum(r[f"{p}_q16"] <= 0.0 <= r[f"{p}_q84"] for r in a))
        paired_slopes.append(summary)
    m.table(OUT / "slopes.csv", slopes)
    m.table(OUT / "paired-slopes.csv", paired_slopes)
    m.table(OUT / "paired-per-mock.csv", [dict(
        rank=a["rank"], target=a["target"], shape=a["shape"], z=a["z"], sn=a["sn"], true_age_gyr=a["true_age_gyr"],
        plain_age_q50=float(b["age_q50"]), cn_free_age_q50=a["age_q50"],
        age_difference_gyr=a["age_q50"] - float(b["age_q50"]),
        plain_afe_q50=float(b["afe_q50"]), cn_free_afe_q50=a["afe_q50"], afe_difference=a["afe_q50"] - float(b["afe_q50"]),
        plain_feh_q50=float(b["feh_q50"]), cn_free_feh_q50=a["feh_q50"], feh_difference=a["feh_q50"] - float(b["feh_q50"]),
        **{k: a[k] for k in ("cfe_q16", "cfe_q50", "cfe_q84", "nfe_q16", "nfe_q50", "nfe_q84")},
        plain_path=b["path"], cn_free_path=a["path"]) for a, b in zip(free, plain)])
    for r in paired_slopes:
        print(f'{r["group"]:9s} N {r["mocks"]:3d}: truth {r["true_slope"]:+.3f}; plain {r["plain_slope"]:+.3f} '
              f'[{r["plain_slope_q16"]:+.3f}, {r["plain_slope_q84"]:+.3f}] ratio {r["plain_over_true"]:.3f}; C/N-free '
              f'{r["cn_free_slope"]:+.3f} [{r["cn_free_slope_q16"]:+.3f}, {r["cn_free_slope_q84"]:+.3f}] ratio '
              f'{r["cn_free_over_true"]:.3f}; difference {r["slope_difference"]:+.3f} [{r["slope_difference_q16"]:+.3f}, '
              f'{r["slope_difference_q84"]:+.3f}] (95% {r["slope_difference_q025"]:+.3f}, {r["slope_difference_q975"]:+.3f})')
        print(f'          age bias plain {r["plain_median_age_bias_gyr"]:+.3f}, C/N-free {r["cn_free_median_age_bias_gyr"]:+.3f}, '
              f'difference {r["age_bias_gyr_difference_mean"]:+.3f} +/- {r["age_bias_gyr_difference_standard_error"]:.3f} Gyr; '
              f'[a/Fe] bias plain {r["plain_median_afe_bias"]:+.3f}, C/N-free {r["cn_free_median_afe_bias"]:+.3f}, '
              f'difference {r["afe_bias_difference_mean"]:+.3f} +/- {r["afe_bias_difference_standard_error"]:.3f}; '
              f'[C/Fe] {r["cfe_median"]:+.3f} [{r["cfe_q16"]:+.3f}, {r["cfe_q84"]:+.3f}], '
              f'[N/Fe] {r["nfe_median"]:+.3f} [{r["nfe_q16"]:+.3f}, {r["nfe_q84"]:+.3f}]')


if __name__ == "__main__":
    main()
