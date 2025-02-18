# tests/conftest.py
import pytest
import asyncio
from typing import AsyncGenerator, Dict
from httpx import AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker
from app.db.base import Base
from app.db.session import get_db
from app.models.user import User
from .utils.user import create_random_user
from .utils.auth import create_test_auth_headers
import logging
from main import app
from fastapi.testclient import TestClient

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Test database URL
TEST_DATABASE_URL = (
    "postgresql+asyncpg://taskmanager:taskmanager@localhost:5432/taskmanager_test"
)

# Create test engine
test_engine = create_async_engine(TEST_DATABASE_URL, echo=True, future=True)

# Create test session factory
TestingSessionLocal = sessionmaker(
    test_engine, class_=AsyncSession, expire_on_commit=False
)


# Override the get_db dependency for tests
async def override_get_db():
    async with TestingSessionLocal() as session:
        try:
            yield session
            await session.commit()
        except Exception:
            await session.rollback()
            raise
        finally:
            await session.close()


app.dependency_overrides[get_db] = override_get_db


@pytest.fixture(scope="session")
def event_loop():
    try:
        loop = asyncio.get_event_loop()
    except RuntimeError:
        loop = asyncio.new_event_loop()
    yield loop
    loop.close()


@pytest.fixture(autouse=True)
async def setup_db():
    """Set up a clean database for each test."""
    try:
        async with test_engine.begin() as conn:
            await conn.run_sync(Base.metadata.create_all)
        yield
    finally:
        async with test_engine.begin() as conn:
            await conn.run_sync(Base.metadata.drop_all)


@pytest.fixture
async def db_session() -> AsyncGenerator[AsyncSession, None]:
    """Create a fresh database session for a test."""
    async with TestingSessionLocal() as session:
        yield session


@pytest.fixture
async def client() -> AsyncGenerator[AsyncClient, None]:
    """Create a test client for making API requests."""
    async with AsyncClient(app=app, base_url="http://test") as ac:
        yield ac


@pytest.fixture
async def test_user(db_session: AsyncSession) -> User:
    """Create a test user."""
    return await create_random_user(db_session)


@pytest.fixture
async def auth_headers(test_user: User) -> Dict[str, str]:
    """Create authentication headers for the test user."""
    return create_test_auth_headers(test_user.id)


@pytest.fixture
async def test_task(db_session: AsyncSession, test_user: User) -> Dict:
    """Create a test task for testing."""
    from tests.utils.task import create_test_task

    task = await create_test_task(db_session, test_user.id)
    return {
        "id": task.id,
        "title": task.title,
        "description": task.description,
        "user_id": task.user_id,
        "status": task.status.value,
        "priority": task.priority,
        "due_date": task.due_date.isoformat() if task.due_date else None,
    }


@pytest.fixture
async def test_tasks(db_session: AsyncSession, test_user: User) -> list:
    """Create multiple test tasks."""
    from tests.utils.task import create_test_task

    tasks = []
    for i in range(3):
        task = await create_test_task(db_session, test_user.id, title=f"Test Task {i}")
        tasks.append(
            {
                "id": task.id,
                "title": task.title,
                "description": task.description,
                "user_id": task.user_id,
                "status": task.status.value,
                "priority": task.priority,
                "due_date": task.due_date.isoformat() if task.due_date else None,
            }
        )
    return tasks
