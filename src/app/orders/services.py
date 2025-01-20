from abc import ABC, abstractmethod
from uuid import UUID

from fastapi import Depends

from app.common import logger
from app.infrastructure.db.models import OrderModel
from app.interfaces.repositories import IOrderRepository
from app.orders.schemas import (
    NewOrderWithProductsSchema,
    OrderSchema,
    UpdateOrderWithProductsSchema,
    OrderFilterSchema,
    UserData,
)
from app.users.schemas import TokenPayload


class IOrderService(ABC):
    repo: IOrderRepository

    def __init__(self, repo: IOrderRepository = Depends()):
        self.repo = repo

    @abstractmethod
    async def create_order(self, user: UserData, data: NewOrderWithProductsSchema) -> None:
        raise NotImplementedError

    @abstractmethod
    async def update_order(self, user: UserData, order_uuid: UUID, data: UpdateOrderWithProductsSchema) -> OrderSchema:
        raise NotImplementedError

    @abstractmethod
    async def get_order(self, user: UserData, order_uuid: UUID) -> OrderSchema:
        raise NotImplementedError

    @abstractmethod
    async def filter_orders(self, user: UserData, filters: OrderFilterSchema) -> list[OrderSchema]:
        raise NotImplementedError

    @abstractmethod
    async def delete_order(self, user: UserData, order_uuid: UUID):
        raise NotImplementedError


class OrderService(IOrderService):

    @staticmethod
    async def get_response_schema(obj: OrderModel) -> OrderSchema:
        return OrderSchema(
            uuid=obj.uuid,
            customer_name=obj.customer_name,
            user_id=obj.user_id,
            status=obj.status,
            products=obj.products
        )

    async def create_order(self, user: UserData, data: NewOrderWithProductsSchema) -> OrderSchema:
        logger.info("OrderService: create_order")
        new_object = await self.repo.create_order_with_products(user, data)
        return await OrderService.get_response_schema(new_object)

    async def update_order(self, user: UserData, order_uuid: UUID, data: UpdateOrderWithProductsSchema) -> OrderSchema:
        logger.info("OrderService: update_order")
        upd_object = await self.repo.update_order_with_products(object_id=order_uuid, data=data, user=user)
        return await OrderService.get_response_schema(upd_object)

    async def get_order(self, user: UserData, order_uuid: UUID) -> OrderSchema:
        logger.info("OrderService: get_order")
        obj = await self.repo.get_by_id(order_uuid)
        return await OrderService.get_response_schema(obj)

    async def filter_orders(self, user: UserData, filters: OrderFilterSchema) -> list[OrderSchema]:
        logger.info("OrderService: filter_orders")
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

    async def delete_order(self, user: TokenPayload, order_uuid: UUID):
        logger.info("OrderService: delete_order")
        await self.repo.soft_delete(object_id=order_uuid, user=user)
