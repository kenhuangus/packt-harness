"""
Course LLM client, built on Andrew Ng's aisuite
(https://github.com/andrewyng/aisuite).

One API, many providers. Model ids are `provider:model`.

Default is the local OpenAI-compatible vLLM server
(http://127.0.0.1:8000/v1, nvidia/Qwen3.6-35B-A3B-NVFP4).
Switch providers with a gitignored .env, for example:

    LLM_PROVIDER=anthropic
    LLM_MODEL=claude-sonnet-4-5
    ANTHROPIC_API_KEY=

    LLM_PROVIDER=google
    LLM_MODEL=gemini-2.5-flash
    GEMINI_API_KEY=

Gemini uses Google's OpenAI-compatible endpoint
(https://generativelanguage.googleapis.com/v1beta/openai/),
not aisuite's Vertex AI google provider. LLM_PROVIDER=vertex
requires aisuite[google] plus GCP credentials and is not
installed by this course.

Never commit API keys. Simulated text is used only when
HARNESS_ALLOW_SIMULATED_LLM=1.
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
DEFAULT_PROVIDER = "openai"
DEFAULT_LOCAL_MODEL = "nvidia/Qwen3.6-35B-A3B-NVFP4"
DEFAULT_ANTHROPIC_MODEL = "claude-sonnet-4-5"
DEFAULT_OPENAI_MODEL = "gpt-4o-mini"
DEFAULT_GEMINI_MODEL = "gemini-2.5-flash"
DEFAULT_OPENROUTER_MODEL = "openai/gpt-4o-mini"
DEFAULT_OLLAMA_MODEL = "qwen2.5-coder"
GEMINI_OPENAI_BASE = "https://generativelanguage.googleapis.com/v1beta/openai/"
OPENROUTER_BASE = "https://openrouter.ai/api/v1"
OLLAMA_DEFAULT_BASE = "http://127.0.0.1:11434"
GEMINI_PROVIDERS = {"google", "gemini"}
CLAUDE_PROVIDERS = {"anthropic", "claude"}
OPENROUTER_PROVIDERS = {"openrouter", "open_router"}
OLLAMA_PROVIDERS = {"ollama"}
VERTEX_PROVIDERS = {"vertex", "vertexai", "google-vertex"}
KNOWN_PROVIDERS = {
    "openai",
    "anthropic",
    "claude",
    "google",
    "gemini",
    "openrouter",
    "open_router",
    "ollama",
    "vertex",
    "vertexai",
    "mistral",
    "huggingface",
    "aws",
    "azure",
    "cohere",
    "groq",
    "together",
    "fireworks",
    "deepseek",
    "xai",
}


def _allow_simulated() -> bool:
    return os.getenv("HARNESS_ALLOW_SIMULATED_LLM", "").strip().lower() in {
        "1",
        "true",
        "yes",
    }


def _normalize_base(url: str) -> str:
    return url.rstrip("/")


def _is_local_base(url: str) -> bool:
    host = url.lower()
    return "127.0.0.1" in host or "localhost" in host or "0.0.0.0" in host


def _split_model(raw: str | None, default_provider: str) -> tuple[str, str | None]:
    """Accept either `claude-sonnet-4-5` or `anthropic:claude-sonnet-4-5`."""
    if not raw:
        return default_provider, None
    raw = raw.strip()
    if ":" in raw:
        provider, model = raw.split(":", 1)
        if provider.lower() in KNOWN_PROVIDERS:
            return provider.lower(), model
    return default_provider, raw


def _http_json(url: str, timeout: float = 5.0) -> dict:
    request = urllib.request.Request(
        url,
        headers={
            "Authorization": f"Bearer {os.getenv('LLM_API_KEY', os.getenv('OPENAI_API_KEY', 'EMPTY'))}"
        },
    )
    with urllib.request.urlopen(request, timeout=timeout) as response:
        return json.loads(response.read().decode("utf-8"))


class LLMClient:
    """aisuite client supporting OpenAI, OpenRouter, Ollama, Gemini, and Claude."""

    def __init__(self, require_live: bool | None = None) -> None:
        env_provider = os.getenv("LLM_PROVIDER", DEFAULT_PROVIDER).strip().lower()
        self.provider, env_model = _split_model(os.getenv("LLM_MODEL"), env_provider)
        if self.provider in VERTEX_PROVIDERS:
            raise RuntimeError(
                "LLM_PROVIDER=vertex uses aisuite's Vertex AI google provider, "
                "which requires aisuite[google] plus GOOGLE_PROJECT_ID, "
                "GOOGLE_REGION, and GOOGLE_APPLICATION_CREDENTIALS. "
                "This course does not install that extra. For the Gemini API, "
                "set LLM_PROVIDER=google (or gemini) and GEMINI_API_KEY; "
                "the client routes that through Google's OpenAI-compatible "
                f"endpoint ({GEMINI_OPENAI_BASE})."
            )
        if self.provider in CLAUDE_PROVIDERS:
            self.provider = "anthropic"
        elif self.provider in GEMINI_PROVIDERS:
            self.provider = "google"
        elif self.provider in OPENROUTER_PROVIDERS:
            self.provider = "openrouter"
        elif self.provider in OLLAMA_PROVIDERS:
            self.provider = "ollama"

        self.base_url = _normalize_base(os.getenv("LLM_BASE_URL", DEFAULT_BASE_URL))
        if self.provider in GEMINI_PROVIDERS or self.provider == "google":
            env_base = os.getenv("LLM_BASE_URL")
            if not env_base or _is_local_base(env_base):
                self.base_url = _normalize_base(GEMINI_OPENAI_BASE)
        elif self.provider in OPENROUTER_PROVIDERS or self.provider == "openrouter":
            env_base = os.getenv("LLM_BASE_URL")
            if not env_base or _is_local_base(env_base):
                self.base_url = _normalize_base(OPENROUTER_BASE)
        elif self.provider in OLLAMA_PROVIDERS or self.provider == "ollama":
            env_base = os.getenv("LLM_BASE_URL")
            if not env_base:
                self.base_url = _normalize_base(OLLAMA_DEFAULT_BASE)

        self.api_key = (
            os.getenv("LLM_API_KEY")
            or os.getenv("OPENAI_API_KEY")
            or os.getenv("ANTHROPIC_API_KEY")
            or os.getenv("GEMINI_API_KEY")
            or os.getenv("GOOGLE_API_KEY")
            or os.getenv("OPENROUTER_API_KEY")
            or "EMPTY"
        )
        self.require_live = (
            (not _allow_simulated()) if require_live is None else require_live
        )
        self.model = env_model or self._default_model()
        self.live = False
        self.last_error = ""
        self._client = None
        self._init_aisuite()
        self._probe()
        print(
            f"[LLM Client] aisuite provider={self.provider} model={self.model} "
            f"endpoint={self.base_url if self._aisuite_provider() == 'openai' else self.provider} "
            f"live={self.live}"
        )
        if self.require_live and not self.live:
            raise RuntimeError(self._missing_backend_message())

    def _aisuite_provider(self) -> str:
        """Gemini and OpenRouter ride aisuite's openai provider at their respective base URLs."""
        if self.provider in GEMINI_PROVIDERS or self.provider == "google" or self.provider in OPENROUTER_PROVIDERS or self.provider == "openrouter":
            return "openai"
        if self.provider in CLAUDE_PROVIDERS or self.provider == "anthropic":
            return "anthropic"
        if self.provider in OLLAMA_PROVIDERS or self.provider == "ollama":
            return "ollama"
        return self.provider

    def _default_model(self) -> str:
        if self.provider in CLAUDE_PROVIDERS or self.provider == "anthropic":
            return DEFAULT_ANTHROPIC_MODEL
        if self.provider in GEMINI_PROVIDERS or self.provider == "google":
            return DEFAULT_GEMINI_MODEL
        if self.provider in OPENROUTER_PROVIDERS or self.provider == "openrouter":
            return DEFAULT_OPENROUTER_MODEL
        if self.provider in OLLAMA_PROVIDERS or self.provider == "ollama":
            return DEFAULT_OLLAMA_MODEL
        if self.provider == "openai" and _is_local_base(self.base_url):
            return self._discover_local_model() or DEFAULT_LOCAL_MODEL
        return DEFAULT_OPENAI_MODEL

    def _discover_local_model(self) -> str | None:
        try:
            listing = _http_json(f"{self.base_url}/models", timeout=5.0)
        except Exception as exc:
            self.last_error = str(exc)
            return None
        models = listing.get("data") or []
        if not models:
            return None
        return str(models[0].get("id") or "").strip() or None

    def _provider_configs(self) -> dict:
        """Build the aisuite provider map from environment, never hardcoding secrets."""
        configs: dict = {}
        if self.provider == "openai":
            configs["openai"] = {
                "api_key": os.getenv("LLM_API_KEY")
                or os.getenv("OPENAI_API_KEY")
                or "EMPTY",
                "base_url": self.base_url,
            }
        elif self.provider in OPENROUTER_PROVIDERS or self.provider == "openrouter":
            key = (
                os.getenv("OPENROUTER_API_KEY")
                or os.getenv("LLM_API_KEY")
                or ""
            )
            if not key and self.require_live:
                raise RuntimeError(
                    "OPENROUTER_API_KEY is not set. Put it in the gitignored "
                    ".env for OpenRouter access."
                )
            configs["openai"] = {
                "api_key": key or "EMPTY",
                "base_url": self.base_url,
            }
        elif self.provider in CLAUDE_PROVIDERS or self.provider == "anthropic":
            key = os.getenv("ANTHROPIC_API_KEY") or os.getenv("LLM_API_KEY")
            if not key and self.require_live:
                raise RuntimeError(
                    "ANTHROPIC_API_KEY is not set. Put it in the gitignored "
                    ".env for local testing only."
                )
            if key:
                configs["anthropic"] = {"api_key": key}
        elif self.provider in GEMINI_PROVIDERS or self.provider == "google":
            key = (
                os.getenv("GEMINI_API_KEY")
                or os.getenv("GOOGLE_API_KEY")
                or os.getenv("LLM_API_KEY")
                or ""
            )
            if not key and self.require_live:
                raise RuntimeError(
                    "GEMINI_API_KEY is not set. Put it in the gitignored "
                    ".env for local testing only. Gemini uses Google's "
                    "OpenAI-compatible endpoint, not Vertex AI."
                )
            configs["openai"] = {
                "api_key": key or "EMPTY",
                "base_url": self.base_url,
            }
        elif self.provider in OLLAMA_PROVIDERS or self.provider == "ollama":
            configs["ollama"] = {
                "api_url": self.base_url,
            }
        else:
            key = os.getenv("LLM_API_KEY") or os.getenv("OPENAI_API_KEY")
            if key:
                configs[self.provider] = {"api_key": key}
                if os.getenv("LLM_BASE_URL"):
                    configs[self.provider]["base_url"] = self.base_url
        return configs

    def _init_aisuite(self) -> None:
        try:
            import aisuite as ai
        except ImportError as exc:
            self.last_error = "aisuite is not installed. pip install aisuite"
            if self.require_live:
                raise RuntimeError(self.last_error) from exc
            return
        try:
            self._client = ai.Client(self._provider_configs())
        except Exception as exc:
            self.last_error = str(exc)
            if self.require_live:
                raise

    def _probe(self) -> None:
        """Confirm the configured backend is reachable. Do not print secrets."""
        if self.provider == "openai" and _is_local_base(self.base_url):
            try:
                listing = _http_json(f"{self.base_url}/models", timeout=5.0)
                self.live = bool(listing.get("data"))
            except Exception as exc:
                self.live = False
                self.last_error = str(exc)
            return
        if self.provider == "openai":
            key = os.getenv("OPENAI_API_KEY") or os.getenv("LLM_API_KEY") or ""
            self.live = bool(key.strip())
            if not self.live:
                self.last_error = "OPENAI_API_KEY missing"
            return
        if self.provider in OPENROUTER_PROVIDERS or self.provider == "openrouter":
            key = os.getenv("OPENROUTER_API_KEY") or os.getenv("LLM_API_KEY") or ""
            self.live = bool(key.strip())
            if not self.live:
                self.last_error = "OPENROUTER_API_KEY missing"
            return
        if self.provider in CLAUDE_PROVIDERS or self.provider == "anthropic":
            key = os.getenv("ANTHROPIC_API_KEY") or os.getenv("LLM_API_KEY") or ""
            self.live = bool(key.strip())
            if not self.live:
                self.last_error = "ANTHROPIC_API_KEY missing"
            return
        if self.provider in GEMINI_PROVIDERS or self.provider == "google":
            key = (
                os.getenv("GEMINI_API_KEY")
                or os.getenv("GOOGLE_API_KEY")
                or os.getenv("LLM_API_KEY")
                or ""
            )
            self.live = bool(key.strip())
            if not self.live:
                self.last_error = "GEMINI_API_KEY missing"
            return
        if self.provider in OLLAMA_PROVIDERS or self.provider == "ollama":
            try:
                url = f"{self.base_url.rstrip('/')}/api/tags"
                req = urllib.request.Request(url)
                with urllib.request.urlopen(req, timeout=3.0) as resp:
                    self.live = resp.status == 200
            except Exception:
                self.live = bool(self._client is not None)
            return
        if self._client is not None:
            self.live = True

    def _missing_backend_message(self) -> str:
        if self.provider in CLAUDE_PROVIDERS or self.provider == "anthropic":
            return (
                "Claude is selected but ANTHROPIC_API_KEY is not set. "
                "Add it to the gitignored .env for local testing only."
            )
        if self.provider in OPENROUTER_PROVIDERS or self.provider == "openrouter":
            return (
                "OpenRouter is selected but OPENROUTER_API_KEY is not set. "
                "Add it to the gitignored .env."
            )
        if self.provider in GEMINI_PROVIDERS or self.provider == "google":
            return (
                "Gemini is selected but GEMINI_API_KEY (or GOOGLE_API_KEY) "
                "is not set. Add it to the gitignored .env for local testing "
                "only. This client uses Google's OpenAI-compatible endpoint, "
                "not Vertex AI."
            )
        if self.provider in OLLAMA_PROVIDERS or self.provider == "ollama":
            return (
                f"Ollama is selected but not reachable at {self.base_url}. "
                "Make sure Ollama is running (`ollama serve`) or set "
                "HARNESS_ALLOW_SIMULATED_LLM=1."
            )
        if self.provider == "openai" and _is_local_base(self.base_url):
            return (
                "Local model is required but not reachable at "
                f"{self.base_url}. Start vLLM or set "
                "HARNESS_ALLOW_SIMULATED_LLM=1. "
                f"Last error: {self.last_error}"
            )
        if self.provider == "openai":
            return (
                "OpenAI is selected but OPENAI_API_KEY is not set. "
                "Add it to the gitignored .env."
            )
        return f"LLM backend {self.provider}:{self.model} is not live: {self.last_error}"

    def generate(self, prompt: str, system_prompt: str | None = None) -> str:
        messages = []
        if system_prompt:
            messages.append({"role": "system", "content": system_prompt})
        messages.append({"role": "user", "content": prompt})

        if self._client is None:
            if self.require_live:
                raise RuntimeError(
                    f"aisuite client was not created: {self.last_error}"
                )
            return f"[Harness Simulated Output for prompt: {prompt[:60]}...]"

        kwargs: dict = {"temperature": 0.2, "max_tokens": 256}
        # Local Qwen thinking models otherwise return empty content.
        if self.provider == "openai" and _is_local_base(self.base_url):
            kwargs["extra_body"] = {
                "chat_template_kwargs": {"enable_thinking": False}
            }

        try:
            response = self._client.chat.completions.create(
                model=f"{self._aisuite_provider()}:{self.model}",
                messages=messages,
                **kwargs,
            )
            message = response.choices[0].message
            text = (getattr(message, "content", None) or "").strip()
            if not text:
                text = (getattr(message, "reasoning", None) or "").strip()
            if text:
                return text
            self.last_error = "empty model content"
        except Exception as exc:
            self.last_error = str(exc)

        if self.require_live:
            raise RuntimeError(
                f"aisuite call failed provider={self.provider} "
                f"model={self.model}: {self.last_error}"
            )
        return f"[Harness Simulated Output for prompt: {prompt[:60]}...]"

    def complete(self, prompt: str, system_prompt: str | None = None) -> str:
        return self.generate(prompt, system_prompt=system_prompt)


CourseLLMClient = LLMClient


def ping_local_model() -> str:
    """Suite preflight. Hits whatever backend .env selected (local by default)."""
    client = LLMClient(require_live=True)
    return client.complete("Reply with exactly: harness-ok")


if __name__ == "__main__":
    reply = ping_local_model()
    print(f"LIVE_REPLY={reply!r}")
    if not reply.strip():
        raise SystemExit("Configured model returned an empty reply.")
    print("LLM Client live check passed.")
