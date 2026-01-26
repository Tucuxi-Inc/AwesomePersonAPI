"""Audit log model."""

import uuid
from typing import Optional

from sqlalchemy import ForeignKey, String, Text
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import Mapped, mapped_column

from app.db.base import Base, TimestampMixin, UUIDMixin


class AuditLog(Base, UUIDMixin, TimestampMixin):
    """Audit trail for system actions."""

    __tablename__ = "audit_logs"

    # Actor
    user_id: Mapped[Optional[uuid.UUID]] = mapped_column(
        ForeignKey("users.id", ondelete="SET NULL"),
        nullable=True,
        index=True,
    )
    organization_id: Mapped[Optional[uuid.UUID]] = mapped_column(
        ForeignKey("organizations.id", ondelete="SET NULL"),
        nullable=True,
        index=True,
    )

    # Action
    action: Mapped[str] = mapped_column(String(100), nullable=False, index=True)
    # Examples: "CREATE", "UPDATE", "DELETE", "LOGIN", "EXPORT", "GENERATE_REPORT"

    # Target resource
    resource_type: Mapped[str] = mapped_column(String(100), nullable=False, index=True)
    # Examples: "candidate", "interview_session", "assessment_report", "user"

    resource_id: Mapped[Optional[uuid.UUID]] = mapped_column(nullable=True, index=True)

    # Details
    description: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    changes: Mapped[Optional[dict]] = mapped_column(JSONB, nullable=True)
    # Format: {"field": {"old": ..., "new": ...}, ...}

    extra_data: Mapped[Optional[dict]] = mapped_column(JSONB, nullable=True)
    # Additional context like IP address, user agent, etc.

    # Request context
    ip_address: Mapped[Optional[str]] = mapped_column(String(50), nullable=True)
    user_agent: Mapped[Optional[str]] = mapped_column(String(500), nullable=True)

    def __repr__(self) -> str:
        return f"<AuditLog(id={self.id}, action={self.action}, resource={self.resource_type}:{self.resource_id})>"
