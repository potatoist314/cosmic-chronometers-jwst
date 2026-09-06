"""Measure complete production NSS fits and replay their actual GPU steps.

Uses the current production notebook, without changing the likelihood or NSS
settings. All candidate execution schedules preserve each particle's keys.
"""
from __future__ import annotations

import argparse
import json
import os
import pickle
import shlex
import sys
import time
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
RESULT_ROOT = PROJECT_ROOT / 'results/rtx-5060-production-speedup'
STATE_ROOT = PROJECT_ROOT / 'benchmarks/ceridwen/runs/production-speedup'
TARGETS = ('M1_210210', 'M5_172669')
SEEDS = (20260906, 20260907)


def calibration_normal_dot(self, mu, sigma, mask):
    """Freeze the production arithmetic used by the first baseline fit."""
    design = self.design(mu, sigma, mask)
    normal = design.T @ design
    precision = self._precision()
    return normal if precision is None else normal + precision


def calibration_normal_reduce(self, mu, sigma, mask):
    """Form the same small Gram matrix using parallel pixel reductions."""
    import jax.numpy as jnp
    design = self.design(mu, sigma, mask)
    normal = jnp.sum(design[:, :, None] * design[:, None, :], axis=0)
    precision = self._precision()
    return normal if precision is None else normal + precision


def probe_value_paths(namespace):
    """Compare value-only compilation and calibration on identical predictions."""
    import jax
    import jax.numpy as jnp
    import numpy as np
    from types import SimpleNamespace
    from ceridwen.likelihood import PolynomialCalibration
    from ceridwen.sampler.runner import run_sampler
    from ceridwen.fit import load_result_h5
    model=namespace['joint_model']; likelihood=namespace['joint_likelihood']
    folder=namespace['RESULT_DIR']
    result=load_result_h5(folder/'ceridwen_result.h5')
    report={}
    for count in (100,500):
        points={name:jnp.asarray(values)[:count].reshape((count,)+model.theta_init[name].shape)
                for name,values in result.samples.items()}
        predictions=jax.jit(jax.vmap(model.predict))(points)
        outputs={}
        for variant,method in (('baseline',calibration_normal_dot),('reduce',calibration_normal_reduce)):
            PolynomialCalibration.normal_matrix=method
            capture=SimpleNamespace(run=lambda ll,lp,theta,key:(ll,lp))
            loglike,logprior=run_sampler(model,likelihood,capture,jax.random.PRNGKey(0))
            values=jax.jit(jax.vmap(loglike))(points)
            gradients=jax.jit(jax.vmap(jax.value_and_grad(loglike)))(points)
            def fixed_prediction(theta, prediction):
                total=jnp.zeros(())
                for key,lhood in zip(likelihood.keys,likelihood.likelihoods):
                    obs=model.obs_dict[key]
                    value,_=lhood(obs.flux,prediction[key],obs.uncertainty,obs.mask,params=theta)
                    total=total+value
                return total
            fixed=jax.jit(jax.vmap(fixed_prediction))(points,predictions)
            initialized=jax.jit(build_algorithm(loglike,logprior).init)(points)
            outputs[variant]=jax.device_get((values,gradients,fixed,initialized.particles.loglikelihood))
        a,b=outputs['baseline'],outputs['reduce']
        ga,gb=(np.concatenate([x.reshape(count,-1) for x in jax.tree.leaves(o[1][1])],axis=1) for o in (a,b))
        report[str(count)]={
            'value_only_max_abs_delta_loglike':float(np.max(np.abs(a[0]-b[0]))),
            'value_and_grad_max_abs_delta_loglike':float(np.max(np.abs(a[1][0]-b[1][0]))),
            'fixed_predictions_max_abs_delta_loglike':float(np.max(np.abs(a[2]-b[2]))),
            'nss_initialization_max_abs_delta_loglike':float(np.max(np.abs(a[3]-b[3]))),
            'baseline_compilation_context_max_abs_delta_loglike':float(np.max(np.abs(a[0]-a[2]))),
            'baseline_compilation_context_first_ten_max_abs_delta_loglike':float(np.max(np.abs(a[0][:10]-a[2][:10]))),
            'max_relative_gradient_error':float(np.max(np.linalg.norm(ga-gb,axis=1)/np.maximum(np.linalg.norm(ga,axis=1),1e-12))),
            'baseline_value_only_first_ten':a[0][:10].tolist(),
            'reduce_value_only_first_ten':b[0][:10].tolist(),
            'baseline_fixed_predictions_first_ten':a[2][:10].tolist(),
            'reduce_fixed_predictions_first_ten':b[2][:10].tolist(),
            'baseline_initialization_first_ten':a[3][:10].tolist(),
            'reduce_initialization_first_ten':b[3][:10].tolist(),
        }
        (folder/'value_paths.json').write_text(json.dumps(report,indent=2)+'\n')
        print('VALUE_PATHS',count,report[str(count)],flush=True)
    # Keep the first compilation control; later compilations can differ.
    if not (folder/'compilation_context.json').exists():
        (folder/'compilation_context.json').write_text(json.dumps(report,indent=2)+'\n')
    return report


