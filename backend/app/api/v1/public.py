"""Public endpoints for self-service access (no authentication required)."""

from datetime import datetime, timezone
from typing import Optional
import uuid

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.dependencies import get_db
from app.models import (
    Invitation,
    InvitationType,
    InvitationStatus,
    Candidate,
    TopPerformer,
    Organization,
    RoleProfile,
    InterviewSession,
    TrainingSession,
    Trait,
    Resume,
    ScoringRubric,
)
from app.schemas.invitation import (
    InvitationValidateResponse,
    SelfServiceSessionStart,
    SelfServiceSessionResponse,
    SelfServiceResponseSubmit,
    DisclosureResponse,
)
from app.services import get_interview_engine, InterviewConfig
from app.services.trait_extractor import get_trait_extractor
from app.services.profiling_engine import get_profiling_engine
from app.services.disclosure_generator import CandidateDisclosureGenerator
from app.api.v1.interviews import _active_sessions, _state_to_dict, _dict_to_state
from app.api.v1.profiling import _session_states
from sqlalchemy.orm.attributes import flag_modified
from sqlalchemy import func

router = APIRouter()


async def get_invitation_by_token(
    db: AsyncSession, token: str
) -> Optional[Invitation]:
    """Get invitation by token."""
    result = await db.execute(
        select(Invitation).where(Invitation.token == token)
    )
    return result.scalar_one_or_none()


@router.get("/invite/{token}/validate", response_model=InvitationValidateResponse)
async def validate_invitation(
    token: str,
    db: AsyncSession = Depends(get_db),
) -> InvitationValidateResponse:
    """Validate an invitation token and return public info."""
    invitation = await get_invitation_by_token(db, token)

    if not invitation:
        return InvitationValidateResponse(
            valid=False,
            error="Invalid invitation link",
        )

    # Check if expired
    if invitation.is_expired:
        if invitation.status != InvitationStatus.EXPIRED:
            invitation.status = InvitationStatus.EXPIRED
            await db.commit()
        return InvitationValidateResponse(
            valid=False,
            error="This invitation has expired",
        )

    # Check status
    if invitation.status == InvitationStatus.REVOKED:
        return InvitationValidateResponse(
            valid=False,
            error="This invitation has been revoked",
        )

    if invitation.status == InvitationStatus.COMPLETED:
        return InvitationValidateResponse(
            valid=False,
            error="This session has already been completed",
        )

    if invitation.status == InvitationStatus.IN_PROGRESS:
        # Allow resuming in-progress sessions
        pass

    # Get organization name
    org_result = await db.execute(
        select(Organization).where(Organization.id == invitation.organization_id)
    )
    org = org_result.scalar_one_or_none()

    # Get role name if applicable
    role_name = None
    if invitation.role_profile_id:
        role_result = await db.execute(
            select(RoleProfile).where(RoleProfile.id == invitation.role_profile_id)
        )
        role = role_result.scalar_one_or_none()
        if role:
            role_name = role.name

    # Mark as viewed if first time
    if invitation.status == InvitationStatus.PENDING:
        invitation.status = InvitationStatus.VIEWED
        invitation.viewed_at = datetime.utcnow()
        await db.commit()

    return InvitationValidateResponse(
        valid=True,
        invitation_type=invitation.invitation_type.value,
        recipient_name=invitation.recipient_name,
        organization_name=org.name if org else None,
        role_name=role_name,
        custom_message=invitation.custom_message,
        expires_at=invitation.expires_at,
    )


