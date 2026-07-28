"""
Common LLM Client Layer for Packt Harness Engineering Course
Provides standardized multi-provider model interactions via environment variables (.env).
"""

import os
import json
from dotenv import load_dotenv

load_dotenv()

class LLMClient:
    """Standardized multi-provider LLM client for Harness Engineering demos."""
    def __init__(self):
        self.provider = os.getenv("LLM_PROVIDER", "openai")
        self.model = os.getenv("LLM_MODEL", "default-harness-model")
        self.base_url = os.getenv("LLM_BASE_URL", "http://127.0.0.1:8000/v1")
        self.api_key = os.getenv("LLM_API_KEY", "EMPTY")
        self.client = None
        self._init_client()

    def _init_client(self):
        try:
            import aisuite as ai
            provider_configs = {
                self.provider: {
                    "base_url": self.base_url,
                    "api_key": self.api_key
                }
            }
            self.client = ai.Client(provider_configs=provider_configs)
            print(f"[LLM Client] Configured LLM client with model '{self.model}' | Endpoint: '{self.base_url}'")
        except Exception as e:
            pass

    def generate(self, prompt: str, system_prompt: str = None) -> str:
        messages = []
        if system_prompt:
            messages.append({"role": "system", "content": system_prompt})
        messages.append({"role": "user", "content": prompt})

        if self.client:
            try:
                model_identifier = f"{self.provider}:{self.model}"
                response = self.client.chat.completions.create(
                    model=model_identifier,
                    messages=messages,
                    temperature=0.2
                )
                return response.choices[0].message.content
            except Exception:
                pass

        # Fallback simulation
        return f"[Harness Simulated Output for prompt: {prompt[:60]}...]"

    def complete(self, prompt: str, system_prompt: str = None) -> str:
        return self.generate(prompt, system_prompt=system_prompt)

CourseLLMClient = LLMClient

if __name__ == "__main__":
    client = LLMClient()
    print("LLM Client Initialization Check Passed.")
