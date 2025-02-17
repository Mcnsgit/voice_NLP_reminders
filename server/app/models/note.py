# 4. Update Note model (app/models/note.py)
from sqlalchemy import Column, String, ForeignKey, UUID
from sqlalchemy.orm import relationship
from app.db.base import BaseModel
import uuid


class Note(BaseModel):
    __tablename__ = "notes"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    content = Column(String, nullable=False)
    task_id = Column(
        UUID(as_uuid=True), ForeignKey("tasks.id", ondelete="CASCADE"), nullable=False
    )

    task = relationship("Task", back_populates="notes")
