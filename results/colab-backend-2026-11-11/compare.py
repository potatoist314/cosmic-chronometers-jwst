"""Test fits (Colab, and the fit handed over to Modal) against the stored Modal fits of the same galaxy,
seed and source; writes comparison.csv.

Run from the project root: ceridwen/.venv/bin/python results/colab-backend-2026-11-11/compare.py
"""
import csv
import json
from pathlib import Path

import h5py
import numpy as np

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
# (test run, stored Modal run, fit directory under fits/)
PAIRS = [
    ('reference/run', 'results/cn-response-2026-11-10/legac-reference/run', 'baseline/210210-M1_210210'),
    *[('resume/run', 'results/carbon-mask-2026-11-08/check/run', f'baseline/{fit}')
      for fit in ('160400-M8_160400', '232005-M9_232005', '113852-M7_113852', '184916-M12_184916')],
    *[('handover/run', 'results/carbon-mask-2026-11-08/check/run', f'baseline/{fit}')
      for fit in ('210210-M1_210210', '117694-M3_117694')],
]


def card(run, fit):
    """(backend, GPU) of the last attempt that fitted the cell; a hand-over keeps the Colab attempts in 'colab'."""
    manifest = json.loads((run / 'manifest.json').read_text())
    name = f"{fit.split('/')[0]}/{fit.split('-', 1)[1]}"
    for backend, attempts in ((manifest['backend'], manifest['attempts']),
                              ('colab', [a for c in manifest.get('colab', []) for a in c['attempts']])):
        fitted = [a for a in attempts if name in a.get('cells', {})]
        if fitted:
            return backend, fitted[-1]['cells'][name].get('gpu_name') or fitted[-1]['gpu_name'].split(',')[0]


def quantiles(directory):
    with h5py.File(directory / 'ceridwen_derived_outputs.h5') as derived:
        summary = derived['summary']
        names = [n.decode() if isinstance(n, bytes) else str(n) for n in summary['parameter'][()]]
        return dict(zip(names, zip(summary['q16'][()], summary['q50'][()], summary['q84'][()])))


rows = []
for colab_run, modal_run, fit in PAIRS:
    a, b = HERE / colab_run / 'fits' / fit, ROOT / modal_run / 'fits' / fit
    if not a.is_dir():
        continue
    with h5py.File(a / 'ceridwen_result.h5') as fa, h5py.File(b / 'ceridwen_result.h5') as fb:
        sa, sb = dict(fa['samples'].attrs), dict(fb['samples'].attrs)
        parameters = [n for n in fb['samples'] if not n.startswith('log_likelihoods') and n != 'log_weights']
        identical = all(fa['samples'][n][()].tobytes() == fb['samples'][n][()].tobytes() for n in parameters)
        relative = 0.0
        for n in fb['samples']:
            x, y = fa['samples'][n][()], fb['samples'][n][()]
            if x.shape != y.shape:
                relative = float('nan')  # another sampler path: the dead points differ in number
                break
            finite = np.isfinite(x) & np.isfinite(y)
            relative = max(relative, float(np.max(np.abs(x[finite] - y[finite])
                                                  / np.maximum(np.abs(y[finite]), 1e-300), initial=0.0)))
    qa, qb = quantiles(a), quantiles(b)
    shifts = {n: abs(qa[n][1] - q50) / ((q84 - q16) / 2) for n, (q16, q50, q84) in qb.items() if n in qa and q84 > q16}
    worst = max(shifts, key=shifts.get)
    rows.append({
        'fit': fit, 'test_run': f'results/colab-backend-2026-11-11/{colab_run}', 'stored_run': modal_run,
        'test_backend': card(HERE / colab_run, fit)[0], 'test_gpu': card(HERE / colab_run, fit)[1],
        'stored_gpu': card(ROOT / modal_run, fit)[1],
        'likelihood_calls_test': int(sa['n_likelihood_calls']), 'likelihood_calls_stored': int(sb['n_likelihood_calls']),
        'same_sampler_path': sa['n_likelihood_calls'] == sb['n_likelihood_calls'] and sa['n_samples'] == sb['n_samples'],
        'parameter_samples_bit_identical': identical,
        'max_relative_difference_same_path': f'{relative:.3g}',
        'lnZ_test': f"{sa['log_evidence']:.6f}", 'lnZ_stored': f"{sb['log_evidence']:.6f}",
        'lnZ_difference': f"{sa['log_evidence'] - sb['log_evidence']:+.4g}",
        'lnZ_difference_over_stored_error': f"{(sa['log_evidence'] - sb['log_evidence']) / sb['log_evidence_err']:+.3f}",
        'max_median_shift_sigma': f'{shifts[worst]:.3g}', 'max_shift_parameter': worst if shifts[worst] else '',
    })

with open(HERE / 'comparison.csv', 'w', newline='') as out:
    writer = csv.DictWriter(out, fieldnames=list(rows[0]))
    writer.writeheader()
    writer.writerows(rows)
for row in rows:
    print(', '.join(f'{k}={v}' for k, v in row.items() if k not in ('test_run', 'stored_run')))
