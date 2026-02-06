"""
Tests for the email service, encryption, and email settings schemas.

Covers:
- Fernet encrypt/decrypt round-trip
- EmailService.send_email_with_settings (mocked aiosmtplib)
- EmailService.render_template
- EmailSettingsUpdate Pydantic validation
"""

import pytest
from unittest.mock import AsyncMock, patch, MagicMock

from app.core.encryption import encrypt_value, decrypt_value
from app.schemas.email_settings import EmailSettingsUpdate


# ---- Encryption Tests ----

class TestEncryption:
    """Fernet encryption/decryption round-trip tests."""

    def test_encrypt_decrypt_round_trip(self):
        """Encrypted value can be decrypted back to original."""
        plaintext = "my-secret-smtp-password"
        ciphertext = encrypt_value(plaintext)
        result = decrypt_value(ciphertext)
        assert result == plaintext

    def test_decrypt_invalid_ciphertext_returns_none(self):
        """Decrypting garbage returns None instead of raising."""
        result = decrypt_value("not-a-valid-ciphertext")
        assert result is None

    def test_different_values_produce_different_ciphertexts(self):
        """Different plaintext values encrypt to different ciphertexts."""
        ct1 = encrypt_value("password-one")
        ct2 = encrypt_value("password-two")
        assert ct1 != ct2

    def test_encrypt_returns_string(self):
        """Encrypted value is a string, suitable for JSON storage."""
        result = encrypt_value("test")
        assert isinstance(result, str)

    def test_empty_string_encrypt_decrypt(self):
        """Empty string can be encrypted and decrypted."""
        ciphertext = encrypt_value("")
        result = decrypt_value(ciphertext)
        assert result == ""


# ---- Email Service Tests ----

class TestEmailService:
    """EmailService methods with mocked SMTP."""

    @pytest.mark.asyncio
    async def test_send_with_full_credentials(self):
        """send_email_with_settings with credentials includes auth."""
        from app.services.email_service import EmailService

        service = EmailService.__new__(EmailService)
        service.jinja_env = MagicMock()

        with patch("app.services.email_service.aiosmtplib.send", new_callable=AsyncMock) as mock_send:
            result = await service.send_email_with_settings(
                to_email="test@example.com",
                subject="Test Subject",
                html_content="<p>Hello</p>",
                smtp_host="smtp.example.com",
                smtp_port=587,
                smtp_user="user@example.com",
                smtp_password="password123",
                smtp_from_email="noreply@example.com",
                smtp_from_name="Test",
                smtp_use_tls=True,
            )

        assert result is True
        mock_send.assert_called_once()
        kwargs = mock_send.call_args.kwargs
        assert kwargs["hostname"] == "smtp.example.com"
        assert kwargs["port"] == 587
        assert kwargs["username"] == "user@example.com"
        assert kwargs["password"] == "password123"
        assert kwargs["start_tls"] is True

    @pytest.mark.asyncio
    async def test_send_without_credentials(self):
        """send_email_with_settings with empty credentials omits auth."""
        from app.services.email_service import EmailService

        service = EmailService.__new__(EmailService)
        service.jinja_env = MagicMock()

        with patch("app.services.email_service.aiosmtplib.send", new_callable=AsyncMock) as mock_send:
            result = await service.send_email_with_settings(
                to_email="test@example.com",
                subject="Test",
                html_content="<p>Hi</p>",
                smtp_host="localhost",
                smtp_port=1025,
                smtp_user="",
                smtp_password="",
                smtp_from_email="noreply@example.com",
                smtp_from_name="Test",
                smtp_use_tls=False,
            )

        assert result is True
        kwargs = mock_send.call_args.kwargs
        assert "username" not in kwargs
        assert "password" not in kwargs

    @pytest.mark.asyncio
    async def test_send_with_no_host_logs_warning(self):
        """send_email_with_settings with no host returns True (dev mode)."""
        from app.services.email_service import EmailService

        service = EmailService.__new__(EmailService)
        service.jinja_env = MagicMock()

        result = await service.send_email_with_settings(
            to_email="test@example.com",
            subject="Test",
            html_content="<p>Hi</p>",
            smtp_host="",
            smtp_port=587,
            smtp_user="",
            smtp_password="",
            smtp_from_email="noreply@example.com",
            smtp_from_name="Test",
        )
        # Returns True for dev/testing when no host configured
        assert result is True

    @pytest.mark.asyncio
    async def test_send_with_smtp_error_raises(self):
        """send_email_with_settings re-raises SMTP exceptions."""
        from app.services.email_service import EmailService

        service = EmailService.__new__(EmailService)
        service.jinja_env = MagicMock()

        with patch("app.services.email_service.aiosmtplib.send", new_callable=AsyncMock) as mock_send:
            mock_send.side_effect = ConnectionRefusedError("Connection refused")
            with pytest.raises(ConnectionRefusedError):
                await service.send_email_with_settings(
                    to_email="test@example.com",
                    subject="Test",
                    html_content="<p>Hi</p>",
                    smtp_host="smtp.example.com",
                    smtp_port=587,
                    smtp_user="user",
                    smtp_password="pass",
                    smtp_from_email="noreply@example.com",
                    smtp_from_name="Test",
                )

    def test_render_template(self):
        """render_template renders interview invitation with all variables."""
        from app.services.email_service import EmailService

        service = EmailService()
        html = service.render_template(
            "interview_invitation.html",
            candidate_name="Jane Doe",
            job_title="Software Engineer",
            organization_name="Acme Corp",
            interview_url="http://localhost:3003/interview/abc123",
        )
        assert "Jane Doe" in html
        assert "Software Engineer" in html
        assert "Acme Corp" in html
        assert "http://localhost:3003/interview/abc123" in html


