"""LLM Provider abstraction layer.

Supports Anthropic, OpenAI, Google AI, Groq, OpenRouter, and Ollama.
All providers expose the same interface: complete() and complete_structured().
"""

import json
import logging
from typing import Any, Dict, List, Optional

import httpx

logger = logging.getLogger(__name__)


# Provider configurations — models populated dynamically via fetch_models()
PROVIDER_CONFIGS: Dict[str, Dict[str, Any]] = {
    "anthropic": {
        "name": "Anthropic",
        "models": [],  # Fetched via API
        "requires_api_key": True,
        "default_base_url": None,
    },
    "openai": {
        "name": "OpenAI",
        "models": [],  # Fetched via API
        "requires_api_key": True,
        "default_base_url": "https://api.openai.com/v1",
    },
    "google": {
        "name": "Google AI",
        "models": [],  # Fetched via API
        "requires_api_key": True,
        "default_base_url": None,
    },
    "groq": {
        "name": "Groq",
        "models": [],  # Fetched via API (OpenAI-compatible)
        "requires_api_key": True,
        "default_base_url": "https://api.groq.com/openai/v1",
    },
    "openrouter": {
        "name": "OpenRouter",
        "models": [],  # Fetched via API
        "requires_api_key": True,
        "default_base_url": "https://openrouter.ai/api/v1",
    },
    "ollama": {
        "name": "Ollama (Local)",
        "models": [],  # Fetched from local Ollama instance
        "requires_api_key": False,
        "default_base_url": "http://ollama:11434/v1",
    },
}


def fetch_models(provider_name: str, api_key: str = "", base_url: Optional[str] = None) -> List[str]:
    """Fetch available models from a provider's API.

    For cloud providers, requires an API key.
    For Ollama, queries the local instance.
    """
    try:
        if provider_name == "ollama":
            url = base_url or "http://ollama:11434"
            # Strip /v1 if present — Ollama native API doesn't use it
            url = url.rstrip("/").removesuffix("/v1")
            return _fetch_ollama_models(url)

        elif provider_name == "anthropic":
            return _fetch_anthropic_models(api_key)

        elif provider_name == "google":
            return _fetch_google_models(api_key)

        elif provider_name in ("openai", "groq", "openrouter"):
            config = PROVIDER_CONFIGS.get(provider_name, {})
            effective_url = base_url or config.get("default_base_url", "")
            return _fetch_openai_compatible_models(api_key, effective_url, provider_name)

    except Exception as e:
        logger.warning(f"Failed to fetch models for {provider_name}: {e}")

    return []


def _fetch_anthropic_models(api_key: str) -> List[str]:
    """Fetch available models from Anthropic API."""
    if not api_key:
        return []
    try:
        response = httpx.get(
            "https://api.anthropic.com/v1/models",
            headers={
                "x-api-key": api_key,
                "anthropic-version": "2023-06-01",
            },
            timeout=5.0,
        )
        if response.status_code == 200:
            data = response.json()
            models = [m["id"] for m in data.get("data", [])]
            return sorted(models)
    except Exception as e:
        logger.debug(f"Could not fetch Anthropic models: {e}")
    return []


def _fetch_openai_compatible_models(api_key: str, base_url: str, provider_name: str = "") -> List[str]:
    """Fetch models from OpenAI-compatible API (OpenAI, Groq, OpenRouter)."""
    if not api_key:
        return []
    try:
        headers = {"Authorization": f"Bearer {api_key}"}
        response = httpx.get(
            f"{base_url.rstrip('/')}/models",
            headers=headers,
            timeout=5.0,
        )
        if response.status_code == 200:
            data = response.json()
            models = [m["id"] for m in data.get("data", [])]
            return sorted(models)
    except Exception as e:
        logger.debug(f"Could not fetch models from {provider_name or base_url}: {e}")
    return []


def _fetch_google_models(api_key: str) -> List[str]:
    """Fetch available Gemini models from Google AI API."""
    if not api_key:
        return []
    try:
        response = httpx.get(
            f"https://generativelanguage.googleapis.com/v1beta/models?key={api_key}",
            timeout=5.0,
        )
        if response.status_code == 200:
            data = response.json()
            models = []
            for m in data.get("models", []):
                name = m.get("name", "")
                # Google returns "models/gemini-..." — strip the prefix
                if name.startswith("models/"):
                    name = name[7:]
                # Only include generative models
                if "generateContent" in m.get("supportedGenerationMethods", []):
                    models.append(name)
            return sorted(models)
    except Exception as e:
        logger.debug(f"Could not fetch Google AI models: {e}")
    return []


