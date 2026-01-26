"""Trait schemas."""

from datetime import datetime
from typing import Optional, List
import uuid

from pydantic import BaseModel


class TraitValenceMappingResponse(BaseModel):
    """Schema for trait valence mapping response."""

    id: uuid.UUID
    role_category: str
    valence: str
    optimal_range_min: int
    optimal_range_max: int
    rationale: str
    notes: Optional[str] = None

    class Config:
        from_attributes = True


class TraitResponse(BaseModel):
    """Schema for trait response."""

    id: uuid.UUID
    name: str
    category: str
    definition: str
    spectrum_low_label: str
    spectrum_high_label: str
    behavioral_markers_low: List[str]
    behavioral_markers_high: List[str]
    counter_indicator_for: List[str]
    display_order: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class TraitDetailResponse(TraitResponse):
    """Schema for detailed trait response with valence mappings."""

    valence_mappings: List[TraitValenceMappingResponse] = []


class TraitList(BaseModel):
    """Schema for list of traits."""

    items: List[TraitResponse]
    total: int


class TraitCategoryResponse(BaseModel):
    """Schema for trait category."""

    name: str
    traits: List[TraitResponse]