@router.get("/invite/{token}/disclosure", response_model=DisclosureResponse)
async def get_disclosure(
    token: str,
    db: AsyncSession = Depends(get_db),
) -> DisclosureResponse:
    """Get disclosure content for a candidate invitation."""
    invitation = await get_invitation_by_token(db, token)

    if not invitation:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Invalid invitation",
        )

    if invitation.invitation_type != InvitationType.CANDIDATE_INTERVIEW:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Disclosure only required for candidate interviews",
        )

    # Get trait names
    trait_names = []
    if invitation.trait_ids:
        for trait_id in invitation.trait_ids:
            result = await db.execute(
                select(Trait).where(Trait.id == uuid.UUID(trait_id))
            )
            trait = result.scalar_one_or_none()
            if trait:
                trait_names.append(trait.name)

    # Generate disclosure content using async method
    disclosure_gen = CandidateDisclosureGenerator()
    disclosure = await disclosure_gen.generate_pre_assessment_disclosure(
        db=db,
        organization_id=invitation.organization_id,
        role_profile_id=invitation.role_profile_id,
        trait_names=trait_names or ["various competencies"],
        jurisdiction="DEFAULT",
    )

    # Convert sections to dict format
    sections = [{"heading": s.heading, "content": s.content} for s in disclosure.sections]

    return DisclosureResponse(
        title=disclosure.title,
        sections=sections,
        consent_required=disclosure.consent_required,
        consent_text=disclosure.consent_text,
        jurisdiction=disclosure.jurisdiction,
    )


@router.post("/invite/{token}/start", response_model=SelfServiceSessionResponse)
async def start_self_service_session(
    token: str,
    start_data: SelfServiceSessionStart,
    db: AsyncSession = Depends(get_db),
) -> SelfServiceSessionResponse:
    """Start a self-service interview or profiling session."""
    invitation = await get_invitation_by_token(db, token)

    if not invitation:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Invalid invitation",
        )

    if not invitation.is_valid and invitation.status != InvitationStatus.IN_PROGRESS:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="This invitation is no longer valid",
        )

    # For candidate interviews, require consent
    if invitation.invitation_type == InvitationType.CANDIDATE_INTERVIEW:
        if not start_data.consent_given:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Consent is required to proceed with the assessment",
            )

    # Check if already has an active session
    if invitation.status == InvitationStatus.IN_PROGRESS:
        # Resume existing session
        if invitation.invitation_type == InvitationType.CANDIDATE_INTERVIEW:
            if invitation.interview_session_id:
                session_id_str = str(invitation.interview_session_id)
                session_data = _active_sessions.get(session_id_str)
                if session_data:
                    # Resume from stored state
                    state = _dict_to_state(session_data["state"])
                    # Find last prompt from exchanges
                    last_prompt = "Please continue with your response."
                    for exchange in reversed(state.exchanges):
                        if exchange.get("role") == "interviewer":
                            last_prompt = exchange.get("content", last_prompt)
                            break
                    # Calculate progress from trait_progress
                    completed_traits = sum(1 for p in state.trait_progress.values() if p.is_complete)
                    total_traits = len(state.trait_progress)
                    overall_progress = completed_traits / total_traits if total_traits > 0 else 0.0
                    # Get current trait name from trait_progress
                    trait_ids = list(state.trait_progress.keys())
                    current_trait_name = None
                    if state.current_trait_index < len(trait_ids):
                        current_trait_id = trait_ids[state.current_trait_index]
                        current_trait_name = state.trait_progress[current_trait_id].trait_name
                    # Check if complete by phase
                    from app.services.interview_engine import InterviewPhase
                    is_complete = state.phase == InterviewPhase.COMPLETED
                    return SelfServiceSessionResponse(
                        session_id=invitation.interview_session_id,
                        session_type="interview",
                        next_prompt=last_prompt,
                        prompt_type="RESUME",
                        trait_name=current_trait_name,
                        overall_progress=overall_progress,
                        is_complete=is_complete,
                    )
        else:
            if invitation.training_session_id:
                session_id_str = str(invitation.training_session_id)
                state = _session_states.get(session_id_str)
                if state:
                    # Find last prompt from transcript
                    last_prompt = "Please continue with your response."
                    for entry in reversed(state.transcript):
                        if entry.get("role") == "interviewer":
                            last_prompt = entry.get("content", last_prompt)
                            break
                    overall_progress = state.current_trait_index / len(state.target_traits) if state.target_traits else 0.0
                    return SelfServiceSessionResponse(
                        session_id=invitation.training_session_id,
                        session_type="profiling",
                        next_prompt=last_prompt,
                        prompt_type="RESUME",
                        trait_name=state.target_traits[state.current_trait_index]["name"] if state.current_trait_index < len(state.target_traits) else None,
                        overall_progress=overall_progress,
                        is_complete=False,
                    )

    # Start new session
    if invitation.invitation_type == InvitationType.CANDIDATE_INTERVIEW:
        return await _start_candidate_interview(db, invitation)
    else:
        return await _start_profiling_session(db, invitation)


