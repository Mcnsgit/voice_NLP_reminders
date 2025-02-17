from sqlalchemy import Column, DateTime, ForeignKey, Boolean, UUID
from sqlalchemy.orm import relationship
from app.db.base import BaseModel
import uuid


class Reminder(BaseModel):
    __tablename__ = "reminders"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    task_id = Column(
        UUID(as_uuid=True), ForeignKey("tasks.id", ondelete="CASCADE"), nullable=False
    )
    reminder_time = Column(DateTime(timezone=True), nullable=False)
    is_sent = Column(Boolean, default=False)

    task = relationship("Task", back_populates="reminders")
