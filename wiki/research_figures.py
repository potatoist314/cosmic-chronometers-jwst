"""Render saved research figures without executing or modifying their sources.

A notebook's PNG outputs are extracted once per notebook version into
`wiki/public.cache/<notebook>/<size>-<mtime>/c<cell>-o<output>.png` and linked
into each build from there, so a build reads no notebook it has already seen.
"""

import base64
import binascii
import html
import json
import os
import shutil
from pathlib import Path
from urllib.parse import quote

VIEWS = ("Fits", "SFH", "Posteriors", "Comparison")
CACHE = "wiki/public.cache"
PNG = b"\x89PNG\r\n\x1a\n"
esc = html.escape


def store(project):
    return project / CACHE


def extracted(project, relative):
    """The directory holding every PNG output of one notebook, extracted on first use."""
    source = os.path.join(project, relative)
    status = os.stat(source)
    version = os.path.join(project, CACHE, os.path.splitext(relative)[0],
                           "%d-%d" % (status.st_size, status.st_mtime_ns))
    if os.path.isdir(version):
        return version
    version = Path(version)
    home = version.parent
    staging = home / (version.name + ".tmp-%d" % os.getpid())
    shutil.rmtree(staging, ignore_errors=True)
    staging.mkdir(parents=True)
    cells = json.loads(Path(source).read_text(encoding="utf-8"))["cells"]
    for cell_index, cell in enumerate(cells):
        for output_index, output in enumerate(cell.get("outputs", [])):
            encoded = output.get("data", {}).get("image/png") if isinstance(output, dict) else None
            if encoded is None:
                continue
            encoded = "".join(encoded) if isinstance(encoded, list) else encoded
            try:
                data = base64.b64decode(encoded, validate=False)
            except (TypeError, binascii.Error):
                continue
            if data.startswith(PNG):
                (staging / ("c%d-o%d.png" % (cell_index, output_index))).write_bytes(data)
    try:
        staging.rename(version)
    except OSError:                              # another process extracted it first
        shutil.rmtree(staging, ignore_errors=True)
    for stale in home.iterdir():
        if stale != version and not stale.name.endswith(".tmp-%d" % os.getpid()):
            shutil.rmtree(stale, ignore_errors=True)
    return str(version)


def image_path(project, figure):
    try:
        path = os.path.join(extracted(project, figure["notebook"]), "c%d-o%d.png" % (figure["cell"], figure["output"]))
    except (KeyError, TypeError, ValueError, OSError) as exc:
        raise ValueError("missing or invalid saved PNG output") from exc
    if not os.path.isfile(path):
        raise ValueError("missing or invalid saved PNG output")
    return path


def image_bytes(project, figure):
    with open(image_path(project, figure), "rb") as saved:
        return saved.read()


def validate(records, project, asset_url):
    faults = []
    for record in records:
        if record["kind"] != "experiment":
            continue
        sections = record["sections"]
        figures = sections["Figures"]
        runs = {r["id"]: r for r in sections["Runs"]}
        prefix = str(record["path"]) + ": "
        if record["status"] in {"recorded", "results-ready", "reviewed"} and not figures and not sections["Measurements"]:
            faults.append(prefix + "result page needs figures or a measured benchmark table")
        if sections["Measurements"] and not sections["Measurements"].lstrip().startswith("|"):
            faults.append(prefix + "Measurements must start with a table")
        for index, figure in enumerate(figures):
            try:
                if not isinstance(figure.get("caption"), str) or not figure["caption"].strip():
                    raise ValueError("caption is required")
                if figure.get("view") not in VIEWS:
                    raise ValueError("unknown figure view")
                for key in ("target", "arm"):
                    if key in figure and not isinstance(figure[key], str):
                        raise ValueError(key + " must be text")
                if bool(figure.get("path")) == bool(figure.get("notebook")):
                    raise ValueError("use one image path or one notebook output")
                if figure.get("path"):
                    asset_url(figure["path"], "", project)
                    if Path(figure["path"]).suffix.lower() not in {".png", ".jpg", ".jpeg", ".svg", ".webp"}:
                        raise ValueError("path must identify an image")
                if figure.get("notebook"):
                    asset_url(figure["notebook"], "", project)
                    if Path(figure["notebook"]).suffix != ".ipynb":
                        raise ValueError("notebook must be an ipynb file")
                    if any(type(figure.get(k)) is not int or figure[k] < 0 for k in ("cell", "output")):
                        raise ValueError("cell and output must be nonnegative integers")
                    run = runs.get(figure.get("run"), {})
                    if not run or figure["notebook"] not in [a.get("path") for a in run.get("artifacts", [])]:
                        raise ValueError("notebook must belong to the identified run")
                    if figure.get("target") != run.get("target") or figure.get("arm") != run.get("arm"):
                        raise ValueError("figure target and arm must match its run")
                    image_path(project, figure)
            except (ValueError, OSError) as exc:
                faults.append(prefix + "figure %d: %s" % (index, exc))
    return faults


def image_url(figure, project, scratch, base, asset_url):
    if figure.get("path"):
        return asset_url(figure["path"], base, project)
    relative = Path("research-images") / Path(figure["notebook"]).with_suffix("") / (
        "c%d-o%d.png" % (figure["cell"], figure["output"]))
    output = scratch / relative
    if not output.exists():
        output.parent.mkdir(parents=True, exist_ok=True)
        source = image_path(project, figure)
        try:
            os.link(source, output)
        except OSError:
            shutil.copyfile(source, output)
    return base + "/" + quote(relative.as_posix())


