from app.infrastructure.repositories.redis.base import RedisBaseRepository
from app.interfaces.repositories.base import MODEL
from app.interfaces.repositories.users import IUserRepository
from app.users.schemas import TokenPayload


class UserRepository(IUserRepository, RedisBaseRepository):
    _MODEL: MODEL = TokenPayload
