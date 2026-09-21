"""Fit settings and priors of one notebook cell, grouped and colour coded.

`render` reads the `SETTINGS` and `PRIORS` dict literals of the cell at build time. Values
and `#` comments come from the cell. Group labels, colours, symbols and value templates
come from the tables below. A key in no group renders last, unlabelled, under its raw key.
Bounds that exist only at run time come from the stdout of an executed copy, `run`.
"""
import ast
import html
import io
import json
import re
import tokenize

esc = html.escape
C_KMS = 299792.458
GROUPS = [  # label, colour token, keys in display order
    ("Data and masks", "--g-data", ["photometry", "emission_lines", "telluric_air"]),
    ("Stellar population", "--g-stars", ["logmass", "Z", "afe"]),
    ("SFH", "--g-sfh", ["logsfr_ratios", "sfh_lookback_gyr"]),
    ("Dust", "--g-dust", ["diffuse_tau_kc", "diffuse_dust_index"]),
    ("Redshift and kinematics", "--g-kin", ["zred", "sigma_smooth"]),
    ("Calibration", "--g-calib", ["calibration_order", "calibration_prior_sigma", "spectrum_scaling"]),
    ("Noise floors", "--g-noise", ["photometry_floor", "log_f_calib"]),
    ("Sampler", "--ink-2", ["sampler"]),
]
# The law Ceridwen evaluates: sedpy_jax/attenuation_dust.py `kriek_conroy(wave, tau_kc, dust_index)`,
# chosen by `diffuse_law='kriek_conroy'` in ceridwen/csp/csp_afe.py; theta keys diffuse_tau_kc, diffuse_dust_index.
EQUATIONS = {"Dust": {
    "equation": r"\tau(\lambda) = \frac{\tau_{\mathrm{dust}}}{4.05}\,\bigl[k'(\lambda) + D(\lambda)\bigr]"
                r"\left(\frac{\lambda}{5500\,\text{\AA}}\right)^{\delta_{\mathrm{dust}}}",
    "notes": [r"\(k'\): Calzetti+2000 curve",
              r"\(D\): Drude bump, 2175 \(\text{\AA}\), width 350 \(\text{\AA}\), "
              r"\(E_b = 0.85 - 1.9\,\delta_{\mathrm{dust}}\)"],
    "cite": ("Kriek & Conroy 2013", "https://arxiv.org/abs/1308.1099"),
}}
SYMBOLS = {
    "logmass": r"\log_{10}(M_\star/M_\odot)",
    "logsfr_ratios": r"\log_{10}(\mathrm{SFR}_n/\mathrm{SFR}_{n+1})",
    "Z": r"[\mathrm{Fe}/\mathrm{H}]",
    "afe": r"[\alpha/\mathrm{Fe}]",
    "diffuse_tau_kc": r"\tau_{\mathrm{dust}}",
    "diffuse_dust_index": r"\delta_{\mathrm{dust}}",
    "log_f_calib": r"\log f_{\mathrm{calib}}",
    "zred": r"z",
    "sigma_smooth": r"\sigma_\star",
}
HIDDEN = {"sampler_quick", "baked_runtime"}
PAIRED = {"Noise floors"}  # groups whose rows sit side by side
NAMES = {"photometry_floor": "Photometry", "log_f_calib": "Spectrum"}  # row names of templated rows
# Value templates, which replace the value and the comment. A slot is `key`, `key:pct` (the number
# times 100) or `key.Class.kwarg:lnpct` (the argument of np.log in that keyword, times 100), read from
# the live cell. Another key's slot folds that key's row into this one. An unfillable slot: generic row.
TEMPLATES = {
    "photometry_floor": "fixed %(photometry_floor:pct)s%%, added in quadrature to each band",
    "log_f_calib": r"\(f_{\mathrm{calib}}\), sampled, prior %(log_f_calib.Uniform.low:lnpct)s–"
                   r"%(log_f_calib.Uniform.high:lnpct)s%% log-uniform, added in quadrature to each pixel",
    "zred": r"Uniform, \(z_{\mathrm{cat}}\) ± %(zred_half_width)s",
    "sigma_smooth": r"Normal, \(\sigma_{\mathrm{DR2}}\) ± err, clipped at %(sigma_clip)s err",
    "calibration_prior_sigma": "Normal, 0 ± %(calibration_prior_sigma)s",
}
# Row equations of templated rows, with the same slots. Photometry: the fit notebook's
# `phot_uncertainty = np.hypot(phot_error_stat * total_scale, SETTINGS["photometry_floor"] * np.abs(phot_flux))`.
# Spectrum: `DiagonalNoiseModel(use_fractional=True)`, ceridwen/likelihood/noise_model.py,
# variance = sigma_obs^2 + [exp(log_f_calib) |mu|]^2 with mu the model prediction.
ROW_EQUATIONS = {
    "photometry_floor": (r"\sigma_{\mathrm{tot}} = \sqrt{\sigma_{\mathrm{phot}}^2 + (%(photometry_floor)s\,F_{\mathrm{obs}})^2}",
                         r"\(F_{\mathrm{obs}}\): observed band flux"),
    "log_f_calib": (r"\sigma_{\mathrm{tot}} = \sqrt{\sigma_{\mathrm{pix}}^2 + (f_{\mathrm{calib}}\,F_{\mathrm{model}})^2}",
                    r"\(F_{\mathrm{model}}\): model flux in that pixel"),
}
DISTRIBUTIONS = {  # class name -> display; slots are the call's keyword arguments
    "Uniform": "Uniform [%(low)s, %(high)s]",
    "StudentT": r"Student-t \(\mu\) %(mean)s, scale %(scale)s, \(\nu\) %(df)s",
    "ClippedNormal": "Clipped normal %(mean)s ± %(sigma)s on [%(low)s, %(high)s]",
}
FUNCTIONS = {"np.log": r"\(\ln\) %s"}
AXES = {"Z": "[Fe/H]"}  # key shown in the units of this `grid axes` entry of the run's stdout
LINES_KEY = "emission_lines"  # rest wavelengths masked within the `dv` km/s of the notebook's `mask_lines` call
LINES = {3726.0: "[O II]", 3728.8: "[O II]", 4861.3: r"H\(\beta\)", 4958.9: "[O III]", 5006.8: "[O III]"}
LINES_NOTE = r"masked ±%d to ±%d \(\text{\AA}\)"
SLOT = re.compile(r"%\(((\w+)[\w.:]*)\)s")
DV = re.compile(r"mask_lines\(.*?\bdv=([0-9.]+)", re.S)
PRIOR_LINE = re.compile(r"^\s+(\w+): .*?prior Uniform\(([^,()]+), ([^()]+)\)", re.M)


