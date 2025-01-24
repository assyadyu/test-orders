import uuid
from decimal import Decimal

import pytest
from sqlalchemy.testing.pickleable import Order

from app.common import logger
from app.common.enums import OrderStatus
from app.orders.schemas import OrderSchema
from app.products.schemas import ProductSchema
from tests.conftest import random_string


class TestOrderSchema:
    schema: OrderSchema

    @pytest.mark.asyncio(loop_scope="session")
    async def test_order_total(self):
        logger.info("test_order_total")
        product_price, product_quantity = 10, 5
        order = OrderSchema(
            uuid=uuid.uuid4(),
            status=OrderStatus.PENDING.value,
            customer_name=await random_string(15),
            user_id=uuid.uuid4(),
            products=[
                ProductSchema(
                    uuid=uuid.uuid4(),
                    name=await random_string(10),
                    price=Decimal(product_price),
                    quantity=product_quantity
                )
            ]
        )
        assert order.total_price == product_price * product_quantity
