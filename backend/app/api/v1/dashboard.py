"""Dashboard API endpoints."""

from typing import Annotated

from fastapi import APIRouter, Depends
from pydantic import BaseModel
from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import AsyncSession

from app.dependencies import get_db, get_current_user
from app.models import User, Candidate, RoleProfile, Trait, ScoringRubric, TopPerformer, InterviewSession

router = APIRouter()


class DashboardStats(BaseModel):
    """Dashboard statistics response."""
    total_candidates: int
    role_profiles: int
    traits: int
    rubrics: int
    top_performers: int
    interviews_completed: int
    interviews_in_progress: int


@router.get("/stats", response_model=DashboardStats)
async def get_dashboard_stats(
    db: Annotated[AsyncSession, Depends(get_db)],
    current_user: Annotated[User, Depends(get_current_user)],
) -> DashboardStats:
    """Get dashboard statistics for the current user's organization."""
    org_id = current_user.organization_id

    # Count candidates
    candidates_result = await db.execute(
        select(func.count(Candidate.id)).where(
            Candidate.organization_id == org_id,
            Candidate.is_active == True
        )
    )
    total_candidates = candidates_result.scalar() or 0

    # Count role profiles (org-specific + templates)
    roles_result = await db.execute(
        select(func.count(RoleProfile.id)).where(
            RoleProfile.is_active == True,
            (RoleProfile.organization_id == org_id) | (RoleProfile.is_template == True)
        )
    )
    role_profiles = roles_result.scalar() or 0

    # Count traits (global - not org-specific)
    traits_result = await db.execute(
        select(func.count(Trait.id))
    )
    traits = traits_result.scalar() or 0

    # Count rubrics (default + org-specific)
    rubrics_result = await db.execute(
        select(func.count(ScoringRubric.id)).where(
            (ScoringRubric.organization_id == org_id) | (ScoringRubric.is_default == True)
        )
    )
    rubrics = rubrics_result.scalar() or 0

    # Count top performers
    performers_result = await db.execute(
        select(func.count(TopPerformer.id)).where(
            TopPerformer.organization_id == org_id,
            TopPerformer.is_active == True
        )
    )
    top_performers = performers_result.scalar() or 0

    # Count completed interviews
    completed_result = await db.execute(
        select(func.count(InterviewSession.id)).where(
            InterviewSession.status == "COMPLETED"
        ).join(Candidate).where(Candidate.organization_id == org_id)
    )
    interviews_completed = completed_result.scalar() or 0

    # Count in-progress interviews
    in_progress_result = await db.execute(
        select(func.count(InterviewSession.id)).where(
            InterviewSession.status == "IN_PROGRESS"
        ).join(Candidate).where(Candidate.organization_id == org_id)
    )
    interviews_in_progress = in_progress_result.scalar() or 0

    return DashboardStats(
        total_candidates=total_candidates,
        role_profiles=role_profiles,
        traits=traits,
        rubrics=rubrics,
        top_performers=top_performers,
        interviews_completed=interviews_completed,
        interviews_in_progress=interviews_in_progress,
    )
