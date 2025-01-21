from redis import asyncio as aioredis

from app.common import settings

r = aioredis.Redis(host=settings.REDIS_HOST, port=settings.REDIS_PORT)
