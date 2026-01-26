"""Invitation schemas."""

from datetime import datetime
from typing import Optional, List
import uuid

from pydantic import BaseModel, Field, EmailStr


class InvitationCreate(BaseModel):
    """Schema for creating an invitation."""

    recipient_email: EmailStr
    recipient_name: Optional[str] = None
    trait_ids: Optional[List[str]] = None
    role_profile_id: Optional[uuid.UUID] = None
    expires_in_days: int = Field(default=7, ge=1, le=30)
    custom_message: Optional[str] = None


class CandidateInvitationCreate(InvitationCreate):
    """Schema for creating a candidate interview invitation."""

    candidate_id: uuid.UUID


class TopPerformerInvitationCreate(InvitationCreate):
    """Schema for creating a top performer profiling invitation."""

    top_performer_id: uuid.UUID
    expires_in_days: int = Field(default=14, ge=1, le=30)


class InvitationResponse(BaseModel):
    """Schema for invitation response."""

    id: uuid.UUID
    invitation_type: str
    token: str
    status: str
    recipient_email: str
    recipient_name: Optional[str] = None
    candidate_id: Optional[uuid.UUID] = None
    top_performer_id: Optional[uuid.UUID] = None
    trait_ids: Optional[List[str]] = None
    role_profile_id: Optional[uuid.UUID] = None
    expires_at: datetime
    sent_at: Optional[datetime] = None
    viewed_at: Optional[datetime] = None
    started_at: Optional[datetime] = None
    completed_at: Optional[datetime] = None
    custom_message: Optional[str] = None
    interview_session_id: Optional[uuid.UUID] = None
    training_session_id: Optional[uuid.UUID] = None
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class InvitationList(BaseModel):
    """Schema for list of invitations."""

    items: List[InvitationResponse]
    total: int


class InvitationLinkResponse(BaseModel):
    """Schema for invitation link response."""

    invitation_id: uuid.UUID
    token: str
    link: str
    expires_at: datetime


# Public-facing schemas (for self-service access)

class InvitationValidateResponse(BaseModel):
    """Schema for validating an invitation token (public)."""

    valid: bool
    invitation_type: Optional[str] = None
    recipient_name: Optional[str] = None
    organization_name: Optional[str] = None
    role_name: Optional[str] = None
    custom_message: Optional[str] = None
    expires_at: Optional[datetime] = None
    error: Optional[str] = None


class SelfServiceSessionStart(BaseModel):
    """Schema for starting a self-service session."""

    consent_given: bool = False


class SelfServiceSessionResponse(BaseModel):
    """Schema for self-service session response."""

    session_id: uuid.UUID
    session_type: str  # "interview" or "profiling"
    next_prompt: str
    prompt_type: str
    trait_name: Optional[str] = None
    overall_progress: float = 0.0
    is_complete: bool = False


class SelfServiceResponseSubmit(BaseModel):
    """Schema for submitting a response in self-service mode."""

    session_id: uuid.UUID
    response_text: str = Field(..., min_length=1, max_length=10000)


class DisclosureResponse(BaseModel):
    """Schema for disclosure content."""

    title: str
    sections: List[dict]
    consent_required: bool
    consent_text: Optional[str] = None
    jurisdiction: Optional[str] = None
