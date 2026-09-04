#!/usr/bin/env python3
"""Build a standalone Ceridwen checkpoint spectrum animation.

The legacy DR2 mode reconstructs the model from the maintained DR2 builder and
uses three scientifically distinct states: the prior predictive distribution,
the last retained periodic checkpoint, and the converged rescue posterior.
Older periodic states cannot be recovered because the legacy writer overwrote
one checkpoint filename.  New schema-2 runs retain compact frame files.
"""

from __future__ import annotations

import argparse
import hashlib
import html
import json
import os
import pickle
import re
from pathlib import Path

import numpy as np

PROJECT_ROOT = Path(__file__).resolve().parents[1]
PAYLOAD_PATTERN = re.compile(
    r'<script id="checkpoint-data" type="application/json">(.*?)</script>', re.S
)
SCIENTIFIC_SHARED_KEYS = (
    "wavelength",
    "observed",
    "uncertainty",
    "target",
    "n_draws",
)
SCIENTIFIC_FRAME_KEYS = (
    "label",
    "kind",
    "iteration",
    "likelihood_calls",
    "discarded",
    "live",
    "ess",
    "logZ",
    "delta_logZ",
    "residual_uncertainty",
    "calibration_fraction",
    "model_q16",
    "model_q50",
    "model_q84",
)


def load_checkpoint_metadata(path: Path) -> dict:
    """Load old or new Ceridwen snapshots and normalize stored metadata."""
    with path.open("rb") as handle:
        checkpoint = pickle.load(handle)
    progress = dict(checkpoint.get("progress", {}))
    return {
        "schema_version": int(checkpoint.get("schema_version", 1)),
        "partial": bool(checkpoint["partial"]),
        "n_dead": int(checkpoint["n_dead"]),
        "logZ": float(checkpoint["logZ"]),
        "progress": progress,
        "positions": checkpoint["positions"],
        "loglikelihood": checkpoint["loglikelihood"],
        "loglikelihood_birth": checkpoint["loglikelihood_birth"],
    }


def load_saved_spectrum(path: Path) -> dict:
    """Load the exact observation arrays recorded with a legacy fit."""
    import h5py

    with h5py.File(path) as result:
        spectrum = result["obs/spectrum"]
        return {
            "wave_vac": spectrum["wavelength"][...],
            "flux": spectrum["flux"][...],
            "uncertainty": spectrum["uncertainty"][...],
            "mask": spectrum["mask"][...],
        }


def equal_weight_draws(checkpoint: dict, count: int) -> tuple[dict, float]:
    """Deterministically resample a nested posterior and return its ESS."""
    from anesthetic import NestedSamples

    names = list(checkpoint["positions"])
    blocks = [
        np.asarray(checkpoint["positions"][name]).reshape(checkpoint["n_dead"], -1)
        for name in names
    ]
    nested = NestedSamples(
        data=np.hstack(blocks),
        logL=np.asarray(checkpoint["loglikelihood"]),
        logL_birth=np.asarray(checkpoint["loglikelihood_birth"]),
        logzero=float("nan"),
    )
    log_weights = np.asarray(nested.logw(), dtype=float)
    weights = np.exp(log_weights - np.max(log_weights))
    weights /= weights.sum()
    targets = (np.arange(count, dtype=float) + 0.5) / count
    indices = np.searchsorted(np.cumsum(weights), targets, side="left")
    draws = {
        name: np.asarray(values)[indices]
        for name, values in checkpoint["positions"].items()
    }
    return draws, float(1.0 / np.sum(weights**2))


def prior_draws(model, names: list[str], count: int, seed: int) -> dict:
    """Draw a fixed-seed prior-predictive sample for the requested parameters."""
    import jax

    key = jax.random.PRNGKey(seed)
    draws = {}
    for name in names:
        key, subkey = jax.random.split(key)
        draws[name] = np.asarray(
            model.priors[name].sample(
                subkey, shape=(count, *model.theta_init[name].shape)
            )
        )
    return draws


