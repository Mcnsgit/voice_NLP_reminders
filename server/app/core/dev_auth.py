# app/core/dev_auth.py
from app.models.user import User
from app.core.config import get_settings

settings = get_settings()


async def get_dev_user() -> User:
    """Development only: Returns a mock user for testing"""
    return User(
        id=1,  # Using integer ID
        email="dev@example.com",
        is_active=True,
        hashed_password="mock_hash",
    )


def use_dev_auth():
    """Switch between dev and production auth"""
    if settings.ENVIRONMENT == "development":
        return get_dev_user
    else:
        from app.core.security import get_current_user

        return get_current_user
