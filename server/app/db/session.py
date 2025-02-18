from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from typing import AsyncGenerator
import logging
from app.core.config import settings

logger = logging.getLogger(__name__)


class DatabaseSession:
    def __init__(self):
        self.database_url = settings.get_database_url
        logger.info("Initializing database connection")

        engine_kwargs = {
            "echo": settings.DB_ECHO,
            "future": True,
            "pool_pre_ping": True,
            "pool_size": settings.DB_POOL_SIZE,
            "max_overflow": settings.DB_MAX_OVERFLOW,
        }
        self.engine = create_async_engine(self.database_url, **engine_kwargs)

        self.async_session_maker = sessionmaker(
            self.engine,
            class_=AsyncSession,
            expire_on_commit=False,
        )

    async def get_database_session(self) -> AsyncGenerator[AsyncSession, None]:
        """Dependency for getting async database session"""
        async with self.async_session_maker() as session:
            try:
                yield session
                await session.commit()
            except Exception as e:
                logger.error(
                    f"Database session error: {str(e)}", exc_info=settings.DEBUG
                )
                await session.rollback()
                raise

    async def init_db(self) -> None:
        """Initialize database"""
        try:
            async with self.engine.begin() as conn:
                from app.db.base import Base

                await conn.run_sync(Base.metadata.create_all)
                logger.info("Database initialized successfully")
        except Exception as e:
            logger.error(f"Database initialization error: {e}", exc_info=settings.DEBUG)
            raise

    async def close_db(self) -> None:
        """Close database connection"""
        try:
            await self.engine.dispose()
            logger.info("Database connection closed")
        except Exception as e:
            logger.error(
                f"Error closing database connection: {e}", exc_info=settings.DEBUG
            )
            raise


# Create an instance of DatabaseSession to use in your application
database_session = DatabaseSession()
