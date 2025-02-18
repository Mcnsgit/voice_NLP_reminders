# app/api/endpoints/voice.py
from fastapi import APIRouter, Depends, UploadFile, File
from sqlalchemy.ext.asyncio import AsyncSession
from app.services.voice_processing import VoiceService
from app.schemas.voice_input import VoiceInputResponse
from typing import List
from app.db.session import database_session
from app.core.deps import get_current_user
from app.models.user import User


router = APIRouter()


@router.post("/upload", response_model=VoiceInputResponse)
async def upload_voice(
    audio_file: UploadFile = File(...),
    db: AsyncSession = Depends(database_session.get_database_session),
    current_user: User = Depends(get_current_user),
):
    voice_service = VoiceService(db)
    return await voice_service.process_voice_input(current_user.id, audio_file)


@router.get("/", response_model=List[VoiceInputResponse])
async def get_voice_inputs(
    skip: int = 0,
    limit: int = 100,
    db: AsyncSession = Depends(database_session.async_session_maker),
    current_user: User = Depends(get_current_user),
):
    voice_service = VoiceService(db)
    return await voice_service.get_voice_inputs(current_user.id, skip, limit)
