"""
Interview API endpoints for conducting and managing interviews.

This module provides endpoints for:
- Starting interview sessions
- Processing candidate responses
- Retrieving interview results and assessments
- Managing interview state
"""

import uuid
from datetime import datetime, timezone
from typing import Annotated, List, Optional

from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel, Field
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.dependencies import get_db, get_current_user
from app.models import (
    User,
    Candidate,
    InterviewSession,
    Trait,
    ScoringRubric,
    Resume,
)
from app.services import (
    get_interview_engine,
    InterviewConfig,
    InterviewState,
    TraitProgress,
)

router = APIRouter()


# --- Pydantic Schemas ---

class InterviewConfigRequest(BaseModel):
    """Configuration for starting an interview."""
    max_duration_minutes: int = Field(default=60, ge=10, le=120)
    max_follow_ups_per_trait: int = Field(default=3, ge=1, le=5)
    confidence_threshold_for_recursion: float = Field(default=0.6, ge=0.0, le=1.0)
    require_reflection: bool = True
    enable_resume_customization: bool = True
    enable_conflict_probing: bool = True


class StartInterviewRequest(BaseModel):
    """Request to start a new interview."""
    candidate_id: str
    rubric_id: Optional[str] = None
    trait_ids: Optional[List[str]] = None  # If not provided, use all traits
    config: Optional[InterviewConfigRequest] = None


class InterviewPromptResponse(BaseModel):
    """Response containing the next prompt."""
    session_id: str
    next_prompt: str
    prompt_type: str
    trait_id: Optional[str] = None
    trait_name: Optional[str] = None
    trait_progress: Optional[dict] = None
    overall_progress: float
    can_end_interview: bool
    interview_complete: bool = False


class CandidateResponseRequest(BaseModel):
    """Request containing candidate's response."""
    response_text: str = Field(..., min_length=1, max_length=10000)


class TraitScoreResponse(BaseModel):
    """Trait score in assessment result."""
    trait_id: str
    trait_name: str
    raw_score: int
    calibrated_score: int
    confidence: float
    explanation: str
    evidence_summary: str
    signal_gaps: List[str]


class AssessmentSummaryResponse(BaseModel):
    """Assessment summary response."""
    session_id: str
    candidate_id: str
    recommendation: str
    recommendation_rationale: str
    composite_score: float
    evidence_quality: str
    confidence: float
    trait_scores: List[TraitScoreResponse]
    key_strengths: List[dict]
    development_areas: List[dict]
    counter_indicator_flags: List[dict]
    assessment_summary: str


class InterviewSessionResponse(BaseModel):
    """Interview session details."""
    id: str
    candidate_id: str
    status: str
    session_type: str
    started_at: Optional[str]
    completed_at: Optional[str]
    duration_minutes: Optional[int]
    target_traits: List[str]
    overall_progress: float
    traits_completed: int
    traits_total: int


# --- In-memory session storage (for demo - use Redis/DB in production) ---
# In a real implementation, this would be stored in Redis or the database
_active_sessions: dict[str, dict] = {}


# --- Helper Functions ---

def _state_to_dict(state: InterviewState) -> dict:
    """Convert InterviewState to serializable dict."""
    return {
        "session_id": state.session_id,
        "candidate_id": state.candidate_id,
        "phase": state.phase.value,
        "current_trait_index": state.current_trait_index,
        "trait_progress": {
            tid: {
                "trait_id": tp.trait_id,
                "trait_name": tp.trait_name,
                "phase": tp.phase.value,
                "probes_used": tp.probes_used,
                "evidence_count": tp.evidence_count,
                "behavioral_evidence_count": tp.behavioral_evidence_count,
                "confidence": tp.confidence,
                "star_coverage": tp.star_coverage,
                "has_conflict_example": tp.has_conflict_example,
                "raw_score": tp.raw_score,
                "is_complete": tp.is_complete,
            }
            for tid, tp in state.trait_progress.items()
        },
        "exchanges": state.exchanges,
        "evidence_items": state.evidence_items,
        "start_time": state.start_time.isoformat() if state.start_time else None,
        "config": {
            "max_duration_minutes": state.config.max_duration_minutes,
            "max_follow_ups_per_trait": state.config.max_follow_ups_per_trait,
            "confidence_threshold_for_recursion": state.config.confidence_threshold_for_recursion,
            "require_reflection": state.config.require_reflection,
            "enable_resume_customization": state.config.enable_resume_customization,
            "enable_conflict_probing": state.config.enable_conflict_probing,
        },
        "resume_elements": [
            {"type": e.element_type, "description": e.description}
            for e in state.resume_elements
        ],
    }


