"""Build one production fit up to the sampler call, time each notebook cell, and dump ln L
at a subsample of the dead points of a finished fit.

    lnl_check.py dump OUT.npz --settings '{"data_source": "legac_dr3", ...}' --dead ns_raw_dead.pkl
    lnl_check.py compare A.npz B.npz

The notebook comes from this worktree; scripts/ and the data from --data-root (the main checkout).
The ceridwen under test is whichever one PYTHONPATH puts first.
"""
import argparse
import json
import os
import pickle
import sys
import time
from pathlib import Path

HERE = Path(__file__).resolve()
WORKTREE = Path(os.environ.get('LNL_CHECK_TREE', HERE.parents[2]))  # the tree with notebooks/


def build(settings, target='M1_210210', seed=20260832, result_dir='fit', data_root='/Users/liuhao/Downloads/Astro project',
          priors=None):
    """The notebook's namespace just before the sampler call, and the seconds each cell took."""
    os.environ.update(
        JAX_ENABLE_X64='1', CERIDWEN_TARGET_ID=target, CERIDWEN_RANDOM_SEED=str(seed),
        CERIDWEN_RESULT_DIR=str(Path(result_dir).resolve()), CERIDWEN_PLOTS='0',
        CERIDWEN_NOTEBOOK_QUICK='0', CERIDWEN_MANIFEST_INDEX='0')
    os.environ.setdefault('JAX_PLATFORMS', 'cpu')
    Path(os.environ['CERIDWEN_RESULT_DIR']).mkdir(parents=True, exist_ok=True)
    notebook = json.loads((WORKTREE / 'notebooks/ceridwen_integrated_photometry_spectra.ipynb').read_text())
    os.chdir(data_root)
    scope, times = {'__name__': '__main__'}, {}
    code = [''.join(cell['source']) for cell in notebook['cells'] if cell['cell_type'] == 'code']
    for index, source in enumerate(code):
        if 'SETTINGS = {' in source:
            source += f'\nSETTINGS.update({settings!r})\n'
        if 'PRIORS = {' in source:  # scripts/run_ceridwen_vast_multi_gpu.py _fit_notebook
            source += ''.join(f'\nPRIORS[{name!r}] = {expression}\n' for name, expression in (priors or {}).items())
        last = 'run_sampler(' in source
        if last:
            source = source[:source.index('# The output cell')]
        start = time.perf_counter()
        exec(compile(source, f'cell{index}', 'exec'), scope)
        times[f'cell{index}'] = time.perf_counter() - start
        if last:
            return scope, times


