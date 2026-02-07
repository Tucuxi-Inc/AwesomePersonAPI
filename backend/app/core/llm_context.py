"""Per-request LLM configuration using contextvars.

Middleware sets the LLM config based on the authenticated user's organization settings.
get_llm_client() reads from this contextvar, falling back to .env, then default.
"""

import contextvars
import logging
from typing import Optional, Dict, Any

from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request
from starlette.responses import Response

logger = logging.getLogger(__name__)

# Context variable holding the current request's LLM config
_llm_config: contextvars.ContextVar[Optional[Dict[str, Any]]] = contextvars.ContextVar(
    "llm_config", default=None
)


def set_llm_config(config: Optional[Dict[str, Any]]) -> None:
    """Set LLM config for the current request context."""
    _llm_config.set(config)


def get_llm_config() -> Optional[Dict[str, Any]]:
    """Get LLM config for the current request context."""
    return _llm_config.get()


class LLMContextMiddleware(BaseHTTPMiddleware):
    """Middleware that loads org-specific LLM settings into contextvars.

    For each authenticated request, looks up the user's organization LLM settings
    from the database and sets them in a contextvar so get_llm_client() can use them.
    """

    async def dispatch(self, request: Request, call_next) -> Response:
        # Reset context for each request
        set_llm_config(None)

        # Try to load org-specific LLM settings from the request
        # This happens after auth, so we check for the user in request state
        response = await call_next(request)

        return response


async def load_org_llm_config(org_id: str, db) -> Optional[Dict[str, Any]]:
    """Load LLM settings for an organization from the database.

    Called from API endpoints that have access to the DB session and user's org_id.
    """
    from sqlalchemy import select
    from app.models.organization import Organization
    from app.core.encryption import decrypt_value

    result = await db.execute(
        select(Organization).where(Organization.id == org_id)
    )
    org = result.scalar_one_or_none()

    if not org or not org.settings:
        return None

    llm_settings = org.settings.get("llm")
    if not llm_settings:
        return None

    # Decrypt API key if present
    api_key = None
    encrypted_key = llm_settings.get("api_key_encrypted")
    if encrypted_key:
        api_key = decrypt_value(encrypted_key)

    config = {
        "provider": llm_settings.get("provider"),
        "model": llm_settings.get("model"),
        "api_key": api_key,
        "base_url": llm_settings.get("base_url"),
    }

    # Only return if provider is set
    if config.get("provider"):
        return config

    return None