def _fetch_ollama_models(base_url: str = "http://ollama:11434") -> List[str]:
    """Fetch available models from an Ollama instance.

    Tries the configured URL first, then falls back to common alternatives
    (Docker service name, host.docker.internal, localhost).
    """
    urls_to_try = [base_url]
    # Add fallback URLs if not already in the list
    for fallback in [
        "http://ollama:11434",
        "http://host.docker.internal:11434",
        "http://localhost:11434",
    ]:
        if fallback not in urls_to_try:
            urls_to_try.append(fallback)

    for url in urls_to_try:
        try:
            response = httpx.get(f"{url}/api/tags", timeout=3.0)
            if response.status_code == 200:
                data = response.json()
                models = [m["name"] for m in data.get("models", [])]
                if models:
                    return sorted(models)
        except Exception:
            continue

    logger.debug(f"Could not fetch Ollama models from any URL: {urls_to_try}")
    return []


def get_provider_list(ollama_base_url: Optional[str] = None) -> List[Dict[str, Any]]:
    """Return list of available providers for the frontend.

    For Ollama, dynamically fetches available models from the running instance.
    """
    from app.config import settings

    result = []
    for provider_id, config in PROVIDER_CONFIGS.items():
        entry = {
            "id": provider_id,
            "name": config["name"],
            "models": config["models"],
            "requires_api_key": config["requires_api_key"],
            "default_base_url": config.get("default_base_url"),
        }
        if provider_id == "ollama":
            url = ollama_base_url or settings.OLLAMA_BASE_URL or "http://ollama:11434"
            entry["models"] = _fetch_ollama_models(url)
        result.append(entry)
    return result


def _parse_json_response(content: str) -> Any:
    """Parse JSON from LLM response, handling markdown code blocks."""
    text = content.strip()
    if text.startswith("```"):
        text = text.split("```")[1]
        if text.startswith("json"):
            text = text[4:]
    text = text.strip()
    return json.loads(text)


class AnthropicProvider:
    """Provider for Anthropic Claude models."""

    def __init__(self, api_key: str, model: str = "claude-sonnet-4-20250514"):
        self.api_key = api_key
        self.model = model
        self._client = None

    @property
    def client(self):
        if self._client is None:
            import anthropic
            self._client = anthropic.Anthropic(api_key=self.api_key)
        return self._client

    async def complete(
        self,
        prompt: str,
        system_prompt: Optional[str] = None,
        response_format: str = "text",
        max_tokens: int = 4096,
        temperature: float = 0.7,
    ) -> Any:
        messages = [{"role": "user", "content": prompt}]
        kwargs: Dict[str, Any] = {
            "model": self.model,
            "max_tokens": max_tokens,
            "temperature": temperature,
            "messages": messages,
        }
        if system_prompt:
            kwargs["system"] = system_prompt

        response = self.client.messages.create(**kwargs)
        content = response.content[0].text

        if response_format == "json":
            return _parse_json_response(content)
        return content

    async def complete_structured(
        self,
        prompt: str,
        system_prompt: Optional[str] = None,
        output_schema: Optional[Dict[str, Any]] = None,
        max_tokens: int = 4096,
    ) -> Dict[str, Any]:
        json_prompt = f"""{prompt}

Respond with valid JSON only. No markdown formatting, no explanation - just the JSON object."""
        return await self.complete(
            prompt=json_prompt,
            system_prompt=system_prompt,
            response_format="json",
            max_tokens=max_tokens,
            temperature=0.5,
        )


