"""product_and_order_models

Revision ID: 89a9cea0ef73
Revises: -
Create Date: 2025-01-14 14:23:17.599483

"""
from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op

from app.common.enums import OrderStatus

# revision identifiers, used by Alembic.
revision: str = '89a9cea0ef73'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table(
        'orders',
        sa.Column('customer_name', sa.String(length=100), nullable=False),
        sa.Column('status', sa.Enum(OrderStatus, name='orderstatus'), nullable=False),
        sa.Column('is_deleted', sa.Boolean(), nullable=False),
        sa.Column('uuid', sa.UUID(), nullable=False),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=True),
        sa.Column('updated_at', sa.DateTime(timezone=True), nullable=True),
        sa.PrimaryKeyConstraint('uuid')
    )
    op.create_table(
        'products',
        sa.Column('name', sa.String(length=150), nullable=False),
        sa.Column('price', sa.DECIMAL(precision=10, scale=2), nullable=False),
        sa.Column('quantity', sa.Integer(), nullable=False),
        sa.Column('order_uuid', sa.UUID(), nullable=True),
        sa.Column('uuid', sa.UUID(), nullable=False),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=True),
        sa.Column('updated_at', sa.DateTime(timezone=True), nullable=True),
        sa.CheckConstraint('price > 0'),
        sa.CheckConstraint('quantity > 0'),
        sa.ForeignKeyConstraint(['order_uuid'], ['orders.uuid'], ondelete='CASCADE'),
        sa.PrimaryKeyConstraint('uuid')
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('products')
    op.drop_table('orders')
    op.execute("DROP TYPE orderstatus")
    # ### end Alembic commands ###