def _frame(
    label: str,
    kind: str,
    spectrum: dict,
    *,
    iteration: int | None,
    likelihood_calls: int | None,
    discarded: int,
    live: int,
    ess: float,
    logz: float | None,
    delta_logz: float | None,
) -> dict:
    return {
        "label": label,
        "kind": kind,
        "iteration": iteration,
        "likelihood_calls": likelihood_calls,
        "discarded": discarded,
        "live": live,
        "ess": ess,
        "logZ": logz,
        "delta_logZ": delta_logz,
        "residual_uncertainty": np.asarray(spectrum["residual_uncertainty"]),
        "calibration_fraction": float(spectrum["calibration_fraction"]),
        "model_q16": np.asarray(spectrum["model_q16"]),
        "model_q50": np.asarray(spectrum["model_q50"]),
        "model_q84": np.asarray(spectrum["model_q84"]),
    }


def build_legacy_dr2_frames(
    run_dir: Path,
    target: str,
    *,
    num_live: int,
    num_delete: int,
    num_inner_steps: int,
    count: int,
    seed: int,
) -> tuple[dict, list[dict]]:
    """Rebuild the DR2 model and evaluate the retained legacy states."""
    os.environ.setdefault("JAX_PLATFORMS", "cpu")
    os.environ.setdefault("JAX_ENABLE_X64", "True")
    published_grid_dir = Path.home() / ".ceridwen/grids"
    if "CERIDWEN_GRID_DIR" not in os.environ and published_grid_dir.is_dir():
        os.environ["CERIDWEN_GRID_DIR"] = str(published_grid_dir)

    from absorption_mask_analysis import build_notebook_model, load_target
    from ceridwen.plotting import spectrum_checkpoint_frame_fn

    result_path = run_dir / "ceridwen_result.h5"
    target_data = load_target(target)
    target_data.update(load_saved_spectrum(result_path))
    model, _, spectrum_observation, _ = build_notebook_model(target_data)
    checkpoints = sorted(run_dir.glob("ns_checkpoint_*.pkl"))
    checkpoints = [path for path in checkpoints if "frame" not in path.name]
    rescues = sorted(run_dir.glob("ns_raw_dead_*.pkl"))
    if len(checkpoints) != 1 or len(rescues) != 1:
        raise ValueError("legacy mode requires one periodic checkpoint and one rescue")

    partial = load_checkpoint_metadata(checkpoints[0])
    final = load_checkpoint_metadata(rescues[0])
    names = list(partial["positions"])
    source_data = PROJECT_ROOT / "data/raw/legac_dr2/sp" / f"legac_{target}_v2.0.fits"
    summarize = spectrum_checkpoint_frame_fn(
        model,
        spectrum_observation.name,
        source_run=str(run_dir),
        source_data=str(source_data),
    )

    prior_positions = prior_draws(model, names, count, seed)
    partial_positions, partial_ess = equal_weight_draws(partial, count)
    final_positions, final_ess = equal_weight_draws(final, count)
    prior_spectrum = summarize(prior_positions)
    partial_spectrum = summarize(partial_positions)
    final_spectrum = summarize(final_positions)

    partial_iteration = (partial["n_dead"] - num_live) // num_delete
    final_iteration = (final["n_dead"] - num_live) // num_delete
    frames = [
        _frame(
            "Prior predictive",
            "prior predictive model spectrum",
            prior_spectrum,
            iteration=0,
            likelihood_calls=0,
            discarded=0,
            live=num_live,
            ess=float(count),
            logz=None,
            delta_logz=None,
        ),
        _frame(
            "Last saved checkpoint",
            "partial checkpoint posterior model spectrum",
            partial_spectrum,
            iteration=partial_iteration,
            likelihood_calls=partial_iteration * num_delete * num_inner_steps,
            discarded=partial["n_dead"] - num_live,
            live=num_live,
            ess=partial_ess,
            logz=partial["logZ"],
            delta_logz=partial["progress"].get("delta_logZ"),
        ),
        _frame(
            "Converged rescue",
            "final posterior model spectrum",
            final_spectrum,
            iteration=final_iteration,
            likelihood_calls=final_iteration * num_delete * num_inner_steps,
            discarded=final["n_dead"] - num_live,
            live=num_live,
            ess=final_ess,
            logz=final["logZ"],
            delta_logz=final["progress"].get("delta_logZ"),
        ),
    ]
    shared = {
        "wavelength": np.asarray(final_spectrum["wavelength"]),
        "observed": np.asarray(final_spectrum["observed"]),
        "uncertainty": np.asarray(final_spectrum["uncertainty"]),
        "target": target,
        "source_run": str(run_dir),
        "source_data": str(source_data),
        "source_checkpoint": str(checkpoints[0]),
        "source_rescue": str(rescues[0]),
        "source_result": str(result_path),
        "n_draws": count,
    }
    return shared, frames


