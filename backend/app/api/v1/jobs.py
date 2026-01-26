"""Job endpoints."""

from typing import Annotated, Optional
import uuid
from datetime import datetime

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.dependencies import get_db, get_current_user, require_role
from app.models import Job, JobStatus, User, RoleProfile
from app.schemas.job import (
    JobCreate,
    JobUpdate,
    JobResponse,
    JobList,
    JobWithRoleProfile,
    ExtractedRequirements,
)

router = APIRouter()


@router.get("", response_model=JobList)
async def list_jobs(
    db: Annotated[AsyncSession, Depends(get_db)],
    current_user: Annotated[User, Depends(get_current_user)],
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=100),
    search: Optional[str] = None,
    status_filter: Optional[JobStatus] = Query(None, alias="status"),
) -> JobList:
    """List jobs for the current organization."""
    query = select(Job).where(Job.organization_id == current_user.organization_id)

    if status_filter:
        query = query.where(Job.status == status_filter)

    if search:
        query = query.where(
            Job.title.ilike(f"%{search}%") | Job.description.ilike(f"%{search}%")
        )

    # Count total
    count_query = select(func.count()).select_from(query.subquery())
    total = (await db.execute(count_query)).scalar_one()

    # Get items
    query = query.offset(skip).limit(limit).order_by(Job.created_at.desc())
    result = await db.execute(query)
    items = result.scalars().all()

    return JobList(items=items, total=total)


@router.post("", response_model=JobResponse, status_code=status.HTTP_201_CREATED)
async def create_job(
    job_in: JobCreate,
    db: Annotated[AsyncSession, Depends(get_db)],
    current_user: Annotated[User, Depends(require_role("ADMIN", "HIRING_MANAGER"))],
) -> Job:
    """Create a new job posting."""
    job_data = job_in.model_dump()

    # Validate role_profile_id if provided
    if job_data.get("role_profile_id"):
        result = await db.execute(
            select(RoleProfile).where(RoleProfile.id == job_data["role_profile_id"])
        )
        role_profile = result.scalar_one_or_none()
        if not role_profile:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Role profile not found",
            )
        # Check access to role profile
        if not current_user.is_superuser and not role_profile.is_template:
            if role_profile.organization_id != current_user.organization_id:
                raise HTTPException(
                    status_code=status.HTTP_403_FORBIDDEN,
                    detail="Not authorized to use this role profile",
                )

    job = Job(
        **job_data,
        organization_id=current_user.organization_id,
        created_by_id=current_user.id,
    )
    db.add(job)
    await db.commit()
    await db.refresh(job)
    return job


@router.get("/{job_id}", response_model=JobWithRoleProfile)
async def get_job(
    job_id: uuid.UUID,
    db: Annotated[AsyncSession, Depends(get_db)],
    current_user: Annotated[User, Depends(get_current_user)],
) -> dict:
    """Get job by ID with role profile details."""
    result = await db.execute(
        select(Job)
        .where(Job.id == job_id)
        .options(selectinload(Job.role_profile))
    )
    job = result.scalar_one_or_none()

    if not job:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Job not found",
        )

    # Check access
    if not current_user.is_superuser:
        if job.organization_id != current_user.organization_id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Not authorized to access this job",
            )

    # Build response with role profile details
    response = {
        "id": job.id,
        "organization_id": job.organization_id,
        "role_profile_id": job.role_profile_id,
        "title": job.title,
        "description": job.description,
        "department": job.department,
        "location": job.location,
        "employment_type": job.employment_type,
        "objective_requirements": job.objective_requirements,
        "nice_to_haves": job.nice_to_haves,
        "responsibilities": job.responsibilities,
        "suggested_traits": job.suggested_traits,
        "status": job.status,
        "created_by_id": job.created_by_id,
        "requirements_extracted_at": job.requirements_extracted_at,
        "extraction_model": job.extraction_model,
        "created_at": job.created_at,
        "updated_at": job.updated_at,
        "role_profile_name": job.role_profile.name if job.role_profile else None,
        "role_profile_category": job.role_profile.role_category if job.role_profile else None,
    }
    return response