def parse(text):
    """{key: (dict name, value node, comment)} for every entry of the two dict literals."""
    comments = {token.start[0]: token.string.lstrip("#").strip()
                for token in tokenize.generate_tokens(io.StringIO(text).readline)
                if token.type == tokenize.COMMENT}
    entries = {}
    for node in ast.parse(text).body:
        if isinstance(node, ast.Assign) and getattr(node.targets[0], "id", "") in ("SETTINGS", "PRIORS"):
            for key, value in zip(node.value.keys, node.value.values):
                lines = range(key.lineno, value.end_lineno + 1)
                entries[key.value] = (node.targets[0].id, value,
                                      next((comments[n] for n in lines if n in comments), ""))
    return entries


def number(text):
    if "." in text and "e" not in text:
        text = text.rstrip("0").rstrip(".")
    return "−" + text[1:] if text.startswith("-") else text


def run_ranges(stdout):
    """{key: (low, high)} of the Uniform priors an executed fit printed; `AXES` keys in grid-axis units."""
    block = stdout.partition("Free parameters and priors\n")[2]
    ranges = {key: (low, high) for key, low, high in PRIOR_LINE.findall(block)}
    for key, axis in AXES.items():
        bounds = re.search(r"grid axes:.*?%s[^\[\n]*\[([^,\]]+), ([^\]]+)\]" % re.escape(axis), stdout)
        if key in ranges and bounds:
            ranges[key] = bounds.groups()
        else:
            ranges.pop(key, None)
    return ranges


def lines_html(node, dv):
    """Masked line names, doublets as `3726/3729`, and the mask half-width range in rest ångströms."""
    waves = [element.value for element in node.elts]
    names = []
    for wave in waves:
        name = LINES.get(wave, number(str(wave)))
        if list(LINES.values()).count(name) > 1:
            if names and names[-1].startswith(name + " "):
                names[-1] += "/%d" % round(wave)
                continue
            name += " %d" % round(wave)
        names.append(name)
    widths = [round(wave * dv / C_KMS) for wave in (min(waves), max(waves))]
    return ", ".join(name.replace(" ", "\u00a0") for name in names), LINES_NOTE % tuple(widths)


