"""User schemas."""

from datetime import datetime
from typing import Optional
import uuid

from pydantic import BaseModel, EmailStr, Field


class UserBase(BaseModel):
    """Base user schema."""

    email: EmailStr
    full_name: str = Field(..., min_length=1, max_length=255)
    role: str = "INTERVIEWER"
    phone: Optional[str] = None
    title: Optional[str] = None
    bio: Optional[str] = None


class UserCreate(UserBase):
    """Schema for creating a user."""

    password: str = Field(..., min_length=8, max_length=100)
    organization_id: Optional[uuid.UUID] = None


class UserUpdate(BaseModel):
    """Schema for updating a user."""

    full_name: Optional[str] = Field(None, min_length=1, max_length=255)
    role: Optional[str] = None
    phone: Optional[str] = None
    title: Optional[str] = None
    bio: Optional[str] = None
    is_active: Optional[bool] = None
    organization_id: Optional[uuid.UUID] = None


class UserResponse(BaseModel):
    """Schema for user response."""

    id: uuid.UUID
    email: str
    full_name: str
    role: str
    is_active: bool
    is_superuser: bool
    phone: Optional[str] = None
    title: Optional[str] = None
    bio: Optional[str] = None
    organization_id: Optional[uuid.UUID] = None
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class UserList(BaseModel):
    """Schema for list of users."""

    items: list[UserResponse]
    total: int
