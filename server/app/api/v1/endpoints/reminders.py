# app/api/v1/endpoints/reminders.py
from fastapi import APIRouter, Depends, HTTPException
from typing import List
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.session import get_db
from app.models.user import User
from app.core.security import get_current_user
from app.schemas.reminder import ReminderCreate, ReminderResponse

router = APIRouter()


@router.post("/", response_model=ReminderResponse)
async def create_reminder(
    task_id: int,
    reminder: ReminderCreate,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    """Set a reminder for a task"""
    # Implementation here


@router.get("/", response_model=List[ReminderResponse])
async def get_task_reminders(
    task_id: int,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    """Get all reminders for a task"""


@router.delete("/")
async def delete_reminder(
    task_id: int,
    reminder_id: int,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    """Delete a reminder"""
