from app.common.enums import UserRoleEnum
from app.common.schemas import BaseSchema


class LoginSchema(BaseSchema):
    username: str
    password: str


class TokenSchema(BaseSchema):
    access_token: str
    token_type: str


class TokenPayload(BaseSchema):
    uuid: str
    username: str
    role: UserRoleEnum
    is_active: bool
