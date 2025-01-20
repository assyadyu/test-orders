from fastapi import (
    FastAPI,
)

from app.common.http import http_session
from app.infrastructure.adapters.http_client import http_client_adapter
from app.infrastructure.db.sessions import async_session, session_factory
from app.infrastructure.repositories.sqlalchemy import OrderRepository
from app.infrastructure.repositories.sqlalchemy.base import SQLAlchemyBaseRepository
from app.interfaces.repositories.base import IBaseRepository
from app.interfaces.repositories.orders import IOrderRepository
from app.orders.services import IOrderService, OrderService
from app.users.services import IAuthService, AuthService


def bind_dependencies(app: FastAPI, db_url: str):
    app.dependency_overrides[async_session] = session_factory(db_url)
    app.dependency_overrides[http_session] = http_client_adapter()

    app.dependency_overrides[IBaseRepository] = SQLAlchemyBaseRepository
    app.dependency_overrides[IOrderRepository] = OrderRepository

    app.dependency_overrides[IOrderService] = OrderService
    app.dependency_overrides[IAuthService] = AuthService
