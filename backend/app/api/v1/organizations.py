"""Organization endpoints."""

from datetime import datetime, timezone
from typing import Annotated, Optional
import uuid

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm.attributes import flag_modified

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
from app.schemas.llm_settings import (
    LLMSettingsUpdate,
    LLMSettingsResponse,
    LLMProviderInfo,
    LLMTestRequest,
    LLMTestResult,
)
from app.core.encryption import encrypt_value, decrypt_value

router = APIRouter()


# --- LLM Provider List (must be before /{org_id} routes) ---


@router.get("/llm-providers", response_model=list[LLMProviderInfo])
async def list_llm_providers(
    current_user: Annotated[User, Depends(require_role("ADMIN"))],
) -> list[LLMProviderInfo]:
    """List available LLM providers with their model catalogs (admin only)."""
    from app.services.llm_providers import get_provider_list

    providers = get_provider_list()
    return [LLMProviderInfo(**p) for p in providers]


@router.post("/llm-providers/{provider_id}/models", response_model=list[str])
async def fetch_provider_models(
    provider_id: str,
    db: Annotated[AsyncSession, Depends(get_db)],
    current_user: Annotated[User, Depends(require_role("ADMIN"))],
    api_key: Optional[str] = None,
    base_url: Optional[str] = None,
) -> list[str]:
    """Fetch available models from a provider's API (admin only).

    For cloud providers, uses the provided API key, or falls back to org settings / .env.
    For Ollama, queries the local instance.
    """
    from app.services.llm_providers import fetch_models, PROVIDER_CONFIGS
    from app.config import settings as app_settings
    from app.services.llm_client import _PROVIDER_ENV_KEYS

    if provider_id not in PROVIDER_CONFIGS:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail=f"Unknown provider: {provider_id}",
        )

    # Resolve API key: provided > org DB > .env
    effective_key = api_key or ""
    if not effective_key and current_user.organization_id:
        result = await db.execute(
            select(Organization).where(Organization.id == current_user.organization_id)
        )
        org = result.scalar_one_or_none()
        if org and org.settings:
            llm_settings = org.settings.get("llm", {})
            if llm_settings.get("provider") == provider_id:
                encrypted = llm_settings.get("api_key_encrypted")
                if encrypted:
                    effective_key = decrypt_value(encrypted) or ""

    if not effective_key:
        env_key_attr = _PROVIDER_ENV_KEYS.get(provider_id)
        if env_key_attr:
            effective_key = getattr(app_settings, env_key_attr, "")

    effective_url = base_url
    if not effective_url and provider_id == "ollama":
        effective_url = app_settings.OLLAMA_BASE_URL

    models = fetch_models(provider_id, effective_key, effective_url)
    return models


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

    # Check if configured (only smtp_host is strictly required — user/password optional for local dev)
    is_configured = bool(email_settings.get("smtp_host"))

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
    flag_modified(org, "settings")

    await db.commit()
    await db.refresh(org)

    # Check if configured (only smtp_host is strictly required — user/password optional for local dev)
    is_configured = bool(email_settings.get("smtp_host"))

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

    if not email_settings.get("smtp_host"):
        return TestEmailResponse(
            success=False,
            message="Email settings not configured",
            error_detail="Please save your SMTP settings first",
        )

    # Decrypt password (may be empty for unauthenticated SMTP like Mailpit)
    smtp_password = ""
    if email_settings.get("smtp_password_encrypted"):
        smtp_password = decrypt_value(email_settings["smtp_password_encrypted"]) or ""

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


# --- LLM Settings Endpoints ---


@router.get("/{org_id}/llm-settings", response_model=LLMSettingsResponse)
async def get_llm_settings(
    org_id: uuid.UUID,
    db: Annotated[AsyncSession, Depends(get_db)],
    current_user: Annotated[User, Depends(require_role("ADMIN"))],
) -> LLMSettingsResponse:
    """Get organization LLM/AI provider settings (admin only)."""
    from app.config import settings as app_settings

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

    # Check for org-specific DB settings first
    llm_settings = (org.settings or {}).get("llm", {})

    if llm_settings.get("provider"):
        return LLMSettingsResponse(
            provider=llm_settings["provider"],
            model=llm_settings.get("model", ""),
            api_key_set=bool(llm_settings.get("api_key_encrypted")),
            base_url=llm_settings.get("base_url"),
            is_configured=True,
            configured_at=llm_settings.get("configured_at"),
            configured_by=llm_settings.get("configured_by"),
            source="database",
        )

    # Fall back to .env settings
    env_provider = app_settings.LLM_PROVIDER or "anthropic"
    env_model = app_settings.LLM_MODEL or ""

    # Check if the relevant API key is set in .env
    from app.services.llm_client import _PROVIDER_ENV_KEYS
    env_key_attr = _PROVIDER_ENV_KEYS.get(env_provider)
    env_key_set = bool(getattr(app_settings, env_key_attr, "")) if env_key_attr else (env_provider == "ollama")

    return LLMSettingsResponse(
        provider=env_provider,
        model=env_model,
        api_key_set=env_key_set,
        base_url=app_settings.OLLAMA_BASE_URL if env_provider == "ollama" else None,
        is_configured=env_key_set,
        source="env" if env_key_set else "default",
    )


