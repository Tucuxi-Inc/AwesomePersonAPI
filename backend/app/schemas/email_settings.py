"""Email settings schemas."""

from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Field, EmailStr


class EmailSettingsUpdate(BaseModel):
    """Schema for updating email/SMTP settings."""

    smtp_host: str = Field(..., min_length=1, max_length=255)
    smtp_port: int = Field(..., ge=1, le=65535)
    smtp_user: str = Field(..., min_length=1, max_length=255)
    smtp_password: Optional[str] = Field(
        None,
        min_length=1,
        description="SMTP password. Only required on first setup or when changing.",
    )
    smtp_from_email: EmailStr
    smtp_from_name: str = Field(..., min_length=1, max_length=255)
    smtp_use_tls: bool = True


class EmailSettingsResponse(BaseModel):
    """Schema for email settings response (password is never returned)."""

    smtp_host: str
    smtp_port: int
    smtp_user: str
    smtp_password_set: bool = Field(
        description="Indicates if a password is configured (actual password never returned)"
    )
    smtp_from_email: str
    smtp_from_name: str
    smtp_use_tls: bool
    configured_at: Optional[datetime] = None
    configured_by: Optional[str] = None
    is_configured: bool = Field(
        description="True if all required settings are present and valid"
    )


class TestEmailRequest(BaseModel):
    """Schema for test email request."""

    recipient_email: EmailStr = Field(
        ..., description="Email address to send test email to"
    )


class TestEmailResponse(BaseModel):
    """Schema for test email response."""

    success: bool
    message: str
    error_detail: Optional[str] = None
