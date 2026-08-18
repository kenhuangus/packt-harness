"""
Unit Tests for Multi-Provider aisuite LLM Clients.
Verifies support for OpenAI, OpenRouter, Ollama, Google Gemini, and Anthropic Claude.
"""

import os
from unittest.mock import patch
import pytest

from course_implementation.common.llm_client import (
    LLMClient,
    DEFAULT_ANTHROPIC_MODEL,
    DEFAULT_GEMINI_MODEL,
    DEFAULT_OPENROUTER_MODEL,
    DEFAULT_OLLAMA_MODEL,
    GEMINI_OPENAI_BASE,
    OPENROUTER_BASE,
    OLLAMA_DEFAULT_BASE,
)
from deep_research_agent.engine.llm_client import ResearchLLMClient


def test_openai_provider_config():
    """Verify OpenAI configuration defaults and local base URL."""
    with patch.dict(os.environ, {
        "LLM_PROVIDER": "openai",
        "LLM_MODEL": "gpt-4o-mini",
        "OPENAI_API_KEY": "sk-mock-openai-key",
        "LLM_BASE_URL": "https://api.openai.com/v1",
        "HARNESS_ALLOW_SIMULATED_LLM": "1",
    }, clear=True):
        client = LLMClient(require_live=False)
        assert client.provider == "openai"
        assert client.model == "gpt-4o-mini"
        assert client._aisuite_provider() == "openai"
        configs = client._provider_configs()
        assert "openai" in configs
        assert configs["openai"]["api_key"] == "sk-mock-openai-key"


def test_openrouter_provider_config():
    """Verify OpenRouter provider routing, base URL, and model defaults."""
    with patch.dict(os.environ, {
        "LLM_PROVIDER": "openrouter",
        "OPENROUTER_API_KEY": "sk-or-v1-mock-key",
        "HARNESS_ALLOW_SIMULATED_LLM": "1",
    }, clear=True):
        client = LLMClient(require_live=False)
        assert client.provider == "openrouter"
        assert client.model == DEFAULT_OPENROUTER_MODEL
        assert client.base_url == OPENROUTER_BASE
        assert client._aisuite_provider() == "openai"
        configs = client._provider_configs()
        assert configs["openai"]["api_key"] == "sk-or-v1-mock-key"
        assert configs["openai"]["base_url"] == OPENROUTER_BASE


def test_ollama_provider_config():
    """Verify Ollama provider config and base URL."""
    with patch.dict(os.environ, {
        "LLM_PROVIDER": "ollama",
        "LLM_MODEL": "llama3",
        "LLM_BASE_URL": "http://127.0.0.1:11434",
        "HARNESS_ALLOW_SIMULATED_LLM": "1",
    }, clear=True):
        client = LLMClient(require_live=False)
        assert client.provider == "ollama"
        assert client.model == "llama3"
        assert client._aisuite_provider() == "ollama"
        configs = client._provider_configs()
        assert configs["ollama"]["api_url"] == "http://127.0.0.1:11434"


def test_gemini_provider_config():
    """Verify Google / Gemini provider routing via OpenAI-compatible endpoint."""
    with patch.dict(os.environ, {
        "LLM_PROVIDER": "gemini",
        "GEMINI_API_KEY": "AIzaSyMockKey",
        "HARNESS_ALLOW_SIMULATED_LLM": "1",
    }, clear=True):
        client = LLMClient(require_live=False)
        assert client.provider == "google"
        assert client.model == DEFAULT_GEMINI_MODEL
        assert client.base_url == GEMINI_OPENAI_BASE.rstrip("/")
        assert client._aisuite_provider() == "openai"
        configs = client._provider_configs()
        assert configs["openai"]["api_key"] == "AIzaSyMockKey"
        assert configs["openai"]["base_url"] == GEMINI_OPENAI_BASE.rstrip("/")


def test_claude_anthropic_provider_config():
    """Verify Anthropic / Claude provider config and normalization."""
    with patch.dict(os.environ, {
        "LLM_PROVIDER": "claude",
        "ANTHROPIC_API_KEY": "sk-ant-mock-key",
        "HARNESS_ALLOW_SIMULATED_LLM": "1",
    }, clear=True):
        client = LLMClient(require_live=False)
        assert client.provider == "anthropic"
        assert client.model == DEFAULT_ANTHROPIC_MODEL
        assert client._aisuite_provider() == "anthropic"
        configs = client._provider_configs()
        assert configs["anthropic"]["api_key"] == "sk-ant-mock-key"


def test_deep_research_llm_client_providers():
    """Verify ResearchLLMClient across all 5 providers."""
    # OpenRouter
    with patch.dict(os.environ, {
        "OPENROUTER_API_KEY": "sk-or-test-key",
        "HARNESS_ALLOW_SIMULATED_LLM": "1",
    }, clear=True):
        r_client = ResearchLLMClient(require_live=False)
        assert r_client.provider == "openrouter"
        assert r_client.base_url == OPENROUTER_BASE

    # Ollama
    with patch.dict(os.environ, {
        "LLM_PROVIDER": "ollama",
        "HARNESS_ALLOW_SIMULATED_LLM": "1",
    }, clear=True):
        r_client = ResearchLLMClient(require_live=False)
        assert r_client.provider == "ollama"
        assert r_client.base_url == OLLAMA_DEFAULT_BASE

    # Claude
    with patch.dict(os.environ, {
        "ANTHROPIC_API_KEY": "sk-ant-test",
        "HARNESS_ALLOW_SIMULATED_LLM": "1",
    }, clear=True):
        r_client = ResearchLLMClient(require_live=False)
        assert r_client.provider == "anthropic"

    # Gemini
    with patch.dict(os.environ, {
        "GEMINI_API_KEY": "AIzaSy-test",
        "HARNESS_ALLOW_SIMULATED_LLM": "1",
    }, clear=True):
        r_client = ResearchLLMClient(require_live=False)
        assert r_client.provider == "google"
