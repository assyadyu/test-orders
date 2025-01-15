from abc import ABC
from decimal import Decimal
from uuid import UUID

from fastapi import Depends

from app.common import logger
from app.common.enums import OrderStatus
from app.db.models import OrderModel
from app.orders.schemas import (
    NewOrderWithProductsSchema,
    OrderSchema, UpdateOrderWithProductsSchema, OrderFilterSchema,
)
from app.interfaces.repositories import IOrderRepository


class IOrderService(ABC):
    repo: IOrderRepository

    def __init__(self, repo: IOrderRepository = Depends()):
        self.repo = repo

    async def create_order(self, data: NewOrderWithProductsSchema) -> None:
        raise NotImplementedError


class OrderService(IOrderService):

    @staticmethod
    async def get_response_schema(obj: OrderModel) -> OrderSchema:
        return OrderSchema(
            uuid=obj.uuid, customer_name=obj.customer_name, status=obj.status, products=obj.products
        )

    async def create_order(self, data: NewOrderWithProductsSchema) -> OrderSchema:
        logger.info("OrderService: create_order")
        new_object = await self.repo.create_order_with_products(data)
        return await OrderService.get_response_schema(new_object)

    async def update_order(self, order_uuid: UUID, data: UpdateOrderWithProductsSchema) -> OrderSchema:
        logger.info("OrderService: update_order")
        upd_object = await self.repo.update_order_with_products(object_id=order_uuid, data=data)
        return await OrderService.get_response_schema(upd_object)

    async def delete_order(self, order_uuid: UUID):
        logger.info("OrderService: delete_order")
        await self.repo.soft_delete(object_id=order_uuid)

    async def filter_orders(self, filters: OrderFilterSchema) -> list[OrderSchema]:
        logger.info("OrderService: filter_orders")
        objs = await self.repo.filter_orders(
            limit=filters.limit, offset=filters.offset,
            status=filters.status,
            min_price=filters.min_price, max_price=filters.max_price,
            min_total=filters.min_total, max_total=filters.max_total,
        )
        result = []
        for obj in objs:
            result.append(await self.get_response_schema(obj))
        return result