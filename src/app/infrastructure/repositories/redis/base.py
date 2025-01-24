import pickle
from abc import ABC, abstractmethod
from datetime import timedelta
from typing import Any, TypeVar, Union
from uuid import UUID

from fastapi import Depends
from redis.exceptions import ConnectionError

from app.common.exceptions import (
    ObjectDoesNotExistException,
    RedisConnectionException,
)
from app.common.redis import r
from app.infrastructure.db.sessions import async_session
from app.interfaces.repositories.base import IBaseRepository

MODEL = TypeVar("MODEL")
KEY = TypeVar("KEY")


class IRedisBaseRepository(IBaseRepository, ABC):

    @abstractmethod
    async def set(self, key, obj) -> None:
        raise NotImplementedError()

    @abstractmethod
    async def set_with_expiration(self, key, obj, exp_minutes: int) -> None:
        raise NotImplementedError()

    @abstractmethod
    async def get(self, key) -> Union[MODEL, None]:
        raise NotImplementedError()


class RedisBaseRepository(IRedisBaseRepository):
    _MODEL: MODEL

    def __init__(self, *, session: async_session = Depends()):
        self.session = session

    async def set(self, key, obj) -> None:
        try:
            await r.set(key, value=pickle.dumps(obj))
        except ConnectionError:
            raise RedisConnectionException()

    async def set_with_expiration(self, key, obj, exp_minutes: int) -> None:
        try:
            await r.setex(key, timedelta(minutes=exp_minutes), value=pickle.dumps(obj))
        except ConnectionError:
            raise RedisConnectionException()

    async def get(self, key) -> Union[MODEL, None]:
        try:
            data = await r.get(key)
        except ConnectionError:
            raise RedisConnectionException
        return pickle.loads(data) if data else None

    async def create(self, obj: MODEL, **kwargs) -> None:
        """
        Saves obj under key from kwargs
        :param obj:
        :param kwargs: exp - expiration time in minutes, key - key for redis
        :return:
        """
        if "exp" in kwargs:
            await self.set_with_expiration(kwargs["key"], obj, kwargs["exp"])
        else:
            await self.set(kwargs["key"], obj)

    async def get_by_id(self, object_id: UUID) -> MODEL:
        try:
            data = await self.get(str(object_id))
        except ConnectionError:
            raise RedisConnectionException

        if data:
            return pickle.loads(data)
        else:
            raise ObjectDoesNotExistException(model=self._MODEL, object_id=object_id)

    async def update(self, object_id: Union[UUID, str], **values: Any) -> MODEL:
        result = await self.get(str(object_id))

        if not result:
            raise ObjectDoesNotExistException(model=self._MODEL, object_id=object_id)

        try:
            await self.set(str(object_id), pickle.dumps(values["value"]))
        except ConnectionError:
            raise RedisConnectionException
        return result
