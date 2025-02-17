# tests/api/test_tasks.py
import pytest
from sqlalchemy.ext.asyncio import AsyncSession
from httpx import AsyncClient
from app.models.enums import TaskStatus
from datetime import datetime, timedelta
import uuid

pytestmark = pytest.mark.asyncio


async def test_create_task(
    client: AsyncClient, db_session: AsyncSession, auth_headers: dict
):
    task_data = {
        "title": "Test Task",
        "description": "Test Description",
        "priority": 1,
        "due_date": (datetime.utcnow() + timedelta(days=1)).isoformat(),
        "status": TaskStatus.TODO.value,
    }

    response = await client.post("/api/v1/tasks/", headers=auth_headers, json=task_data)

    assert response.status_code == 200
    data = response.json()
    assert data["title"] == task_data["title"]
    assert data["description"] == task_data["description"]
    assert uuid.UUID(data["id"])  # Verify it's a valid UUID


async def test_get_task(
    client: AsyncClient, db_session: AsyncSession, auth_headers: dict, test_task: dict
):
    response = await client.get(
        f"/api/v1/tasks/{test_task['id']}", headers=auth_headers
    )

    assert response.status_code == 200
    data = response.json()
    assert data["title"] == test_task["title"]
    assert str(data["id"]) == str(test_task["id"])


async def test_get_tasks(
    client: AsyncClient, db_session: AsyncSession, auth_headers: dict, test_tasks: list
):
    response = await client.get("/api/v1/tasks/", headers=auth_headers)

    assert response.status_code == 200
    data = response.json()
    assert len(data) == len(test_tasks)
    # Verify the returned tasks match our test data
    returned_ids = {str(task["id"]) for task in data}
    test_ids = {str(task["id"]) for task in test_tasks}
    assert returned_ids == test_ids


async def test_update_task(
    client: AsyncClient, db_session: AsyncSession, auth_headers: dict, test_task: dict
):
    update_data = {"title": "Updated Task", "description": "Updated Description"}

    response = await client.put(
        f"/api/v1/tasks/{test_task['id']}", headers=auth_headers, json=update_data
    )

    assert response.status_code == 200
    data = response.json()
    assert data["title"] == update_data["title"]
    assert data["description"] == update_data["description"]
    assert str(data["id"]) == str(test_task["id"])


async def test_delete_task(
    client: AsyncClient, db_session: AsyncSession, auth_headers: dict, test_task: dict
):
    response = await client.delete(
        f"/api/v1/tasks/{test_task['id']}", headers=auth_headers
    )

    assert response.status_code == 200

    # Verify task is deleted
    get_response = await client.get(
        f"/api/v1/tasks/{test_task['id']}", headers=auth_headers
    )
    assert get_response.status_code == 404
