"""Invitation management endpoints."""

from datetime import datetime
from typing import Annotated, Optional
import uuid

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import AsyncSession

from app.dependencies import get_db, get_current_user, require_role
from app.models import (
    Invitation,
    InvitationType,
    InvitationStatus,
    Candidate,
    TopPerformer,
    User,
)
from app.schemas.invitation import (
    CandidateInvitationCreate,
    TopPerformerInvitationCreate,
    InvitationResponse,
    InvitationList,
    InvitationLinkResponse,
)
from app.config import settings

router = APIRouter()


def get_invitation_link(token: str) -> str:
    """Generate the full invitation URL."""
    frontend_url = settings.CORS_ORIGINS[0] if settings.CORS_ORIGINS else "http://localhost:3003"
    return f"{frontend_url}/invite/{token}"


@router.get("", response_model=InvitationList)
async def list_invitations(
    db: Annotated[AsyncSession, Depends(get_db)],
    current_user: Annotated[User, Depends(get_current_user)],
    invitation_type: Optional[InvitationType] = None,
    status_filter: Optional[InvitationStatus] = Query(None, alias="status"),
    skip: int = Query(0, ge=0),
    limit: int = Query(50, ge=1, le=100),
) -> InvitationList:
    """List invitations for the organization."""
    query = select(Invitation).where(
        Invitation.organization_id == current_user.organization_id
    )

    if invitation_type:
        query = query.where(Invitation.invitation_type == invitation_type)

    if status_filter:
        query = query.where(Invitation.status == status_filter)

    # Count total
    count_query = select(func.count()).select_from(query.subquery())
    total = (await db.execute(count_query)).scalar_one()

    # Get items
    query = query.offset(skip).limit(limit).order_by(Invitation.created_at.desc())
    result = await db.execute(query)
    items = result.scalars().all()

    return InvitationList(items=items, total=total)


@router.post("/candidate", response_model=InvitationLinkResponse, status_code=status.HTTP_201_CREATED)
async def create_candidate_invitation(
    invitation_in: CandidateInvitationCreate,
    db: Annotated[AsyncSession, Depends(get_db)],
    current_user: Annotated[User, Depends(require_role("ADMIN", "HIRING_MANAGER"))],
) -> InvitationLinkResponse:
    """Create an invitation for a candidate interview."""
    # Verify candidate exists and belongs to organization
    result = await db.execute(
        select(Candidate).where(Candidate.id == invitation_in.candidate_id)
    )
    candidate = result.scalar_one_or_none()

    if not candidate:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Candidate not found",
        )

    if candidate.organization_id != current_user.organization_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Candidate does not belong to your organization",
        )

    # Create invitation
    invitation = Invitation.create_for_candidate(
        organization_id=current_user.organization_id,
        candidate_id=candidate.id,
        recipient_email=invitation_in.recipient_email,
        recipient_name=invitation_in.recipient_name or candidate.full_name,
        trait_ids=invitation_in.trait_ids,
        role_profile_id=invitation_in.role_profile_id or candidate.role_profile_id,
        expires_in_days=invitation_in.expires_in_days,
        custom_message=invitation_in.custom_message,
        created_by_id=current_user.id,
    )

    db.add(invitation)
    await db.commit()
    await db.refresh(invitation)

    return InvitationLinkResponse(
        invitation_id=invitation.id,
        token=invitation.token,
        link=get_invitation_link(invitation.token),
        expires_at=invitation.expires_at,
    )


