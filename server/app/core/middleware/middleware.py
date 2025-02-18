# app/core/middleware.py
from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware
from starlette.middleware.trustedhost import TrustedHostMiddleware
from starlette.middleware.gzip import GZipMiddleware
from app.core.config import get_settings
from starlette.middleware.base import BaseHTTPMiddleware
from fastapi import Request, Response
import html
import json
import logging
import secrets

settings = get_settings()
logger = logging.getLogger(__name__)


class XSSProtectionMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        try:
            # Skip XSS protection for OpenAPI endpoints
            if request.url.path in ["/openapi.json", "/docs", "/redoc"]:
                return await call_next(request)

            # Process request body if it exists
            if request.method in ["POST", "PUT", "PATCH"]:
                try:
                    body = await request.body()
                    if body:
                        try:
                            # parse and sanitize json data
                            data = json.loads(body)
                            sanitized_data = self.sanitize_data(data)
                            # override request._body with sanitized content
                            request._body = json.dumps(sanitized_data).encode()
                        except json.JSONDecodeError:
                            content = body.decode()
                            sanitized_content = html.escape(content)
                            request._body = sanitized_content.encode()
                except Exception as e:
                    logger.error(f"Error processing request body: {str(e)}")
                    pass

            response = await call_next(request)
            return response

        except Exception as e:
            logger.error(f"XSS Protection error: {str(e)}")
            return Response(
                content=json.dumps({"detail": "Internal server error"}),
                status_code=500,
                media_type="application/json",
            )

    def sanitize_data(self, data):
        """Recursively sanitize data structures"""
        if isinstance(data, dict):
            return {k: self.sanitize_data(v) for k, v in data.items()}
        elif isinstance(data, list):
            return [self.sanitize_data(item) for item in data]
        elif isinstance(data, str):
            return html.escape(data)
        return data


class RequestIDMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):

        request_id = secrets.token_hex(16)
        request.state.request_id = request_id
        response = await call_next(request)
        response.headers["X-Request-ID"] = request_id
        return response


def setup_middleware(app: FastAPI) -> None:
    """Setup all middleware for the application"""

    # Request ID
    app.add_middleware(RequestIDMiddleware)

    # security headers middleware
    @app.middleware("http")
    async def add_security_headers(request: Request, call_next):
        response = await call_next(request)
        response.headers["X-Content-Type-Options"] = "nosniff"
        response.headers["X-Frame-Options"] = "DENY"
        response.headers["X-XSS-Protection"] = "1; mode=block"
        response.headers["Strict-Transport-Security"] = "max-age=31536000"
        return response

    # XSS Protection
    app.add_middleware(XSSProtectionMiddleware)

    # Gzip compression
    app.add_middleware(GZipMiddleware, minimum_size=1000)

    # Trusted hosts
    if settings.ENVIRONMENT != "development":
        app.add_middleware(TrustedHostMiddleware, allowed_hosts=settings.ALLOWED_HOSTS)

    # CORS - add last to ensure it wraps other middleware
    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.ALLOWED_ORIGINS,
        allow_credentials=True,
        allow_methods=settings.ALLOWED_METHODS,
        allow_headers=settings.ALLOWED_HEADERS,
    )