def _dict_to_state(data: dict) -> InterviewState:
    """Convert dict back to InterviewState."""
    from app.services.interview_engine import InterviewPhase, ProbePhase
    from app.services.resume_customizer import ResumeElement

    config = InterviewConfig(
        max_duration_minutes=data["config"]["max_duration_minutes"],
        max_follow_ups_per_trait=data["config"]["max_follow_ups_per_trait"],
        confidence_threshold_for_recursion=data["config"]["confidence_threshold_for_recursion"],
        require_reflection=data["config"]["require_reflection"],
        enable_resume_customization=data["config"]["enable_resume_customization"],
        enable_conflict_probing=data["config"]["enable_conflict_probing"],
    )

    state = InterviewState(
        session_id=data["session_id"],
        candidate_id=data["candidate_id"],
        phase=InterviewPhase(data["phase"]),
        current_trait_index=data["current_trait_index"],
        exchanges=data["exchanges"],
        evidence_items=data["evidence_items"],
        start_time=datetime.fromisoformat(data["start_time"]) if data["start_time"] else None,
        config=config,
        resume_elements=[
            ResumeElement(element_type=e["type"], description=e["description"])
            for e in data.get("resume_elements", [])
        ],
    )

    # Restore trait progress
    for tid, tp_data in data["trait_progress"].items():
        state.trait_progress[tid] = TraitProgress(
            trait_id=tp_data["trait_id"],
            trait_name=tp_data["trait_name"],
            phase=ProbePhase(tp_data["phase"]),
            probes_used=tp_data["probes_used"],
            evidence_count=tp_data["evidence_count"],
            behavioral_evidence_count=tp_data["behavioral_evidence_count"],
            confidence=tp_data["confidence"],
            star_coverage=tp_data["star_coverage"],
            has_conflict_example=tp_data["has_conflict_example"],
            raw_score=tp_data["raw_score"],
            is_complete=tp_data["is_complete"],
        )

    return state


# --- API Endpoints ---

@router.post("/start", response_model=InterviewPromptResponse)
async def start_interview(
    request: StartInterviewRequest,
    db: Annotated[AsyncSession, Depends(get_db)],
    current_user: Annotated[User, Depends(get_current_user)],
) -> InterviewPromptResponse:
    """
    Start a new interview session.

    This initializes the interview engine and returns the introduction prompt.
    """
    # Validate candidate exists
    candidate_result = await db.execute(
        select(Candidate).where(Candidate.id == uuid.UUID(request.candidate_id))
    )
    candidate = candidate_result.scalar_one_or_none()
    if not candidate:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Candidate not found"
        )

    # Get traits to assess
    if request.trait_ids:
        trait_query = select(Trait).where(
            Trait.id.in_([uuid.UUID(tid) for tid in request.trait_ids])
        )
    else:
        # Default to first 6 traits
        trait_query = select(Trait).limit(6)

    trait_result = await db.execute(trait_query)
    traits = trait_result.scalars().all()

    if not traits:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="No traits found to assess"
        )

    # Get resume text if available
    resume_text = None
    resume_result = await db.execute(
        select(Resume).where(Resume.candidate_id == candidate.id).order_by(Resume.created_at.desc())
    )
    resume = resume_result.scalar_one_or_none()
    if resume:
        resume_text = resume.content

    # Get behavioral anchors from rubric
    behavioral_anchors = {}
    if request.rubric_id:
        rubric_result = await db.execute(
            select(ScoringRubric).where(ScoringRubric.id == uuid.UUID(request.rubric_id))
        )
        rubric = rubric_result.scalar_one_or_none()
        if rubric:
            behavioral_anchors = {str(rubric.trait_id): rubric.behavioral_anchors}

    # Prepare traits metadata
    traits_to_assess = [
        {
            "id": str(t.id),
            "name": t.name,
            "definition": t.definition,
            "behavioral_anchors": behavioral_anchors.get(str(t.id)),
        }
        for t in traits
    ]

    # Build config
    config = InterviewConfig()
    if request.config:
        config.max_duration_minutes = request.config.max_duration_minutes
        config.max_follow_ups_per_trait = request.config.max_follow_ups_per_trait
        config.confidence_threshold_for_recursion = request.config.confidence_threshold_for_recursion
        config.require_reflection = request.config.require_reflection
        config.enable_resume_customization = request.config.enable_resume_customization
        config.enable_conflict_probing = request.config.enable_conflict_probing

    # Create database session record
    session_id = str(uuid.uuid4())
    db_session = InterviewSession(
        id=uuid.UUID(session_id),
        candidate_id=candidate.id,
        interviewer_id=current_user.id,
        rubric_id=uuid.UUID(request.rubric_id) if request.rubric_id else None,
        session_type="BEHAVIORAL",
        status="IN_PROGRESS",
        started_at=datetime.now(timezone.utc),
        target_traits=[str(t.id) for t in traits],
        interview_config=config.__dict__,
        traits_total=len(traits),
    )
    db.add(db_session)
    await db.commit()

    # Start interview engine
    engine = get_interview_engine()
    state, response = await engine.start_interview(
        session_id=session_id,
        candidate_id=str(candidate.id),
        traits_to_assess=traits_to_assess,
        config=config,
        resume_text=resume_text,
        behavioral_anchors={str(t.id): behavioral_anchors.get(str(t.id), {}) for t in traits},
    )

    # Store state
    _active_sessions[session_id] = {
        "state": _state_to_dict(state),
        "traits_metadata": {t["id"]: t for t in traits_to_assess},
    }

    return InterviewPromptResponse(
        session_id=session_id,
        next_prompt=response.next_prompt,
        prompt_type=response.prompt_type,
        trait_id=response.trait_id,
        trait_name=response.trait_progress.trait_name if response.trait_progress else None,
        trait_progress=response.trait_progress.__dict__ if response.trait_progress else None,
        overall_progress=response.overall_progress,
        can_end_interview=response.can_end_interview,
        interview_complete=response.interview_complete,
    )


