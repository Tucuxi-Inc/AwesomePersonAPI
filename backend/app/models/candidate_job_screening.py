"""Candidate Job Screening model."""

import enum
import uuid
from datetime import datetime
from typing import TYPE_CHECKING, List, Optional

from sqlalchemy import DateTime, ForeignKey, String, Text, Integer, Boolean
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base, TimestampMixin, UUIDMixin

if TYPE_CHECKING:
    from app.models.candidate import Candidate
    from app.models.job import Job
    from app.models.resume import Resume
    from app.models.user import User


class QualificationStatus(str, enum.Enum):
    """Qualification screening status."""

    PENDING = "PENDING"
    QUALIFIED = "QUALIFIED"
    NOT_QUALIFIED = "NOT_QUALIFIED"
    NEEDS_REVIEW = "NEEDS_REVIEW"


class RequirementStatus(str, enum.Enum):
    """Individual requirement match status."""

    MET = "MET"
    NOT_MET = "NOT_MET"
    UNCLEAR = "UNCLEAR"


class CandidateJobScreening(Base, UUIDMixin, TimestampMixin):
    """Tracks candidate qualification screening against job requirements."""

    __tablename__ = "candidate_job_screenings"

    candidate_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("candidates.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    job_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("jobs.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    resume_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("resumes.id", ondelete="CASCADE"),
        nullable=False,
    )

    # Overall qualification status
    qualification_status: Mapped[QualificationStatus] = mapped_column(
        default=QualificationStatus.PENDING,
        nullable=False,
        index=True,
    )

    # Detailed requirement-by-requirement results
    # Format: [{"requirement_id": "...", "requirement_text": "...", "status": "MET/NOT_MET/UNCLEAR",
    #           "evidence": "Resume evidence...", "explanation": "Why this status..."}]
    requirement_results: Mapped[List[dict]] = mapped_column(JSONB, nullable=False, default=list)

    # Gaps for NOT_QUALIFIED candidates
    # Format: [{"requirement": "...", "explanation": "Why not met"}]
    gaps: Mapped[List[dict]] = mapped_column(JSONB, nullable=False, default=list)

    # Gap count for sorting (candidates with fewer gaps are closer to qualifying)
    gap_count: Mapped[int] = mapped_column(Integer, default=0, nullable=False, index=True)

    # Admin override capability
    admin_override: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
    override_by_id: Mapped[Optional[uuid.UUID]] = mapped_column(
        ForeignKey("users.id", ondelete="SET NULL"),
        nullable=True,
    )
    override_reason: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    override_at: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True), nullable=True)

    # Screening metadata
    screened_at: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True), nullable=True)
    screening_notes: Mapped[Optional[str]] = mapped_column(Text, nullable=True)

    # Relationships
    candidate: Mapped["Candidate"] = relationship("Candidate", back_populates="job_screenings")
    job: Mapped["Job"] = relationship("Job", back_populates="candidate_screenings")
    resume: Mapped["Resume"] = relationship("Resume")
    override_by: Mapped[Optional["User"]] = relationship("User")

    def __repr__(self) -> str:
        return f"<CandidateJobScreening(candidate={self.candidate_id}, job={self.job_id}, status={self.qualification_status})>"
