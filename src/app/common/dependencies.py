from fastapi import (
    FastAPI,
)

from app.db.sessions import (
    async_session,
    session_factory,
)
from app.interfaces.repositories.base import IBaseRepository
from app.interfaces.repositories.orders import IOrderRepository
from app.orders.services import OrderService, IOrderService
from app.repositories.sqlalchemy import OrderRepository
from app.repositories.sqlalchemy.base import SQLAlchemyBaseRepository


def bind_dependencies(app: FastAPI, db_url: str):
    app.dependency_overrides[async_session] = session_factory(db_url)

    app.dependency_overrides[IBaseRepository] = SQLAlchemyBaseRepository
    app.dependency_overrides[IOrderRepository] = OrderRepository

    app.dependency_overrides[IOrderService] = OrderService
