# app/api/v1/router/__init__.py
from fastapi import APIRouter
from app.api.v1.endpoints import (
    task_router,
    note_router,
    reminder_router,
    auth_router,
    test,
)

api_router = APIRouter()

# Include all routers
api_router.include_router(auth_router, prefix="/auth", tags=["auth"])
api_router.include_router(task_router, prefix="/tasks", tags=["tasks"])
api_router.include_router(note_router, prefix="/tasks/{task_id}/notes", tags=["notes"])
api_router.include_router(
    reminder_router, prefix="/tasks/{task_id}/reminders", tags=["reminders"]
)
api_router.include_router(test.router, prefix="/test", tags=["test"])
