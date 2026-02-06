"""
Email service for sending SMTP emails.

Provides async email sending with Jinja2 template rendering.
Falls back to console logging when SMTP is not configured.
"""

import asyncio
import logging
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from pathlib import Path
from typing import Optional

import aiosmtplib
from jinja2 import Environment, FileSystemLoader, select_autoescape

from app.config import settings

logger = logging.getLogger(__name__)

# Template directory
TEMPLATE_DIR = Path(__file__).parent.parent / "templates" / "email"


class EmailService:
    """Service for sending emails via SMTP."""

    def __init__(self):
        """Initialize email service with Jinja2 environment."""
        self.jinja_env = Environment(
            loader=FileSystemLoader(str(TEMPLATE_DIR)),
            autoescape=select_autoescape(["html", "xml"]),
        )

    def _is_configured(self) -> bool:
        """Check if SMTP is properly configured."""
        return settings.smtp_configured

    async def send_email(
        self,
        to_email: str,
        subject: str,
        html_content: str,
        text_content: Optional[str] = None,
    ) -> bool:
        """
        Send an email via SMTP.

        Args:
            to_email: Recipient email address
            subject: Email subject
            html_content: HTML body content
            text_content: Optional plain text body (fallback)

        Returns:
            True if sent successfully, False otherwise
        """
        if not self._is_configured():
            logger.warning(
                "SMTP not configured. Email would be sent to: %s, Subject: %s",
                to_email,
                subject,
            )
            logger.info("Email content:\n%s", text_content or html_content)
            return True  # Return True for dev/testing

        # Build message
        msg = MIMEMultipart("alternative")
        msg["Subject"] = subject
        msg["From"] = f"{settings.SMTP_FROM_NAME} <{settings.SMTP_FROM_EMAIL}>"
        msg["To"] = to_email

        # Add plain text part
        if text_content:
            msg.attach(MIMEText(text_content, "plain"))

        # Add HTML part
        msg.attach(MIMEText(html_content, "html"))

        try:
            await aiosmtplib.send(
                msg,
                hostname=settings.SMTP_HOST,
                port=settings.SMTP_PORT,
                username=settings.SMTP_USER,
                password=settings.SMTP_PASSWORD,
                start_tls=settings.SMTP_USE_TLS,
            )
            logger.info("Email sent successfully to %s", to_email)
            return True
        except Exception as e:
            logger.error("Failed to send email to %s: %s", to_email, str(e))
            return False

    async def send_email_with_settings(
        self,
        to_email: str,
        subject: str,
        html_content: str,
        text_content: Optional[str] = None,
        smtp_host: str = "",
        smtp_port: int = 587,
        smtp_user: str = "",
        smtp_password: str = "",
        smtp_from_email: str = "",
        smtp_from_name: str = "",
        smtp_use_tls: bool = True,
    ) -> bool:
        """
        Send an email via SMTP using explicit settings.

        This method is used when sending with organization-specific SMTP settings
        stored in the database, rather than the default .env configuration.

        Args:
            to_email: Recipient email address
            subject: Email subject
            html_content: HTML body content
            text_content: Optional plain text body (fallback)
            smtp_host: SMTP server hostname
            smtp_port: SMTP server port
            smtp_user: SMTP username
            smtp_password: SMTP password (decrypted)
            smtp_from_email: Sender email address
            smtp_from_name: Sender display name
            smtp_use_tls: Whether to use TLS

        Returns:
            True if sent successfully, False otherwise
        """
        if not smtp_host:
            logger.warning(
                "SMTP host not set. Email would be sent to: %s, Subject: %s",
                to_email,
                subject,
            )
            logger.info("Email content:\n%s", text_content or html_content)
            return True  # Return True for dev/testing

        # Build message
        msg = MIMEMultipart("alternative")
        msg["Subject"] = subject
        msg["From"] = f"{smtp_from_name} <{smtp_from_email}>"
        msg["To"] = to_email

        # Add plain text part
        if text_content:
            msg.attach(MIMEText(text_content, "plain"))

        # Add HTML part
        msg.attach(MIMEText(html_content, "html"))

        try:
            # Build connection kwargs — only include auth if credentials provided
            send_kwargs = {
                "hostname": smtp_host,
                "port": smtp_port,
                "start_tls": smtp_use_tls,
            }
            if smtp_user and smtp_password:
                send_kwargs["username"] = smtp_user
                send_kwargs["password"] = smtp_password

            await aiosmtplib.send(msg, **send_kwargs)
            logger.info("Email sent successfully to %s via custom SMTP settings", to_email)
            return True
        except Exception as e:
            logger.error("Failed to send email to %s: %s", to_email, str(e))
            raise  # Re-raise for caller to handle

    def render_template(self, template_name: str, **context) -> str:
        """
        Render a Jinja2 email template.

        Args:
            template_name: Template filename (e.g., "interview_invitation.html")
            **context: Template context variables

        Returns:
            Rendered HTML string
        """
        template = self.jinja_env.get_template(template_name)
        return template.render(**context)

    async def send_interview_invitation(
        self,
        candidate_email: str,
        candidate_name: str,
        job_title: str,
        organization_name: str,
        interview_token: str,
        custom_message: Optional[str] = None,
    ) -> bool:
        """
        Send interview invitation email with magic link.

        Args:
            candidate_email: Candidate's email address
            candidate_name: Candidate's full name
            job_title: Job position title
            organization_name: Hiring organization name
            interview_token: Magic link token
            custom_message: Optional custom message from employer

        Returns:
            True if sent successfully, False otherwise
        """
        # Build magic link URL
        interview_url = f"{settings.FRONTEND_BASE_URL}/interview/{interview_token}"

        # Render HTML template
        html_content = self.render_template(
            "interview_invitation.html",
            candidate_name=candidate_name,
            job_title=job_title,
            organization_name=organization_name,
            interview_url=interview_url,
            custom_message=custom_message,
        )

        # Plain text fallback
        text_content = f"""
Hi {candidate_name},

{organization_name} has invited you to complete an interview assessment for the {job_title} position.

This is an AI-guided behavioral interview that takes approximately 25-30 minutes. You'll be asked about your experiences and how you've handled various situations in the past.

Tips for success:
- Find a quiet place where you won't be interrupted
- Use specific examples from your experience
- Take your time - there's no time limit
- Be yourself - we want to understand how you think

Start your interview here: {interview_url}

This link expires in 7 days.

{f"Message from the employer: {custom_message}" if custom_message else ""}

---
This interview is conducted using AI technology to ensure a consistent and fair assessment experience for all candidates.
"""

        subject = f"Interview Invitation: {job_title} at {organization_name}"

        return await self.send_email(
            to_email=candidate_email,
            subject=subject,
            html_content=html_content,
            text_content=text_content.strip(),
        )


# Singleton instance
_email_service: Optional[EmailService] = None


def get_email_service() -> EmailService:
    """Get or create the email service singleton."""
    global _email_service
    if _email_service is None:
        _email_service = EmailService()
    return _email_service
