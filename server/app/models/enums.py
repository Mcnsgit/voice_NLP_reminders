# app/models/enums.py
from enum import Enum


class TaskStatus(str, Enum):
    """Task status enumeration"""

    TODO = "TODO"
    IN_PROGRESS = "IN_PROGRESS"
    COMPLETED = "COMPLETED"
    ARCHIVED = "ARCHIVED"


class VoiceInputStatus(str, Enum):
    """Voice input processing status"""

    PENDING = "PENDING"
    PROCESSING = "PROCESSING"
    COMPLETED = "COMPLETED"
    FAILED = "FAILED"


class ReminderType(str, Enum):
    """Reminder type enumeration"""

    ONE_TIME = "ONE_TIME"
    RECURRING = "RECURRING"
    LOCATION_BASED = "LOCATION_BASED"
