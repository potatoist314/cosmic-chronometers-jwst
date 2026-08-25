"""Lick-index fitting helpers that are safe to call from worker processes."""

import emcee
import numpy as np
from scipy.interpolate import RegularGridInterpolator


_WORKER_STATE = None


def log_prob_factory(interp, obs, err, sigma, lo, hi):
    """Return the vectorized Borghi et al. (2022a) Equation 7 likelihood."""

    def log_prob(theta):
        theta = np.atleast_2d(theta)
        inside = np.all((theta >= lo) & (theta <= hi), axis=1)
        out = np.full(len(theta), -np.inf)
        if inside.any():
            points = np.column_stack([theta[inside], np.full(inside.sum(), sigma)])
            chi2 = np.sum(((obs - interp(points)) / err) ** 2, axis=1)
            out[inside] = -0.5 * chi2
        return out

    return log_prob


def fit_galaxy_arrays(
    obs,
    err,
    sigma_star,
    index_names,
    *,
    ages,
    mets,
    alphas,
    sigmas,
    sigma_grid,
    all_indices,
    offset_kms2,
    nwalkers=64,
    nsteps=10_000,
    burn=2_000,
    seed=0,
):
    """Fit one galaxy and return posterior summaries, or a skip reason."""
    obs = np.asarray(obs, dtype=float)
    err = np.asarray(err, dtype=float)
    valid = np.isfinite(obs) & np.isfinite(err) & (err > 0)

    if not valid.all():
        return None, f"{(~valid).sum()} invalid requested indices"
    if not np.isfinite(sigma_star):
        return None, "missing stellar velocity dispersion"

    index_columns = {name: column for column, name in enumerate(all_indices)}
    columns = [index_columns[name] for name in index_names]

    interp = RegularGridInterpolator(
        (ages, mets, alphas, sigmas),
        sigma_grid[..., columns],
        bounds_error=False,
        fill_value=np.nan,
    )

    sigma = min(
        np.sqrt(max(float(sigma_star) ** 2 + offset_kms2, 0.0)),
        sigmas[-1],
    )
    lo = np.array([ages.min(), mets.min(), alphas.min()])
    hi = np.array([ages.max(), mets.max(), alphas.max()])

    rng = np.random.default_rng(seed)
    p0 = rng.uniform(
        lo + 0.05 * (hi - lo),
        hi - 0.05 * (hi - lo),
        (nwalkers, 3),
    )

    sampler = emcee.EnsembleSampler(
        nwalkers,
        3,
        log_prob_factory(interp, obs, err, sigma, lo, hi),
        vectorize=True,
    )
    # emcee uses its own legacy RandomState; set it as well as the walker seed.
    sampler.random_state = np.random.RandomState(seed).get_state()
    sampler.run_mcmc(p0, nsteps, progress=False)

    chain = sampler.get_chain(discard=burn)
    q_lo, median, q_hi = np.percentile(chain.reshape(-1, 3), [16, 50, 84], axis=0)
    tau = emcee.autocorr.integrated_time(chain, tol=0)

    return {
        "n_indices": len(columns),
        "tau_max": tau.max(),
        "age": median[0],
        "age_lo": q_lo[0],
        "age_hi": q_hi[0],
        "ZH": median[1],
        "ZH_lo": q_lo[1],
        "ZH_hi": q_hi[1],
        "aFe": median[2],
        "aFe_lo": q_lo[2],
        "aFe_hi": q_hi[2],
    }, None


def initialize_fit_worker(
    ages,
    mets,
    alphas,
    sigmas,
    sigma_grid,
    all_indices,
    offset_kms2,
    nwalkers,
    nsteps,
    burn,
):
    """Copy immutable model data into one worker when its process starts."""
    global _WORKER_STATE
    _WORKER_STATE = {
        "ages": np.asarray(ages),
        "mets": np.asarray(mets),
        "alphas": np.asarray(alphas),
        "sigmas": np.asarray(sigmas),
        "sigma_grid": np.asarray(sigma_grid),
        "all_indices": tuple(all_indices),
        "offset_kms2": float(offset_kms2),
        "nwalkers": int(nwalkers),
        "nsteps": int(nsteps),
        "burn": int(burn),
    }


def fit_galaxy_task(task):
    """Run one serializable galaxy task inside an initialized worker."""
    if _WORKER_STATE is None:
        raise RuntimeError("initialize_fit_worker must run before fit_galaxy_task")

    identity = {
        "combo": task["combo"],
        "OBJECT": task["OBJECT"],
        "z": task["z"],
        "sigma_star": task["sigma_star"],
        "SN": task["SN"],
    }

    try:
        result, reason = fit_galaxy_arrays(
            task["obs"],
            task["err"],
            task["sigma_star"],
            task["index_names"],
            seed=task["seed"],
            **_WORKER_STATE,
        )
    except Exception as exc:
        return identity | {
            "status": "failed",
            "reason": f"{type(exc).__name__}: {exc}",
        }

    if result is None:
        return identity | {"status": "skipped", "reason": reason}
    return identity | {"status": "completed", "reason": None} | result
