"""Profile development API endpoints for top performer profiling and rubric generation."""

from datetime import datetime, timezone
from typing import List, Optional
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload
from sqlalchemy.orm.attributes import flag_modified

from app.dependencies import get_db, get_current_user
from app.models.top_performer import TopPerformer
from app.models.training_session import TrainingSession
from app.models.user import User
from app.models.trait import Trait
from app.models.rubric import ScoringRubric
from app.schemas.profiling import (
    TopPerformerCreate,
    TopPerformerUpdate,
    TopPerformerResponse,
    TopPerformerList,
    TrainingSessionCreate,
    TrainingSessionUpdate,
    TrainingSessionResponse,
    TrainingSessionDetail,
    TrainingSessionList,
    ProfilingStartRequest,
    ProfilingPromptResponse,
    ProfilingRespondRequest,
    ProfilingCompleteResponse,
    RubricGenerationRequest,
    GeneratedRubricResponse,
    GeneratedRubricItemResponse,
    BehavioralAnchorResponse,
    TraitExtractionResultResponse,
    ExtractedSignalResponse,
    BehavioralPatternResponse,
    CounterIndicatorResponse,
    ProfileSynthesisRequest,
    ProfileSynthesisResponse,
    SynthesizedPatternResponse,
)
from app.services.trait_extractor import get_trait_extractor
from app.services.profiling_engine import (
    get_profiling_engine,
    ProfilingState,
    ProfilingConfig,
    ProfilingPhase,
)
from app.services.rubric_generator import get_rubric_generator


# In-memory state storage for active profiling sessions
# In production, this should be stored in Redis or similar
_session_states: dict = {}

router = APIRouter()


# ============================================================================
# Top Performers CRUD
# ============================================================================


