"""Profile development schemas for top performer profiling and rubric generation."""

from datetime import datetime
from typing import Any, Dict, List, Optional
from uuid import UUID

from pydantic import BaseModel, Field


# Top Performer Schemas


class TopPerformerBase(BaseModel):
    """Base top performer schema."""
    name: Optional[str] = Field(None, max_length=255)
    employee_id: Optional[str] = Field(None, max_length=100)
    email: Optional[str] = Field(None, max_length=255)
    job_title: str = Field(..., min_length=1, max_length=255)
    department: Optional[str] = Field(None, max_length=100)
    role_category: str = Field(..., min_length=1, max_length=100)
    tenure_months: Optional[int] = Field(None, ge=0)
    performance_metrics: Optional[Dict[str, Any]] = None
    notes: Optional[str] = None


class TopPerformerCreate(TopPerformerBase):
    """Schema for creating a top performer."""
    is_anonymized: bool = False


class TopPerformerUpdate(BaseModel):
    """Schema for updating a top performer."""
    name: Optional[str] = Field(None, max_length=255)
    employee_id: Optional[str] = Field(None, max_length=100)
    email: Optional[str] = Field(None, max_length=255)
    job_title: Optional[str] = Field(None, min_length=1, max_length=255)
    department: Optional[str] = Field(None, max_length=100)
    role_category: Optional[str] = Field(None, min_length=1, max_length=100)
    tenure_months: Optional[int] = Field(None, ge=0)
    performance_metrics: Optional[Dict[str, Any]] = None
    profiling_status: Optional[str] = Field(
        None, pattern="^(PENDING|IN_PROGRESS|COMPLETED|ARCHIVED)$"
    )
    notes: Optional[str] = None
    is_active: Optional[bool] = None


class TopPerformerResponse(TopPerformerBase):
    """Schema for top performer response."""
    id: UUID
    organization_id: UUID
    is_anonymized: bool
    profiling_status: str
    trait_profile: Optional[Dict[str, Any]] = None
    counter_indicators_identified: List[Dict[str, Any]] = []
    is_active: bool
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class TopPerformerList(BaseModel):
    """Schema for paginated top performer list."""
    items: List[TopPerformerResponse]
    total: int


# Training Session Schemas


class TrainingSessionBase(BaseModel):
    """Base training session schema."""
    target_traits: List[str] = Field(default_factory=list)
    focus_areas: Optional[str] = None
    scheduled_at: Optional[datetime] = None


class TrainingSessionCreate(TrainingSessionBase):
    """Schema for creating a training session."""
    top_performer_id: UUID


class TrainingSessionUpdate(BaseModel):
    """Schema for updating a training session."""
    target_traits: Optional[List[str]] = None
    focus_areas: Optional[str] = None
    scheduled_at: Optional[datetime] = None
    status: Optional[str] = Field(
        None, pattern="^(SCHEDULED|IN_PROGRESS|COMPLETED|CANCELLED)$"
    )
    interviewer_notes: Optional[str] = None


class TrainingSessionResponse(TrainingSessionBase):
    """Schema for training session response."""
    id: UUID
    top_performer_id: UUID
    interviewer_id: Optional[UUID] = None
    session_number: int
    status: str
    started_at: Optional[datetime] = None
    completed_at: Optional[datetime] = None
    duration_minutes: Optional[int] = None
    ai_summary: Optional[str] = None
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class TrainingSessionDetail(TrainingSessionResponse):
    """Detailed training session response with transcript."""
    transcript: List[Dict[str, Any]] = []
    extracted_evidence: List[Dict[str, Any]] = []
    trait_signals: List[Dict[str, Any]] = []
    counter_indicators_mentioned: List[Dict[str, Any]] = []
    interviewer_notes: Optional[str] = None


class TrainingSessionList(BaseModel):
    """Schema for paginated training session list."""
    items: List[TrainingSessionResponse]
    total: int


# Profiling Session (Interactive) Schemas


class ProfilingStartRequest(BaseModel):
    """Request to start a profiling session."""
    top_performer_id: UUID
    target_traits: List[str] = Field(..., min_items=1)
    role_context: Optional[Dict[str, Any]] = None


