# main.py
from contextlib import asynccontextmanager
from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware
from app.core.config import get_settings
from app.core.middleware import setup_middleware
from app.db.session import database_session
from app.core.redis import init_redis, close_redis
from app.core.error_handlers import setup_error_handlers
from app.api.v1.router import api_router
from app.schemas.user import UserCreate, UserRead, UserUpdate
from app.core.security import get_current_active_user
from app.models.user import User
import logging

settings = get_settings()

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifecycle manager"""
    try:
        logger.info("Starting up application...")
        await database_session.init_db()
        await init_redis()
        yield
    except Exception as e:
        logger.error(f"Error during startup: {str(e)}", exc_info=True)
        raise
    finally:
        logger.info("Shutting down application...")
        await close_redis()
        await database_session.close_db()


def create_application() -> FastAPI:
    """Create and configure the FastAPI application"""
    app = FastAPI(
        title=settings.PROJECT_NAME,
        description="Voice-enabled Task Management API",
        version="1.0.0",
        lifespan=lifespan,
    )

    # CORS middleware
    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.ALLOWED_ORIGINS,  # Changed from CORS_ORIGINS to ALLOWED_ORIGINS
        allow_credentials=True,
        allow_methods=settings.ALLOWED_METHODS,
        allow_headers=settings.ALLOWED_HEADERS,
    )

    # Setup handlers and middleware
    setup_error_handlers(app)
    setup_middleware(app)

    # Include API routers
    app.include_router(api_router, prefix="/api/v1")

    @app.get("/health")
    async def health_check():
        """Health check endpoint"""
        return {
            "status": "healthy",
            "version": settings.VERSION,
            "environment": settings.ENVIRONMENT,
        }

    @app.get("/authenticated-route")
    async def authenticated_route(user: User = Depends(get_current_active_user)):
        return {"message": f"Hello {user.email}!"}

    return app


# Create application instance
app = create_application()

if __name__ == "__main__":
    import uvicorn

    uvicorn.run(
        "main:app",
        host=settings.HOST,
        port=settings.PORT,
        reload=settings.DEBUG,
        workers=settings.WORKERS_COUNT,
    )