async def _start_candidate_interview(
    db: AsyncSession, invitation: Invitation
) -> SelfServiceSessionResponse:
    """Start a candidate interview session."""
    # Get candidate
    candidate_result = await db.execute(
        select(Candidate).where(Candidate.id == invitation.candidate_id)
    )
    candidate = candidate_result.scalar_one_or_none()
    if not candidate:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Candidate not found"
        )

    # Get traits to assess
    trait_ids = invitation.trait_ids or []
    if trait_ids:
        trait_query = select(Trait).where(
            Trait.id.in_([uuid.UUID(tid) if isinstance(tid, str) else tid for tid in trait_ids])
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

    # Get behavioral anchors from rubric if specified
    behavioral_anchors = {}
    if invitation.role_profile_id:
        # Try to find rubrics for traits in this role
        for t in traits:
            rubric_result = await db.execute(
                select(ScoringRubric).where(ScoringRubric.trait_id == t.id)
            )
            rubric = rubric_result.scalar_one_or_none()
            if rubric and rubric.behavioral_anchors:
                behavioral_anchors[str(t.id)] = rubric.behavioral_anchors

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

    # Build config for self-service
    config = InterviewConfig()
    config.require_reflection = True
    config.enable_conflict_probing = True

    # Create database session record
    session_id = str(uuid.uuid4())
    db_session = InterviewSession(
        id=uuid.UUID(session_id),
        candidate_id=candidate.id,
        interviewer_id=None,  # Self-service has no interviewer
        rubric_id=None,
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

    # Store state in shared active sessions
    _active_sessions[session_id] = {
        "state": _state_to_dict(state),
        "traits_metadata": {t["id"]: t for t in traits_to_assess},
    }

    # Update invitation
    invitation.status = InvitationStatus.IN_PROGRESS
    invitation.started_at = datetime.now(timezone.utc)
    invitation.interview_session_id = uuid.UUID(session_id)
    await db.commit()

    # Get first prompt from response
    next_prompt = response.next_prompt if response else "Welcome to your assessment."
    prompt_type = response.prompt_type if response else "INTRODUCTION"
    # Get current trait name from trait_progress keys
    trait_ids = list(state.trait_progress.keys()) if state else []
    current_trait_id = trait_ids[state.current_trait_index] if state and state.current_trait_index < len(trait_ids) else None
    trait_name = traits_to_assess[state.current_trait_index]["name"] if state and state.current_trait_index < len(traits_to_assess) else None

    return SelfServiceSessionResponse(
        session_id=uuid.UUID(session_id),
        session_type="interview",
        next_prompt=next_prompt,
        prompt_type=prompt_type,
        trait_name=trait_name,
        overall_progress=0.0,
        is_complete=False,
    )


async def _start_profiling_session(
    db: AsyncSession, invitation: Invitation
) -> SelfServiceSessionResponse:
    """Start a top performer profiling session."""
    # Get top performer
    performer_result = await db.execute(
        select(TopPerformer).where(TopPerformer.id == invitation.top_performer_id)
    )
    performer = performer_result.scalar_one_or_none()
    if not performer:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Top performer not found"
        )

    # Get trait definitions
    trait_ids = invitation.trait_ids or []
    if trait_ids:
        traits_query = select(Trait).where(
            Trait.id.in_([uuid.UUID(tid) if isinstance(tid, str) else tid for tid in trait_ids])
        )
    else:
        # Default to first 6 traits
        traits_query = select(Trait).limit(6)

    traits_result = await db.execute(traits_query)
    traits = list(traits_result.scalars().all())

    if not traits:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="No traits found"
        )

    target_traits = [
        {"id": t.name, "name": t.name, "definition": t.definition}
        for t in traits
    ]

    # Get next session number
    count_query = select(func.count()).where(TrainingSession.top_performer_id == invitation.top_performer_id)
    count_result = await db.execute(count_query)
    session_count = count_result.scalar() or 0

    # Create training session
    session = TrainingSession(
        top_performer_id=invitation.top_performer_id,
        interviewer_id=None,  # Self-service has no interviewer
        session_number=session_count + 1,
        target_traits=[t["id"] for t in target_traits],
        status="IN_PROGRESS",
        started_at=datetime.now(timezone.utc),
    )

    db.add(session)
    await db.commit()
    await db.refresh(session)

    # Initialize profiling engine
    engine = get_profiling_engine()

    performer_context = {
        "name": performer.name or "Participant",
        "role_category": performer.role_category,
        "job_title": performer.job_title,
        "department": performer.department,
        "tenure_months": performer.tenure_months,
    }

    state, response = await engine.start_session(
        session_id=str(session.id),
        top_performer_id=str(performer.id),
        performer_context=performer_context,
        target_traits=target_traits,
    )

    # Store state in memory
    _session_states[str(session.id)] = state

    # Update transcript
    session.transcript = [
        {"role": "interviewer", "content": response.next_prompt, "timestamp": datetime.now(timezone.utc).isoformat()}
    ]
    flag_modified(session, "transcript")

    # Update invitation
    invitation.status = InvitationStatus.IN_PROGRESS
    invitation.started_at = datetime.now(timezone.utc)
    invitation.training_session_id = session.id
    await db.commit()

    return SelfServiceSessionResponse(
        session_id=session.id,
        session_type="profiling",
        next_prompt=response.next_prompt,
        prompt_type=str(response.phase.value if hasattr(response.phase, 'value') else response.phase),
        trait_name=response.current_trait,
        overall_progress=0.0,
        is_complete=response.session_complete,
    )


