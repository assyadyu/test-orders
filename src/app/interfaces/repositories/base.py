from abc import abstractmethod, ABC
from typing import Any, TypeVar

from pydantic import BaseModel, UUID4

MODEL = TypeVar("MODEL")
KEY = TypeVar("KEY")


class IBaseRepository(ABC):

    @abstractmethod
    async def create(self, *, obj: MODEL) -> MODEL:
        raise NotImplementedError

    @abstractmethod
    async def create_from_data(self, data: BaseModel) -> MODEL:
        raise NotImplementedError

    @abstractmethod
    async def get_by_id(self, *, object_id: UUID4) -> MODEL:
        raise NotImplementedError

    @abstractmethod
    async def update(self, *, object_id: UUID4, **values: Any) -> MODEL:
        raise NotImplementedError
