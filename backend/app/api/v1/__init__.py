"""API v1 router configuration."""

from fastapi import APIRouter

from app.api.v1 import (
    auth,
    organizations,
    users,
    traits,
    roles,
    rubrics,
    interviews,
    candidates,
    compliance,
    profiling,
    invitations,
    public,
    dashboard,
    jobs,
)

router = APIRouter()

# Public routes (no authentication required)
router.include_router(public.router, prefix="/public", tags=["Public/Self-Service"])

# Authenticated routes
router.include_router(auth.router, prefix="/auth", tags=["Authentication"])
router.include_router(organizations.router, prefix="/organizations", tags=["Organizations"])
router.include_router(users.router, prefix="/users", tags=["Users"])
router.include_router(candidates.router, prefix="/candidates", tags=["Candidates"])
router.include_router(traits.router, prefix="/traits", tags=["Traits"])
router.include_router(roles.router, prefix="/roles", tags=["Role Profiles"])
router.include_router(rubrics.router, prefix="/rubrics", tags=["Rubrics"])
router.include_router(interviews.router, prefix="/interviews", tags=["Interviews"])
router.include_router(invitations.router, prefix="/invitations", tags=["Invitations"])
router.include_router(compliance.router, prefix="/compliance", tags=["Compliance"])
router.include_router(profiling.router, prefix="/profiling", tags=["Profile Development"])
router.include_router(dashboard.router, prefix="/dashboard", tags=["Dashboard"])
router.include_router(jobs.router, prefix="/jobs", tags=["Jobs"])
