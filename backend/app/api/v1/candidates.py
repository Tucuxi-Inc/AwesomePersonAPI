"""Candidate endpoints."""

import os
from datetime import datetime
from pathlib import Path
from typing import Annotated, Optional
import uuid

from fastapi import APIRouter, Depends, HTTPException, Query, UploadFile, File, status, BackgroundTasks
from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.config import settings
from app.dependencies import get_db, get_current_user
from app.models import User, Candidate, Resume, ResumeParseStatus
from app.schemas.candidate import (
    CandidateCreate,
    CandidateUpdate,
    CandidateResponse,
    CandidateList,
)
from app.schemas.resume import (
    ResumeUploadResponse,
    ResumeResponse,
    ResumeList,
)
from app.services.resume_parser import get_resume_parser
from app.services.resume_analyzer import get_resume_analyzer

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


# === Resume Endpoints ===

async def process_resume_background(
    resume_id: uuid.UUID,
    file_content: bytes,
    file_type: str,
):
    """Background task to parse and analyze resume."""
    from app.db.session import SyncSessionLocal

    db = SyncSessionLocal()
    try:
        # Get resume
        from sqlalchemy import select as sync_select
        result = db.execute(sync_select(Resume).where(Resume.id == resume_id))
        resume = result.scalar_one_or_none()
        if not resume:
            return

        # Update status to parsing
        resume.parse_status = ResumeParseStatus.PARSING
        db.commit()

        try:
            # Parse file to extract text
            parser = get_resume_parser()
            raw_text = parser.parse(file_content, file_type)
            resume.raw_text = raw_text

            # Analyze with LLM (need to run in event loop)
            import asyncio
            analyzer = get_resume_analyzer()
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
            try:
                parsed_data = loop.run_until_complete(analyzer.analyze(raw_text))
            finally:
                loop.close()

            resume.parsed_data = parsed_data
            resume.parse_status = ResumeParseStatus.PARSED

        except Exception as e:
            resume.parse_status = ResumeParseStatus.FAILED
            resume.parse_error = str(e)

        db.commit()

    except Exception as e:
        # Log error but don't raise (background task)
        import logging
        logging.error(f"Error processing resume {resume_id}: {e}")
    finally:
        db.close()


@router.post("/{candidate_id}/resume", response_model=ResumeUploadResponse, status_code=status.HTTP_201_CREATED)
async def upload_resume(
    candidate_id: uuid.UUID,
    background_tasks: BackgroundTasks,
    db: Annotated[AsyncSession, Depends(get_db)],
    current_user: Annotated[User, Depends(get_current_user)],
    file: UploadFile = File(...),
) -> Resume:
    """Upload a resume for a candidate."""
    # Get candidate
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
                detail="Not authorized to upload resume for this candidate",
            )

    # Validate file
    parser = get_resume_parser()
    file_content = await file.read()

    is_valid, error = parser.validate_file(
        file_content,
        file.filename or "unknown",
        settings.MAX_RESUME_SIZE_MB,
    )
    if not is_valid:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=error,
        )

    file_type = parser.detect_file_type(file.filename or "unknown")

    # Create upload directory if needed
    upload_dir = Path(settings.FILE_UPLOAD_DIR) / "resumes" / str(candidate.organization_id)
    upload_dir.mkdir(parents=True, exist_ok=True)

    # Generate unique filename
    file_ext = Path(file.filename or "resume").suffix
    stored_filename = f"{candidate_id}_{uuid.uuid4()}{file_ext}"
    file_path = upload_dir / stored_filename

    # Save file
    with open(file_path, "wb") as f:
        f.write(file_content)

    # Mark existing resumes as non-primary
    await db.execute(
        Resume.__table__.update()
        .where(Resume.candidate_id == candidate_id)
        .values(is_primary=False)
    )

    # Get current version
    result = await db.execute(
        select(func.max(Resume.version)).where(Resume.candidate_id == candidate_id)
    )
    max_version = result.scalar() or 0

    # Create resume record
    resume = Resume(
        candidate_id=candidate_id,
        filename=file.filename or "resume",
        file_type=file_type,
        file_size_bytes=len(file_content),
        file_path=str(file_path),
        parse_status=ResumeParseStatus.PENDING,
        version=max_version + 1,
        is_primary=True,
    )
    db.add(resume)
    await db.commit()
    await db.refresh(resume)

    # Queue background processing
    background_tasks.add_task(
        process_resume_background,
        resume.id,
        file_content,
        file_type,
    )

    return resume


