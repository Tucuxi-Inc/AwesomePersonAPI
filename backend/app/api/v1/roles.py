"""Role profile endpoints."""

from typing import Annotated, Optional
import uuid

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import AsyncSession

from app.dependencies import get_db, get_current_user, require_role
from app.models import RoleProfile, User
from app.schemas.role_profile import (
    RoleProfileCreate,
    RoleProfileUpdate,
    RoleProfileResponse,
    RoleProfileList,
    RoleProfileClone,
)

router = APIRouter()


@router.get("", response_model=RoleProfileList)
async def list_role_profiles(
    db: Annotated[AsyncSession, Depends(get_db)],
    current_user: Annotated[User, Depends(get_current_user)],
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=100),
    search: Optional[str] = None,
    templates_only: bool = False,
) -> RoleProfileList:
    """List role profiles."""
    query = select(RoleProfile).where(RoleProfile.is_active == True)

    # Filter by organization or templates
    if templates_only:
        query = query.where(RoleProfile.is_template == True)
    elif not current_user.is_superuser:
        query = query.where(
            (RoleProfile.organization_id == current_user.organization_id) |
            (RoleProfile.is_template == True)
        )

    if search:
        query = query.where(RoleProfile.name.ilike(f"%{search}%"))

    # Count total
    count_query = select(func.count()).select_from(query.subquery())
    total = (await db.execute(count_query)).scalar_one()

    # Get items
    query = query.offset(skip).limit(limit).order_by(RoleProfile.name)
    result = await db.execute(query)
    items = result.scalars().all()

    return RoleProfileList(items=items, total=total)


@router.post("", response_model=RoleProfileResponse, status_code=status.HTTP_201_CREATED)
async def create_role_profile(
    profile_in: RoleProfileCreate,
    db: Annotated[AsyncSession, Depends(get_db)],
    current_user: Annotated[User, Depends(require_role("ADMIN", "HIRING_MANAGER"))],
) -> RoleProfile:
    """Create a new role profile."""
    profile_data = profile_in.model_dump()

    # Only superusers can create templates
    if profile_data.get("is_template") and not current_user.is_superuser:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Only superusers can create templates",
        )

    profile = RoleProfile(
        **profile_data,
        organization_id=current_user.organization_id if not profile_data.get("is_template") else None,
    )
    db.add(profile)
    await db.commit()
    await db.refresh(profile)
    return profile


@router.get("/{profile_id}", response_model=RoleProfileResponse)
async def get_role_profile(
    profile_id: uuid.UUID,
    db: Annotated[AsyncSession, Depends(get_db)],
    current_user: Annotated[User, Depends(get_current_user)],
) -> RoleProfile:
    """Get role profile by ID."""
    result = await db.execute(select(RoleProfile).where(RoleProfile.id == profile_id))
    profile = result.scalar_one_or_none()

    if not profile:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Role profile not found",
        )

    # Check access
    if not current_user.is_superuser and not profile.is_template:
        if profile.organization_id != current_user.organization_id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Not authorized to access this role profile",
            )

    return profile


@router.put("/{profile_id}", response_model=RoleProfileResponse)
async def update_role_profile(
    profile_id: uuid.UUID,
    profile_in: RoleProfileUpdate,
    db: Annotated[AsyncSession, Depends(get_db)],
    current_user: Annotated[User, Depends(require_role("ADMIN", "HIRING_MANAGER"))],
) -> RoleProfile:
    """Update role profile."""
    result = await db.execute(select(RoleProfile).where(RoleProfile.id == profile_id))
    profile = result.scalar_one_or_none()

    if not profile:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Role profile not found",
        )

    # Check access
    if not current_user.is_superuser:
        if profile.organization_id != current_user.organization_id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Not authorized to modify this role profile",
            )

    update_data = profile_in.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(profile, field, value)

    await db.commit()
    await db.refresh(profile)
    return profile


@router.post("/{profile_id}/clone", response_model=RoleProfileResponse, status_code=status.HTTP_201_CREATED)
async def clone_role_profile(
    profile_id: uuid.UUID,
    clone_in: RoleProfileClone,
    db: Annotated[AsyncSession, Depends(get_db)],
    current_user: Annotated[User, Depends(require_role("ADMIN", "HIRING_MANAGER"))],
) -> RoleProfile:
    """Clone a role profile (including templates)."""
    result = await db.execute(select(RoleProfile).where(RoleProfile.id == profile_id))
    source_profile = result.scalar_one_or_none()

    if not source_profile:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Source role profile not found",
        )

    # Check access
    if not current_user.is_superuser and not source_profile.is_template:
        if source_profile.organization_id != current_user.organization_id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Not authorized to clone this role profile",
            )

    # Create clone
    new_profile = RoleProfile(
        name=clone_in.name,
        description=clone_in.description or source_profile.description,
        department=source_profile.department,
        level=source_profile.level,
        role_category=source_profile.role_category,
        critical_traits=source_profile.critical_traits,
        positive_traits=source_profile.positive_traits,
        counter_indicators=source_profile.counter_indicators,
        valence_notes=source_profile.valence_notes,
        organization_id=current_user.organization_id,
        is_template=False,
        derived_from=source_profile.id,
        derivation_notes=f"Cloned from: {source_profile.name}",
    )
    db.add(new_profile)
    await db.commit()
    await db.refresh(new_profile)
    return new_profile


@router.delete("/{profile_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_role_profile(
    profile_id: uuid.UUID,
    db: Annotated[AsyncSession, Depends(get_db)],
    current_user: Annotated[User, Depends(require_role("ADMIN"))],
) -> None:
    """Delete role profile."""
    result = await db.execute(select(RoleProfile).where(RoleProfile.id == profile_id))
    profile = result.scalar_one_or_none()

    if not profile:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Role profile not found",
        )

    # Check access
    if not current_user.is_superuser:
        if profile.organization_id != current_user.organization_id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Not authorized to delete this role profile",
            )

    await db.delete(profile)
    await db.commit()
