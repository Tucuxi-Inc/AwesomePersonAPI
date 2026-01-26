"""API v1 router configuration."""

from fastapi import APIRouter

from app.api.v1 import auth, organizations, users, traits, roles, rubrics, interviews

router = APIRouter()

router.include_router(auth.router, prefix="/auth", tags=["Authentication"])
router.include_router(organizations.router, prefix="/organizations", tags=["Organizations"])
router.include_router(users.router, prefix="/users", tags=["Users"])
router.include_router(traits.router, prefix="/traits", tags=["Traits"])
router.include_router(roles.router, prefix="/roles", tags=["Role Profiles"])
router.include_router(rubrics.router, prefix="/rubrics", tags=["Rubrics"])
router.include_router(interviews.router, prefix="/interviews", tags=["Interviews"])
