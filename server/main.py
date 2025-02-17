# main.py
from contextlib import asynccontextmanager
from fastapi import FastAPI
from app.core.config import get_settings
from app.core.middleware import setup_middleware
from app.db.session import init_db, close_db
from app.core.redis import init_redis, close_redis

from fastapi.middleware.cors import CORSMiddleware
from app.core.error_handlers import setup_error_handlers
from app.api.v1.router import api_router
from typing import Optional
import socket
import logging


settings = get_settings()
# Setup logging
logger = logging.getLogger(__name__)


def find_available_port(start_port: int, max_port: int) -> Optional[int]:
    """Find an available port in the given range."""
    for port in range(start_port, max_port + 1):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            try:
                s.bind(("", port))
                return port
            except OSError:
                continue
    return None


@asynccontextmanager
async def lifespan(app: FastAPI):
    try:
        logger.info("Starting up application...")

        # Then initialize
        await init_db()
        await init_redis()

        yield
    except Exception as e:
        logger.error(f"Error during application lifecycle: {str(e)}", exc_info=True)
        raise
    finally:
        logger.info("Shutting down application...")
        await close_redis()
        await close_db()


def create_application() -> FastAPI:
    """Create and configure the FastAPI application"""
    app = FastAPI(
        title=settings.PROJECT_NAME,
        description="Voice-enabled Task Management API",
        version="1.0.0",
        lifespan=lifespan,
    )

    # Setup error handlers

    setup_error_handlers(app)

    # Setup middleware
    setup_middleware(app)

    # Import and include routers

    app.include_router(api_router, prefix=settings.API_V1_STR)

    return app


app = create_application()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # Add your frontend origin here
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
async def root():
    return {"message": "Server on"}


@app.get("/homepage")
def homepage():
    return {"message": "welcome to the homepage"}


# @app.get("/api/user")
# def get_user(credentials:HTTPAuthorizationCredentials = Depends(security)):
#     #extract the token form the authorization header
#     token = credentials.credentials
#     user_data = {
#         token,
#     }

#     if user_data["username"] and user_data["email"]:
#         return user_data
#     raise HTTPException(status_code=401, detial="Invalid Token")


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=settings.DEBUG,
        workers=settings.WORKERS_COUNT,
    )
