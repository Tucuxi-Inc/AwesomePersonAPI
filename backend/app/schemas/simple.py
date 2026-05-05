"""Pydantic schemas for Simple Mode."""

from datetime import datetime
from typing import Any, Dict, List, Optional
from pydantic import BaseModel, Field, EmailStr


# --- Shared bundle types (defined first so request/response schemas can reference) ---

class RequirementResponse(BaseModel):
    """A single objective requirement extracted from a job description."""
    id: str
    type: str  # education, experience, skill, certification
    requirement: str
    required: bool


class ExtractedRequirementsBundle(BaseModel):
    """Full LLM-extracted requirements payload, matching the frontend contract."""
    objective_requirements: List[RequirementResponse] = []
    nice_to_haves: List[Dict[str, Any]] = []
    responsibilities: List[str] = []
    suggested_traits: List[str] = []


# --- Request Schemas ---

class CreateSimpleAssessmentRequest(BaseModel):
    """Request to create a new simple assessment."""
    job_title: str = Field(..., min_length=1, max_length=255)
    job_description: str = Field(..., min_length=10)


class ConfirmRequirementsRequest(BaseModel):
    """Request to confirm extracted requirements.

    Accepts the full bundle (objective_requirements + nice_to_haves +
    responsibilities + suggested_traits) so the user can edit any of them
    before locking in.
    """
    requirements: ExtractedRequirementsBundle = Field(
        ...,
        description="Full bundle of requirements (objective + nice-to-haves + responsibilities + suggested traits)"
    )


class SelectTraitsRequest(BaseModel):
    """Request to select traits for assessment."""
    trait_ids: List[str] = Field(
        ...,
        min_length=1,
        max_length=5,
        description="List of trait IDs (max 5)"
    )


class AddCandidateRequest(BaseModel):
    """Request to add a candidate."""
    email: EmailStr
    full_name: str = Field(..., min_length=1, max_length=255)
    phone: Optional[str] = Field(None, max_length=50)


class SendInviteRequest(BaseModel):
    """Request to send interview invite."""
    custom_message: Optional[str] = Field(
        None,
        max_length=500,
        description="Optional custom message to include in the invitation email"
    )


class SendInviteResponse(BaseModel):
    """Response from sending an interview invite — surfaces the magic link
    so admins can copy it for out-of-band channels."""
    candidate_id: str
    magic_link: str
    expires_at: datetime
    email_queued: bool


# --- Response Schemas ---

class SimpleCandidateResponse(BaseModel):
    """Simple candidate response."""
    id: str
    email: str
    full_name: str
    phone: Optional[str]
    qualification_status: str
    qualification_gaps: Optional[List[dict]]
    interview_status: str
    invited_at: Optional[datetime]
    interview_completed_at: Optional[datetime]
    composite_score: Optional[float]
    recommendation: Optional[str]
    created_at: datetime


class SimpleCandidateDetailResponse(SimpleCandidateResponse):
    """Detailed candidate response with scores."""
    resume_filename: Optional[str]
    resume_parsed_data: Optional[dict]
    qualification_results: Optional[List[dict]]
    trait_scores: Optional[dict]
    recommendation_rationale: Optional[str]


class SimpleAssessmentResponse(BaseModel):
    """Simple assessment response."""
    id: str
    job_title: str
    job_description: str
    status: str
    extracted_requirements: ExtractedRequirementsBundle = ExtractedRequirementsBundle()
    requirements_confirmed: bool
    selected_trait_ids: List[str]
    total_candidates: int
    qualified_candidates: int
    interviews_completed: int
    created_at: datetime
    completed_at: Optional[datetime]


class SimpleAssessmentDetailResponse(SimpleAssessmentResponse):
    """Detailed assessment response with candidates."""
    candidates: List[SimpleCandidateResponse]


class SimpleAssessmentListResponse(BaseModel):
    """Paginated list of assessments."""
    items: List[SimpleAssessmentResponse]
    total: int
    page: int
    page_size: int


class TraitOptionResponse(BaseModel):
    """Trait option for selection."""
    id: str
    name: str
    category: str
    definition: str


class TraitOptionsResponse(BaseModel):
    """Available traits for selection."""
    traits: List[TraitOptionResponse]
    max_selection: int = 5


class CandidateResultResponse(BaseModel):
    """Candidate assessment result."""
    candidate_id: str
    candidate_name: str
    candidate_email: str
    composite_score: float  # 0-10 scale
    recommendation: str
    recommendation_rationale: str
    trait_scores: List[dict]
    # Format: [{"trait_id": "...", "trait_name": "...", "score": 8,
    #           "confidence": 0.9, "explanation": "..."}]


class AssessmentResultsResponse(BaseModel):
    """All assessment results."""
    assessment_id: str
    job_title: str
    status: str
    total_candidates: int
    completed_interviews: int
    results: List[CandidateResultResponse]


# --- Public Interview Schemas (for magic links) ---

class PublicInterviewInfoResponse(BaseModel):
    """Public interview info for candidate."""
    job_title: str
    organization_name: str
    candidate_name: str
    estimated_duration_minutes: int = 30
    traits_count: int
    traits_to_assess: List[str] = []
    interview_status: str = "NOT_STARTED"
    instructions: str


class PublicInterviewStartResponse(BaseModel):
    """Response after starting public interview.

    Includes both `overall_progress`/`interview_complete` (the canonical
    field names used internally) and `progress`/`is_complete` (the names
    the reference frontend reads). Populating both keeps all consumers
    happy without forcing one side or the other to migrate.
    """
    session_id: str
    next_prompt: str
    prompt_type: str
    trait_name: Optional[str]
    overall_progress: float
    progress: float = 0.0
    is_complete: bool = False


class PublicInterviewRespondRequest(BaseModel):
    """Request to submit response in public interview."""
    response_text: str = Field(..., min_length=1, max_length=10000)


class PublicInterviewRespondResponse(BaseModel):
    """Response after submitting answer.

    See PublicInterviewStartResponse note: ships both naming conventions
    so the frontend's `progress`/`is_complete` reads work alongside any
    third-party client that uses the canonical `overall_progress`/
    `interview_complete` names.
    """
    next_prompt: str
    prompt_type: str
    trait_name: Optional[str]
    overall_progress: float
    progress: float = 0.0
    interview_complete: bool
    is_complete: bool = False


class PublicInterviewStatusResponse(BaseModel):
    """Public interview status."""
    status: str  # NOT_STARTED, IN_PROGRESS, COMPLETED, EXPIRED
    progress: float
    is_complete: bool


# --- API Key Schemas ---

class CreateAPIKeyRequest(BaseModel):
    """Request to create an API key."""
    name: str = Field(..., min_length=1, max_length=255)
    tier: str = Field(default="FREE")  # FREE, BASIC, PRO, ENTERPRISE


class APIKeyResponse(BaseModel):
    """API key response (without full key)."""
    id: str
    name: str
    key_prefix: str
    tier: str
    is_active: bool
    created_at: datetime
    last_used_at: Optional[datetime]
    expires_at: Optional[datetime]
    limits: dict


class APIKeyCreatedResponse(APIKeyResponse):
    """API key response with full key (only shown once)."""
    api_key: str  # Full key, only shown on creation