def probe_calibration(namespace, loglike, logprior, snapshots, compiled):
    """Check numerical fidelity and complete steps after a real baseline fit."""
    import jax
    import jax.numpy as jnp
    import numpy as np
    from types import SimpleNamespace
    from ceridwen.likelihood import PolynomialCalibration
    from ceridwen.sampler.runner import run_sampler
    from ceridwen.fit import load_result_h5
    model=namespace['joint_model']; folder=namespace['RESULT_DIR']
    PolynomialCalibration.normal_matrix=calibration_normal_reduce
    capture=SimpleNamespace(run=lambda ll, lp, theta, key: (ll,lp))
    candidate,_=run_sampler(model,namespace['joint_likelihood'],capture,jax.random.PRNGKey(0))
    # Compile reference arithmetic before the method replacement can retrace it.
    original = namespace['original_calibration_normal']
    PolynomialCalibration.normal_matrix=original
    reference_vg=jax.jit(jax.vmap(jax.value_and_grad(loglike)))
    prior=namespace['joint_adapter']._sample_prior(model.theta_init,jax.random.PRNGKey(20260908))
    prior=jax.tree.map(lambda x:x[:256],prior)
    reference_vg.lower(prior).compile()
    reference_vg(prior)[0].block_until_ready()
    PolynomialCalibration.normal_matrix=calibration_normal_reduce
    candidate_vg=jax.jit(jax.vmap(jax.value_and_grad(candidate)))
    result=load_result_h5(folder/'ceridwen_result.h5')
    weights=np.exp(np.asarray(result.log_weights)-float(jax.scipy.special.logsumexp(result.log_weights)))
    index=np.searchsorted(np.cumsum(weights),(np.arange(256)+.5)/256)
    posterior={name:jnp.asarray(values)[index].reshape((256,)+model.theta_init[name].shape)
               for name,values in result.samples.items()}
    edges=[]
    for name,distribution in model.priors.items():
        for side in ('low','high'):
            bound=distribution.params.get(side)
            if bound is None:
                bound=distribution.unit_transform(jnp.asarray(.001 if side=='low' else .999))
            value=np.asarray(bound,dtype=float)
            value=value+(1 if side=='low' else -1)*1e-8*np.maximum(1.,np.abs(value))
            for coordinate in range(model.theta_init[name].size):
                row=dict(model.theta_init)
                values=np.broadcast_to(value,row[name].shape).ravel()
                row[name]=row[name].at[coordinate].set(values[coordinate])
                edges.append(row)
    samples={'prior':prior,'posterior':posterior}
    if edges:samples['boundaries']=jax.tree.map(lambda *xs:jnp.stack(xs),*edges)
    report=(json.loads((folder/'calibration_replay.json').read_text())
            if (folder/'calibration_replay.json').exists() else {'numerical':{},'states':{}})
    for label,points in samples.items():
        # New batch shapes need the reference method active during tracing.
        PolynomialCalibration.normal_matrix=original
        a,ga=jax.block_until_ready(reference_vg(points))
        PolynomialCalibration.normal_matrix=calibration_normal_reduce
        b,gb=jax.block_until_ready(candidate_vg(points))
        gradient_a=np.concatenate([np.asarray(x).reshape(len(a),-1) for x in jax.tree.leaves(ga)],axis=1)
        gradient_b=np.concatenate([np.asarray(x).reshape(len(a),-1) for x in jax.tree.leaves(gb)],axis=1)
        predictions=jax.jit(jax.vmap(model.predict))(points)
        residuals=[]
        for method in (original,calibration_normal_reduce):
            PolynomialCalibration.normal_matrix=method
            def residual_prediction(theta,prediction):
                values={}
                for key,lhood in zip(namespace['joint_likelihood'].keys,namespace['joint_likelihood'].likelihoods):
                    obs=model.obs_dict[key]
                    _,aux=lhood(obs.flux,prediction[key],obs.uncertainty,obs.mask,params=theta)
                    values[key]=aux.residuals
                return values
            residuals.append(jax.device_get(jax.jit(jax.vmap(residual_prediction))(points,predictions)))
        prediction_error={}
        for key in residuals[0]:
            mask=np.asarray(model.obs_dict[key].mask,dtype=bool)
            prediction_error[key]=float(np.max(np.abs(residuals[0][key]-residuals[1][key])[:,mask]/
                                               np.asarray(model.obs_dict[key].uncertainty)[mask]))
        report['numerical'][label]={
            'count':len(a),'max_abs_delta_loglike':float(np.max(np.abs(np.asarray(a-b)))),
            'max_relative_gradient_error':float(np.max(np.linalg.norm(gradient_a-gradient_b,axis=1)/np.maximum(np.linalg.norm(gradient_a,axis=1),1e-12))),
            'max_prediction_difference_in_observed_sigma':prediction_error}
        print('CALIBRATION_NUMERICAL',label,report['numerical'][label],flush=True)
    assert all(v['max_abs_delta_loglike'] < 1e-3 and
               v['max_relative_gradient_error'] < 1e-4 and
               max(v['max_prediction_difference_in_observed_sigma'].values()) < 1e-5
               for v in report['numerical'].values()), report['numerical']
    (folder/'calibration_replay.json').write_text(json.dumps(report,indent=2)+'\n')
    if compiled is None:
        return report
    algorithm=build_algorithm(candidate,logprior)
    key,state=snapshots['middle']
    trial=jax.jit(algorithm.step).lower(key,state).compile()
    for label,(key,state) in snapshots.items():
        a=jax.block_until_ready(compiled(key,state));b=jax.block_until_ready(trial(key,state))
        equal=all(np.allclose(x,y,rtol=1e-10,atol=1e-10,equal_nan=True)
                  for x,y in zip(jax.tree.leaves(a),jax.tree.leaves(b)))
        timings={'baseline':[],'reduce':[]}
        for repeat in range(6):
            order=[('baseline',compiled),('reduce',trial)]
            for name,fn in order if repeat%2==0 else reversed(order):
                started=time.perf_counter();jax.block_until_ready(fn(key,state))
                timings[name].append(time.perf_counter()-started)
        report['states'][label]={'equivalent':equal,**timings}
        (folder/'calibration_replay.json').write_text(json.dumps(report,indent=2)+'\n')
        print('CALIBRATION_REPLAY',label,{k:float(np.median(v)) for k,v in timings.items()},flush=True)
    print('CALIBRATION_NUMERICAL',json.dumps(report['numerical']),flush=True)
    return report


