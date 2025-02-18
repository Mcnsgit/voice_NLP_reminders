from typing import Optional, Dict
from .base import BaseSchema, TimestampedSchema
from app.models.enums import VoiceInputStatus


class VoiceInputBase(BaseSchema):
    """Base Voice Input Schema"""

    raw_text: str
    processed_text: Optional[str] = None
    status: VoiceInputStatus = VoiceInputStatus.PENDING
    confidence_score: Optional[float] = None
    metadata: Optional[Dict] = None
    error_message: Optional[str] = None


class VoiceInputCreate(VoiceInputBase):
    """Schema for creating a new voice input"""

    user_id: int


class VoiceInputUpdate(BaseSchema):
    """Schema for updating a voice input"""

    processed_text: Optional[str] = None
    status: Optional[VoiceInputStatus] = None
    confidence_score: Optional[float] = None
    processing_metadata: Optional[Dict] = None  # Updated to match model
    error_message: Optional[str] = None


class VoiceInputResponse(VoiceInputBase, TimestampedSchema):
    """Schema for voice input response"""

    id: int
    user_id: int
    associated_task_id: Optional[int] = None
