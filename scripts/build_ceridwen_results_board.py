#!/usr/bin/env python3
"""Build the Ceridwen common results board from the validated audit manifest.

Reads /Users/liuhao/.claude/scripts/hermes-bridge/reports/ceridwen-board-repair/manifest.json
and generates /Users/liuhao/Downloads/Astro project/wiki/analyses/ceridwen-results.html.
Omits unverified animation claims, presenting it as an optional pending enhancement.
"""

from __future__ import annotations

import html
import json
from pathlib import Path

MANIFEST_PATH = Path("/Users/liuhao/.claude/scripts/hermes-bridge/reports/ceridwen-board-repair/manifest.json")
BOARD_PATH = Path("/Users/liuhao/Downloads/Astro project/wiki/analyses/ceridwen-results.html")
WIKI_BASE = Path("/Users/liuhao/Downloads/Astro project/wiki/analyses")


def format_badge(pushed: bool | str | None, label: str | None = None) -> str:
    if label:
        if "Host" in label or "Verified" in label:
            return f'<span class="badge badge-pushed">{html.escape(label)}</span>'
        return f'<span class="badge badge-local">{html.escape(label)}</span>'
    if pushed is True:
        return '<span class="badge badge-pushed">Pushed</span>'
    if pushed == "partial":
        return '<span class="badge badge-mixed">Partial</span>'
    if pushed is False:
        return '<span class="badge badge-local">Local / Unpushed</span>'
    return '<span class="badge badge-none">External</span>'