def render(record, project, scratch, base, asset_url, markdown, plain_text):
    figures = record["sections"]["Figures"]
    targets = sorted({f["target"] for f in figures if f.get("target")})
    views = [v for v in VIEWS if any(f["view"] == v for f in figures)]
    target = targets[0] if targets else ""
    view = views[0] if views else ""
    controls = []
    for name, values in (("Target", targets), ("View", views)):
        if len(values) > 1:
            controls.append('<label>%s<select id="figure-%s">%s</select></label>' % (
                name, name.lower(), "".join('<option value="%s">%s</option>' % (esc(v), esc(v)) for v in values)))
    body = '<div class="figure-controls">%s</div>' % "".join(controls) if controls else ""
    body += '<div class="figure-gallery" data-target="%s" data-view="%s">' % (esc(target), esc(view))
    for index, f in enumerate(figures):
        src = image_url(f, project, scratch, base, asset_url)
        visible = (not f.get("target") or f["target"] == target) and f["view"] == view
        body += ('<figure class="result-figure" data-target="%s" data-view="%s"%s>'
                 '<a href="%s"><img %s="%s" alt="%s" loading="lazy"></a>'
                 '<figcaption>%s</figcaption><button type="button" data-annotate-figure="%s:%s">Annotate figure</button></figure>') % (
                    esc(f.get("target", "")), esc(f["view"]), "" if visible else " hidden",
                    esc(src), "src" if visible else "data-src", esc(src), esc(plain_text(f["caption"])), esc(f["caption"]), esc(record["id"]), index)
    body += '</div><p id="figure-empty" class="empty" hidden>No figure for this target and view.</p>'
    if record["sections"]["Measurements"]:
        body += '<div class="measurements">%s</div>' % markdown(record["sections"]["Measurements"])
    body += '<dialog class="figure-attach"><form method="dialog"><h2>Attach annotation</h2><label>Research item<select data-attach-target></select></label><button value="cancel">Cancel</button><button type="button" data-attach-go>Write notes</button></form></dialog>'
    body += '<script type="module" src="%s/activity.js"></script>' % base
    body += '<script src="%s/figures.js" defer></script>' % base
    return body


JS = """(() => {
  const gallery = document.querySelector('.figure-gallery');
  if (!gallery) return;
  const target = document.getElementById('figure-target');
  const view = document.getElementById('figure-view');
  const figures = [...gallery.querySelectorAll('.result-figure')];
  const update = () => {
    const selectedTarget = target ? target.value : gallery.dataset.target;
    const selectedView = view ? view.value : gallery.dataset.view;
    figures.forEach(figure => {
      figure.hidden = !!figure.dataset.target && figure.dataset.target !== selectedTarget || figure.dataset.view !== selectedView;
      if (!figure.hidden) {
        const img = figure.querySelector('img');
        if (img.dataset.src) { img.src = img.dataset.src; delete img.dataset.src; }
      }
    });
    document.getElementById('figure-empty').hidden = !figures.length || figures.some(f => !f.hidden);
  };
  if (target) target.addEventListener('change', update);
  if (view) view.addEventListener('change', update);
  update();

  const table = document.querySelector('.result-report .measurements table');
  if (table) {
    const headers = [...table.tHead.rows[0].cells];
    const body = table.tBodies[0];
    const collator = new Intl.Collator(undefined, { numeric: true });
    headers.forEach((header, column) => {
      const label = header.textContent.trim();
      const button = document.createElement('button');
      button.type = 'button';
      button.textContent = label;
      button.title = `Sort by ${label}`;
      header.replaceChildren(button);
      button.addEventListener('click', () => {
        const ascending = header.getAttribute('aria-sort') !== 'ascending';
        headers.forEach(item => item.removeAttribute('aria-sort'));
        header.setAttribute('aria-sort', ascending ? 'ascending' : 'descending');
        const rows = [...body.rows];
        const values = rows.map(row => row.cells[column].textContent.trim());
        const numbers = values.map(value => Number(value.replace(/[$,]/g, '')));
        const numeric = numbers.every(Number.isFinite);
        rows.sort((a, b) => {
          const left = a.cells[column].textContent.trim();
          const right = b.cells[column].textContent.trim();
          const order = numeric ? Number(left.replace(/[$,]/g, '')) - Number(right.replace(/[$,]/g, ''))
            : collator.compare(left, right);
          return ascending ? order : -order;
        }).forEach(row => body.append(row));
      });
    });
  }
})();
"""

CSS = """
.figure-controls{display:flex;gap:18px;flex-wrap:wrap;margin:24px 0;font-family:system-ui,sans-serif;font-size:.85rem}
.figure-controls label{display:flex;align-items:center;gap:10px}
.figure-controls select{max-width:100%;padding:8px;background:var(--paper);color:var(--ink);border:1px solid var(--rule);font:inherit}
.figure-gallery .result-figure{margin:24px 0 38px;padding:0;border:0}
.result-figure[hidden],#figure-empty[hidden]{display:none}
.result-figure img{display:block;width:100%;height:auto;background:white}
.figure-gallery figcaption{font-size:.9rem;line-height:1.5;margin:10px 0;padding:0;border:0;text-transform:none;letter-spacing:normal}
.report-links{display:flex;justify-content:space-between;gap:14px;flex-wrap:wrap;margin:12px 0 22px;font-size:.85rem}
.measurements{overflow-x:auto}
.measurements th button{border:0;background:none;color:inherit;font:inherit;font-weight:inherit;cursor:pointer;padding:0;text-align:left}
.measurements th button::after{content:" ↕";color:var(--ink-2)}
.measurements th[aria-sort="ascending"] button::after{content:" ↑"}
.measurements th[aria-sort="descending"] button::after{content:" ↓"}
@media print{.figure-controls,.report-links{display:none}.result-figure{break-inside:avoid}}
"""
