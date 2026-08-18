"""
Python HTTP API Server for Deep Research Agent UI and 5-Step Pipeline.
"""

from __future__ import annotations

import asyncio
from http.server import HTTPServer, SimpleHTTPRequestHandler, ThreadingHTTPServer
import json
import os
from pathlib import Path
import sys

# Ensure repository root is in sys.path
REPO_ROOT = Path(__file__).parents[1]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from deep_research_agent.engine.five_step_pipeline import FiveStepResearchPipeline

UI_DIR = Path(__file__).parent / "ui"
WORKSPACE_DIR = Path(__file__).parent / "output"


class DeepResearchAPIHandler(SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=str(UI_DIR), **kwargs)

    def do_GET(self):
        if self.path in ("/favicon.ico", "/favicon.svg"):
            favicon_svg = '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 100 100"><text y=".9em" font-size="90">⚛️</text></svg>'
            self.send_response(200)
            self.send_header("Content-Type", "image/svg+xml")
            self.send_header("Cache-Control", "public, max-age=86400")
            self.end_headers()
            self.wfile.write(favicon_svg.encode("utf-8"))
            return
        super().do_GET()

    def do_POST(self):
        if self.path == "/api/research":
            content_len = int(self.headers.get("Content-Length", 0))
            body = self.rfile.read(content_len).decode("utf-8")
            data = json.loads(body) if body else {}
            query = data.get("query", "Autonomous Harness Engineering")

            # Run 5-step SOP pipeline
            pipeline = FiveStepResearchPipeline(WORKSPACE_DIR)
            result = asyncio.run(pipeline.execute_deep_research(query))

            self.send_response(200)
            self.send_header("Content-Type", "application/json")
            self.send_header("Access-Control-Allow-Origin", "*")
            self.end_headers()
            self.wfile.write(json.dumps(result, ensure_ascii=False).encode("utf-8"))
        else:
            self.send_error(404, "Endpoint not found")

    def do_OPTIONS(self):
        self.send_response(200)
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Methods", "POST, GET, OPTIONS")
        self.send_header("Access-Control-Allow-Headers", "Content-Type")
        self.end_headers()


def run_server(port: int = 8090):
    server = ThreadingHTTPServer(("0.0.0.0", port), DeepResearchAPIHandler)
    print(f"[*] Deep Research Agent UI running at http://localhost:{port}/")
    server.serve_forever()


if __name__ == "__main__":
    port = int(sys.argv[1]) if len(sys.argv) > 1 else 8090
    run_server(port)
