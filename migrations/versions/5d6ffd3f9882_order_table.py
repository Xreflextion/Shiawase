"""order table

Revision ID: 5d6ffd3f9882
Revises: 4145710159a3
Create Date: 2021-08-14 16:23:14.425092

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '5d6ffd3f9882'
down_revision = '4145710159a3'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('order',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('dish', sa.String(length=32), nullable=True),
    sa.Column('quantity', sa.Integer(), nullable=True),
    sa.Column('order_date', sa.Date(), nullable=True),
    sa.Column('delivery_date', sa.Date(), nullable=True),
    sa.Column('user_id', sa.Integer(), nullable=True),
    sa.Column('completed', sa.Boolean(), nullable=True),
    sa.ForeignKeyConstraint(['user_id'], ['user.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_order_delivery_date'), 'order', ['delivery_date'], unique=False)
    op.create_index(op.f('ix_order_order_date'), 'order', ['order_date'], unique=False)
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f('ix_order_order_date'), table_name='order')
    op.drop_index(op.f('ix_order_delivery_date'), table_name='order')
    op.drop_table('order')
    # ### end Alembic commands ###
