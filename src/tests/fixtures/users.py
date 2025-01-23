import uuid

import pytest_asyncio

from app.common.enums import UserRoleEnum
from app.main import app
from app.users.schemas import TokenPayload
from app.users.services import get_current_user


async def get_fake_current_user(user_uuid=str(uuid.uuid4())):
    return TokenPayload(uuid=user_uuid, username="user",
                        role=UserRoleEnum.USER.value, is_active=True)


async def get_fake_current_admin(admin_uuid=str(uuid.uuid4())):
    return TokenPayload(uuid=str(admin_uuid), username="admin",
                        role=UserRoleEnum.ADMIN.value, is_active=True)


async def switch_to_user():
    app.dependency_overrides[get_current_user] = get_fake_current_user
    # yield
    # app.dependency_overrides[get_current_user] = get_current_user


async def switch_to_admin():
    app.dependency_overrides[get_current_user] = get_fake_current_admin
    # yield
    # app.dependency_overrides[get_current_user] = get_current_user


@pytest_asyncio.fixture(scope="module", loop_scope="session")
async def auth_as_admin():
    await switch_to_admin()


@pytest_asyncio.fixture(scope="module", loop_scope="session")
async def auth_as_user():
    await switch_to_user()
