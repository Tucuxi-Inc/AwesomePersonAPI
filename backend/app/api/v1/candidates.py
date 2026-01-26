"""Candidate endpoints."""

from typing import Annotated, Optional
import uuid

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import AsyncSession

from app.dependencies import get_db, get_current_user
from app.models import User, Candidate
from app.schemas.candidate import (
    CandidateCreate,
    CandidateUpdate,
    CandidateResponse,
    CandidateList,
)

router = APIRouter()


@router.get("", response_model=CandidateList)
async def list_candidates(
    db: Annotated[AsyncSession, Depends(get_db)],
    current_user: Annotated[User, Depends(get_current_user)],
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=100),
    search: Optional[str] = None,
    status: Optional[str] = None,
) -> CandidateList:
    """List candidates for the current user's organization."""
    query = select(Candidate).where(Candidate.is_active == True)

    # Filter by organization (non-superusers see only their org)
    if not current_user.is_superuser:
        query = query.where(Candidate.organization_id == current_user.organization_id)

    # Search by name or email
    if search:
        query = query.where(
            (Candidate.full_name.ilike(f"%{search}%")) |
            (Candidate.email.ilike(f"%{search}%"))
        )

    # Filter by status
    if status:
        query = query.where(Candidate.status == status)

    # Count total
    count_query = select(func.count()).select_from(query.subquery())
    total = (await db.execute(count_query)).scalar_one()

    # Get items
    query = query.offset(skip).limit(limit).order_by(Candidate.created_at.desc())
    result = await db.execute(query)
    items = result.scalars().all()

    return CandidateList(items=items, total=total)


@router.post("", response_model=CandidateResponse, status_code=status.HTTP_201_CREATED)
async def create_candidate(
    candidate_in: CandidateCreate,
    db: Annotated[AsyncSession, Depends(get_db)],
    current_user: Annotated[User, Depends(get_current_user)],
) -> Candidate:
    """Create a new candidate."""
    # Check if email exists in org
    result = await db.execute(
        select(Candidate).where(
            Candidate.email == candidate_in.email,
            Candidate.organization_id == current_user.organization_id,
        )
    )
    if result.scalar_one_or_none():
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Candidate with this email already exists in your organization",
        )

    candidate_data = candidate_in.model_dump()
    candidate = Candidate(
        **candidate_data,
        organization_id=current_user.organization_id,
        status="NEW",
    )
    db.add(candidate)
    await db.commit()
    await db.refresh(candidate)
    return candidate


@router.get("/{candidate_id}", response_model=CandidateResponse)
async def get_candidate(
    candidate_id: uuid.UUID,
    db: Annotated[AsyncSession, Depends(get_db)],
    current_user: Annotated[User, Depends(get_current_user)],
) -> Candidate:
    """Get candidate by ID."""
    result = await db.execute(select(Candidate).where(Candidate.id == candidate_id))
    candidate = result.scalar_one_or_none()

    if not candidate:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Candidate not found",
        )

    # Check access
    if not current_user.is_superuser:
        if current_user.organization_id != candidate.organization_id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Not authorized to access this candidate",
            )

    return candidate


@router.put("/{candidate_id}", response_model=CandidateResponse)
async def update_candidate(
    candidate_id: uuid.UUID,
    candidate_in: CandidateUpdate,
    db: Annotated[AsyncSession, Depends(get_db)],
    current_user: Annotated[User, Depends(get_current_user)],
) -> Candidate:
    """Update candidate."""
    result = await db.execute(select(Candidate).where(Candidate.id == candidate_id))
    candidate = result.scalar_one_or_none()

    if not candidate:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Candidate not found",
        )

    # Check access
    if not current_user.is_superuser:
        if current_user.organization_id != candidate.organization_id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Not authorized to modify this candidate",
            )

    update_data = candidate_in.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(candidate, field, value)

    await db.commit()
    await db.refresh(candidate)
    return candidate


@router.delete("/{candidate_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_candidate(
    candidate_id: uuid.UUID,
    db: Annotated[AsyncSession, Depends(get_db)],
    current_user: Annotated[User, Depends(get_current_user)],
) -> None:
    """Soft-delete candidate (mark as inactive)."""
    result = await db.execute(select(Candidate).where(Candidate.id == candidate_id))
    candidate = result.scalar_one_or_none()

    if not candidate:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Candidate not found",
        )

    # Check access
    if not current_user.is_superuser:
        if current_user.organization_id != candidate.organization_id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Not authorized to delete this candidate",
            )

    # Soft delete
    candidate.is_active = False
    await db.commit()
