# app/core/deps.py
from typing import AsyncGenerator, Annotated
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.session import database_session
from app.models.user import User
from app.core.security import get_current_active_user

# from app.schemas.task import TaskResponse
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="api/v1/auth/jwt/login")

decode_access_token = get_current_active_user()


async def get_db() -> AsyncGenerator[AsyncSession, None]:
    """Get database session"""
    async with database_session.async_session_maker() as session:
        try:
            yield session
            await session.commit()
        except Exception:
            await session.rollback()
            raise
        finally:
            await session.close()


async def get_current_user(
    db: AsyncSession = Depends(get_db), token: str = Depends(oauth2_scheme)
) -> User:
    """Get current authenticated user"""
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )

    try:
        user_id = decode_access_token(token)
        if user_id is None:
            raise credentials_exception
    except Exception:
        raise credentials_exception

    query = await db.get(User, user_id)
    user = await query.fetchone()

    if user is None:
        raise credentials_exception

    return user


# Type annotations for dependency injection
DBDependency = Annotated[AsyncSession, Depends(get_db)]
CurrentUser = Annotated[User, Depends(get_current_user)]
