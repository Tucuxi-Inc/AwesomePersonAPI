"""Evidence item model for extracted behavioral evidence."""

import uuid
from enum import Enum
from typing import TYPE_CHECKING, List, Optional

from sqlalchemy import ForeignKey, String, Text, Float
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base, TimestampMixin, UUIDMixin

if TYPE_CHECKING:
    from app.models.interview_session import InterviewSession
    from app.models.trait import Trait


class EvidenceType(str, Enum):
    """Type of evidence based on source."""
    OBSERVED = "OBSERVED"        # Demonstrated during interview (weight: 1.2)
    BEHAVIORAL = "BEHAVIORAL"    # Specific past action with details (weight: 1.0)
    HYPOTHETICAL = "HYPOTHETICAL"  # What they would do (weight: 0.5)
    SELF_REPORT = "SELF_REPORT"  # Claims about themselves (weight: 0.3)
    OPINION = "OPINION"          # Beliefs, values (weight: 0.2)


# Evidence weights for scoring
EVIDENCE_TYPE_WEIGHTS = {
    EvidenceType.OBSERVED: 1.2,
    EvidenceType.BEHAVIORAL: 1.0,
    EvidenceType.HYPOTHETICAL: 0.5,
    EvidenceType.SELF_REPORT: 0.3,
    EvidenceType.OPINION: 0.2,
}


class EvidenceItem(Base, UUIDMixin, TimestampMixin):
    """Extracted behavioral evidence from interview responses."""

    __tablename__ = "evidence_items"

    session_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("interview_sessions.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    exchange_id: Mapped[Optional[uuid.UUID]] = mapped_column(
        ForeignKey("exchanges.id", ondelete="SET NULL"),
        nullable=True,
        index=True,
    )
    trait_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("traits.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )

    # Evidence content
    source_type: Mapped[str] = mapped_column(String(20), nullable=False)
    source_text: Mapped[str] = mapped_column(Text, nullable=False)
    # The actual quote or paraphrase from the candidate

    # Classification
    weight: Mapped[float] = mapped_column(Float, nullable=False)
    # Calculated from source_type

    # Trait signals
    trait_signals: Mapped[List[dict]] = mapped_column(JSONB, nullable=False, default=list)
    # Format: [
    #   {"trait_id": "...", "signal": "positive|negative|neutral", "strength": 0.8}
    # ]

    # STAR+ component coverage
    star_components: Mapped[dict] = mapped_column(JSONB, nullable=False, default=dict)
    # Format: {
    #   "situation": true,
    #   "task": true,
    #   "action": true,
    #   "result": false,
    #   "reflection": false
    # }

    # Confidence and quality
    confidence: Mapped[float] = mapped_column(Float, nullable=False, default=0.5)
    # 0.0-1.0 confidence in evidence quality

    specificity_score: Mapped[float] = mapped_column(Float, nullable=False, default=0.5)
    # How specific/detailed the evidence is (0.0-1.0)

    # Behavioral anchor matching
    matched_anchors: Mapped[List[str]] = mapped_column(JSONB, nullable=False, default=list)
    # Format: ["Score 4: Clear examples of learning within professional domain"]

    # Analysis notes
    extraction_rationale: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    # Why this was classified this way

    # Conflict/tension indicators
    contains_conflict: Mapped[bool] = mapped_column(default=False, nullable=False)
    contains_failure: Mapped[bool] = mapped_column(default=False, nullable=False)
    contains_challenge: Mapped[bool] = mapped_column(default=False, nullable=False)

    # Relationships
    session: Mapped["InterviewSession"] = relationship(
        "InterviewSession",
        back_populates="evidence_items"
    )
    trait: Mapped["Trait"] = relationship("Trait")

    @property
    def is_high_quality(self) -> bool:
        """Check if this is high-quality evidence."""
        return (
            self.source_type in (EvidenceType.OBSERVED.value, EvidenceType.BEHAVIORAL.value)
            and self.confidence >= 0.7
            and self.specificity_score >= 0.6
        )

    @property
    def star_completeness(self) -> float:
        """Calculate STAR completeness percentage."""
        components = ['situation', 'task', 'action', 'result']
        present = sum(1 for c in components if self.star_components.get(c, False))
        return present / len(components)

    def __repr__(self) -> str:
        return f"<EvidenceItem(id={self.id}, type={self.source_type}, trait_id={self.trait_id})>"
