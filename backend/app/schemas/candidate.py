"""Candidate schemas."""

from datetime import datetime
from typing import List, Optional
from uuid import UUID

from pydantic import BaseModel, EmailStr, Field


class CandidateBase(BaseModel):
    """Base candidate schema."""
    email: EmailStr
    full_name: str = Field(..., min_length=1, max_length=255)
    phone: Optional[str] = Field(None, max_length=50)
    current_title: Optional[str] = Field(None, max_length=255)
    current_company: Optional[str] = Field(None, max_length=255)
    linkedin_url: Optional[str] = Field(None, max_length=500)
    years_experience: Optional[int] = Field(None, ge=0)
    source: Optional[str] = Field(None, max_length=100)
    referrer: Optional[str] = Field(None, max_length=255)
    notes: Optional[str] = None
    tags: List[str] = Field(default_factory=list)


class CandidateCreate(CandidateBase):
    """Schema for creating a candidate."""
    role_profile_id: Optional[UUID] = None


class CandidateUpdate(BaseModel):
    """Schema for updating a candidate."""
    email: Optional[EmailStr] = None
    full_name: Optional[str] = Field(None, min_length=1, max_length=255)
    phone: Optional[str] = Field(None, max_length=50)
    current_title: Optional[str] = Field(None, max_length=255)
    current_company: Optional[str] = Field(None, max_length=255)
    linkedin_url: Optional[str] = Field(None, max_length=500)
    years_experience: Optional[int] = Field(None, ge=0)
    source: Optional[str] = Field(None, max_length=100)
    referrer: Optional[str] = Field(None, max_length=255)
    role_profile_id: Optional[UUID] = None
    status: Optional[str] = Field(None, pattern="^(NEW|SCREENING|INTERVIEWING|ASSESSED|OFFER|HIRED|REJECTED|WITHDRAWN)$")
    notes: Optional[str] = None
    tags: Optional[List[str]] = None
    is_active: Optional[bool] = None


class CandidateResponse(CandidateBase):
    """Schema for candidate response."""
    id: UUID
    organization_id: UUID
    role_profile_id: Optional[UUID] = None
    status: str
    is_active: bool
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class CandidateList(BaseModel):
    """Schema for paginated candidate list."""
    items: List[CandidateResponse]
    total: int
