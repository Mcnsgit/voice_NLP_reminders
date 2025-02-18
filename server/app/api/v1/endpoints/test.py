# app/api/v1/endpoints/test.py
from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import text
from app.db.session import database_session

router = APIRouter()


@router.get("/test-db")
async def test_db_connection(
    db: AsyncSession = Depends(database_session.async_session_maker),
):
    """Test database connection"""
    try:
        result = await db.execute(text("SELECT 1"))
        return {"status": "ok", "message": "Database connection successful"}
    except Exception as e:
        return {"status": "error", "message": str(e)}
