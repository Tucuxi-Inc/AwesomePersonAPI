"""Trait and trait valence models."""

import uuid
from enum import Enum
from typing import TYPE_CHECKING, List, Optional

from sqlalchemy import ForeignKey, String, Text, Integer
from sqlalchemy.dialects.postgresql import JSONB, ARRAY
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base, TimestampMixin, UUIDMixin


class TraitCategory(str, Enum):
    """Categories for personality traits."""

    COGNITIVE = "COGNITIVE"
    INTERPERSONAL = "INTERPERSONAL"
    EXECUTION = "EXECUTION"
    STABILITY = "STABILITY"
    SELF_MANAGEMENT = "SELF_MANAGEMENT"
    ORIENTATION = "ORIENTATION"


class Valence(str, Enum):
    """Valence values for trait-role mappings."""

    HIGH_POSITIVE = "HIGH_POSITIVE"
    POSITIVE = "POSITIVE"
    MODERATE = "MODERATE"
    LOWER = "LOWER"
    NEUTRAL = "NEUTRAL"
    CONTEXT_DEPENDENT = "CONTEXT_DEPENDENT"
    NEGATIVE = "NEGATIVE"
    HIGH_NEGATIVE = "HIGH_NEGATIVE"


class Trait(Base, UUIDMixin, TimestampMixin):
    """Personality trait definition from the 24-trait taxonomy."""

    __tablename__ = "traits"

    name: Mapped[str] = mapped_column(String(100), unique=True, nullable=False, index=True)
    category: Mapped[str] = mapped_column(String(50), nullable=False, index=True)
    definition: Mapped[str] = mapped_column(Text, nullable=False)

    # Spectrum definition
    spectrum_low_label: Mapped[str] = mapped_column(String(100), nullable=False)
    spectrum_high_label: Mapped[str] = mapped_column(String(100), nullable=False)

    # Behavioral markers (stored as JSON arrays)
    behavioral_markers_low: Mapped[List[str]] = mapped_column(JSONB, nullable=False, default=list)
    behavioral_markers_high: Mapped[List[str]] = mapped_column(JSONB, nullable=False, default=list)

    # Counter-indicator roles (where HIGH trait is negative)
    counter_indicator_for: Mapped[List[str]] = mapped_column(JSONB, nullable=False, default=list)

    # Research foundation
    research_foundation: Mapped[Optional[dict]] = mapped_column(JSONB, nullable=True)

    # Display order within category
    display_order: Mapped[int] = mapped_column(Integer, default=0, nullable=False)

    # Relationships
    valence_mappings: Mapped[List["TraitValenceMapping"]] = relationship(
        "TraitValenceMapping",
        back_populates="trait",
        cascade="all, delete-orphan",
    )

    def __repr__(self) -> str:
        return f"<Trait(id={self.id}, name={self.name}, category={self.category})>"


class TraitValenceMapping(Base, UUIDMixin, TimestampMixin):
    """Maps trait valence to specific role categories."""

    __tablename__ = "trait_valence_mappings"

    trait_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("traits.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    role_category: Mapped[str] = mapped_column(String(100), nullable=False, index=True)
    valence: Mapped[str] = mapped_column(String(50), nullable=False)
    optimal_range_min: Mapped[int] = mapped_column(Integer, default=1, nullable=False)
    optimal_range_max: Mapped[int] = mapped_column(Integer, default=5, nullable=False)
    rationale: Mapped[str] = mapped_column(Text, nullable=False)
    notes: Mapped[Optional[str]] = mapped_column(Text, nullable=True)

    # Relationships
    trait: Mapped["Trait"] = relationship("Trait", back_populates="valence_mappings")

    def __repr__(self) -> str:
        return f"<TraitValenceMapping(trait_id={self.trait_id}, role={self.role_category}, valence={self.valence})>"