# ---- Email Settings Schema Tests ----

class TestEmailSettingsSchema:
    """Pydantic validation for EmailSettingsUpdate."""

    def test_valid_full_settings(self):
        """Valid settings with all fields are accepted."""
        settings = EmailSettingsUpdate(
            smtp_host="smtp.gmail.com",
            smtp_port=587,
            smtp_user="user@gmail.com",
            smtp_password="app-password",
            smtp_from_email="noreply@company.com",
            smtp_from_name="Company HR",
            smtp_use_tls=True,
        )
        assert settings.smtp_host == "smtp.gmail.com"
        assert settings.smtp_use_tls is True

    def test_empty_smtp_user_accepted(self):
        """Empty smtp_user is valid (for unauthenticated SMTP like Mailpit)."""
        settings = EmailSettingsUpdate(
            smtp_host="localhost",
            smtp_port=1025,
            smtp_user="",
            smtp_password=None,
            smtp_from_email="test@example.com",
            smtp_from_name="Test",
        )
        assert settings.smtp_user == ""

    def test_missing_smtp_host_rejected(self):
        """Missing smtp_host is rejected by validation."""
        with pytest.raises(Exception):  # ValidationError
            EmailSettingsUpdate(
                smtp_port=587,
                smtp_user="user",
                smtp_password="pass",
                smtp_from_email="test@example.com",
                smtp_from_name="Test",
            )

    def test_empty_smtp_host_rejected(self):
        """Empty string smtp_host is rejected (min_length=1)."""
        with pytest.raises(Exception):
            EmailSettingsUpdate(
                smtp_host="",
                smtp_port=587,
                smtp_from_email="test@example.com",
                smtp_from_name="Test",
            )

    def test_port_zero_rejected(self):
        """Port 0 is out of range (ge=1)."""
        with pytest.raises(Exception):
            EmailSettingsUpdate(
                smtp_host="localhost",
                smtp_port=0,
                smtp_from_email="test@example.com",
                smtp_from_name="Test",
            )

    def test_port_too_high_rejected(self):
        """Port above 65535 is rejected."""
        with pytest.raises(Exception):
            EmailSettingsUpdate(
                smtp_host="localhost",
                smtp_port=70000,
                smtp_from_email="test@example.com",
                smtp_from_name="Test",
            )

    def test_default_tls_is_true(self):
        """smtp_use_tls defaults to True when not specified."""
        settings = EmailSettingsUpdate(
            smtp_host="smtp.example.com",
            smtp_port=587,
            smtp_from_email="test@example.com",
            smtp_from_name="Test",
        )
        assert settings.smtp_use_tls is True

    def test_invalid_from_email_rejected(self):
        """Invalid email format for smtp_from_email is rejected."""
        with pytest.raises(Exception):
            EmailSettingsUpdate(
                smtp_host="localhost",
                smtp_port=587,
                smtp_from_email="not-an-email",
                smtp_from_name="Test",
            )
