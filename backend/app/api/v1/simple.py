"""
Simple Mode API endpoints for streamlined assessments.

Provides a 7-step workflow:
1. Create assessment with job description
2. Confirm extracted requirements
3. Add candidates (with resume upload)
4. Select traits (max 5)
5. Send interview invites
6. View results
7. Export report
"""

import secrets
import uuid
from datetime import datetime, timezone, timedelta
from typing import Annotated, List, Optional

from fastapi import APIRouter, Depends, HTTPException, UploadFile, File, status, Query
from fastapi.responses import Response
from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.dependencies import get_db, get_current_user
from app.models import (
    User,
    Trait,
    SimpleAssessment,
    SimpleAssessmentStatus,
    SimpleCandidate,
    SimpleQualificationStatus,
    SimpleInterviewStatus,
)
from app.schemas.simple import (
    CreateSimpleAssessmentRequest,
    ConfirmRequirementsRequest,
    SelectTraitsRequest,
    AddCandidateRequest,
    SendInviteRequest,
    SimpleAssessmentResponse,
    SimpleAssessmentDetailResponse,
    SimpleAssessmentListResponse,
    SimpleCandidateResponse,
    SimpleCandidateDetailResponse,
    RequirementResponse,
    TraitOptionsResponse,
    TraitOptionResponse,
    AssessmentResultsResponse,
    CandidateResultResponse,
)
from app.services import get_job_analyzer, get_resume_parser, get_resume_analyzer
from app.services.qualification_screener import QualificationScreener
from app.tasks.email_tasks import send_interview_invitation_email
from app.core.encryption import decrypt_value

router = APIRouter()


# --- Helper Functions ---

def _to_assessment_response(assessment: SimpleAssessment) -> SimpleAssessmentResponse:
    """Convert assessment to response."""
    return SimpleAssessmentResponse(
        id=str(assessment.id),
        job_title=assessment.job_title,
        job_description=assessment.job_description[:500] + "..." if len(assessment.job_description) > 500 else assessment.job_description,
        status=assessment.status.value,
        extracted_requirements=[
            RequirementResponse(**req) for req in assessment.extracted_requirements
        ],
        requirements_confirmed=assessment.requirements_confirmed,
        selected_trait_ids=assessment.selected_trait_ids,
        total_candidates=assessment.total_candidates,
        qualified_candidates=assessment.qualified_candidates,
        interviews_completed=assessment.interviews_completed,
        created_at=assessment.created_at,
        completed_at=assessment.completed_at,
    )


def _to_candidate_response(candidate: SimpleCandidate) -> SimpleCandidateResponse:
    """Convert candidate to response."""
    return SimpleCandidateResponse(
        id=str(candidate.id),
        email=candidate.email,
        full_name=candidate.full_name,
        phone=candidate.phone,
        qualification_status=candidate.qualification_status.value,
        qualification_gaps=candidate.qualification_gaps,
        interview_status=candidate.interview_status.value,
        invited_at=candidate.invited_at,
        interview_completed_at=candidate.interview_completed_at,
        composite_score=candidate.composite_score,
        recommendation=candidate.recommendation,
        created_at=candidate.created_at,
    )


# --- Assessment CRUD ---

@router.post("/assessments", response_model=SimpleAssessmentResponse)
async def create_assessment(
    request: CreateSimpleAssessmentRequest,
    db: Annotated[AsyncSession, Depends(get_db)],
    current_user: Annotated[User, Depends(get_current_user)],
) -> SimpleAssessmentResponse:
    """
    Create a new simple assessment (Step 1).

    This extracts requirements from the job description using LLM.
    """
    # Create assessment
    assessment = SimpleAssessment(
        organization_id=current_user.organization_id,
        created_by_id=current_user.id,
        job_title=request.job_title,
        job_description=request.job_description,
        status=SimpleAssessmentStatus.REQUIREMENTS_PENDING,
    )

    # Extract requirements using job analyzer
    try:
        analyzer = get_job_analyzer()
        extraction = await analyzer.extract_requirements(
            job_title=request.job_title,
            job_description=request.job_description,
        )
        assessment.extracted_requirements = extraction.objective_requirements or []
    except Exception:
        # If extraction fails, set empty requirements and let user add manually
        assessment.extracted_requirements = []

    db.add(assessment)
    await db.commit()
    await db.refresh(assessment)

    return _to_assessment_response(assessment)


