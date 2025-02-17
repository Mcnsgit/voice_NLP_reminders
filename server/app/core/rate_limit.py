# app/core/rate_limit.py
from fastapi import Request
from fastapi.responses import JSONResponse
import redis.asyncio as redis
from app.core.config import Settings
import logging
from starlette.middleware.base import BaseHTTPMiddleware

logger = logging.getLogger(__name__)


class RateLimitMiddleware(BaseHTTPMiddleware):
    def __init__(self, app, calls: int = 60, period: int = 60):
        super().__init__(app)
        self.calls = calls
        self.period = period
        self.redis = None

    async def get_redis(self):
        if self.redis is None:
            try:
                self.redis = redis.from_url(
                    f"redis://{Settings.REDIS_HOST}:{Settings.REDIS_PORT}",
                    encoding="utf-8",
                    decode_responses=True,
                    socket_timeout=1,
                    socket_connect_timeout=1,
                )
                # Test the connection
                await self.redis.ping()
            except Exception as e:
                logger.warning(f"Redis connection failed: {str(e)}")
                self.redis = None
        return self.redis

    async def dispatch(self, request: Request, call_next):
        try:
            redis_client = await self.get_redis()

            if redis_client:
                # Rate limiting logic
                client_ip = request.client.host
                key = f"rate_limit:{client_ip}"

                try:
                    current = await redis_client.get(key)

                    if current and int(current) > self.calls:
                        return JSONResponse(
                            status_code=429, content={"detail": "Too many requests"}
                        )

                    pipe = redis_client.pipeline()
                    await pipe.incr(key)
                    await pipe.expire(key, self.period)
                    await pipe.execute()

                except Exception as e:
                    logger.error(f"Rate limit error: {str(e)}")
                    # Continue without rate limiting if Redis fails

            response = await call_next(request)
            return response

        except Exception as e:
            logger.error(f"Middleware error: {str(e)}")
            return await call_next(request)
