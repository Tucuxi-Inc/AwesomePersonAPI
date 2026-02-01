"""Organization endpoints."""

from datetime import datetime, timezone
from typing import Annotated, Optional
import uuid

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import AsyncSession

from app.dependencies import get_db, get_current_user, require_role
from app.models import Organization, User
from app.schemas.organization import (
    OrganizationCreate,
    OrganizationUpdate,
    OrganizationResponse,
    OrganizationList,
)
from app.schemas.email_settings import (
    EmailSettingsUpdate,
    EmailSettingsResponse,
    TestEmailRequest,
    TestEmailResponse,
)
from app.core.encryption import encrypt_value, decrypt_value

router = APIRouter()


@router.get("", response_model=OrganizationList)
async def list_organizations(
    db: Annotated[AsyncSession, Depends(get_db)],
    current_user: Annotated[User, Depends(get_current_user)],
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=100),
    search: Optional[str] = None,
) -> OrganizationList:
    """List organizations (superusers see all, others see their own)."""
    query = select(Organization)

    if not current_user.is_superuser:
        query = query.where(Organization.id == current_user.organization_id)

    if search:
        query = query.where(Organization.name.ilike(f"%{search}%"))

    # Count total
    count_query = select(func.count()).select_from(query.subquery())
    total = (await db.execute(count_query)).scalar_one()

    # Get items
    query = query.offset(skip).limit(limit).order_by(Organization.name)
    result = await db.execute(query)
    items = result.scalars().all()

    return OrganizationList(items=items, total=total)


@router.post("", response_model=OrganizationResponse, status_code=status.HTTP_201_CREATED)
async def create_organization(
    org_in: OrganizationCreate,
    db: Annotated[AsyncSession, Depends(get_db)],
    current_user: Annotated[User, Depends(require_role("ADMIN"))],
) -> Organization:
    """Create a new organization (admin only)."""
    # Check if slug exists
    result = await db.execute(
        select(Organization).where(Organization.slug == org_in.slug)
    )
    if result.scalar_one_or_none():
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Organization with this slug already exists",
        )

    org = Organization(**org_in.model_dump())
    db.add(org)
    await db.commit()
    await db.refresh(org)
    return org


@router.get("/{org_id}", response_model=OrganizationResponse)
async def get_organization(
    org_id: uuid.UUID,
    db: Annotated[AsyncSession, Depends(get_db)],
    current_user: Annotated[User, Depends(get_current_user)],
) -> Organization:
    """Get organization by ID."""
    result = await db.execute(select(Organization).where(Organization.id == org_id))
    org = result.scalar_one_or_none()

    if not org:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Organization not found",
        )

    # Check access
    if not current_user.is_superuser and current_user.organization_id != org_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to access this organization",
        )

    return org


@router.put("/{org_id}", response_model=OrganizationResponse)
async def update_organization(
    org_id: uuid.UUID,
    org_in: OrganizationUpdate,
    db: Annotated[AsyncSession, Depends(get_db)],
    current_user: Annotated[User, Depends(require_role("ADMIN"))],
) -> Organization:
    """Update organization (admin only)."""
    result = await db.execute(select(Organization).where(Organization.id == org_id))
    org = result.scalar_one_or_none()

    if not org:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Organization not found",
        )

    # Check access
    if not current_user.is_superuser and current_user.organization_id != org_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to modify this organization",
        )

    update_data = org_in.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(org, field, value)

    await db.commit()
    await db.refresh(org)
    return org


@router.delete("/{org_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_organization(
    org_id: uuid.UUID,
    db: Annotated[AsyncSession, Depends(get_db)],
    current_user: Annotated[User, Depends(require_role("ADMIN"))],
) -> None:
    """Delete organization (superuser only)."""
    if not current_user.is_superuser:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Only superusers can delete organizations",
        )

    result = await db.execute(select(Organization).where(Organization.id == org_id))
    org = result.scalar_one_or_none()

    if not org:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Organization not found",
        )

    await db.delete(org)
    await db.commit()


# --- Email Settings Endpoints ---


@router.get("/{org_id}/email-settings", response_model=EmailSettingsResponse)
async def get_email_settings(
    org_id: uuid.UUID,
    db: Annotated[AsyncSession, Depends(get_db)],
    current_user: Annotated[User, Depends(require_role("ADMIN"))],
) -> EmailSettingsResponse:
    """Get organization email/SMTP settings (admin only)."""
    # Get organization
    result = await db.execute(select(Organization).where(Organization.id == org_id))
    org = result.scalar_one_or_none()

    if not org:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Organization not found",
        )

    # Check access
    if not current_user.is_superuser and current_user.organization_id != org_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to access this organization's settings",
        )

    # Get email settings from organization settings
    email_settings = (org.settings or {}).get("email", {})

    # Check if configured
    is_configured = bool(
        email_settings.get("smtp_host")
        and email_settings.get("smtp_user")
        and email_settings.get("smtp_password_encrypted")
    )

    return EmailSettingsResponse(
        smtp_host=email_settings.get("smtp_host", ""),
        smtp_port=email_settings.get("smtp_port", 587),
        smtp_user=email_settings.get("smtp_user", ""),
        smtp_password_set=bool(email_settings.get("smtp_password_encrypted")),
        smtp_from_email=email_settings.get("smtp_from_email", ""),
        smtp_from_name=email_settings.get("smtp_from_name", ""),
        smtp_use_tls=email_settings.get("smtp_use_tls", True),
        configured_at=email_settings.get("configured_at"),
        configured_by=email_settings.get("configured_by"),
        is_configured=is_configured,
    )


