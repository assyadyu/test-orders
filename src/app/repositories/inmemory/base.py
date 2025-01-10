from typing import Any, TypeVar, Union
from uuid import UUID, uuid4

from pydantic import BaseModel, UUID4

from app.common.exceptions import ObjectDoesNotExistException
from app.interfaces.repositories.base import IBaseRepository

MODEL = TypeVar("MODEL")
KEY = TypeVar("KEY")


class InMemoryBaseRepository(IBaseRepository):
    objects: list[MODEL]
    _MODEL: MODEL

    def __init__(self):
        self.objects = []

    async def set_model(self, model: MODEL) -> None:
        self._MODEL = model

    async def create(self, obj: MODEL) -> MODEL:
        obj.uuid = uuid4()
        self.objects.append(obj)
        return obj

    async def create_from_data(self, data: BaseModel) -> MODEL:
        obj = self._MODEL(**data.model_dump(exclude_none=True))
        return await self.create(obj=obj)

    async def object_exists_by_name(self, name: str) -> bool:
        if hasattr(self._MODEL, "name"):
            return any(obj.name == name for obj in self.objects)
        return False

    async def get_by_id(self, object_id: UUID4) -> MODEL:
        exist = [obj for obj in self.objects if obj.uuid == object_id]
        if exist:
            return exist[0]
        else:
            raise ObjectDoesNotExistException(model=self._MODEL, object_id=object_id)

    async def update(self, object_id: UUID4, **values: Any) -> MODEL:
        try:
            exists = await self.get_by_id(object_id)
        except ObjectDoesNotExistException:
            return
        if exists:
            for value in values:
                setattr(exists, value, values[value])
            return exists

    async def delete(self, object_id: UUID) -> Union[UUID | None]:
        try:
            exists = await self.get_by_id(object_id)
        except ObjectDoesNotExistException:
            return
        if exists:
            self.objects.remove(exists)
            return object_id
