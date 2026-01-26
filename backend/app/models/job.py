"""Job model."""

import enum
import uuid
from typing import TYPE_CHECKING, List, Optional

from sqlalchemy import ForeignKey, String, Text, Enum
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base, TimestampMixin, UUIDMixin

if TYPE_CHECKING:
    from app.models.organization import Organization
    from app.models.role_profile import RoleProfile
    from app.models.user import User


class JobStatus(str, enum.Enum):
    """Job posting status."""
    DRAFT = "DRAFT"
    OPEN = "OPEN"
    CLOSED = "CLOSED"
    ON_HOLD = "ON_HOLD"


class Job(Base, UUIDMixin, TimestampMixin):
    """Job posting with objective requirements for candidate screening."""

    __tablename__ = "jobs"

    organization_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("organizations.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )

    # Link to role profile for trait assessment
    role_profile_id: Mapped[Optional[uuid.UUID]] = mapped_column(
        ForeignKey("role_profiles.id", ondelete="SET NULL"),
        nullable=True,
        index=True,
    )

    # Basic info
    title: Mapped[str] = mapped_column(String(255), nullable=False)
    description: Mapped[str] = mapped_column(Text, nullable=False)  # Full job description text
    department: Mapped[Optional[str]] = mapped_column(String(100), nullable=True)
    location: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)
    employment_type: Mapped[Optional[str]] = mapped_column(String(50), nullable=True)  # FULL_TIME, PART_TIME, CONTRACT

    # Extracted requirements (populated by LLM analysis)
    objective_requirements: Mapped[List[dict]] = mapped_column(JSONB, nullable=False, default=list)
    # Format: [
    #   {"id": "uuid", "type": "education", "requirement": "Bachelor's degree in CS or related field", "required": true},
    #   {"id": "uuid", "type": "experience", "requirement": "5+ years software development", "required": true},
    #   {"id": "uuid", "type": "certification", "requirement": "AWS certification", "required": false},
    #   {"id": "uuid", "type": "skill", "requirement": "Python proficiency", "required": true},
    # ]

    nice_to_haves: Mapped[List[dict]] = mapped_column(JSONB, nullable=False, default=list)
    # Format: [{"description": "Experience with microservices"}, ...]

    responsibilities: Mapped[List[str]] = mapped_column(JSONB, nullable=False, default=list)
    # Format: ["Design and implement APIs", "Mentor junior developers", ...]

    suggested_traits: Mapped[List[str]] = mapped_column(JSONB, nullable=False, default=list)
    # Format: ["ANALYTICAL_THINKING", "COLLABORATION", ...] - suggested by LLM based on JD

    # Status
    status: Mapped[JobStatus] = mapped_column(
        Enum(JobStatus),
        default=JobStatus.DRAFT,
        nullable=False,
        index=True,
    )

    # Tracking
    created_by_id: Mapped[Optional[uuid.UUID]] = mapped_column(
        ForeignKey("users.id", ondelete="SET NULL"),
        nullable=True,
    )

    # Analysis metadata
    requirements_extracted_at: Mapped[Optional[str]] = mapped_column(String(50), nullable=True)
    extraction_model: Mapped[Optional[str]] = mapped_column(String(100), nullable=True)

    # Relationships
    organization: Mapped["Organization"] = relationship("Organization", back_populates="jobs")
    role_profile: Mapped[Optional["RoleProfile"]] = relationship("RoleProfile", back_populates="jobs")
    created_by: Mapped[Optional["User"]] = relationship("User")

    def __repr__(self) -> str:
        return f"<Job(id={self.id}, title={self.title}, status={self.status})>"
