# app/db/session.py
# app/db/session.py
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from app.core.config import settings
import logging
from urllib.parse import quote_plus

logger = logging.getLogger(__name__)


def get_database_url() -> str:
    """Get the database URL based on the environment."""
    if settings.ENVIRONMENT == "test":
        return "sqlite+aiosqlite:///./test.db"
    elif settings.ENVIRONMENT == "development":
        # Convert psycopg2 URL to asyncpg URL
        postgres_url = f"postgresql+asyncpg://{settings.DB_USER}:{quote_plus(settings.DB_PASSWORD)}@{settings.DB_HOST}:{settings.DB_PORT}/{settings.DB_NAME}"
        return postgres_url
    else:
        # Production environment - use Neon DB URL with asyncpg
        if not settings.NEON_DB_URL:
            raise ValueError("NEON_DB_URL must be set in production")
        return settings.NEON_DB_URL.replace("postgresql://", "postgresql+asyncpg://")


# Create async engine with the appropriate URL
database_url = get_database_url()
engine_kwargs = {
    "echo": settings.DEBUG,
    "future": True,
    "pool_pre_ping": True,
}

if "sqlite" in database_url:
    engine_kwargs["connect_args"] = {"check_same_thread": False}

engine = create_async_engine(database_url, **engine_kwargs)

# Create async session factory
AsyncSessionLocal = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)


async def init_db():
    """Initialize database"""
    try:
        async with engine.begin() as conn:
            # Import Base here to avoid circular imports
            from app.db.base_class import Base

            await conn.run_sync(Base.metadata.create_all)
        logger.info("Database initialized successfully")
    except Exception as e:
        logger.error(f"Database initialization error: {e}")
        raise


async def close_db():
    """Close database connection"""
    try:
        await engine.dispose()
        logger.info("Database connection closed")
    except Exception as e:
        logger.error(f"Error closing database connection: {e}")
        raise


async def get_db():
    """Dependency for getting async database session"""
    async with AsyncSessionLocal() as session:
        try:
            yield session
            await session.commit()
        except Exception as e:
            await session.rollback()
            logger.error(f"Database session error: {str(e)}", exc_info=True)
            raise
        finally:
            await session.close()


# async def cleanup_db():
#     """Drop all tables - use with caution!"""
#     try:
#         async with engine.begin() as conn:
#             from app.db.base_class import Base

#             await conn.run_sync(Base.metadata.drop_all)
#         logger.info("Database cleaned successfully")
#     except Exception as e:
#         logger.error(f"Database cleanup error: {e}")
#         raise


# from sqlalchemy import create_engine
# from sqlalchemy.orm import sessionmaker

# from app.core.config import Settings

# import logging


# logger = logging.getLogger(__name__)
# SQLALCHEMY_DATABASE_URL = Settings.DATABASE_URL
# print("Database url is ", SQLALCHEMY_DATABASE_URL)
# # Create async engine
# engine = create_engine(SQLALCHEMY_DATABASE_URL)
# # if you don't want to install postgres or any database, use sqlite, a file system based database,
# # uncomment below lines if you would like to use sqlite and comment above 2 lines of SQLALCHEMY_DATABASE_URL AND engine

# # SQLALCHEMY_DATABASE_URL = "sqlite:///./sql_app.db"
# # engine = create_engine(
# #     SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
# # )

# SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


# async def init_db():
#     """Initialize database connection"""
#     try:
#         async with engine.begin() as conn:
#             await conn.run_sync(lambda _: logger.info("Database connection successful"))
#     except Exception as e:
#         logger.error(f"Database initialization error: {e}")
#         raise


# async def close_db():
#     """Close database connection"""
#     try:
#         await engine.dispose()
#         logger.info("Database connection closed")
#     except Exception as e:
#         logger.error(f"Error closing database connection: {e}")
#         raise


# async def get_db():
#     """Dependency for getting async database session"""
#     async with SessionLocal() as session:
#         try:
#             yield session
#             await session.commit()
#         except Exception as e:
#             await session.rollback()
#             logger.error(f"Database session error: {str(e)}", exc_info=True)
#             raise
#         finally:
#             await session.close()
