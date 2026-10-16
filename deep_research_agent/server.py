"""
Python HTTP API Server for Deep Research Agent UI and 5-Step Pipeline.
Supports synchronous /api/research plus async job + SSE progress + cancel.
"""

from __future__ import annotations

from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
import json
from pathlib import Path
import queue
import sys
import threading
import time
import uuid

# Ensure repository root is in sys.path
REPO_ROOT = Path(__file__).parents[1]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from deep_research_agent.engine.five_step_pipeline import FiveStepResearchPipeline, PipelineCancelled

UI_DIR = Path(__file__).parent / "ui"
# Flat workspace: artifacts land in deep_research_agent/output/ (not output/output/)
WORKSPACE_DIR = Path(__file__).parent / "output"

# In-memory research jobs for SSE progress / cancel
_JOBS: dict[str, dict] = {}
_JOBS_LOCK = threading.Lock()


def _json_response(handler: SimpleHTTPRequestHandler, status: int, payload: dict) -> None:
    body = json.dumps(payload, ensure_ascii=False).encode("utf-8")
    handler.send_response(status)
    handler.send_header("Content-Type", "application/json")
    handler.send_header("Access-Control-Allow-Origin", "*")
    handler.send_header("Content-Length", str(len(body)))
    handler.end_headers()
    handler.wfile.write(body)


def _parse_research_body(handler: SimpleHTTPRequestHandler) -> dict:
    content_len = int(handler.headers.get("Content-Length", 0))
    if content_len > 1_000_000:
        raise ValueError("Request body too large")
    body = handler.rfile.read(content_len).decode("utf-8") if content_len else ""
    data = json.loads(body) if body else {}
    query = str(data.get("query", "Autonomous Harness Engineering")).strip() or "Autonomous Harness Engineering"
    days_back = int(data.get("days_back", 30))
    depth = str(data.get("depth", "multi-source") or "multi-source").strip().lower()
    if depth not in {"multi-source", "deep-audit", "quick-scan"}:
        depth = "multi-source"
    return {"query": query, "days_back": days_back, "depth": depth}


def _run_pipeline_job(job_id: str, params: dict) -> None:
    job = _JOBS[job_id]
    event_q: queue.Queue = job["queue"]
    cancel_event: threading.Event = job["cancel"]

    def progress_cb(event_type: str, details: dict) -> None:
        event_q.put({"event": event_type, "details": details, "ts": time.time()})

    try:
        pipeline = FiveStepResearchPipeline(WORKSPACE_DIR)
        result = pipeline.execute_deep_research(
            params["query"],
            days_back=params["days_back"],
            depth=params["depth"],
            progress_cb=progress_cb,
            cancel_event=cancel_event,
        )
        with _JOBS_LOCK:
            job["status"] = "completed"
            job["result"] = result
        event_q.put({"event": "RESULT", "details": {"status": result.get("status")}, "result": result, "ts": time.time()})
    except PipelineCancelled:
        with _JOBS_LOCK:
            job["status"] = "cancelled"
        event_q.put({"event": "CANCELLED", "details": {"message": "cancelled"}, "ts": time.time()})
    except Exception as exc:
        with _JOBS_LOCK:
            job["status"] = "error"
            job["error"] = str(exc)
        event_q.put({"event": "ERROR", "details": {"message": str(exc)}, "ts": time.time()})
    finally:
        event_q.put(None)  # sentinel