def value_html(node, text, prior=False):
    if isinstance(node, ast.Constant) and isinstance(node.value, str):
        return esc(node.value) if prior and "(" not in node.value else "<code>%s</code>" % esc(node.value)
    if isinstance(node, (ast.List, ast.Tuple)):
        return ", ".join(value_html(e, text) for e in node.elts)
    if isinstance(node, ast.Dict):
        return ", ".join("<code>%s</code> %s" % (esc(k.value), value_html(v, text))
                         for k, v in zip(node.keys, node.values))
    if isinstance(node, ast.Call):
        name = ast.unparse(node.func)
        if name in FUNCTIONS:
            return FUNCTIONS[name] % value_html(node.args[0], text)
        kwargs = {k.arg: value_html(k.value, text) for k in node.keywords}
        if name in DISTRIBUTIONS:
            return DISTRIBUTIONS[name] % kwargs
        return "%s %s" % (esc(name), ", ".join("%s %s" % pair for pair in kwargs.items()))
    return esc(number(ast.get_source_segment(text, node)))


def slot_html(slot, entries, text):
    path, _, unit = slot.partition(":")
    key, *call = path.split(".")
    node = entries[key][1]
    if call:
        if ast.unparse(node.func) != call[0]:
            raise KeyError(slot)
        node = {k.arg: k.value for k in node.keywords}[call[1]]
    if unit == "lnpct":
        if ast.unparse(node.func) != "np.log":
            raise KeyError(slot)
        node = node.args[0]
    return number("%g" % (node.value * 100)) if unit else value_html(node, text)


def row_html(key, entries, text, dv, ranges):
    source, node, note = entries[key]
    note = '<dd class="fs-note no-math">%s</dd>' % esc(note) if note else ""
    name = r"\(%s\)" % SYMBOLS[key] if key in SYMBOLS else "<code>%s</code>" % esc(key)
    def filled(template):
        return template % {slot: slot_html(slot, entries, text) for slot, _ in SLOT.findall(template)}
    try:
        value = filled(TEMPLATES[key])
        name, note = esc(NAMES.get(key, "")) or name, ""
        if key in ROW_EQUATIONS:
            note = '<dd class="fs-math">\\[%s\\]</dd><dd class="fs-note">%s</dd>' % (
                esc(filled(ROW_EQUATIONS[key][0]), quote=False), ROW_EQUATIONS[key][1])
    except (KeyError, AttributeError, TypeError):
        value = ""
    if value:
        pass
    elif key == LINES_KEY and dv:
        value, width = lines_html(node, dv)
        note = '<dd class="fs-note">%s</dd>' % width
    elif key in ranges and isinstance(node, ast.Constant):
        value = DISTRIBUTIONS["Uniform"] % dict(zip(("low", "high"), map(number, ranges[key])))
        if key in AXES:  # the comment describes the raw variable, not the units shown
            note = ""
    else:
        value = value_html(node, text, prior=source == "PRIORS")
    return '<div class="fs-row%s"><dt>%s</dt><dd class="fs-val">%s</dd>%s</div>' % (
        "" if note else " fs-wide", name, value, note)


def equation_html(label):
    if label not in EQUATIONS:
        return ""
    law = EQUATIONS[label]
    return '<div class="fs-eq"><div>\\[%s\\]</div><a href="%s">%s</a></div><p class="fs-eq-note">%s</p>' % (
        esc(law["equation"], quote=False), esc(law["cite"][1]), esc(law["cite"][0]), "<br>".join(law["notes"]))


def component(text, code="", stdout=""):
    """The component for one cell's source, the notebook's other code and a run's stdout."""
    entries = parse(text)
    dv = DV.search(code)
    dv, ranges = float(dv[1]) if dv else 0, run_ranges(stdout)
    folded = {slot for key, template in TEMPLATES.items() if key in entries
              for _, slot in SLOT.findall(template) if slot != key}
    grouped = {key for _, _, keys in GROUPS for key in keys}
    rest = [key for key in entries if key not in grouped | folded | HIDDEN]
    groups = ""
    for label, token, keys in [*GROUPS, ("", "--ink-3", rest)]:
        rows = "".join(row_html(key, entries, text, dv, ranges) for key in keys if key in entries)
        if rows:
            groups += '<section class="fs-group%s" style="--g:var(%s)">%s%s<dl>%s</dl></section>' % (
                " fs-pair" if label in PAIRED else "", token, '<h3 class="fs-label">%s</h3>' % esc(label) if label else "", equation_html(label), rows)
    return '<div class="fitset"><div class="fs-body">%s</div></div>' % groups


def render(project, notebook, cell, run=None):
    def cells(path):
        return json.loads((project / path).read_text(encoding="utf-8"))["cells"]
    code = ["".join(c["source"]) for c in cells(notebook) if c["cell_type"] == "code"]
    stdout = "".join("".join(output["text"]) for c in cells(run) for output in c.get("outputs", [])
                     if output.get("name") == "stdout") if run else ""
    return component("".join(cells(notebook)[cell]["source"]), "\n".join(code), stdout)


