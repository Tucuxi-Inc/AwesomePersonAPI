"""Compliance and bias monitoring schemas."""

from datetime import datetime
from typing import List, Optional, Dict, Any
from uuid import UUID

from pydantic import BaseModel, Field


# Enums as string literals for API
class ProtectedClassEnum:
    GENDER = "gender"
    RACE_ETHNICITY = "race_ethnicity"
    AGE_GROUP = "age_group"
    DISABILITY = "disability"
    VETERAN_STATUS = "veteran_status"


# ==================== Probe Validation ====================

class ProbeViolation(BaseModel):
    """Violation found in a probe."""
    type: str
    topic: str
    severity: str = "HIGH"
    recommendation: str


class ProbeWarning(BaseModel):
    """Warning for a probe."""
    type: str
    phrase: str
    severity: str = "MEDIUM"
    recommendation: str


class ProbeValidationResult(BaseModel):
    """Result of probe compliance validation."""
    is_valid: bool
    violations: List[ProbeViolation] = []
    warnings: List[ProbeWarning] = []
    probe_text: Optional[str] = None


# ==================== Response Analysis Validation ====================

class AnalysisIssue(BaseModel):
    """Issue found in response analysis."""
    type: str
    evidence_id: Optional[str] = None
    topic: str
    action: str
    rationale: str


class AnalysisValidationResult(BaseModel):
    """Result of response analysis compliance validation."""
    is_clean: bool
    issues: List[AnalysisIssue] = []
    actions_taken: List[str] = []


# ==================== Rubric Validation ====================

class RubricIssue(BaseModel):
    """Issue found in rubric configuration."""
    type: str
    severity: str
    trait_id: Optional[str] = None
    description: str
    recommendation: str


class RubricValidationResult(BaseModel):
    """Result of rubric compliance validation."""
    is_valid: bool
    issues: List[RubricIssue] = []
    recommendations: List[str] = []
    sensitive_trait_weight_ratio: Optional[float] = None
    validation_timestamp: datetime


class RubricValidationCreate(BaseModel):
    """Request to validate a rubric."""
    rubric_id: UUID
    role_profile_id: Optional[UUID] = None


# ==================== Disparate Impact ====================

class ImpactRatio(BaseModel):
    """Impact ratio for a protected class group."""
    protected_class: str
    group_a: str
    group_b: str
    group_a_selection_rate: float
    group_b_selection_rate: float
    impact_ratio: float
    passes_four_fifths: bool
    sample_size_adequate: bool
    group_a_sample_size: int = 0
    group_b_sample_size: int = 0


class ImpactReportSection(BaseModel):
    """Section of disparate impact report for one protected class."""
    protected_class: str
    impact_ratios: List[ImpactRatio]
    has_disparate_impact: bool
    failing_groups: List[ImpactRatio] = []
    sample_sizes: Dict[str, int] = {}
    recommendations: List[str] = []


class DisparateImpactReportResponse(BaseModel):
    """Full disparate impact report."""
    id: UUID
    organization_id: UUID
    period_start: datetime
    period_end: datetime
    report_type: str
    total_assessments: int
    assessments_with_demographics: int
    sections: List[ImpactReportSection] = []
    has_disparate_impact: bool
    overall_assessment: Optional[str] = None
    recommendations: List[str] = []
    required_actions: List[str] = []
    created_at: datetime

    class Config:
        from_attributes = True


class DisparateImpactReportCreate(BaseModel):
    """Request to generate a disparate impact report."""
    organization_id: UUID
    period_start: datetime
    period_end: datetime
    report_type: str = "ANNUAL"


class ImpactDashboardAlert(BaseModel):
    """Alert for disparate impact dashboard."""
    protected_class: str
    group: str
    current_ratio: float
    threshold: float = 0.8
    severity: str


class ImpactDashboardResponse(BaseModel):
    """Disparate impact monitoring dashboard."""
    current_ratios: List[ImpactRatio]
    trends: List[Dict[str, Any]] = []
    alerts: List[ImpactDashboardAlert] = []
    last_full_audit: Optional[datetime] = None
    next_audit_due: Optional[datetime] = None


# ==================== Candidate Demographics ====================

class CandidateDemographicsCreate(BaseModel):
    """Create or update candidate demographics."""
    candidate_id: UUID
    gender: Optional[str] = Field(None, description="male, female, non_binary, prefer_not_to_say")
    race_ethnicity: Optional[str] = Field(
        None,
        description="white, black_african_american, hispanic_latino, asian, native_american, pacific_islander, two_or_more, prefer_not_to_say"
    )
    age_group: Optional[str] = Field(None, description="under_40, 40_plus, prefer_not_to_say")
    disability_status: Optional[str] = Field(None, description="yes, no, prefer_not_to_say")
    veteran_status: Optional[str] = Field(None, description="yes, no, prefer_not_to_say")
    consent_given: bool = False


