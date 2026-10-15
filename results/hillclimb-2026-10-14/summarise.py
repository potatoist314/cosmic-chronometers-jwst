"""Stage split, sampler numbers and result hashes of modal_ab.py or experiment.py run directories.

    ceridwen/.venv/bin/python summarise.py RUN_DIR [RUN_DIR ...]

An experiment.py output (manifest.json) is summarised end to end: driver wall time,
container seconds, Modal billed cost, and the fit stage from the retrieved files'
start time and the result file's modification time (tar keeps the container's clock).
"""
import hashlib
import json
import sys
from datetime import datetime
from pathlib import Path

import h5py
import numpy as np

STAGES = {2: 'imports', 4: 'data', 6: 'observations', 8: 'model', 10: 'sampler cell', 12: 'diagnostics',
          14: 'predictive', 16: 'spectrum fig', 18: 'calibration', 20: 'corner/sfh', 22: 'kl'}


def cell_times(notebook):
    cells = json.loads(notebook.read_text())['cells']
    parse = lambda s: datetime.fromisoformat(s.replace('Z', '+00:00')).timestamp()
    times, first, last = {}, None, None
    for index, cell in enumerate(cells):
        ex = cell.get('metadata', {}).get('execution', {})
        if 'iopub.execute_input' in ex and 'shell.execute_reply' in ex:
            a, b = parse(ex['iopub.execute_input']), parse(ex['shell.execute_reply'])
            first = a if first is None else first
            last = b
            times[STAGES.get(index, str(index))] = b - a
    return times, first, last


def result_hash(path):
    """sha256 over every samples/ dataset (dead points, lnL, weights) in name order, and over the
    dead-point parameters alone: GPU repeats of one build can share the parameters (the same
    sampler path) while lnL differs in rounding."""
    digest, parameters = hashlib.sha256(), hashlib.sha256()
    with h5py.File(path) as f:
        for name in sorted(f['samples']):
            data = name.encode() + np.ascontiguousarray(f['samples'][name][()]).tobytes()
            digest.update(data)
            if name not in ('log_likelihoods', 'log_likelihoods_birth', 'log_weights'):
                parameters.update(data)
        attrs = dict(f['samples'].attrs)
    return digest.hexdigest()[:16], parameters.hexdigest()[:16], attrs


def fit_row(fit, step):
    row = {'step': step['index'], 'copy': step.get('copy', 0), 'label': step['label'], 'target': fit.name,
           'rc': step['returncode'], 'process_s': round(step['end'] - step['start'], 1)}
    notebooks = list(fit.glob('*_executed.ipynb'))
    results = list(fit.glob('ceridwen_result.h5'))
    if notebooks:
        times, first, last = cell_times(notebooks[0])
        row['kernel_start_s'] = round(first - step['start'], 1)
        row['notebook_s'] = round(last - first, 1)
        row['after_kernel_s'] = round(step['end'] - last, 1)
        row.update({k: round(v, 1) for k, v in times.items() if v >= 0.05})
    if results:
        row.update(sampler_row(results[0]))
    return row


ESS_PARAMETERS = ('logzsol', 'afe', 'logmass', 't50')


def t50(logsfr_ratios, sfh_times_yr):
    """Median formation lookback (Gyr) per sample; mass fractions as the notebook's SFH cell."""
    sys.path.insert(0, str(Path(__file__).resolve().parents[2] / 'scripts'))
    from build_dr2_quiescent_summary import formation_times
    sfr = 10.0 ** np.concatenate([np.zeros((len(logsfr_ratios), 1)), -np.cumsum(logsfr_ratios, axis=1)], axis=1)
    lookback = sfh_times_yr / 1e9
    masses = 0.5 * (sfr[:, :-1] + sfr[:, 1:]) * np.diff(lookback)
    return formation_times(lookback, masses / masses.sum(axis=1)[:, None])[1]


def quantiles(path):
    """Weighted 16/50/84 per cent posterior quantiles of the ESS parameters."""
    with h5py.File(path) as f:
        data = {name: f['samples'][name][()] for name in ESS_PARAMETERS[:-1]}
        data['t50'] = t50(f['samples/logsfr_ratios'][()], f['model/sfh_times_yr'][()])
        lw = f['samples/log_weights'][()]
    w = np.exp(lw - lw.max())
    out = {}
    for name, x in data.items():
        order = np.argsort(x)
        cdf = np.cumsum(w[order]) / w.sum()
        out[name] = [round(float(np.interp(q, cdf, x[order])), 4) for q in (0.16, 0.5, 0.84)]
    return out


