"""Job endpoints."""

from typing import Annotated, Optional
import uuid
from datetime import datetime, timezone

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy import select, func, and_
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.dependencies import get_db, get_current_user, require_role
from app.models import (
    Job,
    JobStatus,
    User,
    RoleProfile,
    Candidate,
    Resume,
    ResumeParseStatus,
    CandidateJobScreening,
    QualificationStatus,
)
from app.schemas.job import (
    JobCreate,
    JobUpdate,
    JobResponse,
    JobList,
    JobWithRoleProfile,
    ExtractedRequirements,
)
from app.schemas.screening import (
    ScreenCandidateRequest,
    ScreeningResponse,
    ScreeningSummary,
    QualifiedCandidatesList,
    GapAnalysisCandidatesList,
    OverrideRequest,
    OverrideResponse,
    JobCandidatesStats,
)
from app.services.qualification_screener import get_qualification_screener

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


# === Candidate Screening Endpoints ===

@router.post("/{job_id}/screen-candidate/{candidate_id}", response_model=ScreeningResponse)
async def screen_candidate(
    job_id: uuid.UUID,
    candidate_id: uuid.UUID,
    request: ScreenCandidateRequest,
    db: Annotated[AsyncSession, Depends(get_db)],
    current_user: Annotated[User, Depends(require_role("ADMIN", "HIRING_MANAGER", "INTERVIEWER"))],
) -> CandidateJobScreening:
    """Screen a candidate's resume against job requirements.

    This endpoint compares the candidate's resume against the job's objective
    requirements and determines if they are QUALIFIED, NOT_QUALIFIED, or NEEDS_REVIEW.
    """
    # Get job
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

    # Get candidate
    result = await db.execute(select(Candidate).where(Candidate.id == candidate_id))
    candidate = result.scalar_one_or_none()

    if not candidate:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Candidate not found",
        )

    if not current_user.is_superuser:
        if candidate.organization_id != current_user.organization_id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Not authorized to access this candidate",
            )

    # Get resume
    if request.resume_id:
        result = await db.execute(
            select(Resume).where(
                Resume.id == request.resume_id,
                Resume.candidate_id == candidate_id,
            )
        )
        resume = result.scalar_one_or_none()
    else:
        # Get primary resume
        result = await db.execute(
            select(Resume).where(
                Resume.candidate_id == candidate_id,
                Resume.is_primary == True,
            )
        )
        resume = result.scalar_one_or_none()

    if not resume:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="No resume found for this candidate. Please upload a resume first.",
        )

    if resume.parse_status != ResumeParseStatus.PARSED:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Resume is not ready for screening. Status: {resume.parse_status.value}",
        )

    if not resume.parsed_data:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Resume has not been analyzed yet. Please wait for processing to complete.",
        )

    # Check if screening already exists
    result = await db.execute(
        select(CandidateJobScreening).where(
            CandidateJobScreening.candidate_id == candidate_id,
            CandidateJobScreening.job_id == job_id,
        )
    )
    existing = result.scalar_one_or_none()

    # If no requirements, auto-qualify
    if not job.objective_requirements:
        if existing:
            existing.qualification_status = QualificationStatus.QUALIFIED
            existing.requirement_results = []
            existing.gaps = []
            existing.gap_count = 0
            existing.resume_id = resume.id
            existing.screened_at = datetime.now(timezone.utc)
            await db.commit()
            await db.refresh(existing)
            return existing
        else:
            screening = CandidateJobScreening(
                candidate_id=candidate_id,
                job_id=job_id,
                resume_id=resume.id,
                qualification_status=QualificationStatus.QUALIFIED,
                requirement_results=[],
                gaps=[],
                gap_count=0,
                screened_at=datetime.now(timezone.utc),
            )
            db.add(screening)
            await db.commit()
            await db.refresh(screening)
            return screening

    # Screen using LLM
    screener = get_qualification_screener()
    qualification_status, requirement_results, gaps = await screener.screen(
        parsed_resume=resume.parsed_data,
        job_requirements=job.objective_requirements,
    )

    # Map status string to enum
    status_map = {
        "QUALIFIED": QualificationStatus.QUALIFIED,
        "NOT_QUALIFIED": QualificationStatus.NOT_QUALIFIED,
        "NEEDS_REVIEW": QualificationStatus.NEEDS_REVIEW,
    }
    qual_status = status_map.get(qualification_status, QualificationStatus.NEEDS_REVIEW)

    if existing:
        # Update existing screening
        existing.resume_id = resume.id
        existing.qualification_status = qual_status
        existing.requirement_results = requirement_results
        existing.gaps = gaps
        existing.gap_count = len(gaps)
        existing.screened_at = datetime.now(timezone.utc)
        await db.commit()
        await db.refresh(existing)
        return existing
    else:
        # Create new screening
        screening = CandidateJobScreening(
            candidate_id=candidate_id,
            job_id=job_id,
            resume_id=resume.id,
            qualification_status=qual_status,
            requirement_results=requirement_results,
            gaps=gaps,
            gap_count=len(gaps),
            screened_at=datetime.now(timezone.utc),
        )
        db.add(screening)
        await db.commit()
        await db.refresh(screening)
        return screening


