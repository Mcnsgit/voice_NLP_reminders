# app/api/v1/endpoints/reminders.py
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List
from app.db.session import database_session
from app.schemas.reminder import ReminderCreate, ReminderUpdate, ReminderResponse
from app.models.user import User
from app.core.deps import get_current_user
from app.services.reminder_service import ReminderService

router = APIRouter()


@router.post("/", response_model=ReminderResponse)
async def create_reminder(
    reminder: ReminderCreate,
    db: AsyncSession = Depends(database_session.async_session_maker),
    current_user: User = Depends(get_current_user),
):
    """Create a new reminder"""
    reminder_service = ReminderService(db)
    return await reminder_service.create_reminder(current_user.id, reminder)


@router.get("/task/{task_id}", response_model=List[ReminderResponse])
async def get_task_reminders(
    task_id: int,
    db: AsyncSession = Depends(database_session.async_session_maker),
    current_user: User = Depends(get_current_user),
):
    """Get reminders for a specific task"""
    reminder_service = ReminderService(db)
    return await reminder_service.get_task_reminders(current_user.id, task_id)


@router.get("/upcoming", response_model=List[ReminderResponse])
async def get_upcoming_reminders(
    hours: int = 24,
    db: AsyncSession = Depends(database_session.async_session_maker),
    current_user: User = Depends(get_current_user),
):
    """Get upcoming reminders for the next N hours"""
    reminder_service = ReminderService(db)
    return await reminder_service.get_upcoming_reminders(current_user.id, hours)


@router.put("/{reminder_id}", response_model=ReminderResponse)
async def update_reminder(
    reminder_id: int,
    reminder_update: ReminderUpdate,
    db: AsyncSession = Depends(database_session.async_session_maker),
    current_user: User = Depends(get_current_user),
):
    """Update a reminder"""
    reminder_service = ReminderService(db)
    updated_reminder = await reminder_service.update_reminder(
        current_user.id, reminder_id, reminder_update
    )
    if not updated_reminder:
        raise HTTPException(status_code=404, detail="Reminder not found")
    return updated_reminder


@router.delete("/{reminder_id}")
async def delete_reminder(
    reminder_id: int,
    db: AsyncSession = Depends(database_session.async_session_maker),
    current_user: User = Depends(get_current_user),
):
    """Delete a reminder"""
    reminder_service = ReminderService(db)
    deleted = await reminder_service.delete_reminder(current_user.id, reminder_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Reminder not found")
    return {"message": "Reminder deleted successfully"}