def parameter_ess(path, draws=200, seed=0):
    """Posterior variance over the variance of the posterior mean across simulated NS weight draws.

    anesthetic simulates the prior-volume compression (logw(nsamples)); this ESS counts only
    that noise, per parameter, with a fixed numpy seed so reruns agree. The reported ESS
    adds the Kish sampling term: 1/ESS = 1/Kish + 1/ESS_compression.
    """
    from anesthetic import NestedSamples
    with h5py.File(path) as f:
        data = {name: f['samples'][name][()] for name in ESS_PARAMETERS[:-1]}
        data['t50'] = t50(f['samples/logsfr_ratios'][()], f['model/sfh_times_yr'][()])
        logl, birth = f['samples/log_likelihoods'][()], f['samples/log_likelihoods_birth'][()]
        lw = f['samples/log_weights'][()]
    np.random.seed(seed)
    logw = np.asarray(NestedSamples(data=data, logL=logl, logL_birth=birth).logw(draws))
    w = np.exp(logw - logw.max(axis=0))
    mean_w = np.exp(lw - lw.max())
    kish = mean_w.sum() ** 2 / (mean_w ** 2).sum()
    out = {}
    for name, x in data.items():
        means = (w * x[:, None]).sum(axis=0) / w.sum(axis=0)
        mean = (mean_w * x).sum() / mean_w.sum()
        variance = (mean_w * (x - mean) ** 2).sum() / mean_w.sum()
        out[name] = round(float(1 / (1 / kish + means.var() / variance)), 1)
    return out


def sampler_row(path):
    digest, path_hash, attrs = result_hash(path)
    with h5py.File(path) as f:
        lw = f['samples/log_weights'][()]
    w = np.exp(lw - lw.max())
    row = dict(hash=digest, path=path_hash, wall_sampler=round(float(attrs['wall_time_s']), 1), n_calls=int(attrs['n_likelihood_calls']),
               lnZ=float(attrs['log_evidence']), n_samples=int(attrs['n_samples']),
               kish_ess=round(float(w.sum() ** 2 / (w ** 2).sum()), 1))
    row['ess_per_s'] = round(row['kish_ess'] / row['wall_sampler'], 2)
    row['ess'] = parameter_ess(path)
    row['quantiles'] = quantiles(path)
    row['ess_per_s_param'] = {k: round(v / row['wall_sampler'], 2) for k, v in row['ess'].items()}
    derived = Path(path).with_name('ceridwen_derived_outputs.h5')
    if derived.exists():  # the notebook's stored convergence check: finite ln Z and error, weight ESS >= 200
        with h5py.File(derived) as f:
            row['check_passed'] = bool(f['diagnostics'].attrs['passed'])
            row['lnZ_err'] = round(float(f['diagnostics'].attrs['log_evidence_err']), 3)
    return row


def end_to_end(run):
    manifest = json.loads((run / 'manifest.json').read_text())
    rows = []
    for attempt in manifest['attempts']:
        for name, cell in attempt['cells'].items():
            row = {'cell': name, 'driver_s': round(attempt['elapsed'], 1), 'error': cell.get('error'),
                   'container_s': round(cell.get('container_seconds', 0), 1),
                   'billed_usd': attempt.get('billed_usd'), 'estimated_usd': round(cell.get('estimated_usd', 0), 4),
                   **{k: cell[k] for k in ('container_cells', 'mode', 'tuned', 'compiled', 'retuned') if k in cell}}
            fit = next(run.glob(f"fits/{name.split('/')[0]}/*"), None)
            if fit is not None and (fit / 'execution.log').exists():
                first = (fit / 'execution.log').read_text().split('] starting', 1)[0].lstrip('\n[')
                start = datetime.fromisoformat(first).timestamp()
                # The local figure rebuild rewrites the notebook and derived outputs, not the result file.
                row['fit_start_to_sampler_end_s'] = round((fit / 'ceridwen_result.h5').stat().st_mtime - start, 1)
                row.update(sampler_row(fit / 'ceridwen_result.h5'))
            rows.append(row)
    return {'run': run.name, 'rows': rows}


def summarise(run):
    if (run / 'manifest.json').exists():
        return end_to_end(run)
    timings = json.loads((run / 'timings.json').read_text())
    rows = []
    for step in timings['steps']:
        if 'copy' not in step and step['label'] == 'mps-start':
            continue
        directory = run / f"{step['index']:02d}-{step['label']}-{step.get('copy', 0)}"
        if not directory.exists():
            directory = run / f"{step['index']:02d}-{step['label']}"
        fits = [fit_row(fit, step) for fit in directory.glob('results/*/*')]
        rows += sorted(fits, key=lambda row: row.get('kernel_start_s', 0))
    return {'gpu': timings.get('gpu'), 'cold_start_s': round(timings['entered'] - timings['called_at'], 1),
            'container_s': round(timings['finished'] - timings['entered'], 1), 'rows': rows}


if __name__ == '__main__':
    for arg in sys.argv[1:]:
        print(json.dumps(summarise(Path(arg)), indent=1))
