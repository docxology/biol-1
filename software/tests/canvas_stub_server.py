"""Minimal threaded HTTP server mimicking Canvas API paths used by canvas_integration."""

from __future__ import annotations

import json
import re
import threading
from http.server import BaseHTTPRequestHandler, HTTPServer
from pathlib import PurePosixPath
from typing import Callable, Optional

from urllib.parse import parse_qs, unquote, urlparse


class _CanvasStubHandler(BaseHTTPRequestHandler):
    """Handle list folders, create folder, initiate upload, and raw upload steps."""

    def log_message(self, format: str, *args: object) -> None:
        """Suppress server stderr noise during pytest."""
        del format, args

    def _send_json(self, status: int, payload: dict) -> None:
        raw = json.dumps(payload).encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(raw)))
        self.end_headers()
        self.wfile.write(raw)

    def _read_body(self) -> Optional[bytes]:
        length = self.headers.get("Content-Length")
        if not length:
            return None
        return self.rfile.read(int(length))

    def do_GET(self) -> None:  # noqa: N802
        parsed = urlparse(self.path)
        path = unquote(parsed.path)
        courses_folders = re.match(r"^/api/v1/courses/(\d+)/folders$", path)
        if courses_folders:
            self._send_json(200, [])
            return
        self.send_error(404, "unsupported GET")

    def do_POST(self) -> None:  # noqa: N802
        parsed = urlparse(self.path)
        path = unquote(parsed.path)

        courses_folders = re.match(r"^/api/v1/courses/(\d+)/folders$", path)
        if courses_folders:
            payload = json.loads(self._read_body().decode("utf-8"))
            fid = getattr(self.server, "_next_folder_id", 4242)
            setattr(self.server, "_next_folder_id", fid + 1)
            self._send_json(
                200,
                {"id": fid, "name": payload.get("name", "")},
            )
            return

        folder_files = re.match(r"^/api/v1/folders/(\d+)/files$", path)
        if folder_files:
            qs = parse_qs(parsed.query)
            name_vals = qs.get("name", ["file.bin"])
            srv_host = self.server.server_address[0]
            srv_port = self.server.server_address[1]
            upload_endpoint = getattr(self.server, "_upload_endpoint", "/raw-upload/")
            scheme = getattr(self.server, "_scheme", "http")
            upload_url = f"{scheme}://{srv_host}:{srv_port}{upload_endpoint}"
            setattr(self.server, "_last_upload_stub", PurePosixPath(name_vals[0]))
            self._send_json(
                200,
                {
                    "upload_url": upload_url,
                    "upload_params": [],
                },
            )
            return

        if "/raw-upload" in path.replace("//", "/"):
            self._read_body()
            self._send_json(
                200,
                {"url": "http://stub.local/files/uploaded-file", "display_name": "stub"},
            )
            return

        self.send_error(404, "unsupported POST")


def start_canvas_stub_http(
    scheme: str = "http",
    upload_endpoint: str = "/raw-upload/",
    pre_ready: Optional[Callable[[HTTPServer], None]] = None,
) -> HTTPServer:
    """Start daemon server; return HTTPServer bound to localhost with random port."""

    srv = HTTPServer(("127.0.0.1", 0), _CanvasStubHandler)
    setattr(srv, "_scheme", scheme)
    setattr(srv, "_upload_endpoint", upload_endpoint)
    setattr(srv, "_next_folder_id", 9001)

    thread = threading.Thread(target=srv.serve_forever, daemon=True)
    thread.start()
    host, port = srv.server_address
    setattr(srv, "_thread", thread)
    if pre_ready:
        pre_ready(srv)

    setattr(srv, "host", host)
    setattr(srv, "port", port)
    return srv


def stop_canvas_stub(server: HTTPServer, timeout_s: float = 2.0) -> None:
    """Shut down threaded HTTP server cleanly."""
    del timeout_s  # shutdown + join clears the daemon thread
    server.shutdown()
    thr = getattr(server, "_thread", None)
    if thr is not None:
        thr.join(timeout=10.0)
    server.server_close()
