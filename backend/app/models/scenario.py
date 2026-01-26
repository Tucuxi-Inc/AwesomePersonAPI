"""Interview scenario model."""

import uuid
from typing import Optional, List

from sqlalchemy import ForeignKey, String, Text, Boolean, Integer
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import Mapped, mapped_column

from app.db.base import Base, TimestampMixin, UUIDMixin


class Scenario(Base, UUIDMixin, TimestampMixin):
    """Interview scenario/case study template."""

    __tablename__ = "scenarios"

    name: Mapped[str] = mapped_column(String(255), nullable=False)
    description: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    category: Mapped[str] = mapped_column(String(100), nullable=False, index=True)

    # Scenario content
    context: Mapped[str] = mapped_column(Text, nullable=False)
    prompt: Mapped[str] = mapped_column(Text, nullable=False)
    expected_elements: Mapped[List[dict]] = mapped_column(JSONB, nullable=False, default=list)
    # Format: [{"element": "...", "weight": 1.0, "trait_signals": ["trait_id1", ...]}, ...]

    # Traits assessed by this scenario
    target_traits: Mapped[List[str]] = mapped_column(JSONB, nullable=False, default=list)

    # Difficulty and timing
    difficulty_level: Mapped[int] = mapped_column(Integer, default=3, nullable=False)  # 1-5
    estimated_duration_minutes: Mapped[int] = mapped_column(Integer, default=15, nullable=False)

    # Role applicability
    applicable_role_categories: Mapped[List[str]] = mapped_column(JSONB, nullable=False, default=list)

    # Status
    is_active: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)

    def __repr__(self) -> str:
        return f"<Scenario(id={self.id}, name={self.name})>"
