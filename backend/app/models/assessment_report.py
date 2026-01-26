"""Assessment report model."""

import uuid
from datetime import datetime
from enum import Enum
from typing import TYPE_CHECKING, List, Optional

from sqlalchemy import ForeignKey, String, Text, DateTime, Float
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base, TimestampMixin, UUIDMixin

if TYPE_CHECKING:
    from app.models.candidate import Candidate


class Recommendation(str, Enum):
    """Hiring recommendation values."""

    STRONG_HIRE = "STRONG_HIRE"
    HIRE = "HIRE"
    HOLD = "HOLD"
    NO_HIRE = "NO_HIRE"


class AssessmentReport(Base, UUIDMixin, TimestampMixin):
    """Final assessment report for a candidate."""

    __tablename__ = "assessment_reports"

    candidate_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("candidates.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    role_profile_id: Mapped[Optional[uuid.UUID]] = mapped_column(
        ForeignKey("role_profiles.id", ondelete="SET NULL"),
        nullable=True,
    )
    generated_by_id: Mapped[Optional[uuid.UUID]] = mapped_column(
        ForeignKey("users.id", ondelete="SET NULL"),
        nullable=True,
    )

    # Report metadata
    version: Mapped[int] = mapped_column(default=1, nullable=False)
    status: Mapped[str] = mapped_column(String(50), default="DRAFT", nullable=False)
    # Values: DRAFT, FINAL, ARCHIVED

    generated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
    )
    finalized_at: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True), nullable=True)

    # Trait scores with full explanations
    trait_scores: Mapped[dict] = mapped_column(JSONB, nullable=False)
    # Format: {
    #   "trait_id": {
    #     "raw_score": 4,
    #     "adjusted_score": 4,  # After valence adjustment
    #     "fit_score": 5,  # How well score matches role optimal range
    #     "confidence": 0.85,
    #     "evidence": [
    #       {"type": "BEHAVIORAL", "text": "...", "weight": 1.0},
    #       ...
    #     ],
    #     "explanation": "Human-readable rationale..."
    #   },
    #   ...
    # }

    # Composite score
    composite_score: Mapped[float] = mapped_column(Float, nullable=False)
    composite_explanation: Mapped[str] = mapped_column(Text, nullable=False)

    # Recommendation
    recommendation: Mapped[str] = mapped_column(String(50), nullable=False)
    recommendation_rationale: Mapped[str] = mapped_column(Text, nullable=False)

    # Counter-indicator flags
    counter_indicator_flags: Mapped[List[dict]] = mapped_column(JSONB, nullable=False, default=list)
    # Format: [
    #   {
    #     "trait_id": "...",
    #     "score": 5,
    #     "severity": "HIGH|MEDIUM",
    #     "rationale": "...",
    #     "recommended_action": "..."
    #   },
    #   ...
    # ]
    has_counter_indicators: Mapped[bool] = mapped_column(default=False, nullable=False)

    # Strengths and development areas
    key_strengths: Mapped[List[dict]] = mapped_column(JSONB, nullable=False, default=list)
    # Format: [{"trait_id": "...", "description": "..."}, ...]

    development_areas: Mapped[List[dict]] = mapped_column(JSONB, nullable=False, default=list)
    # Format: [{"trait_id": "...", "description": "...", "suggestions": [...]}, ...]

    # Interview summary
    interview_summary: Mapped[str] = mapped_column(Text, nullable=False)

    # Additional notes
    notes: Mapped[Optional[str]] = mapped_column(Text, nullable=True)

    # Derivation tracking
    source_sessions: Mapped[List[str]] = mapped_column(JSONB, nullable=False, default=list)
    # List of interview_session IDs used to generate this report

    # Relationships
    candidate: Mapped["Candidate"] = relationship("Candidate", back_populates="assessment_reports")

    def __repr__(self) -> str:
        return f"<AssessmentReport(id={self.id}, candidate_id={self.candidate_id}, recommendation={self.recommendation})>"
