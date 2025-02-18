# app/repositories/task.py
from sqlalchemy import select, and_
from datetime import datetime
from app.models.task import Task
from app.models.enums import TaskStatus
from .base import BaseRepository
from typing import List, Optional


# Fix task repository
class TaskRepository(BaseRepository[Task]):
    async def get_user_tasks(
        self, user_id: int, skip: int = 0, limit: int = 100
    ) -> List[Task]:
        query = (
            select(self.model)
            .where(self.model.user_id == user_id)
            .order_by(self.model.created_at.desc())
            .offset(skip)
            .limit(limit)
        )
        result = await self.session.execute(query)
        return result.scalars().all()

    async def get_task_with_relations(
        self, task_id: int, user_id: int
    ) -> Optional[Task]:
        query = select(self.model).where(
            and_(self.model.id == task_id, self.model.user_id == user_id)
        )
        result = await self.session.execute(query)
        return result.scalar_one_or_none()
