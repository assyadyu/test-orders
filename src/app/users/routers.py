from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordRequestForm

from app.users.schemas import (
    LoginSchema,
    TokenSchema,
)
from app.users.services import IAuthService

auth_router = APIRouter(prefix="/auth", tags=["users"])


@auth_router.post("/token", response_model=TokenSchema)
async def get_access_token(
        request_data: OAuth2PasswordRequestForm = Depends(),
        service: IAuthService = Depends(),
):
    login = LoginSchema(username=request_data.username, password=request_data.password)
    return await service.login_user(data=login)
