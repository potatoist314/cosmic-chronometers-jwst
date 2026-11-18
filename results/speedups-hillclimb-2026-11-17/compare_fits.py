"""Full-fit check of two fits of one galaxy: posterior medians, widths and ln Z.

    compare_fits.py REFERENCE_FIT_DIR TEST_FIT_DIR [more pairs ...]

A fit directory holds ceridwen_result.h5 and execution.log.  sigma is half the 16-84 % range
of the reference fit.
"""
import re
import sys
from pathlib import Path

import h5py
import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parents[2] / 'scripts'))
from absorption_mask_analysis import weighted_quantiles


def summary(directory):
    directory = Path(directory)
    rows = {}
    with h5py.File(directory / 'ceridwen_result.h5') as handle:
        samples = handle['samples']
        log_weights = samples['log_weights'][()]
        for name in samples:
            if name.startswith('log_'):
                continue
            values = samples[name][()].reshape(len(log_weights), -1)
            for column in range(values.shape[1]):
                rows[f'{name}[{column}]' if values.shape[1] > 1 else name] = weighted_quantiles(
                    values[:, column], log_weights)
        weights = np.exp(log_weights - log_weights.max())
        rows['log_f_calib'] = weighted_quantiles(samples['log_f_calib'][()].ravel(), log_weights)
        effective = weights.sum() ** 2 / (weights ** 2).sum()
    lnz, error = map(float, re.findall(r'ln Z: ([-\d.]+) \+/- ([\d.]+)',
                                       (directory / 'execution.log').read_text())[-1])
    return rows, lnz, error, effective


def compare(reference, test):
    a, lnz_a, error_a, n_a = summary(reference)
    b, lnz_b, error_b, n_b = summary(test)
    shift = {name: (b[name][1] - a[name][1]) / (.5 * (a[name][2] - a[name][0])) for name in a}
    width = {name: (b[name][2] - b[name][0]) / (a[name][2] - a[name][0]) - 1. for name in a}
    worst_shift = max(shift, key=lambda name: abs(shift[name]))
    worst_width = max(width, key=lambda name: abs(width[name]))
    values = np.abs(np.array(list(shift.values())))
    return (f'max |median shift| {abs(shift[worst_shift]):.3f} sigma ({worst_shift}), rms {np.sqrt((values ** 2).mean()):.3f}; '
            f'max |width change| {100 * abs(width[worst_width]):.1f} % ({worst_width}); '
            f'ln Z {lnz_a:.3f} +/- {error_a:.3f} -> {lnz_b:.3f} +/- {error_b:.3f} (delta {lnz_b - lnz_a:+.3f}); '
            f'effective samples {n_a:.0f}, {n_b:.0f}')


if __name__ == '__main__':
    for reference, test in zip(sys.argv[1::2], sys.argv[2::2]):
        print(f'{reference}\n -> {test}\n    {compare(reference, test)}')
