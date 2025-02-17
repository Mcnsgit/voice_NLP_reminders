# app/api/v1/endpoints/__init__.py
from .tasks import router as task_router
from .notes import router as note_router
from .reminders import router as reminder_router
from .auth import router as auth_router

__all__ = ["task_router", "note_router", "reminder_router", "auth_router"]