@router.put("/{org_id}/email-settings", response_model=EmailSettingsResponse)
async def update_email_settings(
    org_id: uuid.UUID,
    settings_in: EmailSettingsUpdate,
    db: Annotated[AsyncSession, Depends(get_db)],
    current_user: Annotated[User, Depends(require_role("ADMIN"))],
) -> EmailSettingsResponse:
    """Update organization email/SMTP settings (admin only)."""
    # Get organization
    result = await db.execute(select(Organization).where(Organization.id == org_id))
    org = result.scalar_one_or_none()

    if not org:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Organization not found",
        )

    # Check access
    if not current_user.is_superuser and current_user.organization_id != org_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to modify this organization's settings",
        )

    # Get existing settings or initialize
    org_settings = org.settings or {}
    existing_email = org_settings.get("email", {})

    # Build new email settings
    email_settings = {
        "smtp_host": settings_in.smtp_host,
        "smtp_port": settings_in.smtp_port,
        "smtp_user": settings_in.smtp_user,
        "smtp_from_email": settings_in.smtp_from_email,
        "smtp_from_name": settings_in.smtp_from_name,
        "smtp_use_tls": settings_in.smtp_use_tls,
        "configured_at": datetime.now(timezone.utc).isoformat(),
        "configured_by": str(current_user.id),
    }

    # Handle password: encrypt if provided, keep existing if not
    if settings_in.smtp_password:
        email_settings["smtp_password_encrypted"] = encrypt_value(settings_in.smtp_password)
    elif existing_email.get("smtp_password_encrypted"):
        email_settings["smtp_password_encrypted"] = existing_email["smtp_password_encrypted"]

    # Update organization settings
    org_settings["email"] = email_settings
    org.settings = org_settings

    await db.commit()
    await db.refresh(org)

    # Check if configured
    is_configured = bool(
        email_settings.get("smtp_host")
        and email_settings.get("smtp_user")
        and email_settings.get("smtp_password_encrypted")
    )

    return EmailSettingsResponse(
        smtp_host=email_settings["smtp_host"],
        smtp_port=email_settings["smtp_port"],
        smtp_user=email_settings["smtp_user"],
        smtp_password_set=bool(email_settings.get("smtp_password_encrypted")),
        smtp_from_email=email_settings["smtp_from_email"],
        smtp_from_name=email_settings["smtp_from_name"],
        smtp_use_tls=email_settings["smtp_use_tls"],
        configured_at=email_settings["configured_at"],
        configured_by=email_settings["configured_by"],
        is_configured=is_configured,
    )


@router.post("/{org_id}/email-settings/test", response_model=TestEmailResponse)
async def test_email_settings(
    org_id: uuid.UUID,
    test_request: TestEmailRequest,
    db: Annotated[AsyncSession, Depends(get_db)],
    current_user: Annotated[User, Depends(require_role("ADMIN"))],
) -> TestEmailResponse:
    """Send a test email to verify SMTP configuration (admin only)."""
    from app.services.email_service import EmailService

    # Get organization
    result = await db.execute(select(Organization).where(Organization.id == org_id))
    org = result.scalar_one_or_none()

    if not org:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Organization not found",
        )

    # Check access
    if not current_user.is_superuser and current_user.organization_id != org_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to test this organization's email settings",
        )

    # Get email settings
    email_settings = (org.settings or {}).get("email", {})

    if not email_settings.get("smtp_password_encrypted"):
        return TestEmailResponse(
            success=False,
            message="Email settings not configured",
            error_detail="Please save your SMTP settings first",
        )

    # Decrypt password
    smtp_password = decrypt_value(email_settings["smtp_password_encrypted"])
    if not smtp_password:
        return TestEmailResponse(
            success=False,
            message="Failed to decrypt SMTP password",
            error_detail="The stored password could not be decrypted. Please re-enter your SMTP password.",
        )

    # Create email service with org settings
    email_service = EmailService()

    # Build test email content
    html_content = f"""
    <html>
    <body style="font-family: Arial, sans-serif; padding: 20px;">
        <h2>Test Email from AP API</h2>
        <p>This is a test email to verify your SMTP configuration.</p>
        <p><strong>Organization:</strong> {org.name}</p>
        <p><strong>Sent by:</strong> {current_user.email}</p>
        <p><strong>Timestamp:</strong> {datetime.now(timezone.utc).isoformat()}</p>
        <hr>
        <p style="color: #666; font-size: 12px;">
            If you received this email, your SMTP settings are configured correctly.
        </p>
    </body>
    </html>
    """

    text_content = f"""
Test Email from AP API

This is a test email to verify your SMTP configuration.

Organization: {org.name}
Sent by: {current_user.email}
Timestamp: {datetime.now(timezone.utc).isoformat()}

If you received this email, your SMTP settings are configured correctly.
    """

    try:
        success = await email_service.send_email_with_settings(
            to_email=test_request.recipient_email,
            subject=f"Test Email - {org.name}",
            html_content=html_content,
            text_content=text_content,
            smtp_host=email_settings["smtp_host"],
            smtp_port=email_settings["smtp_port"],
            smtp_user=email_settings["smtp_user"],
            smtp_password=smtp_password,
            smtp_from_email=email_settings["smtp_from_email"],
            smtp_from_name=email_settings["smtp_from_name"],
            smtp_use_tls=email_settings["smtp_use_tls"],
        )

        if success:
            return TestEmailResponse(
                success=True,
                message=f"Test email sent successfully to {test_request.recipient_email}",
            )
        else:
            return TestEmailResponse(
                success=False,
                message="Failed to send test email",
                error_detail="The email could not be sent. Check your SMTP settings.",
            )
    except Exception as e:
        return TestEmailResponse(
            success=False,
            message="Failed to send test email",
            error_detail=str(e),
        )
