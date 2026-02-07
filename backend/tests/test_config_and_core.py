"""
Tests for config, encryption, and security modules — targeting quick-win coverage gaps.
"""

import pytest
from datetime import timedelta
from unittest.mock import patch, MagicMock


# ── Config Tests ──────────────────────────────────────────────────────────────


class TestSettingsCorsOrigins:
    """Tests for Settings.cors_origins_list property."""

    def test_single_origin(self):
        from app.config import Settings
        s = Settings(CORS_ORIGINS="http://localhost:3003")
        assert s.cors_origins_list == ["http://localhost:3003"]

    def test_multiple_origins(self):
        from app.config import Settings
        s = Settings(CORS_ORIGINS="http://localhost:3003,http://localhost:3004")
        assert s.cors_origins_list == ["http://localhost:3003", "http://localhost:3004"]

    def test_origins_with_whitespace(self):
        from app.config import Settings
        s = Settings(CORS_ORIGINS="http://a.com , http://b.com , http://c.com")
        assert s.cors_origins_list == ["http://a.com", "http://b.com", "http://c.com"]


class TestSettingsSmtpConfigured:
    """Tests for Settings.smtp_configured property."""

    def test_configured_with_host(self):
        from app.config import Settings
        s = Settings(SMTP_HOST="mailpit")
        assert s.smtp_configured is True

    def test_not_configured_empty_host(self):
        from app.config import Settings
        s = Settings(SMTP_HOST="")
        assert s.smtp_configured is False


# ── Encryption Tests ──────────────────────────────────────────────────────────


class TestDecryptionEdgeCases:
    """Tests for decrypt_value error handling paths."""

    def test_decrypt_non_base64_input_returns_none(self):
        """Non-base64 input should return None via the generic Exception handler."""
        from app.core.encryption import decrypt_value
        result = decrypt_value("not-valid-base64!!!")
        assert result is None

    def test_decrypt_empty_string_returns_none(self):
        """Empty ciphertext should return None."""
        from app.core.encryption import decrypt_value
        result = decrypt_value("")
        assert result is None

    def test_decrypt_truncated_ciphertext_returns_none(self):
        """Truncated ciphertext should trigger InvalidToken path."""
        from app.core.encryption import encrypt_value, decrypt_value
        encrypted = encrypt_value("hello")
        truncated = encrypted[:10]
        result = decrypt_value(truncated)
        assert result is None


# ── Security Tests ────────────────────────────────────────────────────────────


class TestAccessTokenCustomExpiry:
    """Tests for create_access_token with custom expires_delta."""

    def test_custom_expiry_delta(self):
        from app.core.security import create_access_token, decode_token
        token = create_access_token(
            subject="user-123",
            expires_delta=timedelta(minutes=5),
        )
        payload = decode_token(token)
        assert payload is not None
        assert payload["sub"] == "user-123"
        assert payload["type"] == "access"

    def test_additional_claims_included(self):
        from app.core.security import create_access_token, decode_token
        token = create_access_token(
            subject="user-456",
            additional_claims={"role": "ADMIN", "org_id": "org-789"},
        )
        payload = decode_token(token)
        assert payload is not None
        assert payload["role"] == "ADMIN"
        assert payload["org_id"] == "org-789"

    def test_additional_claims_with_custom_expiry(self):
        from app.core.security import create_access_token, decode_token
        token = create_access_token(
            subject="user-789",
            expires_delta=timedelta(hours=1),
            additional_claims={"scope": "read"},
        )
        payload = decode_token(token)
        assert payload is not None
        assert payload["scope"] == "read"


class TestRefreshTokenCustomExpiry:
    """Tests for create_refresh_token with custom expires_delta."""

    def test_custom_expiry_delta(self):
        from app.core.security import create_refresh_token, decode_token
        token = create_refresh_token(
            subject="user-123",
            expires_delta=timedelta(days=1),
        )
        payload = decode_token(token)
        assert payload is not None
        assert payload["sub"] == "user-123"
        assert payload["type"] == "refresh"
