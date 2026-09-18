#!/usr/bin/env python3
"""HTTP server for the Astro lab notebook and the project deliverables.

Standard library only. Bound strictly to loopback (127.0.0.1). It runs on the
TrueNAS box in the python container of scripts/truenas-wiki/docker-compose.yml,
behind the nginx there, which reaches it for /wiki/api/ and /wiki/ask only;
Tailscale Serve on the NAS carries the tailnet to that nginx.

Routes:
  /                 redirect to /wiki/
  /wiki/...         the built notebook in `wiki/public/`
  /wiki/f/<path>    one file from the project tree, read-only
  /wiki/ask         POST a question to the worker that made a note
  everything else   the project tree, as before
"""

from __future__ import annotations

import argparse
import json
import mimetypes
import os
import re
import subprocess
import sys
import threading
from http import HTTPStatus
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from urllib.parse import unquote, urlsplit

# The project is the folder above scripts/, wherever the tree is copied.
DEFAULT_ROOT = Path(__file__).resolve().parent.parent
CLAUDE_ROOT = Path.home() / ".claude"
BRIDGE = CLAUDE_ROOT / "scripts/hermes-bridge/bridge.py"
sys.path.insert(0, str(DEFAULT_ROOT / "wiki"))
import activity
import research
import research_figures

ASK_TIMEOUT = 480
SLUG = re.compile(r"^[a-z0-9][a-z0-9-]{0,80}$")
JOB = re.compile(r"^t_[0-9a-f]{6,16}$")

# Ensure customary scientific and data formats are recognized
mimetypes.add_type("text/csv", ".csv")
mimetypes.add_type("text/tab-separated-values", ".tsv")
mimetypes.add_type("application/json", ".json")
mimetypes.add_type("application/pdf", ".pdf")
mimetypes.add_type("application/x-ipynb+json", ".ipynb")
mimetypes.add_type("application/x-hdf5", ".h5")
mimetypes.add_type("text/x-python", ".py")
mimetypes.add_type("font/woff2", ".woff2")
mimetypes.add_type("text/javascript; charset=utf-8", ".js")

_ask_lock = threading.Lock()
_asking: set = set()


class Publication:
    """Coalesce saves into serialized background builds; report failures separately."""

    def __init__(self):
        self.lock = threading.Lock()
        self.pending = False
        self.running = False
        self.state = "ready"

    def request(self, root):
        with self.lock:
            self.pending = True
            self.state = "pending"
            if self.running:
                return
            self.running = True
        threading.Thread(target=self.work, args=(root,), daemon=True).start()

    def work(self, root):
        while True:
            with self.lock:
                self.pending = False
            try:
                result = subprocess.run([sys.executable, str(root / "wiki/build.py")],
                                        capture_output=True, text=True, timeout=300)
                state = "ready" if result.returncode == 0 else "failed"
                if result.returncode:
                    print(result.stderr, file=sys.stderr)
            except Exception as exc:
                print("Wiki publication failed:", exc, file=sys.stderr)
                state = "failed"
            with self.lock:
                if not self.pending:
                    self.state = state
                    self.running = False
                    return


publication = Publication()


def today() -> str:
    import datetime
    return datetime.date.today().isoformat()


def note_job(note_path: Path) -> str:
    """The card id recorded in a note's frontmatter."""
    head = note_path.read_text(encoding="utf-8").split("---", 2)
    if len(head) < 3:
        return ""
    m = re.search(r"^job:[^\S\n]*(\S+)[^\S\n]*$", head[1], re.M)
    return m.group(1) if m else ""


def append_thread(note_path: Path, question: str, answer: str) -> None:
    """Record one exchange in the note, so the page rebuilds with it."""
    text = note_path.read_text(encoding="utf-8").rstrip("\n")
    if not re.search(r"^##\s+Thread\s*$", text, re.M):
        text += "\n\n## Thread"
    one_line = lambda s: re.sub(r"\s+", " ", s).strip()
    text += "\n\n**Q** %s · %s\n\n**A** %s\n" % (today(), one_line(question), one_line(answer))
    note_path.write_text(text, encoding="utf-8")


