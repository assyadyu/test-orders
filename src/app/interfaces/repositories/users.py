from abc import ABC

from app.interfaces.repositories.base import IBaseRepository


class IUserRepository(IBaseRepository, ABC):
    pass
