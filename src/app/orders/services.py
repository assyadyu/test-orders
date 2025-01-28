from abc import ABC, abstractmethod
from uuid import UUID

from fastapi import Depends

from app.common import (
    logger,
    order_logger,
)
from app.infrastructure.db.models import OrderModel
from app.interfaces.repositories import IOrderRepository
from app.orders.schemas import (
    NewOrderWithProductsSchema,
    OrderSchema,
    UpdateOrderWithProductsSchema,
    OrderFilterSchema,
    UserData,
)


class IOrderService(ABC):
    """
    Business logic for order management (CRUD)
    """
    repo: IOrderRepository

    def __init__(self, repo: IOrderRepository = Depends()):
        self.repo = repo

    @abstractmethod
    async def create_order(self, user: UserData, data: NewOrderWithProductsSchema) \
            -> OrderSchema:
        """
        Create a new order from request data with authentication data
        :param user: user data from authentication service
        :param data: order data from request
        :return: created order (dto)
        """
        raise NotImplementedError

    @abstractmethod
    async def update_order(self, user: UserData, order_uuid: UUID, data: UpdateOrderWithProductsSchema) \
            -> OrderSchema:
        """
        Update existing order from request data with authentication data, admin can update any order,
        user - only their own
        :param user: user data from authentication service
        :param order_uuid: order uuid to be updated
        :param data: new order data from request
        :return: updated order (dto)
        """
        raise NotImplementedError

    @abstractmethod
    async def get_order(self, user: UserData, order_uuid: UUID) -> OrderSchema:
        """
        Retrieve existing order
        (which was not deleted, i.e. is_deleted is False)
        :param user: user data from authentication service,
        admin can see any order, user - only their own
        :param order_uuid: order uuid to be retrieved
        :return: order from database (dto)
        """
        raise NotImplementedError

    @abstractmethod
    async def filter_orders(self, user: UserData, filters: OrderFilterSchema) -> list[OrderSchema]:
        """
        Retrieve list of orders based on filters
        (which were not deleted, i.e. is_deleted is False)
        :param user: user data from authentication service,
        admin can see all orders, user - only their own
        :param filters: values for filters
        :return: list of orders corresponding to filters
        """
        raise NotImplementedError

    @abstractmethod
    async def delete_order(self, user: UserData, order_uuid: UUID):
        """
        Delete existing order by uuid
        :param user: user data from authentication service,
        admin can delete any order, user - only their own
        :param order_uuid: order uuid to be deleted
        :return: nothing
        """
        raise NotImplementedError


class OrderService(IOrderService):

    @staticmethod
    async def get_response_schema(obj: OrderModel) -> OrderSchema:
        """
        Convert Database Model to DTO
        :param obj: object of Model
        :return: DTO
        """
        return OrderSchema(
            uuid=obj.uuid,
            customer_name=obj.customer_name,
            user_id=obj.user_id,
            status=obj.status,
            products=obj.products if "products" in obj.__dict__ else [],
        )

    async def create_order(self, user: UserData, data: NewOrderWithProductsSchema) -> OrderSchema:
        logger.info("OrderService: create_order")
        order_logger.info(f"create_order: {user}, data: {data}")
        new_object = await self.repo.create_order_with_products(user, data)
        return await OrderService.get_response_schema(new_object)

    async def update_order(self, user: UserData, order_uuid: UUID, data: UpdateOrderWithProductsSchema) \
            -> OrderSchema:
        logger.info("OrderService: update_order")
        order_logger.info(f"update_order: {user}, order_uuid {order_uuid} data: {data}")
        upd_object = await self.repo.update_order_with_products(object_id=order_uuid, data=data, user=user)
        return await OrderService.get_response_schema(upd_object)

    async def get_order(self, user: UserData, order_uuid: UUID) -> OrderSchema:
        logger.info("OrderService: get_order")
        order_logger.info(f"get_order: {user}, order_uuid: {order_uuid}")
        obj = await self.repo.get_order(order_uuid, user)
        return await OrderService.get_response_schema(obj)

    async def filter_orders(self, user: UserData, filters: OrderFilterSchema) -> list[OrderSchema]:
        logger.info("OrderService: filter_orders")
        order_logger.info(f"filter_orders: {user}, filters: {filters}")
        objects = await self.repo.filter_orders(
            limit=filters.limit, offset=filters.offset,
            status=filters.status,
            min_price=filters.min_price, max_price=filters.max_price,
            min_total=filters.min_total, max_total=filters.max_total,
            user=user
        )
        result = []
        for obj in objects:
            result.append(await self.get_response_schema(obj))
        return result

    async def delete_order(self, user: UserData, order_uuid: UUID):
        logger.info("OrderService: delete_order")
        order_logger.info(f"delete_order: {user}, order_uuid: {order_uuid}")
        await self.repo.soft_delete(object_id=order_uuid, user=user)
