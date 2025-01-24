from abc import ABC

from app.infrastructure.repositories.redis.base import IRedisBaseRepository


class IUserRepository(IRedisBaseRepository, ABC):
    pass
