from typing import Annotated
from uuid import UUID

from fastapi import (
    APIRouter,
    Depends,
    Query,
)
from starlette import status
from starlette.responses import Response

from app.orders.cache import order_cache
from app.orders.schemas import (
    NewOrderWithProductsSchema,
    OrderSchema,
    UpdateOrderWithProductsSchema,
    OrderFilterSchema,
    UserData,
)
from app.orders.services import IOrderService
from app.users.services import get_current_active_user

order_router = APIRouter(prefix="/orders", tags=["orders"])


@order_router.post("/create", response_model=OrderSchema)
async def create_order(
        user: Annotated[UserData, Depends(get_current_active_user)],
        request_data: NewOrderWithProductsSchema,
        service: IOrderService = Depends(),
):
    return await service.create_order(user, request_data)


@order_router.put("/{order_uuid}", response_model=OrderSchema)
@order_cache(update=True)
async def update_order(
        user: Annotated[UserData, Depends(get_current_active_user)],
        order_uuid: UUID,
        request_data: UpdateOrderWithProductsSchema,
        service: IOrderService = Depends(),
):
    return await service.update_order(user, order_uuid, request_data)


@order_router.get("/{order_uuid}", response_model=OrderSchema)
@order_cache()
async def get_order(
        user: Annotated[UserData, Depends(get_current_active_user)],
        order_uuid: UUID,
        service: IOrderService = Depends(),
):
    return await service.get_order(user, order_uuid)


@order_router.get("", response_model=list[OrderSchema])
@order_cache(expiration=30)
async def get_orders(
        user: Annotated[UserData, Depends(get_current_active_user)],
        filter_query: Annotated[OrderFilterSchema, Query()],
        service: IOrderService = Depends(),
):
    return await service.filter_orders(user, filters=filter_query)


@order_router.delete("/{order_uuid}")
@order_cache(delete=True)
async def delete_order(
        user: Annotated[UserData, Depends(get_current_active_user)],
        order_uuid: UUID,
        service: IOrderService = Depends(),
):
    await service.delete_order(user, order_uuid)
    return Response(status_code=status.HTTP_204_NO_CONTENT)
