# app/models/user.py
from sqlalchemy import Boolean, Column, String
from sqlalchemy.orm import relationship
from app.db.base_class import Base


class User(Base):
    __tablename__ = "users"

    email = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    is_active = Column(Boolean, default=True, nullable=False)

    # Relationships
    tasks = relationship("Task", back_populates="user", cascade="all, delete-orphan")
    voice_inputs = relationship(
        "VoiceInput", back_populates="user", cascade="all, delete-orphan"
    )
