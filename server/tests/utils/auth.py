# app/tests/utils/auth.py
from typing import Dict
from datetime import timedelta
from app.core.security import create_access_token
from app.core.config import settings


def create_test_auth_headers(user_id: int) -> Dict[str, str]:
    """Create authentication headers for testing."""
    access_token = create_access_token(
        data={"sub": str(user_id)},
        expires_delta=timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES),
    )
    return {"Authorization": f"Bearer {access_token}"}
