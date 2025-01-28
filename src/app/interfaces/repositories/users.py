from abc import ABC

from app.infrastructure.repositories.redis.base import IRedisBaseRepository


class IUserRepository(IRedisBaseRepository, ABC):
    """
    User repository interface
    No specific additional methods
    """
    pass
