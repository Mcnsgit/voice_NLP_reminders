# app/tests/utils/task.py
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.task import Task
from app.models.enums import TaskStatus
from datetime import datetime, timedelta


async def create_test_task(
    db: AsyncSession, user_id: int, title: str = "Test Task"
) -> Task:
    """Create a test task for a given user."""
    task = Task(
        title=title,
        description="Test Description",
        user_id=user_id,
        status=TaskStatus.TODO,
        priority=1,
        due_date=datetime.utcnow() + timedelta(days=1),
    )
    db.add(task)
    await db.commit()
    await db.refresh(task)
    return task
