"""Invitation model for self-service access."""

import enum
import secrets
import uuid
from datetime import datetime, timedelta
from typing import TYPE_CHECKING, Optional

from sqlalchemy import ForeignKey, String, Text, Boolean, DateTime, Enum
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base, TimestampMixin, UUIDMixin

if TYPE_CHECKING:
    from app.models.candidate import Candidate
    from app.models.top_performer import TopPerformer
    from app.models.organization import Organization


class InvitationType(str, enum.Enum):
    """Type of invitation."""
    CANDIDATE_INTERVIEW = "CANDIDATE_INTERVIEW"
    TOP_PERFORMER_PROFILING = "TOP_PERFORMER_PROFILING"


class InvitationStatus(str, enum.Enum):
    """Status of an invitation."""
    PENDING = "PENDING"  # Sent but not yet accessed
    VIEWED = "VIEWED"  # Recipient opened the link
    IN_PROGRESS = "IN_PROGRESS"  # Session started
    COMPLETED = "COMPLETED"  # Session finished
    EXPIRED = "EXPIRED"  # Past expiration date
    REVOKED = "REVOKED"  # Manually cancelled


def generate_invitation_token() -> str:
    """Generate a secure random token for invitations."""
    return secrets.token_urlsafe(32)


class Invitation(Base, UUIDMixin, TimestampMixin):
    """Invitation for self-service access to interviews or profiling sessions."""

    __tablename__ = "invitations"

    organization_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("organizations.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )

    # Invitation details
    invitation_type: Mapped[InvitationType] = mapped_column(
        Enum(InvitationType), nullable=False, index=True
    )
    token: Mapped[str] = mapped_column(
        String(64), nullable=False, unique=True, index=True,
        default=generate_invitation_token
    )
    status: Mapped[InvitationStatus] = mapped_column(
        Enum(InvitationStatus), nullable=False, default=InvitationStatus.PENDING
    )

    # Target references (one of these will be set based on type)
    candidate_id: Mapped[Optional[uuid.UUID]] = mapped_column(
        ForeignKey("candidates.id", ondelete="CASCADE"),
        nullable=True,
        index=True,
    )
    top_performer_id: Mapped[Optional[uuid.UUID]] = mapped_column(
        ForeignKey("top_performers.id", ondelete="CASCADE"),
        nullable=True,
        index=True,
    )

    # Session reference (set when session starts)
    interview_session_id: Mapped[Optional[uuid.UUID]] = mapped_column(
        ForeignKey("interview_sessions.id", ondelete="SET NULL"),
        nullable=True,
    )
    training_session_id: Mapped[Optional[uuid.UUID]] = mapped_column(
        ForeignKey("training_sessions.id", ondelete="SET NULL"),
        nullable=True,
    )

    # Recipient info
    recipient_email: Mapped[str] = mapped_column(String(255), nullable=False)
    recipient_name: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)

    # Configuration
    trait_ids: Mapped[Optional[list]] = mapped_column(
        JSONB,
        nullable=True,
        default=list,
    )  # Which traits to assess
    role_profile_id: Mapped[Optional[uuid.UUID]] = mapped_column(
        ForeignKey("role_profiles.id", ondelete="SET NULL"),
        nullable=True,
    )

    # Expiration
    expires_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), nullable=False
    )

    # Tracking
    sent_at: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True), nullable=True)
    viewed_at: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True), nullable=True)
    started_at: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True), nullable=True)
    completed_at: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True), nullable=True)

    # Invitation message
    custom_message: Mapped[Optional[str]] = mapped_column(Text, nullable=True)

    # Created by
    created_by_id: Mapped[Optional[uuid.UUID]] = mapped_column(
        ForeignKey("users.id", ondelete="SET NULL"),
        nullable=True,
    )

    # Relationships
    organization: Mapped["Organization"] = relationship("Organization")
    candidate: Mapped[Optional["Candidate"]] = relationship("Candidate", back_populates="invitations")
    top_performer: Mapped[Optional["TopPerformer"]] = relationship("TopPerformer", back_populates="invitations")

    @property
    def is_expired(self) -> bool:
        """Check if invitation has expired."""
        return datetime.utcnow() > self.expires_at.replace(tzinfo=None)

    @property
    def is_valid(self) -> bool:
        """Check if invitation can still be used."""
        return (
            self.status in (InvitationStatus.PENDING, InvitationStatus.VIEWED) and
            not self.is_expired
        )

    @classmethod
    def create_for_candidate(
        cls,
        organization_id: uuid.UUID,
        candidate_id: uuid.UUID,
        recipient_email: str,
        recipient_name: Optional[str] = None,
        trait_ids: Optional[list] = None,
        role_profile_id: Optional[uuid.UUID] = None,
        expires_in_days: int = 7,
        custom_message: Optional[str] = None,
        created_by_id: Optional[uuid.UUID] = None,
    ) -> "Invitation":
        """Create an invitation for a candidate interview."""
        return cls(
            organization_id=organization_id,
            invitation_type=InvitationType.CANDIDATE_INTERVIEW,
            candidate_id=candidate_id,
            recipient_email=recipient_email,
            recipient_name=recipient_name,
            trait_ids=trait_ids or [],
            role_profile_id=role_profile_id,
            expires_at=datetime.utcnow() + timedelta(days=expires_in_days),
            custom_message=custom_message,
            created_by_id=created_by_id,
        )

    @classmethod
    def create_for_top_performer(
        cls,
        organization_id: uuid.UUID,
        top_performer_id: uuid.UUID,
        recipient_email: str,
        recipient_name: Optional[str] = None,
        trait_ids: Optional[list] = None,
        expires_in_days: int = 14,
        custom_message: Optional[str] = None,
        created_by_id: Optional[uuid.UUID] = None,
    ) -> "Invitation":
        """Create an invitation for a top performer profiling session."""
        return cls(
            organization_id=organization_id,
            invitation_type=InvitationType.TOP_PERFORMER_PROFILING,
            top_performer_id=top_performer_id,
            recipient_email=recipient_email,
            recipient_name=recipient_name,
            trait_ids=trait_ids or [],
            expires_at=datetime.utcnow() + timedelta(days=expires_in_days),
            custom_message=custom_message,
            created_by_id=created_by_id,
        )

    def __repr__(self) -> str:
        return f"<Invitation(id={self.id}, type={self.invitation_type}, status={self.status})>"