@router.get("/assessments", response_model=SimpleAssessmentListResponse)
async def list_assessments(
    db: Annotated[AsyncSession, Depends(get_db)],
    current_user: Annotated[User, Depends(get_current_user)],
    page: int = Query(1, ge=1),
    page_size: int = Query(20, ge=1, le=100),
    status: Optional[str] = None,
) -> SimpleAssessmentListResponse:
    """List all assessments for the current user's organization."""
    query = select(SimpleAssessment).where(
        SimpleAssessment.organization_id == current_user.organization_id
    )

    if status:
        query = query.where(SimpleAssessment.status == status)

    # Count total
    count_query = select(func.count()).select_from(query.subquery())
    total = (await db.execute(count_query)).scalar() or 0

    # Get page
    query = query.order_by(SimpleAssessment.created_at.desc())
    query = query.offset((page - 1) * page_size).limit(page_size)
    result = await db.execute(query)
    assessments = result.scalars().all()

    return SimpleAssessmentListResponse(
        items=[_to_assessment_response(a) for a in assessments],
        total=total,
        page=page,
        page_size=page_size,
    )


@router.get("/assessments/{assessment_id}", response_model=SimpleAssessmentDetailResponse)
async def get_assessment(
    assessment_id: str,
    db: Annotated[AsyncSession, Depends(get_db)],
    current_user: Annotated[User, Depends(get_current_user)],
) -> SimpleAssessmentDetailResponse:
    """Get assessment details with candidates."""
    result = await db.execute(
        select(SimpleAssessment)
        .where(SimpleAssessment.id == uuid.UUID(assessment_id))
        .where(SimpleAssessment.organization_id == current_user.organization_id)
        .options(selectinload(SimpleAssessment.candidates))
    )
    assessment = result.scalar_one_or_none()

    if not assessment:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Assessment not found"
        )

    response = _to_assessment_response(assessment)
    return SimpleAssessmentDetailResponse(
        **response.model_dump(),
        candidates=[_to_candidate_response(c) for c in assessment.candidates],
    )


# --- Step 2: Confirm Requirements ---

@router.post("/assessments/{assessment_id}/requirements/confirm")
async def confirm_requirements(
    assessment_id: str,
    request: ConfirmRequirementsRequest,
    db: Annotated[AsyncSession, Depends(get_db)],
    current_user: Annotated[User, Depends(get_current_user)],
) -> SimpleAssessmentResponse:
    """Confirm (and optionally edit) extracted requirements (Step 2)."""
    result = await db.execute(
        select(SimpleAssessment)
        .where(SimpleAssessment.id == uuid.UUID(assessment_id))
        .where(SimpleAssessment.organization_id == current_user.organization_id)
    )
    assessment = result.scalar_one_or_none()

    if not assessment:
        raise HTTPException(status_code=404, detail="Assessment not found")

    assessment.extracted_requirements = request.requirements
    assessment.requirements_confirmed = True
    assessment.requirements_confirmed_at = datetime.now(timezone.utc)
    assessment.status = SimpleAssessmentStatus.TRAITS_PENDING

    await db.commit()
    await db.refresh(assessment)

    return _to_assessment_response(assessment)


# --- Step 3: Add Candidates ---

