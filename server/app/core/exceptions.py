# app/core/exceptions.py
from fastapi import HTTPException
from typing import Any, Dict, Optional


class AppException(HTTPException):
    def __init__(
        self,
        status_code: int,
        detail: Any = None,
        headers: Optional[Dict[str, str]] = None,
    ) -> None:
        super().__init__(status_code=status_code, detail=detail, headers=headers)


class DatabaseError(AppException):
    def __init__(self, detail: str = "Database error occurred"):
        super().__init__(status_code=500, detail=detail)


class NotFoundError(AppException):
    def __init__(self, detail: str = "Resource not found"):
        super().__init__(status_code=404, detail=detail)


class ValidationError(AppException):
    def __init__(self, detail: str = "Validation error"):
        super().__init__(status_code=422, detail=detail)


class AuthenticationError(AppException):
    def __init__(self, detail: str = "Authentication failed"):
        super().__init__(
            status_code=401, detail=detail, headers={"WWW-Authenticate": "Bearer"}
        )


class PermissionError(AppException):
    def __init__(
        self, detail: str = "You don't have permssion to do complete this action"
    ):
        super().__init__(status_code=403, detail=detail)
