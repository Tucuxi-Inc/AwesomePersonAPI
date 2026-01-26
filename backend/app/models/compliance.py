"""Compliance and bias monitoring models."""

import uuid
from datetime import datetime
from enum import Enum
from typing import Optional, List

from sqlalchemy import ForeignKey, String, Text, Float, Integer, Boolean, DateTime
from sqlalchemy.dialects.postgresql import JSONB, ARRAY
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base, TimestampMixin, UUIDMixin


class ProtectedClass(str, Enum):
    """Protected demographic classes for disparate impact monitoring."""
    GENDER = "gender"
    RACE_ETHNICITY = "race_ethnicity"
    AGE_GROUP = "age_group"
    DISABILITY = "disability"
    VETERAN_STATUS = "veteran_status"


class ComplianceCheckType(str, Enum):
    """Types of compliance checks performed."""
    PROBE_VALIDATION = "probe_validation"
    RESPONSE_ANALYSIS = "response_analysis"
    EVIDENCE_FILTERING = "evidence_filtering"
    RUBRIC_VALIDATION = "rubric_validation"
    SCORE_CALIBRATION = "score_calibration"


class ComplianceSeverity(str, Enum):
    """Severity levels for compliance issues."""
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"


class AssessmentAuditRecord(Base, UUIDMixin, TimestampMixin):
    """
    Complete audit record for every assessment decision.
    Designed to answer: "Why did this candidate receive this score?"
    """

    __tablename__ = "assessment_audit_records"

    # What was assessed
    assessment_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("assessment_reports.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    candidate_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("candidates.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    interview_session_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("interview_sessions.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    role_profile_id: Mapped[Optional[uuid.UUID]] = mapped_column(
        ForeignKey("role_profiles.id", ondelete="SET NULL"),
        nullable=True,
    )
    rubric_id: Mapped[Optional[uuid.UUID]] = mapped_column(
        ForeignKey("scoring_rubrics.id", ondelete="SET NULL"),
        nullable=True,
    )
    rubric_version: Mapped[Optional[str]] = mapped_column(String(50), nullable=True)

    # Rubric derivation chain
    rubric_source: Mapped[Optional[str]] = mapped_column(String(50), nullable=True)
    # Values: RESEARCH_DEFAULT, ORGANIZATIONAL, ADJUSTED
    rubric_derivation_trace: Mapped[Optional[dict]] = mapped_column(JSONB, nullable=True)

    # For each trait - array of TraitAuditRecord objects
    trait_audit_records: Mapped[Optional[dict]] = mapped_column(JSONB, nullable=True)

    # Final decision
    composite_score: Mapped[Optional[float]] = mapped_column(Float, nullable=True)
    recommendation: Mapped[Optional[str]] = mapped_column(String(50), nullable=True)
    recommendation_explanation: Mapped[Optional[str]] = mapped_column(Text, nullable=True)

    # Compliance metadata
    protected_info_excluded: Mapped[Optional[dict]] = mapped_column(JSONB, nullable=True)
    # What was explicitly excluded from scoring
    compliance_checks_passed: Mapped[Optional[dict]] = mapped_column(JSONB, nullable=True)
    # Which validations ran and their results

    # Timestamps and actors
    assessed_at: Mapped[Optional[datetime]] = mapped_column(
        DateTime(timezone=True), nullable=True
    )
    assessed_by: Mapped[Optional[uuid.UUID]] = mapped_column(
        ForeignKey("users.id", ondelete="SET NULL"),
        nullable=True,
    )

    def __repr__(self) -> str:
        return f"<AssessmentAuditRecord(assessment={self.assessment_id}, candidate={self.candidate_id})>"


class ComplianceCheck(Base, UUIDMixin, TimestampMixin):
    """
    Record of individual compliance checks performed during assessment.
    """

    __tablename__ = "compliance_checks"

    # Context
    interview_session_id: Mapped[Optional[uuid.UUID]] = mapped_column(
        ForeignKey("interview_sessions.id", ondelete="CASCADE"),
        nullable=True,
        index=True,
    )
    exchange_id: Mapped[Optional[uuid.UUID]] = mapped_column(
        ForeignKey("exchanges.id", ondelete="CASCADE"),
        nullable=True,
        index=True,
    )
    organization_id: Mapped[Optional[uuid.UUID]] = mapped_column(
        ForeignKey("organizations.id", ondelete="CASCADE"),
        nullable=True,
        index=True,
    )

    # Check details
    check_type: Mapped[str] = mapped_column(String(50), nullable=False, index=True)
    passed: Mapped[bool] = mapped_column(Boolean, nullable=False, default=True)
    severity: Mapped[Optional[str]] = mapped_column(String(20), nullable=True)

    # What was checked
    checked_content: Mapped[Optional[str]] = mapped_column(Text, nullable=True)

    # Violations found
    violations: Mapped[Optional[dict]] = mapped_column(JSONB, nullable=True)
    # Format: [{"type": "...", "topic": "...", "severity": "...", "recommendation": "..."}]

    warnings: Mapped[Optional[dict]] = mapped_column(JSONB, nullable=True)
    # Similar format for non-blocking warnings

    # Actions taken
    action_taken: Mapped[Optional[str]] = mapped_column(String(100), nullable=True)
    # Examples: "BLOCKED", "EXCLUDED_FROM_SCORING", "ALLOWED_WITH_WARNING"

    def __repr__(self) -> str:
        return f"<ComplianceCheck(type={self.check_type}, passed={self.passed})>"


class DisparateImpactReport(Base, UUIDMixin, TimestampMixin):
    """
    Disparate impact analysis report for an organization.
    Required annually under NYC Local Law 144 and similar regulations.
    """

    __tablename__ = "disparate_impact_reports"

    organization_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("organizations.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )

    # Report period
    period_start: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), nullable=False
    )
    period_end: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), nullable=False
    )

    # Report metadata
    report_type: Mapped[str] = mapped_column(String(50), nullable=False, default="ANNUAL")
    # Values: ANNUAL, QUARTERLY, AD_HOC

    generated_by: Mapped[Optional[uuid.UUID]] = mapped_column(
        ForeignKey("users.id", ondelete="SET NULL"),
        nullable=True,
    )

    # Sample information
    total_assessments: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    assessments_with_demographics: Mapped[int] = mapped_column(Integer, nullable=False, default=0)

    # Impact ratios by protected class
    # Format: {
    #   "gender": {"ratios": [...], "has_disparate_impact": bool},
    #   "race_ethnicity": {"ratios": [...], "has_disparate_impact": bool},
    #   ...
    # }
    impact_analysis: Mapped[Optional[dict]] = mapped_column(JSONB, nullable=True)

    # Overall assessment
    has_disparate_impact: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)
    overall_assessment: Mapped[Optional[str]] = mapped_column(Text, nullable=True)

    # Recommendations
    recommendations: Mapped[Optional[dict]] = mapped_column(JSONB, nullable=True)
    # Format: ["Review trait weights...", "Consider alternative criteria..."]

    # Required actions (if any)
    required_actions: Mapped[Optional[dict]] = mapped_column(JSONB, nullable=True)

    # Report file storage
    report_file_path: Mapped[Optional[str]] = mapped_column(String(500), nullable=True)

    def __repr__(self) -> str:
        return f"<DisparateImpactReport(org={self.organization_id}, period={self.period_start}-{self.period_end})>"


