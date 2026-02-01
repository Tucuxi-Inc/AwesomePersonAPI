"""Email-related Celery tasks."""

import asyncio
import logging
from typing import Optional

from app.tasks.celery_app import celery_app
from app.services.email_service import get_email_service
from app.config import settings

logger = logging.getLogger(__name__)


@celery_app.task(bind=True, max_retries=3, default_retry_delay=60)
def send_interview_invitation_email(
    self,
    candidate_email: str,
    candidate_name: str,
    job_title: str,
    organization_name: str,
    interview_token: str,
    custom_message: Optional[str] = None,
    smtp_settings: Optional[dict] = None,
) -> dict:
    """
    Send interview invitation email with magic link.

    This task is queued when an employer sends an interview invite to a candidate.
    It renders the email template and sends via SMTP.

    Args:
        candidate_email: Candidate's email address
        candidate_name: Candidate's full name
        job_title: Job position title
        organization_name: Hiring organization name
        interview_token: Magic link token for interview access
        custom_message: Optional custom message from employer
        smtp_settings: Optional dict with org-specific SMTP settings:
            - smtp_host, smtp_port, smtp_user, smtp_password,
            - smtp_from_email, smtp_from_name, smtp_use_tls

    Returns:
        dict with status and details
    """
    logger.info(
        "Sending interview invitation to %s for %s at %s",
        candidate_email,
        job_title,
        organization_name,
    )

    try:
        email_service = get_email_service()

        # Build magic link URL
        interview_url = f"{settings.FRONTEND_BASE_URL}/interview/{interview_token}"

        # Render email content
        html_content = email_service.render_template(
            "interview_invitation.html",
            candidate_name=candidate_name,
            job_title=job_title,
            organization_name=organization_name,
            interview_url=interview_url,
            custom_message=custom_message,
        )

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

        # Run async email sending in event loop
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        try:
            if smtp_settings:
                # Use organization-specific SMTP settings
                success = loop.run_until_complete(
                    email_service.send_email_with_settings(
                        to_email=candidate_email,
                        subject=subject,
                        html_content=html_content,
                        text_content=text_content.strip(),
                        smtp_host=smtp_settings.get("smtp_host", ""),
                        smtp_port=smtp_settings.get("smtp_port", 587),
                        smtp_user=smtp_settings.get("smtp_user", ""),
                        smtp_password=smtp_settings.get("smtp_password", ""),
                        smtp_from_email=smtp_settings.get("smtp_from_email", ""),
                        smtp_from_name=smtp_settings.get("smtp_from_name", ""),
                        smtp_use_tls=smtp_settings.get("smtp_use_tls", True),
                    )
                )
            else:
                # Fall back to .env SMTP settings
                success = loop.run_until_complete(
                    email_service.send_email(
                        to_email=candidate_email,
                        subject=subject,
                        html_content=html_content,
                        text_content=text_content.strip(),
                    )
                )
        finally:
            loop.close()

        if success:
            logger.info("Interview invitation sent successfully to %s", candidate_email)
            return {
                "status": "sent",
                "email": candidate_email,
                "job_title": job_title,
            }
        else:
            # Retry on failure
            raise Exception("Email sending failed")

    except Exception as exc:
        logger.error(
            "Failed to send interview invitation to %s: %s",
            candidate_email,
            str(exc),
        )
        # Retry with exponential backoff
        raise self.retry(exc=exc, countdown=60 * (2 ** self.request.retries))
