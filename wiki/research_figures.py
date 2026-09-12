"""Render saved research figures without executing or modifying their sources."""

import base64
import binascii
import html
import json
from functools import lru_cache
from pathlib import Path
from urllib.parse import quote

VIEWS = ("Fits", "SFH", "Posteriors", "Comparison")
esc = html.escape


@lru_cache(maxsize=1)
def notebook(path):
    return json.loads(path.read_text(encoding="utf-8"))


def image_bytes(project, figure):
    try:
        output = notebook(project / figure["notebook"])["cells"][figure["cell"]]["outputs"][figure["output"]]
        encoded = output["data"]["image/png"]
        encoded = "".join(encoded) if isinstance(encoded, list) else encoded
        data = base64.b64decode(encoded, validate=False)
        if not data.startswith(b"\x89PNG\r\n\x1a\n"):
            raise ValueError("saved output is not a PNG")
        return data
    except (KeyError, IndexError, TypeError, ValueError, binascii.Error) as exc:
        raise ValueError("missing or invalid saved PNG output") from exc


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
                    image_bytes(project, figure)
            except (ValueError, OSError) as exc:
                faults.append(prefix + "figure %d: %s" % (index, exc))
    notebook.cache_clear()
    return faults


def image_url(figure, project, scratch, base, asset_url):
    if figure.get("path"):
        return asset_url(figure["path"], base, project)
    relative = Path("research-images") / Path(figure["notebook"]).with_suffix("") / (
        "c%d-o%d.png" % (figure["cell"], figure["output"]))
    output = scratch / relative
    if not output.exists():
        output.parent.mkdir(parents=True, exist_ok=True)
        output.write_bytes(image_bytes(project, figure))
    return base + "/" + quote(relative.as_posix())


def render(record, project, scratch, base, asset_url, markdown):
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
    for f in figures:
        src = image_url(f, project, scratch, base, asset_url)
        visible = (not f.get("target") or f["target"] == target) and f["view"] == view
        body += ('<figure class="result-figure" data-target="%s" data-view="%s"%s>'
                 '<a href="%s"><img %s="%s" alt="%s" loading="lazy"></a>'
                 '<figcaption>%s</figcaption></figure>') % (
                    esc(f.get("target", "")), esc(f["view"]), "" if visible else " hidden",
                    esc(src), "src" if visible else "data-src", esc(src), esc(f["caption"]), esc(f["caption"]))
    body += '</div><p id="figure-empty" class="empty" hidden>No figure for this target and view.</p>'
    if record["sections"]["Measurements"]:
        body += '<div class="measurements">%s</div>' % markdown(record["sections"]["Measurements"])
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
@media print{.figure-controls,.report-links{display:none}.result-figure{break-inside:avoid}}
"""
