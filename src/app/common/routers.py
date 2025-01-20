from fastapi import (
    APIRouter,
    FastAPI,
)

from app.users.routers import auth_router
from app.orders.routers import order_router


def bind_routers(app: FastAPI):
    router = APIRouter(prefix="/api")
    router.include_router(order_router)
    router.include_router(auth_router)
    app.include_router(router=router)
