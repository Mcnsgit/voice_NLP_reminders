# app/schemas/user.py
from pydantic import EmailStr, Field
from typing import Optional, List
from datetime import datetime
from .base import BaseSchema
from app.schemas.task import TaskResponse


class UserRead(BaseSchema):
    """Schema for reading user data"""

    id: int
    email: EmailStr
    username: Optional[str] = None
    is_active: bool
    last_login: Optional[datetime] = None
    created_at: datetime
    updated_at: datetime


class UserCreate(BaseSchema):
    """Schema for creating a new user"""

    email: EmailStr
    password: str = Field(..., min_length=8)
    username: Optional[str] = None


class UserUpdate(BaseSchema):
    """Schema for updating a user"""

    email: Optional[EmailStr] = None
    username: Optional[str] = None
    password: Optional[str] = Field(None, min_length=8)


class UserDetail(UserRead):
    """Detailed user response with related data"""

    tasks_count: int
    voice_inputs_count: int
    recent_tasks: List[TaskResponse]
