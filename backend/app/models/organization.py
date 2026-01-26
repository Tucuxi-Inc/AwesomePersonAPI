"""Organization model."""

import uuid
from typing import TYPE_CHECKING, List, Optional

from sqlalchemy import String, Text, Boolean
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base, TimestampMixin, UUIDMixin

if TYPE_CHECKING:
    from app.models.user import User
    from app.models.role_profile import RoleProfile
    from app.models.rubric import ScoringRubric
    from app.models.candidate import Candidate
    from app.models.top_performer import TopPerformer
    from app.models.job import Job


class Organization(Base, UUIDMixin, TimestampMixin):
    """Organization/tenant in the multi-tenant system."""

    __tablename__ = "organizations"

    name: Mapped[str] = mapped_column(String(255), nullable=False)
    slug: Mapped[str] = mapped_column(String(100), unique=True, nullable=False, index=True)
    description: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    website: Mapped[Optional[str]] = mapped_column(String(500), nullable=True)
    industry: Mapped[Optional[str]] = mapped_column(String(100), nullable=True)
    size: Mapped[Optional[str]] = mapped_column(String(50), nullable=True)  # e.g., "1-10", "11-50", etc.
    is_active: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)
    settings: Mapped[Optional[dict]] = mapped_column(JSONB, nullable=True, default=dict)

    # Relationships
    users: Mapped[List["User"]] = relationship("User", back_populates="organization")
    role_profiles: Mapped[List["RoleProfile"]] = relationship("RoleProfile", back_populates="organization")
    rubrics: Mapped[List["ScoringRubric"]] = relationship("ScoringRubric", back_populates="organization")
    candidates: Mapped[List["Candidate"]] = relationship("Candidate", back_populates="organization")
    top_performers: Mapped[List["TopPerformer"]] = relationship("TopPerformer", back_populates="organization")
    jobs: Mapped[List["Job"]] = relationship("Job", back_populates="organization")

    def __repr__(self) -> str:
        return f"<Organization(id={self.id}, name={self.name})>"
