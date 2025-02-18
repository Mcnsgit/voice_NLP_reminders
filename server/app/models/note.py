# 4. Update Note model (app/models/note.py)
from sqlalchemy import Column, String, ForeignKey, Integer
from sqlalchemy.orm import relationship
from app.db.base_class import Base


class Note(Base):
    __tablename__ = "notes"

    content = Column(String, nullable=False)
    task_id = Column(
        Integer, ForeignKey("tasks.id", ondelete="CASCADE"), nullable=False
    )

    task = relationship("Task", back_populates="notes")