def _jsonable(value):
    if isinstance(value, dict):
        return {key: _jsonable(item) for key, item in value.items()}
    if isinstance(value, (list, tuple)):
        return [_jsonable(item) for item in value]
    if isinstance(value, np.ndarray):
        return [_jsonable(item) for item in value.tolist()]
    if isinstance(value, (np.floating, float)):
        return None if not np.isfinite(value) else float(value)
    if isinstance(value, np.integer):
        return int(value)
    return value


def load_embedded_payload(path: Path) -> tuple[str, dict]:
    """Load the exact embedded payload text from a generated viewer."""
    match = PAYLOAD_PATTERN.search(path.read_text())
    if match is None:
        raise ValueError(f"no checkpoint payload in {path}")
    payload = match.group(1)
    return payload, json.loads(payload)


def scientific_payload_sha256(payload: dict) -> str:
    """Hash checkpoint science independently from layout-only metadata."""
    scientific = {
        "shared": {
            key: payload["shared"][key] for key in SCIENTIFIC_SHARED_KEYS
        },
        "frames": [
            {key: frame[key] for key in SCIENTIFIC_FRAME_KEYS}
            for frame in payload["frames"]
        ],
    }
    canonical = json.dumps(
        scientific,
        sort_keys=True,
        separators=(",", ":"),
        ensure_ascii=False,
    ).encode()
    return hashlib.sha256(canonical).hexdigest()


def _file_url(path: str) -> str:
    return Path(path).resolve().as_uri()


def _fallback_svg(shared: dict, frame: dict) -> str:
    wave = np.asarray(shared["wavelength"], dtype=float)
    observed = np.asarray(shared["observed"], dtype=float)
    lower = np.asarray(frame["model_q16"], dtype=float)
    median = np.asarray(frame["model_q50"], dtype=float)
    upper = np.asarray(frame["model_q84"], dtype=float)
    visible = np.isfinite(wave) & np.isfinite(observed + lower + median + upper)
    x = wave[visible]
    arrays = [observed[visible], lower[visible], median[visible], upper[visible]]
    ymin = min(float(np.min(values)) for values in arrays)
    ymax = max(float(np.max(values)) for values in arrays)
    pad = 0.05 * (ymax - ymin or 1.0)
    ymin, ymax = ymin - pad, ymax + pad

    def xy(index, values):
        px = 70 + 790 * (wave[index] - x.min()) / (x.max() - x.min())
        py = 25 + 275 * (ymax - values[index]) / (ymax - ymin)
        return f"{px:.2f},{py:.2f}"

    def line_path(values):
        parts = []
        open_run = False
        for index in range(len(wave)):
            if np.isfinite(wave[index]) and np.isfinite(values[index]):
                parts.append(("L" if open_run else "M") + xy(index, values))
                open_run = True
            else:
                open_run = False
        return "".join(parts)

    runs = []
    run = []
    for index in range(len(wave)):
        if all(np.isfinite(values[index]) for values in (wave, lower, upper)):
            run.append(index)
        elif run:
            runs.append(run)
            run = []
    if run:
        runs.append(run)
    band = "".join(
        "M"
        + "L".join(xy(index, upper) for index in indices)
        + "L"
        + "L".join(xy(index, lower) for index in reversed(indices))
        + "Z"
        for indices in runs
    )
    return f"""
    <svg viewBox="0 0 900 340" role="img" aria-labelledby="fallback-title fallback-desc">
      <title id="fallback-title">Static final checkpoint spectrum</title>
      <desc id="fallback-desc">Observed spectrum, posterior median, and 16 to 84 percent model-spectrum interval.</desc>
      <rect x="70" y="25" width="790" height="275" class="plot-frame" />
      <path d="{band}" class="fallback-band" />
      <path d="{line_path(observed)}" class="fallback-observed" />
      <path d="{line_path(median)}" class="fallback-model" />
      <text x="465" y="330" text-anchor="middle">Observed wavelength [Å]</text>
      <text x="18" y="165" text-anchor="middle" transform="rotate(-90 18 165)">Fν [cgs]</text>
    </svg>"""


