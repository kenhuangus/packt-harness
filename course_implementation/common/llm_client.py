"""
Local-first LLM client for the Packt harness course.

Tests talk to an OpenAI-compatible server on this machine (default
http://127.0.0.1:8000/v1, the vLLM Qwen endpoint). They do not call
paid cloud APIs. Simulated text is used only when
HARNESS_ALLOW_SIMULATED_LLM=1 is set.
"""

from __future__ import annotations

import json
import os
from pathlib import Path
import urllib.error
import urllib.request

from dotenv import load_dotenv


def _load_env_files() -> None:
    here = Path(__file__).resolve()
    for candidate in (
        here.parents[2] / ".env",
        here.parents[1] / ".env",
        here.parent / ".env",
    ):
        if candidate.is_file():
            load_dotenv(candidate, override=False)
    load_dotenv(override=False)


_load_env_files()

DEFAULT_BASE_URL = "http://127.0.0.1:8000/v1"
DEFAULT_MODEL = "nvidia/Qwen3.6-35B-A3B-NVFP4"


def _allow_simulated() -> bool:
    return os.getenv("HARNESS_ALLOW_SIMULATED_LLM", "").strip() in {
        "1",
        "true",
        "TRUE",
        "yes",
    }


def _normalize_base(url: str) -> str:
    return url.rstrip("/")


def _http_json(url: str, payload: dict | None = None, timeout: float = 120.0) -> dict:
    headers = {
        "Authorization": f"Bearer {os.getenv('LLM_API_KEY', 'EMPTY')}",
    }
    data = None
    if payload is not None:
        headers["Content-Type"] = "application/json"
        data = json.dumps(payload).encode("utf-8")
    request = urllib.request.Request(url, data=data, headers=headers)
    with urllib.request.urlopen(request, timeout=timeout) as response:
        return json.loads(response.read().decode("utf-8"))


class LLMClient:
    """OpenAI-compatible client pinned to a local endpoint."""

    def __init__(self, require_live: bool | None = None) -> None:
        self.provider = os.getenv("LLM_PROVIDER", "openai")
        self.base_url = _normalize_base(os.getenv("LLM_BASE_URL", DEFAULT_BASE_URL))
        self.api_key = os.getenv("LLM_API_KEY", "EMPTY")
        self.require_live = (not _allow_simulated()) if require_live is None else require_live
        self.model = os.getenv("LLM_MODEL") or self._discover_model() or DEFAULT_MODEL
        self.live = False
        self.last_error = ""
        self._probe()
        print(
            f"[LLM Client] Configured local model '{self.model}' | "
            f"Endpoint: '{self.base_url}' | live={self.live}"
        )
        if self.require_live and not self.live:
            raise RuntimeError(
                "Local model is required but not reachable at "
                f"{self.base_url}. Start vLLM/Ollama locally or set "
                "HARNESS_ALLOW_SIMULATED_LLM=1. "
                f"Last error: {self.last_error}"
            )

    def _discover_model(self) -> str | None:
        try:
            listing = _http_json(f"{self.base_url}/models", timeout=5.0)
        except Exception as exc:
            self.last_error = str(exc)
            return None
        models = listing.get("data") or []
        if not models:
            return None
        return str(models[0].get("id") or "").strip() or None

    def _probe(self) -> None:
        try:
            listing = _http_json(f"{self.base_url}/models", timeout=5.0)
            ids = [item.get("id") for item in listing.get("data") or []]
            self.live = bool(ids)
            if ids and self.model not in ids:
                # Keep the configured name if the server is up; some
                # routers accept aliases that /models does not list.
                self.live = True
        except Exception as exc:
            self.live = False
            self.last_error = str(exc)

    def generate(self, prompt: str, system_prompt: str | None = None) -> str:
        messages = []
        if system_prompt:
            messages.append({"role": "system", "content": system_prompt})
        messages.append({"role": "user", "content": prompt})

        payload = {
            "model": self.model,
            "messages": messages,
            "temperature": 0.2,
            "max_tokens": 256,
            "chat_template_kwargs": {"enable_thinking": False},
        }
        try:
            body = _http_json(
                f"{self.base_url}/chat/completions",
                payload=payload,
                timeout=180.0,
            )
            message = body["choices"][0]["message"]
            text = (message.get("content") or message.get("reasoning") or "").strip()
            if text:
                return text
            self.last_error = "empty model content"
        except (urllib.error.URLError, urllib.error.HTTPError, KeyError, IndexError, TimeoutError) as exc:
            self.last_error = str(exc)

        if self.require_live:
            raise RuntimeError(
                f"Local model call failed at {self.base_url} "
                f"model={self.model}: {self.last_error}"
            )
        return f"[Harness Simulated Output for prompt: {prompt[:60]}...]"

    def complete(self, prompt: str, system_prompt: str | None = None) -> str:
        return self.generate(prompt, system_prompt=system_prompt)


CourseLLMClient = LLMClient


def ping_local_model() -> str:
    """Used by the suite preflight. Must return a live non-empty string."""
    client = LLMClient(require_live=True)
    return client.complete("Reply with exactly: harness-ok")


if __name__ == "__main__":
    reply = ping_local_model()
    print(f"LIVE_REPLY={reply!r}")
    if "harness-ok" not in reply.lower() and not reply.strip():
        raise SystemExit("Local model returned an empty reply.")
    print("LLM Client live local-model check passed.")
