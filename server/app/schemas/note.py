# app/schemas/note.py
from datetime import datetime
from typing import Optional
from pydantic import BaseModel, Field


class NoteBase(BaseModel):
    content: str = Field(..., min_length=1)
    task_id: int


class NoteCreate(NoteBase):
    pass


class NoteUpdate(BaseModel):
    content: str = Field(..., min_length=1)


class NoteInDB(NoteBase):
    id: int
    created_at: datetime

    class Config:
        from_attributes = True


class NoteResponse(NoteInDB):
    pass
