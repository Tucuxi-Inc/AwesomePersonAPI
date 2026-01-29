"""Simple Assessment model for API-first streamlined interface."""

import enum
import uuid
from datetime import datetime
from typing import TYPE_CHECKING, List, Optional

from sqlalchemy import ForeignKey, String, Text, Boolean, DateTime, Integer
from sqlalchemy.dialects.postgresql import JSONB, ARRAY
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base, TimestampMixin, UUIDMixin

if TYPE_CHECKING:
    from app.models.organization import Organization
    from app.models.api_key import APIKey
    from app.models.simple_candidate import SimpleCandidate


class SimpleAssessmentStatus(str, enum.Enum):
    """Simple assessment status."""
    DRAFT = "DRAFT"
    REQUIREMENTS_PENDING = "REQUIREMENTS_PENDING"
    TRAITS_PENDING = "TRAITS_PENDING"
    CANDIDATES_PENDING = "CANDIDATES_PENDING"
    INTERVIEWING = "INTERVIEWING"
    COMPLETED = "COMPLETED"


class SimpleAssessment(Base, UUIDMixin, TimestampMixin):
    """
    Simplified assessment for API consumers and demo users.

    Provides a streamlined 7-step workflow:
    1. Enter job description
    2. Confirm extracted requirements
    3. Upload candidate resumes
    4. Select traits (max 5)
    5. Conduct interviews (via magic links)
    6. View results
    7. Export report
    """

    __tablename__ = "simple_assessments"

    organization_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("organizations.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    api_key_id: Mapped[Optional[uuid.UUID]] = mapped_column(
        ForeignKey("api_keys.id", ondelete="SET NULL"),
        nullable=True,
        index=True,
    )
    created_by_id: Mapped[Optional[uuid.UUID]] = mapped_column(
        ForeignKey("users.id", ondelete="SET NULL"),
        nullable=True,
    )

    # Job details (Step 1)
    job_title: Mapped[str] = mapped_column(String(255), nullable=False)
    job_description: Mapped[str] = mapped_column(Text, nullable=False)

    # Extracted requirements (Step 2)
    extracted_requirements: Mapped[List[dict]] = mapped_column(
        JSONB, nullable=False, default=list
    )
    # Format: [{"id": "uuid", "type": "education|experience|skill|certification",
    #           "requirement": "text", "required": true}]
    requirements_confirmed: Mapped[bool] = mapped_column(
        Boolean, default=False, nullable=False
    )
    requirements_confirmed_at: Mapped[Optional[datetime]] = mapped_column(
        DateTime(timezone=True), nullable=True
    )

    # Selected traits (Step 4) - max 5
    selected_trait_ids: Mapped[List[str]] = mapped_column(
        JSONB, nullable=False, default=list
    )

    # Status tracking
    status: Mapped[SimpleAssessmentStatus] = mapped_column(
        default=SimpleAssessmentStatus.DRAFT,
        nullable=False,
        index=True,
    )

    # Completion tracking
    completed_at: Mapped[Optional[datetime]] = mapped_column(
        DateTime(timezone=True), nullable=True
    )

    # Statistics (denormalized for quick access)
    total_candidates: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    qualified_candidates: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    interviews_completed: Mapped[int] = mapped_column(Integer, default=0, nullable=False)

    # Relationships
    organization: Mapped["Organization"] = relationship("Organization")
    api_key: Mapped[Optional["APIKey"]] = relationship("APIKey")
    candidates: Mapped[List["SimpleCandidate"]] = relationship(
        "SimpleCandidate",
        back_populates="assessment",
        cascade="all, delete-orphan",
    )

    def __repr__(self) -> str:
        return f"<SimpleAssessment(id={self.id}, title={self.job_title}, status={self.status})>"
