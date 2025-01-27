from decimal import Decimal
from typing import Sequence
from uuid import UUID

import sqlalchemy as sa
from sqlalchemy import func

from app.common import (
    logger,
    order_logger,
)
from app.common.enums import OrderStatus
from app.common.exceptions import (
    NoPermissionException,
    ObjectDoesNotExistException,
)
from app.infrastructure.db.models import (
    OrderModel,
    ProductModel,
)
from app.infrastructure.repositories.sqlalchemy.base import (
    SQLAlchemyBaseRepository,
    MODEL,
)
from app.interfaces.repositories.orders import IOrderRepository
from app.orders.schemas import (
    NewOrderWithProductsSchema,
    UpdateOrderWithProductsSchema,
    UserData,
)


class OrderRepository(IOrderRepository, SQLAlchemyBaseRepository):
    _MODEL: MODEL = OrderModel

    async def create_order_with_products(self, user: UserData, data: NewOrderWithProductsSchema) -> MODEL:
        logger.info("OrderRepository: Creating new order with products")
        obj = self._MODEL(
            user_id=user.user_id,
            customer_name=data.customer_name,
            status=OrderStatus.PENDING.value
        )
        for product in data.products:
            nested_obj = ProductModel(
                name=product.name,
                price=product.price,
                quantity=product.quantity,
            )
            obj.products.append(nested_obj)
        await self.create(obj)
        return obj

    async def get_order(
            self,
            object_id: UUID,
            user: UserData,
    ) -> MODEL:
        logger.info("OrderRepository: Get one order with permission check")
        stmt = sa.select(OrderModel).join(ProductModel).where(
            OrderModel.is_deleted == False,
            OrderModel.uuid == object_id)
        resp = await self.session.execute(stmt)
        obj = resp.scalar()
        if not obj:
            raise ObjectDoesNotExistException(model=self._MODEL, object_id=object_id)

        if not user.is_admin and obj.user_id != user.user_id:
            order_logger.info(f"NoPermissionException {user} object_id {object_id}")
            raise NoPermissionException(object_id)
        return obj

    async def update_order_with_products(
            self,
            object_id: UUID,
            data: UpdateOrderWithProductsSchema,
            user: UserData,
    ) -> MODEL:
        logger.info("OrderRepository: Updating existing order with products")
        upd_object = await self.get_order(object_id=object_id, user=user)

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
            user: UserData,
            limit: int = 10,
            offset: int = 0,
            status: OrderStatus = OrderStatus.PENDING.value,
            min_price: Decimal | None = None,
            max_price: Decimal | None = None,
            min_total: Decimal | None = None,
            max_total: Decimal | None = None,
    ) -> Sequence[MODEL]:
        logger.info("OrderRepository: Filtering orders")

        stmt = sa.select(
            OrderModel,
        ).join(
            ProductModel
        ).where(
            OrderModel.status == status,
            OrderModel.is_deleted == False
        )
        if not user.is_admin:
            stmt = stmt.where(
                OrderModel.user_id == user.user_id
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

    async def soft_delete(self, object_id: UUID, user: UserData) -> None:
        logger.info("OrderRepository: Changing flag of the order is_deleted to True")
        await self.get_order(object_id=object_id, user=user)
        await self.update(object_id=object_id, is_deleted=True)
