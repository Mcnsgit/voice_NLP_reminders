# app/schemas/base.py
from pydantic import BaseModel, ConfigDict
from datetime import datetime


class BaseSchema(BaseModel):
    """Base schema with common configuration"""

    model_config = ConfigDict(from_attributes=True)


class TimestampedSchema(BaseSchema):
    """Base schema with timestamp fields"""

    created_at: datetime
    updated_at: datetime


# class BaseModel:
#     """Base mode with common fields"""

#     id = Column(Integer, primary_key=True, autoincrement=True)
#     created_at = Column(
#         DateTime(timezone=True), server_default=func.now(), nullable=False
#     )
#     updated_at = Column(
#         DateTime(timezone=True),
#         server_default=func.now(),
#         onupdate=func.now(),
#         nullable=False,
#     )


# Base = declarative_base(cls=BaseModel)