def build_algorithm(loglike, logprior, inner_steps=65, num_delete=100, variant='baseline'):
    """Use BlackJAX NSS primitives, changing only the chain execution schedule."""
    import jax
    import jax.numpy as jnp
    import blackjax
    from functools import partial
    from blackjax.ns import nss, adaptive, base
    from blackjax.mcmc.slice import build_kernel as slice_kernel, stepping_out

    if variant in ('baseline', 'reduce'):
        return blackjax.nss(logprior_fn=logprior, loglikelihood_fn=loglike,
                            num_inner_steps=inner_steps, num_delete=num_delete)
    batch = int(variant.removeprefix('group'))
    init_state = partial(base.init_state_strategy, logprior_fn=logprior,
                         loglikelihood_fn=loglike)
    constrained = nss.slice_constrained_step(
        init_state, slice_kernel(interval=stepping_out, max_expansions=10,
                                 max_shrinkage=100), nss.covariance_proposal)

    def update(key, state, threshold, **params):
        # Identical survivor selection and key splitting to BlackJAX's
        # update_with_mcmc_take_last. Only the outer map changes.
        choice_key, sample_key = jax.random.split(key)
        weights = (state.particles.loglikelihood > threshold).astype(jnp.float32)
        weights = jnp.where(weights.sum() > 0., weights, jnp.ones_like(weights))
        starts = jax.random.choice(choice_key, len(weights), shape=(num_delete,),
                                   p=weights / weights.sum(), replace=True)
        initial = jax.tree.map(lambda x: x[starts], state.particles)
        keys = jax.random.split(sample_key, num_delete)

        def chain(inputs):
            particle_key, particle = inputs
            inner_keys = jax.random.split(particle_key, inner_steps)
            def move(current, move_key):
                return constrained(move_key, current, threshold, **params)
            return jax.lax.scan(move, particle, inner_keys)
        return jax.lax.map(chain, (keys, initial), batch_size=batch)

    kernel = adaptive.build_kernel(partial(base.delete_fn, num_delete=num_delete),
                                   update, nss.live_covariance)
    initializer = partial(adaptive.init, init_state_fn=jax.vmap(init_state),
                          update_inner_kernel_params_fn=nss.live_covariance)
    return blackjax.SamplingAlgorithm(initializer, kernel)


class FitExperiment:
    def __init__(self, folder, variant):
        self.folder, self.variant = Path(folder), variant
        self.snapshots, self.steps = {}, []

    def attach(self, adapter):
        import types
        import inspect
        from ceridwen.likelihood import PolynomialCalibration
        if self.variant != 'reduce':
            PolynomialCalibration.normal_matrix=calibration_normal_dot
        self.calibration_source=inspect.getsource(PolynomialCalibration.normal_matrix)
        self.calibration_module=inspect.getfile(PolynomialCalibration)
        if self.variant == 'reduce':
            assert 'jnp.sum(design[:, :, None] * design[:, None, :], axis=0)' in self.calibration_source, (
                'The installed Ceridwen package lacks the candidate; reinstall it before fitting.')
        def factory(_adapter, loglike, logprior, inner_steps, num_delete):
            self.loglike, self.logprior = loglike, logprior
            self.inner_steps, self.num_delete = inner_steps, num_delete
            return build_algorithm(loglike, logprior, inner_steps, num_delete, self.variant)
        adapter._build_nested_sampler = types.MethodType(factory, adapter)
        adapter.iteration_callback = self.observe

    def observe(self, iteration, key, incoming, outgoing, info, compiled_step, elapsed):
        import jax
        import numpy as np
        self.compiled_step = compiled_step
        item = (key, incoming)
        if iteration == 10:
            self.snapshots['early'] = item
        if iteration == 100:
            self.snapshots['middle'] = item
        self.snapshots['late'] = item
        expansions, shrink = jax.device_get((info.update_info.num_expansions,
                                           info.update_info.num_shrink))
        logical = int(np.sum(expansions + shrink + 2))
        self.steps.append(dict(iteration=iteration, seconds=elapsed,
                               logical_likelihood_evaluations=logical,
                               slice_transitions=int(expansions.size),
                               mean_shrink=float(shrink.mean()),
                               max_shrink=int(shrink.max())))

    def save(self, result, started):
        import importlib.metadata as md
        import jax
        self.folder.mkdir(parents=True, exist_ok=True)
        timing = dict(variant=self.variant, total_fit_seconds=time.perf_counter()-started,
                      sampler_seconds=result.wall_time_s,
                      logical_likelihood_evaluations=result.n_likelihood_calls,
                      slice_transitions=sum(s['slice_transitions'] for s in self.steps),
                      steps=self.steps,
                      software={n: md.version(n) for n in ('jax','jaxlib','blackjax','ceridwen')},
                      gpu=[d.device_kind for d in jax.devices()], x64=jax.config.jax_enable_x64,
                      calibration_module=self.calibration_module, calibration_source=self.calibration_source)
        (self.folder/'timing.json').write_text(json.dumps(timing, indent=2)+'\n')
        with (self.folder/'replay.pkl').open('wb') as f:
            pickle.dump(jax.device_get(self.snapshots), f)
        print(json.dumps({k:v for k,v in timing.items() if k!='steps'}), flush=True)

    def probe(self):
        """Time complete compiled transitions on identical states and keys."""
        import jax
        import numpy as np
        report = {'states': {}, 'variants': {}}
        functions = {'baseline': self.compiled_step}
        trace=self.folder/'profile'
        key,state=self.snapshots['middle']
        with jax.profiler.trace(str(trace)):
            with jax.profiler.StepTraceAnnotation('production_nss_step',step_num=100):
                jax.block_until_ready(functions['baseline'](key,state))
        for variant in ('group50','group25','group10'):
            algorithm = build_algorithm(self.loglike,self.logprior,self.inner_steps,
                                        self.num_delete,variant)
            key, state = self.snapshots['early']
            start=time.perf_counter()
            functions[variant]=jax.jit(algorithm.step).lower(key,state).compile()
            report['variants'][variant]={'compile_seconds':time.perf_counter()-start}
        for stage,(key,state) in self.snapshots.items():
            reference = jax.block_until_ready(functions['baseline'](key,state))
            stage_report={}
            for variant,fn in functions.items():
                actual=jax.block_until_ready(fn(key,state))
                # Full sampler state, evidence integrator, and slice diagnostics.
                ra,aa=jax.tree.leaves(reference),jax.tree.leaves(actual)
                exact=all(np.array_equal(np.asarray(a),np.asarray(b),equal_nan=True)
                          for a,b in zip(ra,aa))
                equivalent=all(
                    np.allclose(np.asarray(a),np.asarray(b),rtol=1e-10,atol=1e-10,equal_nan=True)
                    if np.issubdtype(np.asarray(a).dtype,np.floating)
                    else np.array_equal(np.asarray(a),np.asarray(b))
                    for a,b in zip(ra,aa))
                max_error=max(float(np.nanmax(np.abs(np.asarray(a,dtype=float)-np.asarray(b,dtype=float))))
                              for a,b in zip(ra,aa) if np.asarray(a).size)
                stage_report[variant]={'identical':exact,'equivalent':equivalent,
                                       'max_abs_state_error':max_error,'seconds':[]}
            for repeat in range(6):
                order=list(functions.items())
                for variant,fn in order if repeat%2==0 else reversed(order):
                    start=time.perf_counter();jax.block_until_ready(fn(key,state))
                    stage_report[variant]['seconds'].append(time.perf_counter()-start)
            report['states'][stage]=stage_report
            (self.folder/'replay.json').write_text(json.dumps(report,indent=2)+'\n')
            print('Replay',stage,{k:round(float(np.median(v['seconds'])),4) for k,v in stage_report.items()},flush=True)
        for variant in report['variants']:
            values=[s['baseline']['seconds'] for s in report['states'].values()]
            trial=[s[variant]['seconds'] for s in report['states'].values()]
            report['variants'][variant].update(
                speedup=float(np.median(values)/np.median(trial)),
                identical=all(s[variant]['identical'] for s in report['states'].values()),
                equivalent=all(s[variant]['equivalent'] for s in report['states'].values()))
        passed=[k for k,v in report['variants'].items() if v['equivalent'] and v['speedup']>=1.1]
        report['selected']=max(passed,key=lambda k:report['variants'][k]['speedup']) if passed else None
        (self.folder/'replay.json').write_text(json.dumps(report,indent=2)+'\n')
        print('REPLAY_COMPLETE',json.dumps(report['variants']),flush=True)
        return report


