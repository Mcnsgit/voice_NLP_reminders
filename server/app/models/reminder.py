# app/models/reminder.py
from sqlalchemy import (
    Column,
    DateTime,
    ForeignKey,
    Boolean,
    Integer,
    Enum as SQLEnum,
    String,
)
from sqlalchemy.orm import relationship
from app.db.base_class import Base

from .enums import ReminderType


class Reminder(Base):
    __tablename__ = "reminders"

    task_id = Column(
        Integer, ForeignKey("tasks.id", ondelete="CASCADE"), nullable=False
    )
    reminder_time = Column(DateTime(timezone=True), nullable=False)
    is_sent = Column(Boolean, default=False)
    type = Column(SQLEnum(ReminderType), default=ReminderType.ONE_TIME, nullable=False)
    recurrence_pattern = Column(String, nullable=True)

    task = relationship("Task", back_populates="reminders")
