from typing import Any, TypeVar, Sequence
from uuid import UUID

import sqlalchemy as sa
from fastapi import Depends
from pydantic import BaseModel, UUID4
from sqlalchemy.ext.asyncio import AsyncSession

from app.common.exceptions import ObjectDoesNotExistException
from app.db.sessions import async_session
from app.interfaces.repositories.base import IBaseRepository

MODEL = TypeVar("MODEL")
KEY = TypeVar("KEY")


class SQLAlchemyBaseRepository(IBaseRepository):
    session: AsyncSession
    _MODEL: MODEL

    def __init__(self, *, session: async_session = Depends()):
        self.session = session

    async def set_model(self, model: MODEL) -> None:
        self._MODEL = model

    async def create(self, obj: MODEL) -> MODEL:
        self.session.add(obj)
        await self.session.commit()
        return obj

    async def create_from_data(self, data: BaseModel) -> MODEL:
        obj = self._MODEL(**data.model_dump(exclude_none=True))
        return await self.create(obj=obj)

    async def object_exists_by_name(self, *, name: str) -> bool:
        if hasattr(self._MODEL, "name"):
            stmt = sa.select(self._MODEL).filter_by(name=name)
            resp = await self.session.execute(stmt)
            return resp.first() is not None
        return False

    async def get_by_id(self, *, object_id: UUID4) -> MODEL:
        stmt = sa.select(self._MODEL).filter_by(uuid=object_id)
        resp = await self.session.execute(stmt)
        if resp.scalar():
            return resp.scalar()
        else:
            raise ObjectDoesNotExistException(model=self._MODEL, object_id=object_id)

    async def update(self, object_id: UUID, **values: Any) -> MODEL:
        stmt = sa.update(self._MODEL)
        stmt = stmt.filter_by(uuid=object_id)
        stmt = stmt.values(values).returning(self._MODEL)
        result = (await self.session.execute(stmt)).scalar()
        if not result:
            raise ObjectDoesNotExistException(model=self._MODEL, object_id=object_id)
        await self.session.commit()

        return result

    async def delete(self, *, object_id: UUID) -> Sequence[int | UUID]:
        stmt = sa.delete(self._MODEL)
        stmt = stmt.where(self._MODEL.uuid == object_id).returning(self._MODEL.uuid)
        deleted_id = (await self.session.execute(stmt)).scalars().all()

        if not deleted_id:
            raise ObjectDoesNotExistException(
                model=self._MODEL, object_id=object_id
            )  # noqa: E501

        await self.session.commit()
        return deleted_id
