"""Role profile model."""

import uuid
from typing import TYPE_CHECKING, List, Optional

from sqlalchemy import ForeignKey, String, Text, Boolean
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base, TimestampMixin, UUIDMixin

if TYPE_CHECKING:
    from app.models.organization import Organization
    from app.models.rubric import ScoringRubric
    from app.models.candidate import Candidate
    from app.models.job import Job


class RoleProfile(Base, UUIDMixin, TimestampMixin):
    """Job role configuration with trait requirements."""

    __tablename__ = "role_profiles"

    organization_id: Mapped[Optional[uuid.UUID]] = mapped_column(
        ForeignKey("organizations.id", ondelete="CASCADE"),
        nullable=True,
        index=True,
    )

    name: Mapped[str] = mapped_column(String(255), nullable=False)
    description: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    department: Mapped[Optional[str]] = mapped_column(String(100), nullable=True)
    level: Mapped[Optional[str]] = mapped_column(String(50), nullable=True)  # e.g., "Junior", "Senior", "Lead"
    role_category: Mapped[str] = mapped_column(String(100), nullable=False, index=True)

    # Trait requirements
    critical_traits: Mapped[List[dict]] = mapped_column(JSONB, nullable=False, default=list)
    # Format: [{"trait_id": "...", "level": "HIGH", "weight": 1.5}, ...]

    positive_traits: Mapped[List[dict]] = mapped_column(JSONB, nullable=False, default=list)
    # Format: [{"trait_id": "...", "level": "MODERATE", "weight": 1.0}, ...]

    counter_indicators: Mapped[List[dict]] = mapped_column(JSONB, nullable=False, default=list)
    # Format: [{"trait_id": "...", "threshold": "HIGH", "reason": "..."}, ...]

    valence_notes: Mapped[Optional[dict]] = mapped_column(JSONB, nullable=True)
    # Format: {"trait_name": "context note", ...}

    # Status
    is_template: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)

    # Derivation tracking
    derived_from: Mapped[Optional[uuid.UUID]] = mapped_column(
        ForeignKey("role_profiles.id", ondelete="SET NULL"),
        nullable=True,
    )
    derivation_notes: Mapped[Optional[str]] = mapped_column(Text, nullable=True)

    # Relationships
    organization: Mapped[Optional["Organization"]] = relationship("Organization", back_populates="role_profiles")
    rubrics: Mapped[List["ScoringRubric"]] = relationship("ScoringRubric", back_populates="role_profile")
    candidates: Mapped[List["Candidate"]] = relationship("Candidate", back_populates="role_profile")
    jobs: Mapped[List["Job"]] = relationship("Job", back_populates="role_profile")

    def __repr__(self) -> str:
        return f"<RoleProfile(id={self.id}, name={self.name})>"
