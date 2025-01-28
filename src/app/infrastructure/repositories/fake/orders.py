import uuid
from decimal import Decimal
from typing import Sequence
from uuid import UUID

from app.common import logger
from app.common.enums import OrderStatus
from app.common.exceptions import (
    NoPermissionException,
    ObjectDoesNotExistException,
)
from app.infrastructure.db.models import (
    OrderModel,
    ProductModel,
)
from app.infrastructure.repositories.fake.base import FakeBaseRepository
from app.interfaces.repositories import IOrderRepository
from app.interfaces.repositories.base import MODEL
from app.orders.schemas import (
    UserData,
    NewOrderWithProductsSchema,
    UpdateOrderWithProductsSchema,
)


class FakeOrderRepository(IOrderRepository, FakeBaseRepository):
    _MODEL: MODEL = OrderModel

    async def update_object(self, upd_object):
        for i, item in enumerate(self.objects):
            if item.uuid == upd_object.uuid:
                self.objects[i] = upd_object

    async def create_order_with_products(self, user: UserData, data: NewOrderWithProductsSchema) -> MODEL:
        logger.info("FakeOrderRepository: Creating new order with products")
        obj = self._MODEL(
            uuid=uuid.uuid4(),
            user_id=user.user_id,
            customer_name=data.customer_name,
            status=OrderStatus.PENDING.value,
            is_deleted=False,
        )
        for product in data.products:
            nested_obj = ProductModel(
                uuid=uuid.uuid4(),
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
        logger.info("FakeOrderRepository: Get one order with permission check")
        exist = [obj for obj in self.objects if obj.uuid == object_id and not obj.is_deleted]
        if not exist:
            raise ObjectDoesNotExistException(model=self._MODEL, object_id=object_id)
        obj = exist[0]
        if not user.is_admin and obj.user_id != user.user_id:
            raise NoPermissionException(object_id)
        return obj

    async def update_order_with_products(
            self,
            object_id: UUID,
            data: UpdateOrderWithProductsSchema,
            user: UserData,
    ) -> MODEL:
        logger.info("FakeOrderRepository: Updating existing order with products")
        await self.get_order(object_id=object_id, user=user)
        upd_object = self._MODEL(
            uuid=object_id,
            user_id=user.user_id,
            customer_name=data.customer_name,
            status=data.status,
            is_deleted=False,
        )
        for product in data.products:
            nested_obj = ProductModel(
                name=product.name,
                price=product.price,
                quantity=product.quantity,
            )
            upd_object.products.append(nested_obj)
        await self.update_object(upd_object)
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
        logger.info("FakeOrderRepository: Filtering orders")
        # Only by status
        return [obj for obj in self.objects
                if obj.status == status
                and not obj.is_deleted
                and (obj.user_id != user.user_id or user.is_admin) # noqa E201, E202
                ]

    async def soft_delete(self, object_id: UUID, user: UserData) -> None:
        logger.info("FakeOrderRepository: Changing flag of the order is_deleted to True")
        obj = await self.get_order(object_id=object_id, user=user)
        obj.is_deleted = True
        await self.update_object(obj)