@router.post("/top-performer", response_model=InvitationLinkResponse, status_code=status.HTTP_201_CREATED)
async def create_top_performer_invitation(
    invitation_in: TopPerformerInvitationCreate,
    db: Annotated[AsyncSession, Depends(get_db)],
    current_user: Annotated[User, Depends(require_role("ADMIN", "HIRING_MANAGER"))],
) -> InvitationLinkResponse:
    """Create an invitation for a top performer profiling session."""
    # Verify top performer exists and belongs to organization
    result = await db.execute(
        select(TopPerformer).where(TopPerformer.id == invitation_in.top_performer_id)
    )
    performer = result.scalar_one_or_none()

    if not performer:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Top performer not found",
        )

    if performer.organization_id != current_user.organization_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Top performer does not belong to your organization",
        )

    # Create invitation
    invitation = Invitation.create_for_top_performer(
        organization_id=current_user.organization_id,
        top_performer_id=performer.id,
        recipient_email=invitation_in.recipient_email,
        recipient_name=invitation_in.recipient_name or performer.name,
        trait_ids=invitation_in.trait_ids,
        expires_in_days=invitation_in.expires_in_days,
        custom_message=invitation_in.custom_message,
        created_by_id=current_user.id,
    )

    db.add(invitation)
    await db.commit()
    await db.refresh(invitation)

    return InvitationLinkResponse(
        invitation_id=invitation.id,
        token=invitation.token,
        link=get_invitation_link(invitation.token),
        expires_at=invitation.expires_at,
    )


@router.get("/{invitation_id}", response_model=InvitationResponse)
async def get_invitation(
    invitation_id: uuid.UUID,
    db: Annotated[AsyncSession, Depends(get_db)],
    current_user: Annotated[User, Depends(get_current_user)],
) -> Invitation:
    """Get invitation by ID."""
    result = await db.execute(
        select(Invitation).where(Invitation.id == invitation_id)
    )
    invitation = result.scalar_one_or_none()

    if not invitation:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Invitation not found",
        )

    if invitation.organization_id != current_user.organization_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to access this invitation",
        )

    return invitation


@router.post("/{invitation_id}/resend", response_model=InvitationLinkResponse)
async def resend_invitation(
    invitation_id: uuid.UUID,
    db: Annotated[AsyncSession, Depends(get_db)],
    current_user: Annotated[User, Depends(require_role("ADMIN", "HIRING_MANAGER"))],
) -> InvitationLinkResponse:
    """Resend an invitation (regenerate link if expired)."""
    result = await db.execute(
        select(Invitation).where(Invitation.id == invitation_id)
    )
    invitation = result.scalar_one_or_none()

    if not invitation:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Invitation not found",
        )

    if invitation.organization_id != current_user.organization_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to access this invitation",
        )

    if invitation.status in (InvitationStatus.COMPLETED, InvitationStatus.IN_PROGRESS):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Cannot resend an invitation that is in progress or completed",
        )

    # If expired or revoked, reset status and extend expiration
    if invitation.status in (InvitationStatus.EXPIRED, InvitationStatus.REVOKED):
        invitation.status = InvitationStatus.PENDING
        from datetime import timedelta
        invitation.expires_at = datetime.utcnow() + timedelta(days=7)

    invitation.sent_at = datetime.utcnow()
    await db.commit()
    await db.refresh(invitation)

    return InvitationLinkResponse(
        invitation_id=invitation.id,
        token=invitation.token,
        link=get_invitation_link(invitation.token),
        expires_at=invitation.expires_at,
    )


@router.post("/{invitation_id}/revoke", status_code=status.HTTP_204_NO_CONTENT)
async def revoke_invitation(
    invitation_id: uuid.UUID,
    db: Annotated[AsyncSession, Depends(get_db)],
    current_user: Annotated[User, Depends(require_role("ADMIN", "HIRING_MANAGER"))],
) -> None:
    """Revoke an invitation."""
    result = await db.execute(
        select(Invitation).where(Invitation.id == invitation_id)
    )
    invitation = result.scalar_one_or_none()

    if not invitation:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Invitation not found",
        )

    if invitation.organization_id != current_user.organization_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to access this invitation",
        )

    if invitation.status == InvitationStatus.COMPLETED:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Cannot revoke a completed invitation",
        )

    invitation.status = InvitationStatus.REVOKED
    await db.commit()
