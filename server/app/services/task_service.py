# app/services/task_service.py
from fastapi import HTTPException
from app.repositories.task import TaskRepository
from sqlalchemy.ext.asyncio import AsyncSession
from app.schemas.task import TaskCreate, TaskUpdate
from typing import List, Optional
from app.models.task import Task


class TaskService:
    def __init__(self, session: AsyncSession):
        self.repository = TaskRepository(Task, session)
        self.session = session

    async def create_task(self, user_id: int, task_data: TaskCreate) -> Task:
        try:
            db_task = await self.repository.create(
                user_id=user_id, **task_data.model_dump(exclude={"voice_input_id"})
            )
            return db_task
        except Exception as e:
            await self.session.rollback()
            raise HTTPException(status_code=500, detail=str(e))

    async def get_task(self, task_id: int, user_id: int) -> Optional[Task]:
        task = await self.repository.get_task_with_relations(task_id, user_id)
        return task

    async def delete_task(self, task_id: int, user_id: int) -> bool:
        # First verify task belongs to user
        task = await self.repository.get_task_with_relations(task_id, user_id)
        if not task:
            return False
        return await self.repository.delete(task_id)

    async def update_task(
        self, task_id: int, user_id: int, task_data: TaskUpdate
    ) -> Optional[Task]:
        # Verify task belongs to user
        task = await self.repository.get(task_id)
        if not task or task.user_id != user_id:
            return None

        update_data = task_data.model_dump(exclude_unset=True)
        return await self.repository.update(task_id, **update_data)


#
