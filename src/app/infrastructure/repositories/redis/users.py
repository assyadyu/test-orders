from app.infrastructure.repositories.redis.base import RedisBaseRepository
from app.interfaces.repositories.base import MODEL
from app.interfaces.repositories.users import IUserRepository
from app.users.schemas import TokenPayload


class UserRepository(IUserRepository, RedisBaseRepository):
    """
    User repository implementation that uses Redis implementation
    No specific additional methods
    """
    _MODEL: MODEL = TokenPayload
