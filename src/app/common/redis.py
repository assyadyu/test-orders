from functools import cache

from redis import asyncio as aioredis

from app.common import settings, logger


@cache
def redis():
    logger.warning("redis connection")
    return aioredis.Redis(host=settings.REDIS_HOST, port=settings.REDIS_PORT)


r = redis()