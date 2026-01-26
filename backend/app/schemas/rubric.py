"""Scoring rubric schemas."""

from datetime import datetime
from typing import Optional, List, Dict, Any
import uuid

from pydantic import BaseModel, Field


class BehavioralAnchor(BaseModel):
    """Schema for a behavioral anchor."""

    label: str
    description: str
    indicators: List[str]


class Probe(BaseModel):
    """Schema for an interview probe."""

    question: str
    purpose: str
    star_focus: str  # situation, task, action, result


class RubricBase(BaseModel):
    """Base rubric schema."""

    name: str = Field(..., min_length=1, max_length=255)
    description: Optional[str] = None
    trait_id: uuid.UUID


class RubricCreate(RubricBase):
    """Schema for creating a rubric."""

    behavioral_anchors: Dict[str, Dict[str, Any]]
    primary_probes: List[Dict[str, Any]] = []
    follow_up_probes: Dict[str, List[str]] = {}
    star_indicators: Optional[Dict[str, List[str]]] = None
    role_profile_id: Optional[uuid.UUID] = None


class RubricUpdate(BaseModel):
    """Schema for updating a rubric."""

    name: Optional[str] = Field(None, min_length=1, max_length=255)
    description: Optional[str] = None
    behavioral_anchors: Optional[Dict[str, Dict[str, Any]]] = None
    primary_probes: Optional[List[Dict[str, Any]]] = None
    follow_up_probes: Optional[Dict[str, List[str]]] = None
    star_indicators: Optional[Dict[str, List[str]]] = None
    is_active: Optional[bool] = None


class RubricResponse(RubricBase):
    """Schema for rubric response."""

    id: uuid.UUID
    organization_id: Optional[uuid.UUID] = None
    role_profile_id: Optional[uuid.UUID] = None
    version: int
    behavioral_anchors: Dict[str, Dict[str, Any]]
    primary_probes: List[Dict[str, Any]]
    follow_up_probes: Dict[str, List[str]]
    star_indicators: Optional[Dict[str, List[str]]] = None
    is_default: bool
    is_active: bool
    derived_from: Optional[uuid.UUID] = None
    derivation_notes: Optional[str] = None
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class RubricList(BaseModel):
    """Schema for list of rubrics."""

    items: List[RubricResponse]
    total: int


class RubricClone(BaseModel):
    """Schema for cloning a rubric."""

    name: str = Field(..., min_length=1, max_length=255)
    description: Optional[str] = None
    role_profile_id: Optional[uuid.UUID] = None
