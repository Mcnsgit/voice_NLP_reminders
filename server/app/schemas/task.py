# app/schemas/task.py
from pydantic import Field
from datetime import datetime
from typing import Optional, List, Dict
from .base import BaseSchema, TimestampedSchema
from app.models.enums import TaskStatus


class TaskBase(BaseSchema):
    """Base Task Schema"""

    title: str = Field(..., min_length=1, max_length=255)
    description: Optional[str] = None
    due_date: Optional[datetime] = None
    priority: int = Field(default=1, ge=1, le=5)
    status: TaskStatus = Field(default=TaskStatus.TODO)


class TaskCreate(TaskBase):
    """Schema for creating a new task"""

    voice_input_id: Optional[int] = None


class TaskUpdate(BaseSchema):
    """Schema for updating a task"""

    title: Optional[str] = Field(None, min_length=1, max_length=255)
    description: Optional[str] = None
    due_date: Optional[datetime] = None
    priority: Optional[int] = Field(None, ge=1, le=5)
    status: Optional[TaskStatus] = None


class TaskResponse(TaskBase, TimestampedSchema):
    """Basic task response schema"""

    id: int
    user_id: int
    voice_input_id: Optional[int] = None


# Move this to a separate file if needed
class TaskWithRelations(TaskResponse):
    """Task response with basic relation information"""

    reminders_count: int = 0
    has_voice_input: bool = False


class TaskDetail(TaskResponse):
    """Detailed task response with additional information"""

    is_overdue: bool
    days_until_due: Optional[int]
    reminders: List[dict] = []  # Will be populated with reminder data when needed
    voice_input: Optional[dict] = (
        None  # Will be populated with voice input data when needed
    )


class TaskStatisticsResponse(BaseSchema):
    """
    Schema for task statistics response. Provides aggregate statistics
    about user's tasks.
    """

    total_tasks: int
    tasks_by_status: Dict[str, int]
    overdue_tasks: int
    completion_rate: float
    tasks_by_priority: Dict[int, int]
    tasks_created_this_week: int
    tasks_completed_this_week: int
    upcoming_tasks: List[TaskResponse]

    class Config:
        from_attributes = True


# Task list response with pagination
class TaskListResponse(BaseSchema):
    """
    Schema for paginated task list response. Includes tasks and
    pagination metadata.
    """

    items: List[TaskResponse]
    total: int
    page: int
    size: int
    pages: int

    class Config:
        from_attributes = True
