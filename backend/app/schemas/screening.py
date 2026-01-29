"""Candidate job screening schemas."""

from datetime import datetime
from typing import List, Optional
from uuid import UUID

from pydantic import BaseModel, Field


class RequirementResult(BaseModel):
    """Result of checking a single requirement against resume."""
    requirement_id: str
    requirement_text: str
    requirement_type: str  # education, experience, certification, skill
    required: bool
    status: str  # MET, NOT_MET, UNCLEAR
    evidence: Optional[str] = None  # Text from resume that supports status
    explanation: str  # Why this status was determined


class GapItem(BaseModel):
    """A gap in candidate qualifications."""
    requirement_id: str
    requirement: str
    requirement_type: str
    explanation: str


class ScreenCandidateRequest(BaseModel):
    """Request to screen a candidate against job requirements."""
    resume_id: Optional[UUID] = None  # If not provided, uses primary resume


class ScreeningResponse(BaseModel):
    """Response from screening a candidate."""
    id: UUID
    candidate_id: UUID
    job_id: UUID
    resume_id: UUID
    qualification_status: str  # PENDING, QUALIFIED, NOT_QUALIFIED, NEEDS_REVIEW
    requirement_results: List[RequirementResult]
    gaps: List[GapItem]
    gap_count: int
    admin_override: bool
    override_by_id: Optional[UUID] = None
    override_reason: Optional[str] = None
    override_at: Optional[datetime] = None
    screened_at: Optional[datetime] = None
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class ScreeningSummary(BaseModel):
    """Summary of screening for list views."""
    id: UUID
    candidate_id: UUID
    candidate_name: str
    candidate_email: str
    qualification_status: str
    gap_count: int
    admin_override: bool
    screened_at: Optional[datetime] = None


class QualifiedCandidatesList(BaseModel):
    """List of qualified candidates for a job."""
    items: List[ScreeningSummary]
    total: int


class GapAnalysisCandidatesList(BaseModel):
    """List of candidates with gaps (not qualified)."""
    items: List[ScreeningSummary]
    total: int


class OverrideRequest(BaseModel):
    """Request to override qualification status."""
    reason: str = Field(..., min_length=10, max_length=1000)


class OverrideResponse(BaseModel):
    """Response after overriding qualification."""
    id: UUID
    candidate_id: UUID
    job_id: UUID
    qualification_status: str
    admin_override: bool
    override_by_id: UUID
    override_reason: str
    override_at: datetime

    class Config:
        from_attributes = True


class JobCandidatesStats(BaseModel):
    """Statistics about candidates for a job."""
    total: int
    qualified: int
    not_qualified: int
    needs_review: int
    pending: int
    overridden: int
