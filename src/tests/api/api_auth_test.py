import uuid

import pytest
import pytest_asyncio
from fastapi import status
from httpx import AsyncClient

from app.common import logger
from app.common.enums import OrderStatus
from app.infrastructure.repositories.fake.base import FakeBaseRepository
from app.orders.schemas import (
    NewOrderWithProductsSchema,
    UpdateOrderWithProductsSchema,
)
from tests.fixtures.users import (
    switch_to_user,
    switch_to_admin,
)


class TestAuthOrdersAPI:
    """
    E2E tests to check permissions in Orders API depending on user role performing action
    (admin can access or change any order, regular user - only those orders that belong to them)
    """
    BASE_URL: str = '/api/orders'
    test_http_client: AsyncClient
    repo: FakeBaseRepository = FakeBaseRepository()

    async def create_new_order(self):
        data = NewOrderWithProductsSchema(
            customer_name=str(uuid.uuid4()),
            products=[]
        )
        response = await self.test_http_client.post(
            url=f"{self.BASE_URL}/create",
            json=data.model_dump(),
        )
        return response.json()

    @staticmethod
    @pytest_asyncio.fixture(autouse=True, scope="class", loop_scope="session")
    async def setup(test_http_client, fake_repo):
        TestAuthOrdersAPI.test_http_client = test_http_client

    @pytest.mark.asyncio(loop_scope="session")
    async def test_auth_create_order_fail(self):
        logger.info("test_auth_create_order_fail")
        data = NewOrderWithProductsSchema(
            customer_name="customer",
            products=[]
        )
        response = await self.test_http_client.post(
            url=f"{self.BASE_URL}/create",
            json=data.model_dump(),
        )
        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    @pytest.mark.asyncio(loop_scope="session")
    async def test_auth_get_order_fail(self, auth_as_admin):
        logger.info("test_auth_update_order_fail")
        order = await self.create_new_order()
        await switch_to_user()
        response = await self.test_http_client.get(
            url=f"{self.BASE_URL}/{order['uuid']}"
        )
        assert response.status_code == status.HTTP_401_UNAUTHORIZED
        result = response.json()
        assert result["message"] == f"You don't have permission to perform this action with object id {order['uuid']}"

    #
    @pytest.mark.asyncio(loop_scope="session")
    async def test_auth_get_order_as_admin(self, auth_as_user):
        logger.info("test_auth_get_order_as_admin")
        order = await self.create_new_order()
        await switch_to_admin()
        response = await self.test_http_client.get(
            url=f"{self.BASE_URL}/{order['uuid']}"
        )
        assert response.status_code == status.HTTP_200_OK

    @pytest.mark.asyncio(loop_scope="session")
    async def test_auth_update_order_fail(self, auth_as_admin):
        logger.info("test_auth_update_order_fail")
        order = await self.create_new_order()
        await switch_to_user()
        new_status = OrderStatus.CONFIRMED.value
        upd_data = UpdateOrderWithProductsSchema(
            customer_name=order['customer_name'],
            status=new_status,
            products=[],
        )
        response = await self.test_http_client.put(
            url=f"{self.BASE_URL}/{order["uuid"]}",
            json=upd_data.model_dump(),
        )
        assert response.status_code == status.HTTP_401_UNAUTHORIZED
        result = response.json()
        assert result["message"] == f"You don't have permission to perform this action with object id {order['uuid']}"

    @pytest.mark.asyncio(loop_scope="session")
    async def test_auth_update_order_as_admin(self, auth_as_user):
        logger.info("test_auth_update_order_as_admin")
        order = await self.create_new_order()
        await switch_to_admin()
        new_status = OrderStatus.CONFIRMED.value
        upd_data = UpdateOrderWithProductsSchema(
            customer_name=order['customer_name'],
            status=new_status,
            products=[],
        )
        response = await self.test_http_client.put(
            url=f"{self.BASE_URL}/{order["uuid"]}",
            json=upd_data.model_dump(),
        )
        assert response.status_code == status.HTTP_200_OK
        result = response.json()
        assert result["status"] == new_status

    @pytest.mark.asyncio(loop_scope="session")
    async def test_auth_delete_order_fail(self, auth_as_admin):
        logger.info("test_auth_delete_order_fail")
        order = await self.create_new_order()
        await switch_to_user()
        response = await self.test_http_client.delete(
            url=f"{self.BASE_URL}/{order["uuid"]}"
        )
        assert response.status_code == status.HTTP_401_UNAUTHORIZED
        result = response.json()
        assert result["message"] == f"You don't have permission to perform this action with object id {order['uuid']}"
