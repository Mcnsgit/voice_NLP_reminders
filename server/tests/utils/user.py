# app/tests/utils/user.py
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.user import User
from app.core.security import get_password_hash


async def create_random_user(db: AsyncSession) -> User:
    """Create a random user for testing."""
    user = User(
        email="test@example.com",
        hashed_password=get_password_hash("testpassword"),
        is_active=True,
        username="testuser",
    )
    db.add(user)
    await db.commit()
    await db.refresh(user)
    return user
