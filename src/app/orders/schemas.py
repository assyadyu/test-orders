from decimal import Decimal
from typing import Optional
from uuid import UUID

from pydantic import computed_field, Field

from app.common.enums import OrderStatus
from app.common.schemas import BaseSchema
from app.products.schemas import (
    NewProductSchema,
    ProductSchema,
)


class NewOrderWithProductsSchema(BaseSchema):
    customer_name: str
    products: Optional[list[NewProductSchema]]


class UpdateOrderWithProductsSchema(BaseSchema):
    status: OrderStatus
    customer_name: str
    products: list[NewProductSchema]


class OrderSchema(BaseSchema):
    uuid: UUID
    status: OrderStatus
    customer_name: str
    user_id: UUID
    products: Optional[list[ProductSchema]]

    @computed_field
    @property
    def total_price(self) -> Decimal:
        total = 0
        if self.products:
            total = sum(product.quantity * product.price for product in self.products)
        return Decimal(total)


class OrderFilterSchema(BaseSchema):
    limit: int = Field(20, gt=0, le=100)
    offset: int = Field(0, ge=0)
    status: OrderStatus
    min_price: Optional[Decimal] = None
    max_price: Optional[Decimal] = None
    min_total: Optional[Decimal] = None
    max_total: Optional[Decimal] = None


class UserData(BaseSchema):
    user_id: UUID
    is_admin: bool
