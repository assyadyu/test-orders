import uuid

import pytest
import pytest_asyncio

from app.common import logger
from app.common.enums import OrderStatus
from app.common.exceptions import ObjectDoesNotExistException
from app.infrastructure.db.models import OrderModel
from app.infrastructure.repositories.fake.orders import FakeOrderRepository
from app.infrastructure.repositories.sqlalchemy import OrderRepository
from app.interfaces.repositories.base import IBaseRepository
from app.orders.schemas import UserData, NewOrderWithProductsSchema
from tests.conftest import (
    new_session,
    random_string,
)



class TestFakeOrderRepository:
    repo: FakeOrderRepository
    user: UserData
    admin: UserData

    async def create_new_order(self, user):
        data = NewOrderWithProductsSchema(
            customer_name=str(uuid.uuid4()),
            products=[]
        )
        obj = await self.repo.create_order_with_products(user, data)
        return obj

    async def clear_repo(self):
        self.repo.objects = []

    @staticmethod
    @pytest_asyncio.fixture(autouse=True, scope="class", loop_scope="session")
    async def setup():
        TestFakeOrderRepository.repo = FakeOrderRepository()
        TestFakeOrderRepository.admin = UserData(user_id=uuid.uuid4(), is_admin=True)
        TestFakeOrderRepository.user = UserData(user_id=uuid.uuid4(), is_admin=False)

    @pytest.mark.asyncio(loop_scope="session")
    async def test_auth_get_orders_as_admin(self):
        await self.clear_repo()
        logger.info("test_auth_get_orders_as_admin")
        await self.create_new_order(self.user)
        await self.create_new_order(self.admin)
        result = await self.repo.filter_orders(user=self.admin)
        assert len(result) == 2

    @pytest.mark.asyncio(loop_scope="session")
    async def test_auth_get_orders_as_user(self):
        await self.clear_repo()
        logger.info("test_auth_get_orders_as_user")
        await self.create_new_order(self.user)
        await self.create_new_order(self.admin)
        result = await self.repo.filter_orders(user=self.user)
        assert len(result) == 1


class TestOrderRepository:
    repo: IBaseRepository

    async def create_order(self) -> OrderModel:
        obj = OrderModel(
            uuid=uuid.uuid4(),
            user_id=uuid.uuid4(),
            customer_name=await random_string(15),
            status=OrderStatus.PENDING.value,
            is_deleted=False,
        )
        await self.repo.create(obj=obj)
        return obj

    @staticmethod
    @pytest_asyncio.fixture(autouse=True, scope="class", loop_scope="session")
    async def setup(prepare_test_db):
        TestOrderRepository.prepare_test_db = prepare_test_db
        TestOrderRepository.repo = OrderRepository(session=new_session())

    @pytest.mark.asyncio(loop_scope="session")
    async def test_get_by_id_fail(self):
        logger.info("OrderRepository test_get_by_id_fail")
        non_existing_id = uuid.uuid4()
        with pytest.raises(ObjectDoesNotExistException) as exception:
            await self.repo.get_by_id(object_id=non_existing_id)
        assert str(exception.value) == f"{OrderModel.__name__} object id {non_existing_id} not found"

    @pytest.mark.asyncio(loop_scope="session")
    async def test_get_by_id_success(self):
        logger.info("OrderRepository test_get_by_id_success")
        obj = await self.create_order()
        db_obj = await self.repo.get_by_id(object_id=obj.uuid)
        assert db_obj is not None
        assert db_obj.customer_name == obj.customer_name
