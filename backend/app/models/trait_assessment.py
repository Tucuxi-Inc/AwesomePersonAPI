"""Trait assessment model for per-trait assessment during interview."""

import uuid
from enum import Enum
from typing import TYPE_CHECKING, List, Optional

from sqlalchemy import ForeignKey, String, Text, Integer, Float
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base, TimestampMixin, UUIDMixin

if TYPE_CHECKING:
    from app.models.interview_session import InterviewSession
    from app.models.trait import Trait


class AssessmentStatus(str, Enum):
    """Status of trait assessment."""
    NOT_STARTED = "NOT_STARTED"
    IN_PROGRESS = "IN_PROGRESS"
    NEEDS_RECURSION = "NEEDS_RECURSION"  # Low confidence, need second example
    COMPLETED = "COMPLETED"
    SKIPPED = "SKIPPED"


class TraitAssessment(Base, UUIDMixin, TimestampMixin):
    """Per-trait assessment during an interview session."""

    __tablename__ = "trait_assessments"

    session_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("interview_sessions.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    trait_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("traits.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    rubric_id: Mapped[Optional[uuid.UUID]] = mapped_column(
        ForeignKey("scoring_rubrics.id", ondelete="SET NULL"),
        nullable=True,
    )

    # Assessment status
    status: Mapped[str] = mapped_column(
        String(30),
        default=AssessmentStatus.NOT_STARTED.value,
        nullable=False
    )

    # Scoring
    raw_score: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)
    # 1-5 score before calibration

    confidence: Mapped[float] = mapped_column(Float, default=0.0, nullable=False)
    # 0.0-1.0 confidence in the assessment

    # Evidence tracking
    evidence_count: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    behavioral_evidence_count: Mapped[int] = mapped_column(Integer, default=0, nullable=False)

    # STAR+ coverage for this trait
    star_coverage: Mapped[dict] = mapped_column(JSONB, nullable=False, default=dict)
    # Format: {
    #   "situation": true,
    #   "task": true,
    #   "action": true,
    #   "result": false,
    #   "reflection": false,
    #   "recursion": false  # Has second example
    # }

    # Probes used for this trait
    probes_used_count: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    has_primary_probe: Mapped[bool] = mapped_column(default=False, nullable=False)
    has_follow_ups: Mapped[bool] = mapped_column(default=False, nullable=False)
    has_reflection: Mapped[bool] = mapped_column(default=False, nullable=False)
    has_recursion: Mapped[bool] = mapped_column(default=False, nullable=False)

    # Response quality indicators
    last_response_depth: Mapped[Optional[str]] = mapped_column(String(20), nullable=True)
    # SURFACE, MODERATE, DEEP

    last_evidence_type: Mapped[Optional[str]] = mapped_column(String(20), nullable=True)
    # Last extracted evidence type

    # Signal gaps identified
    signal_gaps: Mapped[List[str]] = mapped_column(JSONB, nullable=False, default=list)
    # Format: ["No behavioral evidence", "Missing conflict example", "No failure scenario"]

    # Matched behavioral anchors
    matched_anchors: Mapped[List[dict]] = mapped_column(JSONB, nullable=False, default=list)
    # Format: [{"score": 4, "anchor": "Clear examples...", "evidence_ids": [...]}]

    # Explanation
    explanation: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    # Human-readable rationale for the score

    score_rationale: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    # Detailed reasoning for scoring decision

    # Patterns applied during assessment
    patterns_applied: Mapped[List[str]] = mapped_column(JSONB, nullable=False, default=list)
    # All reasoning patterns used: ["MC24", "MC35", "IP7", ...]

    # Relationships
    session: Mapped["InterviewSession"] = relationship(
        "InterviewSession",
        back_populates="trait_assessments"
    )
    trait: Mapped["Trait"] = relationship("Trait")

    @property
    def needs_more_evidence(self) -> bool:
        """Check if more evidence is needed."""
        return self.confidence < 0.6 or self.behavioral_evidence_count < 1

    @property
    def star_completeness(self) -> float:
        """Calculate STAR completeness percentage."""
        components = ['situation', 'task', 'action', 'result']
        present = sum(1 for c in components if self.star_coverage.get(c, False))
        return present / len(components)

    def __repr__(self) -> str:
        return f"<TraitAssessment(id={self.id}, trait_id={self.trait_id}, score={self.raw_score})>"
