import asyncio
import random
import string
from os import environ
from typing import Generator

import pytest_asyncio
from dotenv import load_dotenv
from httpx import AsyncClient, ASGITransport

from app.common import logger, settings
from app.infrastructure.adapters import http_client
from app.infrastructure.db.config import Base
from app.infrastructure.db.sessions import async_engine, async_session
from app.infrastructure.repositories.fake.orders import FakeOrderRepository
from app.infrastructure.repositories.sqlalchemy import OrderRepository
from app.interfaces.repositories import IOrderRepository
from app.main import app

load_dotenv()
settings.PG_DB = environ.get("POSTGRES_DB")
settings.PG_HOST = environ.get("POSTGRES_HOST")
settings.PG_USER = environ.get("POSTGRES_USER")
settings.PG_PASSWORD = environ.get("POSTGRES_PASSWORD")
settings.REDIS_PORT = environ.get("REDIS_PORT")
settings.REDIS_PORT = environ.get("REDIS_PORT")

test_engine = async_engine(settings.db_url)
new_session = async_session(test_engine)

pytest_plugins = [
    "tests.fixtures.users",
]


@pytest_asyncio.fixture(scope="session")
async def event_loop(request) -> Generator:
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()


@pytest_asyncio.fixture(scope="session", loop_scope="session")
def fake_repo():
    app.dependency_overrides[IOrderRepository] = FakeOrderRepository
    yield
    app.dependency_overrides[IOrderRepository] = OrderRepository


def override_async_session():
    logger.info("test session created")
    yield new_session()


@pytest_asyncio.fixture(scope="session", autouse=False, loop_scope="session")
async def test_http_client() -> AsyncClient:
    async with AsyncClient(transport=ASGITransport(app=app), base_url='http://test') as client:
        yield client


app.dependency_overrides[async_session] = override_async_session
app.dependency_overrides[http_client] = test_http_client


@pytest_asyncio.fixture(autouse=False, scope="class")
async def prepare_test_db():
    logger.warning("prepare_test_db")
    logger.warning("CREATE TABLES")
    async with test_engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    await test_engine.dispose()

    yield
    logger.warning("DROP TABLES")
    await test_engine.dispose()
    async with test_engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
    await test_engine.dispose()


async def random_string(length: int = 10) -> str:
    letters = string.ascii_lowercase
    return ''.join(random.choice(letters) for _ in range(length))