def render_html(
    shared: dict,
    frames: list[dict],
    *,
    title: str,
    command: str,
    payload_json: str | None = None,
    hosted: bool = False,
) -> str:
    """Render the self-contained checkpoint viewer."""
    payload = payload_json
    if payload is None:
        payload = json.dumps(
            _jsonable({"shared": shared, "frames": frames}),
            separators=(",", ":"),
            allow_nan=False,
        ).replace("</", "<\\/")
    fallback = _fallback_svg(shared, frames[-1])
    source_items = (
        ("source_run", "run directory"),
        ("source_data", "DR2 spectrum"),
        ("source_checkpoint", "saved checkpoint"),
        ("source_rescue", "converged rescue"),
        ("source_result", "saved fit"),
    )
    if hosted:
        source_links = " ".join(
            f'<span id="{key.replace("_", "-")}">'
            f'<a href="#{key.replace("_", "-")}">{label}</a>: '
            f'<code>{html.escape(shared[key])}</code></span>'
            for key, label in source_items
        )
        navigation = '<a href="../ceridwen-results.html">Ceridwen results board</a>'
    else:
        source_links = " ".join(
            f'<a href="{html.escape(_file_url(shared[key]))}">{label}</a>'
            for key, label in source_items
        )
        navigation = ""
    wiki_metadata = ""
    if hosted:
        wiki_metadata = """\n<meta name="wiki-type" content="analysis">
<meta name="wiki-status" content="current">
<meta name="wiki-updated" content="2026-09-04">"""
    return f"""<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">{wiki_metadata}
<link rel="icon" href="data:,">
<title>{html.escape(title)}</title>
<style>
:root {{ color-scheme: light dark; --paper:#fff; --ink:#17202a; --muted:#59636e; --line:#b8c0c8; --grid:#d9dee3; --obs:#3f4850; --model:#0969da; --band:#0969da33; --res:#bc4c00; --focus:#8250df; }}
@media (prefers-color-scheme: dark) {{ :root {{ --paper:#0d1117; --ink:#e6edf3; --muted:#9da7b1; --line:#57606a; --grid:#30363d; --obs:#c9d1d9; --model:#58a6ff; --band:#58a6ff38; --res:#ffa657; --focus:#d2a8ff; }} }}
* {{ box-sizing:border-box; }}
body {{ margin:0; background:var(--paper); color:var(--ink); font:16px/1.45 -apple-system,BlinkMacSystemFont,"Segoe UI",sans-serif; }}
main {{ width:min(1180px,calc(100% - 2rem)); margin:auto; padding:1.5rem 0 2.5rem; }}
h1 {{ margin:0 0 .35rem; font-size:clamp(1.45rem,4vw,2rem); line-height:1.2; }}
p {{ margin:.45rem 0; }}
.note {{ max-width:90ch; color:var(--muted); }}
.viewer {{ display:grid; gap:.4rem; }}
.controls {{ display:flex; flex-wrap:wrap; align-items:center; gap:.75rem; margin:1.1rem 0 .7rem; }}
button,select,input {{ font:inherit; }}
button {{ min-height:44px; min-width:64px; padding:.5rem 1rem; border:1px solid var(--line); border-radius:.35rem; color:var(--ink); background:var(--paper); cursor:pointer; }}
button:focus-visible,input:focus-visible {{ outline:3px solid var(--focus); outline-offset:2px; }}
label {{ display:flex; flex:1 1 20rem; align-items:center; gap:.65rem; }}
input[type=range] {{ width:100%; min-height:44px; cursor:pointer; }}
.frame-status {{ min-height:1.5rem; font-weight:600; }}
.mobile-progress {{ display:none; color:var(--muted); font-size:.78rem; font-variant-numeric:tabular-nums; }}
.metadata {{ display:grid; grid-template-columns:repeat(7,minmax(0,1fr)); gap:.65rem; margin:.7rem 0 1rem; }}
.metric {{ min-width:0; border-top:2px solid var(--line); padding-top:.35rem; }}
.metric span {{ display:block; color:var(--muted); font-size:.78rem; }}
.metric strong {{ display:block; overflow-wrap:anywhere; font-variant-numeric:tabular-nums; font-size:.95rem; }}
.legend {{ display:flex; flex-wrap:wrap; gap:0.5rem 1.25rem; margin:.5rem 0; color:var(--muted); font-size:.88rem; }}
.key {{ display:inline-flex; align-items:center; }}
.key::before {{ display:inline-block; width:1.5rem; height:.22rem; margin-right:.4rem; flex-shrink:0; vertical-align:middle; content:""; background:var(--key); }}
.key.band::before {{ height:.65rem; }}
.chart {{ width:100%; min-height:0; display:block; }}
.plot-frame {{ fill:none; stroke:var(--line); }}
.grid {{ stroke:var(--grid); stroke-width:1; }}
.axis {{ fill:var(--muted); font-size:12px; }}
.observed,.fallback-observed {{ fill:none; stroke:var(--obs); stroke-width:1; vector-effect:non-scaling-stroke; }}
.model,.fallback-model {{ fill:none; stroke:var(--model); stroke-width:2; vector-effect:non-scaling-stroke; }}
.band-shape,.fallback-band {{ fill:var(--band); stroke:none; }}
.residual-line {{ fill:none; stroke:var(--res); stroke-width:1.5; vector-effect:non-scaling-stroke; }}
.zero {{ stroke:var(--line); stroke-width:1; stroke-dasharray:5 4; }}
.sources,.reproduce {{ margin-top:1rem; color:var(--muted); font-size:.86rem; overflow-wrap:anywhere; }}
.sources a {{ color:var(--model); margin-right:.7rem; }}
code {{ font-family:ui-monospace,SFMono-Regular,Menlo,monospace; font-size:.88em; }}
.static-fallback {{ margin-top:1rem; }}
.static-fallback svg {{ width:100%; height:auto; }}
.provenance {{ margin-top:1rem; }}
.sources span {{ display:block; }}
@media (max-width:760px) {{ .metadata {{ grid-template-columns:repeat(3,minmax(0,1fr)); }} main {{ width:min(100% - 1rem,1180px); padding-top:.8rem; }} }}
@media (max-width:480px) {{
  .metadata {{ display:none; }}
  .mobile-progress {{ display:block; }}
  .legend {{ display:grid; grid-template-columns:repeat(2,minmax(0,1fr)); gap:.45rem .6rem; font-size:.82rem; }}
  .key {{ display:flex; align-items:center; min-width:0; line-height:1.25; }}
  .key::before {{ width:1.2rem; height:.2rem; margin-right:.35rem; flex-shrink:0; }}
  .key.band::before {{ height:.55rem; }}
}}
@media (max-width:430px) {{ .metadata {{ grid-template-columns:repeat(2,minmax(0,1fr)); }} .controls {{ align-items:stretch; }} label {{ flex-basis:100%; }} }}
@media (max-height:500px) {{
  main {{ width:calc(100% - 1rem); padding:.25rem 0 1rem; }}
  h1 {{ display:none; }}
  .controls {{ display:grid; grid-template-columns:auto 1fr; gap:.35rem; margin:0; }}
  .controls label {{ min-width:0; }}
  .metadata {{ display:none; }}
  .mobile-progress {{ display:block; white-space:nowrap; font-size:.72rem; }}
  .legend {{ margin:0; gap:.25rem 1rem; font-size:.78rem; }}
}}
@media (prefers-reduced-motion:reduce) {{ * {{ scroll-behavior:auto!important; }} }}
</style>
</head>
<body>
<main>
  <h1>{html.escape(title)}</h1>
  <div class="viewer">
  <div class="controls">
    <button id="play" type="button" aria-pressed="false">Play</button>
    <label for="frame">Inference state <input id="frame" type="range" min="0" max="{len(frames)-1}" step="1" value="0"></label>
  </div>
  <div id="frame-status" class="frame-status" aria-live="polite"></div>
  <div id="mobile-progress" class="mobile-progress"></div>
  <div class="metadata" aria-label="Inference progress">
    <div class="metric"><span>State</span><strong id="kind"></strong></div>
    <div class="metric"><span>Iteration</span><strong id="iteration"></strong></div>
    <div class="metric"><span>Likelihood calls</span><strong id="calls"></strong></div>
    <div class="metric"><span>Discarded / live</span><strong id="samples"></strong></div>
    <div class="metric"><span>Weighted ESS</span><strong id="ess"></strong></div>
    <div class="metric"><span>Calibration floor</span><strong id="floor"></strong></div>
    <div class="metric"><span>logZ / remaining</span><strong id="logz"></strong></div>
  </div>
  <div class="legend" aria-label="Legend">
    <span class="key" style="--key:var(--obs)">Observed spectrum</span>
    <span class="key" style="--key:var(--model)">Model median</span>
    <span class="key band" style="--key:var(--band)">16–84% model interval</span>
    <span class="key" style="--key:var(--res)">Residual / effective σ</span>
  </div>
  <svg id="spectrum" class="chart" role="img" aria-label="Observed and model spectrum with credible interval"></svg>
  <svg id="residual" class="chart residual" role="img" aria-label="Observed minus model residual in effective standard deviations"></svg>
  </div>
  <section class="provenance">
  <p class="note">The fixed observed spectrum comes from the saved fit. It is compared with model spectra from a prior sample, the last retained partial checkpoint, and the converged rescue posterior. Legacy runs overwrote earlier periodic checkpoints, so this page does not invent those missing states.</p>
  <p class="note">The band is the 16th–84th percentile of noiseless model spectra from {int(shared['n_draws'])} deterministic equal-weight draws. It shows parameter uncertainty, not measurement noise. Nested-sampling bands can widen or narrow between checkpoints.</p>
  <p class="note">The spectrum axis rescales for each state because the prior range is much wider. Compare the labelled flux values and residuals, not the apparent band height between states.</p>
  <p class="note">Residuals use the saved measurement uncertainty plus the state’s median sampled fractional calibration floor in quadrature.</p>
  <noscript><section class="static-fallback"><h2>Static final checkpoint</h2>{fallback}<p>Interactive controls require JavaScript. The final spectrum remains available above as a static SVG.</p></section></noscript>
  <p class="sources">Sources: {source_links}</p>
  <p class="reproduce">Reproduce: <code>{html.escape(command)}</code></p>
  <p class="sources">{navigation}</p>
  </section>
</main>
<script id="checkpoint-data" type="application/json">{payload}</script>
<script>
(() => {{
  const data=JSON.parse(document.getElementById('checkpoint-data').textContent);
  const frames=data.frames, shared=data.shared, slider=document.getElementById('frame'), play=document.getElementById('play');
  let timer=null;
  const ns='http://www.w3.org/2000/svg';
  const fmt=(v,d=0)=>v===null||v===undefined?'not stored':Number(v).toLocaleString(undefined,{{maximumFractionDigits:d}});
  const finite=v=>v!==null&&Number.isFinite(v);
  function el(name,attrs={{}},text=''){{const n=document.createElementNS(ns,name);for(const [k,v] of Object.entries(attrs))n.setAttribute(k,v);if(text)n.textContent=text;return n;}}
  function extent(arrays){{let lo=Infinity,hi=-Infinity;for(const arr of arrays)for(const v of arr)if(finite(v)){{lo=Math.min(lo,v);hi=Math.max(hi,v);}}const pad=(hi-lo||1)*.05;return [lo-pad,hi+pad];}}
  function path(values,xScale,yScale){{let d='',open=false;for(let i=0;i<values.length;i++){{const v=values[i];if(!finite(v)||!finite(shared.wavelength[i])){{open=false;continue;}}d+=(open?'L':'M')+xScale(shared.wavelength[i]).toFixed(2)+','+yScale(v).toFixed(2);open=true;}}return d;}}
  function band(lower,upper,xScale,yScale){{const runs=[];let run=[];for(let i=0;i<lower.length;i++){{if(finite(lower[i])&&finite(upper[i])&&finite(shared.wavelength[i]))run.push(i);else if(run.length){{runs.push(run);run=[];}}}}if(run.length)runs.push(run);return runs.map(indices=>{{const forward=indices.map((i,j)=>(j?'L':'M')+xScale(shared.wavelength[i]).toFixed(2)+','+yScale(upper[i]).toFixed(2)).join('');const reverse=[...indices].reverse().map(i=>'L'+xScale(shared.wavelength[i]).toFixed(2)+','+yScale(lower[i]).toFixed(2)).join('');return forward+reverse+'Z';}}).join('');}}
  function axes(svg,width,height,domain,yDomain,xLabel,yLabel,compactResidual=false){{const isNarrow=width<480,compact=compactResidual&&window.innerHeight<=500;const m={{l:compact?92:72,r:24,t:8,b:42}},iw=width-m.l-m.r,ih=height-m.t-m.b;const xs=x=>m.l+(x-domain[0])/(domain[1]-domain[0])*iw,ys=y=>m.t+(yDomain[1]-y)/(yDomain[1]-yDomain[0])*ih;svg.append(el('rect',{{x:m.l,y:m.t,width:iw,height:ih,class:'plot-frame'}}));const ticks=isNarrow?4:6;for(let i=0;i<ticks;i++){{const tx=domain[0]+i*(domain[1]-domain[0])/(ticks-1),x=xs(tx),anchor=i===0?'start':i===ticks-1?'end':'middle';svg.append(el('line',{{x1:x,y1:m.t,x2:x,y2:m.t+ih,class:'grid'}}));svg.append(el('text',{{x,y:height-22,'text-anchor':anchor,class:'axis'}},Math.round(tx).toLocaleString()));}}const yTicks=compact?3:5;for(let i=0;i<yTicks;i++){{const ty=yDomain[0]+i*(yDomain[1]-yDomain[0])/(yTicks-1),y=ys(ty);svg.append(el('line',{{x1:m.l,y1:y,x2:m.l+iw,y2:y,class:'grid'}}));svg.append(el('text',{{x:m.l-8,y:y+4,'text-anchor':'end',class:'axis'}},ty.toExponential(1)));}}svg.append(el('text',{{x:m.l+iw/2,y:height-4,'text-anchor':'middle',class:'axis'}},xLabel));const labelX=compact?22:14,yl=el('text',{{x:labelX,y:m.t+ih/2,'text-anchor':'middle',class:'axis',transform:`rotate(-90 ${{labelX}} ${{m.t+ih/2}})`}},yLabel);svg.append(yl);return {{xs,ys,m,iw,ih}};}}
  function plotHeights(width){{const short=window.innerHeight<=500;return short?[120,127]:width<480?[240,135]:[410,220];}}
  function draw(){{const index=Number(slider.value),frame=frames[index],status=`${{index+1}} / ${{frames.length}} — ${{frame.label}}`;document.getElementById('frame-status').textContent=status;document.getElementById('kind').textContent=frame.kind;document.getElementById('iteration').textContent=fmt(frame.iteration);document.getElementById('calls').textContent=fmt(frame.likelihood_calls);document.getElementById('samples').textContent=`${{fmt(frame.discarded)}} / ${{fmt(frame.live)}}`;document.getElementById('ess').textContent=fmt(frame.ess,1);document.getElementById('floor').textContent=`${{fmt(100*frame.calibration_fraction,2)}}%`;document.getElementById('logz').textContent=`${{fmt(frame.logZ,3)}} / ${{fmt(frame.delta_logZ,3)}}`;document.getElementById('mobile-progress').textContent=`Iter ${{fmt(frame.iteration)}} · calls ${{fmt(frame.likelihood_calls)}} · dead/live ${{fmt(frame.discarded)}}/${{fmt(frame.live)}} · ESS ${{fmt(frame.ess,1)}} · logZ ${{fmt(frame.logZ,3)}}`;
    const width=Math.max(320,document.getElementById('spectrum').clientWidth),[height,rh]=plotHeights(width),xDomain=extent([shared.wavelength]),yDomain=extent([shared.observed,frame.model_q16,frame.model_q84]);const svg=document.getElementById('spectrum');svg.replaceChildren();svg.setAttribute('viewBox',`0 0 ${{width}} ${{height}}`);svg.style.height=`${{height}}px`;const a=axes(svg,width,height,xDomain,yDomain,'Observed wavelength [Å]','Fν [cgs]');svg.append(el('path',{{d:band(frame.model_q16,frame.model_q84,a.xs,a.ys),class:'band-shape'}}));svg.append(el('path',{{d:path(shared.observed,a.xs,a.ys),class:'observed'}}));svg.append(el('path',{{d:path(frame.model_q50,a.xs,a.ys),class:'model'}}));
    const residual=shared.observed.map((v,i)=>finite(v)&&finite(frame.model_q50[i])&&finite(frame.residual_uncertainty[i])?(v-frame.model_q50[i])/frame.residual_uncertainty[i]:null);const abs=residual.filter(finite).map(Math.abs).sort((a,b)=>a-b),q=abs[Math.floor(.99*Math.max(0,abs.length-1))]||3,rmax=Math.max(3,q*1.1);const rsvg=document.getElementById('residual');rsvg.replaceChildren();rsvg.setAttribute('viewBox',`0 0 ${{width}} ${{rh}}`);rsvg.style.height=`${{rh}}px`;const ra=axes(rsvg,width,rh,xDomain,[-rmax,rmax],'Observed wavelength [Å]',((window.innerHeight<=500||rh<=135)?'Residual / σeff':'(observed − model) / σeff'),true);rsvg.append(el('line',{{x1:ra.m.l,y1:ra.ys(0),x2:ra.m.l+ra.iw,y2:ra.ys(0),class:'zero'}}));rsvg.append(el('path',{{d:path(residual,ra.xs,ra.ys),class:'residual-line'}}));
  }}
  function stop(){{if(timer)clearInterval(timer);timer=null;play.textContent='Play';play.setAttribute('aria-pressed','false');document.getElementById('frame-status').setAttribute('aria-live','polite');}}
  play.addEventListener('click',()=>{{if(timer){{stop();return;}}play.textContent='Pause';play.setAttribute('aria-pressed','true');document.getElementById('frame-status').setAttribute('aria-live','off');timer=setInterval(()=>{{if(Number(slider.value)>=frames.length-1){{stop();return;}}slider.value=String(Number(slider.value)+1);draw();}},1400);}});
  slider.addEventListener('input',()=>{{stop();draw();}});new ResizeObserver(draw).observe(document.querySelector('main'));window.addEventListener('resize',draw);window.addEventListener('orientationchange',draw);draw();
}})();
</script>
</body>
</html>
"""


