"""LLM Client wrapper for Anthropic Claude API."""

from typing import Any, Dict, Optional
import json

from app.config import settings


class LLMClient:
    """Wrapper for Anthropic Claude API for interview and assessment tasks."""

    def __init__(self, api_key: Optional[str] = None):
        self.api_key = api_key or settings.ANTHROPIC_API_KEY
        self._client = None

    @property
    def client(self):
        """Lazy-load the Anthropic client."""
        if self._client is None:
            try:
                import anthropic
                self._client = anthropic.Anthropic(api_key=self.api_key)
            except ImportError:
                raise ImportError("anthropic package not installed")
        return self._client

    async def complete(
        self,
        prompt: str,
        system_prompt: Optional[str] = None,
        response_format: str = "text",
        max_tokens: int = 4096,
        temperature: float = 0.7,
    ) -> Any:
        """
        Generate a completion using Claude.

        Args:
            prompt: The user prompt
            system_prompt: Optional system prompt
            response_format: "text" or "json"
            max_tokens: Maximum tokens in response
            temperature: Sampling temperature

        Returns:
            The response content (parsed JSON if response_format="json")
        """
        messages = [{"role": "user", "content": prompt}]

        # Build request
        kwargs: Dict[str, Any] = {
            "model": "claude-sonnet-4-20250514",
            "max_tokens": max_tokens,
            "temperature": temperature,
            "messages": messages,
        }

        if system_prompt:
            kwargs["system"] = system_prompt

        # Make request (synchronous client used with async wrapper)
        response = self.client.messages.create(**kwargs)

        # Extract content
        content = response.content[0].text

        # Parse JSON if requested
        if response_format == "json":
            # Handle potential markdown code blocks
            if content.startswith("```"):
                content = content.split("```")[1]
                if content.startswith("json"):
                    content = content[4:]
            content = content.strip()
            return json.loads(content)

        return content

    async def complete_structured(
        self,
        prompt: str,
        system_prompt: Optional[str] = None,
        output_schema: Optional[Dict[str, Any]] = None,
        max_tokens: int = 4096,
    ) -> Dict[str, Any]:
        """
        Generate a structured JSON completion.

        Args:
            prompt: The user prompt
            system_prompt: Optional system prompt
            output_schema: Expected JSON schema (for validation)
            max_tokens: Maximum tokens in response

        Returns:
            Parsed JSON response
        """
        # Add JSON instruction to prompt
        json_prompt = f"""{prompt}

Respond with valid JSON only. No markdown formatting, no explanation - just the JSON object."""

        result = await self.complete(
            prompt=json_prompt,
            system_prompt=system_prompt,
            response_format="json",
            max_tokens=max_tokens,
            temperature=0.5,  # Lower temperature for structured output
        )

        return result


# Singleton instance
llm_client = LLMClient()


def get_llm_client() -> LLMClient:
    """Get the LLM client instance."""
    return llm_client