@router.post("/assessments/{assessment_id}/candidates", response_model=SimpleCandidateResponse)
async def add_candidate(
    assessment_id: str,
    request: AddCandidateRequest,
    db: Annotated[AsyncSession, Depends(get_db)],
    current_user: Annotated[User, Depends(get_current_user)],
) -> SimpleCandidateResponse:
    """Add a candidate to the assessment (Step 3)."""
    result = await db.execute(
        select(SimpleAssessment)
        .where(SimpleAssessment.id == uuid.UUID(assessment_id))
        .where(SimpleAssessment.organization_id == current_user.organization_id)
    )
    assessment = result.scalar_one_or_none()

    if not assessment:
        raise HTTPException(status_code=404, detail="Assessment not found")

    # Check for duplicate email
    existing = await db.execute(
        select(SimpleCandidate)
        .where(SimpleCandidate.assessment_id == assessment.id)
        .where(SimpleCandidate.email == request.email)
    )
    if existing.scalar_one_or_none():
        raise HTTPException(
            status_code=400,
            detail="Candidate with this email already exists in this assessment"
        )

    candidate = SimpleCandidate(
        assessment_id=assessment.id,
        email=request.email,
        full_name=request.full_name,
        phone=request.phone,
    )

    db.add(candidate)
    assessment.total_candidates += 1

    await db.commit()
    await db.refresh(candidate)

    return _to_candidate_response(candidate)


@router.post("/assessments/{assessment_id}/candidates/{candidate_id}/resume")
async def upload_candidate_resume(
    assessment_id: str,
    candidate_id: str,
    file: Annotated[UploadFile, File(...)],
    db: Annotated[AsyncSession, Depends(get_db)],
    current_user: Annotated[User, Depends(get_current_user)],
) -> SimpleCandidateResponse:
    """Upload resume for a candidate."""
    # Get candidate
    result = await db.execute(
        select(SimpleCandidate)
        .join(SimpleAssessment)
        .where(SimpleCandidate.id == uuid.UUID(candidate_id))
        .where(SimpleAssessment.id == uuid.UUID(assessment_id))
        .where(SimpleAssessment.organization_id == current_user.organization_id)
    )
    candidate = result.scalar_one_or_none()

    if not candidate:
        raise HTTPException(status_code=404, detail="Candidate not found")

    # Get assessment for requirements
    assessment_result = await db.execute(
        select(SimpleAssessment).where(SimpleAssessment.id == uuid.UUID(assessment_id))
    )
    assessment = assessment_result.scalar_one()

    # Read file
    content = await file.read()

    # Parse resume
    parser = get_resume_parser()
    file_type = file.filename.split(".")[-1].lower() if file.filename else "txt"
    parse_result = parser.parse(content, file_type)

    if not parse_result.success:
        raise HTTPException(
            status_code=400,
            detail=f"Failed to parse resume: {parse_result.error}"
        )

    # Save file
    import os
    from app.config import settings
    upload_dir = os.path.join(settings.FILE_UPLOAD_DIR, "simple", str(assessment_id))
    os.makedirs(upload_dir, exist_ok=True)
    file_path = os.path.join(upload_dir, f"{candidate_id}_{file.filename}")
    with open(file_path, "wb") as f:
        f.write(content)

    # Analyze resume with LLM
    analyzer = get_resume_analyzer()
    try:
        parsed_data = await analyzer.analyze(parse_result.text)
    except Exception:
        parsed_data = {"raw_text": parse_result.text}

    # Update candidate
    candidate.resume_file_path = file_path
    candidate.resume_filename = file.filename
    candidate.resume_raw_text = parse_result.text
    candidate.resume_parsed_data = parsed_data

    # Screen against requirements if confirmed
    if assessment.requirements_confirmed and assessment.extracted_requirements:
        screener = QualificationScreener()
        screening = await screener.screen(
            resume_data=parsed_data,
            requirements=assessment.extracted_requirements,
        )
        candidate.qualification_status = SimpleQualificationStatus(screening.status.upper())
        candidate.qualification_results = screening.requirement_results
        candidate.qualification_gaps = screening.gaps

        if candidate.qualification_status == SimpleQualificationStatus.QUALIFIED:
            assessment.qualified_candidates += 1

    await db.commit()
    await db.refresh(candidate)

    return _to_candidate_response(candidate)