class ProfilingPromptResponse(BaseModel):
    """Response containing the next prompt in profiling."""
    session_id: UUID
    phase: str
    prompt_text: str
    progress: Dict[str, Any]
    trait_being_explored: Optional[str] = None
    is_complete: bool = False


class ProfilingRespondRequest(BaseModel):
    """Request to submit a top performer's response."""
    response_text: str = Field(..., min_length=1)


class ProfilingCompleteResponse(BaseModel):
    """Response when profiling session is complete."""
    session_id: UUID
    summary: str
    traits_profiled: List[str]
    signals_extracted: int
    patterns_identified: int
    counter_indicators_found: int


# Trait Extraction Schemas


class ExtractedSignalResponse(BaseModel):
    """Response for an extracted signal."""
    trait_id: str
    trait_name: str
    signal_type: str  # POSITIVE, NEGATIVE, NEUTRAL
    strength: float
    evidence_text: str
    behavioral_indicator: str
    context: str
    confidence: float


class BehavioralPatternResponse(BaseModel):
    """Response for a behavioral pattern."""
    trait_id: str
    trait_name: str
    pattern_description: str
    frequency: str  # ALWAYS, OFTEN, SOMETIMES, RARELY
    example_quotes: List[str]
    implications_for_role: str


class CounterIndicatorResponse(BaseModel):
    """Response for a counter-indicator."""
    trait_id: str
    trait_name: str
    context: str
    evidence: str
    role_categories_affected: List[str]
    severity: str  # LOW, MEDIUM, HIGH


class TraitExtractionResultResponse(BaseModel):
    """Complete trait extraction result."""
    session_id: str
    top_performer_id: str
    extracted_signals: List[ExtractedSignalResponse]
    behavioral_patterns: List[BehavioralPatternResponse]
    counter_indicators: List[CounterIndicatorResponse]
    trait_scores: Dict[str, Dict[str, Any]]
    summary: str


# Rubric Generation Schemas


class RubricGenerationRequest(BaseModel):
    """Request to generate a rubric from top performer profiles."""
    role_category: str = Field(..., min_length=1)
    top_performer_ids: List[UUID] = Field(..., min_items=1)
    target_trait_ids: List[str] = Field(..., min_items=1)
    role_context: Optional[Dict[str, Any]] = None
    base_rubric_id: Optional[UUID] = None


class BehavioralAnchorResponse(BaseModel):
    """Response for a behavioral anchor."""
    score: int
    description: str
    example_behaviors: List[str]
    evidence_indicators: List[str]


class GeneratedRubricItemResponse(BaseModel):
    """Response for a generated rubric item."""
    trait_id: str
    trait_name: str
    behavioral_anchors: List[BehavioralAnchorResponse]
    primary_probes: List[str]
    follow_up_probes: List[str]
    star_indicators: Dict[str, List[str]]
    job_relatedness_rationale: str
    derivation_notes: str
    confidence: float


class GeneratedRubricResponse(BaseModel):
    """Response for a complete generated rubric."""
    name: str
    description: str
    organization_id: str
    role_category: str
    items: List[GeneratedRubricItemResponse]
    derivation_metadata: Dict[str, Any]
    research_basis: Optional[str] = None
    created_at: datetime


# Profile Synthesis Schemas


class ProfileSynthesisRequest(BaseModel):
    """Request to synthesize profiles across multiple top performers."""
    top_performer_ids: List[UUID] = Field(..., min_items=1)
    role_category: str


class SynthesizedPatternResponse(BaseModel):
    """Response for a synthesized pattern."""
    trait_id: str
    trait_name: str
    patterns: List[BehavioralPatternResponse]
    average_score: Optional[float] = None
    confidence: float


class ProfileSynthesisResponse(BaseModel):
    """Response for profile synthesis."""
    role_category: str
    top_performer_count: int
    synthesized_patterns: List[SynthesizedPatternResponse]
    common_strengths: List[str]
    role_success_indicators: List[str]
    generated_at: datetime