class DeepResearchAPIHandler(SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=str(UI_DIR), **kwargs)

    def log_message(self, format: str, *args) -> None:
        sys.stderr.write("%s - - [%s] %s\n" % (self.address_string(), self.log_date_time_string(), format % args))

    def do_GET(self):
        path = self.path.split("?", 1)[0]
        if path in ("/favicon.ico", "/favicon.svg"):
            favicon_path = UI_DIR / "favicon.svg"
            if favicon_path.is_file():
                content = favicon_path.read_bytes()
            else:
                content = b'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 100 100"><text y=".9em" font-size="90">\xe2\x9a\x9b\xef\xb8\x8f</text></svg>'
            self.send_response(200)
            self.send_header("Content-Type", "image/svg+xml")
            self.send_header("Cache-Control", "public, max-age=86400")
            self.end_headers()
            self.wfile.write(content)
            return

        if path == "/api/research/events":
            self._handle_sse()
            return

        if path == "/api/health":
            _json_response(self, 200, {"status": "ok", "workspace": str(WORKSPACE_DIR)})
            return

        super().do_GET()

    def _handle_sse(self) -> None:
        from urllib.parse import parse_qs, urlparse

        qs = parse_qs(urlparse(self.path).query)
        job_id = (qs.get("job_id") or [""])[0]
        with _JOBS_LOCK:
            job = _JOBS.get(job_id)
        if not job:
            _json_response(self, 404, {"error": "unknown job_id"})
            return

        self.send_response(200)
        self.send_header("Content-Type", "text/event-stream")
        self.send_header("Cache-Control", "no-cache")
        self.send_header("Connection", "keep-alive")
        self.send_header("Access-Control-Allow-Origin", "*")
        self.end_headers()

        event_q: queue.Queue = job["queue"]
        try:
            while True:
                try:
                    item = event_q.get(timeout=15.0)
                except queue.Empty:
                    self.wfile.write(b": keepalive\n\n")
                    self.wfile.flush()
                    continue
                if item is None:
                    break
                payload = json.dumps(item, ensure_ascii=False)
                self.wfile.write(f"event: progress\ndata: {payload}\n\n".encode("utf-8"))
                self.wfile.flush()
                if item.get("event") in {"RESULT", "ERROR", "CANCELLED"}:
                    break
        except (BrokenPipeError, ConnectionResetError):
            pass

    def do_POST(self):
        path = self.path.split("?", 1)[0]
        try:
            if path == "/api/research":
                params = _parse_research_body(self)
                pipeline = FiveStepResearchPipeline(WORKSPACE_DIR)
                result = pipeline.execute_deep_research(
                    params["query"], days_back=params["days_back"], depth=params["depth"]
                )
                _json_response(self, 200, result)
                return

            if path == "/api/research/start":
                params = _parse_research_body(self)
                job_id = uuid.uuid4().hex
                job = {
                    "id": job_id,
                    "status": "running",
                    "queue": queue.Queue(),
                    "cancel": threading.Event(),
                    "params": params,
                    "result": None,
                    "error": None,
                    "started": time.time(),
                }
                with _JOBS_LOCK:
                    _JOBS[job_id] = job
                t = threading.Thread(target=_run_pipeline_job, args=(job_id, params), daemon=True)
                t.start()
                _json_response(self, 200, {"job_id": job_id, "status": "running"})
                return

            if path == "/api/research/cancel":
                content_len = int(self.headers.get("Content-Length", 0))
                body = self.rfile.read(content_len).decode("utf-8") if content_len else "{}"
                data = json.loads(body) if body else {}
                job_id = str(data.get("job_id", ""))
                with _JOBS_LOCK:
                    job = _JOBS.get(job_id)
                if not job:
                    _json_response(self, 404, {"error": "unknown job_id"})
                    return
                job["cancel"].set()
                _json_response(self, 200, {"job_id": job_id, "status": "cancel_requested"})
                return

            self.send_error(404, "Endpoint not found")
        except Exception as exc:
            _json_response(self, 500, {"error": str(exc)})

    def do_OPTIONS(self):
        self.send_response(200)
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Methods", "POST, GET, OPTIONS")
        self.send_header("Access-Control-Allow-Headers", "Content-Type")
        self.end_headers()


def run_server(port: int = 8090):
    WORKSPACE_DIR.mkdir(parents=True, exist_ok=True)
    server = ThreadingHTTPServer(("0.0.0.0", port), DeepResearchAPIHandler)
    print(f"[*] Deep Research Agent UI running at http://localhost:{port}/", flush=True)
    print(f"[*] Workspace: {WORKSPACE_DIR}", flush=True)
    server.serve_forever()


if __name__ == "__main__":
    port = int(sys.argv[1]) if len(sys.argv) > 1 else 8090
    run_server(port)
