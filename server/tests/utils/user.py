# app/tests/utils/user.py
import uuid
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.user import User
from app.core.security import get_password_hash


async def create_random_user(db: AsyncSession) -> User:
    """Create a random user for testing."""
    unique_id = uuid.uuid4()
    user = User(
        id=uuid.uuid4(),
        email=f"test_{unique_id}@example.com",
        hashed_password=get_password_hash("testpassword"),
        is_active=True,
        username=f"testuser_{unique_id}",
    )
    db.add(user)
    await db.commit()
    await db.refresh(user)
    return user
