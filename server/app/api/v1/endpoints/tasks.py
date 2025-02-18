# app/api/v1/endpoints/tasks.py
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List
from app.db.session import database_session
from app.schemas.task import TaskCreate, TaskResponse, TaskUpdate, TaskDetail
from app.models.user import User
from app.core.deps import get_current_user
from app.services.task_service import TaskService

router = APIRouter()


@router.post("/", response_model=TaskResponse)
async def create_task(
    task: TaskCreate,
    db: AsyncSession = Depends(database_session.get_database_session),
    current_user: User = Depends(get_current_user),
) -> TaskResponse:
    """Create a new task"""
    task_service = TaskService(db)
    task_data = task.model_dump()
    return await task_service.create_task(current_user.id, task)


@router.get("/", response_model=List[TaskResponse])
async def get_tasks(
    skip: int = 0,
    limit: int = 100,
    db: AsyncSession = Depends(database_session.get_database_session),
    current_user: User = Depends(get_current_user),
) -> List[TaskResponse]:
    """Get user's tasks with pagination"""
    task_service = TaskService(db)
    return await task_service.get_user_tasks(current_user.id, skip, limit)


@router.get("/{task_id}", response_model=TaskDetail)
async def get_task(
    task_id: int,
    db: AsyncSession = Depends(database_session.get_database_session),
    current_user: User = Depends(get_current_user),
) -> TaskDetail:
    """Get a specific task by ID"""
    task_service = TaskService(db)
    task = await task_service.get_task(task_id, current_user.id)
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    return task


@router.put("/{task_id}", response_model=TaskResponse)
async def update_task(
    task_id: int,
    task_update: TaskUpdate,
    db: AsyncSession = Depends(database_session.get_database_session),
    current_user: User = Depends(get_current_user),
) -> TaskResponse:
    """Update a task"""
    task_service = TaskService(db)
    updated_task = await task_service.update_task(task_id, current_user.id, task_update)
    if not updated_task:
        raise HTTPException(status_code=404, detail="Task not found")
    return updated_task


@router.delete("/{task_id}")
async def delete_task(
    task_id: int,
    db: AsyncSession = Depends(database_session.get_database_session),
    current_user: User = Depends(get_current_user),
) -> dict:
    """Delete a task"""
    task_service = TaskService(db)
    deleted = await task_service.delete_task(task_id, current_user.id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Task not found")
    return {"message": "Task deleted successfully"}
