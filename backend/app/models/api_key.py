"""API Key model for Simple Mode authentication."""

import enum
import uuid
from datetime import datetime
from typing import TYPE_CHECKING, Optional

from sqlalchemy import ForeignKey, String, Boolean, DateTime, Integer
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base, TimestampMixin, UUIDMixin

if TYPE_CHECKING:
    from app.models.organization import Organization
    from app.models.user import User


class APIKeyTier(str, enum.Enum):
    """API key tier for rate limiting."""
    FREE = "FREE"
    BASIC = "BASIC"
    PRO = "PRO"
    ENTERPRISE = "ENTERPRISE"


# Rate limits by tier
TIER_LIMITS = {
    APIKeyTier.FREE: {
        "assessments_per_month": 5,
        "candidates_per_assessment": 10,
        "api_calls_per_minute": 10,
        "api_calls_per_day": 100,
    },
    APIKeyTier.BASIC: {
        "assessments_per_month": 50,
        "candidates_per_assessment": 50,
        "api_calls_per_minute": 60,
        "api_calls_per_day": 1000,
    },
    APIKeyTier.PRO: {
        "assessments_per_month": 500,
        "candidates_per_assessment": 200,
        "api_calls_per_minute": 300,
        "api_calls_per_day": 10000,
    },
    APIKeyTier.ENTERPRISE: {
        "assessments_per_month": -1,  # Unlimited
        "candidates_per_assessment": -1,
        "api_calls_per_minute": 1000,
        "api_calls_per_day": -1,
    },
}


class APIKey(Base, UUIDMixin, TimestampMixin):
    """
    API Key for Simple Mode authentication.

    Supports tiered rate limiting and usage tracking.
    Keys are stored as bcrypt hashes - full key only shown once on creation.
    """

    __tablename__ = "api_keys"

    organization_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("organizations.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    created_by_id: Mapped[Optional[uuid.UUID]] = mapped_column(
        ForeignKey("users.id", ondelete="SET NULL"),
        nullable=True,
    )

    # Key identification
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    key_prefix: Mapped[str] = mapped_column(String(12), nullable=False)
    # First 8 chars of the key for identification (e.g., "sk_live_Ab")
    key_hash: Mapped[str] = mapped_column(String(255), nullable=False)
    # bcrypt hash of the full key

    # Tier and limits
    tier: Mapped[APIKeyTier] = mapped_column(
        default=APIKeyTier.FREE,
        nullable=False,
    )

    # Status
    is_active: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)
    expires_at: Mapped[Optional[datetime]] = mapped_column(
        DateTime(timezone=True), nullable=True
    )

    # Usage tracking
    last_used_at: Mapped[Optional[datetime]] = mapped_column(
        DateTime(timezone=True), nullable=True
    )
    total_requests: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    requests_this_month: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    assessments_this_month: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    last_reset_at: Mapped[Optional[datetime]] = mapped_column(
        DateTime(timezone=True), nullable=True
    )

    # Relationships
    organization: Mapped["Organization"] = relationship("Organization")
    created_by: Mapped[Optional["User"]] = relationship("User")

    @property
    def limits(self) -> dict:
        """Get rate limits for this key's tier."""
        return TIER_LIMITS.get(self.tier, TIER_LIMITS[APIKeyTier.FREE])

    @property
    def is_expired(self) -> bool:
        """Check if the key has expired."""
        if self.expires_at is None:
            return False
        return datetime.now(self.expires_at.tzinfo) > self.expires_at

    @property
    def is_valid(self) -> bool:
        """Check if the key is active and not expired."""
        return self.is_active and not self.is_expired

    def __repr__(self) -> str:
        return f"<APIKey(id={self.id}, prefix={self.key_prefix}, tier={self.tier})>"
