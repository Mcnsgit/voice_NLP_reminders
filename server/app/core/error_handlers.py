# app/core/error_handlers.py
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from sqlalchemy.exc import SQLAlchemyError
from app.core.exceptions import AppException
import logging

logger = logging.getLogger(__name__)


def setup_error_handlers(app: FastAPI) -> None:
    @app.exception_handler(AppException)
    async def app_exception_handler(request: Request, exc: AppException):
        logger.error(f"AppException: {exc.detail}", exc_info=True)
        return JSONResponse(status_code=exc.status_code, content={"detail": exc.detail})

    @app.exception_handler(SQLAlchemyError)
    async def sqlalchemy_exception_handler(request: Request, exc: SQLAlchemyError):
        logger.error("Database error", exc_info=True)
        return JSONResponse(
            status_code=500,
            content={"detail": "An error occurred while processing your request"},
        )

    @app.exception_handler(Exception)
    async def general_exception_handler(request: Request, exc: Exception):
        logger.error("Unhandled exception", exc_info=True)
        return JSONResponse(
            status_code=500, content={"detail": "Internal server error"}
        )
