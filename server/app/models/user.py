from sqlalchemy import Column, String, Boolean, Integer, DateTime, UUID
from sqlalchemy.orm import relationship
from app.db.base import BaseModel
import uuid


class User(BaseModel):
    __tablename__ = "users"

    # Change id to UUID type
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    email = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    username = Column(String)
    is_active = Column(Boolean, default=True)
    last_login = Column(DateTime(timezone=True), nullable=True)
    failed_login_attempts = Column(Integer, default=0)
    email_verified = Column(Boolean, default=False)
    password_changed_at = Column(DateTime(timezone=True), nullable=True)

    tasks = relationship("Task", back_populates="user", cascade="all, delete-orphan")


# TODO Update the User model:
# - Add last_login timestamp
#   - Add failed_login_attempts counter
#   - Add email_verified field
#   - Add password_changed_at field
