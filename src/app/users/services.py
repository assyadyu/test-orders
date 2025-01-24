from abc import ABC, abstractmethod
from typing import Annotated
from uuid import UUID

from fastapi import Depends
from httpx import AsyncClient, Response

from app.common import logger, settings
from app.common.enums import UserRoleEnum
from app.common.exceptions import AuthenticationException
from app.common.http import http_session
from app.common.settings import oauth2_scheme
from app.interfaces.repositories.users import IUserRepository
from app.orders.schemas import UserData
from app.users.schemas import (
    LoginSchema,
    TokenSchema,
    TokenPayload,
)


async def get_current_user(
        token: Annotated[str, Depends(oauth2_scheme)],
        repo: IUserRepository = Depends()
) -> TokenPayload:
    return await repo.get(token)


async def get_current_active_user(
        current_user: Annotated[TokenPayload, Depends(get_current_user)],
) -> UserData:
    if not current_user.is_active:
        raise AuthenticationException(username=current_user.username)
    is_admin = current_user.role == UserRoleEnum.ADMIN.value
    return UserData(user_id=UUID(current_user.uuid), is_admin=is_admin)


class IAuthService(ABC):
    http_client: AsyncClient
    repo: IUserRepository
    url: str = settings.AUTH_URL

    def __init__(self, http_client: http_session = Depends(), repo: IUserRepository = Depends()):
        self.http_client = http_client
        self.repo = repo

    @abstractmethod
    async def login_user(self, data: LoginSchema) -> TokenSchema:
        raise NotImplementedError

    @abstractmethod
    async def validate_token(self, data: TokenSchema) -> TokenPayload:
        raise NotImplementedError


class AuthService(IAuthService):

    async def request_data(self, url, payload) -> Response:
        return await self.http_client.post(url, json=payload.dict())

    async def validate_token(self, data: TokenSchema) -> None:
        logger.info("AuthService: validate_token and save to cache")
        response = await self.request_data(url=f'{self.url}/validate', payload=data)
        logger.info(f"validate_token: {response.json()}")
        if response.status_code != 200:
            logger.error(f'AuthService: validate_token failed: {response}')
        else:
            logger.info(f'AuthService: {response.json()}')
            await self.repo.create(TokenPayload(**response.json()), key=data.access_token)

    async def login_user(self, data: LoginSchema) -> TokenSchema:
        logger.info("AuthService: login_user")
        response = await self.request_data(url=f'{self.url}/signin', payload=data)
        if response.status_code != 200:
            raise AuthenticationException(username=data.username)

        result = TokenSchema(**response.json())
        # TODO move to queue ?
        await self.validate_token(result)
        return result
