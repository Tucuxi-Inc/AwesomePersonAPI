"""Trait endpoints (read-only, seeded data)."""

from typing import Annotated, List, Optional
import uuid

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.dependencies import get_db, get_current_user
from app.models import Trait, TraitValenceMapping, User
from app.schemas.trait import (
    TraitResponse,
    TraitDetailResponse,
    TraitList,
    TraitCategoryResponse,
)
from app.data.traits import TRAIT_CATEGORIES

router = APIRouter()


@router.get("", response_model=TraitList)
async def list_traits(
    db: Annotated[AsyncSession, Depends(get_db)],
    current_user: Annotated[User, Depends(get_current_user)],
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=100),
    category: Optional[str] = None,
    search: Optional[str] = None,
) -> TraitList:
    """List all traits."""
    query = select(Trait)

    if category:
        query = query.where(Trait.category == category)

    if search:
        query = query.where(Trait.name.ilike(f"%{search}%"))

    # Count total
    count_query = select(func.count()).select_from(query.subquery())
    total = (await db.execute(count_query)).scalar_one()

    # Get items
    query = query.offset(skip).limit(limit).order_by(Trait.category, Trait.display_order)
    result = await db.execute(query)
    items = result.scalars().all()

    return TraitList(items=items, total=total)


@router.get("/categories", response_model=List[TraitCategoryResponse])
async def list_trait_categories(
    db: Annotated[AsyncSession, Depends(get_db)],
    current_user: Annotated[User, Depends(get_current_user)],
) -> List[TraitCategoryResponse]:
    """List traits organized by category."""
    categories = []

    for category_name in TRAIT_CATEGORIES:
        query = select(Trait).where(Trait.category == category_name).order_by(Trait.display_order)
        result = await db.execute(query)
        traits = result.scalars().all()

        categories.append(TraitCategoryResponse(
            name=category_name,
            traits=traits,
        ))

    return categories


@router.get("/{trait_id}", response_model=TraitDetailResponse)
async def get_trait(
    trait_id: uuid.UUID,
    db: Annotated[AsyncSession, Depends(get_db)],
    current_user: Annotated[User, Depends(get_current_user)],
) -> Trait:
    """Get trait with valence mappings."""
    query = (
        select(Trait)
        .where(Trait.id == trait_id)
        .options(selectinload(Trait.valence_mappings))
    )
    result = await db.execute(query)
    trait = result.scalar_one_or_none()

    if not trait:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Trait not found",
        )

    return trait


@router.get("/name/{trait_name}", response_model=TraitDetailResponse)
async def get_trait_by_name(
    trait_name: str,
    db: Annotated[AsyncSession, Depends(get_db)],
    current_user: Annotated[User, Depends(get_current_user)],
) -> Trait:
    """Get trait by name with valence mappings."""
    query = (
        select(Trait)
        .where(Trait.name == trait_name)
        .options(selectinload(Trait.valence_mappings))
    )
    result = await db.execute(query)
    trait = result.scalar_one_or_none()

    if not trait:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Trait not found",
        )

    return trait
