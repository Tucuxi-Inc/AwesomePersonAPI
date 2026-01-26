"""Role profile schemas."""

from datetime import datetime
from typing import Optional, List, Dict, Any
import uuid

from pydantic import BaseModel, Field


class TraitRequirement(BaseModel):
    """Schema for a trait requirement in a role profile."""

    trait_id: uuid.UUID
    level: str  # HIGH, MODERATE, LOW
    weight: float = 1.0


class CounterIndicator(BaseModel):
    """Schema for a counter-indicator in a role profile."""

    trait_id: uuid.UUID
    threshold: str  # HIGH, MODERATE
    reason: str


class RoleProfileBase(BaseModel):
    """Base role profile schema."""

    name: str = Field(..., min_length=1, max_length=255)
    description: Optional[str] = None
    department: Optional[str] = None
    level: Optional[str] = None
    role_category: str


class RoleProfileCreate(RoleProfileBase):
    """Schema for creating a role profile."""

    critical_traits: List[Dict[str, Any]] = []
    positive_traits: List[Dict[str, Any]] = []
    counter_indicators: List[Dict[str, Any]] = []
    valence_notes: Optional[Dict[str, str]] = None
    is_template: bool = False


class RoleProfileUpdate(BaseModel):
    """Schema for updating a role profile."""

    name: Optional[str] = Field(None, min_length=1, max_length=255)
    description: Optional[str] = None
    department: Optional[str] = None
    level: Optional[str] = None
    role_category: Optional[str] = None
    critical_traits: Optional[List[Dict[str, Any]]] = None
    positive_traits: Optional[List[Dict[str, Any]]] = None
    counter_indicators: Optional[List[Dict[str, Any]]] = None
    valence_notes: Optional[Dict[str, str]] = None
    is_active: Optional[bool] = None


class RoleProfileResponse(RoleProfileBase):
    """Schema for role profile response."""

    id: uuid.UUID
    organization_id: Optional[uuid.UUID] = None
    critical_traits: List[Dict[str, Any]]
    positive_traits: List[Dict[str, Any]]
    counter_indicators: List[Dict[str, Any]]
    valence_notes: Optional[Dict[str, str]] = None
    is_template: bool
    is_active: bool
    derived_from: Optional[uuid.UUID] = None
    derivation_notes: Optional[str] = None
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class RoleProfileList(BaseModel):
    """Schema for list of role profiles."""

    items: List[RoleProfileResponse]
    total: int


class RoleProfileClone(BaseModel):
    """Schema for cloning a role profile."""

    name: str = Field(..., min_length=1, max_length=255)
    description: Optional[str] = None


class RoleTemplateCategory(BaseModel):
    """Schema for a category of role templates."""

    name: str
    templates: List[RoleProfileResponse]


class RoleTemplatesByCategory(BaseModel):
    """Schema for role templates grouped by category."""

    categories: List[RoleTemplateCategory]
    total: int
