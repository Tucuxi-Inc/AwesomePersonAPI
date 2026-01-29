"""Resume schemas."""

from datetime import datetime
from typing import List, Optional
from uuid import UUID

from pydantic import BaseModel, Field


class ResumeBase(BaseModel):
    """Base resume schema."""
    filename: str


class ResumeUploadResponse(BaseModel):
    """Response after uploading a resume."""
    id: UUID
    candidate_id: UUID
    filename: str
    file_type: str
    file_size_bytes: int
    parse_status: str
    created_at: datetime

    class Config:
        from_attributes = True


class ParsedExperience(BaseModel):
    """Parsed work experience entry."""
    company: str
    title: str
    start_date: Optional[str] = None
    end_date: Optional[str] = None
    duration_months: Optional[int] = None
    description: Optional[str] = None
    achievements: List[str] = Field(default_factory=list)


class ParsedEducation(BaseModel):
    """Parsed education entry."""
    institution: str
    degree: Optional[str] = None
    field_of_study: Optional[str] = None
    graduation_year: Optional[int] = None
    gpa: Optional[str] = None


class ParsedCertification(BaseModel):
    """Parsed certification entry."""
    name: str
    issuer: Optional[str] = None
    issue_date: Optional[str] = None
    expiration_date: Optional[str] = None


class ParsedResumeData(BaseModel):
    """Structured data extracted from resume."""
    contact: Optional[dict] = None
    summary: Optional[str] = None
    experience: List[ParsedExperience] = Field(default_factory=list)
    education: List[ParsedEducation] = Field(default_factory=list)
    skills: List[str] = Field(default_factory=list)
    certifications: List[ParsedCertification] = Field(default_factory=list)
    languages: List[str] = Field(default_factory=list)
    total_years_experience: Optional[float] = None


class ResumeResponse(BaseModel):
    """Full resume response with parsed data."""
    id: UUID
    candidate_id: UUID
    filename: str
    file_type: str
    file_size_bytes: int
    parse_status: str
    parse_error: Optional[str] = None
    raw_text: Optional[str] = None
    parsed_data: Optional[ParsedResumeData] = None
    ai_analysis: Optional[dict] = None
    version: int
    is_primary: bool
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class ResumeList(BaseModel):
    """List of resumes for a candidate."""
    items: List[ResumeUploadResponse]
    total: int