# --- Step 4: Select Traits ---

@router.get("/traits", response_model=TraitOptionsResponse)
async def get_trait_options(
    db: Annotated[AsyncSession, Depends(get_db)],
    current_user: Annotated[User, Depends(get_current_user)],
) -> TraitOptionsResponse:
    """Get available traits for selection."""
    result = await db.execute(
        select(Trait).order_by(Trait.category, Trait.display_order)
    )
    traits = result.scalars().all()

    return TraitOptionsResponse(
        traits=[
            TraitOptionResponse(
                id=str(t.id),
                name=t.name,
                category=t.category.value if hasattr(t.category, 'value') else t.category,
                definition=t.definition,
            )
            for t in traits
        ],
        max_selection=5,
    )


@router.post("/assessments/{assessment_id}/traits")
async def select_traits(
    assessment_id: str,
    request: SelectTraitsRequest,
    db: Annotated[AsyncSession, Depends(get_db)],
    current_user: Annotated[User, Depends(get_current_user)],
) -> SimpleAssessmentResponse:
    """Select traits for assessment (Step 4). Maximum 5 traits."""
    if len(request.trait_ids) > 5:
        raise HTTPException(
            status_code=400,
            detail="Maximum 5 traits allowed"
        )

    result = await db.execute(
        select(SimpleAssessment)
        .where(SimpleAssessment.id == uuid.UUID(assessment_id))
        .where(SimpleAssessment.organization_id == current_user.organization_id)
    )
    assessment = result.scalar_one_or_none()

    if not assessment:
        raise HTTPException(status_code=404, detail="Assessment not found")

    # Verify traits exist
    trait_result = await db.execute(
        select(Trait).where(Trait.id.in_([uuid.UUID(tid) for tid in request.trait_ids]))
    )
    traits = trait_result.scalars().all()

    if len(traits) != len(request.trait_ids):
        raise HTTPException(status_code=400, detail="One or more traits not found")

    assessment.selected_trait_ids = request.trait_ids
    assessment.status = SimpleAssessmentStatus.CANDIDATES_PENDING

    # If we have qualified candidates, move to interviewing
    if assessment.qualified_candidates > 0:
        assessment.status = SimpleAssessmentStatus.INTERVIEWING

    await db.commit()
    await db.refresh(assessment)

    return _to_assessment_response(assessment)


# --- Step 5: Send Invites ---