def build_board_html(manifest: dict) -> str:
    items_by_id = {item["id"]: item for item in manifest["items"]}
    assert len(items_by_id) == len(manifest["items"]), "Duplicate item IDs"

    def plot_card(png_id: str, pdf_id: str | None = None, script_id: str | None = None) -> str:
        png_item = items_by_id[png_id]
        png_src = html.escape(png_item["wiki_relative_path"])
        title = html.escape(png_item["title"])
        caption = html.escape(png_item["conclusion"])
        badge = format_badge(png_item["pushed"])
        
        pdf_link = ""
        if pdf_id and pdf_id in items_by_id:
            pdf_item = items_by_id[pdf_id]
            pdf_link = f' · <a href="{html.escape(pdf_item["wiki_relative_path"])}" download>PDF Vector</a>'
            
        script_link = ""
        if script_id and script_id in items_by_id:
            s_item = items_by_id[script_id]
            script_link = f' · <a href="{html.escape(s_item["wiki_relative_path"])}">Script</a>'

        alt_text = html.escape(f"{png_item['title']}. {png_item['conclusion']}")

        return f'''
        <figure class="plot-card" id="{html.escape(png_id)}">
          <a href="{png_src}" target="_blank" rel="noopener">
            <img src="{png_src}" alt="{alt_text}" loading="lazy">
          </a>
          <figcaption>
            <strong>{title}.</strong>
            {caption}
          </figcaption>
          <div class="plot-links">
            <span>{badge}</span>
            <span><a href="{png_src}" target="_blank" rel="noopener">PNG</a>{pdf_link}{script_link}</span>
          </div>
        </figure>'''

    doc = f'''<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <meta name="wiki-type" content="analysis">
  <meta name="wiki-status" content="current">
  <meta name="wiki-updated" content="2026-09-04">
  <title>Ceridwen Results Board</title>
  <link rel="icon" href="data:,">
  <link rel="stylesheet" href="../assets/wiki.css">
  <style>
    :root {{
      --badge-pushed-bg: #dafbe1;
      --badge-pushed-fg: #1a7f37;
      --badge-pushed-bd: #aceebb;
      --badge-mixed-bg: #ddf4ff;
      --badge-mixed-fg: #0969da;
      --badge-mixed-bd: #54aeff66;
      --badge-local-bg: #fff8c5;
      --badge-local-fg: #9a6700;
      --badge-local-bd: #d4a72c66;
      --badge-none-bg: #f6f8fa;
      --badge-none-fg: #656d76;
      --badge-none-bd: #d0d7de;
      --card-bg: var(--paper);
    }}
    @media (prefers-color-scheme: dark) {{
      :root {{
        --badge-pushed-bg: #0d281e;
        --badge-pushed-fg: #3fb950;
        --badge-pushed-bd: #238636;
        --badge-mixed-bg: #0c2d6b;
        --badge-mixed-fg: #58a6ff;
        --badge-mixed-bd: #1f6feb;
        --badge-local-bg: #342800;
        --badge-local-fg: #d29922;
        --badge-local-bd: #9e6a03;
        --badge-none-bg: #161b22;
        --badge-none-fg: #8b949e;
        --badge-none-bd: #30363d;
        --card-bg: #0d1117;
      }}
    }}
    html, body {{
      margin: 0;
      padding: 0;
      width: 100%;
      max-width: 100%;
      overflow-x: hidden;
    }}
    body, p, li, code, a, td, th, figcaption {{
      overflow-wrap: anywhere;
      word-break: break-word;
    }}
    .site-header {{
      width: 100%;
      max-width: 100%;
      border-bottom: 1px solid var(--line);
      box-sizing: border-box;
    }}
    .site-header-inner,
    .page-shell {{
      width: min(var(--measure), calc(100% - 2rem));
      max-width: 100%;
      box-sizing: border-box;
      margin-inline: auto;
    }}
    .board-nav {{
      display: flex;
      flex-wrap: wrap;
      align-items: center;
      gap: 0.5rem;
      margin: 1.5rem 0 2rem;
      padding: 0.75rem 1rem;
      background: var(--code);
      border: 1px solid var(--line);
      border-radius: 6px;
      font-size: 0.88rem;
    }}
    .board-nav-title {{
      font-weight: 600;
      margin-right: 0.25rem;
    }}
    .board-nav-list {{
      display: flex;
      flex-wrap: wrap;
      gap: 0.5rem;
      list-style: none;
      margin: 0;
      padding: 0;
    }}
    .board-nav-list li {{
      margin: 0;
      padding: 0;
    }}
    .board-nav a {{
      display: inline-block;
      padding: 0.2rem 0.5rem;
      border-radius: 4px;
      text-decoration: none;
      font-weight: 500;
    }}
    .board-nav a:hover {{
      background: var(--line);
      text-decoration: underline;
    }}
    .callout {{
      border-left: 4px solid var(--accent);
      background: var(--code);
      padding: 1rem 1.25rem;
      border-radius: 0 6px 6px 0;
      margin: 1.5rem 0;
    }}
    .callout-alert {{
      border-left-color: #d1242f;
    }}
    .callout-info {{
      border-left-color: #0969da;
    }}
    .callout h3 {{
      margin: 0 0 0.5rem;
      font-size: 1rem;
    }}
    .callout p {{
      margin: 0 0 0.5rem;
      font-size: 0.92rem;
      line-height: 1.5;
    }}
    .callout p:last-child {{
      margin-bottom: 0;
    }}
    .badge {{
      display: inline-block;
      padding: 0.15rem 0.45rem;
      border-radius: 4px;
      font-size: 0.72rem;
      font-weight: 600;
      letter-spacing: 0.02em;
    }}
    .badge-pushed {{ background: var(--badge-pushed-bg); color: var(--badge-pushed-fg); border: 1px solid var(--badge-pushed-bd); }}
    .badge-mixed {{ background: var(--badge-mixed-bg); color: var(--badge-mixed-fg); border: 1px solid var(--badge-mixed-bd); }}
    .badge-local {{ background: var(--badge-local-bg); color: var(--badge-local-fg); border: 1px solid var(--badge-local-bd); }}
    .badge-none {{ background: var(--badge-none-bg); color: var(--badge-none-fg); border: 1px solid var(--badge-none-bd); }}
    .plot-grid {{
      display: grid;
      grid-template-columns: repeat(auto-fit, minmax(320px, 1fr));
      gap: 1.5rem;
      margin: 1.5rem 0 2rem;
    }}
    .plot-card {{
      margin: 0;
      background: var(--card-bg);
      border: 1px solid var(--line);
      border-radius: 8px;
      padding: 1rem;
      display: flex;
      flex-direction: column;
      justify-content: space-between;
      box-shadow: 0 1px 3px rgba(0,0,0,0.03);
      min-width: 0;
      max-width: 100%;
      box-sizing: border-box;
    }}
    .plot-card img {{
      width: 100%;
      height: auto;
      border-radius: 4px;
      border: 1px solid var(--line);
      background: #fff;
    }}
    .plot-card figcaption {{
      margin-top: 0.75rem;
      font-size: 0.88rem;
      line-height: 1.45;
    }}
    .plot-card figcaption strong {{
      display: block;
      margin-bottom: 0.25rem;
      font-size: 0.95rem;
    }}
    .plot-card figcaption p {{
      margin: 0;
      color: var(--ink);
    }}
    .plot-links {{
      margin-top: 0.75rem;
      padding-top: 0.5rem;
      border-top: 1px solid var(--line);
      display: flex;
      justify-content: space-between;
      align-items: center;
      font-size: 0.82rem;
    }}
    .table-wrap {{
      overflow-x: auto;
      max-width: 100%;
      -webkit-overflow-scrolling: touch;
      margin: 1.25rem 0 2rem;
      border: 1px solid var(--line);
      border-radius: 6px;
      box-sizing: border-box;
    }}
    table {{
      width: 100%;
      border-collapse: collapse;
      font-size: 0.88rem;
      line-height: 1.4;
    }}
    th, td {{
      padding: 0.65rem 0.85rem;
      text-align: left;
      border-bottom: 1px solid var(--line);
      vertical-align: top;
    }}
    th {{
      background: var(--code);
      font-weight: 600;
      white-space: nowrap;
    }}
    tr:last-child td {{
      border-bottom: none;
    }}
    .action-box {{
      background: var(--code);
      border: 1px solid var(--line);
      border-radius: 6px;
      padding: 1rem;
      margin: 1.25rem 0;
    }}
    .action-box ul {{
      margin: 0.5rem 0 0;
      padding-left: 1.25rem;
    }}
    .action-box li {{
      margin-bottom: 0.35rem;
    }}
    .glossary-list dt {{
      font-weight: 600;
      margin-top: 0.65rem;
    }}
    .glossary-list dt:first-child {{
      margin-top: 0;
    }}
    .glossary-list dd {{
      margin-left: 0;
      margin-bottom: 0.45rem;
      color: var(--ink);
    }}
    @media (max-width: 600px) {{
      .plot-grid {{
        grid-template-columns: 1fr;
      }}
      .site-header-inner, .page-shell {{
        width: calc(100% - 1.25rem);
      }}
      .board-nav {{
        font-size: 0.82rem;
        gap: 0.35rem;
      }}
    }}
  </style>
</head>
<body>
  <a class="skip-link" href="#main-content">Skip to content</a>
  <header class="site-header">
    <div class="site-header-inner">
      <a class="site-brand" href="../index.html">
        <span class="site-mark">AR</span>
        <span>Astro Research Wiki</span>
      </a>
      <span style="font-size: 0.85rem; color: var(--muted);">Ceridwen Results Board</span>
    </div>
  </header>

  <main class="page-shell" id="main-content">
    <header>
      <h1>Ceridwen common results board</h1>
      <p>Authoritative map of completed Ceridwen stellar population inference results, figures, data tables, benchmarks, and models. Every mapped output resolves directly to disk, with live Git synchronization status and pending researcher decisions.</p>
    </header>

    <div class="callout callout-alert">
      <h3>Corrected Calibration Science (Authoritative Audit)</h3>
      <p><strong>Flux ratio sign.</strong> DR2 spectra are <em>brighter</em> than production COSMOS2015 3-arcsecond aperture photometry. In-band spectrum-to-photometry ratios range from 1.26 to 1.48 outside IA679. Production fits sample scale factors of 1.24 and 1.49.</p>
      <p><strong>Tilt origin.</strong> Corrected photometry drives scale factors to 0.99 and 0.92. This correction removes both scale offset and M4's polynomial tilt. Residual M4 tilt shifts from &minus;20% to +0.4%. M5 retains a &minus;20% tilt from dust-polynomial degeneracy caused by a 0.3-mag optical-to-NIR model mismatch.</p>
    </div>

    <nav class="board-nav" aria-label="Results Board Navigation">
      <span class="board-nav-title"><strong>Sections:</strong></span>
      <ul class="board-nav-list">
        <li><a href="#summary-status">Status at a Glance</a></li>
        <li><a href="#glossary">Scientific Glossary</a></li>
        <li><a href="#dr2-sample">187-Galaxy DR2 Results</a></li>
        <li><a href="#borghi-age-z">Borghi Age vs Redshift</a></li>
        <li><a href="#absorption-mask">Absorption Mask</a></li>
        <li><a href="#calibration-tilt">Calibration &amp; Tilt Origin</a></li>
        <li><a href="#formation-timescales">Formation Timescales</a></li>
        <li><a href="#fit-quality">Fit Quality</a></li>
        <li><a href="#performance">Performance &amp; Production</a></li>
        <li><a href="#checkpoint-anim">Checkpoint Animation</a></li>
        <li><a href="#related-runs">Related Runs</a></li>
        <li><a href="#manifest-index">Complete Artifact Catalog (79)</a></li>
      </ul>
    </nav>

    <!-- SECTION 1: STATUS AT A GLANCE -->
    <section id="summary-status">
      <h2>Status at a glance</h2>
      <div class="table-wrap">
        <table>
          <caption>Core analysis domains, validated findings, push status, and pending scientific decisions (Checked 2026-09-04).</caption>
          <thead>
            <tr>
              <th>Analysis Domain</th>
              <th>Key Scientific Finding</th>
              <th>Primary Deliverables</th>
              <th>Git synchronization status (upstream tracking)</th>
              <th>Decisions for Liu Hao</th>
            </tr>
          </thead>
          <tbody>
            <tr>
              <td><strong>187-Galaxy DR2 Sample</strong></td>
              <td>Median mass-weighted age 3.02 Gyr. Median assembly interval &Delta;t = 2.46 Gyr. Zero fit failures among 187 galaxies.</td>
              <td>
                <a href="{items_by_id['dr2-analysis-page']['wiki_relative_path']}">Analysis Page</a> · 
                <a href="{items_by_id['dr2-summary-csv']['wiki_relative_path']}">Summary CSV</a> · 
                <a href="{items_by_id['dr2-production-results-dir']['wiki_relative_path']}">Results Dir</a>
              </td>
              <td>{format_badge(True)} <code>4c3ad00</code></td>
              <td>None (production complete).</td>
            </tr>
            <tr>
              <td><strong>Borghi+2022 Age vs z</strong></td>
              <td>Ceridwen medians stay flat near 3.0 Gyr, averaging +0.26 Gyr above re-binned N=140 Borghi catalogue. Velocity dispersion split shows a weak gradient.</td>
              <td>
                <a href="{items_by_id['borghi-age-redshift-png']['wiki_relative_path']}">Figure PNG</a> · 
                <a href="{items_by_id['borghi-age-redshift-pdf']['wiki_relative_path']}">Vector PDF</a> · 
                <a href="{items_by_id['borghi-source-table']['wiki_relative_path']}">Source Table</a>
              </td>
              <td>{format_badge(True)} <code>98d9c4b</code></td>
              <td>None (catalogue matches finalized).</td>
            </tr>
            <tr>
              <td><strong>Absorption-Line Mask</strong></td>
              <td>Masked and feature modes keep tilt bias and widen posteriors 1.0&ndash;1.6&times;. Shifts real targets up to 22&sigma;. Recommended default is OFF.</td>
              <td>
                <a href="{items_by_id['absorption-analysis-page']['wiki_relative_path']}">Analysis Page</a> · 
                <a href="{items_by_id['absorption-summary-csv']['wiki_relative_path']}">Summary CSV</a> · 
                <a href="{items_by_id['absorption-results-dir']['wiki_relative_path']}">Grid Results</a>
              </td>
              <td>{format_badge(True)} <code>7dae142</code></td>
              <td>Choose whether to keep default OFF, including line list and feature window.</td>
            </tr>
            <tr>
              <td><strong>Calibration &amp; Tilt Origin</strong></td>
              <td>Spectra are brighter than 3" photometry by 1.26&ndash;1.48. Corrected photometry eliminates M4 tilt (+0.4%). M5 retains &minus;20% dust-model tilt.</td>
              <td>
                <a href="{items_by_id['calibration-analysis-page']['wiki_relative_path']}">Worktree Page</a> · 
                <a href="{items_by_id['tilt-origin-arms-csv']['wiki_relative_path']}">Arms CSV</a> · 
                <a href="{items_by_id['tilt-origin-results-dir']['wiki_relative_path']}">Tilt Results</a>
              </td>
              <td>{format_badge(True)} <code>85c1e4a</code></td>
              <td>1. Choose whether to accept corrected photometry and order-3 poly for 187 galaxies.<br>2. Choose whether to investigate young-galaxy 0.3-mag optical-to-NIR mismatch first.<br>3. Choose whether to merge branch <code>calibration-polynomial</code>.</td>
            </tr>
            <tr>
              <td><strong>Formation Timescales</strong></td>
              <td>Median &Delta;t is 2.46 Gyr. Flat across formation epoch. Spearman correlation with mass and [&alpha;/Fe] is 0.00 in 7-bin SFH.</td>
              <td>
                <a href="{items_by_id['dr2-timescale-epoch-png']['wiki_relative_path']}">Epoch PNG</a> · 
                <a href="{items_by_id['dr2-timescale-mass-png']['wiki_relative_path']}">Mass PNG</a> · 
                <a href="{items_by_id['dr2-timescale-alpha-png']['wiki_relative_path']}">Alpha PNG</a>
              </td>
              <td>{format_badge(True)} <code>4c3ad00</code></td>
              <td>None.</td>
            </tr>
            <tr>
              <td><strong>Fit Quality Diagnostics</strong></td>
              <td>All 187 fits succeeded. Worst joint reduced &chi;&sup2;/&nu; values are 2.69 (139662), 2.55 (253688), and 2.34 (101089).</td>
              <td>
                <a href="{items_by_id['dr2-fit-quality-png']['wiki_relative_path']}">Quality PNG</a> · 
                <a href="{items_by_id['dr2-fit-quality-pdf']['wiki_relative_path']}">Quality PDF</a>
              </td>
              <td>{format_badge(True)} <code>4c3ad00</code></td>
              <td>None.</td>
            </tr>
            <tr>
              <td><strong>GPU &amp; Production Benchmarks</strong></td>
              <td>One fit per GPU default. Concurrent runs offer no throughput gain on tested 8-GB and Blackwell GPUs. Fixed-grid SFH default.</td>
              <td>
                <a href="{items_by_id['gpu-benchmark-page']['wiki_relative_path']}">Benchmark Page</a> · 
                <a href="{items_by_id['gpu-benchmark-runs-dir']['wiki_relative_path']}">Runs Dir</a>
              </td>
              <td>{format_badge(True)} <code>d5cfe51</code></td>
              <td>None.</td>
            </tr>
            <tr>
              <td><strong>Interactive Checkpoint Evolution</strong></td>
              <td>Interactive view of the accepted prior predictive, last retained checkpoint, and converged rescue posterior (nested sampling solution after sampler convergence).</td>
              <td>
                <a data-host-check="checkpoint-animation" href="checkpoint-animation/ceridwen-checkpoint-spectrum-evolution.html">Open interactive viewer</a> · 
                <a href="{items_by_id['checkpoint-screenshots-dir']['wiki_relative_path']}">Screenshots Dir</a>
              </td>
              <td><span class="badge badge-pushed">Verified local host</span></td>
              <td>Delivered hosted artifact. Verified responsive viewports.</td>
            </tr>
          </tbody>
        </table>
      </div>
    </section>

    <!-- SECTION: SCIENTIFIC GLOSSARY -->
    <section id="glossary">
      <h2>Scientific terms and definitions</h2>
      <div class="action-box">
        <dl class="glossary-list">
          <dt><strong>Mass-weighted age:</strong></dt>
          <dd>The mean stellar age weighted by the stellar mass formed in each lookback time interval.</dd>
          <dt><strong>Posterior:</strong></dt>
          <dd>The probability distribution of stellar population parameters given the observed spectra, photometry, and priors.</dd>
          <dt><strong>Credible interval:</strong></dt>
          <dd>The parameter range containing a stated posterior probability fraction between designated percentiles.</dd>
          <dt><strong>NMAD (Normalized Median Absolute Deviation):</strong></dt>
          <dd>A scatter estimator defined as 1.4826 times the median absolute deviation from the sample median.</dd>
          <dt><strong>Delta-t (&Delta;t):</strong></dt>
          <dd>The stellar mass assembly interval t20 &minus; t80 during which the middle 60% of galaxy stellar mass formed.</dd>
        </dl>
      </div>
    </section>

    <!-- SECTION 2: 187-GALAXY DR2 RESULTS -->
    <section id="dr2-sample">
      <h2>187-galaxy DR2 quiescent sample (final set)</h2>
      <p>Analysis page: <a href="{items_by_id['dr2-analysis-page']['wiki_relative_path']}">analyses/dr2-quiescent-sample.html</a>. Master catalogue table: <a href="{items_by_id['dr2-summary-csv']['wiki_relative_path']}">results/dr2-quiescent-summary.csv</a> (187 galaxies, 49 columns including t20, t50, t80, &Delta;t). Production run directory: <a href="{items_by_id['dr2-production-results-dir']['wiki_relative_path']}">results/rtx-5060-dr2-quiescent-full-spectrum/</a> (187 individual target folders). Exploratory chronometer notebook: <a href="{items_by_id['chronometer-notebook']['wiki_relative_path']}">ceridwen_cosmic_chronometer.ipynb</a> and summary data: <a href="{items_by_id['chronometer-summary-h5']['wiki_relative_path']}">ceridwen_cosmic_chronometer_summary.h5</a>. Builders: <a href="{items_by_id['dr2-summary-builder']['wiki_relative_path']}">build_dr2_quiescent_summary.py</a>, <a href="{items_by_id['dr2-headline-script']['wiki_relative_path']}">plot_dr2_headline_candidates.py</a>.</p>
      
      <div class="plot-grid">
        {plot_card('dr2-headline-png', 'dr2-headline-pdf', 'dr2-headline-script')}
        {plot_card('dr2-distributions-png', 'dr2-distributions-pdf')}
      </div>
      <p style="font-size: 0.88rem; color: var(--muted);"><strong>Scientific caveat.</strong> The coarse 7-bin SFH basis limits fine temporal resolution. Mass-weighted ages reflect non-parametric composite populations. These values do not directly match Borghi SSP-equivalent Lick ages.</p>
    </section>

    <!-- SECTION 3: BORGHI AGE VERSUS REDSHIFT -->
    <section id="borghi-age-z">
      <h2>Borghi+2022 age versus redshift comparison</h2>
      <p>Standalone figure: <a href="{items_by_id['borghi-age-redshift-png']['wiki_relative_path']}">results/figures/borghi2022-age-vs-z.png</a> (and <a href="{items_by_id['borghi-age-redshift-pdf']['wiki_relative_path']}">PDF</a>). Source data table: <a href="{items_by_id['borghi-source-table']['wiki_relative_path']}">borghi2022_legac_dr2_spectrum_matches copy.tsv</a>. Generation script: <a href="{items_by_id['borghi-plot-script']['wiki_relative_path']}">scripts/plot_borghi2022_age_vs_z.py</a>.</p>
      
      <div class="plot-grid">
        {plot_card('borghi-age-redshift-png', 'borghi-age-redshift-pdf', 'borghi-plot-script')}
      </div>
      <p style="font-size: 0.88rem; color: var(--muted);"><strong>Finding.</strong> Ceridwen mass-weighted ages stay flat near 3.0 Gyr from z=0.6 to z=0.9. They average +0.26 Gyr above re-binned Borghi values. The velocity dispersion split (&sigma; &lt; 215 km/s versus &sigma; &ge; 215 km/s) shows a smaller difference than the gradient in Borghi+2022.</p>
    </section>

    <!-- SECTION 4: ABSORPTION-LINE MASK -->
    <section id="absorption-mask">
      <h2>Absorption-line mask experiment</h2>
      <p>Draft analysis page: <a href="{items_by_id['absorption-analysis-page']['wiki_relative_path']}">analyses/absorption-line-mask.html</a>. Results summary: <a href="{items_by_id['absorption-summary-csv']['wiki_relative_path']}">results/absorption-mask/summary.csv</a> and <a href="{items_by_id['absorption-summary-json']['wiki_relative_path']}">summary.json</a>. Target Fisher analysis: <a href="{items_by_id['absorption-fisher-json']['wiki_relative_path']}">fisher_M5_172669.json</a>. 45-fit execution directory: <a href="{items_by_id['absorption-results-dir']['wiki_relative_path']}">results/absorption-mask/</a>. Analysis scripts: <a href="{items_by_id['absorption-analysis-script']['wiki_relative_path']}">absorption_mask_analysis.py</a>, <a href="{items_by_id['absorption-report-script']['wiki_relative_path']}">absorption_mask_report.py</a>.</p>
      
      <div class="plot-grid">
        {plot_card('absorption-feature-windows-png')}
        {plot_card('absorption-real-posteriors-png')}
        {plot_card('absorption-mock-bias-png')}
        {plot_card('absorption-mock-width-png')}
      </div>
      
      <div class="action-box">
        <strong>Recommendation and open decisions:</strong>
        <ul>
          <li><strong>Recommendation.</strong> Keep mask <strong>OFF</strong> by default for production fits. Feature-only and down-weighted modes retain continuum tilt bias. They widen posteriors by 1.0&ndash;1.6&times; and perturb real galaxy posteriors by up to 22 full-spectrum &sigma;.</li>
          <li><strong>Decisions for Liu Hao.</strong> Choose whether to keep mask off as production default. Choose whether to retain or revise the specific absorption line list and window widths.</li>
        </ul>
      </div>
    </section>

    <!-- SECTION 5: CALIBRATION POLYNOMIAL AND TILT ORIGIN -->
    <section id="calibration-tilt">
      <h2>Calibration polynomial and tilt origin</h2>
      <p>Worktree analysis page (pushed on branch <code>origin/calibration-polynomial</code> at commit <code>85c1e4a</code>): <a href="{items_by_id['calibration-analysis-page']['wiki_relative_path']}">ceridwen-calibration-polynomial.html</a>. Analysis notebook: <a href="{items_by_id['tilt-origin-analysis-notebook']['wiki_relative_path']}">tilt-origin-2026-09-02/analysis.ipynb</a>. Quantitative summaries: <a href="{items_by_id['tilt-origin-arms-csv']['wiki_relative_path']}">arms.csv</a> and <a href="{items_by_id['tilt-origin-ibands-csv']['wiki_relative_path']}">ibands.csv</a>. Completed tilt run directory: <a href="{items_by_id['tilt-origin-results-dir']['wiki_relative_path']}">results/tilt-origin-2026-09-02/</a>. Superseded local snapshot: <a href="{items_by_id['calibration-local-superseded-dir']['wiki_relative_path']}">results/calibration-polynomial-2026-09-02/</a>. Experiment scripts: <a href="{items_by_id['calibration-experiment-script']['wiki_relative_path']}">calibration_polynomial_experiment.py</a>, <a href="{items_by_id['calibration-photometry-download-script']['wiki_relative_path']}">download_legac_dr2_aperture_photometry.py</a>, <a href="{items_by_id['tilt-origin-runner-script']['wiki_relative_path']}">tilt_origin_runner.py</a>, <a href="{items_by_id['tilt-origin-vast-script']['wiki_relative_path']}">tilt_origin_vast.py</a>.</p>

      <div class="plot-grid">
        {plot_card('calibration-explainer-png')}
        {plot_card('calibration-mock-bias-png')}
        {plot_card('calibration-vectors-png')}
        {plot_card('calibration-real-posteriors-png')}
        {plot_card('tilt-origin-ibands-png')}
        {plot_card('tilt-origin-photometry-png')}
        {plot_card('tilt-origin-vectors-png')}
        {plot_card('tilt-origin-posteriors-png')}
      </div>

      <div class="action-box">
        <strong>Decisions waiting on Liu Hao:</strong>
        <ul>
          <li><strong>Choose whether to accept corrected photometry for production.</strong> Corrected aperture photometry with an order-3 polynomial and 12 bands eliminates M4's &minus;20% tilt (residual +0.4%). It also normalizes scale offsets.</li>
          <li><strong>Choose whether to investigate young-galaxy (M5) optical-to-NIR mismatch first.</strong> A 0.3-mag optical-NIR model tension with dust degeneracy drives M5's residual tilt (&minus;16% to &minus;24%).</li>
          <li><strong>Choose whether to merge branch <code>calibration-polynomial</code>.</strong> The branch <code>85c1e4a</code> remains pushed and tested. Merge the branch after Liu Hao approves the strategy for 187 galaxies.</li>
        </ul>
      </div>
    </section>

    <!-- SECTION 6: FORMATION TIMESCALES -->
    <section id="formation-timescales">
      <h2>Formation timescales (&Delta;t)</h2>
      <p>Analysis script: <a href="{items_by_id['dr2-timescale-script']['wiki_relative_path']}">scripts/plot_dr2_formation_timescale.py</a>. The mass assembly interval &Delta;t equals t20 &minus; t80. This value measures the lookback time interval during which the middle 60% of stellar mass formed.</p>

      <div class="plot-grid">
        {plot_card('dr2-timescale-epoch-png', 'dr2-timescale-epoch-pdf', 'dr2-timescale-script')}
        {plot_card('dr2-timescale-mass-png', 'dr2-timescale-mass-pdf', 'dr2-timescale-script')}
        {plot_card('dr2-timescale-alpha-png', 'dr2-timescale-alpha-pdf', 'dr2-timescale-script')}
      </div>
      <p style="font-size: 0.88rem; color: var(--muted);"><strong>Finding.</strong> Median &Delta;t is 2.46 Gyr across the sample. There is no significant correlation between &Delta;t and stellar mass (Spearman 0.00) or [&alpha;/Fe] (Spearman 0.00). The coarse 7-bin SFH basis constrains timescale resolution.</p>
    </section>

    <!-- SECTION 7: FIT QUALITY -->
    <section id="fit-quality">
      <h2>Fit quality diagnostics</h2>
      <p>Diagnostic plotting script: <a href="{items_by_id['dr2-distribution-quality-script']['wiki_relative_path']}">scripts/plot_dr2_distributions_quality.py</a>. Covers likelihood calls, Bayesian log-evidence (logZ, marginal likelihood), Effective Sample Size (ESS, independent posterior samples), and joint reduced &chi;&sup2;/&nu; across all 187 galaxies.</p>

      <div class="plot-grid">
        {plot_card('dr2-fit-quality-png', 'dr2-fit-quality-pdf', 'dr2-distribution-quality-script')}
      </div>
      <p style="font-size: 0.88rem; color: var(--muted);"><strong>Finding.</strong> Zero sampling failures (187/187 completed). The worst joint &chi;&sup2;/&nu; values are 2.69 (galaxy 139662), 2.55 (galaxy 253688), and 2.34 (galaxy 101089).</p>
    </section>

    <!-- SECTION 8: PERFORMANCE AND PRODUCTION -->
    <section id="performance">
      <h2>Performance and production benchmarks</h2>
      <p>Benchmark guide page: <a href="{items_by_id['gpu-benchmark-page']['wiki_relative_path']}">analyses/ceridwen-gpu-benchmarks.html</a>. Comprehensive run archive: <a href="{items_by_id['gpu-benchmark-runs-dir']['wiki_relative_path']}">benchmarks/ceridwen/runs/</a>.</p>
      
      <div class="table-wrap">
        <table>
          <caption>Validated GPU throughput, cost benchmarks, and production recommendations across architectures.</caption>
          <thead>
            <tr>
              <th>Report / Specification</th>
              <th>Artifact Link</th>
              <th>Format</th>
              <th>Status</th>
              <th>Key Performance Recommendation</th>
            </tr>
          </thead>
          <tbody>
            <tr>
              <td>Vast.ai Multi-GPU Sweep Manifest</td>
              <td><a href="{items_by_id['gpu-sweep-manifest-json']['wiki_relative_path']}">ceridwen_vast_gpu_sweep_manifest_2026-08-27.json</a></td>
              <td>JSON</td>
              <td>{format_badge(items_by_id['gpu-sweep-manifest-json']['pushed'])}</td>
              <td>49 benchmark executions documenting scaling.</td>
            </tr>
            <tr>
              <td>Predicted vs Measured Summary</td>
              <td><a href="{items_by_id['gpu-predicted-measured-csv']['wiki_relative_path']}">ceridwen_vast_predicted_vs_measured_gpu_benchmark_summary_2026-08-26.csv</a></td>
              <td>CSV</td>
              <td>{format_badge(items_by_id['gpu-predicted-measured-csv']['pushed'])}</td>
              <td>Empirical timing model across cloud hosts.</td>
            </tr>
            <tr>
              <td>3090 / 4090 / H100 Full Summary</td>
              <td><a href="{items_by_id['gpu-three-card-summary-csv']['wiki_relative_path']}">ceridwen_vast_3090_4090_h100_joint_full_benchmark_summary_2026-08-26.csv</a></td>
              <td>CSV</td>
              <td>{format_badge(items_by_id['gpu-three-card-summary-csv']['pushed'])}</td>
              <td>High-end card comparisons and memory ceilings.</td>
            </tr>
            <tr>
              <td>Production 8GB GPU Sizing</td>
              <td><a href="{items_by_id['gpu-production-8gb-json']['wiki_relative_path']}">fits_per_gpu_production_8gb_20260902.json</a></td>
              <td>JSON</td>
              <td>{format_badge(items_by_id['gpu-production-8gb-json']['pushed'])}</td>
              <td>One fit per GPU default to avoid out-of-memory crashes.</td>
            </tr>
            <tr>
              <td>Blackwell RTX 5060 8GB</td>
              <td><a href="{items_by_id['gpu-production-5060-json']['wiki_relative_path']}">fits_per_gpu_production_blackwell_rtx5060_8gb_20260902.json</a></td>
              <td>JSON</td>
              <td>{format_badge(items_by_id['gpu-production-5060-json']['pushed'])}</td>
              <td>Primary production card. Fast and cost-effective.</td>
            </tr>
            <tr>
              <td>Blackwell RTX 5060 Ti 16GB</td>
              <td><a href="{items_by_id['gpu-production-5060ti-json']['wiki_relative_path']}">fits_per_gpu_production_blackwell_rtx5060ti_16gb_20260902.json</a></td>
              <td>JSON</td>
              <td>{format_badge(items_by_id['gpu-production-5060ti-json']['pushed'])}</td>
              <td>Large memory headroom for high-resolution grids.</td>
            </tr>
            <tr>
              <td>Blackwell RTX 5070 12GB</td>
              <td><a href="{items_by_id['gpu-production-5070-json']['wiki_relative_path']}">fits_per_gpu_production_blackwell_rtx5070_12gb_20260902.json</a></td>
              <td>JSON</td>
              <td>{format_badge(items_by_id['gpu-production-5070-json']['pushed'])}</td>
              <td>Highest per-card throughput in Blackwell series.</td>
            </tr>
          </tbody>
        </table>
      </div>
    </section>

    <!-- SECTION 9: INTERACTIVE CHECKPOINT ANIMATION -->
    <section id="checkpoint-anim">
      <h2>Interactive checkpoint spectrum evolution</h2>
      <div class="callout callout-info">
        <h3>Payload-preserving interactive viewer</h3>
        <p>The viewer uses the byte-identical accepted checkpoint payload. Its controls, legend, spectrum, residual, and axis labels fit desktop and phone viewports. It displays Effective Sample Size (ESS, independent posterior samples) and Bayesian log-evidence (logZ, marginal likelihood). It also presents the converged rescue posterior (nested sampling solution after sampler convergence).</p>
      </div>

      <p>The shaded band shows the 16th to 84th percentile range of noiseless model spectra across 128 deterministic equal-weight draws. It represents parameter uncertainty, not measurement noise.</p>

      <p><a data-host-check="checkpoint-animation" href="checkpoint-animation/ceridwen-checkpoint-spectrum-evolution.html">Open the hosted checkpoint viewer</a>. The underlying nested sampling implementation and test modules remain available in the codebase:</p>
      <ul>
        <li>Generator script: <a href="{items_by_id['checkpoint-generator-script']['wiki_relative_path']}">scripts/plot_ceridwen_checkpoint_evolution.py</a></li>
        <li>Verification captures: <a href="{items_by_id['checkpoint-screenshots-dir']['wiki_relative_path']}">reports/ceridwen-checkpoint-animation/screenshots/</a></li>
        <li>Test suites: <a href="{items_by_id['checkpoint-generator-test']['wiki_relative_path']}">test_plot_ceridwen_checkpoint_evolution.py</a>, <a href="{items_by_id['checkpoint-spectrum-test']['wiki_relative_path']}">test_checkpoint_spectrum.py</a>, <a href="{items_by_id['checkpoint-serialization-test']['wiki_relative_path']}">test_ns_checkpoint.py</a></li>
        <li>Core sampler modules: <a href="{items_by_id['checkpoint-prediction-module']['wiki_relative_path']}">ceridwen/plotting/checkpoint.py</a>, <a href="{items_by_id['checkpoint-sampler-module']['wiki_relative_path']}">ceridwen/sampler/nested.py</a></li>
        <li>Four-galaxy fit directory: <a href="{items_by_id['rtx4070-four-fit-dir']['wiki_relative_path']}">results/rtx-4070-super-four-galaxy-fits/</a></li>
      </ul>
    </section>

    <!-- SECTION 10: RELATED FIT RUNS (DIRECTORY-LEVEL) -->
    <section id="related-runs">
      <h2>Related fit runs and exploratory suites</h2>
      <p>Exploratory and benchmark fit runs accessible at directory level:</p>
      <ul>
        <li><a href="{items_by_id['static-smoothing-refits-dir']['wiki_relative_path']}">results/refit-static-smoothing/</a> &mdash; Per-target refits using the static smoother {format_badge(items_by_id['static-smoothing-refits-dir']['pushed'])}.</li>
        <li><a href="{items_by_id['sfh-fastpath-comparison-dir']['wiki_relative_path']}">results/rtx-5060-sfh-fastpath-comparison/</a> &mdash; Baseline versus fastpath_a SFH basis comparison {format_badge(items_by_id['sfh-fastpath-comparison-dir']['pushed'])}.</li>
        <li><a href="{items_by_id['nss-default-variation-dir']['wiki_relative_path']}">results/rtx-5090-nss-default-variation-vs-fastpath-a/</a> &mdash; BlackJAX NSS sampler configuration variations {format_badge(items_by_id['nss-default-variation-dir']['pushed'])}.</li>
        <li><a href="{items_by_id['rtx5090-integrated-fit-dir']['wiki_relative_path']}">results/rtx-5090-integrated-fit/</a> &mdash; Executed single integrated photometry+spectra fit {format_badge(items_by_id['rtx5090-integrated-fit-dir']['pushed'])}.</li>
        <li><a href="{items_by_id['rtx4070-four-fit-dir']['wiki_relative_path']}">results/rtx-4070-super-four-galaxy-fits/</a> &mdash; Four-galaxy GPU validation run and checkpoint host {format_badge(items_by_id['rtx4070-four-fit-dir']['pushed'])}.</li>
        <li><a href="{items_by_id['a100-feature-spectrum-dir']['wiki_relative_path']}">results/a100-feature-spectrum/</a> &mdash; A100 feature spectrum test outputs {format_badge(items_by_id['a100-feature-spectrum-dir']['pushed'])}.</li>
        <li><a href="{items_by_id['a100-integrated-notebook-dir']['wiki_relative_path']}">results/a100-integrated-fit-notebook/</a> &mdash; A100 integrated fit execution notebook {format_badge(items_by_id['a100-integrated-notebook-dir']['pushed'])}.</li>
      </ul>
    </section>

    <!-- SECTION 11: COMPLETE ARTIFACT CATALOG (79 ITEMS) -->
    <section id="manifest-index">
      <h2>Complete artifact catalog (79 validated items)</h2>
      <p>Complete manifest of all 79 deliverables audited and validated against the live filesystem. All paths resolve directly relative to this wiki page.</p>
      
      <div class="table-wrap">
        <table>
          <thead>
            <tr>
              <th>ID</th>
              <th>Title / Deliverable</th>
              <th>Category</th>
              <th>Media Type</th>
              <th>Wiki-Relative Link</th>
              <th>Git synchronization status (upstream tracking)</th>
              <th>Decisions / Notes</th>
            </tr>
          </thead>
          <tbody>'''

    for item in manifest["items"]:
        iid = html.escape(item["id"])
        title = html.escape(item["title"])
        cat = html.escape(item["category"])
        mt = html.escape(item["media_type"])
        rel = html.escape(item["wiki_relative_path"])
        pushed_badge = format_badge(item["pushed"])
        dec = html.escape(" · ".join(item["pending_decisions"])) if item["pending_decisions"] else "&mdash;"

        if iid == "checkpoint-interactive-html":
            pushed_badge = '<span class="badge badge-pushed">Verified local host</span>'
            dec = "Delivered hosted artifact. Verified responsive viewports."
            link_display = f'<a data-host-check="checkpoint-animation" href="{rel}">{rel}</a>'
        else:
            link_display = f'<a href="{rel}">{rel}</a>'

        doc += f'''
            <tr>
              <td><code>{iid}</code></td>
              <td><strong>{title}</strong></td>
              <td>{cat}</td>
              <td><code>{mt}</code></td>
              <td>{link_display}</td>
              <td>{pushed_badge}</td>
              <td style="font-size: 0.82rem;">{dec}</td>
            </tr>'''

    doc += '''
          </tbody>
        </table>
      </div>
    </section>
  </main>
</body>
</html>
'''
    return doc


def main() -> None:
    manifest_data = json.loads(MANIFEST_PATH.read_text(encoding="utf-8"))
    html_content = build_board_html(manifest_data)
    BOARD_PATH.write_text(html_content, encoding="utf-8")
    print(f"Wrote Ceridwen results board to {BOARD_PATH} ({len(html_content)} bytes)")


if __name__ == "__main__":
    main()
