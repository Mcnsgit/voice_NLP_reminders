# app/api/endpoints/health.py
from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.session import database_session
from app.core.config import settings
import time

router = APIRouter()


@router.get("/health")
async def health_check(
    session: AsyncSession = Depends(database_session.async_session_maker),
):
    """
    Health check endpoint that verifies:
    - Database connection
    - Application status
    - Response time
    """
    start_time = time.time()
    # Check database connection
    db_status = await database_session.database_url()
    response_time = (time.time() - start_time) * 1000  # Convert to milliseconds
    return {
        "status": "healthy" if db_status else "unhealthy",
        "environment": settings.ENVIRONMENT,
        "database": {
            "status": "connected" if db_status else "disconnected",
            "host": settings.DB_HOST,
            "name": settings.DB_NAME,
        },
        "response_time_ms": round(response_time, 2),
        "version": settings.PROJECT_NAME,
    }


@router.get("/health/db", include_in_schema=settings.DEBUG)
async def database_health(
    session: AsyncSession = Depends(database_session.async_session_maker),
):
    """Detailed database health check (only available in debug mode)"""
    if not settings.DEBUG:
        return {"message": "Endpoint not available in production"}
    try:
        # Get database statistics
        async with session.begin():
            result = await session.execute(
                """
                SELECT 
                    sum(n_live_tup) as row_count,
                    sum(n_dead_tup) as dead_rows,
                    sum(pg_total_relation_size(schemaname || '.' || tablename)) as total_size
                FROM pg_stat_user_tables
                """
            )
            stats = result.first()
            return {
                "status": "healthy",
                "statistics": {
                    "total_rows": stats[0] if stats else 0,
                    "dead_rows": stats[1] if stats else 0,
                    "total_size_bytes": stats[2] if stats else 0,
                },
                "connection_info": {
                    "host": settings.DB_HOST,
                    "database": settings.DB_NAME,
                    "port": settings.DB_PORT,
                },
            }
    except Exception as e:
        return {
            "status": "unhealthy",
            "error": str(e),
            "connection_info": {
                "host": settings.DB_HOST,
                "database": settings.DB_NAME,
                "port": settings.DB_PORT,
            },
        }