@router.post("/invite/{token}/respond", response_model=SelfServiceSessionResponse)
async def submit_self_service_response(
    token: str,
    response_data: SelfServiceResponseSubmit,
    db: AsyncSession = Depends(get_db),
) -> SelfServiceSessionResponse:
    """Submit a response in a self-service session."""
    invitation = await get_invitation_by_token(db, token)

    if not invitation:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Invalid invitation",
        )

    if invitation.status != InvitationStatus.IN_PROGRESS:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="No active session for this invitation",
        )

    # Verify session ID matches
    if invitation.invitation_type == InvitationType.CANDIDATE_INTERVIEW:
        if invitation.interview_session_id != response_data.session_id:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Session ID mismatch",
            )

        session_id = str(response_data.session_id)

        # Get session data from active sessions
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
            response_text=response_data.response_text,
            traits_metadata=traits_metadata,
        )

        # Update stored state
        _active_sessions[session_id]["state"] = _state_to_dict(state)

        # Check if complete by response or phase
        from app.services.interview_engine import InterviewPhase
        is_complete = response.interview_complete if response else (state.phase == InterviewPhase.COMPLETED)
        if is_complete:
            invitation.status = InvitationStatus.COMPLETED
            invitation.completed_at = datetime.now(timezone.utc)
            # Clean up active session
            del _active_sessions[session_id]
            await db.commit()

        # Calculate progress from trait_progress
        completed_traits = sum(1 for p in state.trait_progress.values() if p.is_complete)
        total_traits = len(state.trait_progress)
        overall_progress = completed_traits / total_traits if total_traits > 0 else 0.0

        # Get current trait name
        trait_ids = list(state.trait_progress.keys())
        current_trait_name = None
        if state.current_trait_index < len(trait_ids):
            current_trait_id = trait_ids[state.current_trait_index]
            current_trait_name = state.trait_progress[current_trait_id].trait_name

        return SelfServiceSessionResponse(
            session_id=response_data.session_id,
            session_type="interview",
            next_prompt=response.next_prompt if response else "Thank you for completing the assessment!",
            prompt_type=response.prompt_type if response else "COMPLETE",
            trait_name=current_trait_name,
            overall_progress=overall_progress,
            is_complete=is_complete,
        )
    else:
        if invitation.training_session_id != response_data.session_id:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Session ID mismatch",
            )

        session_id = str(response_data.session_id)

        # Get session data from profiling states
        state = _session_states.get(session_id)
        if not state:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Session state not found. Session may have expired."
            )

        # Get training session from DB
        session_result = await db.execute(
            select(TrainingSession).where(TrainingSession.id == response_data.session_id)
        )
        session = session_result.scalar_one_or_none()
        if not session:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Training session not found"
            )

        # Get trait definitions
        traits_query = select(Trait).where(Trait.name.in_(session.target_traits))
        traits_result = await db.execute(traits_query)
        traits = list(traits_result.scalars().all())
        target_traits = [
            {"id": t.name, "name": t.name, "definition": t.definition}
            for t in traits
        ]
        traits_metadata = {t["id"]: t for t in target_traits}

        # Process response through profiling engine
        engine = get_profiling_engine()
        state, response = await engine.process_response(
            state=state,
            response_text=response_data.response_text,
            traits_metadata=traits_metadata,
        )

        # Update stored state
        _session_states[session_id] = state

        is_complete = response.session_complete
        if is_complete:
            invitation.status = InvitationStatus.COMPLETED
            invitation.completed_at = datetime.now(timezone.utc)
            # Clean up state
            if session_id in _session_states:
                del _session_states[session_id]
            await db.commit()

        overall_progress = state.current_trait_index / len(state.target_traits) if state.target_traits else 0.0

        return SelfServiceSessionResponse(
            session_id=response_data.session_id,
            session_type="profiling",
            next_prompt=response.next_prompt if response else "Thank you for your time!",
            prompt_type=str(response.phase.value if hasattr(response.phase, 'value') else response.phase),
            trait_name=response.current_trait,
            overall_progress=overall_progress,
            is_complete=is_complete,
        )


