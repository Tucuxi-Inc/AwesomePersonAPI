"""Simple Candidate model for Simple Mode assessments."""

import enum
import uuid
from datetime import datetime
from typing import TYPE_CHECKING, Optional

from sqlalchemy import ForeignKey, String, Text, DateTime
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base, TimestampMixin, UUIDMixin

if TYPE_CHECKING:
    from app.models.simple_assessment import SimpleAssessment
    from app.models.interview_session import InterviewSession


class SimpleQualificationStatus(str, enum.Enum):
    """Candidate qualification status."""
    PENDING = "PENDING"
    QUALIFIED = "QUALIFIED"
    NOT_QUALIFIED = "NOT_QUALIFIED"


class SimpleInterviewStatus(str, enum.Enum):
    """Candidate interview status."""
    NOT_STARTED = "NOT_STARTED"
    INVITED = "INVITED"
    IN_PROGRESS = "IN_PROGRESS"
    COMPLETED = "COMPLETED"
    EXPIRED = "EXPIRED"


class SimpleCandidate(Base, UUIDMixin, TimestampMixin):
    """
    Candidate in a Simple Mode assessment.

    Tracks the candidate through the simplified workflow:
    - Resume upload and parsing
    - Qualification screening
    - Magic link invitation
    - Interview completion
    - Results
    """

    __tablename__ = "simple_candidates"

    assessment_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("simple_assessments.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )

    # Candidate info
    email: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    full_name: Mapped[str] = mapped_column(String(255), nullable=False)
    phone: Mapped[Optional[str]] = mapped_column(String(50), nullable=True)

    # Resume data
    resume_file_path: Mapped[Optional[str]] = mapped_column(String(500), nullable=True)
    resume_filename: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)
    resume_raw_text: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    resume_parsed_data: Mapped[Optional[dict]] = mapped_column(JSONB, nullable=True)
    # Format: {
    #   "contact": {...},
    #   "summary": "...",
    #   "experience": [{...}],
    #   "education": [{...}],
    #   "skills": [...],
    #   "certifications": [...]
    # }

    # Qualification screening
    qualification_status: Mapped[SimpleQualificationStatus] = mapped_column(
        default=SimpleQualificationStatus.PENDING,
        nullable=False,
        index=True,
    )
    qualification_results: Mapped[Optional[dict]] = mapped_column(JSONB, nullable=True)
    # Format: [{"requirement_id": "...", "status": "MET/NOT_MET/UNCLEAR",
    #           "evidence": "...", "explanation": "..."}]
    qualification_gaps: Mapped[Optional[dict]] = mapped_column(JSONB, nullable=True)
    # Format: [{"requirement": "...", "explanation": "Why not met"}]

    # Magic link for self-service interview
    magic_link_token: Mapped[Optional[str]] = mapped_column(
        String(255), nullable=True, unique=True, index=True
    )
    magic_link_expires_at: Mapped[Optional[datetime]] = mapped_column(
        DateTime(timezone=True), nullable=True
    )

    # Interview tracking
    interview_status: Mapped[SimpleInterviewStatus] = mapped_column(
        default=SimpleInterviewStatus.NOT_STARTED,
        nullable=False,
        index=True,
    )
    interview_session_id: Mapped[Optional[uuid.UUID]] = mapped_column(
        ForeignKey("interview_sessions.id", ondelete="SET NULL"),
        nullable=True,
    )
    invited_at: Mapped[Optional[datetime]] = mapped_column(
        DateTime(timezone=True), nullable=True
    )
    interview_started_at: Mapped[Optional[datetime]] = mapped_column(
        DateTime(timezone=True), nullable=True
    )
    interview_completed_at: Mapped[Optional[datetime]] = mapped_column(
        DateTime(timezone=True), nullable=True
    )

    # Results (simplified 0-10 scores)
    trait_scores: Mapped[Optional[dict]] = mapped_column(JSONB, nullable=True)
    # Format: {"trait_id": {"score": 8, "confidence": 0.9, "explanation": "..."},
    #          "trait_id2": {...}}
    composite_score: Mapped[Optional[float]] = mapped_column(nullable=True)
    recommendation: Mapped[Optional[str]] = mapped_column(String(50), nullable=True)
    # Values: STRONG_HIRE, HIRE, HOLD, NO_HIRE
    recommendation_rationale: Mapped[Optional[str]] = mapped_column(Text, nullable=True)

    # Relationships
    assessment: Mapped["SimpleAssessment"] = relationship(
        "SimpleAssessment",
        back_populates="candidates",
    )
    interview_session: Mapped[Optional["InterviewSession"]] = relationship(
        "InterviewSession",
        foreign_keys=[interview_session_id],
    )

    def __repr__(self) -> str:
        return f"<SimpleCandidate(id={self.id}, email={self.email}, status={self.interview_status})>"