class CandidateDemographicsResponse(BaseModel):
    """Candidate demographics response."""
    id: UUID
    candidate_id: UUID
    gender: Optional[str] = None
    race_ethnicity: Optional[str] = None
    age_group: Optional[str] = None
    disability_status: Optional[str] = None
    veteran_status: Optional[str] = None
    consent_given: bool
    consent_given_at: Optional[datetime] = None
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


# ==================== Candidate Disclosure ====================

class DisclosureSection(BaseModel):
    """Section of a disclosure document."""
    heading: str
    content: str


class CandidateDisclosureContent(BaseModel):
    """Full disclosure content."""
    title: str
    sections: List[DisclosureSection]
    consent_required: bool
    consent_text: Optional[str] = None
    jurisdiction: Optional[str] = None


class CandidateDisclosureCreate(BaseModel):
    """Record a disclosure shown to a candidate."""
    candidate_id: UUID
    interview_session_id: Optional[UUID] = None
    disclosure_type: str = Field(..., description="PRE_ASSESSMENT, POST_ASSESSMENT, RESULTS_AVAILABLE")
    disclosure_content: str
    jurisdiction: Optional[str] = None
    consent_required: bool = False
    consent_given: Optional[bool] = None


class CandidateDisclosureResponse(BaseModel):
    """Recorded disclosure response."""
    id: UUID
    candidate_id: UUID
    interview_session_id: Optional[UUID] = None
    organization_id: UUID
    disclosure_type: str
    disclosure_version: str
    jurisdiction: Optional[str] = None
    consent_required: bool
    consent_given: Optional[bool] = None
    consent_given_at: Optional[datetime] = None
    shown_at: datetime
    acknowledged_at: Optional[datetime] = None
    created_at: datetime

    class Config:
        from_attributes = True


class DisclosureAcknowledgement(BaseModel):
    """Acknowledgement of a disclosure."""
    disclosure_id: UUID
    consent_given: Optional[bool] = None


# ==================== Assessment Audit ====================

class EvidenceAuditRecord(BaseModel):
    """Audit record for a single piece of evidence."""
    evidence_id: str
    source_type: str
    source_exchange_id: Optional[str] = None
    source_text: str
    classification_rationale: str
    weight_applied: float
    weight_rationale: str
    protected_info_detected: bool = False
    protected_info_excluded: bool = False
    exclusion_rationale: Optional[str] = None


class TraitAuditRecord(BaseModel):
    """Audit record for a single trait assessment."""
    trait_id: str
    trait_name: Optional[str] = None
    raw_score: Optional[int] = None
    calibrated_score: Optional[int] = None
    confidence: float
    evidence_items: List[EvidenceAuditRecord] = []
    matched_behavioral_anchors: List[str] = []
    scoring_criteria_applied: Optional[str] = None
    score_explanation: str
    rubric_item_id: Optional[str] = None
    rubric_item_source: Optional[str] = None
    job_relatedness_rationale: Optional[str] = None
    research_citations: Optional[List[str]] = None
    extraction_session_ids: Optional[List[str]] = None


class AssessmentAuditRecordResponse(BaseModel):
    """Full assessment audit record."""
    id: UUID
    assessment_id: UUID
    candidate_id: UUID
    interview_session_id: UUID
    role_profile_id: Optional[UUID] = None
    rubric_id: Optional[UUID] = None
    rubric_version: Optional[str] = None
    rubric_source: Optional[str] = None
    rubric_derivation_trace: Optional[Dict[str, Any]] = None
    trait_audit_records: List[TraitAuditRecord] = []
    composite_score: Optional[float] = None
    recommendation: Optional[str] = None
    recommendation_explanation: Optional[str] = None
    protected_info_excluded: Optional[Dict[str, Any]] = None
    compliance_checks_passed: Optional[Dict[str, Any]] = None
    assessed_at: Optional[datetime] = None
    assessed_by: Optional[UUID] = None
    created_at: datetime

    class Config:
        from_attributes = True


# ==================== Compliance Status ====================

class ComplianceStatusResponse(BaseModel):
    """Organization compliance status."""
    organization_id: UUID
    is_compliant: bool
    missing_documentation: List[str] = []
    warnings: List[str] = []
    last_audit_date: Optional[datetime] = None
    next_audit_due: Optional[datetime] = None
    rubric_validation_issues: int = 0
    pending_disclosures: int = 0


# ==================== Configuration Warnings ====================

class ConfigurationWarning(BaseModel):
    """Warning about a potentially problematic configuration."""
    severity: str
    trait_id: Optional[str] = None
    message: str
    action_required: bool = False
    documentation_recommended: bool = False
    link_to_documentation: Optional[str] = None


class ConfigurationValidationResult(BaseModel):
    """Result of configuration validation."""
    warnings: List[ConfigurationWarning] = []
    is_recommended: bool = True