class AstroWikiHandler(SimpleHTTPRequestHandler):
    """Serves the built notebook, the project tree, and the per-note question."""

    server_version = "AstroWikiServer/2.0"
    project_root = DEFAULT_ROOT

    def __init__(self, *args, **kwargs):
        self.project_root = self.project_root.resolve()
        super().__init__(*args, directory=str(self.project_root), **kwargs)

    # -- helpers ---------------------------------------------------------
    def reply_json(self, status, payload):
        body = json.dumps(payload).encode()
        self.send_response(status)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    # -- routing ---------------------------------------------------------
    def do_GET(self) -> None:
        clean_path = urlsplit(self.path).path
        if clean_path.startswith("/wiki/api/"):
            self.activity_api("GET")
            return
        if clean_path in {"", "/", "/index.html"}:
            self.send_response(HTTPStatus.FOUND)
            self.send_header("Location", "/wiki/")
            self.end_headers()
            return
        if clean_path == "/wiki":
            self.send_response(HTTPStatus.FOUND)
            self.send_header("Location", "/wiki/")
            self.end_headers()
            return
        super().do_GET()

    def do_POST(self) -> None:
        if urlsplit(self.path).path.startswith("/wiki/api/"):
            self.activity_api("POST")
            return
        if urlsplit(self.path).path != "/wiki/ask":
            self.send_error(HTTPStatus.NOT_FOUND)
            return
        try:
            size = int(self.headers.get("Content-Length") or 0)
            payload = json.loads(self.rfile.read(size) or b"{}")
        except Exception:
            self.reply_json(HTTPStatus.BAD_REQUEST, {"ok": False, "state": "Bad request"})
            return
        self.ask(payload)

    def activity_api(self, method):
        """Serve known research targets and accept bounded same-origin writes."""
        try:
            root = self.project_root / "wiki/research"
            records, faults = research.load(root)
            if faults:
                raise ValueError("Research records could not be loaded")
            parts = unquote(urlsplit(self.path).path).removeprefix("/wiki/api/").split("/")
            if method == "GET" and parts == ["publication"]:
                self.reply_json(200, {"state": publication.state})
                return
            if method == "GET" and parts == ["catalog"]:
                items = [{"kind": kind, "id": ident, "title": item["title"],
                          "url": "/wiki/" + ("p/" if kind == "priority" else "q/") + ident + "/",
                          "state": activity.state(activity.read(root, kind, ident)) if kind == "priority" else item["status"]}
                         for (kind, ident), item in activity.targets(records).items()]
                figures = [{"key": key, "title": " · ".join(filter(None, [f["experiment"], f.get("target"), f.get("arm"), f.get("view"), f["caption"]])),
                            "url": "/wiki/api/figure/" + key}
                           for key, f in activity.figures(records).items()]
                self.reply_json(200, {"targets": items, "figures": figures})
                return
            if method == "GET" and len(parts) == 2 and parts[0] == "figure":
                figure = activity.figures(records).get(parts[1])
                if figure is None:
                    raise ValueError("Unknown figure")
                if "path" in figure:
                    research.asset_url(figure["path"], "/wiki", self.project_root)
                    path = self.project_root / unquote(figure["path"])
                    data, mime = path.read_bytes(), mimetypes.guess_type(str(path))[0]
                else:
                    data, mime = research_figures.image_bytes(self.project_root, figure), "image/png"
                    research_figures.notebook.cache_clear()
                self.send_response(200)
                self.send_header("Content-Type", mime or "application/octet-stream")
                self.send_header("Content-Length", str(len(data)))
                self.end_headers()
                self.wfile.write(data)
                return
            if len(parts) != 3 or parts[0] != "activity" or tuple(parts[1:]) not in activity.targets(records):
                self.reply_json(404, {"error": "Unknown research target"})
                return
            kind, ident = parts[1:]
            if method == "POST":
                origin = urlsplit(self.headers.get("Origin", ""))
                host = self.headers.get("X-Forwarded-Host", self.headers.get("Host", ""))
                if origin.scheme not in {"http", "https"} or origin.netloc != host:
                    self.reply_json(403, {"error": "Same-origin request required"})
                    return
                size = int(self.headers.get("Content-Length", "0"))
                if not 0 < size <= activity.MAX_REQUEST:
                    self.reply_json(413, {"error": "Note exceeds 24 MB"})
                    return
                if self.headers.get_content_type() != "application/json":
                    raise ValueError("JSON request required")
                payload = json.loads(self.rfile.read(size))
                result = activity.save(root, self.project_root, records, kind, ident, payload)
                publication.request(self.project_root)
            else:
                result = activity.snapshot(root, kind, ident)
            result["html"] = activity.history_html(result["entries"], "/wiki", self.project_root)
            result["publication"] = publication.state
            self.reply_json(200, result)
        except activity.Conflict as exc:
            self.reply_json(409, {"error": str(exc)})
        except (ValueError, TypeError, KeyError) as exc:
            self.reply_json(400, {"error": str(exc)})
        except Exception as exc:
            print("Activity request failed:", exc, file=sys.stderr)
            self.reply_json(500, {"error": "Save failed; draft retained"})

    def ask(self, payload) -> None:
        slug = str(payload.get("note", ""))
        job = str(payload.get("job", ""))
        question = str(payload.get("question", "")).strip()
        if not (SLUG.match(slug) and JOB.match(job) and question):
            self.reply_json(HTTPStatus.BAD_REQUEST, {"ok": False, "state": "Bad request"})
            return
        note_path = self.project_root / "wiki/notes" / (slug + ".md")
        if not note_path.is_file() or note_job(note_path) != job:
            self.reply_json(HTTPStatus.NOT_FOUND, {"ok": False, "state": "Unknown note"})
            return

        with _ask_lock:                      # one question in flight per note
            if slug in _asking:
                self.reply_json(HTTPStatus.CONFLICT, {"ok": False, "state": "Busy"})
                return
            _asking.add(slug)
        try:
            run = subprocess.run(
                ["/usr/bin/python3", str(BRIDGE), "ask", job, question],
                capture_output=True, text=True, timeout=ASK_TIMEOUT)
            answer = (run.stdout or "").strip()
            if run.returncode != 0 or not answer:
                self.reply_json(HTTPStatus.BAD_GATEWAY, {"ok": False, "state": "No answer"})
                return
            append_thread(note_path, question, answer)
            subprocess.run([sys.executable, str(self.project_root / "wiki/build.py")],
                           capture_output=True, text=True, timeout=300)
            self.reply_json(HTTPStatus.OK, {"ok": True})
        except subprocess.TimeoutExpired:
            self.reply_json(HTTPStatus.GATEWAY_TIMEOUT, {"ok": False, "state": "Timed out"})
        except Exception:
            self.reply_json(HTTPStatus.INTERNAL_SERVER_ERROR, {"ok": False, "state": "Failed"})
        finally:
            with _ask_lock:
                _asking.discard(slug)

    def translate_path(self, path: str) -> str:
        clean_path = unquote(urlsplit(path).path)
        missing = str(self.project_root / "__not_found__")

        if clean_path.startswith("/wiki/f/"):
            resolved = (self.project_root / clean_path[len("/wiki/f/"):]).resolve()
            try:
                resolved.relative_to(self.project_root)
                return str(resolved)
            except ValueError:
                return missing

        if clean_path == "/wiki/" or clean_path.startswith("/wiki/"):
            public = (self.project_root / "wiki/public").resolve()
            rest = clean_path[len("/wiki/"):]
            resolved = (public / rest).resolve()
            try:
                resolved.relative_to(public)
            except ValueError:
                return missing
            if resolved.is_dir():
                resolved = resolved / "index.html"
            if resolved.exists():
                return str(resolved)
            return missing

        if clean_path.startswith("/.claude/"):
            resolved = (CLAUDE_ROOT / clean_path[len("/.claude/"):]).resolve()
            try:
                resolved.relative_to(CLAUDE_ROOT)
                return str(resolved)
            except ValueError:
                return missing

        return super().translate_path(path)

    def end_headers(self) -> None:
        self.send_header("Cache-Control", "no-cache, no-store, must-revalidate")
        super().end_headers()


