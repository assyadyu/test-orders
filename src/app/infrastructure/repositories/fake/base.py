from typing import Any, TypeVar, Union
from uuid import UUID, uuid4

from app.common.exceptions import ObjectDoesNotExistException
from app.interfaces.repositories.base import IBaseRepository

MODEL = TypeVar("MODEL")
KEY = TypeVar("KEY")


class FakeBaseRepository(IBaseRepository):
    _MODEL: MODEL
    objects: list[MODEL] = []

    async def set_model(self, model: MODEL) -> None:
        self._MODEL = model

    async def create(self, obj: MODEL, **kwargs) -> Union[MODEL, None]:
        obj.uuid = uuid4()
        self.objects.append(obj)
        return obj

    async def get_by_id(self, object_id: UUID) -> MODEL:
        exist = [obj for obj in self.objects if obj.uuid == object_id]
        if exist:
            return exist[0]
        else:
            raise ObjectDoesNotExistException(model=self._MODEL, object_id=object_id)  # noqa E501

    async def update(self, object_id: UUID, **values: Any) -> MODEL:
        """updates specific attributes"""
        try:
            exists = await self.get_by_id(object_id)
        except ObjectDoesNotExistException:
            return
        if exists:
            for value in values:
                setattr(exists, value, values[value])
            return exists
