# app/models/voice_input.py
from sqlalchemy import (
    Column,
    String,
    ForeignKey,
    Text,
    Integer,
    Enum as SQLEnum,
    JSON,
    Float,
)
from sqlalchemy.orm import relationship
from app.db.base_class import Base
from .enums import VoiceInputStatus


class VoiceInput(Base):
    __tablename__ = "voice_inputs"

    user_id = Column(
        Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True
    )
    raw_text = Column(
        Text, nullable=True
    )  # Changed to nullable since we might process audio first
    processed_text = Column(Text, nullable=True)
    status = Column(
        SQLEnum(VoiceInputStatus),
        default=VoiceInputStatus.PENDING,
        nullable=False,
        index=True,
    )
    confidence_score = Column(Float, nullable=True)
    processing_metadata = Column(JSON, nullable=True, default={})
    error_message = Column(String(500), nullable=True)

    # Relationships
    user = relationship("User", back_populates="voice_inputs")
    task = relationship(
        "Task", back_populates="voice_input", uselist=False, passive_deletes=True
    )
