from typing import Annotated
from uuid import UUID

from fastapi import (
    APIRouter,
    Depends, Query,
)
from fastapi.responses import JSONResponse

from app.orders.schemas import (
    NewOrderWithProductsSchema,
    OrderSchema, UpdateOrderWithProductsSchema, OrderFilterSchema,
)
from app.orders.services import OrderService

order_router = APIRouter(prefix="/orders", tags=["orders"])


@order_router.post("/create", response_model=OrderSchema)
async def create_order(
        request_data: NewOrderWithProductsSchema,
        service: OrderService = Depends(),
):
    return await service.create_order(request_data)


@order_router.put("/{order_uuid}", response_model=OrderSchema)
async def update_order(
        order_uuid: UUID,
        request_data: UpdateOrderWithProductsSchema,
        service: OrderService = Depends(),
):
    return await service.update_order(order_uuid, request_data)


@order_router.get("", response_model=list[OrderSchema])
async def get_orders(
        filter_query: Annotated[OrderFilterSchema, Query()],
        service: OrderService = Depends(),

):
    return await service.filter_orders(filters=filter_query)


@order_router.delete("/{order_uuid}")
async def delete_order(
        order_uuid: UUID,
        service: OrderService = Depends(),
):
    await service.delete_order(order_uuid)
    return JSONResponse(content={"message": "deleted"})
