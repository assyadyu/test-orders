from typing import ClassVar
from uuid import uuid4

import sqlalchemy as sa
from sqlalchemy.dialects.postgresql.base import UUID

from app.db.config import Base


class UUIDMixin(Base):
    __abstract__: ClassVar[bool] = True

    uuid = sa.Column(UUID(as_uuid=True), primary_key=True, default=uuid4)


class TimeStampMixin(Base):
    __abstract__: ClassVar[bool] = True

    created_at = sa.Column(
        sa.DateTime(timezone=True), server_default=sa.func.now()
    )  # noqa: E501
    updated_at = sa.Column(sa.DateTime(timezone=True), onupdate=sa.func.now())


class BaseModel(UUIDMixin, TimeStampMixin):
    __abstract__: ClassVar[bool] = True
