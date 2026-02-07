"""
Extended tests for email_service.py — covering unconfigured SMTP fallback,
interview invitation, singleton pattern, and send_email exception handling.
"""

import pytest
from unittest.mock import AsyncMock, patch, MagicMock

from app.services.email_service import EmailService, get_email_service


# ── Helpers ───────────────────────────────────────────────────────────────────


def _make_email_service() -> EmailService:
    """Create a fresh EmailService instance."""
    return EmailService()


# ── Unconfigured SMTP Fallback Tests ──────────────────────────────────────────


class TestUnconfiguredSmtpFallback:
    """Tests for send_email when SMTP is not configured."""

    @pytest.mark.asyncio
    async def test_unconfigured_returns_true(self):
        """When SMTP is unconfigured, send_email logs and returns True."""
        svc = _make_email_service()
        with patch.object(svc, "_is_configured", return_value=False):
            result = await svc.send_email(
                to_email="test@example.com",
                subject="Test Subject",
                html_content="<h1>Hello</h1>",
            )
        assert result is True

    @pytest.mark.asyncio
    async def test_unconfigured_with_text_content(self):
        svc = _make_email_service()
        with patch.object(svc, "_is_configured", return_value=False):
            result = await svc.send_email(
                to_email="test@example.com",
                subject="Test",
                html_content="<p>Hi</p>",
                text_content="Hi plain text",
            )
        assert result is True


# ── send_email Exception Handling ─────────────────────────────────────────────


class TestSendEmailExceptionHandling:
    """Tests for send_email SMTP error handling."""

    @pytest.mark.asyncio
    async def test_smtp_exception_returns_false(self):
        """When aiosmtplib.send raises, send_email catches and returns False."""
        svc = _make_email_service()
        with patch.object(svc, "_is_configured", return_value=True), \
             patch("app.services.email_service.aiosmtplib") as mock_smtp, \
             patch("app.services.email_service.settings") as mock_settings:
            mock_settings.SMTP_HOST = "smtp.test.com"
            mock_settings.SMTP_PORT = 587
            mock_settings.SMTP_USER = "user"
            mock_settings.SMTP_PASSWORD = "pass"
            mock_settings.SMTP_FROM_EMAIL = "noreply@test.com"
            mock_settings.SMTP_FROM_NAME = "Test"
            mock_settings.SMTP_USE_TLS = True
            mock_smtp.send = AsyncMock(side_effect=ConnectionRefusedError("Connection refused"))

            result = await svc.send_email(
                to_email="test@example.com",
                subject="Test",
                html_content="<p>Hi</p>",
            )
        assert result is False


# ── send_email_with_settings Tests ────────────────────────────────────────────


class TestSendEmailWithSettings:
    """Tests for send_email_with_settings method."""

    @pytest.mark.asyncio
    async def test_no_host_returns_true(self):
        """When smtp_host is empty, logs and returns True."""
        svc = _make_email_service()
        result = await svc.send_email_with_settings(
            to_email="test@example.com",
            subject="Test",
            html_content="<p>Hi</p>",
            smtp_host="",
        )
        assert result is True

    @pytest.mark.asyncio
    async def test_with_text_content_attaches_plain(self):
        """When text_content is provided, it gets attached to the message."""
        svc = _make_email_service()
        with patch("app.services.email_service.aiosmtplib") as mock_smtp:
            mock_smtp.send = AsyncMock()
            result = await svc.send_email_with_settings(
                to_email="test@example.com",
                subject="Test",
                html_content="<p>Hi</p>",
                text_content="Hi plain text",
                smtp_host="mailpit",
                smtp_port=1025,
            )
        assert result is True
        mock_smtp.send.assert_called_once()


# ── Interview Invitation Tests ────────────────────────────────────────────────