@router.get("/{job_id}/candidates/stats", response_model=JobCandidatesStats)
async def get_job_candidates_stats(
    job_id: uuid.UUID,
    db: Annotated[AsyncSession, Depends(get_db)],
    current_user: Annotated[User, Depends(get_current_user)],
) -> JobCandidatesStats:
    """Get statistics about candidates screened for this job."""
    # Get job
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

    # Count by status
    result = await db.execute(
        select(
            func.count().filter(CandidateJobScreening.qualification_status == QualificationStatus.QUALIFIED),
            func.count().filter(CandidateJobScreening.qualification_status == QualificationStatus.NOT_QUALIFIED),
            func.count().filter(CandidateJobScreening.qualification_status == QualificationStatus.NEEDS_REVIEW),
            func.count().filter(CandidateJobScreening.qualification_status == QualificationStatus.PENDING),
            func.count().filter(CandidateJobScreening.admin_override == True),
            func.count(),
        ).where(CandidateJobScreening.job_id == job_id)
    )
    stats = result.one()

    return JobCandidatesStats(
        qualified=stats[0],
        not_qualified=stats[1],
        needs_review=stats[2],
        pending=stats[3],
        overridden=stats[4],
        total=stats[5],
    )


@router.get("/{job_id}/candidates/qualified", response_model=QualifiedCandidatesList)
async def list_qualified_candidates(
    job_id: uuid.UUID,
    db: Annotated[AsyncSession, Depends(get_db)],
    current_user: Annotated[User, Depends(get_current_user)],
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=100),
) -> QualifiedCandidatesList:
    """List candidates who are qualified for this job (ready for interview)."""
    # Get job
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

    # Query qualified candidates (including overridden)
    query = (
        select(CandidateJobScreening, Candidate)
        .join(Candidate, CandidateJobScreening.candidate_id == Candidate.id)
        .where(
            CandidateJobScreening.job_id == job_id,
            (CandidateJobScreening.qualification_status == QualificationStatus.QUALIFIED) |
            (CandidateJobScreening.admin_override == True)
        )
        .order_by(CandidateJobScreening.screened_at.desc())
    )

    # Count
    count_query = select(func.count()).select_from(query.subquery())
    total = (await db.execute(count_query)).scalar_one()

    # Get items
    query = query.offset(skip).limit(limit)
    result = await db.execute(query)
    rows = result.all()

    items = [
        ScreeningSummary(
            id=screening.id,
            candidate_id=screening.candidate_id,
            candidate_name=candidate.full_name,
            candidate_email=candidate.email,
            qualification_status=screening.qualification_status.value,
            gap_count=screening.gap_count,
            admin_override=screening.admin_override,
            screened_at=screening.screened_at,
        )
        for screening, candidate in rows
    ]

    return QualifiedCandidatesList(items=items, total=total)


@router.get("/{job_id}/candidates/gaps", response_model=GapAnalysisCandidatesList)
async def list_candidates_with_gaps(
    job_id: uuid.UUID,
    db: Annotated[AsyncSession, Depends(get_db)],
    current_user: Annotated[User, Depends(get_current_user)],
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=100),
    sort_by: str = Query("gap_count", pattern="^(gap_count|screened_at|name)$"),
) -> GapAnalysisCandidatesList:
    """List candidates who are not qualified, sorted by gap count.

    Candidates with fewer gaps are closer to qualifying and may be candidates
    for admin override if their gaps are minor or circumstantial.
    """
    # Get job
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

    # Query not qualified candidates (excluding already overridden)
    query = (
        select(CandidateJobScreening, Candidate)
        .join(Candidate, CandidateJobScreening.candidate_id == Candidate.id)
        .where(
            CandidateJobScreening.job_id == job_id,
            CandidateJobScreening.qualification_status == QualificationStatus.NOT_QUALIFIED,
            CandidateJobScreening.admin_override == False,
        )
    )

    # Sort
    if sort_by == "gap_count":
        query = query.order_by(CandidateJobScreening.gap_count.asc())
    elif sort_by == "screened_at":
        query = query.order_by(CandidateJobScreening.screened_at.desc())
    elif sort_by == "name":
        query = query.order_by(Candidate.full_name.asc())

    # Count
    count_query = select(func.count()).select_from(query.subquery())
    total = (await db.execute(count_query)).scalar_one()

    # Get items
    query = query.offset(skip).limit(limit)
    result = await db.execute(query)
    rows = result.all()

    items = [
        ScreeningSummary(
            id=screening.id,
            candidate_id=screening.candidate_id,
            candidate_name=candidate.full_name,
            candidate_email=candidate.email,
            qualification_status=screening.qualification_status.value,
            gap_count=screening.gap_count,
            admin_override=screening.admin_override,
            screened_at=screening.screened_at,
        )
        for screening, candidate in rows
    ]

    return GapAnalysisCandidatesList(items=items, total=total)


