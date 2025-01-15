from uuid import UUID

from decimal import Decimal

from pydantic import Field, PositiveInt

from app.common.schemas import BaseSchema


class NewProductSchema(BaseSchema):
    name: str = Field(..., max_length=100)
    price: Decimal = Field(ge=0.01, decimal_places=2)
    quantity: PositiveInt


class ProductSchema(BaseSchema):
    uuid: UUID
    name: str = Field(..., max_length=100)
    price: Decimal = Field(ge=0.01, decimal_places=2)
    quantity: PositiveInt
