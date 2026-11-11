#!/usr/bin/env python3
"""Local CPU information maps from existing LEGA-C fits; never run a sampler."""
from __future__ import annotations

import argparse
import ast
import contextlib
import csv
import gc
import hashlib
import io
import json
import os
from pathlib import Path
import shutil
import sys
import tempfile

os.environ.update(JAX_PLATFORMS="cpu", JAX_ENABLE_X64="1", MPLBACKEND="Agg",
                  CERIDWEN_PLOTS="0")
ROOT = Path(__file__).resolve().parents[3]
sys.path[:0] = [str(ROOT), str(ROOT / "ceridwen"), str(ROOT / "external/sedpy_jax")]
os.chdir(ROOT)

import h5py
import jax
import jax.numpy as jnp
import numpy as np
from jax.flatten_util import ravel_pytree

from ceridwen.fit import load_result_h5
from scripts.absorption_mask_report import weighted_quantiles
from scripts.run_ceridwen_vast_multi_gpu import _fit_notebook
from ceridwen.observation.absorption_features import ABSORPTION_FEATURES, absorption_feature_mask

OUT = Path(__file__).resolve().parent
BASE = OUT.parent


def sha(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def cases():
    targets = {t["spect_id"] for t in json.loads(
        (ROOT / "results/quiescent-test-set/targets.json").read_text())["targets"]}
    rows = list(csv.DictReader((BASE / "exp3-per-galaxy.csv").open()))
    return [row for row in rows if row["group"] == "legac"
            and row["arm"] in ("baseline", "cn") and row["target"] in targets]


def assemble(row):
    raw = BASE / row["result_path"]
    directory = raw.parent
    manifest = json.loads((directory.parents[2] / "manifest.json").read_text())
    cell = next(c for c in manifest["source"]["experiment"]
                if c["target"] == row["target"] and c["arm"] == row["arm"])
    settings = dict(cell["settings"])
    settings["ssp_grid"] = manifest["source"]["grid"]
    settings["mock_data"] = None
    os.environ.update(CERIDWEN_TARGET_ID=row["target"],
                      CERIDWEN_MANIFEST_INDEX=str(cell["target_metadata"]["manifest_index"]),
                      CERIDWEN_RANDOM_SEED=str(cell["seed"]),
                      CERIDWEN_RESULT_DIR=str(OUT / "assembly" / row["arm"] / row["target"]))
    namespace = {}
    text = io.StringIO()
    with contextlib.redirect_stdout(text), contextlib.redirect_stderr(text):
        document = _fit_notebook(json.dumps(settings), json.dumps(cell["priors"]))
        for index, notebook_cell in enumerate(document.cells[:9]):
            if notebook_cell.cell_type == "code":
                exec(compile(notebook_cell.source, f"production-cell-{index}", "exec"), namespace)
    model = namespace["joint_model"]
    assert namespace["joint_csp"].sfh_basis_fastpath
    fit = load_result_h5(raw)
    assert set(model.param_names) == set(fit.samples)
    theta = {}
    labels = []
    for name in sorted(fit.samples):
        values = np.asarray(fit.samples[name])
        shape = values.shape[1:]
        flat = values.reshape(len(fit.log_weights), -1)
        med = [weighted_quantiles(flat[:, i], fit.log_weights)[2]
               for i in range(flat.shape[1])]
        theta[name] = jnp.asarray(np.asarray(med).reshape(shape))
        labels.extend(name if flat.shape[1] == 1 else f"{name}[{i}]"
                      for i in range(flat.shape[1]))
    vector, unravel = ravel_pytree(theta)
    with h5py.File(directory / "ceridwen_derived_outputs.h5", "r") as stored:
        arrays = {group: {key: np.asarray(value) for key, value in stored[group].items()}
                  for group in ("spectrum", "photometry")}
        redshift = float(stored.attrs["redshift"])
    for group, obs in (("spectrum", namespace["spectrum_obs"]),
                       ("photometry", namespace["phot_obs"])):
        assert np.array_equal(np.asarray(obs.mask), arrays[group]["mask"])
        assert np.array_equal(np.asarray(obs.flux), arrays[group]["observed"])
    return namespace, fit, vector, unravel, labels, arrays, redshift, raw


def covariance(a, prior):
    """Invert the identifiable local quadratic after diagonal unit scaling."""
    keep = (np.max(np.abs(a), axis=0) > 0) | (np.max(np.abs(prior), axis=0) > 0)
    f = a[:, keep].T @ a[:, keep] + prior[np.ix_(keep, keep)]
    if np.any(np.diag(f) <= 0):
        return None, dict(status="nonpositive_diagonal", omitted=np.flatnonzero(~keep).tolist())
    scale = 1 / np.sqrt(np.diag(f))
    scaled = scale[:, None] * f * scale[None, :]
    eigenvalues = np.linalg.eigvalsh(scaled)
    info = dict(status="ok", omitted=np.flatnonzero(~keep).tolist(),
                scaled_min_eigenvalue=float(eigenvalues[0]),
                scaled_condition=float(eigenvalues[-1] / eigenvalues[0]))
    if eigenvalues[0] <= 0:
        info["status"] = "indefinite_local_prior_curvature"
        return None, info
    # Cholesky, without a ridge or eigenvalue clipping.
    chol = np.linalg.cholesky(scaled)
    inverse_chol = np.linalg.solve(chol, np.eye(len(chol)))
    reduced = scale[:, None] * (inverse_chol.T @ inverse_chol) * scale[None, :]
    cov = np.zeros((len(keep), len(keep)))
    cov[np.ix_(keep, keep)] = reduced
    return cov, info


def age_function(namespace, unravel):
    times = jnp.asarray(namespace["lookback_template"])

    def age(x):
        history = namespace["sfh_from_ratios"](unravel(x))
        masses = .5 * (history[:-1] + history[1:]) * jnp.diff(times) * 1e9
        return jnp.sum(masses * .5 * (times[:-1] + times[1:])) / jnp.sum(masses)

    return age


def data_regions(wave, redshift, smask, nphot):
    assigned = np.zeros(len(wave), bool)
    regions = {}
    explicit = ("Mgb", "CN4150", "G4300", "Fe4383", "C4668")
    definitions = [(name, [name]) for name in explicit]
    for label, group in (("Balmer", "balmer"), ("Fe_other", "fe")):
        definitions.append((label, [f.name for f in ABSORPTION_FEATURES
                                    if f.group == group and f.name not in explicit]))
    definitions.append(("features_other", [f.name for f in ABSORPTION_FEATURES
                                           if f.group not in ("balmer", "fe")
                                           and f.name not in explicit]))
    for name, selected in definitions:
        mask = absorption_feature_mask(wave, zred=redshift, features=selected) & ~assigned
        assigned |= mask
        regions[name] = np.r_[mask[smask], np.zeros(nphot, bool)]
    regions["remaining_spectrum"] = np.r_[~assigned[smask], np.zeros(nphot, bool)]
    regions["photometry"] = np.r_[np.zeros(int(smask.sum()), bool), np.ones(nphot, bool)]
    assert np.all(np.sum(list(regions.values()), axis=0) == 1)
    return regions


def analyse_case(row):
    ns, fit, x, unravel, labels, stored, redshift, raw = assemble(row)
    raw_digest = sha(raw)
    derived = raw.with_name("ceridwen_derived_outputs.h5")
    derived_digest = sha(derived)
    model = ns["joint_model"]
    # Execute only the production calibration assignment, never its sampler/warmup.
    doc = _fit_notebook(None, None)
    tree = ast.parse(doc.cells[10].source)
    assignment = next(node for node in tree.body if isinstance(node, ast.Assign)
                      and any(isinstance(t, ast.Name) and t.id == "calibration_polynomial"
                              for t in node.targets))
    exec(compile(ast.Module(body=[assignment], type_ignores=[]), "production-calibration", "exec"), ns)
    cal, lines = ns["calibration_polynomial"], ns["emission_line_columns"]
    smask = stored["spectrum"]["mask"].astype(bool)
    pmask = stored["photometry"]["mask"].astype(bool)
    ssigma = stored["spectrum"]["effective_uncertainty"]
    psigma = stored["photometry"].get("effective_uncertainty", stored["photometry"]["uncertainty"])
    sigma = np.r_[ssigma[smask], psigma[pmask]]
    residual = np.r_[stored["spectrum"]["pull"][smask], stored["photometry"]["pull"][pmask]]
    theta = unravel(x)
    continuum = model.predict_jit(theta)
    phi = lines.columns(theta)
    band = jnp.asarray(lines.band_matrix)
    phot = (band, jnp.asarray(stored["photometry"]["observed"]), continuum["photometry"],
            jnp.asarray(psigma), jnp.asarray(pmask))
    _, coeffs, fluxes, _ = cal.calibrate_with_lines(
        stored["spectrum"]["observed"], continuum["spectrum"], ssigma, smask,
        phi, pairs=lines.pairs, ridge=lines.ridge, photometry=phot)
    polynomial = cal.polynomial(coeffs)

    def prediction(vector):
        point = unravel(vector)
        p = model.predict(point)
        spec = polynomial * p["spectrum"] + lines.columns(point) @ fluxes
        photo = p["photometry"] + band @ fluxes
        return jnp.concatenate((spec[smask], photo[pmask]))

    y0 = np.asarray(jax.jit(prediction)(x))
    j = np.asarray(jax.jit(jax.jacfwd(prediction))(x))
    if not np.isfinite(j).all():
        raise RuntimeError("Production fast-path derivative unavailable; stop without model edits")
    a_phys = j / sigma[:, None]
    # The nuisance columns and their priors are the likelihood's exact linear system.
    bspec = np.c_[np.asarray(cal.basis) * np.asarray(continuum["spectrum"])[:, None], np.asarray(phi)]
    bphot = np.c_[np.zeros((len(psigma), cal.n_coeff)), np.asarray(band)]
    b = np.r_[bspec[smask], bphot[pmask]] / sigma[:, None]
    nphys = len(x)
    a = np.c_[a_phys, b]
    observed_prior_phys = np.asarray(-jax.hessian(lambda v: model.ln_prior(unravel(v)))(x))
    prior_phys = observed_prior_phys.copy()
    # The local Student-t Hessian can be negative. Use its positive expected
    # curvature (Bayesian prior Fisher information), with the observed case
    # retained below as an explicit diagnostic, never clipped or ridged.
    for name, distribution in model.priors.items():
        if type(distribution).__name__ == "StudentT":
            nu = float(distribution.params["df"])
            scale = float(distribution.params["scale"])
            expected = (nu + 1) / ((nu + 3) * scale**2)
            for index, label in enumerate(labels):
                if label == name or label.startswith(name+"["):
                    prior_phys[index, index] = expected
    precision = np.r_[1 / np.asarray(cal.prior_sigma) ** 2, np.asarray(lines.ridge)]
    prior = np.zeros((a.shape[1], a.shape[1]))
    prior[:nphys, :nphys] = prior_phys
    prior[nphys:, nphys:] = np.diag(precision)
    observed_prior = prior.copy()
    observed_prior[:nphys, :nphys] = observed_prior_phys
    _, observed_matrix_info = covariance(a, observed_prior)
    library_normal, _ = cal._joint_system(
        stored["spectrum"]["observed"], continuum["spectrum"], ssigma, smask,
        phi, lines.ridge, phot)
    normal = b.T @ b + np.diag(precision)
    diag_scale = 1 / np.sqrt(np.diag(normal))
    np.testing.assert_allclose(diag_scale[:, None] * normal * diag_scale[None, :],
                               diag_scale[:, None] * np.asarray(library_normal) * diag_scale[None, :],
                               rtol=1e-11, atol=1e-11)
    nuisance_names = [f"calibration_a{i}" for i in range(cal.n_coeff)] + list(lines.free_names)
    all_labels = labels + nuisance_names
    regions = data_regions(stored["spectrum"]["wavelength"], redshift, smask, int(pmask.sum()))
    coverage = "with_Mgb" if regions["Mgb"].any() else "without_Mgb"
    common = dict(target=row["target"], arm=row["arm"], coverage=coverage)
    age = age_function(ns, unravel)
    gradients = dict(afe=np.eye(a.shape[1])[labels.index("afe")],
                     age_gyr=np.r_[np.asarray(jax.grad(age)(x)), np.zeros(b.shape[1])])
    # Validate alpha and the most informative SFH coordinate with two step sizes.
    sfh_indices = [i for i, name in enumerate(labels) if name.startswith("logsfr_ratios[")]
    sfh_index = max(sfh_indices, key=lambda i: np.linalg.norm(a_phys[:, i]))
    fd_rows = []
    for index in (labels.index("afe"), sfh_index):
        for h in (1e-3, 5e-4):
            step = np.zeros(nphys); step[index] = h
            fd = (np.asarray(jax.jit(prediction)(x + step)) - np.asarray(jax.jit(prediction)(x - step))) / (2*h)
            relative = float(np.linalg.norm((fd-j[:, index])/sigma) / np.linalg.norm(a_phys[:, index]))
            fd_rows.append(common | dict(parameter=labels[index],step=h,whitened_relative_L2_error=relative))
        if min(r["whitened_relative_L2_error"] for r in fd_rows if r["parameter"] == labels[index]) > .02:
            raise RuntimeError(f"Finite differences do not validate {labels[index]}; stop without model edits")
    cov, matrix_info = covariance(a, prior)
    widths = []; regional = []; pixels = []; parameters = []
    for index, name in enumerate(all_labels):
        parameters.append(common | dict(parameter=name,kind="sampled" if index<nphys else "linear_nuisance",
                          whitened_derivative_norm=float(np.linalg.norm(a[:,index])),
                          prior_curvature=float(prior[index,index]),
                          observed_prior_curvature=float(observed_prior[index,index]),
                          fixed_weight_null=index in matrix_info["omitted"]))
    # Actual posterior widths use the stored distribution, not a refit.
    actual = {}
    q = weighted_quantiles(np.asarray(fit.samples["afe"]).reshape(len(fit.log_weights)), fit.log_weights)
    actual["afe"] = np.array(q[1:4])
    with h5py.File(derived,"r") as f:
        actual["age_gyr"] = np.quantile(f["sfh/mass_weighted_age_gyr"][:],[.16,.5,.84])
    prior_score = np.r_[np.asarray(jax.grad(lambda v: model.ln_prior(unravel(v)))(x)),
                         -precision*np.r_[np.asarray(coeffs),np.asarray(fluxes)]]
    forecasts = {"all":(cov,matrix_info)}
    for label, excluded in (("without_Mgb",regions["Mgb"]),
                            ("without_carbon",np.logical_or.reduce([regions[k] for k in ("CN4150","G4300","Fe4383","C4668")]))):
        forecasts[label] = covariance(a[~excluded],prior)
    for target,g in gradients.items():
        wrow = common | dict(quantity=target,unit="dex" if target=="afe" else "Gyr",
                              posterior_q16=float(actual[target][0]),posterior_q50=float(actual[target][1]),
                              posterior_q84=float(actual[target][2]),posterior_half_16_84=float((actual[target][2]-actual[target][0])/2),
                              expansion_value=float(x[labels.index("afe")]) if target=="afe" else float(age(x)))
        for scenario,(c,info) in forecasts.items():
            wrow[scenario+"_status"] = info["status"]
            wrow[scenario+"_sigma"] = float(np.sqrt(g@c@g)) if c is not None else np.nan
        widths.append(wrow)
        if cov is None:continue
        variance = float(g@cov@g);dual=cov@g;efficient=a@dual
        prior_information=float(dual@prior@dual/variance**2)
        data_information=float(efficient@efficient/variance**2)
        assert np.isclose((data_information+prior_information)*variance,1,rtol=2e-7)
        total_tug=float(efficient@residual)
        for region,mask in regions.items():
            information=float(np.sum(efficient[mask]**2)/variance**2)
            regional.append(common | dict(quantity=target,region=region,pixels=int(mask.sum()),
                            marginal_information=information,fraction_of_total_information=information*variance,
                            fraction_of_data_information=information/data_information,
                            delta=float(efficient[mask]@residual[mask]),sigma_all=float(np.sqrt(variance))))
        regional.append(common | dict(quantity=target,region="prior",pixels=0,
                        marginal_information=prior_information,fraction_of_total_information=prior_information*variance,
                        fraction_of_data_information=np.nan,delta=float(g@cov@prior_score),sigma_all=float(np.sqrt(variance))))
        wrow.update(total_data_tug=total_tug,prior_tug=float(g@cov@prior_score),
                    data_plus_prior_tug=total_tug+float(g@cov@prior_score),
                    scaled_min_eigenvalue=matrix_info["scaled_min_eigenvalue"])
        rsum=sum(r["delta"] for r in regional if r["quantity"]==target and r["region"]!="prior")
        assert np.isclose(rsum,total_tug,rtol=2e-9,atol=1e-10)
        for i in range(len(sigma)):
            kind="spectrum" if i<int(smask.sum()) else "photometry"
            native=np.flatnonzero(smask if kind=="spectrum" else pmask)[i if kind=="spectrum" else i-int(smask.sum())]
            region=next(k for k,v in regions.items() if v[i])
            wave=float(stored[kind]["wavelength"][native])
            pixels.append(common | dict(quantity=target,data_kind=kind,native_index=int(native),
                          observed_vacuum_A=wave,rest_vacuum_A=wave/(1+redshift),region=region,
                          stored_pull=float(residual[i]),marginal_information=float(efficient[i]**2/variance**2),
                          fraction_of_total_information=float(efficient[i]**2/variance),delta=float(efficient[i]*residual[i])))
    record=common | dict(raw=str(raw.relative_to(ROOT)),raw_sha256=raw_digest,
                         derived=str(derived.relative_to(ROOT)),derived_sha256=derived_digest,
                         fast_path=True, sampled_parameters=labels, nuisance_columns=nuisance_names,
                         conditional_polynomial=np.asarray(coeffs).tolist(),conditional_unconstrained_line_flux=np.asarray(fluxes).tolist(),
                         prior_descriptions={k:repr(v) for k,v in model.priors.items()},matrix=matrix_info,
                         observed_prior_matrix=observed_matrix_info,
                         negative_observed_prior_curvature_parameters=[all_labels[i] for i in np.flatnonzero(np.diag(observed_prior)<0)])
    assert sha(raw)==raw_digest and sha(derived)==derived_digest
    print(json.dumps(common | dict(matrix=matrix_info,finite_difference_max=max(r["whitened_relative_L2_error"] for r in fd_rows),
                                   forecasts=[{k:r[k] for k in ("quantity","all_sigma","without_Mgb_sigma","without_carbon_sigma","posterior_half_16_84")} for r in widths])),flush=True)
    return dict(widths=widths,regions=regional,pixels=pixels,parameters=parameters,finite_differences=fd_rows,record=record)


def self_test():
    from scipy.integrate import quad
    from scipy.stats import t
    a=np.array([[1.,2.],[3.,-1.],[2.,1.]])
    p=np.diag([.5,2.]);c,info=covariance(a,p)
    np.testing.assert_allclose(c,np.linalg.inv(a.T@a+p),rtol=1e-13)
    for g in (np.array([1.,0.]),np.array([.3,2.])):
        v=g@c@g;d=c@g
        assert np.isclose((np.sum((a@d)**2)+d@p@d)/v,1)
        r=np.array([1.,-2.,3.]);assert np.isclose(sum((a@d)*r),g@c@a.T@r)
    # Physical-unit rescaling leaves the propagated variance invariant.
    s=np.diag([1e-10,1e8]);cs,_=covariance(a@s,s@p@s)
    np.testing.assert_allclose(s@cs@s,c,rtol=1e-12)
    # Independent integration of -log p'' against the Student-t prior density.
    nu, scale = 2., .3
    def integrand(x):
        curvature=(nu+1)*(nu*scale**2-x*x)/(nu*scale**2+x*x)**2
        return curvature*t.pdf(x,df=nu,scale=scale)
    expected=(nu+1)/((nu+3)*scale**2)
    np.testing.assert_allclose(quad(integrand,-np.inf,np.inf)[0],expected,rtol=1e-11)
    print("Self-test: covariance, information decomposition, tug closure, units and expected Student-t curvature passed.")


def write_csv(filename, rows):
    fields=list(dict.fromkeys(k for row in rows for k in row))
    with (OUT/filename).open("w",newline="") as f:
        writer=csv.DictWriter(f,fieldnames=fields,lineterminator="\n")
        writer.writeheader();writer.writerows(rows)


def backup_outputs(names):
    existing=[OUT/name for name in names if (OUT/name).is_file()]
    if existing:
        destination=Path(tempfile.mkdtemp(prefix="cn-response-information-backup-"))
        for path in existing:shutil.copy2(path,destination/path.name)
        print(f"Existing outputs backed up to {destination}",flush=True)


def summarize():
    """Summaries of the saved per-galaxy calculations, with no model execution."""
    import pandas as pd
    widths=pd.read_csv(OUT/"widths.csv")
    regions=pd.read_csv(OUT/"regions.csv")
    keys=["target","arm","coverage","quantity"]
    widths["sigma_over_posterior_halfwidth"]=widths.all_sigma/widths.posterior_half_16_84
    widths["sigma_without_Mgb_over_all"]=widths.without_Mgb_sigma/widths.all_sigma
    widths["sigma_without_carbon_over_all"]=widths.without_carbon_sigma/widths.all_sigma
    def grouped(frame, extra=()):
        output=[]
        for group in ("all","with_Mgb","without_Mgb"):
            selected=frame if group=="all" else frame[frame.coverage==group]
            for index,sub in selected.groupby(["arm","quantity",*extra],sort=False):
                if not isinstance(index,tuple):index=(index,)
                row=dict(zip(["arm","quantity",*extra],index))
                row.update(coverage=group,galaxies=int(sub.target.nunique()))
                for column in sub.select_dtypes(include="number"):
                    values=sub[column].to_numpy();finite=values[np.isfinite(values)]
                    row[column]=float(np.median(finite)) if len(finite) else np.nan
                output.append(row)
        return output
    write_csv("medians-widths.csv",grouped(widths))
    write_csv("medians-regions.csv",grouped(regions,("region",)))
    comparisons=[]
    for key,sub in regions.groupby(keys,sort=False):
        by_region=sub.set_index("region")
        carbon=by_region.loc[["CN4150","G4300","Fe4383","C4668"]]
        row=dict(zip(keys,key))
        for label,part in (("Mgb",by_region.loc[["Mgb"]]),("carbon_union",carbon),
                           ("remaining",by_region.loc[["remaining_spectrum"]]),
                           ("photometry",by_region.loc[["photometry"]])):
            row[label+"_fraction_data"]=float(part.fraction_of_data_information.sum())
            row[label+"_fraction_total"]=float(part.fraction_of_total_information.sum())
            row[label+"_tug"]=float(part.delta.sum())
        row["prior_fraction_total"]=float(by_region.loc["prior","fraction_of_total_information"])
        comparisons.append(row)
    write_csv("region-comparisons.csv",comparisons)
    write_csv("medians-comparisons.csv",grouped(pd.DataFrame(comparisons)))
    metadata=json.loads((OUT/"inputs.json").read_text())
    metadata.setdefault("calculation_script_sha256",metadata["script_sha256"])
    metadata["script_sha256"]=sha(__file__)
    metadata["summary_convention"]="Medians of per-galaxy values; medians of region fractions need not sum to one. Coverage all/with_Mgb/without_Mgb. Carbon-union comparisons sum four regions within each galaxy before the group median."
    (OUT/"inputs.json").write_text(json.dumps(metadata,indent=2)+"\n")
    print("Wrote per-galaxy region comparisons and medians split by Mg b coverage.")


def check_outputs():
    """Independent accounting checks on CSVs and the original read-only inputs."""
    import pandas as pd
    from ceridwen.model import logsfr_ratios_to_sfh
    from scripts.absorption_mask_report import mass_weighted_age
    metadata=json.loads((OUT/"inputs.json").read_text())
    old=json.loads((BASE/"exp3-artifact-checks.json").read_text())
    assert len(metadata["records"])==20
    assert sha(ROOT/"notebooks/ceridwen_integrated_photometry_spectra.ipynb")==metadata["notebook_sha256"]
    widths=pd.read_csv(OUT/"widths.csv")
    regions=pd.read_csv(OUT/"regions.csv")
    pixels=pd.read_csv(OUT/"pixels.csv")
    fd=pd.read_csv(OUT/"finite-differences.csv")
    parameters=pd.read_csv(OUT/"parameters.csv")
    assert len(widths)==40 and len(regions)==440 and len(fd)==80
    assert (widths[["all_status","without_Mgb_status","without_carbon_status"]]=="ok").all().all()
    assert (widths.without_Mgb_sigma>=widths.all_sigma*(1-1e-10)).all()
    assert (widths.without_carbon_sigma>=widths.all_sigma*(1-1e-10)).all()
    absent=widths.coverage=="without_Mgb"
    np.testing.assert_allclose(widths.loc[absent,"without_Mgb_sigma"],widths.loc[absent,"all_sigma"],rtol=1e-12)
    assert fd.whitened_relative_L2_error.max()<.02
    assert parameters[parameters.fixed_weight_null].parameter.unique().tolist()==["log_f_calib"]
    keys=["target","arm","quantity"]
    for key,sub in regions.groupby(keys):
        w=widths[(widths.target==key[0])&(widths.arm==key[1])&(widths.quantity==key[2])].iloc[0]
        pp=pixels[(pixels.target==key[0])&(pixels.arm==key[1])&(pixels.quantity==key[2])]
        assert np.isclose(sub.marginal_information.sum(),1/w.all_sigma**2,rtol=2e-7)
        assert np.isclose(sub.fraction_of_total_information.sum(),1,rtol=2e-7)
        data=sub[sub.region!="prior"]
        assert np.isclose(data.fraction_of_data_information.sum(),1,rtol=2e-12)
        assert np.isclose(data.delta.sum(),w.total_data_tug,rtol=1e-8,atol=1e-10)
        for region,r in data.set_index("region").iterrows():
            selected=pp[pp.region==region]
            assert len(selected)==r.pixels
            assert np.isclose(selected.marginal_information.sum(),r.marginal_information,rtol=1e-9,atol=1e-10)
            assert np.isclose(selected.delta.sum(),r.delta,rtol=1e-8,atol=1e-10)
    age_errors=[]
    for r in metadata["records"]:
        assert sha(ROOT/r["raw"])==r["raw_sha256"] and sha(ROOT/r["derived"])==r["derived_sha256"]
        previous=next(o for o in old if o["result_sha256"]==r["raw_sha256"])
        assert previous["derived_sha256"]==r["derived_sha256"]
        fit=load_result_h5(ROOT/r["raw"])
        values=np.asarray(fit.samples["logsfr_ratios"])
        med=np.array([weighted_quantiles(values[:,i],fit.log_weights)[2] for i in range(values.shape[1])])
        with h5py.File(ROOT/r["derived"],"r") as source:
            times=np.asarray(source["sfh/lookback_time_gyr"])
        age=mass_weighted_age(med,times)
        w=widths[(widths.target==r["target"])&(widths.arm==r["arm"])&(widths.quantity=="age_gyr")].iloc[0]
        assert np.isclose(age,w.expansion_value,rtol=1e-11)
        if r["target"]=="M1_210210":
            def age_jax(v):
                history=logsfr_ratios_to_sfh(v,sfh_times_yr=times*1e9)
                masses=.5*(history[:-1]+history[1:])*jnp.diff(jnp.asarray(times))*1e9
                return jnp.sum(masses*.5*(times[:-1]+times[1:]))/jnp.sum(masses)
            grad=np.asarray(jax.grad(age_jax)(jnp.asarray(med)))
            for i in (0,len(med)-1):
                step=np.zeros_like(med);step[i]=1e-4
                numerical=(mass_weighted_age(med+step,times)-mass_weighted_age(med-step,times))/(2e-4)
                age_errors.append(abs(numerical-grad[i]));assert np.isclose(numerical,grad[i],atol=1e-7,rtol=1e-5)
    zero_width_groups=widths.groupby(["arm","coverage","quantity"]).size().to_dict()
    assert set(zero_width_groups.values())=={5}
    result=dict(fits=20,source_files_unchanged=40,source_files_match_experiment3=True,
                physical_jacobians_available=20,finite_difference_checks=len(fd),
                maximum_finite_difference_relative_L2_error=float(fd.whitened_relative_L2_error.max()),
                age_derivative_max_absolute_error_Gyr=float(max(age_errors)),
                gaussian_nuisance_normal_matches_likelihood=True,
                information_and_tug_accounting_passed=True,
                observed_local_prior_indefinite=sum(r["observed_prior_matrix"]["status"]!="ok" for r in metadata["records"]),
                expected_prior_positive_definite=20,source_notebook_unchanged=True,
                output_sha256={p.name:sha(p) for p in OUT.iterdir() if p.is_file() and p.name!="checks.json"})
    (OUT/"checks.json").write_text(json.dumps(result,indent=2)+"\n")
    print("PASS: 20 Jacobians; 80 finite differences; 40 unchanged original files; pixel/region information and tug closure; SFH age derivative and units.")


def derivative_probe(row):
    namespace, fit, vector, unravel, labels, stored, redshift, raw = assemble(row)
    model = namespace["joint_model"]
    masks = {k: np.asarray(stored[k]["mask"], bool) for k in stored}
    sigma = np.concatenate([stored[k]["effective_uncertainty"][masks[k]]
                            if "effective_uncertainty" in stored[k]
                            else stored[k]["uncertainty"][masks[k]]
                            for k in ("spectrum", "photometry")])

    def prediction(x):
        p = model.predict(unravel(x))
        return jnp.concatenate([p[k][masks[k]] for k in ("spectrum", "photometry")])

    # Populate the production model's static basis caches before differentiation.
    np.asarray(jax.jit(prediction)(vector))
    jacobian = np.asarray(jax.jit(jax.jacfwd(prediction))(vector))
    if not np.isfinite(jacobian).all():
        raise RuntimeError("Production fast-path Jacobian has non-finite derivatives; stop without model edits")
    prior_curvature = np.asarray(-jax.hessian(lambda x: model.ln_prior(unravel(x)))(vector))
    result = dict(target=row["target"], arm=row["arm"], raw=str(raw.relative_to(ROOT)),
                  raw_sha256=sha(raw), fast_path=True, sampled_dimension=len(vector),
                  pixels=len(sigma), labels=labels,
                  whitened_column_norm=np.linalg.norm(jacobian / sigma[:, None], axis=0).tolist(),
                  prior_curvature_diagonal=np.diag(prior_curvature).tolist())
    print(json.dumps(result), flush=True)
    return result


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--probe-only", action="store_true")
    parser.add_argument("--self-test", action="store_true")
    parser.add_argument("--summarize-only", action="store_true")
    parser.add_argument("--check-only", action="store_true")
    args = parser.parse_args()
    if args.self_test:
        self_test();return
    if args.summarize_only:
        backup_outputs(["inputs.json","medians-widths.csv","medians-regions.csv",
                        "region-comparisons.csv","medians-comparisons.csv"])
        summarize();return
    if args.check_only:
        backup_outputs(["checks.json"])
        check_outputs();return
    rows=cases()
    if args.probe_only:
        backup_outputs(["derivative-probe.json"])
        rows=[r for r in rows if r["target"]=="M1_210210"]
        results=[derivative_probe(row) for row in rows]
        (OUT/"derivative-probe.json").write_text(json.dumps(results,indent=2)+"\n");return
    backup_outputs(["widths.csv","regions.csv","pixels.csv","parameters.csv",
                    "finite-differences.csv","inputs.json","medians-widths.csv",
                    "medians-regions.csv","region-comparisons.csv",
                    "medians-comparisons.csv","checks.json"])
    results=[]
    for row in rows:
        results.append(analyse_case(row));jax.clear_caches();gc.collect()
    for key in ("widths","regions","pixels","parameters","finite_differences"):
        write_csv(key.replace("_","-")+".csv",[r for result in results for r in result[key]])
    (OUT/"inputs.json").write_text(json.dumps(dict(script_sha256=sha(__file__),
        notebook_sha256=sha(ROOT/"notebooks/ceridwen_integrated_photometry_spectra.ipynb"),
        prior_curvature="Student-t expected negative log-density Hessian: (nu+1)/((nu+3)*scale^2); all other priors use exact local negative Hessian; nuisance polynomial precision and line ridge from production likelihood",
        expansion="Componentwise weighted posterior medians; conditional unconstrained linear-nuisance modes under frozen stored effective uncertainties",
        approximations=["Gaussian linear-response Fisher, not a new fit",
          "Expected rather than observed Student-t prior curvature; observed-matrix status also recorded",
          "Stored effective uncertainties fixed; covariance derivatives and noise-scale information omitted",
          "Exact production calibration/line design and Gaussian precisions; positivity orthant and parameter-dependent marginal-volume curvature omitted",
          "Hard prior and SSP-grid boundaries do not truncate the Fisher covariance",
          "All exclusion forecasts use the same expansion point, Jacobian, calibration basis and priors",
          "Stored predictive-median pulls need not be residuals of the componentwise-median parameter point; no zero-tug recentering",
          "Mass-weighted age propagated through the production SFH mapping and notebook formed-mass convention"],
        records=[r["record"] for r in results]),indent=2)+"\n")
    summarize()
    check_outputs()


if __name__ == "__main__":
    main()
