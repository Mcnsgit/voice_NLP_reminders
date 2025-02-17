from typing import Any
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.ext.declarative import declared_attr


class Base(DeclarativeBase):
    """Base class for all models"""

    @declared_attr
    def __tablename__(cls) -> str:
        return cls.__name__.lower()
