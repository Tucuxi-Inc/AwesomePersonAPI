"""Interview session model for candidate assessment."""

import uuid
from datetime import datetime
from enum import Enum
from typing import TYPE_CHECKING, List, Optional

from sqlalchemy import ForeignKey, String, Text, DateTime, Integer, Float
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base, TimestampMixin, UUIDMixin

if TYPE_CHECKING:
    from app.models.candidate import Candidate
    from app.models.simple_candidate import SimpleCandidate
    from app.models.exchange import Exchange
    from app.models.probe import Probe
    from app.models.evidence_item import EvidenceItem
    from app.models.trait_assessment import TraitAssessment


class InterviewStatus(str, Enum):
    """Interview session status."""
    CREATED = "CREATED"
    SCHEDULED = "SCHEDULED"
    IN_PROGRESS = "IN_PROGRESS"
    PAUSED = "PAUSED"
    COMPLETED = "COMPLETED"
    INTERRUPTED = "INTERRUPTED"
    CANCELLED = "CANCELLED"
    NO_SHOW = "NO_SHOW"


class InterviewSession(Base, UUIDMixin, TimestampMixin):
    """Interview session with a candidate."""

    __tablename__ = "interview_sessions"

    candidate_id: Mapped[Optional[uuid.UUID]] = mapped_column(
        ForeignKey("candidates.id", ondelete="CASCADE"),
        nullable=True,  # Nullable for Simple Mode interviews
        index=True,
    )
    simple_candidate_id: Mapped[Optional[uuid.UUID]] = mapped_column(
        ForeignKey("simple_candidates.id", ondelete="CASCADE"),
        nullable=True,  # Used for Simple Mode interviews
        index=True,
    )
    interviewer_id: Mapped[Optional[uuid.UUID]] = mapped_column(
        ForeignKey("users.id", ondelete="SET NULL"),
        nullable=True,
    )
    rubric_id: Mapped[Optional[uuid.UUID]] = mapped_column(
        ForeignKey("scoring_rubrics.id", ondelete="SET NULL"),
        nullable=True,
    )
    job_id: Mapped[Optional[uuid.UUID]] = mapped_column(
        ForeignKey("jobs.id", ondelete="SET NULL"),
        nullable=True,
        index=True,
    )

    # Session metadata
    session_number: Mapped[int] = mapped_column(Integer, default=1, nullable=False)
    session_type: Mapped[str] = mapped_column(String(50), default="BEHAVIORAL", nullable=False)
    # Values: BEHAVIORAL, TECHNICAL, CASE_STUDY, FINAL

    status: Mapped[str] = mapped_column(String(50), default="SCHEDULED", nullable=False, index=True)
    # Values: SCHEDULED, IN_PROGRESS, COMPLETED, CANCELLED, NO_SHOW

    # Timing
    scheduled_at: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True), nullable=True)
    started_at: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True), nullable=True)
    completed_at: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True), nullable=True)
    duration_minutes: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)

    # Focus areas
    target_traits: Mapped[List[str]] = mapped_column(JSONB, nullable=False, default=list)

    # Conversation transcript
    transcript: Mapped[List[dict]] = mapped_column(JSONB, nullable=False, default=list)
    # Format: [
    #   {
    #     "role": "interviewer|candidate",
    #     "content": "...",
    #     "timestamp": "...",
    #     "probe_type": "primary|follow_up_situation|follow_up_action|...",
    #     "trait_id": "..."
    #   },
    #   ...
    # ]

    # Extracted evidence
    extracted_evidence: Mapped[List[dict]] = mapped_column(JSONB, nullable=False, default=list)
    # Format: [
    #   {
    #     "source_type": "BEHAVIORAL|HYPOTHETICAL|SELF_REPORT|OBSERVED",
    #     "source_text": "...",
    #     "trait_signals": [{"trait_id": "...", "signal": "positive|negative", "strength": 0.8}],
    #     "star_components": {"situation": true, "task": true, "action": true, "result": false},
    #     "confidence": 0.8
    #   },
    #   ...
    # ]

    # Session scores (preliminary, before calibration)
    preliminary_scores: Mapped[Optional[dict]] = mapped_column(JSONB, nullable=True)
    # Format: {"trait_id": {"score": 4, "confidence": 0.8, "evidence_count": 3}, ...}

    # Interview flow tracking
    current_trait_index: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    probes_used: Mapped[List[dict]] = mapped_column(JSONB, nullable=False, default=list)

    # Notes
    interviewer_notes: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    ai_notes: Mapped[Optional[str]] = mapped_column(Text, nullable=True)

    # Interview configuration
    interview_config: Mapped[Optional[dict]] = mapped_column(JSONB, nullable=True)

    # Job context for resume-informed interviews
    job_context: Mapped[Optional[dict]] = mapped_column(JSONB, nullable=True)
    # Format: {
    #   "job_id": "uuid",
    #   "title": "Product Manager",
    #   "responsibilities": ["...", "..."],
    #   "objective_requirements": [...],
    #   "nice_to_haves": [...],
    # }
    # Format: {
    #   "max_duration_minutes": 60,
    #   "enable_resume_customization": true,
    #   "confidence_threshold_for_recursion": 0.6,
    #   "max_follow_ups_per_trait": 3,
    #   ...
    # }

    # Overall progress tracking
    overall_confidence: Mapped[float] = mapped_column(Float, default=0.0, nullable=False)
    traits_completed: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    traits_total: Mapped[int] = mapped_column(Integer, default=0, nullable=False)

    # Relationships
    candidate: Mapped[Optional["Candidate"]] = relationship(
        "Candidate",
        back_populates="interview_sessions",
        foreign_keys=[candidate_id],
    )
    simple_candidate: Mapped[Optional["SimpleCandidate"]] = relationship(
        "SimpleCandidate",
        foreign_keys=[simple_candidate_id],
    )
    exchanges: Mapped[List["Exchange"]] = relationship(
        "Exchange",
        back_populates="session",
        order_by="Exchange.sequence_number",
        cascade="all, delete-orphan"
    )
    probes: Mapped[List["Probe"]] = relationship(
        "Probe",
        back_populates="session",
        foreign_keys="Probe.session_id",
        cascade="all, delete-orphan"
    )
    evidence_items: Mapped[List["EvidenceItem"]] = relationship(
        "EvidenceItem",
        back_populates="session",
        cascade="all, delete-orphan"
    )
    trait_assessments: Mapped[List["TraitAssessment"]] = relationship(
        "TraitAssessment",
        back_populates="session",
        cascade="all, delete-orphan"
    )

    def __repr__(self) -> str:
        return f"<InterviewSession(id={self.id}, candidate_id={self.candidate_id}, type={self.session_type})>"
