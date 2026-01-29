"""Candidate model."""

import uuid
from typing import TYPE_CHECKING, List, Optional

from sqlalchemy import ForeignKey, String, Text, Boolean
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base, TimestampMixin, UUIDMixin

if TYPE_CHECKING:
    from app.models.organization import Organization
    from app.models.role_profile import RoleProfile
    from app.models.resume import Resume
    from app.models.interview_session import InterviewSession
    from app.models.assessment_report import AssessmentReport
    from app.models.invitation import Invitation
    from app.models.candidate_job_screening import CandidateJobScreening


class Candidate(Base, UUIDMixin, TimestampMixin):
    """Job candidate for assessment."""

    __tablename__ = "candidates"

    organization_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("organizations.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    role_profile_id: Mapped[Optional[uuid.UUID]] = mapped_column(
        ForeignKey("role_profiles.id", ondelete="SET NULL"),
        nullable=True,
        index=True,
    )

    # Identity
    email: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    full_name: Mapped[str] = mapped_column(String(255), nullable=False)
    phone: Mapped[Optional[str]] = mapped_column(String(50), nullable=True)

    # Professional info
    current_title: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)
    current_company: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)
    linkedin_url: Mapped[Optional[str]] = mapped_column(String(500), nullable=True)
    years_experience: Mapped[Optional[int]] = mapped_column(nullable=True)

    # Application info
    source: Mapped[Optional[str]] = mapped_column(String(100), nullable=True)  # e.g., "LinkedIn", "Referral"
    referrer: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)

    # Assessment status
    status: Mapped[str] = mapped_column(String(50), default="NEW", nullable=False, index=True)
    # Values: NEW, SCREENING, INTERVIEWING, ASSESSED, OFFER, HIRED, REJECTED, WITHDRAWN

    # Additional data
    notes: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    tags: Mapped[List[str]] = mapped_column(JSONB, nullable=False, default=list)
    custom_fields: Mapped[Optional[dict]] = mapped_column(JSONB, nullable=True)

    # Status
    is_active: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)

    # Relationships
    organization: Mapped["Organization"] = relationship("Organization", back_populates="candidates")
    role_profile: Mapped[Optional["RoleProfile"]] = relationship("RoleProfile", back_populates="candidates")
    resumes: Mapped[List["Resume"]] = relationship("Resume", back_populates="candidate", cascade="all, delete-orphan")
    interview_sessions: Mapped[List["InterviewSession"]] = relationship(
        "InterviewSession",
        back_populates="candidate",
        cascade="all, delete-orphan",
    )
    assessment_reports: Mapped[List["AssessmentReport"]] = relationship(
        "AssessmentReport",
        back_populates="candidate",
        cascade="all, delete-orphan",
    )
    invitations: Mapped[List["Invitation"]] = relationship(
        "Invitation",
        back_populates="candidate",
        cascade="all, delete-orphan",
    )
    job_screenings: Mapped[List["CandidateJobScreening"]] = relationship(
        "CandidateJobScreening",
        back_populates="candidate",
        cascade="all, delete-orphan",
    )

    def __repr__(self) -> str:
        return f"<Candidate(id={self.id}, name={self.full_name}, status={self.status})>"