class TestSendInterviewInvitation:
    """Tests for send_interview_invitation method."""

    @pytest.mark.asyncio
    async def test_invitation_constructs_correct_url(self):
        """Magic link URL should use FRONTEND_BASE_URL + token."""
        svc = _make_email_service()
        with patch.object(svc, "send_email", new_callable=AsyncMock, return_value=True) as mock_send:
            await svc.send_interview_invitation(
                candidate_email="jane@example.com",
                candidate_name="Jane Smith",
                job_title="Software Engineer",
                organization_name="Acme Corp",
                interview_token="abc123xyz",
            )
        mock_send.assert_called_once()
        call_kwargs = mock_send.call_args
        assert "abc123xyz" in call_kwargs.kwargs.get("text_content", "") or "abc123xyz" in call_kwargs.kwargs.get("html_content", "")
        assert call_kwargs.kwargs["subject"] == "Interview Invitation: Software Engineer at Acme Corp"

    @pytest.mark.asyncio
    async def test_invitation_with_custom_message(self):
        """Custom message should appear in the text content."""
        svc = _make_email_service()
        with patch.object(svc, "send_email", new_callable=AsyncMock, return_value=True) as mock_send:
            await svc.send_interview_invitation(
                candidate_email="jane@example.com",
                candidate_name="Jane Smith",
                job_title="Engineer",
                organization_name="TestCo",
                interview_token="token123",
                custom_message="We look forward to speaking with you!",
            )
        call_kwargs = mock_send.call_args.kwargs
        assert "We look forward to speaking with you!" in call_kwargs["text_content"]

    @pytest.mark.asyncio
    async def test_invitation_without_custom_message(self):
        """Without custom message, the employer message section should be empty."""
        svc = _make_email_service()
        with patch.object(svc, "send_email", new_callable=AsyncMock, return_value=True) as mock_send:
            await svc.send_interview_invitation(
                candidate_email="jane@example.com",
                candidate_name="Jane Smith",
                job_title="Engineer",
                organization_name="TestCo",
                interview_token="token123",
            )
        call_kwargs = mock_send.call_args.kwargs
        assert "Message from the employer" not in call_kwargs["text_content"]

    @pytest.mark.asyncio
    async def test_invitation_renders_template(self):
        """HTML content should include candidate name from template rendering."""
        svc = _make_email_service()
        with patch.object(svc, "send_email", new_callable=AsyncMock, return_value=True) as mock_send:
            await svc.send_interview_invitation(
                candidate_email="jane@example.com",
                candidate_name="Jane Smith",
                job_title="Engineer",
                organization_name="TestCo",
                interview_token="token123",
            )
        call_kwargs = mock_send.call_args.kwargs
        assert "Jane Smith" in call_kwargs["text_content"]
        assert "TestCo" in call_kwargs["text_content"]


# ── Template Rendering Tests ──────────────────────────────────────────────────


class TestRenderTemplate:
    """Tests for render_template method."""

    def test_render_invitation_template(self):
        """Interview invitation template should render with correct variables."""
        svc = _make_email_service()
        html = svc.render_template(
            "interview_invitation.html",
            candidate_name="John Doe",
            job_title="Data Analyst",
            organization_name="Corp Inc",
            interview_url="http://localhost:3003/interview/abc123",
            custom_message=None,
        )
        assert "John Doe" in html
        assert "Data Analyst" in html
        assert "Corp Inc" in html
        assert "http://localhost:3003/interview/abc123" in html

    def test_render_with_custom_message(self):
        svc = _make_email_service()
        html = svc.render_template(
            "interview_invitation.html",
            candidate_name="Jane",
            job_title="PM",
            organization_name="Co",
            interview_url="http://example.com",
            custom_message="Good luck!",
        )
        assert "Good luck!" in html


# ── Singleton Tests ───────────────────────────────────────────────────────────


class TestEmailServiceSingleton:
    """Tests for get_email_service singleton pattern."""

    def test_returns_same_instance(self):
        import app.services.email_service as mod
        mod._email_service = None  # Reset
        first = get_email_service()
        second = get_email_service()
        assert first is second
        mod._email_service = None  # Cleanup

    def test_returns_email_service_type(self):
        import app.services.email_service as mod
        mod._email_service = None
        svc = get_email_service()
        assert isinstance(svc, EmailService)
        mod._email_service = None
