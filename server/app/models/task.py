from sqlalchemy import Column, String, ForeignKey, Integer, Enum, DateTime, UUID
from sqlalchemy.orm import relationship
from app.db.base import BaseModel
from app.models.enums import TaskStatus
import uuid


class Task(BaseModel):
    __tablename__ = "tasks"

    # Change id to UUID type
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    title = Column(String, nullable=False)
    description = Column(String)
    due_date = Column(DateTime(timezone=True))
    status = Column(Enum(TaskStatus), default=TaskStatus.TODO)
    priority = Column(Integer)
    user_id = Column(
        UUID(as_uuid=True), ForeignKey("users.id", ondelete="CASCADE"), nullable=False
    )

    user = relationship("User", back_populates="tasks")
    notes = relationship("Note", back_populates="task", cascade="all, delete-orphan")
    reminders = relationship(
        "Reminder", back_populates="task", cascade="all, delete-orphan"
    )
