"""Authentication schemas."""

from typing import Optional
import uuid

from pydantic import BaseModel, EmailStr, Field


class UserRegister(BaseModel):
    """Schema for user registration."""

    email: EmailStr
    password: str = Field(..., min_length=8, max_length=100)
    full_name: str = Field(..., min_length=1, max_length=255)
    organization_id: Optional[uuid.UUID] = None


class UserLogin(BaseModel):
    """Schema for user login."""

    email: EmailStr
    password: str


class Token(BaseModel):
    """Schema for JWT tokens."""

    access_token: str
    refresh_token: str
    token_type: str = "bearer"


class TokenRefresh(BaseModel):
    """Schema for token refresh."""

    refresh_token: str


class TokenPayload(BaseModel):
    """Schema for decoded token payload."""

    sub: str
    exp: int
    type: str


class UserResponse(BaseModel):
    """Schema for user response."""

    id: uuid.UUID
    email: str
    full_name: str
    role: str
    is_active: bool
    is_superuser: bool
    organization_id: Optional[uuid.UUID] = None
    phone: Optional[str] = None
    title: Optional[str] = None
    bio: Optional[str] = None

    class Config:
        from_attributes = True


class PasswordChange(BaseModel):
    """Schema for password change."""

    current_password: str
    new_password: str = Field(..., min_length=8, max_length=100)


class ProfileUpdate(BaseModel):
    """Schema for updating current user's profile."""

    full_name: Optional[str] = Field(None, min_length=1, max_length=255)
    phone: Optional[str] = Field(None, max_length=20)
    title: Optional[str] = Field(None, max_length=100)
    bio: Optional[str] = Field(None, max_length=500)
