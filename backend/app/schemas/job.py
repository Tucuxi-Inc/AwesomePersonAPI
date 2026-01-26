"""Job schemas."""

from datetime import datetime
from typing import Optional, List, Dict, Any
import uuid

from pydantic import BaseModel, Field

from app.models.job import JobStatus


class ObjectiveRequirement(BaseModel):
    """Schema for an objective requirement."""

    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    type: str  # education, experience, certification, skill, other
    requirement: str
    required: bool = True


class JobBase(BaseModel):
    """Base job schema."""

    title: str = Field(..., min_length=1, max_length=255)
    description: str = Field(..., min_length=1)
    department: Optional[str] = Field(None, max_length=100)
    location: Optional[str] = Field(None, max_length=255)
    employment_type: Optional[str] = Field(None, max_length=50)  # FULL_TIME, PART_TIME, CONTRACT


class JobCreate(JobBase):
    """Schema for creating a job."""

    role_profile_id: Optional[uuid.UUID] = None
    objective_requirements: List[Dict[str, Any]] = []
    nice_to_haves: List[Dict[str, Any]] = []
    responsibilities: List[str] = []
    suggested_traits: List[str] = []
    status: JobStatus = JobStatus.DRAFT


class JobUpdate(BaseModel):
    """Schema for updating a job."""

    title: Optional[str] = Field(None, min_length=1, max_length=255)
    description: Optional[str] = Field(None, min_length=1)
    department: Optional[str] = Field(None, max_length=100)
    location: Optional[str] = Field(None, max_length=255)
    employment_type: Optional[str] = Field(None, max_length=50)
    role_profile_id: Optional[uuid.UUID] = None
    objective_requirements: Optional[List[Dict[str, Any]]] = None
    nice_to_haves: Optional[List[Dict[str, Any]]] = None
    responsibilities: Optional[List[str]] = None
    suggested_traits: Optional[List[str]] = None
    status: Optional[JobStatus] = None


class JobResponse(JobBase):
    """Schema for job response."""

    id: uuid.UUID
    organization_id: uuid.UUID
    role_profile_id: Optional[uuid.UUID] = None
    objective_requirements: List[Dict[str, Any]]
    nice_to_haves: List[Dict[str, Any]]
    responsibilities: List[str]
    suggested_traits: List[str]
    status: JobStatus
    created_by_id: Optional[uuid.UUID] = None
    requirements_extracted_at: Optional[str] = None
    extraction_model: Optional[str] = None
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class JobList(BaseModel):
    """Schema for list of jobs."""

    items: List[JobResponse]
    total: int


class JobWithRoleProfile(JobResponse):
    """Schema for job with role profile details."""

    role_profile_name: Optional[str] = None
    role_profile_category: Optional[str] = None


class ExtractedRequirements(BaseModel):
    """Schema for LLM-extracted requirements from job description."""

    objective_requirements: List[Dict[str, Any]]
    nice_to_haves: List[Dict[str, Any]]
    responsibilities: List[str]
    suggested_traits: List[str]
    extraction_notes: Optional[str] = None