def main(argv=None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--legacy-dr2-run", type=Path, required=True)
    parser.add_argument("--target", required=True)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--num-live", type=int, default=300)
    parser.add_argument("--num-delete", type=int, default=25)
    parser.add_argument("--num-inner-steps", type=int, default=40)
    parser.add_argument("--draws", type=int, default=128)
    parser.add_argument("--seed", type=int, default=20260904)
    parser.add_argument("--preserve-payload-from", type=Path)
    parser.add_argument("--hosted", action="store_true")
    args = parser.parse_args(argv)
    payload_json = None
    if args.preserve_payload_from:
        payload_json, payload = load_embedded_payload(args.preserve_payload_from)
        shared, frames = payload["shared"], payload["frames"]
        if shared["target"] != args.target:
            raise ValueError("preserved payload target does not match --target")
    else:
        shared, frames = build_legacy_dr2_frames(
            args.legacy_dr2_run,
            args.target,
            num_live=args.num_live,
            num_delete=args.num_delete,
            num_inner_steps=args.num_inner_steps,
            count=args.draws,
            seed=args.seed,
        )
    command = " ".join(
        part
        for part in (
            "python scripts/plot_ceridwen_checkpoint_evolution.py",
            f"--legacy-dr2-run {args.legacy_dr2_run}",
            f"--target {args.target}",
            (
                f"--preserve-payload-from {args.preserve_payload_from}"
                if args.preserve_payload_from
                else ""
            ),
            f"--output {args.output}",
            "--hosted" if args.hosted else "",
        )
        if part
    )
    document = render_html(
        shared,
        frames,
        title=f"Ceridwen checkpoint spectrum evolution — {args.target}",
        command=command,
        payload_json=payload_json,
        hosted=args.hosted,
    )
    args.output.parent.mkdir(parents=True, exist_ok=True)
    temporary = args.output.with_suffix(args.output.suffix + ".tmp")
    temporary.write_text(document, encoding="utf-8")
    temporary.replace(args.output)
    print(args.output)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