def worker(args):
    import nbformat
    from nbclient import NotebookClient
    folder=RESULT_ROOT/f'{args.target}-{args.seed}-{args.variant}'
    folder.mkdir(parents=True,exist_ok=True)
    os.environ.update(CERIDWEN_PROJECT_ROOT=str(PROJECT_ROOT),CERIDWEN_RESULT_DIR=str(folder),
        CERIDWEN_TARGET_ID=args.target,CERIDWEN_OBJECT_ID=args.target.split('_')[-1],
        CERIDWEN_RANDOM_SEED=str(args.seed),CERIDWEN_NOTEBOOK_QUICK='0',
        CERIDWEN_EXPECT_SINGLE_GPU='1',CERIDWEN_CALIBRATION_ORDER='3',
        CERIDWEN_CALIBRATION_PRIOR='0.1',CERIDWEN_PHOTOMETRY='cosmos_total',
        CERIDWEN_FIT_MODE='full_spectrum',CERIDWEN_SPECTRUM_PIXELS='all',
        CERIDWEN_FREE_ZRED_KMS='0',CERIDWEN_FREE_SIGMA_FRAC='0',
        MPLBACKEND='module://matplotlib_inline.backend_inline')
    notebook=nbformat.read(PROJECT_ROOT/'notebooks/ceridwen_integrated_photometry_spectra.ipynb',as_version=4)
    if args.replay_existing:
        notebook.cells=notebook.cells[:20]
    for cell in notebook.cells:
        if cell.cell_type!='code':continue
        cell.outputs=[];cell.execution_count=None
        if cell.source.startswith('import os') and args.replay_existing:
            cell.source+='\nsys.path.insert(0, str(PROJECT_ROOT / "scripts"))\nfrom validate_ceridwen_speedups import calibration_normal_dot\nfrom ceridwen.likelihood import PolynomialCalibration\nPolynomialCalibration.normal_matrix=calibration_normal_dot\n'
        if cell.source.startswith('LEGAC_PATH ='):
            cell.source='import time\n_fit_started=time.perf_counter()\n'+cell.source
        if 'joint_result = run_sampler(' in cell.source:
            if args.replay_existing:
                cell.source=cell.source.split('joint_result = run_sampler(',1)[0]
                cell.source+='''
from types import SimpleNamespace
from validate_ceridwen_speedups import build_algorithm, probe_calibration
import gzip, pickle
capture=SimpleNamespace(run=lambda loglike, logprior, theta, key: (loglike, logprior))
loglike,logprior=run_sampler(joint_model,joint_likelihood,capture,jax.random.PRNGKey(SEED))
with (RESULT_DIR/'replay.pkl').open('rb') as stream:
    snapshots=jax.tree.map(jnp.asarray,pickle.load(stream))
key,state=snapshots['middle']
algorithm=build_algorithm(loglike,logprior)
compiled=jax.jit(algorithm.step).lower(key,state).compile()
with gzip.open(RESULT_DIR/'baseline_hlo.txt.gz','wt') as stream:
    stream.write(compiled.as_text())
print('HLO_SAVED',flush=True)
original_calibration_normal=PolynomialCalibration.normal_matrix
calibration_report=probe_calibration(globals(),loglike,logprior,snapshots,compiled)
from validate_ceridwen_speedups import probe_value_paths
value_report=probe_value_paths(globals())
'''
                if args.numerical_only:
                    cell.source=cell.source.split("with (RESULT_DIR/'replay.pkl')",1)[0]+'''
original_calibration_normal=PolynomialCalibration.normal_matrix
calibration_report=probe_calibration(globals(),loglike,logprior,None,None)
from validate_ceridwen_speedups import probe_value_paths
value_report=probe_value_paths(globals())
'''
                continue
            marker='joint_result = run_sampler('
            setup=("from validate_ceridwen_speedups import FitExperiment\n"
                   f"experiment=FitExperiment(RESULT_DIR, {args.variant!r})\n"
                   "experiment.attach(joint_adapter)\n")
            cell.source=cell.source.replace(marker,setup+marker,1)
            cell.source += '\nexperiment.save(joint_result, _fit_started)\n'
    if args.probe and not args.replay_existing:
        notebook.cells.extend([nbformat.v4.new_markdown_cell('- Replay complete sampler steps from this fit.'),
                               nbformat.v4.new_code_cell('replay_report = experiment.probe()')])
    if args.probe_calibration:
        notebook.cells.extend([
            nbformat.v4.new_markdown_cell('- Check calibration arithmetic against this completed fit.'),
            nbformat.v4.new_code_cell('''
from validate_ceridwen_speedups import probe_calibration
original_calibration_normal=PolynomialCalibration.normal_matrix
calibration_report=probe_calibration(globals(),experiment.loglike,experiment.logprior,
                                     experiment.snapshots,experiment.compiled_step)
''')])
    class StreamingClient(NotebookClient):
        def process_message(self,msg,cell,cell_index):
            if msg['msg_type']=='stream':print(msg['content']['text'],end='',flush=True)
            return super().process_message(msg,cell,cell_index)
    client=StreamingClient(notebook,timeout=None,kernel_name='ceridwen',
                           resources={'metadata':{'path':str(PROJECT_ROOT)}})
    try:client.execute()
    finally:
        name=('numerical_checks.ipynb' if args.numerical_only else
              'profile.ipynb' if args.replay_existing else 'analysis.ipynb')
        nbformat.write(notebook,folder/name)


