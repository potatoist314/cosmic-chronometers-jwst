from __future__ import annotations

import functools
import hashlib
import http.server
import pickle
import shutil
import threading
import urllib.parse
import urllib.request
from html.parser import HTMLParser
from pathlib import Path

import numpy as np

from scripts import plot_ceridwen_checkpoint_evolution as animation


PROJECT_ROOT = Path(__file__).resolve().parents[1]
RESULT_ARTIFACT = (
    PROJECT_ROOT
    / "results/rtx-4070-super-four-galaxy-fits/gpu_0_m1_210210"
    / "ceridwen-checkpoint-spectrum-evolution.html"
)
HOST_ARTIFACT = (
    PROJECT_ROOT
    / "wiki/analyses/checkpoint-animation"
    / "ceridwen-checkpoint-spectrum-evolution.html"
)
ACCEPTED_PAYLOAD_SHA256 = (
    "9823f0f769775d647bec933ba82d9569ee4375f36459886a39299da138df492d"
)
ACCEPTED_SCIENCE_SHA256 = (
    "805d810ed9afe1cc86ab8f4cd0f05c6bb68d514009ee7c1f7335d988e3c57990"
)


class _LinkParser(HTMLParser):
    def __init__(self):
        super().__init__()
        self.links = []

    def handle_starttag(self, tag, attrs):
        attributes = dict(attrs)
        if tag == "a" and "href" in attributes:
            self.links.append(attributes)


class _QuietHandler(http.server.SimpleHTTPRequestHandler):
    def log_message(self, format, *args):
        pass


def _payload_hash(path: Path) -> tuple[str, str]:
    raw, payload = animation.load_embedded_payload(path)
    return (
        hashlib.sha256(raw.encode()).hexdigest(),
        animation.scientific_payload_sha256(payload),
    )


def test_load_checkpoint_metadata_accepts_legacy_snapshot(tmp_path):
    path = tmp_path / "legacy.pkl"
    legacy = {
        "positions": {"x": np.arange(4.0)[:, None]},
        "loglikelihood": np.arange(4.0),
        "loglikelihood_birth": np.arange(4.0) - 1,
        "logZ": 2.5,
        "n_dead": 4,
        "partial": True,
    }
    with path.open("wb") as handle:
        pickle.dump(legacy, handle)

    loaded = animation.load_checkpoint_metadata(path)

    assert loaded["schema_version"] == 1
    assert loaded["progress"] == {}
    assert loaded["n_dead"] == 4


def test_render_html_has_controls_metadata_and_static_fallback():
    shared = {
        "wavelength": np.array([4000.0, 4100.0, 4200.0]),
        "observed": np.array([1.0, 1.2, 0.9]),
        "uncertainty": np.array([0.1, 0.1, 0.2]),
        "target": "fixture",
        "source_run": "/tmp/run",
        "source_data": "/tmp/data.fits",
        "source_checkpoint": "/tmp/checkpoint.pkl",
        "source_rescue": "/tmp/rescue.pkl",
        "source_result": "/tmp/result.h5",
        "n_draws": 4,
    }
    frames = [
        {
            "label": "Checkpoint 1",
            "kind": "posterior model spectrum",
            "iteration": 10,
            "likelihood_calls": 100,
            "discarded": 8,
            "live": 2,
            "ess": 3.5,
            "logZ": 1.25,
            "delta_logZ": 0.2,
            "calibration_fraction": 0.03,
            "residual_uncertainty": np.array([0.1, 0.1, 0.2]),
            "model_q16": np.array([0.8, 1.0, 0.7]),
            "model_q50": np.array([0.9, 1.1, 0.8]),
            "model_q84": np.array([1.0, 1.2, 0.9]),
        }
    ]

    document = animation.render_html(
        shared, frames, title="Fixture", command="python generate.py"
    )

    assert '<button id="play"' in document
    assert '<input id="frame" type="range"' in document
    assert "min-height:44px" in document
    assert "grid-template-columns:repeat(2,minmax(0,1fr))" in document
    assert "orientationchange" in document
    assert "compactResidual&&window.innerHeight<=500" in document
    assert "Residual / σeff" in document
    assert "const yTicks=compact?3:5" in document
    assert "Likelihood calls" in document
    assert "Weighted ESS" in document
    assert "Calibration floor" in document
    assert "Static final checkpoint" in document
    assert "<polyline" not in document
    assert "<polygon" not in document
    assert "Nested-sampling bands can widen or narrow" in document
    assert "axis rescales for each state" in document
    assert "https://" not in document
    assert "NaN" not in document


def test_generated_artifacts_preserve_accepted_payload():
    for path in (RESULT_ARTIFACT, HOST_ARTIFACT):
        assert _payload_hash(path) == (
            ACCEPTED_PAYLOAD_SHA256,
            ACCEPTED_SCIENCE_SHA256,
        )


def test_preserved_payload_survives_regeneration(tmp_path):
    output = tmp_path / "viewer.html"
    assert (
        animation.main(
            [
                "--legacy-dr2-run",
                "results/rtx-4070-super-four-galaxy-fits/gpu_0_m1_210210",
                "--target",
                "M1_210210",
                "--preserve-payload-from",
                str(RESULT_ARTIFACT),
                "--output",
                str(output),
                "--hosted",
            ]
        )
        == 0
    )
    assert _payload_hash(output) == (
        ACCEPTED_PAYLOAD_SHA256,
        ACCEPTED_SCIENCE_SHA256,
    )
    document = output.read_text()
    assert "file://" not in document
    assert 'href="../ceridwen-results.html"' in document
    assert document.index('class="controls"') < document.index('class="provenance"')
    assert "short?[120,127]" in document
    assert "Residual / σeff" in document
    assert "i===ticks-1?'end'" in document


def test_pages_host_root_serves_checkpoint_links(tmp_path):
    site_root = tmp_path / "_site"
    shutil.copytree(
        PROJECT_ROOT / "wiki",
        site_root,
        ignore=shutil.ignore_patterns("*.md", ".DS_Store"),
    )
    board = site_root / "analyses/ceridwen-results.html"
    hosted = site_root / "analyses/checkpoint-animation/ceridwen-checkpoint-spectrum-evolution.html"

    board_parser = _LinkParser()
    board_parser.feed(board.read_text())
    checkpoint_links = [
        link["href"]
        for link in board_parser.links
        if link.get("data-host-check") == "checkpoint-animation"
    ]
    assert checkpoint_links

    hosted_parser = _LinkParser()
    hosted_parser.feed(hosted.read_text())
    documents = ((board, checkpoint_links), (hosted, [link["href"] for link in hosted_parser.links]))
    targets = []
    for document, links in documents:
        for href in links:
            parsed = urllib.parse.urlsplit(href)
            if not parsed.path:
                assert f'id="{parsed.fragment}"' in document.read_text()
                continue
            target = (document.parent / urllib.parse.unquote(parsed.path)).resolve()
            assert target.is_relative_to(site_root.resolve())
            assert target.is_file()
            targets.append(target.relative_to(site_root).as_posix())

    handler = functools.partial(_QuietHandler, directory=str(site_root))
    server = http.server.ThreadingHTTPServer(("127.0.0.1", 0), handler)
    thread = threading.Thread(target=server.serve_forever, daemon=True)
    thread.start()
    try:
        for target in targets:
            url = f"http://127.0.0.1:{server.server_port}/{urllib.parse.quote(target)}"
            with urllib.request.urlopen(url) as response:
                assert response.status == 200
    finally:
        server.shutdown()
        thread.join()
