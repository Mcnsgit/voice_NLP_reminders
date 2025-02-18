# app/repositories/voice_input.py
from sqlalchemy import select
from typing import List
from app.models.voice_input import VoiceInput
from .base import BaseRepository


class VoiceInputRepository(BaseRepository[VoiceInput]):
    async def get_user_inputs(
        self, user_id: int, skip: int = 0, limit: int = 100
    ) -> List[VoiceInput]:
        query = (
            select(self.model)
            .where(self.model.user_id == user_id)
            .order_by(self.model.created_at.desc())
            .offset(skip)
            .limit(limit)
        )
        result = await self.session.execute(query)
        return result.scalars().all()