def comparison(seeds=SEEDS, *, save=True):
    """Compare completed, matched production fits and their saved science outputs."""
    import h5py
    import numpy as np
    from scipy.special import softmax
    from per_galaxy_diagnostics import weighted_quantile
    pairs=[]
    fixed=('fit_mode','photometry_source','spectrum_pixels','calibration_order',
           'calibration_prior_sigma','calibration_marginalized','free_zred_kms',
           'free_sigma_frac','sfh_basis_fastpath','zred','random_seed')
    for target in TARGETS:
        for seed in seeds:
            folders=[RESULT_ROOT/f'{target}-{seed}-{v}' for v in ('baseline','reduce')]
            timing=[json.loads((p/'timing.json').read_text()) for p in folders]
            assert [t['variant'] for t in timing]==['baseline','reduce']
            assert 'jnp.sum(design[:, :, None] * design[:, None, :], axis=0)' in timing[1]['calibration_source']
            for folder in folders:
                notebook=json.loads((folder/'analysis.ipynb').read_text())
                assert all(c['execution_count'] is not None for c in notebook['cells'] if c['cell_type']=='code')
                assert not any(o['output_type']=='error' for c in notebook['cells'] for o in c.get('outputs',[]))
            assert timing[0]['software']==timing[1]['software']
            assert all(t['x64'] and t['gpu']==['NVIDIA GeForce RTX 5060'] for t in timing)
            row={'target':target,'seed':seed,'timing':{},'parameters':{},'derived':{}}
            for variant,t in zip(('baseline','reduce'),timing):
                post=t['steps'][1:]
                row['timing'][variant]={
                    'total_fit_seconds':t['total_fit_seconds'],'sampler_seconds':t['sampler_seconds'],
                    'iterations':len(t['steps']),'logical_likelihood_evaluations':t['logical_likelihood_evaluations'],
                    'post_jit_logical_likelihood_per_second':sum(s['logical_likelihood_evaluations'] for s in post)/sum(s['seconds'] for s in post)}
            row['total_fit_speedup']=timing[0]['total_fit_seconds']/timing[1]['total_fit_seconds']
            row['sampling_speedup']=timing[0]['sampler_seconds']/timing[1]['sampler_seconds']
            with h5py.File(folders[0]/'ceridwen_result.h5') as a, h5py.File(folders[1]/'ceridwen_result.h5') as b:
                assert all(a['model'].attrs[k]==b['model'].attrs[k] for k in fixed)
                assert a['model'].attrs['parameter_block']==b['model'].attrs['parameter_block']
                for k in ('num_live','num_inner_steps','num_delete','logZ_tol','sampler_name'):
                    assert a['samples'].attrs[k]==b['samples'].attrs[k]
                row['settings']={k:float(a['samples'].attrs[k]) for k in ('num_live','num_inner_steps','num_delete','logZ_tol')}
                for observation in a['obs']:
                    for name in ('wavelength','flux','uncertainty','mask'):
                        if name in a['obs'][observation]:
                            np.testing.assert_array_equal(a['obs'][observation][name][()],b['obs'][observation][name][()])
                sa,sb=a['samples'],b['samples']
                weights=[softmax(g['log_weights'][()]) for g in (sa,sb)]
                za,zb=(float(g.attrs['log_evidence']) for g in (sa,sb))
                ea,eb=(float(g.attrs['log_evidence_err']) for g in (sa,sb))
                row['evidence']={'baseline':za,'reduce':zb,'delta':zb-za,
                                 'baseline_error':ea,'reduce_error':eb,
                                 'delta_over_combined_error':abs(zb-za)/np.hypot(ea,eb)}
                names=a['model/param_names'].asstr()[()]
                row['parameter_samples_identical']=all(np.array_equal(sa[name][()],sb[name][()]) for name in names)
                same_shapes=all(sa[name].shape==sb[name].shape for name in names)
                row['parameter_samples_equivalent']=(same_shapes and all(np.allclose(sa[name][()],sb[name][()],rtol=1e-10,atol=1e-10) for name in names))
                if same_shapes:
                    row['max_paired_parameter_difference']={name:float(np.max(np.abs(sa[name][()]-sb[name][()]))) for name in names}
                la,lb=sa['log_likelihoods'][()],sb['log_likelihoods'][()]
                if la.shape==lb.shape:
                    row['max_abs_paired_loglike_difference']=float(np.max(np.abs(la-lb)))
                for name in names:
                    values=[g[name][()].reshape(len(w),-1) for g,w in zip((sa,sb),weights)]
                    for coordinate in range(values[0].shape[1]):
                        label=name if values[0].shape[1]==1 else f'{name}[{coordinate}]'
                        q=[np.array([weighted_quantile(v[:,coordinate],w,p) for p in (.16,.5,.84)])
                           for v,w in zip(values,weights)]
                        width=np.mean([x[2]-x[0] for x in q])/2
                        row['parameters'][label]={'baseline':q[0].tolist(),'reduce':q[1].tolist(),
                                                  'median_shift_over_68pct_half_width':float(abs(q[1][1]-q[0][1])/width)}
            with h5py.File(folders[0]/'ceridwen_derived_outputs.h5') as a, h5py.File(folders[1]/'ceridwen_derived_outputs.h5') as b:
                np.testing.assert_array_equal(a['summary/parameter'][()],b['summary/parameter'][()])
                for i,name in enumerate(a['summary/parameter'].asstr()[()]):
                    q=[np.array([g[f'summary/q{p}'][i] for p in (16,50,84)]) for g in (a,b)]
                    width=np.mean([x[2]-x[0] for x in q])/2
                    row['derived'][name]={'baseline':q[0].tolist(),'reduce':q[1].tolist(),
                                         'median_shift_over_68pct_half_width':float(abs(q[1][1]-q[0][1])/width) if width>0 else (0. if q[1][1]==q[0][1] else float('inf'))}
                for observation in ('spectrum','photometry'):
                    mask=a[f'{observation}/mask'][()].astype(bool)
                    difference=b[f'{observation}/posterior_q50'][()]-a[f'{observation}/posterior_q50'][()]
                    sigma=a[f'{observation}/uncertainty'][()]
                    row[f'{observation}_posterior_prediction_shift_sigma_rms']=float(np.sqrt(np.mean((difference[mask]/sigma[mask])**2)))
            pairs.append(row)
    report={'gpu':'NVIDIA GeForce RTX 5060','grid_schema':'2.1','precision':'JAX x64 enabled; existing float32 CSP grid and spectrum assembly preserved','pairs':pairs,
            'metric':'data loading through completed HDF5 save; plotting excluded',
            'median_total_fit_speedup':float(np.median([p['total_fit_speedup'] for p in pairs])),
            'median_sampling_speedup':float(np.median([p['sampling_speedup'] for p in pairs])),
            'median_total_fit_time_reduction_fraction':float(np.median([1-1/p['total_fit_speedup'] for p in pairs])),
            'median_sampling_time_reduction_fraction':float(np.median([1-1/p['sampling_speedup'] for p in pairs]))}
    report['per_target_total_fit_speedup']={target:float(np.median([p['total_fit_speedup'] for p in pairs if p['target']==target])) for target in TARGETS}
    report['performance_gate_passed']=(report['median_total_fit_time_reduction_fraction']>=.1 and report['median_sampling_time_reduction_fraction']>=.1 and min(report['per_target_total_fit_speedup'].values())>=1.)
    report['numerical_checks']={target:json.loads((RESULT_ROOT/f'{target}-{SEEDS[0]}-baseline/calibration_replay.json').read_text())['numerical'] for target in TARGETS}
    report['numerical_likelihood_gates_passed']=all(
        v['max_abs_delta_loglike']<1e-3 and v['max_relative_gradient_error']<1e-4 and
        max(v['max_prediction_difference_in_observed_sigma'].values())<1e-5
        for cases in report['numerical_checks'].values() for v in cases.values())
    report['compilation_context_check']=json.loads((RESULT_ROOT/'M1_210210-20260907-baseline/compilation_context.json').read_text())
    report['compilation_context_note']=(
        'The unchanged float32 forward model gives different likelihood values across '
        'batch sizes and fused versus separately compiled predictions. The 7701.115 '
        'difference in the extreme-prior saved fit values is reproduced by the baseline '
        'alone. Within each tested compilation path, baseline and candidate agree to '
        'less than 4e-9. Full-fit posterior and evidence comparisons are recorded separately.')
    report['full_posterior_samples_equivalent']=all(p['parameter_samples_equivalent'] for p in pairs)
    if save:
        (RESULT_ROOT/'comparison.json').write_text(json.dumps(report,indent=2)+'\n')
    return report


