"""Resume model."""

import enum
import uuid
from typing import TYPE_CHECKING, Optional

from sqlalchemy import ForeignKey, String, Text, Integer
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base, TimestampMixin, UUIDMixin

if TYPE_CHECKING:
    from app.models.candidate import Candidate


class ResumeParseStatus(str, enum.Enum):
    """Resume parsing status."""

    PENDING = "PENDING"
    PARSING = "PARSING"
    PARSED = "PARSED"
    FAILED = "FAILED"


class Resume(Base, UUIDMixin, TimestampMixin):
    """Candidate resume/CV."""

    __tablename__ = "resumes"

    candidate_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("candidates.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )

    # File information
    filename: Mapped[str] = mapped_column(String(255), nullable=False)
    file_type: Mapped[str] = mapped_column(String(50), nullable=False)  # e.g., "pdf", "docx"
    file_size_bytes: Mapped[int] = mapped_column(Integer, nullable=False)
    file_path: Mapped[str] = mapped_column(String(500), nullable=False)

    # Parsing status
    parse_status: Mapped[ResumeParseStatus] = mapped_column(
        default=ResumeParseStatus.PENDING,
        nullable=False,
    )
    parse_error: Mapped[Optional[str]] = mapped_column(Text, nullable=True)

    # Extracted content
    raw_text: Mapped[Optional[str]] = mapped_column(Text, nullable=True)

    # Parsed/structured data
    parsed_data: Mapped[Optional[dict]] = mapped_column(JSONB, nullable=True)
    # Format: {
    #   "contact": {...},
    #   "summary": "...",
    #   "experience": [{...}],
    #   "education": [{...}],
    #   "skills": [...],
    #   ...
    # }

    # AI analysis
    ai_analysis: Mapped[Optional[dict]] = mapped_column(JSONB, nullable=True)
    # Format: {
    #   "trait_signals": [...],
    #   "experience_summary": "...",
    #   "strengths": [...],
    #   "gaps": [...],
    #   ...
    # }

    # Version tracking
    version: Mapped[int] = mapped_column(Integer, default=1, nullable=False)
    is_primary: Mapped[bool] = mapped_column(default=True, nullable=False)

    # Relationships
    candidate: Mapped["Candidate"] = relationship("Candidate", back_populates="resumes")

    def __repr__(self) -> str:
        return f"<Resume(id={self.id}, candidate_id={self.candidate_id}, filename={self.filename})>"
