from datetime import datetime, timedelta, timezone
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy import and_
from typing import List, Optional
from app.models.reminder import Reminder
from app.models.task import Task
from app.schemas.reminder import ReminderCreate, ReminderUpdate
from fastapi import HTTPException
import logging

logger = logging.getLogger(__name__)


class ReminderService:
    """
    Service class for managing reminders. This class handles all business logic
    related to reminders, including creation, updates, and scheduling.
    """

    def __init__(self, session: AsyncSession):
        """Initialize the service with a database session."""
        self.session = session

    async def create_reminder(
        self, user_id: int, reminder_data: ReminderCreate
    ) -> Reminder:
        """
        Create a new reminder for a task. This method verifies task ownership
        and handles reminder creation with proper validation.
        Args:
            user_id: ID of the user creating the reminder
            reminder_data: Validated reminder creation data
        Returns:
            Newly created reminder
        Raises:
            HTTPException: If task doesn't exist or user doesn't own the task
        """
        task = await self._get_user_task(user_id, reminder_data.task_id)
        if not task:
            raise HTTPException(
                status_code=404, detail="Task not found or you don't have access to it"
            )
        try:
            reminder = Reminder(
                task_id=task.id,
                reminder_time=reminder_data.reminder_time,
                type=reminder_data.type,
                recurrence_pattern=reminder_data.recurrence_pattern,
            )
            self.session.add(reminder)
            await self.session.commit()
            await self.session.refresh(reminder)
            logger.info(
                f"Created reminder for task {task.id} at {reminder.reminder_time}"
            )
            return reminder
        except Exception as e:
            await self.session.rollback()
            logger.error(f"Error creating reminder: {str(e)}")
            raise HTTPException(status_code=500, detail="Error creating reminder")

    async def get_task_reminders(self, user_id: int, task_id: int) -> List[Reminder]:
        """
        Get all reminders for a specific task, verifying user ownership.
        Args:
            user_id: ID of the user requesting reminders
            task_id: ID of the task to get reminders for
        Returns:
            List of reminders for the task
        """
        task = await self._get_user_task(user_id, task_id)
        if not task:
            raise HTTPException(
                status_code=404, detail="Task not found or you don't have access to it"
            )
        query = select(Reminder).where(Reminder.task_id == task_id)
        result = await self.session.execute(query)
        return result.scalars().all()

    async def get_upcoming_reminders(
        self, user_id: int, hours: int = 24
    ) -> List[Reminder]:
        """
        Get upcoming reminders for a user within the specified time window.
        Args:
            user_id: ID of the user
            hours: Number of hours to look ahead (default 24)
        Returns:
            List of upcoming reminders
        """
        now = datetime.now(timezone.utc)
        end_time = now + timedelta(hours=hours)
        query = (
            select(Reminder)
            .join(Task)
            .where(
                and_(
                    Task.user_id == user_id,
                    Reminder.reminder_time >= now,
                    Reminder.reminder_time <= end_time,
                    not Reminder.is_sent,  # Changed to use `not`
                )
            )
            .order_by(Reminder.reminder_time)
        )
        result = await self.session.execute(query)
        return result.scalars().all()

    async def update_reminder(
        self, user_id: int, reminder_id: int, reminder_data: ReminderUpdate
    ) -> Optional[Reminder]:
        """
        Update an existing reminder, verifying user ownership.
        Args:
            user_id: ID of the user updating the reminder
            reminder_id: ID of the reminder to update
            reminder_data: Updated reminder data
        Returns:
            Updated reminder or None if not found
        """
        reminder = await self._get_user_reminder(user_id, reminder_id)
        if not reminder:
            return None
        try:
            for field, value in reminder_data.model_dump(exclude_unset=True).items():
                setattr(reminder, field, value)
            await self.session.commit()
            await self.session.refresh(reminder)
            logger.info(f"Updated reminder {reminder_id}")
            return reminder
        except Exception as e:
            await self.session.rollback()
            logger.error(f"Error updating reminder: {str(e)}")
            raise HTTPException(status_code=500, detail="Error updating reminder")

    async def mark_reminder_sent(self, reminder_id: int) -> bool:
        """
        Mark a reminder as sent. Used by the notification system.
        Args:
            reminder_id: ID of the reminder to mark
        Returns:
            True if reminder was marked, False if not found
        """
        reminder = await self._get_reminder(reminder_id)
        if not reminder:
            return False
        try:
            reminder.is_sent = True
            await self.session.commit()
            return True
        except Exception as e:
            await self.session.rollback()
            logger.error(f"Error marking reminder as sent: {str(e)}")
            return False

    async def delete_reminder(self, user_id: int, reminder_id: int) -> bool:
        """
        Delete a reminder, verifying user ownership.
        Args:
            user_id: ID of the user deleting the reminder
            reminder_id: ID of the reminder to delete
        Returns:
            True if reminder was deleted, False if not found
        """
        reminder = await self._get_user_reminder(user_id, reminder_id)
        if not reminder:
            return False
        try:
            await self.session.delete(reminder)
            await self.session.commit()
            logger.info(f"Deleted reminder {reminder_id}")
            return True
        except Exception as e:
            await self.session.rollback()
            logger.error(f"Error deleting reminder: {str(e)}")
            return False

    # Helper methods
    async def _get_reminder(self, reminder_id: int) -> Optional[Reminder]:
        """Get a reminder by ID."""
        query = select(Reminder).where(Reminder.id == reminder_id)
        result = await self.session.execute(query)
        return result.scalar_one_or_none()

    async def _get_user_task(self, user_id: int, task_id: int) -> Optional[Task]:
        """Get a task, verifying user ownership."""
        query = select(Task).where(and_(Task.id == task_id, Task.user_id == user_id))
        result = await self.session.execute(query)
        return result.scalar_one_or_none()

    async def _get_user_reminder(
        self, user_id: int, reminder_id: int
    ) -> Optional[Reminder]:
        """Get a reminder, verifying user ownership through task relationship."""
        query = (
            select(Reminder)
            .join(Task)
            .where(and_(Reminder.id == reminder_id, Task.user_id == user_id))
        )
        result = await self.session.execute(query)
        return result.scalar_one_or_none()
