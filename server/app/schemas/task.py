from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional
from uuid import UUID
from app.models.enums import TaskStatus


class TaskBase(BaseModel):
    """Base Task Schema"""

    title: str = Field(..., min_length=1, max_length=255)
    description: Optional[str] = None
    due_date: Optional[datetime] = None
    priority: Optional[int] = Field(None, ge=1, le=5)
    # Fix: Only use Field() or default, not both
    status: Optional[TaskStatus] = Field(default=TaskStatus.TODO)


class TaskCreate(TaskBase):
    """Schema for creating a task"""

    pass


class TaskUpdate(BaseModel):
    """Schema for updating a task"""

    title: Optional[str] = Field(None, min_length=1, max_length=255)
    description: Optional[str] = None
    due_date: Optional[datetime] = None
    priority: Optional[int] = Field(None, ge=1, le=5)
    status: Optional[TaskStatus] = None


class TaskResponse(TaskBase):
    """Schema for task response"""

    id: UUID
    user_id: UUID
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True
