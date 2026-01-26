"""Probe model for generated interview probes."""

import uuid
from typing import TYPE_CHECKING, List, Optional

from sqlalchemy import ForeignKey, String, Text
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base, TimestampMixin, UUIDMixin

if TYPE_CHECKING:
    from app.models.interview_session import InterviewSession
    from app.models.trait import Trait


class Probe(Base, UUIDMixin, TimestampMixin):
    """Generated or selected interview probe."""

    __tablename__ = "probes"

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

    # Probe content
    text: Mapped[str] = mapped_column(Text, nullable=False)
    probe_type: Mapped[str] = mapped_column(String(50), nullable=False)
    # Values: PRIMARY, FOLLOW_UP_SITUATION, FOLLOW_UP_TASK, FOLLOW_UP_ACTION,
    #         FOLLOW_UP_RESULT, REFLECTION, RECURSION, DEPTH_ESCALATION

    # Pattern application tracking
    patterns_applied: Mapped[List[str]] = mapped_column(JSONB, nullable=False, default=list)
    # Format: ["MC24", "MC35", "IP7"]

    generation_rationale: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    # Why these patterns were selected and how they shaped the probe

    # Resume customization
    is_resume_customized: Mapped[bool] = mapped_column(default=False, nullable=False)
    resume_anchors: Mapped[List[str]] = mapped_column(JSONB, nullable=False, default=list)
    # Format: ["Amazon Kindle to Echo transition", "AWS migration project"]

    base_probe_id: Mapped[Optional[uuid.UUID]] = mapped_column(
        ForeignKey("probes.id", ondelete="SET NULL"),
        nullable=True,
    )
    # If this probe was customized from a template/base probe

    # Expected evidence
    evidence_expectations: Mapped[List[str]] = mapped_column(JSONB, nullable=False, default=list)
    # Format: ["specific situation context", "personal action taken", "measurable result"]

    follow_up_triggers: Mapped[List[dict]] = mapped_column(JSONB, nullable=False, default=list)
    # Format: [
    #   {"condition": "missing_action", "follow_up_type": "FOLLOW_UP_ACTION"},
    #   {"condition": "surface_response", "follow_up_type": "DEPTH_ESCALATION"}
    # ]

    # STAR component focus
    star_focus: Mapped[Optional[str]] = mapped_column(String(20), nullable=True)
    # Which STAR component this probe primarily targets: situation, task, action, result, reflection

    # Relationships
    session: Mapped["InterviewSession"] = relationship(
        "InterviewSession",
        back_populates="probes",
        foreign_keys=[session_id]
    )
    trait: Mapped["Trait"] = relationship("Trait")

    def __repr__(self) -> str:
        return f"<Probe(id={self.id}, trait_id={self.trait_id}, type={self.probe_type})>"
