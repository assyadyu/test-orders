import uuid

import pytest
import pytest_asyncio
from fastapi import status
from httpx import AsyncClient
import unittest.mock
from app.common import logger
from app.common.enums import OrderStatus
from app.interfaces.repositories import IOrderRepository
from app.orders.schemas import (
    NewOrderWithProductsSchema,
    UpdateOrderWithProductsSchema,
)
from app.common.redis import redis


class TestOrdersAPI:
    BASE_URL: str = '/api/orders'
    test_http_client: AsyncClient
    repo: IOrderRepository

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
    @pytest_asyncio.fixture(autouse=True, scope='class')
    @unittest.mock.patch("app.common.redis.redis")
    async def setup(redis, test_http_client, fake_repo):
        TestOrdersAPI.test_http_client = test_http_client
        TestOrdersAPI.repo = fake_repo
        TestOrdersAPI.redis = redis

    @pytest.mark.asyncio
    async def test_create_order_success(self, auth_as_user):
        logger.info("test_create_order_success")
        data = NewOrderWithProductsSchema(
            customer_name="customer",
            products=[]
        )
        response = await self.test_http_client.post(
            url=f"{self.BASE_URL}/create",
            json=data.model_dump(),
        )
        assert response.status_code == status.HTTP_200_OK

    @pytest.mark.asyncio
    async def test_update_order_success(self, auth_as_user):
        logger.info("test_update_order_success")
        order = await self.create_new_order()
        new_customer_name = "new_customer"
        new_status = OrderStatus.CONFIRMED.value
        upd_data = UpdateOrderWithProductsSchema(
            customer_name=new_customer_name,
            status=new_status,
            products=[],
        )
        response = await self.test_http_client.put(
            url=f"{self.BASE_URL}/{order["uuid"]}",
            json=upd_data.model_dump(),
        )
        assert response.status_code == status.HTTP_200_OK
        response = await self.test_http_client.get(
            url=f"{self.BASE_URL}/{order["uuid"]}"
        )
        upd_order = response.json()
        assert upd_order["customer_name"] == new_customer_name
        assert upd_order["status"] == new_status

    @pytest.mark.asyncio
    async def test_delete_order_success(self, auth_as_user):
        logger.info("test_delete_order_success")
        order = await self.create_new_order()
        response = await self.test_http_client.delete(
            url=f"{self.BASE_URL}/{order["uuid"]}"
        )
        assert response.status_code == status.HTTP_204_NO_CONTENT
        response = await self.test_http_client.get(
            url=f"{self.BASE_URL}/{order["uuid"]}"
        )
        assert response.status_code == status.HTTP_404_NOT_FOUND

    @pytest.mark.asyncio
    async def test_get_order_fail(self, auth_as_user):
        logger.info("test_get_order_fail")
        response = await self.test_http_client.get(
            url=f"{self.BASE_URL}/{uuid.uuid4()}"
        )
        assert response.status_code == status.HTTP_404_NOT_FOUND
