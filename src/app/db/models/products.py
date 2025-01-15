import sqlalchemy as sa
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import UUID

from app.db.models.base import BaseModel


class ProductModel(BaseModel):
    __tablename__ = "products"

    name = sa.Column(sa.String(150), nullable=False)
    price = sa.Column(sa.DECIMAL(10, 2), nullable=False)
    quantity = sa.Column(sa.Integer, nullable=False)
    order_uuid = sa.Column(UUID(as_uuid=True), sa.ForeignKey("orders.uuid", ondelete="CASCADE"))
    order = relationship("OrderModel", back_populates="products", uselist=False)

    __table_args__ = (
        sa.CheckConstraint('quantity > 0'),
        sa.CheckConstraint('price > 0'),
    )