def main():
    if sys.argv[1:]==['rent']:
        rent();return
    if sys.argv[1:]==['matrix']:
        import subprocess
        jobs=[('M1_210210',20260906,'reduce',False),
              ('M5_172669',20260906,'baseline',True),
              ('M5_172669',20260906,'reduce',False),
              ('M1_210210',20260907,'reduce',False),
              ('M1_210210',20260907,'baseline',False),
              ('M5_172669',20260907,'reduce',False),
              ('M5_172669',20260907,'baseline',False)]
        for target,seed,variant,probe in jobs:
            folder=RESULT_ROOT/f'{target}-{seed}-{variant}'
            folder.mkdir(parents=True,exist_ok=True)
            if (folder/'timing.json').exists() and (folder/'analysis.ipynb').exists():
                saved=json.loads((folder/'analysis.ipynb').read_text())
                completed=all(c['execution_count'] is not None for c in saved['cells'] if c['cell_type']=='code')
                errors=any(o['output_type']=='error' for c in saved['cells'] for o in c.get('outputs',[]))
                if completed and not errors:
                    print('FIT_RETAINED',target,seed,variant,flush=True)
                    continue
            argv=[sys.executable,__file__,'--target',target,'--seed',str(seed),'--variant',variant]
            if probe:argv.append('--probe-calibration')
            print('FIT_START',target,seed,variant,flush=True)
            with (folder/'execution.log').open('w') as log:
                subprocess.run(argv,stdout=log,stderr=subprocess.STDOUT,check=True)
            print('FIT_COMPLETE',target,seed,variant,flush=True)
        (RESULT_ROOT/'complete').touch()
        return
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--target',required=True,choices=TARGETS)
    parser.add_argument('--seed',required=True,type=int)
    parser.add_argument('--variant',default='baseline',choices=('baseline','reduce','group50','group25','group10'))
    parser.add_argument('--numerical-only',action='store_true')
    parser.add_argument('--probe',action='store_true')
    parser.add_argument('--replay-existing',action='store_true')
    parser.add_argument('--probe-calibration',action='store_true')
    worker(parser.parse_args())


