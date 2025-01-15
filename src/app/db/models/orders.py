import sqlalchemy as sa

from app.common.enums import OrderStatus
from app.db.models.base import BaseModel
from sqlalchemy.orm import relationship


class OrderModel(BaseModel):
    __tablename__ = "orders"

    customer_name = sa.Column(sa.String(100), nullable=False)
    status = sa.Column(sa.Enum(OrderStatus), nullable=False, default=OrderStatus.PENDING.value)
    is_deleted = sa.Column(sa.Boolean, nullable=False, default=False)

    products = relationship(
        "ProductModel",
        back_populates="order",
        cascade="all, delete-orphan",
        lazy='selectin'
    )
