"""Top performer model for profiling."""

import uuid
from typing import TYPE_CHECKING, List, Optional

from sqlalchemy import ForeignKey, String, Text, Boolean
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base, TimestampMixin, UUIDMixin

if TYPE_CHECKING:
    from app.models.organization import Organization
    from app.models.training_session import TrainingSession
    from app.models.invitation import Invitation


class TopPerformer(Base, UUIDMixin, TimestampMixin):
    """Top performer employee for trait profiling."""

    __tablename__ = "top_performers"

    organization_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("organizations.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )

    # Identity (can be anonymized)
    name: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)
    employee_id: Mapped[Optional[str]] = mapped_column(String(100), nullable=True)
    email: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)
    is_anonymized: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)

    # Role information
    job_title: Mapped[str] = mapped_column(String(255), nullable=False)
    department: Mapped[Optional[str]] = mapped_column(String(100), nullable=True)
    role_category: Mapped[str] = mapped_column(String(100), nullable=False, index=True)
    tenure_months: Mapped[Optional[int]] = mapped_column(nullable=True)

    # Performance indicators
    performance_metrics: Mapped[Optional[dict]] = mapped_column(JSONB, nullable=True)
    # Format: {"metric_name": value, ...}

    # Profiling status
    profiling_status: Mapped[str] = mapped_column(String(50), default="PENDING", nullable=False)
    # Values: PENDING, IN_PROGRESS, COMPLETED, ARCHIVED

    # Extracted profile (populated after profiling sessions)
    trait_profile: Mapped[Optional[dict]] = mapped_column(JSONB, nullable=True)
    # Format: {"trait_id": {"score": 4, "evidence": [...], "confidence": 0.8}, ...}

    counter_indicators_identified: Mapped[List[dict]] = mapped_column(JSONB, nullable=False, default=list)
    # Format: [{"trait_id": "...", "context": "...", "evidence": "..."}, ...]

    notes: Mapped[Optional[str]] = mapped_column(Text, nullable=True)

    # Status
    is_active: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)

    # Relationships
    organization: Mapped["Organization"] = relationship("Organization", back_populates="top_performers")
    training_sessions: Mapped[List["TrainingSession"]] = relationship(
        "TrainingSession",
        back_populates="top_performer",
        cascade="all, delete-orphan",
    )
    invitations: Mapped[List["Invitation"]] = relationship(
        "Invitation",
        back_populates="top_performer",
        cascade="all, delete-orphan",
    )

    def __repr__(self) -> str:
        return f"<TopPerformer(id={self.id}, job_title={self.job_title})>"