class WikiServer(ThreadingHTTPServer):
    """One connection per request over HTTP/1.0, so a page load is a burst.

    Safari opens a connection for every script, stylesheet and font of a page,
    plus speculative preconnects for each subresource it remembers, before the
    HTML has arrived. The default listen backlog of 5 let the kernel reset the
    rest of that burst, and a reset `<script defer>` fails silently, leaving
    the page without KaTeX. 128 matches kern.ipc.somaxconn.
    """

    request_queue_size = 128


def run_server(host: str = "127.0.0.1", port: int = 8765, root: Path = DEFAULT_ROOT) -> None:
    if host not in {"127.0.0.1", "localhost", "::1"}:
        sys.stderr.write(
            "Refusing to bind to non-loopback address %r. Security policy requires loopback only.\n"
            % host)
        sys.exit(1)

    AstroWikiHandler.project_root = root
    publication.request(root)
    with WikiServer((host, port), AstroWikiHandler) as httpd:
        print("Serving Astro Lab Notebook on http://%s:%d/wiki/ (root: %s)" % (host, port, root))
        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            print("\nShutting down Astro Wiki server.")


def main() -> None:
    parser = argparse.ArgumentParser(description="Serve the Astro lab notebook on loopback.")
    parser.add_argument("--bind", default="127.0.0.1", help="Address to bind (default: 127.0.0.1)")
    parser.add_argument("--port", type=int, default=8765, help="Port to listen on (default: 8765)")
    parser.add_argument("--root", type=Path, default=DEFAULT_ROOT, help="Project root to serve")
    args = parser.parse_args()
    run_server(host=args.bind, port=args.port, root=args.root.resolve())


if __name__ == "__main__":
    main()