@router.get("/{candidate_id}/resumes", response_model=ResumeList)
async def list_candidate_resumes(
    candidate_id: uuid.UUID,
    db: Annotated[AsyncSession, Depends(get_db)],
    current_user: Annotated[User, Depends(get_current_user)],
) -> ResumeList:
    """List all resumes for a candidate."""
    # Get candidate
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
                detail="Not authorized to view resumes for this candidate",
            )

    # Get resumes
    result = await db.execute(
        select(Resume)
        .where(Resume.candidate_id == candidate_id)
        .order_by(Resume.version.desc())
    )
    resumes = result.scalars().all()

    return ResumeList(items=resumes, total=len(resumes))


@router.get("/{candidate_id}/resume", response_model=ResumeResponse)
async def get_primary_resume(
    candidate_id: uuid.UUID,
    db: Annotated[AsyncSession, Depends(get_db)],
    current_user: Annotated[User, Depends(get_current_user)],
) -> Resume:
    """Get the primary (most recent) resume for a candidate."""
    # Get candidate
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
                detail="Not authorized to view resume for this candidate",
            )

    # Get primary resume
    result = await db.execute(
        select(Resume)
        .where(Resume.candidate_id == candidate_id, Resume.is_primary == True)
    )
    resume = result.scalar_one_or_none()

    if not resume:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="No resume found for this candidate",
        )

    return resume


@router.get("/{candidate_id}/resume/{resume_id}", response_model=ResumeResponse)
async def get_resume(
    candidate_id: uuid.UUID,
    resume_id: uuid.UUID,
    db: Annotated[AsyncSession, Depends(get_db)],
    current_user: Annotated[User, Depends(get_current_user)],
) -> Resume:
    """Get a specific resume for a candidate."""
    # Get resume
    result = await db.execute(
        select(Resume).where(
            Resume.id == resume_id,
            Resume.candidate_id == candidate_id,
        )
    )
    resume = result.scalar_one_or_none()

    if not resume:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Resume not found",
        )

    # Get candidate for auth check
    result = await db.execute(select(Candidate).where(Candidate.id == candidate_id))
    candidate = result.scalar_one_or_none()

    # Check access
    if not current_user.is_superuser:
        if current_user.organization_id != candidate.organization_id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Not authorized to view this resume",
            )

    return resume


@router.post("/{candidate_id}/resume/{resume_id}/reparse", response_model=ResumeResponse)
async def reparse_resume(
    candidate_id: uuid.UUID,
    resume_id: uuid.UUID,
    background_tasks: BackgroundTasks,
    db: Annotated[AsyncSession, Depends(get_db)],
    current_user: Annotated[User, Depends(get_current_user)],
) -> Resume:
    """Re-parse a resume (useful if parsing failed or to refresh analysis)."""
    # Get resume
    result = await db.execute(
        select(Resume).where(
            Resume.id == resume_id,
            Resume.candidate_id == candidate_id,
        )
    )
    resume = result.scalar_one_or_none()

    if not resume:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Resume not found",
        )

    # Get candidate for auth check
    result = await db.execute(select(Candidate).where(Candidate.id == candidate_id))
    candidate = result.scalar_one_or_none()

    # Check access
    if not current_user.is_superuser:
        if current_user.organization_id != candidate.organization_id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Not authorized to reparse this resume",
            )

    # Read file content
    try:
        with open(resume.file_path, "rb") as f:
            file_content = f.read()
    except FileNotFoundError:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Resume file not found on disk",
        )

    # Reset status and queue for processing
    resume.parse_status = ResumeParseStatus.PENDING
    resume.parse_error = None
    await db.commit()
    await db.refresh(resume)

    # Queue background processing
    background_tasks.add_task(
        process_resume_background,
        resume.id,
        file_content,
        resume.file_type,
    )

    return resume