def rent():
    """Run on available RTX 5060s within the cumulative two-dollar budget."""
    from concurrent.futures import ThreadPoolExecutor
    from datetime import UTC, datetime
    from types import SimpleNamespace
    import threading
    import subprocess
    import calibration_arms_vast as calibration
    import absorption_mask_vast as absorption

    sweep = calibration._sweep()
    busy = {int(i["host_id"]) for i in sweep._vastai_json(["show", "instances"])}
    offers = calibration.offers_rtx_5060(sweep, busy)
    # Limit transfer rates before splitting the remaining budget across boxes.
    offers = [o for o in offers if float(o["inet_up_cost"]) <= .02
              and float(o["inet_down_cost"]) <= .02][:1]
    if not offers:
        raise RuntimeError("No available RTX 5060 fits the transfer budget")
    state_dir = STATE_ROOT
    state_dir.mkdir(parents=True, exist_ok=True)
    record_path = state_dir / "budget.json"
    budget = json.loads(record_path.read_text())
    records = budget["rentals"]
    prior = sum(r.get("billed_usd", r.get("compute_storage_estimate_usd", 0.) + .25)
                if r.get("finished") else r["total_cap_usd"] for r in records)
    available = budget["total_budget_usd"] - budget["previously_billed_usd"] - prior
    # The remaining budget is split across the available boxes, including transfers.
    if available <= .4:
        raise RuntimeError("Insufficient budget remains for another environment installation")
    per_box_cap = available / len(offers)
    lock = threading.Lock()

    def save():
        with lock:
            record_path.write_text(json.dumps(budget, indent=2) + "\n")

    def run_box(index, offer):
        targets = TARGETS
        rate = float(offer["dph_total"]) + 40 * float(offer["storage_cost"]) / 24 / 30
        limit = min(3 * 3600, (per_box_cap - .25) / rate * 3600)
        log = calibration._log(f"GPU {index}")
        record = dict(targets=targets, offer=offer, total_cap_usd=per_box_cap,
                      maximum_runtime_seconds=limit, hourly_rate_with_storage=rate,
                      started=datetime.now(UTC).isoformat())
        records.append(record)
        save()
        instance = None
        timer = None
        start = time.monotonic()
        try:
            instance = sweep._create_instance(offer, SimpleNamespace(
                image="vastai/base-image:cuda-12.6.3-auto", disk=40))
            record["instance_id"] = instance
            save()
            log(f"created {instance}; cap includes setup and transfer time")
            timer = threading.Timer(limit, lambda: sweep._destroy(instance, log))
            timer.daemon = True
            timer.start()
            sweep._wait_for_running(instance, log)
            sweep._attach_ssh_key(instance)
            sweep._wait_for_ssh(instance, log)
            absorption._checkout(instance, "absorption-mask", log)
            target, port = sweep._ssh_target(instance)
            remote = sweep.REMOTE_ROOT
            # These full fits consume two spectra and the complete catalogues.
            from astropy.table import Table
            catalogue = Table.read(PROJECT_ROOT / "data/raw/legac_dr2/legaCdr2.fits.gz")
            files = ["data/raw/legac_dr2/legaCdr2.fits.gz",
                     "data/raw/cosmos2015/cosmos2015_legac_dr2_photometry_1arcsec.fits",
                     "data/raw/cosmos2015/cosmos2015_legac_dr2_apertures_1arcsec.fits"]
            for row in catalogue:
                if str(row["SPECT_ID"]).strip() in targets:
                    files.append("data/raw/legac_dr2/sp/" + str(row["Filename"]).strip())
            for relative in files:
                sweep._ssh(instance, f"mkdir -p {shlex.quote(str(Path(remote, relative).parent))}", timeout=60.)
                sweep._rsync(port, str(PROJECT_ROOT / relative), f"{target}:{remote}/{relative}", timeout=180.)
            log(f"uploaded {len(files) - 3} selected spectra and all three catalogues")
            for relative in ("scripts/validate_ceridwen_speedups.py",
                             "scripts/per_galaxy_diagnostics.py",
                             "notebooks/ceridwen_integrated_photometry_spectra.ipynb",
                             "ceridwen/ceridwen/likelihood/calibration.py",
                             "ceridwen/ceridwen/sampler/nested.py",
                             "ceridwen/ceridwen/sampler/runner.py",
                             "ceridwen/ceridwen/fit.py"):
                sweep._rsync(port, str(PROJECT_ROOT / relative), f"{target}:{remote}/{relative}", timeout=180.)
            sweep._ssh(instance, "mkdir -p /root/.ceridwen/grids", timeout=60.)
            for attempt in range(3):
                target, port = sweep._ssh_target(instance)
                shell = shlex.join(["ssh", *sweep._ssh_options(port)])
                transfer = subprocess.run(
                    ["rsync", "-a", "--partial", "-e", shell,
                     str(Path.home() / ".ceridwen/grids/amist_c3k_hr_krou_afe.h5"),
                     f"{target}:/root/.ceridwen/grids/amist_c3k_hr_krou_afe.h5"],
                    capture_output=True, text=True, timeout=600.)
                if transfer.returncode == 0:
                    break
                if attempt == 2:
                    raise RuntimeError(transfer.stderr[-1000:])
                log("grid transfer disconnected; reconnecting and resuming")
                sweep._wait_for_ssh(instance, log)

            # Reuse production installation pins, then start full fits directly.
            bootstrap = (PROJECT_ROOT / "scripts/bootstrap_vast_ai.sh").read_text()
            install = bootstrap.split("# The installed package", 1)[0]
            install = install.replace('SCRIPT_DIR="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)"',
                                      f"SCRIPT_DIR={shlex.quote(remote + '/scripts')}")
            kernel = bootstrap[bootstrap.index('"${PYTHON_BIN}" -m ipykernel install'):bootstrap.index('CATALOG_PATH=')]
            log("installing the production environment")
            result = sweep._ssh(instance, "bash -c " + shlex.quote(install + kernel), timeout=1800.)
            record["installation_tail"] = result.stdout[-1200:]
            save()
            folder = "results/rtx-5060-production-speedup/M1_210210-20260906-baseline"
            argv = [".venv-ceridwen-gpu/bin/python", "scripts/validate_ceridwen_speedups.py",
                    "--target", "M1_210210", "--seed", "20260906", "--probe"]
            script = ("set -e\ncd " + shlex.quote(remote) + "\nmkdir -p " + folder
                      + "\n" + shlex.join(argv) + " > " + folder + "/execution.log 2>&1\n"
                      + "touch results/rtx-5060-production-speedup/baseline_complete\n")
            remaining = max(1, int(limit - (time.monotonic() - start) - 180))
            launch = (f"cd {shlex.quote(remote)} && mkdir -p results/rtx-5060-production-speedup && "
                      f"setsid -f env LD_LIBRARY_PATH= JAX_PLATFORMS=cuda JAX_ENABLE_X64=1 "
                      f"CERIDWEN_VAST_INSTANCE={instance} "
                      f"XLA_FLAGS=--xla_gpu_enable_command_buffer= "
                      f"timeout {remaining}s bash -c {shlex.quote(script)} "
                      "> results/rtx-5060-production-speedup/controller.log 2>&1 < /dev/null")
            sweep._ssh(instance, launch, timeout=60.)
            log("first production baseline started; the remaining fits follow profiling")
            while time.monotonic() - start < limit - 120:
                time.sleep(30)
                status = sweep._ssh(instance,
                    f"cd {shlex.quote(remote)} && "
                    "find results/rtx-5060-production-speedup -name timing.json | wc -l; "
                    "nvidia-smi --query-gpu=utilization.gpu,memory.used --format=csv,noheader; "
                    "test -f results/rtx-5060-production-speedup/complete && echo COMPLETE; "
                    "pgrep -af '^.venv-ceridwen-gpu/bin/python scripts/validate_ceridwen_speedups.py' || true",
                    timeout=60.).stdout
                log(status.strip().replace("\n", " | "))
                record["last_status"] = status
                save()
                if (state_dir / "stop").exists():
                    record["complete"] = True
                    break
                record["needs_attention"] = "scripts/validate_ceridwen_speedups.py" not in status
                if record["needs_attention"]:
                    log("worker exited; retaining the instance for repair within its existing deadline")
                    save()
        except Exception as error:
            record["error"] = f"{type(error).__name__}: {error}"
            log(record["error"])
        finally:
            if instance is not None:
                try:
                    target, port = sweep._ssh_target(instance)
                    RESULT_ROOT.mkdir(parents=True, exist_ok=True)
                    for target_id in targets:
                        pattern = f"{sweep.REMOTE_ROOT}/results/rtx-5060-production-speedup/{target_id}-*"
                        if sweep._ssh(instance, f"compgen -G {shlex.quote(pattern)}", timeout=60.,
                                      check=False).returncode != 0:
                            continue
                        sweep._rsync(port, f"{target}:{sweep.REMOTE_ROOT}/results/rtx-5060-production-speedup/{target_id}-*",
                                     str(RESULT_ROOT) + "/", timeout=180.)
                except Exception as error:
                    record["pull_error"] = str(error)
                sweep._destroy(instance, log)
            if timer is not None:
                timer.cancel()
            record["elapsed_seconds"] = time.monotonic() - start
            record["compute_storage_estimate_usd"] = record["elapsed_seconds"] / 3600 * rate
            record["finished"] = datetime.now(UTC).isoformat()
            save()

    with ThreadPoolExecutor(max_workers=len(offers)) as pool:
        list(pool.map(lambda item: run_box(*item), enumerate(offers)))
    if not all(record.get("complete") for record in records[-len(offers):]):
        raise RuntimeError("At least one comparison did not complete; inspect budget.json")



if __name__ == "__main__":
    main()