CSS = """
:root{--g-data:#346841;--g-stars:#844642;--g-sfh:#2d5f87;--g-dust:#745519;--g-kin:#694d7e;--g-calib:#00696a;--g-noise:#7e4661}
@media (prefers-color-scheme: dark){:root:not([data-theme="light"]){--g-data:#8dc096;--g-stars:#e09e97;--g-sfh:#86b7e1;--g-dust:#ccac76;--g-kin:#c1a3d8;--g-calib:#70c1c1;--g-noise:#d99cb8}}
:root[data-theme="dark"]{--g-data:#8dc096;--g-stars:#e09e97;--g-sfh:#86b7e1;--g-dust:#ccac76;--g-kin:#c1a3d8;--g-calib:#70c1c1;--g-noise:#d99cb8}
.fitset{container-type:inline-size;width:100%;min-width:0;max-width:none}
.fitset dl,.fitset dt,.fitset dd{margin:0;padding:0;max-width:none}
.fitset .fs-body{columns:2;column-gap:44px}
.fitset .fs-group{break-inside:avoid;padding-bottom:20px}
.fitset .fs-label{margin:0;padding:0 0 4px;border-bottom:2px solid var(--g);font:600 .8rem/1.3 system-ui,sans-serif;letter-spacing:0;color:var(--g)}
.fitset .fs-group:not(:has(.fs-label)) dl{border-top:2px solid var(--g)}
.fitset .fs-row{display:grid;grid-template-columns:172px minmax(0,1fr);column-gap:14px;align-items:baseline;padding:6px 0;font-size:.9rem;line-height:1.4;font-variant-numeric:tabular-nums lining-nums}
.fitset dt{grid-row:1 / span 2;min-width:0;overflow-wrap:anywhere;font-family:inherit;font-size:inherit;color:var(--ink);letter-spacing:0;text-transform:none}
.fitset dt code{font-size:.76rem}
.fitset .fs-val{min-width:0;overflow-wrap:anywhere}
.fitset .fs-val code{font-size:.74rem}
.fitset code{background:none;padding:0;color:var(--ink)}
.fitset .fs-pair{column-span:all}
.fitset .fs-pair dl{display:grid;grid-template-columns:repeat(2,minmax(0,1fr));column-gap:44px}
.fitset .fs-pair .fs-row{grid-row:span 4;grid-template-rows:subgrid;grid-template-columns:minmax(0,1fr)}
.fitset .fs-pair dt{grid-row:auto;font-weight:500}
.fitset .fs-pair dd{grid-column:1}
.fitset .fs-math{min-width:0;overflow-x:auto;overflow-y:hidden;padding:6px 0 2px}
.fitset .fs-math .katex-display{margin:0;padding:0}
.fitset .fs-math .katex-display,.fitset .fs-math .katex-display>.katex{text-align:left}
.fitset .fs-eq{display:flex;flex-wrap:wrap;justify-content:space-between;align-items:center;gap:0 16px;padding-top:8px;font-size:.9rem}
.fitset .fs-eq>div{min-width:0;max-width:100%;overflow-x:auto;overflow-y:hidden}
.fitset .fs-eq .katex-display{margin:0;padding:2px 0}
.fitset .fs-eq a,.fitset .fs-eq-note{font-size:.8rem;line-height:1.35}
.fitset .fs-eq-note{margin:4px 0 2px;max-width:none;color:var(--ink-2)}
.fitset .fs-note{grid-column:2;min-width:0;font-size:.8rem;line-height:1.35;color:var(--ink-2);text-wrap:balance}
@container (max-width:860px){
  .fitset .fs-body{columns:1}
  .fitset .fs-row{grid-template-columns:190px 290px minmax(0,1fr)}
  .fitset dt{grid-row:auto}
  .fitset .fs-note{grid-column:3}
  .fitset .fs-wide .fs-val{grid-column:2 / -1}
}
@container (max-width:640px){
  .fitset .fs-pair dl{grid-template-columns:minmax(0,1fr)}
  .fitset .fs-pair .fs-row+.fs-row{padding-top:10px}
  .fitset .fs-row{grid-template-columns:172px minmax(0,1fr)}
  .fitset dt{grid-row:1 / span 2}
  .fitset .fs-note,.fitset .fs-wide .fs-val{grid-column:2}
}
@container (max-width:420px){
  .fitset .fs-row{grid-template-columns:minmax(0,1fr)}
  .fitset dt{grid-row:auto}
  .fitset .fs-note,.fitset .fs-wide .fs-val{grid-column:1}
}
"""
