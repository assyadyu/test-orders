import uuid
from uuid import uuid4

import pytest
import pytest_asyncio

from app.common import logger
from app.common.enums import OrderStatus
from app.common.exceptions import ObjectDoesNotExistException
from app.infrastructure.db.models import OrderModel
from app.infrastructure.repositories.sqlalchemy import OrderRepository
from app.interfaces.repositories.base import IBaseRepository
from tests.conftest import (
    new_session,
    random_string,
)


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
        non_existing_id = uuid4()
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