@router.put("/{org_id}/llm-settings", response_model=LLMSettingsResponse)
async def update_llm_settings(
    org_id: uuid.UUID,
    settings_in: LLMSettingsUpdate,
    db: Annotated[AsyncSession, Depends(get_db)],
    current_user: Annotated[User, Depends(require_role("ADMIN"))],
) -> LLMSettingsResponse:
    """Update organization LLM/AI provider settings (admin only)."""
    from app.services.llm_providers import PROVIDER_CONFIGS

    # Validate provider
    if settings_in.provider not in PROVIDER_CONFIGS:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail=f"Unknown provider: {settings_in.provider}",
        )

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
    existing_llm = org_settings.get("llm", {})

    # Build new LLM settings
    llm_settings = {
        "provider": settings_in.provider,
        "model": settings_in.model,
        "base_url": settings_in.base_url,
        "configured_at": datetime.now(timezone.utc).isoformat(),
        "configured_by": str(current_user.id),
    }

    # Handle API key: encrypt if provided, keep existing if not
    if settings_in.api_key:
        llm_settings["api_key_encrypted"] = encrypt_value(settings_in.api_key)
    elif existing_llm.get("api_key_encrypted"):
        llm_settings["api_key_encrypted"] = existing_llm["api_key_encrypted"]

    # Update organization settings
    org_settings["llm"] = llm_settings
    org.settings = org_settings
    flag_modified(org, "settings")

    await db.commit()
    await db.refresh(org)

    return LLMSettingsResponse(
        provider=llm_settings["provider"],
        model=llm_settings["model"],
        api_key_set=bool(llm_settings.get("api_key_encrypted")),
        base_url=llm_settings.get("base_url"),
        is_configured=True,
        configured_at=llm_settings["configured_at"],
        configured_by=llm_settings["configured_by"],
        source="database",
    )


@router.post("/{org_id}/llm-settings/test", response_model=LLMTestResult)
async def test_llm_settings(
    org_id: uuid.UUID,
    test_request: LLMTestRequest,
    db: Annotated[AsyncSession, Depends(get_db)],
    current_user: Annotated[User, Depends(require_role("ADMIN"))],
) -> LLMTestResult:
    """Test LLM connection with the given provider settings (admin only)."""
    from app.services.llm_providers import create_provider, PROVIDER_CONFIGS

    # Check access
    if not current_user.is_superuser and current_user.organization_id != org_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized",
        )

    # Validate provider
    if test_request.provider not in PROVIDER_CONFIGS:
        return LLMTestResult(
            success=False,
            message=f"Unknown provider: {test_request.provider}",
        )

    # Resolve API key: use provided key, or try org DB key, or try .env key
    api_key = test_request.api_key
    if not api_key:
        # Try org settings
        result = await db.execute(select(Organization).where(Organization.id == org_id))
        org = result.scalar_one_or_none()
        if org and org.settings:
            llm_settings = org.settings.get("llm", {})
            encrypted = llm_settings.get("api_key_encrypted")
            if encrypted:
                api_key = decrypt_value(encrypted) or ""

    if not api_key:
        # Try .env
        from app.config import settings as app_settings
        from app.services.llm_client import _PROVIDER_ENV_KEYS
        env_key_attr = _PROVIDER_ENV_KEYS.get(test_request.provider)
        if env_key_attr:
            api_key = getattr(app_settings, env_key_attr, "")

    # Ollama doesn't need an API key
    provider_config = PROVIDER_CONFIGS[test_request.provider]
    if provider_config["requires_api_key"] and not api_key:
        return LLMTestResult(
            success=False,
            message=f"No API key configured for {provider_config['name']}. Enter a key or set it in .env.",
        )

    try:
        provider = create_provider(
            provider_name=test_request.provider,
            api_key=api_key or "",
            model=test_request.model,
            base_url=test_request.base_url,
        )

        response = await provider.complete(
            prompt="Say 'Hello from AP API!' in one short sentence.",
            max_tokens=50,
            temperature=0.3,
        )

        preview = str(response)[:150] if response else ""

        return LLMTestResult(
            success=True,
            message=f"Successfully connected to {provider_config['name']}",
            response_preview=preview,
        )

    except Exception as e:
        return LLMTestResult(
            success=False,
            message=f"Connection failed: {str(e)[:200]}",
        )
