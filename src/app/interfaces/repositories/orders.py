from abc import ABC, abstractmethod
from decimal import Decimal
from uuid import UUID

from app.common.enums import OrderStatus
from app.interfaces.repositories.base import IBaseRepository
from app.interfaces.repositories.base import MODEL
from app.orders.schemas import (
    NewOrderWithProductsSchema,
    UpdateOrderWithProductsSchema,
    UserData,
)


class IOrderRepository(IBaseRepository, ABC):
    """
    Interface for order repository that reflects logic specific to orders
    """

    @abstractmethod
    async def create_order_with_products(
            self,
            user: UserData,
            data: NewOrderWithProductsSchema,
    ) -> MODEL:
        """
        Create a new order with nested product objects
        :param data: request data with order data
        :param user: authenticated user data, id and is_admin
        :return: Order object
        """
        raise NotImplementedError()

    @abstractmethod
    async def get_order(
            self,
            object_id: UUID,
            user: UserData,
    ) -> MODEL:
        """
        Return order by id if is_deleted = True was not set
        :param object_id: uuid of order to retrieve
        :param user: authenticated user data, id and is_admin, admin has access to all orders, user - only to their own
        :return: Order object
        """
        raise NotImplementedError

    @abstractmethod
    async def update_order_with_products(
            self,
            object_id: UUID,
            data: UpdateOrderWithProductsSchema,
            user: UserData
    ) -> MODEL:
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
            user: UserData,
            limit: int = 10,
            offset: int = 0,
            status: OrderStatus = OrderStatus.PENDING.value,
            min_price: Decimal | None = None,
            max_price: Decimal | None = None,
            min_total: Decimal | None = None,
            max_total: Decimal | None = None,
    ) -> list[MODEL]:
        """
        Filters orders according to parameters
        :param user: authenticated user data, id and is_admin; if user is not admin,
            only orders created by this user will be filtered
        :param limit: maximum number of orders to return
        :param offset: offset of orders
        :param status: status of orders
        :param min_price: minimum price of orders
        :param max_price: maximum price of orders
        :param min_total: minimum total price of orders
        :param max_total: maximum total price of orders
        :return: filtered list of Order objects
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
