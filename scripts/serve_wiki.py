#!/usr/bin/env python3
"""Lightweight HTTP server for Astro research wiki and deliverables.

Standard library only. Bound strictly to loopback (127.0.0.1).
Exposed securely to the user's Tailscale network via Tailscale Serve.
"""

from __future__ import annotations

import argparse
import mimetypes
import os
import sys
from http import HTTPStatus
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from urllib.parse import unquote, urlsplit

DEFAULT_ROOT = Path("/Users/liuhao/Downloads/Astro project").resolve()
CLAUDE_ROOT = Path.home() / ".claude"

# Ensure customary scientific and data formats are recognized
mimetypes.add_type("text/csv", ".csv")
mimetypes.add_type("text/tab-separated-values", ".tsv")
mimetypes.add_type("application/json", ".json")
mimetypes.add_type("application/pdf", ".pdf")
mimetypes.add_type("application/x-ipynb+json", ".ipynb")
mimetypes.add_type("application/x-hdf5", ".h5")
mimetypes.add_type("text/x-python", ".py")


class AstroWikiHandler(SimpleHTTPRequestHandler):
    """Custom request handler that supports root redirect and .claude evidence mapping."""

    server_version = "AstroWikiServer/1.0"
    project_root = DEFAULT_ROOT

    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=str(self.project_root), **kwargs)

    def do_GET(self) -> None:
        clean_path = urlsplit(self.path).path
        if clean_path in {"", "/", "/index.html"}:
            self.send_response(HTTPStatus.FOUND)
            self.send_header("Location", "/wiki/index.html")
            self.end_headers()
            return
        super().do_GET()

    def translate_path(self, path: str) -> str:
        clean_path = urlsplit(path).path
        clean_path = unquote(clean_path)

        if clean_path.startswith("/.claude/"):
            relative_sub = clean_path[len("/.claude/") :]
            resolved = (CLAUDE_ROOT / relative_sub).resolve()
            try:
                resolved.relative_to(CLAUDE_ROOT)
                return str(resolved)
            except ValueError:
                return str(self.project_root / "__not_found__")

        return super().translate_path(path)

    def end_headers(self) -> None:
        self.send_header("Cache-Control", "no-cache, no-store, must-revalidate")
        super().end_headers()


def run_server(host: str = "127.0.0.1", port: int = 8765, root: Path = DEFAULT_ROOT) -> None:
    if host not in {"127.0.0.1", "localhost", "::1"}:
        sys.stderr.write(f"Refusing to bind to non-loopback address {host!r}. Security policy requires loopback only.\n")
        sys.exit(1)

    AstroWikiHandler.project_root = root
    server_address = (host, port)
    with ThreadingHTTPServer(server_address, AstroWikiHandler) as httpd:
        print(f"Serving Astro Wiki on http://{host}:{port} (root: {root})")
        print("Redirecting / to /wiki/index.html")
        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            print("\nShutting down Astro Wiki server.")


def main() -> None:
    parser = argparse.ArgumentParser(description="Serve Astro Research Wiki on loopback.")
    parser.add_argument("--bind", default="127.0.0.1", help="Address to bind (default: 127.0.0.1)")
    parser.add_argument("--port", type=int, default=8765, help="Port to listen on (default: 8765)")
    parser.add_argument("--root", type=Path, default=DEFAULT_ROOT, help="Project root to serve")
    args = parser.parse_args()
    run_server(host=args.bind, port=args.port, root=args.root.resolve())


if __name__ == "__main__":
    main()