def dump(args):
    out = Path(args.out).resolve()
    dead_path = Path(args.dead).resolve()
    scope, times = build(json.loads(args.settings), args.target, args.seed, out.parent / 'fit', args.data_root)
    import jax
    import numpy as np

    class Capture:
        def run(self, loglike_fn, logprior_fn, theta_init, rng_key):
            self.loglike = loglike_fn

    capture = Capture()
    from ceridwen.sampler import run_sampler
    run_sampler(scope['joint_model'], scope['joint_likelihood'], capture, jax.random.PRNGKey(0))
    with dead_path.open('rb') as handle:
        dead = pickle.load(handle)
    rows = np.arange(0, dead['n_dead'], args.step)
    rows = rows[:len(rows) // args.batch * args.batch]
    batched = jax.jit(jax.vmap(capture.loglike))
    lnl, seconds = [], []
    for chunk in rows.reshape(-1, args.batch):
        theta = {name: jax.numpy.asarray(value[chunk]) for name, value in dead['positions'].items()}
        start = time.perf_counter()
        lnl.append(np.asarray(batched(theta)))
        seconds.append(time.perf_counter() - start)
    times['loglike_compile_and_first_batch'] = seconds[0]
    times['loglike_batch_median'] = float(np.median(seconds[1:]))
    spectrum_mask = np.asarray(scope['spectrum_obs'].mask)
    np.savez(out, rows=rows, lnl=np.concatenate(lnl), gpu_lnl=dead['loglikelihood'][rows],
             times=json.dumps(times), pixels=np.array([spectrum_mask.sum(), spectrum_mask.size]))
    print(json.dumps({k: round(v, 3) for k, v in times.items()}, indent=1))
    print('pixels fitted / total', spectrum_mask.sum(), spectrum_mask.size)
    print('max |lnL - GPU production lnL|', np.abs(np.concatenate(lnl) - dead['loglikelihood'][rows]).max())


def parts(args):
    """Seconds per batch of each part of ln L on this device, and ln L at the dead-point subsample."""
    out = Path(args.out).resolve()
    dead_path = Path(args.dead).resolve()
    if args.cell:  # an experiment cell: its settings, priors, target and seed
        cell = json.loads(Path(args.cell).read_text())[0]
        scope, times = build(cell['settings'], cell['target'], cell['seed'], out.parent / 'fit', args.data_root,
                             cell['priors'])
    else:
        scope, times = build(json.loads(args.settings), args.target, args.seed, out.parent / 'fit', args.data_root)
    import jax
    import numpy as np
    from ceridwen.likelihood.likelihood import observation_data
    from ceridwen.sampler import run_sampler

    class Capture:
        def run(self, loglike_fn, logprior_fn, theta_init, rng_key):
            self.loglike = loglike_fn

    capture = Capture()
    model, likelihood = scope['joint_model'], scope['joint_likelihood']
    run_sampler(model, likelihood, capture, jax.random.PRNGKey(0))
    with dead_path.open('rb') as handle:
        dead = pickle.load(handle)
    rows = np.arange(0, dead['n_dead'], args.step)
    rows = rows[:len(rows) // args.batch * args.batch].reshape(-1, args.batch)
    batches = [{name: jax.numpy.asarray(value[chunk]) for name, value in dead['positions'].items()}
               for chunk in rows]
    csp, observations = model.csp, model.observations
    transformed = model.apply_transforms(model.theta_init)
    support = csp._support_for(observations, transformed, False)
    response = getattr(csp, 'abundance_response', None)
    functions = {
        'loglike': capture.loglike,
        'predict': model.predict,
        'transforms': model.apply_transforms,
        'get_spectrum': lambda theta: csp.get_spectrum(
            theta=model.apply_transforms(theta), include_lines=False, support=support),
    }
    if response is not None:
        for key in response.tables:
            functions[f'factor {key}'] = lambda theta, key=key: response.factor(
                csp, model.apply_transforms(theta), key)

    def timed(function, *extra):
        compiled = jax.jit(jax.vmap(function))
        start = time.perf_counter()
        first = jax.block_until_ready(compiled(batches[0], *extra))
        compile_seconds = time.perf_counter() - start
        seconds = []
        for _ in range(args.repeats):
            start = time.perf_counter()
            for batch in batches[:args.rounds]:
                last = compiled(batch, *extra)
            jax.block_until_ready(last)
            seconds.append((time.perf_counter() - start) / args.rounds)
        return compiled, compile_seconds, float(np.median(seconds)), first

    result, late = {}, {}
    for name, function in functions.items():
        compiled, compile_seconds, seconds, _ = timed(function)
        result[name] = {'compile_s': compile_seconds, 'batch_ms': 1e3 * seconds}
        if name == 'loglike':
            lnl = np.concatenate([np.asarray(compiled(batch)) for batch in batches])
        if name == 'predict':
            data = {obs.name: observation_data(obs) for obs in observations}
            prediction = compiled(batches[0])
            late = {f'mu_{key}': np.asarray(value) for key, value in compiled(batches[-1]).items()}
            _, compile_seconds, seconds, _ = timed(
                lambda theta, predicted: likelihood.loglike(data, predicted, theta, None), prediction)
            result['likelihood given prediction'] = {'compile_s': compile_seconds, 'batch_ms': 1e3 * seconds}
    for name, row in result.items():
        print(f"{name:30s} compile {row['compile_s']:7.2f} s   batch of {args.batch} {row['batch_ms']:9.3f} ms")
    np.savez(out, rows=rows.ravel(), lnl=lnl, gpu_lnl=dead['loglikelihood'][rows.ravel()],
             times=json.dumps({**times, **{f'{k} batch_ms': v['batch_ms'] for k, v in result.items()}}),
             device=str(jax.devices()[0]), **late)


def compare(args):
    import numpy as np
    a, b = np.load(args.a), np.load(args.b)
    assert (a['rows'] == b['rows']).all()
    delta = np.abs(a['lnl'] - b['lnl'])
    print(f"points {delta.size}  differ {(delta > 0).sum()}  max |delta lnL| {delta.max():.3e}  "
          f"lnL range [{a['lnl'].min():.1f}, {a['lnl'].max():.1f}]")
    ta, tb = json.loads(str(a['times'])), json.loads(str(b['times']))
    for key in ta:
        print(f'{key:34s} {ta[key]:8.3f} -> {tb.get(key, float("nan")):8.3f} s')


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    commands = parser.add_subparsers(dest='command', required=True)
    p = commands.add_parser('dump')
    p.add_argument('out')
    p.add_argument('--settings', required=True)
    p.add_argument('--dead', required=True)
    p.add_argument('--target', default='M1_210210')
    p.add_argument('--seed', type=int, default=20260832)
    p.add_argument('--step', type=int, default=20)
    p.add_argument('--batch', type=int, default=100)
    p.add_argument('--data-root', default='/Users/liuhao/Downloads/Astro project')
    p.set_defaults(run=dump)
    p = commands.add_parser('parts')
    p.add_argument('out')
    p.add_argument('--settings')
    p.add_argument('--cell')
    p.add_argument('--dead', required=True)
    p.add_argument('--target', default='M1_210210')
    p.add_argument('--seed', type=int, default=20260832)
    p.add_argument('--step', type=int, default=20)
    p.add_argument('--batch', type=int, default=100)
    p.add_argument('--rounds', type=int, default=8)
    p.add_argument('--repeats', type=int, default=5)
    p.add_argument('--data-root', default='/Users/liuhao/Downloads/Astro project')
    p.set_defaults(run=parts)
    p = commands.add_parser('compare')
    p.add_argument('a')
    p.add_argument('b')
    p.set_defaults(run=compare)
    arguments = parser.parse_args()
    arguments.run(arguments)
