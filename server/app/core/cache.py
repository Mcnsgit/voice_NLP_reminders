# app/core/cache.py
from functools import wraps
from app.core.redis import get_redis
import json
import logging

logger = logging.getLogger(__name__)


def cache_response(expire: int = 300, key_prefix: str = "cache"):
    """Cache decorator for API responses"""

    def decorator(func):
        @wraps(func)
        async def wrapper(*args, **kwargs):
            # Generate cache key
            cache_key = f"{key_prefix}:{func.__name__}:{hash(str(args)+str(kwargs))}"

            # Try to get from cache
            redis = await get_redis()
            cached = await redis.get(cache_key)

            if cached:
                return json.loads(cached)

            # Execute function and cache result
            result = await func(*args, **kwargs)

            try:
                await redis.setex(cache_key, expire, json.dumps(result))
            except Exception:
                logger.error("Cache storage error", exc_info=True)

            return result

        return wrapper
