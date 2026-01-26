"""Training session model for top performer profiling."""

import uuid
from datetime import datetime
from typing import TYPE_CHECKING, List, Optional

from sqlalchemy import ForeignKey, String, Text, DateTime
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base, TimestampMixin, UUIDMixin

if TYPE_CHECKING:
    from app.models.top_performer import TopPerformer


class TrainingSession(Base, UUIDMixin, TimestampMixin):
    """Training-framed profiling conversation with a top performer."""

    __tablename__ = "training_sessions"

    top_performer_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("top_performers.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    interviewer_id: Mapped[Optional[uuid.UUID]] = mapped_column(
        ForeignKey("users.id", ondelete="SET NULL"),
        nullable=True,
    )

    # Session metadata
    session_number: Mapped[int] = mapped_column(default=1, nullable=False)
    status: Mapped[str] = mapped_column(String(50), default="SCHEDULED", nullable=False)
    # Values: SCHEDULED, IN_PROGRESS, COMPLETED, CANCELLED

    scheduled_at: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True), nullable=True)
    started_at: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True), nullable=True)
    completed_at: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True), nullable=True)
    duration_minutes: Mapped[Optional[int]] = mapped_column(nullable=True)

    # Focus areas for this session
    target_traits: Mapped[List[str]] = mapped_column(JSONB, nullable=False, default=list)
    focus_areas: Mapped[Optional[str]] = mapped_column(Text, nullable=True)

    # Conversation transcript
    transcript: Mapped[List[dict]] = mapped_column(JSONB, nullable=False, default=list)
    # Format: [{"role": "interviewer|performer", "content": "...", "timestamp": "..."}, ...]

    # Extracted data
    extracted_evidence: Mapped[List[dict]] = mapped_column(JSONB, nullable=False, default=list)
    # Format: [{"trait_id": "...", "evidence_type": "...", "text": "...", "confidence": 0.8}, ...]

    trait_signals: Mapped[List[dict]] = mapped_column(JSONB, nullable=False, default=list)
    # Format: [{"trait_id": "...", "signal": "positive|negative", "strength": 0.8, "source": "..."}, ...]

    counter_indicators_mentioned: Mapped[List[dict]] = mapped_column(JSONB, nullable=False, default=list)
    # Format: [{"trait_id": "...", "context": "...", "quote": "..."}, ...]

    # Session notes and summary
    interviewer_notes: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    ai_summary: Mapped[Optional[str]] = mapped_column(Text, nullable=True)

    # Relationships
    top_performer: Mapped["TopPerformer"] = relationship("TopPerformer", back_populates="training_sessions")

    def __repr__(self) -> str:
        return f"<TrainingSession(id={self.id}, performer_id={self.top_performer_id}, session={self.session_number})>"
