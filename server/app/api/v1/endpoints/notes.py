# app/api/v1/endpoints/notes.py
from fastapi import APIRouter, Depends, HTTPException
from typing import List
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.session import database_session
from app.models.user import User
from app.core.security import get_current_user
from app.schemas.note import NoteCreate, NoteResponse

router = APIRouter()


@router.post("/", response_model=NoteResponse)
async def create_note(
    task_id: int,
    note: NoteCreate,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(database_session.get_database_session),
):
    """Add a note to a task"""
    # Implementation here


@router.get("/")
async def get_task_notes(
    task_id: int,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(database_session.get_database_session),
):
    """Get all notes for a task"""


@router.delete("/")
async def delete_note(
    task_id: int,
    note_id: int,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(database_session.get_database_session),
):
    """Delete a note"""
