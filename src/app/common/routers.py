from fastapi import (
    APIRouter,
    FastAPI,
)

from app.orders.routers import order_router


def bind_routers(app: FastAPI):
    router = APIRouter(prefix="/api")
    router.include_router(order_router)
    app.include_router(router=router)
