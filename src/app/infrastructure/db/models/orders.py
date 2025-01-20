import sqlalchemy as sa
from sqlalchemy.dialects.postgresql.base import UUID
from sqlalchemy.orm import relationship

from app.common.enums import OrderStatus
from app.infrastructure.db.models.base import BaseModel


class OrderModel(BaseModel):
    __tablename__ = "orders"

    customer_name = sa.Column(sa.String(100), nullable=False)
    status = sa.Column(sa.Enum(OrderStatus), nullable=False, default=OrderStatus.PENDING.value)
    is_deleted = sa.Column(sa.Boolean, nullable=False, default=False)
    user_id = sa.Column(UUID(as_uuid=True), nullable=False)

    products = relationship(
        "ProductModel",
        back_populates="order",
        cascade="all, delete-orphan",
        lazy='selectin'
    )