@router.post("/{session_id}/respond", response_model=InterviewPromptResponse)
async def submit_response(
    session_id: str,
    request: CandidateResponseRequest,
    db: Annotated[AsyncSession, Depends(get_db)],
    current_user: Annotated[User, Depends(get_current_user)],
) -> InterviewPromptResponse:
    """
    Submit a candidate response and get the next prompt.

    The interview engine will analyze the response, extract evidence,
    and determine the appropriate next action (follow-up, reflection,
    recursion, or next trait).
    """
    # Get session data
    session_data = _active_sessions.get(session_id)
    if not session_data:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Interview session not found or expired"
        )

    # Restore state
    state = _dict_to_state(session_data["state"])
    traits_metadata = session_data["traits_metadata"]

    # Process response
    engine = get_interview_engine()
    state, response = await engine.process_response(
        state=state,
        response_text=request.response_text,
        traits_metadata=traits_metadata,
    )

    # Update stored state
    _active_sessions[session_id]["state"] = _state_to_dict(state)

    # Update database session
    db_session_result = await db.execute(
        select(InterviewSession).where(InterviewSession.id == uuid.UUID(session_id))
    )
    db_session = db_session_result.scalar_one_or_none()
    if db_session:
        db_session.transcript = state.exchanges
        db_session.extracted_evidence = state.evidence_items
        db_session.current_trait_index = state.current_trait_index
        db_session.traits_completed = sum(
            1 for p in state.trait_progress.values() if p.is_complete
        )
        db_session.overall_confidence = sum(
            p.confidence for p in state.trait_progress.values()
        ) / len(state.trait_progress) if state.trait_progress else 0

        if response.interview_complete:
            db_session.status = "COMPLETED"
            db_session.completed_at = datetime.now(timezone.utc)
            if db_session.started_at:
                delta = db_session.completed_at - db_session.started_at
                db_session.duration_minutes = int(delta.total_seconds() / 60)

        await db.commit()

    return InterviewPromptResponse(
        session_id=session_id,
        next_prompt=response.next_prompt,
        prompt_type=response.prompt_type,
        trait_id=response.trait_id,
        trait_name=response.trait_progress.trait_name if response.trait_progress else None,
        trait_progress=response.trait_progress.__dict__ if response.trait_progress else None,
        overall_progress=response.overall_progress,
        can_end_interview=response.can_end_interview,
        interview_complete=response.interview_complete,
    )


@router.get("/{session_id}", response_model=InterviewSessionResponse)
async def get_interview_session(
    session_id: str,
    db: Annotated[AsyncSession, Depends(get_db)],
    current_user: Annotated[User, Depends(get_current_user)],
) -> InterviewSessionResponse:
    """Get interview session details."""
    result = await db.execute(
        select(InterviewSession).where(InterviewSession.id == uuid.UUID(session_id))
    )
    session = result.scalar_one_or_none()

    if not session:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Interview session not found"
        )

    return InterviewSessionResponse(
        id=str(session.id),
        candidate_id=str(session.candidate_id),
        status=session.status,
        session_type=session.session_type,
        started_at=session.started_at.isoformat() if session.started_at else None,
        completed_at=session.completed_at.isoformat() if session.completed_at else None,
        duration_minutes=session.duration_minutes,
        target_traits=session.target_traits,
        overall_progress=session.traits_completed / session.traits_total if session.traits_total else 0,
        traits_completed=session.traits_completed,
        traits_total=session.traits_total,
    )


