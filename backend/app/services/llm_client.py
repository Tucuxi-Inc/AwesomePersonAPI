"""LLM Client wrapper with multi-provider support.

Resolution order:
1. Per-request org settings (from contextvars, set by middleware)
2. .env file settings (LLM_PROVIDER, LLM_MODEL, etc.)
3. Hardcoded default: Anthropic with ANTHROPIC_API_KEY
"""

import logging
from typing import Any, Dict, Optional

from app.config import settings
from app.core.llm_context import get_llm_config
from app.services.llm_providers import create_provider, PROVIDER_CONFIGS

logger = logging.getLogger(__name__)

# Map provider names to their .env API key setting names
_PROVIDER_ENV_KEYS = {
    "anthropic": "ANTHROPIC_API_KEY",
    "openai": "OPENAI_API_KEY",
    "google": "GOOGLE_API_KEY",
    "groq": "GROQ_API_KEY",
    "openrouter": "OPENROUTER_API_KEY",
    "ollama": None,  # No key needed
}


def _resolve_config() -> Dict[str, Any]:
    """Resolve the LLM configuration from contextvar → .env → default."""
    # 1. Check contextvar (per-request org settings from DB)
    ctx_config = get_llm_config()
    if ctx_config and ctx_config.get("provider"):
        return ctx_config

    # 2. Check .env settings
    env_provider = settings.LLM_PROVIDER
    env_model = settings.LLM_MODEL

    if env_provider and env_provider != "anthropic":
        # Non-default provider set in .env
        env_key_attr = _PROVIDER_ENV_KEYS.get(env_provider)
        api_key = getattr(settings, env_key_attr, "") if env_key_attr else ""
        base_url = None
        if env_provider == "ollama":
            base_url = settings.OLLAMA_BASE_URL

        return {
            "provider": env_provider,
            "model": env_model or "",
            "api_key": api_key,
            "base_url": base_url,
        }

    # 3. Default: Anthropic
    return {
        "provider": "anthropic",
        "model": env_model or "claude-sonnet-4-20250514",
        "api_key": settings.ANTHROPIC_API_KEY,
        "base_url": None,
    }


class LLMClient:
    """Multi-provider LLM client. Resolves provider per-request via contextvars."""

    def __init__(self, api_key: Optional[str] = None):
        # Keep backward compat: if explicit api_key passed, use it for Anthropic
        self._explicit_api_key = api_key

    def _get_provider(self):
        """Get the current provider based on config resolution."""
        if self._explicit_api_key:
            # Explicit key = always Anthropic (backward compat for direct instantiation)
            return create_provider("anthropic", api_key=self._explicit_api_key)

        config = _resolve_config()
        return create_provider(
            provider_name=config["provider"],
            api_key=config.get("api_key", ""),
            model=config.get("model", ""),
            base_url=config.get("base_url"),
        )

    async def complete(
        self,
        prompt: str,
        system_prompt: Optional[str] = None,
        response_format: str = "text",
        max_tokens: int = 4096,
        temperature: float = 0.7,
    ) -> Any:
        """Generate a completion using the resolved provider."""
        provider = self._get_provider()
        return await provider.complete(
            prompt=prompt,
            system_prompt=system_prompt,
            response_format=response_format,
            max_tokens=max_tokens,
            temperature=temperature,
        )

    async def complete_structured(
        self,
        prompt: str,
        system_prompt: Optional[str] = None,
        output_schema: Optional[Dict[str, Any]] = None,
        max_tokens: int = 4096,
    ) -> Dict[str, Any]:
        """Generate a structured JSON completion using the resolved provider."""
        provider = self._get_provider()
        return await provider.complete_structured(
            prompt=prompt,
            system_prompt=system_prompt,
            output_schema=output_schema,
            max_tokens=max_tokens,
        )


# Singleton instance
llm_client = LLMClient()


def get_llm_client() -> LLMClient:
    """Get the LLM client instance."""
    return llm_client
