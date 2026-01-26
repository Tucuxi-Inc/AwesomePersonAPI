"""Scoring rubric endpoints."""

from typing import Annotated, Optional
import uuid

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import AsyncSession

from app.dependencies import get_db, get_current_user, require_role
from app.models import ScoringRubric, User
from app.schemas.rubric import (
    RubricCreate,
    RubricUpdate,
    RubricResponse,
    RubricList,
    RubricClone,
)

router = APIRouter()


@router.get("", response_model=RubricList)
async def list_rubrics(
    db: Annotated[AsyncSession, Depends(get_db)],
    current_user: Annotated[User, Depends(get_current_user)],
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=100),
    trait_id: Optional[uuid.UUID] = None,
    role_profile_id: Optional[uuid.UUID] = None,
    defaults_only: bool = False,
) -> RubricList:
    """List scoring rubrics."""
    query = select(ScoringRubric).where(ScoringRubric.is_active == True)

    # Filter by defaults or organization
    if defaults_only:
        query = query.where(ScoringRubric.is_default == True)
    elif not current_user.is_superuser:
        query = query.where(
            (ScoringRubric.organization_id == current_user.organization_id) |
            (ScoringRubric.is_default == True)
        )

    if trait_id:
        query = query.where(ScoringRubric.trait_id == trait_id)

    if role_profile_id:
        query = query.where(ScoringRubric.role_profile_id == role_profile_id)

    # Count total
    count_query = select(func.count()).select_from(query.subquery())
    total = (await db.execute(count_query)).scalar_one()

    # Get items
    query = query.offset(skip).limit(limit).order_by(ScoringRubric.name)
    result = await db.execute(query)
    items = result.scalars().all()

    return RubricList(items=items, total=total)


@router.get("/defaults", response_model=RubricList)
async def list_default_rubrics(
    db: Annotated[AsyncSession, Depends(get_db)],
    current_user: Annotated[User, Depends(get_current_user)],
) -> RubricList:
    """List research-based default rubrics."""
    query = (
        select(ScoringRubric)
        .where(ScoringRubric.is_default == True)
        .where(ScoringRubric.is_active == True)
        .order_by(ScoringRubric.name)
    )
    result = await db.execute(query)
    items = result.scalars().all()

    return RubricList(items=items, total=len(items))


@router.post("", response_model=RubricResponse, status_code=status.HTTP_201_CREATED)
async def create_rubric(
    rubric_in: RubricCreate,
    db: Annotated[AsyncSession, Depends(get_db)],
    current_user: Annotated[User, Depends(require_role("ADMIN", "HIRING_MANAGER"))],
) -> ScoringRubric:
    """Create a new scoring rubric."""
    rubric_data = rubric_in.model_dump()

    rubric = ScoringRubric(
        **rubric_data,
        organization_id=current_user.organization_id,
        is_default=False,
    )
    db.add(rubric)
    await db.commit()
    await db.refresh(rubric)
    return rubric


@router.get("/{rubric_id}", response_model=RubricResponse)
async def get_rubric(
    rubric_id: uuid.UUID,
    db: Annotated[AsyncSession, Depends(get_db)],
    current_user: Annotated[User, Depends(get_current_user)],
) -> ScoringRubric:
    """Get scoring rubric by ID."""
    result = await db.execute(select(ScoringRubric).where(ScoringRubric.id == rubric_id))
    rubric = result.scalar_one_or_none()

    if not rubric:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Rubric not found",
        )

    # Check access
    if not current_user.is_superuser and not rubric.is_default:
        if rubric.organization_id != current_user.organization_id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Not authorized to access this rubric",
            )

    return rubric


@router.put("/{rubric_id}", response_model=RubricResponse)
async def update_rubric(
    rubric_id: uuid.UUID,
    rubric_in: RubricUpdate,
    db: Annotated[AsyncSession, Depends(get_db)],
    current_user: Annotated[User, Depends(require_role("ADMIN", "HIRING_MANAGER"))],
) -> ScoringRubric:
    """Update scoring rubric."""
    result = await db.execute(select(ScoringRubric).where(ScoringRubric.id == rubric_id))
    rubric = result.scalar_one_or_none()

    if not rubric:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Rubric not found",
        )

    # Cannot modify default rubrics
    if rubric.is_default:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Cannot modify default rubrics. Clone first.",
        )

    # Check access
    if not current_user.is_superuser:
        if rubric.organization_id != current_user.organization_id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Not authorized to modify this rubric",
            )

    update_data = rubric_in.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(rubric, field, value)

    # Increment version
    rubric.version += 1

    await db.commit()
    await db.refresh(rubric)
    return rubric


@router.post("/{rubric_id}/clone", response_model=RubricResponse, status_code=status.HTTP_201_CREATED)
async def clone_rubric(
    rubric_id: uuid.UUID,
    clone_in: RubricClone,
    db: Annotated[AsyncSession, Depends(get_db)],
    current_user: Annotated[User, Depends(require_role("ADMIN", "HIRING_MANAGER"))],
) -> ScoringRubric:
    """Clone a scoring rubric (including defaults)."""
    result = await db.execute(select(ScoringRubric).where(ScoringRubric.id == rubric_id))
    source_rubric = result.scalar_one_or_none()

    if not source_rubric:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Source rubric not found",
        )

    # Check access
    if not current_user.is_superuser and not source_rubric.is_default:
        if source_rubric.organization_id != current_user.organization_id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Not authorized to clone this rubric",
            )

    # Create clone
    new_rubric = ScoringRubric(
        name=clone_in.name,
        description=clone_in.description or source_rubric.description,
        trait_id=source_rubric.trait_id,
        behavioral_anchors=source_rubric.behavioral_anchors,
        primary_probes=source_rubric.primary_probes,
        follow_up_probes=source_rubric.follow_up_probes,
        star_indicators=source_rubric.star_indicators,
        organization_id=current_user.organization_id,
        role_profile_id=clone_in.role_profile_id,
        is_default=False,
        version=1,
        derived_from=source_rubric.id,
        derivation_notes=f"Cloned from: {source_rubric.name}",
    )
    db.add(new_rubric)
    await db.commit()
    await db.refresh(new_rubric)
    return new_rubric


@router.delete("/{rubric_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_rubric(
    rubric_id: uuid.UUID,
    db: Annotated[AsyncSession, Depends(get_db)],
    current_user: Annotated[User, Depends(require_role("ADMIN"))],
) -> None:
    """Delete scoring rubric."""
    result = await db.execute(select(ScoringRubric).where(ScoringRubric.id == rubric_id))
    rubric = result.scalar_one_or_none()

    if not rubric:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Rubric not found",
        )

    # Cannot delete default rubrics
    if rubric.is_default:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Cannot delete default rubrics",
        )

    # Check access
    if not current_user.is_superuser:
        if rubric.organization_id != current_user.organization_id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Not authorized to delete this rubric",
            )

    await db.delete(rubric)
    await db.commit()