@router.post("/{session_id}/end", response_model=InterviewPromptResponse)
async def end_interview(
    session_id: str,
    db: Annotated[AsyncSession, Depends(get_db)],
    current_user: Annotated[User, Depends(get_current_user)],
) -> InterviewPromptResponse:
    """
    End an interview session early.

    This will finalize the interview and generate a partial assessment
    based on evidence collected so far.
    """
    # Get session data
    session_data = _active_sessions.get(session_id)
    if not session_data:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Interview session not found or expired"
        )

    # Restore state
    state = _dict_to_state(session_data["state"])

    # Mark as complete
    from app.services.interview_engine import InterviewPhase
    state.phase = InterviewPhase.COMPLETED

    # Update database
    db_session_result = await db.execute(
        select(InterviewSession).where(InterviewSession.id == uuid.UUID(session_id))
    )
    db_session = db_session_result.scalar_one_or_none()
    if db_session:
        db_session.status = "COMPLETED"
        db_session.completed_at = datetime.now(timezone.utc)
        if db_session.started_at:
            delta = db_session.completed_at - db_session.started_at
            db_session.duration_minutes = int(delta.total_seconds() / 60)
        await db.commit()

    # Clean up active session
    del _active_sessions[session_id]

    return InterviewPromptResponse(
        session_id=session_id,
        next_prompt="Interview ended. Assessment will be generated from collected evidence.",
        prompt_type="COMPLETE",
        overall_progress=1.0,
        can_end_interview=True,
        interview_complete=True,
    )


@router.get("/{session_id}/result", response_model=AssessmentSummaryResponse)
async def get_interview_result(
    session_id: str,
    db: Annotated[AsyncSession, Depends(get_db)],
    current_user: Annotated[User, Depends(get_current_user)],
) -> AssessmentSummaryResponse:
    """
    Get the assessment result for a completed interview.

    This generates calibrated scores and recommendations based on
    all evidence collected during the interview.
    """
    from app.services import get_score_calibrator, EvidenceForScoring, EvidenceType

    # Get session from database
    result = await db.execute(
        select(InterviewSession).where(InterviewSession.id == uuid.UUID(session_id))
    )
    session = result.scalar_one_or_none()

    if not session:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Interview session not found"
        )

    if session.status != "COMPLETED":
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Interview not yet completed"
        )

    # Get traits
    trait_result = await db.execute(
        select(Trait).where(Trait.id.in_([uuid.UUID(tid) for tid in session.target_traits]))
    )
    traits = {str(t.id): t for t in trait_result.scalars().all()}

    # Get behavioral anchors
    rubric_result = await db.execute(
        select(ScoringRubric).where(ScoringRubric.is_default == True)
    )
    rubrics = {str(r.trait_id): r for r in rubric_result.scalars().all()}

    # Generate calibrated scores
    calibrator = get_score_calibrator()
    trait_scores = []

    for trait_id in session.target_traits:
        trait = traits.get(trait_id)
        if not trait:
            continue

        # Get evidence for this trait
        trait_evidence = [
            EvidenceForScoring(
                source_type=EvidenceType(e.get("source_type", "SELF_REPORT")),
                source_text=e.get("source_text", ""),
                weight=e.get("weight", 0.3),
                trait_signal=e.get("trait_signal", "neutral"),
                signal_strength=e.get("signal_strength", 0.5),
                star_components=e.get("star_components", {}),
                contains_conflict=e.get("contains_conflict", False),
                contains_failure=e.get("contains_failure", False),
            )
            for e in session.extracted_evidence
            if e.get("trait_id") == trait_id
        ]

        # Get behavioral anchors for this trait
        rubric = rubrics.get(trait_id)
        anchors = rubric.behavioral_anchors if rubric else {}

        # Calibrate score
        score = await calibrator.calibrate_trait_score(
            trait_id=trait_id,
            trait_name=trait.name,
            evidence_items=trait_evidence,
            behavioral_anchors=anchors,
            counter_indicators=trait.counter_indicator_for,
        )

        trait_scores.append(score)

    # Generate assessment
    assessment = await calibrator.generate_assessment(trait_scores)

    return AssessmentSummaryResponse(
        session_id=session_id,
        candidate_id=str(session.candidate_id),
        recommendation=assessment.recommendation.value,
        recommendation_rationale=assessment.recommendation_rationale,
        composite_score=assessment.composite_score.composite_score,
        evidence_quality=assessment.composite_score.evidence_quality,
        confidence=assessment.composite_score.confidence,
        trait_scores=[
            TraitScoreResponse(
                trait_id=ts.trait_id,
                trait_name=ts.trait_name,
                raw_score=ts.raw_score,
                calibrated_score=ts.calibrated_score,
                confidence=ts.confidence,
                explanation=ts.explanation,
                evidence_summary=ts.evidence_summary,
                signal_gaps=ts.signal_gaps,
            )
            for ts in trait_scores
        ],
        key_strengths=assessment.key_strengths,
        development_areas=assessment.development_areas,
        counter_indicator_flags=assessment.counter_indicator_flags,
        assessment_summary=assessment.assessment_summary,
    )