class OpenAICompatibleProvider:
    """Provider for OpenAI, Groq, OpenRouter, and Ollama (all use OpenAI chat completions API)."""

    def __init__(self, api_key: str, model: str, base_url: str):
        self.api_key = api_key
        self.model = model
        self.base_url = base_url
        self._client = None

    @property
    def client(self):
        if self._client is None:
            from openai import OpenAI
            self._client = OpenAI(
                api_key=self.api_key or "ollama",  # Ollama doesn't need a key
                base_url=self.base_url,
            )
        return self._client

    async def complete(
        self,
        prompt: str,
        system_prompt: Optional[str] = None,
        response_format: str = "text",
        max_tokens: int = 4096,
        temperature: float = 0.7,
    ) -> Any:
        messages = []
        if system_prompt:
            messages.append({"role": "system", "content": system_prompt})
        messages.append({"role": "user", "content": prompt})

        kwargs: Dict[str, Any] = {
            "model": self.model,
            "max_tokens": max_tokens,
            "temperature": temperature,
            "messages": messages,
        }

        if response_format == "json":
            kwargs["response_format"] = {"type": "json_object"}

        response = self.client.chat.completions.create(**kwargs)
        content = response.choices[0].message.content

        if response_format == "json":
            return _parse_json_response(content)
        return content

    async def complete_structured(
        self,
        prompt: str,
        system_prompt: Optional[str] = None,
        output_schema: Optional[Dict[str, Any]] = None,
        max_tokens: int = 4096,
    ) -> Dict[str, Any]:
        json_prompt = f"""{prompt}

Respond with valid JSON only. No markdown formatting, no explanation - just the JSON object."""
        return await self.complete(
            prompt=json_prompt,
            system_prompt=system_prompt,
            response_format="json",
            max_tokens=max_tokens,
            temperature=0.5,
        )


class GoogleProvider:
    """Provider for Google AI (Gemini) models."""

    def __init__(self, api_key: str, model: str = "gemini-2.0-flash"):
        self.api_key = api_key
        self.model = model
        self._client = None

    def _get_model(self):
        if self._client is None:
            import google.generativeai as genai
            genai.configure(api_key=self.api_key)
            self._client = genai.GenerativeModel(self.model)
        return self._client

    async def complete(
        self,
        prompt: str,
        system_prompt: Optional[str] = None,
        response_format: str = "text",
        max_tokens: int = 4096,
        temperature: float = 0.7,
    ) -> Any:
        import google.generativeai as genai

        model = self._get_model()
        generation_config = genai.GenerationConfig(
            max_output_tokens=max_tokens,
            temperature=temperature,
        )
        if response_format == "json":
            generation_config.response_mime_type = "application/json"

        full_prompt = prompt
        if system_prompt:
            full_prompt = f"{system_prompt}\n\n{prompt}"

        response = model.generate_content(
            full_prompt,
            generation_config=generation_config,
        )
        content = response.text

        if response_format == "json":
            return _parse_json_response(content)
        return content

    async def complete_structured(
        self,
        prompt: str,
        system_prompt: Optional[str] = None,
        output_schema: Optional[Dict[str, Any]] = None,
        max_tokens: int = 4096,
    ) -> Dict[str, Any]:
        json_prompt = f"""{prompt}

Respond with valid JSON only. No markdown formatting, no explanation - just the JSON object."""
        return await self.complete(
            prompt=json_prompt,
            system_prompt=system_prompt,
            response_format="json",
            max_tokens=max_tokens,
            temperature=0.5,
        )


def create_provider(
    provider_name: str,
    api_key: str = "",
    model: str = "",
    base_url: Optional[str] = None,
):
    """Factory function to create the appropriate provider instance."""
    config = PROVIDER_CONFIGS.get(provider_name)
    if not config:
        raise ValueError(f"Unknown provider: {provider_name}")

    # Use first model as default if not specified
    if not model and config["models"]:
        model = config["models"][0]

    if provider_name == "anthropic":
        return AnthropicProvider(api_key=api_key, model=model)

    elif provider_name == "google":
        return GoogleProvider(api_key=api_key, model=model)

    elif provider_name in ("openai", "groq", "openrouter", "ollama"):
        effective_base_url = base_url or config.get("default_base_url", "")
        # For Ollama, ensure the base_url has /v1 suffix for OpenAI-compatible API
        if provider_name == "ollama" and effective_base_url and not effective_base_url.endswith("/v1"):
            effective_base_url = effective_base_url.rstrip("/") + "/v1"
        return OpenAICompatibleProvider(
            api_key=api_key,
            model=model,
            base_url=effective_base_url,
        )

    raise ValueError(f"No provider implementation for: {provider_name}")
