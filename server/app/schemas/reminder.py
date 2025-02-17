# app/schemas/reminder.py
from datetime import datetime
from typing import Optional
from pydantic import BaseModel


class ReminderBase(BaseModel):
    task_id: int
    reminder_time: datetime
    is_sent: bool = False


class ReminderCreate(ReminderBase):
    pass


class ReminderUpdate(BaseModel):
    reminder_time: Optional[datetime] = None
    is_sent: Optional[bool] = None


class ReminderInDB(ReminderBase):
    id: int
    created_at: datetime

    class Config:
        from_attributes = True


class ReminderResponse(ReminderInDB):
    pass
