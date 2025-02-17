from enum import Enum


class TaskStatus(str, Enum):
    """Task status enumeration"""

    TODO = "TODO"
    IN_PROGRESS = "IN_PROGRESS"
    COMPLETED = "COMPLETED"