@router.put("/{job_id}", response_model=JobResponse)
async def update_job(
    job_id: uuid.UUID,
    job_in: JobUpdate,
    db: Annotated[AsyncSession, Depends(get_db)],
    current_user: Annotated[User, Depends(require_role("ADMIN", "HIRING_MANAGER"))],
) -> Job:
    """Update job."""
    result = await db.execute(select(Job).where(Job.id == job_id))
    job = result.scalar_one_or_none()

    if not job:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Job not found",
        )

    # Check access
    if not current_user.is_superuser:
        if job.organization_id != current_user.organization_id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Not authorized to modify this job",
            )

    update_data = job_in.model_dump(exclude_unset=True)

    # Validate role_profile_id if being updated
    if "role_profile_id" in update_data and update_data["role_profile_id"]:
        result = await db.execute(
            select(RoleProfile).where(RoleProfile.id == update_data["role_profile_id"])
        )
        role_profile = result.scalar_one_or_none()
        if not role_profile:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Role profile not found",
            )

    for field, value in update_data.items():
        setattr(job, field, value)

    await db.commit()
    await db.refresh(job)
    return job


@router.delete("/{job_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_job(
    job_id: uuid.UUID,
    db: Annotated[AsyncSession, Depends(get_db)],
    current_user: Annotated[User, Depends(require_role("ADMIN"))],
) -> None:
    """Delete (archive) a job."""
    result = await db.execute(select(Job).where(Job.id == job_id))
    job = result.scalar_one_or_none()

    if not job:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Job not found",
        )

    # Check access
    if not current_user.is_superuser:
        if job.organization_id != current_user.organization_id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Not authorized to delete this job",
            )

    # Soft delete by setting status to CLOSED
    job.status = JobStatus.CLOSED
    await db.commit()


@router.post("/{job_id}/extract-requirements", response_model=ExtractedRequirements)
async def extract_requirements(
    job_id: uuid.UUID,
    db: Annotated[AsyncSession, Depends(get_db)],
    current_user: Annotated[User, Depends(require_role("ADMIN", "HIRING_MANAGER"))],
) -> ExtractedRequirements:
    """Extract requirements from job description using LLM.

    This endpoint analyzes the job description and extracts:
    - Objective requirements (education, experience, certifications, skills)
    - Nice-to-have qualifications
    - Key responsibilities
    - Suggested traits to assess
    """
    result = await db.execute(select(Job).where(Job.id == job_id))
    job = result.scalar_one_or_none()

    if not job:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Job not found",
        )

    # Check access
    if not current_user.is_superuser:
        if job.organization_id != current_user.organization_id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Not authorized to access this job",
            )

    # Import the analyzer service
    from app.services.job_analyzer import JobDescriptionAnalyzer

    analyzer = JobDescriptionAnalyzer()
    extracted = await analyzer.extract_requirements(
        job_title=job.title,
        job_description=job.description,
    )

    # Update the job with extracted data
    job.objective_requirements = extracted.objective_requirements
    job.nice_to_haves = extracted.nice_to_haves
    job.responsibilities = extracted.responsibilities
    job.suggested_traits = extracted.suggested_traits
    job.requirements_extracted_at = datetime.utcnow().isoformat()
    job.extraction_model = extracted.extraction_notes or "claude-sonnet-4-20250514"

    await db.commit()
    await db.refresh(job)

    return extracted


@router.post("/{job_id}/save-requirements", response_model=JobResponse)
async def save_requirements(
    job_id: uuid.UUID,
    requirements: ExtractedRequirements,
    db: Annotated[AsyncSession, Depends(get_db)],
    current_user: Annotated[User, Depends(require_role("ADMIN", "HIRING_MANAGER"))],
) -> Job:
    """Save manually edited requirements to a job."""
    result = await db.execute(select(Job).where(Job.id == job_id))
    job = result.scalar_one_or_none()

    if not job:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Job not found",
        )

    # Check access
    if not current_user.is_superuser:
        if job.organization_id != current_user.organization_id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Not authorized to modify this job",
            )

    # Update requirements
    job.objective_requirements = requirements.objective_requirements
    job.nice_to_haves = requirements.nice_to_haves
    job.responsibilities = requirements.responsibilities
    job.suggested_traits = requirements.suggested_traits

    await db.commit()
    await db.refresh(job)
    return job
