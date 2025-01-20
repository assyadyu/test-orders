from abc import ABC, abstractmethod
from decimal import Decimal
from uuid import UUID

from app.common.enums import OrderStatus
from app.infrastructure.db.models import OrderModel
from app.interfaces.repositories.base import IBaseRepository
from app.orders.schemas import (
    NewOrderWithProductsSchema,
    UpdateOrderWithProductsSchema,
    UserData,
)


class IOrderRepository(IBaseRepository, ABC):

    @abstractmethod
    async def create_order_with_products(
            self,
            user: UserData,
            data: NewOrderWithProductsSchema,
    ) -> OrderModel:
        """
        Creates a new order with nested product objects
        :param data: request data with order data
        :param user: authenticated user data, id and is_admin
        :return: Order object
        """
        raise NotImplementedError()

    @abstractmethod
    async def update_order_with_products(
            self,
            object_id: UUID,
            data: UpdateOrderWithProductsSchema,
            user: UserData
    ) -> OrderModel:
        """
        Replaces existing order with nested product objects
        :param object_id: uuid of order
        :param data: request data with new order data
        :param user: authenticated user data, id and is_admin
        :return: updated Order object
        """
        raise NotImplementedError()

    @abstractmethod
    async def filter_orders(
            self,
            limit: int,
            offset: int,
            status: OrderStatus,
            min_price: Decimal,
            max_price: Decimal,
            min_total: Decimal,
            max_total: Decimal,
            user: UserData,
    ) -> list[OrderModel]:
        """
        Filters orders according to parameters
        :param user: authenticated user data, id and is_admin
        :return: list of Order objects
        """
        raise NotImplementedError

    @abstractmethod
    async def soft_delete(
            self,
            object_id: UUID,
            user: UserData,
    ) -> None:
        """
        Sets flag is_deleted to True
        :param object_id: uuid of the order to be deleted
        :param user: authenticated user data, id and is_admin
        :return: nothing
        """
        raise NotImplementedError
