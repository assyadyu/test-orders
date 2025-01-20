from abc import abstractmethod, ABC
from typing import Any, TypeVar

from uuid import UUID

MODEL = TypeVar("MODEL")
KEY = TypeVar("KEY")


class IBaseRepository(ABC):

    @abstractmethod
    async def create(self, obj: MODEL) -> MODEL:
        raise NotImplementedError

    @abstractmethod
    async def get_by_id(self, object_id: UUID) -> MODEL:
        raise NotImplementedError

    @abstractmethod
    async def update(self, object_id: UUID, **values: Any) -> MODEL:
        raise NotImplementedError