@router.get("/{job_id}/candidates/needs-review", response_model=GapAnalysisCandidatesList)
async def list_candidates_needing_review(
    job_id: uuid.UUID,
    db: Annotated[AsyncSession, Depends(get_db)],
    current_user: Annotated[User, Depends(get_current_user)],
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=100),
) -> GapAnalysisCandidatesList:
    """List candidates who need manual review (unclear qualification status)."""
    # Get job
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

    # Query candidates needing review
    query = (
        select(CandidateJobScreening, Candidate)
        .join(Candidate, CandidateJobScreening.candidate_id == Candidate.id)
        .where(
            CandidateJobScreening.job_id == job_id,
            CandidateJobScreening.qualification_status == QualificationStatus.NEEDS_REVIEW,
            CandidateJobScreening.admin_override == False,
        )
        .order_by(CandidateJobScreening.screened_at.desc())
    )

    # Count
    count_query = select(func.count()).select_from(query.subquery())
    total = (await db.execute(count_query)).scalar_one()

    # Get items
    query = query.offset(skip).limit(limit)
    result = await db.execute(query)
    rows = result.all()

    items = [
        ScreeningSummary(
            id=screening.id,
            candidate_id=screening.candidate_id,
            candidate_name=candidate.full_name,
            candidate_email=candidate.email,
            qualification_status=screening.qualification_status.value,
            gap_count=screening.gap_count,
            admin_override=screening.admin_override,
            screened_at=screening.screened_at,
        )
        for screening, candidate in rows
    ]

    return GapAnalysisCandidatesList(items=items, total=total)


@router.get("/{job_id}/screening/{candidate_id}", response_model=ScreeningResponse)
async def get_screening_details(
    job_id: uuid.UUID,
    candidate_id: uuid.UUID,
    db: Annotated[AsyncSession, Depends(get_db)],
    current_user: Annotated[User, Depends(get_current_user)],
) -> CandidateJobScreening:
    """Get detailed screening results for a candidate."""
    # Get screening
    result = await db.execute(
        select(CandidateJobScreening).where(
            CandidateJobScreening.job_id == job_id,
            CandidateJobScreening.candidate_id == candidate_id,
        )
    )
    screening = result.scalar_one_or_none()

    if not screening:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Screening not found. Please screen the candidate first.",
        )

    # Get job for auth check
    result = await db.execute(select(Job).where(Job.id == job_id))
    job = result.scalar_one_or_none()

    if not current_user.is_superuser:
        if job.organization_id != current_user.organization_id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Not authorized to access this screening",
            )

    return screening


@router.post("/{job_id}/candidates/{candidate_id}/override", response_model=OverrideResponse)
async def override_qualification(
    job_id: uuid.UUID,
    candidate_id: uuid.UUID,
    request: OverrideRequest,
    db: Annotated[AsyncSession, Depends(get_db)],
    current_user: Annotated[User, Depends(require_role("ADMIN", "HIRING_MANAGER"))],
) -> CandidateJobScreening:
    """Override a candidate's qualification status to QUALIFIED.

    This allows admins to manually qualify candidates who didn't meet all
    objective requirements but are deemed suitable for interview.
    """
    # Get screening
    result = await db.execute(
        select(CandidateJobScreening).where(
            CandidateJobScreening.job_id == job_id,
            CandidateJobScreening.candidate_id == candidate_id,
        )
    )
    screening = result.scalar_one_or_none()

    if not screening:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Screening not found. Please screen the candidate first.",
        )

    # Get job for auth check
    result = await db.execute(select(Job).where(Job.id == job_id))
    job = result.scalar_one_or_none()

    if not current_user.is_superuser:
        if job.organization_id != current_user.organization_id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Not authorized to override this screening",
            )

    # Apply override
    screening.admin_override = True
    screening.override_by_id = current_user.id
    screening.override_reason = request.reason
    screening.override_at = datetime.now(timezone.utc)

    await db.commit()
    await db.refresh(screening)
    return screening


@router.delete("/{job_id}/candidates/{candidate_id}/override", status_code=status.HTTP_204_NO_CONTENT)
async def remove_override(
    job_id: uuid.UUID,
    candidate_id: uuid.UUID,
    db: Annotated[AsyncSession, Depends(get_db)],
    current_user: Annotated[User, Depends(require_role("ADMIN"))],
) -> None:
    """Remove an override from a candidate's qualification status."""
    # Get screening
    result = await db.execute(
        select(CandidateJobScreening).where(
            CandidateJobScreening.job_id == job_id,
            CandidateJobScreening.candidate_id == candidate_id,
        )
    )
    screening = result.scalar_one_or_none()

    if not screening:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Screening not found",
        )

    # Get job for auth check
    result = await db.execute(select(Job).where(Job.id == job_id))
    job = result.scalar_one_or_none()

    if not current_user.is_superuser:
        if job.organization_id != current_user.organization_id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Not authorized to modify this screening",
            )

    # Remove override
    screening.admin_override = False
    screening.override_by_id = None
    screening.override_reason = None
    screening.override_at = None

    await db.commit()
