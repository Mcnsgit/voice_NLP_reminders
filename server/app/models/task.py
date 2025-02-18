# app/models/task.py
from sqlalchemy import (
    Column,
    String,
    ForeignKey,
    Integer,
    Enum as SQLEnum,
    DateTime,
    Text,
)
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.db.base_class import Base
from .enums import TaskStatus


class Task(Base):
    """
    Task model representing a user's task in the system.
    Includes all necessary fields for basic task management and tracking.
    """

    __tablename__ = "tasks"

    title = Column(String(255), nullable=False, index=True)
    description = Column(Text, nullable=True)
    due_date = Column(DateTime(timezone=True), nullable=True, index=True)
    status = Column(
        SQLEnum(TaskStatus), default=TaskStatus.TODO, nullable=False, index=True
    )
    priority = Column(Integer, default=1, nullable=False, index=True)
    user_id = Column(
        Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True
    )
    voice_input_id = Column(
        Integer,
        ForeignKey("voice_inputs.id", ondelete="SET NULL"),
        nullable=True,
        unique=True,  # One voice input per task
    )

    # Relationships
    user = relationship("User", back_populates="tasks")
    reminders = relationship(
        "Reminder", back_populates="task", cascade="all, delete-orphan"
    )
    voice_input = relationship("VoiceInput", back_populates="task", single_parent=True)
