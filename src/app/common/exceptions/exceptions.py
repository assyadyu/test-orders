from typing import Union
from uuid import UUID

from app.infrastructure.db.models.base import BaseModel


class ApplicationBaseException(Exception):
    def __init__(self, *args):
        super().__init__(*args)


class ObjectDoesNotExistException(ApplicationBaseException):
    def __init__(self, model: BaseModel, object_id: Union[UUID, str, int]):
        msg = f"{model.__name__} object id {object_id} not found"
        super().__init__(msg)


class AuthenticationException(ApplicationBaseException):
    def __init__(self, username: str):
        msg = f"Problem occurred during authentication - {username} not found or not active"
        super().__init__(msg)


class NoPermissionException(ApplicationBaseException):
    def __init__(self, object_id: Union[UUID, str, int]):
        msg = f"You don't have permission to perform this action with object id {object_id}"
        super().__init__(msg)


class RedisConnectionException(ApplicationBaseException):
    def __init__(self):
        msg = f"Error connecting to Redis server"
        super().__init__(msg)


class AuthServiceNotAvailable(ApplicationBaseException):
    def __init__(self):
        msg = f"Auth Service Not Available"
        super().__init__(msg)