class CandidateDemographics(Base, UUIDMixin, TimestampMixin):
    """
    Voluntary demographic data for disparate impact monitoring.

    IMPORTANT: This data is:
    - Separate from hiring decisions
    - Optional for candidates
    - Used only for monitoring, not scoring
    - Stored securely with access controls
    """

    __tablename__ = "candidate_demographics"

    candidate_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("candidates.id", ondelete="CASCADE"),
        nullable=False,
        unique=True,
        index=True,
    )

    # Voluntary self-identification
    gender: Mapped[Optional[str]] = mapped_column(String(50), nullable=True)
    # Values: male, female, non_binary, prefer_not_to_say

    race_ethnicity: Mapped[Optional[str]] = mapped_column(String(100), nullable=True)
    # Values: white, black_african_american, hispanic_latino, asian,
    #         native_american, pacific_islander, two_or_more, prefer_not_to_say

    age_group: Mapped[Optional[str]] = mapped_column(String(20), nullable=True)
    # Values: under_40, 40_plus, prefer_not_to_say

    disability_status: Mapped[Optional[str]] = mapped_column(String(50), nullable=True)
    # Values: yes, no, prefer_not_to_say

    veteran_status: Mapped[Optional[str]] = mapped_column(String(50), nullable=True)
    # Values: yes, no, prefer_not_to_say

    # Consent tracking
    consent_given: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)
    consent_given_at: Mapped[Optional[datetime]] = mapped_column(
        DateTime(timezone=True), nullable=True
    )
    consent_text_shown: Mapped[Optional[str]] = mapped_column(Text, nullable=True)

    def __repr__(self) -> str:
        return f"<CandidateDemographics(candidate={self.candidate_id})>"