@router.post("/invite/{token}/end", response_model=SelfServiceSessionResponse)
async def end_self_service_session(
    token: str,
    db: AsyncSession = Depends(get_db),
) -> SelfServiceSessionResponse:
    """End a self-service session early."""
    invitation = await get_invitation_by_token(db, token)

    if not invitation:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Invalid invitation",
        )

    if invitation.status != InvitationStatus.IN_PROGRESS:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="No active session to end",
        )

    session_id = None
    session_type = ""

    if invitation.invitation_type == InvitationType.CANDIDATE_INTERVIEW:
        session_id = invitation.interview_session_id
        session_type = "interview"
        if session_id:
            session_id_str = str(session_id)
            # Clean up active session
            if session_id_str in _active_sessions:
                del _active_sessions[session_id_str]

            # Update database session
            db_session_result = await db.execute(
                select(InterviewSession).where(InterviewSession.id == session_id)
            )
            db_session = db_session_result.scalar_one_or_none()
            if db_session:
                db_session.status = "COMPLETED"
                db_session.completed_at = datetime.now(timezone.utc)
                if db_session.started_at:
                    delta = db_session.completed_at - db_session.started_at
                    db_session.duration_minutes = int(delta.total_seconds() / 60)
    else:
        session_id = invitation.training_session_id
        session_type = "profiling"
        if session_id:
            session_id_str = str(session_id)
            # Clean up profiling state
            if session_id_str in _session_states:
                del _session_states[session_id_str]

            # Update database session
            db_session_result = await db.execute(
                select(TrainingSession).where(TrainingSession.id == session_id)
            )
            db_session = db_session_result.scalar_one_or_none()
            if db_session:
                db_session.status = "COMPLETED"
                db_session.completed_at = datetime.now(timezone.utc)

    invitation.status = InvitationStatus.COMPLETED
    invitation.completed_at = datetime.now(timezone.utc)
    await db.commit()

    return SelfServiceSessionResponse(
        session_id=session_id or uuid.uuid4(),
        session_type=session_type,
        next_prompt="Session ended. Thank you for your time!",
        prompt_type="COMPLETE",
        overall_progress=1.0,
        is_complete=True,
    )