@router.get("/top-performers", response_model=TopPerformerList)
async def list_top_performers(
    role_category: Optional[str] = None,
    profiling_status: Optional[str] = None,
    is_active: bool = True,
    skip: int = Query(0, ge=0),
    limit: int = Query(20, ge=1, le=100),
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """List top performers for the organization."""
    query = select(TopPerformer).where(
        TopPerformer.organization_id == current_user.organization_id,
        TopPerformer.is_active == is_active,
    )

    if role_category:
        query = query.where(TopPerformer.role_category == role_category)
    if profiling_status:
        query = query.where(TopPerformer.profiling_status == profiling_status)

    # Count total
    count_query = select(func.count()).select_from(query.subquery())
    total_result = await db.execute(count_query)
    total = total_result.scalar() or 0

    # Get paginated results
    query = query.order_by(TopPerformer.created_at.desc()).offset(skip).limit(limit)
    result = await db.execute(query)
    performers = result.scalars().all()

    return TopPerformerList(items=performers, total=total)


@router.post("/top-performers", response_model=TopPerformerResponse, status_code=status.HTTP_201_CREATED)
async def create_top_performer(
    data: TopPerformerCreate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """Create a new top performer for profiling."""
    performer = TopPerformer(
        organization_id=current_user.organization_id,
        name=data.name,
        employee_id=data.employee_id,
        email=data.email,
        is_anonymized=data.is_anonymized,
        job_title=data.job_title,
        department=data.department,
        role_category=data.role_category,
        tenure_months=data.tenure_months,
        performance_metrics=data.performance_metrics,
        notes=data.notes,
        profiling_status="PENDING",
    )

    db.add(performer)
    await db.commit()
    await db.refresh(performer)

    return performer


@router.get("/top-performers/{performer_id}", response_model=TopPerformerResponse)
async def get_top_performer(
    performer_id: UUID,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """Get a top performer by ID."""
    query = select(TopPerformer).where(
        TopPerformer.id == performer_id,
        TopPerformer.organization_id == current_user.organization_id,
    )
    result = await db.execute(query)
    performer = result.scalar_one_or_none()

    if not performer:
        raise HTTPException(status_code=404, detail="Top performer not found")

    return performer


@router.patch("/top-performers/{performer_id}", response_model=TopPerformerResponse)
async def update_top_performer(
    performer_id: UUID,
    data: TopPerformerUpdate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """Update a top performer."""
    query = select(TopPerformer).where(
        TopPerformer.id == performer_id,
        TopPerformer.organization_id == current_user.organization_id,
    )
    result = await db.execute(query)
    performer = result.scalar_one_or_none()

    if not performer:
        raise HTTPException(status_code=404, detail="Top performer not found")

    # Update fields
    update_data = data.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(performer, field, value)

    await db.commit()
    await db.refresh(performer)

    return performer


@router.delete("/top-performers/{performer_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_top_performer(
    performer_id: UUID,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """Soft delete a top performer."""
    query = select(TopPerformer).where(
        TopPerformer.id == performer_id,
        TopPerformer.organization_id == current_user.organization_id,
    )
    result = await db.execute(query)
    performer = result.scalar_one_or_none()

    if not performer:
        raise HTTPException(status_code=404, detail="Top performer not found")

    performer.is_active = False
    await db.commit()


# ============================================================================
# Training Sessions CRUD
# ============================================================================


@router.get("/top-performers/{performer_id}/sessions", response_model=TrainingSessionList)
async def list_training_sessions(
    performer_id: UUID,
    status: Optional[str] = None,
    skip: int = Query(0, ge=0),
    limit: int = Query(20, ge=1, le=100),
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """List training sessions for a top performer."""
    # Verify performer exists and belongs to org
    performer_query = select(TopPerformer).where(
        TopPerformer.id == performer_id,
        TopPerformer.organization_id == current_user.organization_id,
    )
    performer_result = await db.execute(performer_query)
    if not performer_result.scalar_one_or_none():
        raise HTTPException(status_code=404, detail="Top performer not found")

    query = select(TrainingSession).where(TrainingSession.top_performer_id == performer_id)

    if status:
        query = query.where(TrainingSession.status == status)

    # Count total
    count_query = select(func.count()).select_from(query.subquery())
    total_result = await db.execute(count_query)
    total = total_result.scalar() or 0

    # Get paginated results
    query = query.order_by(TrainingSession.session_number.desc()).offset(skip).limit(limit)
    result = await db.execute(query)
    sessions = result.scalars().all()

    return TrainingSessionList(items=sessions, total=total)


@router.post("/sessions", response_model=TrainingSessionResponse, status_code=status.HTTP_201_CREATED)
async def create_training_session(
    data: TrainingSessionCreate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """Create a new training session."""
    # Verify performer exists and belongs to org
    performer_query = select(TopPerformer).where(
        TopPerformer.id == data.top_performer_id,
        TopPerformer.organization_id == current_user.organization_id,
    )
    performer_result = await db.execute(performer_query)
    performer = performer_result.scalar_one_or_none()

    if not performer:
        raise HTTPException(status_code=404, detail="Top performer not found")

    # Get next session number
    count_query = select(func.count()).where(TrainingSession.top_performer_id == data.top_performer_id)
    count_result = await db.execute(count_query)
    session_count = count_result.scalar() or 0

    session = TrainingSession(
        top_performer_id=data.top_performer_id,
        interviewer_id=current_user.id,
        session_number=session_count + 1,
        target_traits=data.target_traits,
        focus_areas=data.focus_areas,
        scheduled_at=data.scheduled_at,
        status="SCHEDULED",
    )

    db.add(session)
    await db.commit()
    await db.refresh(session)

    return session


@router.get("/sessions/{session_id}", response_model=TrainingSessionDetail)
async def get_training_session(
    session_id: UUID,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """Get a training session with full details."""
    query = (
        select(TrainingSession)
        .options(selectinload(TrainingSession.top_performer))
        .where(TrainingSession.id == session_id)
    )
    result = await db.execute(query)
    session = result.scalar_one_or_none()

    if not session:
        raise HTTPException(status_code=404, detail="Training session not found")

    # Verify org access
    if session.top_performer.organization_id != current_user.organization_id:
        raise HTTPException(status_code=404, detail="Training session not found")

    return session


@router.patch("/sessions/{session_id}", response_model=TrainingSessionResponse)
async def update_training_session(
    session_id: UUID,
    data: TrainingSessionUpdate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """Update a training session."""
    query = (
        select(TrainingSession)
        .options(selectinload(TrainingSession.top_performer))
        .where(TrainingSession.id == session_id)
    )
    result = await db.execute(query)
    session = result.scalar_one_or_none()

    if not session:
        raise HTTPException(status_code=404, detail="Training session not found")

    if session.top_performer.organization_id != current_user.organization_id:
        raise HTTPException(status_code=404, detail="Training session not found")

    # Update fields
    update_data = data.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(session, field, value)

    await db.commit()
    await db.refresh(session)

    return session


# ============================================================================
# Interactive Profiling Session
# ============================================================================


@router.post("/sessions/start", response_model=ProfilingPromptResponse)
async def start_profiling_session(
    data: ProfilingStartRequest,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """Start an interactive profiling session with a top performer."""
    # Verify performer exists and belongs to org
    performer_query = select(TopPerformer).where(
        TopPerformer.id == data.top_performer_id,
        TopPerformer.organization_id == current_user.organization_id,
    )
    performer_result = await db.execute(performer_query)
    performer = performer_result.scalar_one_or_none()

    if not performer:
        raise HTTPException(status_code=404, detail="Top performer not found")

    # Get trait definitions (target_traits contains trait names)
    traits_query = select(Trait).where(Trait.name.in_(data.target_traits))
    traits_result = await db.execute(traits_query)
    traits = list(traits_result.scalars().all())

    if not traits:
        raise HTTPException(status_code=400, detail="No valid traits specified")

    target_traits = [
        {"id": t.name, "name": t.name, "definition": t.definition}
        for t in traits
    ]

    # Get next session number
    count_query = select(func.count()).where(TrainingSession.top_performer_id == data.top_performer_id)
    count_result = await db.execute(count_query)
    session_count = count_result.scalar() or 0

    # Create training session
    session = TrainingSession(
        top_performer_id=data.top_performer_id,
        interviewer_id=current_user.id,
        session_number=session_count + 1,
        target_traits=[t["id"] for t in target_traits],
        status="IN_PROGRESS",
        started_at=datetime.now(timezone.utc),
    )

    db.add(session)
    await db.commit()
    await db.refresh(session)

    # Update performer status
    performer.profiling_status = "IN_PROGRESS"
    await db.commit()

    # Initialize profiling engine
    engine = get_profiling_engine()

    performer_context = {
        "name": performer.name or "Participant",
        "role_category": performer.role_category,
        "job_title": performer.job_title,
        "department": performer.department,
        "tenure_months": performer.tenure_months,
        **(data.role_context or {}),
    }

    state, response = await engine.start_session(
        session_id=str(session.id),
        top_performer_id=str(performer.id),
        performer_context=performer_context,
        target_traits=target_traits,
    )

    # Store state in memory (in production, use Redis)
    _session_states[str(session.id)] = state

    # Update transcript - must flag_modified for SQLAlchemy to detect JSONB changes
    session.transcript = [
        {"role": "interviewer", "content": response.next_prompt, "timestamp": datetime.now(timezone.utc).isoformat()}
    ]
    flag_modified(session, "transcript")
    await db.commit()

    progress = {
        "current_trait_index": state.current_trait_index,
        "total_traits": len(target_traits),
        "exchanges_count": len(state.transcript),
        "traits_explored": [],
    }

    return ProfilingPromptResponse(
        session_id=session.id,
        phase=str(response.phase.value if hasattr(response.phase, 'value') else response.phase),
        prompt_text=response.next_prompt,
        progress=progress,
        trait_being_explored=response.current_trait,
        is_complete=response.session_complete,
    )


@router.post("/sessions/{session_id}/respond", response_model=ProfilingPromptResponse)
async def submit_profiling_response(
    session_id: UUID,
    data: ProfilingRespondRequest,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """Submit a top performer's response and get the next prompt."""
    query = (
        select(TrainingSession)
        .options(selectinload(TrainingSession.top_performer))
        .where(TrainingSession.id == session_id)
    )
    result = await db.execute(query)
    session = result.scalar_one_or_none()

    if not session:
        raise HTTPException(status_code=404, detail="Training session not found")

    if session.top_performer.organization_id != current_user.organization_id:
        raise HTTPException(status_code=404, detail="Training session not found")

    if session.status != "IN_PROGRESS":
        raise HTTPException(status_code=400, detail="Session is not in progress")

    # Get trait definitions (target_traits contains trait names)
    traits_query = select(Trait).where(Trait.name.in_(session.target_traits))
    traits_result = await db.execute(traits_query)
    traits = list(traits_result.scalars().all())

    target_traits = [
        {"id": t.name, "name": t.name, "definition": t.definition}
        for t in traits
    ]

    # Get stored state
    state = _session_states.get(str(session.id))
    if not state:
        raise HTTPException(status_code=400, detail="Session state not found. Session may have expired.")

    # Build traits metadata
    traits_metadata = {t["id"]: t for t in target_traits}

    # Process response through profiling engine
    engine = get_profiling_engine()

    state, response = await engine.process_response(
        state=state,
        response_text=data.response_text,
        traits_metadata=traits_metadata,
    )

    # Update stored state
    _session_states[str(session.id)] = state

    # Update transcript - use list() to create new list and flag_modified for JSONB
    transcript = list(session.transcript or [])
    transcript.append({"role": "performer", "content": data.response_text, "timestamp": datetime.now(timezone.utc).isoformat()})
    if not response.session_complete:
        transcript.append({"role": "interviewer", "content": response.next_prompt, "timestamp": datetime.now(timezone.utc).isoformat()})
    session.transcript = transcript
    flag_modified(session, "transcript")

    if response.session_complete:
        session.status = "COMPLETED"
        session.completed_at = datetime.now(timezone.utc)
        if session.started_at:
            duration = (session.completed_at - session.started_at).total_seconds() / 60
            session.duration_minutes = int(duration)

        # Extract traits from session
        await _extract_and_store_traits(session, target_traits, db)

        # Clean up state
        if str(session.id) in _session_states:
            del _session_states[str(session.id)]

    await db.commit()

    progress = {
        "current_trait_index": state.current_trait_index,
        "total_traits": len(target_traits),
        "exchanges_count": len(state.transcript),
        "traits_explored": [],
    }

    return ProfilingPromptResponse(
        session_id=session.id,
        phase=str(response.phase.value if hasattr(response.phase, 'value') else response.phase),
        prompt_text=response.next_prompt,
        progress=progress,
        trait_being_explored=response.current_trait,
        is_complete=response.session_complete,
    )


@router.post("/sessions/{session_id}/end", response_model=ProfilingCompleteResponse)
async def end_profiling_session(
    session_id: UUID,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """End a profiling session early and extract traits."""
    query = (
        select(TrainingSession)
        .options(selectinload(TrainingSession.top_performer))
        .where(TrainingSession.id == session_id)
    )
    result = await db.execute(query)
    session = result.scalar_one_or_none()

    if not session:
        raise HTTPException(status_code=404, detail="Training session not found")

    if session.top_performer.organization_id != current_user.organization_id:
        raise HTTPException(status_code=404, detail="Training session not found")

    if session.status == "COMPLETED":
        raise HTTPException(status_code=400, detail="Session is already completed")

    # Get trait definitions (target_traits contains trait names)
    traits_query = select(Trait).where(Trait.name.in_(session.target_traits))
    traits_result = await db.execute(traits_query)
    traits = list(traits_result.scalars().all())

    target_traits = [
        {"id": t.name, "name": t.name, "definition": t.definition}
        for t in traits
    ]

    # Complete session
    session.status = "COMPLETED"
    session.completed_at = datetime.now(timezone.utc)
    if session.started_at:
        duration = (session.completed_at - session.started_at).total_seconds() / 60
        session.duration_minutes = int(duration)

    # Extract traits from session
    extraction_result = await _extract_and_store_traits(session, target_traits, db)

    await db.commit()

    return ProfilingCompleteResponse(
        session_id=session.id,
        summary=extraction_result.summary if extraction_result else "Session completed with insufficient data for extraction.",
        traits_profiled=session.target_traits,
        signals_extracted=len(extraction_result.extracted_signals) if extraction_result else 0,
        patterns_identified=len(extraction_result.behavioral_patterns) if extraction_result else 0,
        counter_indicators_found=len(extraction_result.counter_indicators) if extraction_result else 0,
    )


async def _extract_and_store_traits(session: TrainingSession, target_traits: List[dict], db: AsyncSession):
    """Extract traits from session and store results."""
    if not session.transcript or len(session.transcript) < 2:
        return None

    extractor = get_trait_extractor()

    role_context = {
        "role_category": session.top_performer.role_category,
        "job_title": session.top_performer.job_title,
    }

    extraction_result = await extractor.extract_from_session(
        session_id=str(session.id),
        top_performer_id=str(session.top_performer_id),
        transcript=session.transcript,
        target_traits=target_traits,
        role_context=role_context,
    )

    # Store extraction results in session
    session.extracted_evidence = [
        {
            "trait_id": s.trait_id,
            "evidence_type": s.signal_type,
            "text": s.evidence_text,
            "confidence": s.confidence,
        }
        for s in extraction_result.extracted_signals
    ]

    session.trait_signals = [
        {
            "trait_id": s.trait_id,
            "signal": s.signal_type.lower(),
            "strength": s.strength,
            "source": s.behavioral_indicator,
        }
        for s in extraction_result.extracted_signals
    ]

    session.counter_indicators_mentioned = [
        {
            "trait_id": ci.trait_id,
            "context": ci.context,
            "quote": ci.evidence,
        }
        for ci in extraction_result.counter_indicators
    ]

    session.ai_summary = extraction_result.summary

    # Flag JSONB fields as modified
    flag_modified(session, "extracted_evidence")
    flag_modified(session, "trait_signals")
    flag_modified(session, "counter_indicators_mentioned")

    # Update performer's trait profile
    performer = session.top_performer
    current_profile = performer.trait_profile or {}

    def normalize_trait_id(trait_id: str) -> str:
        """Normalize trait ID for matching: lowercase, replace spaces/underscores."""
        return trait_id.lower().replace("_", " ").replace("-", " ")

    # Build normalized lookup for existing profile keys
    profile_key_lookup = {normalize_trait_id(k): k for k in current_profile.keys()}

    for trait_id, scores in extraction_result.trait_scores.items():
        # Match normalized trait ID to existing profile keys
        normalized_id = normalize_trait_id(trait_id)
        actual_key = profile_key_lookup.get(normalized_id, trait_id)

        if actual_key not in current_profile:
            current_profile[actual_key] = {
                "scores": [],
                "evidence": [],
                "confidence": 0.0,
            }
            profile_key_lookup[normalized_id] = actual_key

        if scores.get("score") is not None:
            current_profile[actual_key]["scores"].append(scores["score"])
            # Match evidence using normalized trait IDs
            current_profile[actual_key]["evidence"].extend(
                [s.evidence_text for s in extraction_result.extracted_signals
                 if normalize_trait_id(s.trait_id) == normalized_id]
            )

            # Calculate average
            all_scores = current_profile[actual_key]["scores"]
            current_profile[actual_key]["average_score"] = sum(all_scores) / len(all_scores)
            current_profile[actual_key]["confidence"] = min(0.95, len(all_scores) * 0.15)

    performer.trait_profile = current_profile
    flag_modified(performer, "trait_profile")

    # Update counter-indicators
    existing_indicators = list(performer.counter_indicators_identified or [])
    for ci in extraction_result.counter_indicators:
        existing_indicators.append({
            "trait_id": ci.trait_id,
            "context": ci.context,
            "evidence": ci.evidence,
            "severity": ci.severity,
        })
    performer.counter_indicators_identified = existing_indicators
    flag_modified(performer, "counter_indicators_identified")

    # Check if profiling is complete (has sufficient evidence for all target traits)
    has_all_traits = all(
        trait_id in current_profile and current_profile[trait_id].get("average_score") is not None
        for trait_id in session.target_traits
    )
    if has_all_traits:
        performer.profiling_status = "COMPLETED"

    return extraction_result


# ============================================================================
# Rubric Generation
# ============================================================================


@router.post("/rubrics/generate", response_model=GeneratedRubricResponse)
async def generate_rubric(
    data: RubricGenerationRequest,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """Generate a scoring rubric from top performer profiles."""
    # Verify all performers exist and belong to org
    performers_query = select(TopPerformer).where(
        TopPerformer.id.in_(data.top_performer_ids),
        TopPerformer.organization_id == current_user.organization_id,
    )
    performers_result = await db.execute(performers_query)
    performers = list(performers_result.scalars().all())

    if len(performers) != len(data.top_performer_ids):
        raise HTTPException(status_code=404, detail="One or more top performers not found")

    # Get completed sessions for these performers
    sessions_query = (
        select(TrainingSession)
        .where(
            TrainingSession.top_performer_id.in_(data.top_performer_ids),
            TrainingSession.status == "COMPLETED",
        )
    )
    sessions_result = await db.execute(sessions_query)
    sessions = list(sessions_result.scalars().all())

    if not sessions:
        raise HTTPException(status_code=400, detail="No completed profiling sessions found")

    # Get trait definitions (target_trait_ids contains trait names)
    traits_query = select(Trait).where(Trait.name.in_(data.target_trait_ids))
    traits_result = await db.execute(traits_query)
    traits = list(traits_result.scalars().all())

    if not traits:
        raise HTTPException(status_code=400, detail="No valid traits specified")

    target_traits = [
        {"id": t.name, "name": t.name, "definition": t.definition}
        for t in traits
    ]

    # Get base rubrics if specified (ScoringRubric is per-trait)
    base_rubric = None
    if data.base_rubric_id:
        # Get all rubrics for the specified role category as base
        rubrics_query = select(ScoringRubric).where(
            ScoringRubric.id == data.base_rubric_id,
            ScoringRubric.organization_id == current_user.organization_id,
        )
        rubric_result = await db.execute(rubrics_query)
        rubric = rubric_result.scalar_one_or_none()
        if rubric:
            # Convert to the format expected by the generator
            base_rubric = {
                "items": [{
                    "trait_id": str(rubric.trait_id),
                    "behavioral_anchors": rubric.behavioral_anchors,
                    "primary_probes": rubric.primary_probes,
                    "follow_up_probes": rubric.follow_up_probes,
                }],
            }

    # Extract traits from all sessions
    extractor = get_trait_extractor()
    extraction_results = []

    for session in sessions:
        performer = next((p for p in performers if p.id == session.top_performer_id), None)
        if not performer:
            continue

        role_context = {
            "role_category": performer.role_category,
            "job_title": performer.job_title,
        }

        extraction_result = await extractor.extract_from_session(
            session_id=str(session.id),
            top_performer_id=str(session.top_performer_id),
            transcript=session.transcript,
            target_traits=target_traits,
            role_context=role_context,
        )
        extraction_results.append(extraction_result)

    # Generate rubric
    generator = get_rubric_generator()

    generated_rubric = await generator.generate_rubric(
        organization_id=str(current_user.organization_id),
        role_category=data.role_category,
        extraction_results=extraction_results,
        target_traits=target_traits,
        role_context=data.role_context,
        base_rubric=base_rubric,
    )

    # Convert to response
    items = [
        GeneratedRubricItemResponse(
            trait_id=item.trait_id,
            trait_name=item.trait_name,
            behavioral_anchors=[
                BehavioralAnchorResponse(
                    score=anchor.score,
                    description=anchor.description,
                    example_behaviors=anchor.example_behaviors,
                    evidence_indicators=anchor.evidence_indicators,
                )
                for anchor in item.behavioral_anchors
            ],
            primary_probes=item.primary_probes,
            follow_up_probes=item.follow_up_probes,
            star_indicators=item.star_indicators,
            job_relatedness_rationale=item.job_relatedness_rationale,
            derivation_notes=item.derivation_notes,
            confidence=item.confidence,
        )
        for item in generated_rubric.items
    ]

    return GeneratedRubricResponse(
        name=generated_rubric.name,
        description=generated_rubric.description,
        organization_id=generated_rubric.organization_id,
        role_category=generated_rubric.role_category,
        items=items,
        derivation_metadata=generated_rubric.derivation_metadata,
        research_basis=generated_rubric.research_basis,
        created_at=generated_rubric.created_at,
    )


@router.post("/rubrics/generate-and-save", response_model=dict)
async def generate_and_save_rubric(
    data: RubricGenerationRequest,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """Generate rubrics and save them to the database (one per trait)."""
    # Generate rubric using the same logic
    generated = await generate_rubric(data, db, current_user)

    # Get trait UUIDs for the foreign key
    trait_names = [item.trait_id for item in generated.items]
    traits_query = select(Trait).where(Trait.name.in_(trait_names))
    traits_result = await db.execute(traits_query)
    traits_by_name = {t.name: t for t in traits_result.scalars().all()}

    # Create individual ScoringRubric entries for each trait
    created_rubrics = []
    for item in generated.items:
        trait = traits_by_name.get(item.trait_id)
        if not trait:
            continue

        # Convert behavioral anchors to the expected dict format
        behavioral_anchors = {}
        for anchor in item.behavioral_anchors:
            behavioral_anchors[str(anchor.score)] = {
                "label": f"Level {anchor.score}",
                "description": anchor.description,
                "indicators": anchor.evidence_indicators,
                "example_behaviors": anchor.example_behaviors,
            }

        # Convert follow-up probes to dict format
        follow_up_probes = {}
        for component in ["situation", "task", "action", "result"]:
            component_probes = [p for p in item.follow_up_probes if component in p.lower()]
            follow_up_probes[component] = component_probes if component_probes else item.follow_up_probes[:2]

        rubric = ScoringRubric(
            organization_id=current_user.organization_id,
            trait_id=trait.id,
            name=f"{item.trait_name} - {generated.role_category}",
            description=item.job_relatedness_rationale,
            behavioral_anchors=behavioral_anchors,
            primary_probes=[{"question": p, "purpose": "primary", "star_focus": "situation"} for p in item.primary_probes],
            follow_up_probes=follow_up_probes,
            star_indicators=item.star_indicators,
            derivation_notes=f"{item.derivation_notes} Generated from {generated.derivation_metadata.get('top_performer_count', 0)} top performer(s).",
            is_active=True,
        )

        db.add(rubric)
        created_rubrics.append(rubric)

    await db.commit()

    # Refresh to get IDs
    for rubric in created_rubrics:
        await db.refresh(rubric)

    return {
        "rubric_count": len(created_rubrics),
        "rubric_ids": [str(r.id) for r in created_rubrics],
        "role_category": generated.role_category,
        "traits": [item.trait_name for item in generated.items],
        "created_at": generated.created_at.isoformat(),
    }


# ============================================================================
# Profile Synthesis
# ============================================================================


@router.post("/synthesize", response_model=ProfileSynthesisResponse)
async def synthesize_profiles(
    data: ProfileSynthesisRequest,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """Synthesize trait patterns across multiple top performers."""
    # Verify all performers exist and belong to org
    performers_query = select(TopPerformer).where(
        TopPerformer.id.in_(data.top_performer_ids),
        TopPerformer.organization_id == current_user.organization_id,
        TopPerformer.profiling_status == "COMPLETED",
    )
    performers_result = await db.execute(performers_query)
    performers = list(performers_result.scalars().all())

    if not performers:
        raise HTTPException(status_code=404, detail="No completed top performer profiles found")

    # Collect all trait profiles
    all_patterns = {}
    common_strengths = set()

    for performer in performers:
        profile = performer.trait_profile or {}
        for trait_id, trait_data in profile.items():
            if trait_id not in all_patterns:
                all_patterns[trait_id] = {
                    "scores": [],
                    "evidence": [],
                }
            if trait_data.get("average_score"):
                all_patterns[trait_id]["scores"].append(trait_data["average_score"])
            if trait_data.get("evidence"):
                all_patterns[trait_id]["evidence"].extend(trait_data["evidence"])

            # Track common strengths (traits with high scores across performers)
            if trait_data.get("average_score", 0) >= 4.0:
                common_strengths.add(trait_id)

    # Get trait names
    trait_ids = list(all_patterns.keys())
    traits_query = select(Trait).where(Trait.name.in_(trait_ids))
    traits_result = await db.execute(traits_query)
    traits = {t.name: t for t in traits_result.scalars().all()}

    # Build synthesized patterns
    synthesized_patterns = []
    for trait_id, pattern_data in all_patterns.items():
        trait = traits.get(trait_id)
        if not trait:
            continue

        avg_score = None
        if pattern_data["scores"]:
            avg_score = sum(pattern_data["scores"]) / len(pattern_data["scores"])

        synthesized_patterns.append(SynthesizedPatternResponse(
            trait_id=trait_id,
            trait_name=trait.name,
            patterns=[],  # Would require re-extraction for patterns
            average_score=avg_score,
            confidence=min(0.95, len(pattern_data["scores"]) * 0.15),
        ))

    # Get common strength names
    strength_names = [traits[tid].name for tid in common_strengths if tid in traits]

    # Derive role success indicators
    role_success_indicators = []
    high_confidence_traits = [p for p in synthesized_patterns if p.confidence >= 0.5 and p.average_score and p.average_score >= 4.0]
    for pattern in high_confidence_traits[:5]:
        role_success_indicators.append(f"Strong {pattern.trait_name} (avg: {pattern.average_score:.1f})")

    return ProfileSynthesisResponse(
        role_category=data.role_category,
        top_performer_count=len(performers),
        synthesized_patterns=synthesized_patterns,
        common_strengths=strength_names,
        role_success_indicators=role_success_indicators,
        generated_at=datetime.now(timezone.utc),
    )


# ============================================================================
# Trait Extraction (Manual)
# ============================================================================


@router.post("/sessions/{session_id}/extract", response_model=TraitExtractionResultResponse)
async def extract_traits_from_session(
    session_id: UUID,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """Manually trigger trait extraction from a completed session."""
    query = (
        select(TrainingSession)
        .options(selectinload(TrainingSession.top_performer))
        .where(TrainingSession.id == session_id)
    )
    result = await db.execute(query)
    session = result.scalar_one_or_none()

    if not session:
        raise HTTPException(status_code=404, detail="Training session not found")

    if session.top_performer.organization_id != current_user.organization_id:
        raise HTTPException(status_code=404, detail="Training session not found")

    if not session.transcript or len(session.transcript) < 2:
        raise HTTPException(status_code=400, detail="Session has insufficient transcript data")

    # Get trait definitions (target_traits contains trait names)
    traits_query = select(Trait).where(Trait.name.in_(session.target_traits))
    traits_result = await db.execute(traits_query)
    traits = list(traits_result.scalars().all())

    target_traits = [
        {"id": t.name, "name": t.name, "definition": t.definition}
        for t in traits
    ]

    # Extract traits
    extractor = get_trait_extractor()

    role_context = {
        "role_category": session.top_performer.role_category,
        "job_title": session.top_performer.job_title,
    }

    extraction_result = await extractor.extract_from_session(
        session_id=str(session.id),
        top_performer_id=str(session.top_performer_id),
        transcript=session.transcript,
        target_traits=target_traits,
        role_context=role_context,
    )

    return TraitExtractionResultResponse(
        session_id=extraction_result.session_id,
        top_performer_id=extraction_result.top_performer_id,
        extracted_signals=[
            ExtractedSignalResponse(
                trait_id=s.trait_id,
                trait_name=s.trait_name,
                signal_type=s.signal_type,
                strength=s.strength,
                evidence_text=s.evidence_text,
                behavioral_indicator=s.behavioral_indicator,
                context=s.context,
                confidence=s.confidence,
            )
            for s in extraction_result.extracted_signals
        ],
        behavioral_patterns=[
            BehavioralPatternResponse(
                trait_id=p.trait_id,
                trait_name=p.trait_name,
                pattern_description=p.pattern_description,
                frequency=p.frequency,
                example_quotes=p.example_quotes,
                implications_for_role=p.implications_for_role,
            )
            for p in extraction_result.behavioral_patterns
        ],
        counter_indicators=[
            CounterIndicatorResponse(
                trait_id=ci.trait_id,
                trait_name=ci.trait_name,
                context=ci.context,
                evidence=ci.evidence,
                role_categories_affected=ci.role_categories_affected,
                severity=ci.severity,
            )
            for ci in extraction_result.counter_indicators
        ],
        trait_scores=extraction_result.trait_scores,
        summary=extraction_result.summary,
    )
