# app/services/task.py
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func
from datetime import datetime, timezone
from typing import List, Optional
from app.models.task import Task
from app.models.user import User
from app.schemas.task import TaskCreate, TaskUpdate
from app.core.exceptions import NotFoundError


class TaskService:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def create_task(self, task: TaskCreate, user: User) -> Task:
        """Create a new task"""
        db_task = Task(
            title=task.title,
            description=task.description,
            due_date=task.due_date,
            priority=task.priority,
            status=task.status,
            user_id=user.id,
        )
        self.db.add(db_task)
        await self.db.commit()
        await self.db.refresh(db_task)
        return db_task

    async def get_user_tasks(
        self,
        user: User,
        status: Optional[str] = None,
        priority: Optional[int] = None,
        due_date_from: Optional[datetime] = None,
        due_date_to: Optional[datetime] = None,
        skip: int = 0,
        limit: int = 100,
    ) -> List[Task]:
        """Get tasks for a user with filters"""
        query = select(Task).where(Task.user_id == user.id)

        if status:
            query = query.where(Task.status == status)
        if priority:
            query = query.where(Task.priority == priority)
        if due_date_from:
            query = query.where(Task.due_date >= due_date_from)
        if due_date_to:
            query = query.where(Task.due_date <= due_date_to)

        query = query.offset(skip).limit(limit)
        result = await self.db.execute(query)
        return result.scalars().all()

    async def get_task(self, task_id: int, user: User) -> Task:
        """Get a specific task"""
        query = select(Task).where(Task.id == task_id, Task.user_id == user.id)
        result = await self.db.execute(query)
        task = result.scalar_one_or_none()

        if task is None:
            raise NotFoundError(f"Task {task_id} not found")

        return task

    async def update_task(
        self, task_id: int, task_update: TaskUpdate, user: User
    ) -> Task:
        """Update a task"""
        task = await self.get_task(task_id, user)

        update_data = task_update.dict(exclude_unset=True)
        for field, value in update_data.items():
            setattr(task, field, value)

        await self.db.commit()
        await self.db.refresh(task)
        return task

    async def delete_task(self, task_id: int, user: User) -> None:
        """Delete a task"""
        task = await self.get_task(task_id, user)
        await self.db.delete(task)
        await self.db.commit()

    async def get_task_statistics(self, user: User) -> dict:
        """Get task statistics for a user"""
        # Total tasks
        total_query = (
            select(func.count()).select_from(Task).where(Task.user_id == user.id)
        )
        total_result = await self.db.execute(total_query)
        total_tasks = total_result.scalar()

        # Tasks by status
        status_query = (
            select(Task.status, func.count())
            .where(Task.user_id == user.id)
            .group_by(Task.status)
        )
        status_result = await self.db.execute(status_query)
        tasks_by_status = dict(status_result.all())

        # Overdue tasks
        overdue_query = (
            select(func.count())
            .select_from(Task)
            .where(
                Task.user_id == user.id,
                Task.due_date < datetime.now(timezone.utc),
                Task.status != "COMPLETED",
            )
        )
        overdue_result = await self.db.execute(overdue_query)
        overdue_tasks = overdue_result.scalar()

        return {
            "total_tasks": total_tasks,
            "tasks_by_status": tasks_by_status,
            "overdue_tasks": overdue_tasks,
        }