# =============================================================================
# Simple Mode Public Interview Endpoints (Magic Links)
# =============================================================================

from app.models import (
    SimpleAssessment,
    SimpleCandidate,
    SimpleInterviewStatus,
)
from app.schemas.simple import (
    PublicInterviewInfoResponse,
    PublicInterviewStartResponse,
    PublicInterviewRespondRequest,
    PublicInterviewRespondResponse,
    PublicInterviewStatusResponse,
)
from app.services.interview_engine import JobContext

# In-memory session storage for simple mode public interviews
_simple_sessions: dict[str, dict] = {}


async def get_simple_candidate_by_token(
    token: str,
    db: AsyncSession,
) -> tuple[SimpleCandidate, SimpleAssessment]:
    """Get simple candidate and assessment by magic link token."""
    result = await db.execute(
        select(SimpleCandidate)
        .where(SimpleCandidate.magic_link_token == token)
        .options(selectinload(SimpleCandidate.assessment))
    )
    candidate = result.scalar_one_or_none()

    if not candidate:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Invalid or expired interview link"
        )

    # Check expiration
    if candidate.magic_link_expires_at:
        if datetime.now(timezone.utc) > candidate.magic_link_expires_at:
            candidate.interview_status = SimpleInterviewStatus.EXPIRED
            await db.commit()
            raise HTTPException(
                status_code=status.HTTP_410_GONE,
                detail="Interview link has expired"
            )

    return candidate, candidate.assessment


@router.get("/simple/{token}", response_model=PublicInterviewInfoResponse)
async def get_simple_interview_info(
    token: str,
    db: AsyncSession = Depends(get_db),
) -> PublicInterviewInfoResponse:
    """Get interview information for the simple mode candidate landing page."""
    candidate, assessment = await get_simple_candidate_by_token(token, db)

    # Get organization name
    org_result = await db.execute(
        select(Organization).where(Organization.id == assessment.organization_id)
    )
    org = org_result.scalar_one()

    return PublicInterviewInfoResponse(
        job_title=assessment.job_title,
        organization_name=org.name,
        candidate_name=candidate.full_name,
        estimated_duration_minutes=30,
        traits_count=len(assessment.selected_trait_ids),
        instructions="""
Welcome to your interview! Here's what to expect:

1. You'll be asked behavioral questions about your past experiences
2. Please provide specific examples with details about:
   - The situation you faced
   - What you did
   - What the outcome was
3. Take your time to think before answering
4. There are no right or wrong answers - we want to hear about your real experiences
5. The interview typically takes 20-30 minutes

When you're ready, click "Start Interview" to begin.
        """.strip(),
    )


