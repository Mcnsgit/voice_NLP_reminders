# app/schemas/reminder.py
from datetime import datetime
from typing import Optional
from .base import BaseSchema, TimestampedSchema
from app.models.enums import ReminderType


class ReminderBase(BaseSchema):
    """Base Reminder Schema"""

    reminder_time: datetime
    type: ReminderType = ReminderType.ONE_TIME
    recurrence_pattern: Optional[str] = None


class ReminderCreate(ReminderBase):
    """Schema for creating a new reminder"""

    task_id: int


class ReminderUpdate(BaseSchema):
    """Schema for updating a reminder"""

    reminder_time: Optional[datetime] = None
    is_sent: Optional[bool] = None
    type: Optional[ReminderType] = None
    recurrence_pattern: Optional[str] = None


class ReminderResponse(ReminderBase, TimestampedSchema):
    """Schema for reminder response"""

    id: int
    task_id: int
    is_sent: bool
