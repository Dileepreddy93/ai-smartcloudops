"""Mock live endpoints for Phase 7 aws_live tests.

Starts lightweight HTTP servers to simulate:
- Node Exporter metrics at http://127.0.0.1:9100/metrics
- App health at http://127.0.0.1:5000/health
- Prometheus readiness at http://127.0.0.1:9090/-/ready
- Grafana health at http://127.0.0.1:3000/api/health

Usage:
  python infra/scripts/mock_live_endpoints.py
Press Ctrl+C to stop.
"""

from __future__ import annotations

import json
import threading
from http.server import BaseHTTPRequestHandler, HTTPServer


class _Handler(BaseHTTPRequestHandler):
    def do_GET(self):  # noqa: N802
        if self.server.server_port == 9100 and self.path == "/metrics":
            body = (
                "# HELP dummy Dummy metric\n"
                "# TYPE dummy gauge\n"
                "dummy 1\n"
            ).encode("utf-8")
            self._send(200, "text/plain; version=0.0.4", body)
            return

        if self.server.server_port == 5000 and self.path == "/health":
            body = json.dumps({"status": "ok"}).encode("utf-8")
            self._send(200, "application/json", body)
            return

        if self.server.server_port == 9090 and self.path == "/-/ready":
            self._send(200, "text/plain", b"ready\n")
            return

        if self.server.server_port == 3000 and self.path == "/api/health":
            body = json.dumps({"database": "ok"}).encode("utf-8")
            self._send(200, "application/json", body)
            return

        self._send(404, "text/plain", b"not found\n")

    def log_message(self, format, *args):  # noqa: A003 - silence default logging
        return

    def _send(self, code: int, ctype: str, body: bytes):
        self.send_response(code)
        self.send_header("Content-Type", ctype)
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)


def _serve(port: int):
    server = HTTPServer(("127.0.0.1", port), _Handler)
    server.serve_forever()


def main():
    ports = [9100, 5000, 9090, 3000]
    threads = []
    for p in ports:
        t = threading.Thread(target=_serve, args=(p,), daemon=True)
        t.start()
        threads.append(t)
    # Keep the main thread alive
    try:
        for t in threads:
            t.join()
    except KeyboardInterrupt:
        pass


if __name__ == "__main__":
    main()