@router.post("/simple/{token}/start", response_model=PublicInterviewStartResponse)
async def start_simple_interview(
    token: str,
    db: AsyncSession = Depends(get_db),
) -> PublicInterviewStartResponse:
    """Start the simple mode interview session."""
    candidate, assessment = await get_simple_candidate_by_token(token, db)

    # Check if already completed
    if candidate.interview_status == SimpleInterviewStatus.COMPLETED:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Interview has already been completed"
        )

    # Get traits
    trait_result = await db.execute(
        select(Trait).where(
            Trait.id.in_([uuid.UUID(tid) for tid in assessment.selected_trait_ids])
        )
    )
    traits = trait_result.scalars().all()

    if not traits:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="No traits configured for this assessment"
        )

    # Create interview session
    session_id = str(uuid.uuid4())

    # Create job context from assessment
    job_context = JobContext(
        job_id=str(assessment.id),
        title=assessment.job_title,
        responsibilities=[],
        objective_requirements=assessment.extracted_requirements,
        nice_to_haves=[],
        description=assessment.job_description,
    )

    # Prepare traits metadata
    traits_to_assess = [
        {
            "id": str(t.id),
            "name": t.name,
            "definition": t.definition,
        }
        for t in traits
    ]

    # Build config
    config = InterviewConfig(
        max_duration_minutes=45,
        max_follow_ups_per_trait=2,
        enable_resume_customization=bool(candidate.resume_parsed_data),
        require_reflection=True,
    )

    # Start interview engine
    engine = get_interview_engine()
    state, response = await engine.start_interview(
        session_id=session_id,
        candidate_id=str(candidate.id),
        traits_to_assess=traits_to_assess,
        config=config,
        resume_text=candidate.resume_raw_text,
        job_context=job_context,
        parsed_resume_data=candidate.resume_parsed_data,
    )

    # Create database session record
    db_session = InterviewSession(
        id=uuid.UUID(session_id),
        candidate_id=None,  # Not linked to Candidate model
        simple_candidate_id=candidate.id,  # Linked to SimpleCandidate
        session_type="SIMPLE_MODE",
        status="IN_PROGRESS",
        started_at=datetime.now(timezone.utc),
        target_traits=[str(t.id) for t in traits],
        interview_config=config.__dict__,
        job_context={
            "job_id": str(assessment.id),
            "title": assessment.job_title,
        },
        traits_total=len(traits),
    )
    db.add(db_session)

    # Update candidate
    candidate.interview_status = SimpleInterviewStatus.IN_PROGRESS
    candidate.interview_session_id = uuid.UUID(session_id)
    candidate.interview_started_at = datetime.now(timezone.utc)

    await db.commit()

    # Store state for this session
    _simple_sessions[session_id] = {
        "state": _state_to_dict(state),
        "traits_metadata": {t["id"]: t for t in traits_to_assess},
        "candidate_id": str(candidate.id),
        "assessment_id": str(assessment.id),
        "token": token,
    }

    return PublicInterviewStartResponse(
        session_id=session_id,
        next_prompt=response.next_prompt,
        prompt_type=response.prompt_type,
        trait_name=response.trait_progress.trait_name if response.trait_progress else None,
        overall_progress=response.overall_progress,
    )


