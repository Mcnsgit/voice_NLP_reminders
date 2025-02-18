# app/api/v1/router.py
from fastapi import APIRouter
from app.api.v1.endpoints import (
    tasks,
    reminders,
    voice,
    health,
    # auth,
)

api_router = APIRouter()

# Health check endpoints
api_router.include_router(health.router, prefix="/health", tags=["health"])

# Authentication endpoints
# api_router.include_router(auth.router, prefix="/auth", tags=["auth"])

# Task management endpoints
api_router.include_router(tasks.router, prefix="/tasks", tags=["tasks"])

# Reminder endpoints
api_router.include_router(reminders.router, prefix="/reminders", tags=["reminders"])

# Voice processing endpoints
api_router.include_router(voice.router, prefix="/voice", tags=["voice"])
