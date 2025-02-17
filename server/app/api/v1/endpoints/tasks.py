from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List, Optional
from uuid import UUID
from app.db.session import get_db
from app.models.user import User
from app.core.security import get_current_user
from app.schemas.task import TaskCreate, TaskUpdate, TaskResponse
from app.crud.task import task_crud
from app.core.dev_auth import use_dev_auth
from app.models.enums import TaskStatus

router = APIRouter()

current_user = use_dev_auth()


@router.post("/", response_model=TaskResponse)
async def create_task(
    task_in: TaskCreate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(current_user),
):
    """Create a new task"""
    try:
        task = await task_crud.create_with_user(
            db=db, obj_in=task_in, user_id=current_user.id
        )
        return task
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Could not create task: {str(e)}")


@router.get("/{task_id}", response_model=TaskResponse)
async def get_task(
    task_id: UUID,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(current_user),
):
    """Get a specific task"""
    task = await task_crud.get_by_user(db=db, task_id=task_id, user_id=current_user.id)
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    return task


@router.get("/", response_model=List[TaskResponse])
async def get_tasks(
    skip: int = 0,
    limit: int = 100,
    status: Optional[TaskStatus] = None,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(current_user),
):
    """Get all tasks for the current user"""
    tasks = await task_crud.get_multi_by_user(
        db=db,
        user_id=current_user.id,
        skip=skip,
        limit=limit,
        status=status.value if status else None,
    )
    return tasks


@router.put("/{task_id}", response_model=TaskResponse)
async def update_task(
    task_id: UUID,
    task_in: TaskUpdate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(current_user),
):
    """Update a task"""
    try:
        task = await task_crud.update_by_user(
            db=db, task_id=task_id, user_id=current_user.id, obj_in=task_in
        )
        return task
    except Exception as e:
        raise HTTPException(status_code=404, detail=f"Could not update task: {str(e)}")


@router.delete("/{task_id}")
async def delete_task(
    task_id: UUID,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(current_user),
):
    """Delete a task"""
    try:
        await task_crud.remove_by_user(db=db, task_id=task_id, user_id=current_user.id)
        return {"message": "Task deleted successfully"}
    except Exception as e:
        raise HTTPException(status_code=404, detail=f"Could not delete task: {str(e)}")


# @router.get("/", response_model=List[TaskResponse])
# async def get_tasks(
#     status: Optional[str] = Query(None, enum=[s.value for s in TaskStatus]),
#     priority: Optional[int] = Query(None, ge=1, le=5),
#     due_date_from: Optional[datetime] = None,
#     due_date_to: Optional[datetime] = None,
#     skip: int = 0,
#     limit: int = 100,
#     current_user: User = Depends(current_user),
#     db: AsyncSession = Depends(get_db),
# ):
#     """Get list of tasks with filtering options"""
#     query = select(Task).where(Task.user_id == current_user.id)

#     if status:
#         query = query.where(Task.status == status)
#     if priority:
#         query = query.where(Task.priority == priority)
#     if due_date_from:
#         query = query.where(Task.due_date >= due_date_from)
#     if due_date_to:
#         query = query.where(Task.due_date <= due_date_to)

#     query = query.offset(skip).limit(limit)
#     result = await db.execute(query)
#     return result.scalars().all()


# @router.get("/{task_id}", response_model=TaskDetailResponse)
# async def get_task(
#     task_id: int,
#     current_user: User = Depends(current_user),
#     db: AsyncSession = Depends(get_db),
# ):
#     """Get detailed task information"""
#     query = select(Task).where(Task.id == task_id, Task.user_id == current_user.id)
#     result = await db.execute(query)
#     task = result.scalar_one_or_none()

#     if task is None:
#         raise HTTPException(status_code=404, detail="Task not found")

#     return task


# @router.put("/{task_id}", response_model=TaskResponse)
# async def update_task(
#     task_id: int,
#     task_update: TaskUpdate,
#     current_user: User = Depends(current_user),
#     db: AsyncSession = Depends(get_db),
# ):
#     """Update task details"""
#     query = select(Task).where(Task.id == task_id, Task.user_id == current_user.id)
#     result = await db.execute(query)
#     task = result.scalar_one_or_none()

#     if task is None:
#         raise HTTPException(status_code=404, detail="Task not found")

#     update_data = task_update.dict(exclude_unset=True)
#     for field, value in update_data.items():
#         setattr(task, field, value)

#     await db.commit()
#     await db.refresh(task)
#     return task


# @router.delete("/{task_id}")
# async def delete_task(
#     task_id: int,
#     current_user: User = Depends(current_user),
#     db: AsyncSession = Depends(get_db),
# ):
#     """Delete a task"""
#     query = select(Task).where(Task.id == task_id, Task.user_id == current_user.id)
#     result = await db.execute(query)
#     task = result.scalar_one_or_none()

#     if task is None:
#         raise HTTPException(status_code=404, detail="Task not found")

#     await db.delete(task)
#     await db.commit()
#     return {"message": "Task deleted successfully"}