@router.post("/assessments/{assessment_id}/candidates/{candidate_id}/send-invite")
async def send_interview_invite(
    assessment_id: str,
    candidate_id: str,
    request: Optional[SendInviteRequest] = None,
    db: Annotated[AsyncSession, Depends(get_db)] = None,
    current_user: Annotated[User, Depends(get_current_user)] = None,
) -> SimpleCandidateResponse:
    """Send magic link interview invite to candidate (Step 5)."""
    result = await db.execute(
        select(SimpleCandidate)
        .join(SimpleAssessment)
        .where(SimpleCandidate.id == uuid.UUID(candidate_id))
        .where(SimpleAssessment.id == uuid.UUID(assessment_id))
        .where(SimpleAssessment.organization_id == current_user.organization_id)
    )
    candidate = result.scalar_one_or_none()

    if not candidate:
        raise HTTPException(status_code=404, detail="Candidate not found")

    # Generate magic link token
    token = secrets.token_urlsafe(32)
    candidate.magic_link_token = token
    candidate.magic_link_expires_at = datetime.now(timezone.utc) + timedelta(days=7)
    candidate.interview_status = SimpleInterviewStatus.INVITED
    candidate.invited_at = datetime.now(timezone.utc)

    # Update assessment status and load organization for email
    assessment_result = await db.execute(
        select(SimpleAssessment)
        .where(SimpleAssessment.id == uuid.UUID(assessment_id))
        .options(selectinload(SimpleAssessment.organization))
    )
    assessment = assessment_result.scalar_one()
    if assessment.status == SimpleAssessmentStatus.CANDIDATES_PENDING:
        assessment.status = SimpleAssessmentStatus.INTERVIEWING

    await db.commit()
    await db.refresh(candidate)

    # Check for organization-specific email settings
    smtp_settings = None
    if assessment.organization and assessment.organization.settings:
        org_email = assessment.organization.settings.get("email", {})
        if org_email.get("smtp_password_encrypted"):
            decrypted_password = decrypt_value(org_email["smtp_password_encrypted"])
            if decrypted_password:
                smtp_settings = {
                    "smtp_host": org_email.get("smtp_host", ""),
                    "smtp_port": org_email.get("smtp_port", 587),
                    "smtp_user": org_email.get("smtp_user", ""),
                    "smtp_password": decrypted_password,
                    "smtp_from_email": org_email.get("smtp_from_email", ""),
                    "smtp_from_name": org_email.get("smtp_from_name", ""),
                    "smtp_use_tls": org_email.get("smtp_use_tls", True),
                }

    # Queue email task to send invitation
    send_interview_invitation_email.delay(
        candidate_email=candidate.email,
        candidate_name=candidate.full_name,
        job_title=assessment.job_title,
        organization_name=assessment.organization.name if assessment.organization else "Assessment Platform",
        interview_token=token,
        custom_message=request.custom_message if request else None,
        smtp_settings=smtp_settings,
    )

    return _to_candidate_response(candidate)


# --- Step 6: View Results ---

@router.get("/assessments/{assessment_id}/results", response_model=AssessmentResultsResponse)
async def get_assessment_results(
    assessment_id: str,
    db: Annotated[AsyncSession, Depends(get_db)],
    current_user: Annotated[User, Depends(get_current_user)],
) -> AssessmentResultsResponse:
    """Get all assessment results (Step 6)."""
    result = await db.execute(
        select(SimpleAssessment)
        .where(SimpleAssessment.id == uuid.UUID(assessment_id))
        .where(SimpleAssessment.organization_id == current_user.organization_id)
        .options(selectinload(SimpleAssessment.candidates))
    )
    assessment = result.scalar_one_or_none()

    if not assessment:
        raise HTTPException(status_code=404, detail="Assessment not found")

    # Get completed interviews with results
    completed_candidates = [
        c for c in assessment.candidates
        if c.interview_status == SimpleInterviewStatus.COMPLETED and c.trait_scores
    ]

    # Build results
    results = []
    for candidate in completed_candidates:
        trait_scores = []
        if candidate.trait_scores:
            for trait_id, score_data in candidate.trait_scores.items():
                trait_scores.append({
                    "trait_id": trait_id,
                    "trait_name": score_data.get("trait_name", "Unknown"),
                    "score": score_data.get("score", 0),  # 0-10 scale
                    "confidence": score_data.get("confidence", 0),
                    "explanation": score_data.get("explanation", ""),
                })

        results.append(CandidateResultResponse(
            candidate_id=str(candidate.id),
            candidate_name=candidate.full_name,
            candidate_email=candidate.email,
            composite_score=candidate.composite_score or 0,
            recommendation=candidate.recommendation or "PENDING",
            recommendation_rationale=candidate.recommendation_rationale or "",
            trait_scores=trait_scores,
        ))

    return AssessmentResultsResponse(
        assessment_id=str(assessment.id),
        job_title=assessment.job_title,
        status=assessment.status.value,
        total_candidates=assessment.total_candidates,
        completed_interviews=assessment.interviews_completed,
        results=results,
    )


# --- Delete Assessment ---

