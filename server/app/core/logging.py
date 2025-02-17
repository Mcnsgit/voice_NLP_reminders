# server/app/core/logging.py
import logging
import sys
from pathlib import Path
from logging.handlers import RotatingFileHandler
from app.core.config import settings


def setup_logging():
    # create logs directory if it doesn't exist
    log_dir = Path("logs")
    log_dir.mkdir(exist_ok=True)

    # Configure logging format
    formatter = logging.Formatter(settings.LOG_FORMAT)

    # File handler with rotation
    file_handler = RotatingFileHandler(
        "logs/app.log", maxBytes=10485760, backupCount=5  # 10MB
    )
    file_handler.setFormatter(formatter)

    # console handler
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setFormatter(formatter)

    # setup root logger
    root_logger = logging.getLogger()
    root_logger.setLevel(settings.LOG_LEVEL)
    root_logger.addHandler(file_handler)
    root_logger.addHandler(console_handler)

    # setup specific loggers


loggers = {
    "uvicorn": settings.LOG_LEVEL,
    "fastapi": settings.LOG_LEVEL,
    "sqlalchemy": settings.LOG_LEVEL,
}

for logger_name, level in loggers.items():
    logging.getLogger(logger_name).setLevel(level)

logger = logging.getLogger(__name__)
