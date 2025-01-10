from fastapi import (
    APIRouter,
    FastAPI,
)


def bind_routers(app: FastAPI):
    router = APIRouter(prefix="/api")
    app.include_router(router=router)