@router.delete("/assessments/{assessment_id}")
async def delete_assessment(
    assessment_id: str,
    db: Annotated[AsyncSession, Depends(get_db)],
    current_user: Annotated[User, Depends(get_current_user)],
) -> dict:
    """Delete an assessment and all its candidates."""
    result = await db.execute(
        select(SimpleAssessment)
        .where(SimpleAssessment.id == uuid.UUID(assessment_id))
        .where(SimpleAssessment.organization_id == current_user.organization_id)
    )
    assessment = result.scalar_one_or_none()

    if not assessment:
        raise HTTPException(status_code=404, detail="Assessment not found")

    await db.delete(assessment)
    await db.commit()

    return {"status": "deleted"}


# --- Delete Candidate ---

@router.delete("/assessments/{assessment_id}/candidates/{candidate_id}")
async def delete_candidate(
    assessment_id: str,
    candidate_id: str,
    db: Annotated[AsyncSession, Depends(get_db)],
    current_user: Annotated[User, Depends(get_current_user)],
) -> dict:
    """Delete a candidate from an assessment."""
    result = await db.execute(
        select(SimpleCandidate)
        .join(SimpleAssessment)
        .where(SimpleCandidate.id == uuid.UUID(candidate_id))
        .where(SimpleAssessment.id == uuid.UUID(assessment_id))
        .where(SimpleAssessment.organization_id == current_user.organization_id)
    )
    candidate = result.scalar_one_or_none()

    if not candidate:
        raise HTTPException(status_code=404, detail="Candidate not found")

    # Update assessment counts
    assessment_result = await db.execute(
        select(SimpleAssessment).where(SimpleAssessment.id == uuid.UUID(assessment_id))
    )
    assessment = assessment_result.scalar_one()
    assessment.total_candidates = max(0, assessment.total_candidates - 1)
    if candidate.qualification_status == SimpleQualificationStatus.QUALIFIED:
        assessment.qualified_candidates = max(0, assessment.qualified_candidates - 1)

    await db.delete(candidate)
    await db.commit()

    return {"status": "deleted"}


# --- Step 7: Export PDF Report ---

@router.get("/assessments/{assessment_id}/export/pdf")
async def export_assessment_pdf(
    assessment_id: str,
    db: Annotated[AsyncSession, Depends(get_db)],
    current_user: Annotated[User, Depends(get_current_user)],
) -> Response:
    """
    Export assessment results as PDF report (Step 7).

    Generates a professional PDF report containing:
    - Assessment summary with job details
    - Candidate rankings by composite score
    - Detailed trait scores and explanations for each candidate
    - Recommendations and rationale
    """
    from app.models import Trait
    from app.services.pdf_generator import get_pdf_generator

    # Get assessment with candidates and organization
    result = await db.execute(
        select(SimpleAssessment)
        .where(SimpleAssessment.id == uuid.UUID(assessment_id))
        .where(SimpleAssessment.organization_id == current_user.organization_id)
        .options(selectinload(SimpleAssessment.candidates))
        .options(selectinload(SimpleAssessment.organization))
    )
    assessment = result.scalar_one_or_none()

    if not assessment:
        raise HTTPException(status_code=404, detail="Assessment not found")

    # Get selected traits
    trait_result = await db.execute(
        select(Trait).where(
            Trait.id.in_([uuid.UUID(tid) for tid in assessment.selected_trait_ids])
        )
    )
    traits = list(trait_result.scalars().all())

    # Generate PDF
    generator = get_pdf_generator()
    pdf_bytes = await generator.generate_assessment_report(
        assessment=assessment,
        candidates=list(assessment.candidates),
        traits=traits,
        organization_name=assessment.organization.name if assessment.organization else "Assessment Platform",
    )

    # Create filename from job title
    safe_title = "".join(c if c.isalnum() or c in " -_" else "" for c in assessment.job_title)
    safe_title = safe_title.replace(" ", "-")[:50]
    filename = f"assessment-{safe_title}-{str(assessment_id)[:8]}.pdf"

    return Response(
        content=pdf_bytes,
        media_type="application/pdf",
        headers={
            "Content-Disposition": f'attachment; filename="{filename}"',
        },
    )
