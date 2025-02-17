# app/schemas/user.py
from pydantic import BaseModel, EmailStr, Field
from datetime import datetime
from typing import Optional
from uuid import UUID


class UserBase(BaseModel):
    """Base User Schema"""

    email: EmailStr
    username: Optional[str] = None
    is_active: bool = True


class UserCreate(UserBase):
    """Schema for creating a user"""

    password: str = Field(..., min_length=8)


class UserUpdate(BaseModel):
    """Schema for updating a user"""

    email: Optional[EmailStr] = None
    username: Optional[str] = None
    password: Optional[str] = Field(None, min_length=8)


class UserInDB(UserBase):
    """Schema for user in database"""

    id: UUID
    hashed_password: str
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True


class UserResponse(UserBase):
    """Schema for user response"""

    id: UUID
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True


class Token(BaseModel):
    """Schema for authentication token"""

    access_token: str
    token_type: str = "bearer"


class TokenData(BaseModel):
    """Schema for token data"""

    user_id: str
