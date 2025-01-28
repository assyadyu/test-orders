from redis import asyncio as aioredis

from app.common import settings


def redis():
    """
    Create global redis connection
    :return: Redis connection
    """
    return aioredis.Redis(host=settings.REDIS_HOST, port=settings.REDIS_PORT)


r = redis()
