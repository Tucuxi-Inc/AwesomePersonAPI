"""Exchange model for individual Q&A pairs in an interview."""

import uuid
from datetime import datetime
from enum import Enum
from typing import TYPE_CHECKING, Optional

from sqlalchemy import ForeignKey, String, Text, DateTime, Integer
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base, TimestampMixin, UUIDMixin

if TYPE_CHECKING:
    from app.models.interview_session import InterviewSession


class Speaker(str, Enum):
    """Speaker in an exchange."""
    SYSTEM = "SYSTEM"
    CANDIDATE = "CANDIDATE"


class ExchangeType(str, Enum):
    """Type of exchange in the interview."""
    INTRODUCTION = "INTRODUCTION"
    PRIMARY_PROBE = "PRIMARY_PROBE"
    FOLLOW_UP_SITUATION = "FOLLOW_UP_SITUATION"
    FOLLOW_UP_TASK = "FOLLOW_UP_TASK"
    FOLLOW_UP_ACTION = "FOLLOW_UP_ACTION"
    FOLLOW_UP_RESULT = "FOLLOW_UP_RESULT"
    FOLLOW_UP_DEPTH = "FOLLOW_UP_DEPTH"
    REFLECTION = "REFLECTION"
    RECURSION = "RECURSION"
    CANDIDATE_QUESTION = "CANDIDATE_QUESTION"
    SYSTEM_ANSWER = "SYSTEM_ANSWER"
    CLOSING = "CLOSING"
    RESPONSE = "RESPONSE"


class Exchange(Base, UUIDMixin, TimestampMixin):
    """Individual Q&A exchange in an interview session."""

    __tablename__ = "exchanges"

    session_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("interview_sessions.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )

    # Exchange details
    sequence_number: Mapped[int] = mapped_column(Integer, nullable=False)
    speaker: Mapped[str] = mapped_column(String(20), nullable=False)
    exchange_type: Mapped[str] = mapped_column(String(50), nullable=False)
    content: Mapped[str] = mapped_column(Text, nullable=False)

    # Timing
    timestamp: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
    )

    # Context
    trait_id: Mapped[Optional[uuid.UUID]] = mapped_column(
        ForeignKey("traits.id", ondelete="SET NULL"),
        nullable=True,
        index=True,
    )
    probe_id: Mapped[Optional[uuid.UUID]] = mapped_column(
        ForeignKey("probes.id", ondelete="SET NULL"),
        nullable=True,
    )

    # Analysis metadata (populated after response analysis)
    analysis_metadata: Mapped[Optional[dict]] = mapped_column(JSONB, nullable=True)
    # Format: {
    #   "star_completeness": {"situation": true, "task": false, ...},
    #   "evidence_type": "BEHAVIORAL",
    #   "depth": "SURFACE|MODERATE|DEEP",
    #   "patterns_applied": ["MC24", "IP7"],
    #   "follow_up_recommended": ["IP3", "MC38"]
    # }

    # Relationships
    session: Mapped["InterviewSession"] = relationship(
        "InterviewSession",
        back_populates="exchanges"
    )

    def __repr__(self) -> str:
        return f"<Exchange(id={self.id}, speaker={self.speaker}, type={self.exchange_type})>"