@router.post("/simple/{token}/respond", response_model=PublicInterviewRespondResponse)
async def submit_simple_response(
    token: str,
    request: PublicInterviewRespondRequest,
    db: AsyncSession = Depends(get_db),
) -> PublicInterviewRespondResponse:
    """Submit a response to the current simple mode interview prompt."""
    candidate, assessment = await get_simple_candidate_by_token(token, db)

    if candidate.interview_status != SimpleInterviewStatus.IN_PROGRESS:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Interview is not in progress"
        )

    session_id = str(candidate.interview_session_id)
    session_data = _simple_sessions.get(session_id)

    if not session_data:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Interview session not found"
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
    _simple_sessions[session_id]["state"] = _state_to_dict(state)

    # Update database session
    db_session_result = await db.execute(
        select(InterviewSession).where(InterviewSession.id == uuid.UUID(session_id))
    )
    db_session = db_session_result.scalar_one_or_none()
    if db_session:
        db_session.transcript = state.exchanges
        db_session.extracted_evidence = state.evidence_items
        db_session.traits_completed = sum(
            1 for p in state.trait_progress.values() if p.is_complete
        )

    # Check if interview complete
    if response.interview_complete:
        candidate.interview_status = SimpleInterviewStatus.COMPLETED
        candidate.interview_completed_at = datetime.now(timezone.utc)

        if db_session:
            db_session.status = "COMPLETED"
            db_session.completed_at = datetime.now(timezone.utc)

        # Update assessment stats
        assessment.interviews_completed += 1

        # Generate scores
        await _generate_simple_candidate_scores(candidate, state, traits_metadata, db)

        # Check if all interviews complete
        if assessment.interviews_completed >= assessment.qualified_candidates:
            from app.models import SimpleAssessmentStatus
            assessment.status = SimpleAssessmentStatus.COMPLETED
            assessment.completed_at = datetime.now(timezone.utc)

        # Clean up session
        del _simple_sessions[session_id]

    await db.commit()

    return PublicInterviewRespondResponse(
        next_prompt=response.next_prompt,
        prompt_type=response.prompt_type,
        trait_name=response.trait_progress.trait_name if response.trait_progress else None,
        overall_progress=response.overall_progress,
        interview_complete=response.interview_complete,
    )


@router.get("/simple/{token}/status", response_model=PublicInterviewStatusResponse)
async def get_simple_interview_status(
    token: str,
    db: AsyncSession = Depends(get_db),
) -> PublicInterviewStatusResponse:
    """Check the current simple mode interview status."""
    candidate, _ = await get_simple_candidate_by_token(token, db)

    progress = 0.0
    if candidate.interview_status == SimpleInterviewStatus.COMPLETED:
        progress = 1.0
    elif candidate.interview_session_id:
        session_data = _simple_sessions.get(str(candidate.interview_session_id))
        if session_data:
            state_data = session_data["state"]
            total_traits = len(state_data.get("trait_progress", {}))
            completed_traits = sum(
                1 for tp in state_data.get("trait_progress", {}).values()
                if tp.get("is_complete")
            )
            progress = completed_traits / total_traits if total_traits > 0 else 0.0

    return PublicInterviewStatusResponse(
        status=candidate.interview_status.value,
        progress=progress,
        is_complete=candidate.interview_status == SimpleInterviewStatus.COMPLETED,
    )


async def _generate_simple_candidate_scores(
    candidate: SimpleCandidate,
    state,
    traits_metadata: dict,
    db: AsyncSession,
) -> None:
    """Generate scores for a completed simple mode interview."""
    from app.services import get_score_calibrator, EvidenceForScoring, EvidenceType

    calibrator = get_score_calibrator()
    trait_scores = {}
    all_calibrated_scores = []

    for trait_id, progress in state.trait_progress.items():
        trait_meta = traits_metadata.get(trait_id, {})

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
            for e in state.evidence_items
            if e.get("trait_id") == trait_id
        ]

        # Calibrate score
        score = await calibrator.calibrate_trait_score(
            trait_id=trait_id,
            trait_name=trait_meta.get("name", "Unknown"),
            evidence_items=trait_evidence,
            behavioral_anchors={},
            counter_indicators=[],
        )

        all_calibrated_scores.append(score)

        # Convert 1-5 to 0-10 scale
        score_0_10 = (score.calibrated_score - 1) * 2.5

        trait_scores[trait_id] = {
            "trait_name": trait_meta.get("name", "Unknown"),
            "score": round(score_0_10, 1),
            "confidence": score.confidence,
            "explanation": score.explanation,
        }

    # Generate assessment
    assessment = await calibrator.generate_assessment(all_calibrated_scores)

    # Update candidate with results
    candidate.trait_scores = trait_scores
    candidate.composite_score = round((assessment.composite_score.composite_score - 1) * 2.5, 1)
    candidate.recommendation = assessment.recommendation.value
    candidate.recommendation_rationale = assessment.recommendation_rationale
