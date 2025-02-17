from typing import List, Optional
from uuid import UUID
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from app.models.task import Task
from app.schemas.task import TaskCreate, TaskUpdate
from app.crud.base import CRUDBase
from app.core.exceptions import NotFoundError, PermissionError


class CRUDTask(CRUDBase[Task, TaskCreate, TaskUpdate]):
    async def create_with_user(
        self, db: AsyncSession, *, obj_in: TaskCreate, user_id: UUID
    ) -> Task:
        """Create a new task with user ownership"""
        db_obj = Task(
            title=obj_in.title,
            description=obj_in.description,
            due_date=obj_in.due_date,
            priority=obj_in.priority,
            status=obj_in.status,
            user_id=user_id,
        )
        db.add(db_obj)
        await db.commit()
        await db.refresh(db_obj)
        return db_obj

    async def get_by_user(
        self, db: AsyncSession, *, task_id: UUID, user_id: UUID
    ) -> Optional[Task]:
        """Get a task ensuring user ownership"""
        query = select(self.model).where(
            self.model.id == task_id, self.model.user_id == user_id
        )
        result = await db.execute(query)
        return result.scalar_one_or_none()

    async def get_multi_by_user(
        self,
        db: AsyncSession,
        *,
        user_id: UUID,
        skip: int = 0,
        limit: int = 100,
        status: Optional[str] = None
    ) -> List[Task]:
        """Get multiple tasks for a specific user"""
        query = select(self.model).where(self.model.user_id == user_id)

        if status:
            query = query.where(self.model.status == status)

        query = query.offset(skip).limit(limit)
        result = await db.execute(query)
        return result.scalars().all()

    async def update_by_user(
        self, db: AsyncSession, *, task_id: UUID, user_id: UUID, obj_in: TaskUpdate
    ) -> Task:
        """Update a task ensuring user ownership"""
        db_obj = await self.get_by_user(db, task_id=task_id, user_id=user_id)
        if not db_obj:
            raise NotFoundError("Task not found")

        return await super().update(db, db_obj=db_obj, obj_in=obj_in)

    async def remove_by_user(
        self, db: AsyncSession, *, task_id: UUID, user_id: UUID
    ) -> Task:
        """Delete a task ensuring user ownership"""
        db_obj = await self.get_by_user(db, task_id=task_id, user_id=user_id)
        if not db_obj:
            raise NotFoundError("Task not found")

        await db.delete(db_obj)
        await db.commit()
        return db_obj


task_crud = CRUDTask(Task)
