"""Posterior of a changed likelihood on the samples of a finished fit, without sampler noise.

    reweight.py RESULT.h5 BASE.npz CHANGED.npz

BASE.npz and CHANGED.npz are `lnl_check.py parts --step 1` outputs: ln L of two builds at every
stored sample.  The samples get the weight w * exp(ln L_changed - ln L_base); sigma is half
the 16-84 % range of the stored posterior.
"""
import sys
from pathlib import Path

import h5py
import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parents[2] / 'scripts'))
from absorption_mask_analysis import weighted_quantiles


def reweight(result, base, changed):
    a, b = np.load(base), np.load(changed)
    assert (a['rows'] == b['rows']).all()
    rows = a['rows']
    delta = b['lnl'] - a['lnl']
    with h5py.File(result) as handle:
        samples = handle['samples']
        log_weights = samples['log_weights'][()][rows]
        weight = np.exp(log_weights - log_weights.max())
        used = weight > 1e-12 * weight.max()
        shift, width, trend = {}, {}, {}
        for name in samples:
            if name in ('log_weights', 'log_likelihoods', 'log_likelihoods_birth'):
                continue
            values = samples[name][()][rows].reshape(len(rows), -1)
            for column in range(values.shape[1]):
                before = weighted_quantiles(values[:, column], log_weights)
                after = weighted_quantiles(values[:, column], log_weights + delta)
                key = f'{name}[{column}]' if values.shape[1] > 1 else name
                shift[key] = (after[1] - before[1]) / (.5 * (before[2] - before[0]))
                width[key] = (after[2] - after[0]) / (before[2] - before[0]) - 1.
                if np.ptp(values[used, column]) > 0:
                    trend[key] = abs(np.corrcoef(delta[used], values[used, column])[0, 1])
    d = delta[used]
    theta_trend = max(abs(np.corrcoef(d, a['lnl'][used])[0, 1]), 0.)
    return {
        'samples': int(used.sum()),
        'max': float(np.abs(d).max()), 'rms': float(np.sqrt((d ** 2).mean())), 'mean': float(d.mean()),
        'relative': float(np.abs(d / a['lnl'][used]).max()),
        'corr_lnl': float(theta_trend),
        'corr_theta': max(trend.items(), key=lambda item: item[1]),
        'delta_lnz': float(np.log((weight[used] * np.exp(d)).sum() / weight[used].sum())),
        'shift': float(max(abs(v) for v in shift.values())),
        'width': float(max(abs(v) for v in width.values())),
    }


if __name__ == '__main__':
    out = reweight(*sys.argv[1:4])
    print(f"samples with weight {out['samples']}: delta ln L max {out['max']:.3e} rms {out['rms']:.3e} "
          f"mean {out['mean']:+.3e} relative {out['relative']:.2e} corr with ln L {out['corr_lnl']:.3f}, "
          f"largest |corr| with a parameter {out['corr_theta'][1]:.3f} ({out['corr_theta'][0]}); "
          f"reweighted: delta ln Z {out['delta_lnz']:+.2e}, max median shift {out['shift']:.1e} sigma, "
          f"max width change {100 * out['width']:.1e} %")
