from decimal import Decimal
from itertools import product
from typing import Sequence

from pydantic import UUID4
from sqlalchemy import func
from sqlalchemy.orm import joinedload

from app.common import logger
import sqlalchemy as sa
from app.common.enums import OrderStatus
from app.common.exceptions import ObjectDoesNotExistException
from app.db.models import OrderModel, ProductModel
from app.interfaces.repositories.orders import IOrderRepository
from app.orders.schemas import NewOrderWithProductsSchema, UpdateOrderWithProductsSchema
from app.repositories.sqlalchemy.base import (
    SQLAlchemyBaseRepository,
    MODEL,
)


class OrderRepository(IOrderRepository, SQLAlchemyBaseRepository):
    _MODEL: MODEL = OrderModel

    async def create_order_with_products(self, data: NewOrderWithProductsSchema) -> _MODEL:
        logger.info("Creating new order with products")
        obj = self._MODEL(customer_name=data.customer_name, status=OrderStatus.PENDING.value)
        for product in data.products:
            nested_obj = ProductModel(
                name=product.name,
                price=product.price,
                quantity=product.quantity,
            )
            obj.products.append(nested_obj)
        await self.create(obj)
        return obj

    async def update_order_with_products(self, object_id: UUID4, data: UpdateOrderWithProductsSchema) -> _MODEL:
        logger.info("Updating existing order with products")
        upd_object = await self.get_by_id(object_id=object_id)
        upd_object.customer_name = data.customer_name
        upd_object.status = data.status
        new_products = []
        for new_product in data.products:
            new_products.append(ProductModel(
                name=new_product.name,
                price=new_product.price,
                quantity=new_product.quantity,
            ))
        upd_object.products = new_products
        self.session.add(upd_object)
        await self.session.commit()
        return upd_object

    async def filter_orders(
            self,
            limit: int,
            offset: int,
            status: OrderStatus,
            min_price: Decimal,
            max_price: Decimal,
            min_total: Decimal,
            max_total: Decimal,
    ) -> Sequence[_MODEL]:
        logger.info("Filtering orders")

        stmt = sa.select(
            OrderModel,
        ).join(
            ProductModel
        ).where(
            OrderModel.status == status,
            OrderModel.is_deleted == False
        )
        if min_price and max_price:
            stmt = stmt.where(
                ProductModel.price >= min_price,
                ProductModel.price <= max_price,
            )
        if min_total and max_total:
            stmt = stmt.group_by(
                OrderModel.uuid
            ).having(
                func.sum(ProductModel.price * ProductModel.quantity) >= min_total,
                func.sum(ProductModel.price * ProductModel.quantity) <= max_total,
            )
        stmt = stmt.limit(limit).offset(offset)
        resp = await self.session.execute(stmt)
        return resp.scalars().all()

    async def soft_delete(self, object_id: UUID4) -> None:
        await self.update(object_id=object_id, is_deleted=True)
