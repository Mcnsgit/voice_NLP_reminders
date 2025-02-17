# app/core/redis.py
import redis.asyncio as redis
from app.core.config import settings

redis_client = None


async def init_redis():
    global redis_client
    redis_client = redis.from_url(
        f"redis://{settings.REDIS_HOST}:{settings.REDIS_PORT}",
        encoding="utf-8",
        decode_responses=True,
    )
    return redis_client


async def get_redis():
    if redis_client is None:
        await init_redis()
    return redis_client


async def close_redis():
    if redis_client is not None:
        await redis_client.close()
