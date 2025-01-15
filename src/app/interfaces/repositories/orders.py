from abc import ABC, abstractmethod
from decimal import Decimal

from pydantic import UUID4

from app.common.enums import OrderStatus
from app.orders.schemas import NewOrderWithProductsSchema, UpdateOrderWithProductsSchema
from app.db.models.orders import OrderModel

from app.interfaces.repositories.base import IBaseRepository


class IOrderRepository(IBaseRepository, ABC):

    @abstractmethod
    async def create_order_with_products(self, data: NewOrderWithProductsSchema) -> OrderModel:
        """
        Creates a new order with nested product objects
        :param data: request data with order data
        :return: Order object
        """
        raise NotImplementedError()

    @abstractmethod
    async def update_order_with_products(self, object_id: UUID4, data: UpdateOrderWithProductsSchema) -> OrderModel:
        """
        Replaces existing order with nested product objects
        :param object_id: uuid of order
        :param data: request data with new order data
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
    ) -> list[OrderModel]:
        """
        Filters orders according to parameters
        :return: list of Order objects
        """
        raise NotImplementedError

    @abstractmethod
    async def soft_delete(self, *, object_id: UUID4) -> None:
        """
        Sets flag is_deleted to True
        :param object_id: uuid of the order to be deleted
        :return: nothing
        """
        raise NotImplementedError