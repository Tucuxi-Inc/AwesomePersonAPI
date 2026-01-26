"""Scoring rubric model."""

import uuid
from typing import TYPE_CHECKING, List, Optional

from sqlalchemy import ForeignKey, String, Text, Boolean, Integer
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base, TimestampMixin, UUIDMixin

if TYPE_CHECKING:
    from app.models.organization import Organization
    from app.models.role_profile import RoleProfile


class ScoringRubric(Base, UUIDMixin, TimestampMixin):
    """Scoring rubric for trait assessment."""

    __tablename__ = "scoring_rubrics"

    organization_id: Mapped[Optional[uuid.UUID]] = mapped_column(
        ForeignKey("organizations.id", ondelete="CASCADE"),
        nullable=True,
        index=True,
    )
    role_profile_id: Mapped[Optional[uuid.UUID]] = mapped_column(
        ForeignKey("role_profiles.id", ondelete="SET NULL"),
        nullable=True,
        index=True,
    )
    trait_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("traits.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )

    name: Mapped[str] = mapped_column(String(255), nullable=False)
    description: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    version: Mapped[int] = mapped_column(Integer, default=1, nullable=False)

    # Behavioral anchors for each score level (1-5)
    behavioral_anchors: Mapped[dict] = mapped_column(JSONB, nullable=False)
    # Format: {
    #   "1": {"label": "...", "description": "...", "indicators": ["..."]},
    #   "2": {...}, "3": {...}, "4": {...}, "5": {...}
    # }

    # Interview probes
    primary_probes: Mapped[List[dict]] = mapped_column(JSONB, nullable=False, default=list)
    # Format: [{"question": "...", "purpose": "...", "star_focus": "situation|task|action|result"}, ...]

    follow_up_probes: Mapped[dict] = mapped_column(JSONB, nullable=False, default=dict)
    # Format: {"situation": ["..."], "task": ["..."], "action": ["..."], "result": ["..."]}

    # STAR component indicators
    star_indicators: Mapped[Optional[dict]] = mapped_column(JSONB, nullable=True)
    # Format: {"situation": ["indicator1", ...], "task": [...], ...}

    # Status
    is_default: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)

    # Derivation tracking
    derived_from: Mapped[Optional[uuid.UUID]] = mapped_column(
        ForeignKey("scoring_rubrics.id", ondelete="SET NULL"),
        nullable=True,
    )
    derivation_notes: Mapped[Optional[str]] = mapped_column(Text, nullable=True)

    # Relationships
    organization: Mapped[Optional["Organization"]] = relationship("Organization", back_populates="rubrics")
    role_profile: Mapped[Optional["RoleProfile"]] = relationship("RoleProfile", back_populates="rubrics")

    def __repr__(self) -> str:
        return f"<ScoringRubric(id={self.id}, name={self.name})>"