class CandidateDisclosure(Base, UUIDMixin, TimestampMixin):
    """
    Record of disclosures shown to candidates about AI assessment.
    """

    __tablename__ = "candidate_disclosures"

    candidate_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("candidates.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    interview_session_id: Mapped[Optional[uuid.UUID]] = mapped_column(
        ForeignKey("interview_sessions.id", ondelete="SET NULL"),
        nullable=True,
        index=True,
    )
    organization_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("organizations.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )

    # Disclosure details
    disclosure_type: Mapped[str] = mapped_column(String(50), nullable=False)
    # Values: PRE_ASSESSMENT, POST_ASSESSMENT, RESULTS_AVAILABLE

    disclosure_version: Mapped[str] = mapped_column(String(20), nullable=False, default="1.0")
    disclosure_content: Mapped[str] = mapped_column(Text, nullable=False)
    jurisdiction: Mapped[Optional[str]] = mapped_column(String(50), nullable=True)
    # Examples: NYC, IL, CA, EU

    # Consent (if required)
    consent_required: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)
    consent_given: Mapped[Optional[bool]] = mapped_column(Boolean, nullable=True)
    consent_given_at: Mapped[Optional[datetime]] = mapped_column(
        DateTime(timezone=True), nullable=True
    )

    # Delivery tracking
    shown_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), nullable=False
    )
    acknowledged_at: Mapped[Optional[datetime]] = mapped_column(
        DateTime(timezone=True), nullable=True
    )

    def __repr__(self) -> str:
        return f"<CandidateDisclosure(candidate={self.candidate_id}, type={self.disclosure_type})>"


class RubricValidationRecord(Base, UUIDMixin, TimestampMixin):
    """
    Record of rubric validation checks for compliance.
    """

    __tablename__ = "rubric_validation_records"

    rubric_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("scoring_rubrics.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    organization_id: Mapped[Optional[uuid.UUID]] = mapped_column(
        ForeignKey("organizations.id", ondelete="SET NULL"),
        nullable=True,
        index=True,
    )
    validated_by: Mapped[Optional[uuid.UUID]] = mapped_column(
        ForeignKey("users.id", ondelete="SET NULL"),
        nullable=True,
    )

    # Validation results
    is_valid: Mapped[bool] = mapped_column(Boolean, nullable=False, default=True)

    # Issues found
    issues: Mapped[Optional[dict]] = mapped_column(JSONB, nullable=True)
    # Format: [{"type": "...", "severity": "...", "trait_id": "...", "description": "...", "recommendation": "..."}]

    # Warnings
    warnings: Mapped[Optional[dict]] = mapped_column(JSONB, nullable=True)

    # Sensitive trait analysis
    sensitive_trait_weight_ratio: Mapped[Optional[float]] = mapped_column(Float, nullable=True)
    # Ratio of weight on demographically sensitive traits

    # Job relatedness documentation status
    job_relatedness_documented: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)
    missing_documentation: Mapped[Optional[dict]] = mapped_column(JSONB, nullable=True)
    # Format: ["trait_id_1", "trait_id_2", ...]

    def __repr__(self) -> str:
        return f"<RubricValidationRecord(rubric={self.rubric_id}, valid={self.is_valid})>"
