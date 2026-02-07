"""Pydantic schemas for LLM provider settings."""

from typing import List, Optional
from pydantic import BaseModel, Field


class LLMSettingsUpdate(BaseModel):
    """Schema for updating LLM settings."""
    provider: str = Field(..., description="Provider ID: anthropic, openai, google, groq, openrouter, ollama")
    model: str = Field(..., description="Model name to use")
    api_key: Optional[str] = Field(None, description="API key (None = keep existing)")
    base_url: Optional[str] = Field(None, description="Custom base URL (for Ollama)")


class LLMSettingsResponse(BaseModel):
    """Schema for returning LLM settings (API key masked)."""
    provider: str
    model: str
    api_key_set: bool = False
    base_url: Optional[str] = None
    is_configured: bool = False
    configured_at: Optional[str] = None
    configured_by: Optional[str] = None
    source: str = "default"  # "database", "env", "default"


class LLMProviderInfo(BaseModel):
    """Schema for provider information."""
    id: str
    name: str
    models: List[str]
    requires_api_key: bool
    default_base_url: Optional[str] = None


class LLMTestRequest(BaseModel):
    """Schema for testing LLM connection."""
    provider: str
    model: str
    api_key: Optional[str] = None
    base_url: Optional[str] = None


class LLMTestResult(BaseModel):
    """Schema for LLM test result."""
    success: bool
    message: str
    response_preview: Optional[str] = None
